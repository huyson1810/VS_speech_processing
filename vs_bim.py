import ctypes
import tkinter
from tkinter import *
from tkinter.ttk import Style

from gtts import gTTS
import datetime
import speech_recognition as sr
import webbrowser
import os
import random
import smtplib
import requests
import json
import playsound
import threading
import bs4, requests
import sys
import subprocess
from local_time import *
from browser import *
# from weather import *
from youtube import *
# from wakeup import *
from wiki import *
from vietnam_news import *
# from game import *
from PIL import ImageTk, Image

numbers = {'hundred': 100, 'thousand': 1000, 'lakh': 100000}
a = {'name': 'your email'}

window = Tk()
# window = Toplevel()
window.title('My Virtual Assistant - Bim Bim')

global var
global var1

var = StringVar()
var1 = StringVar()


def speak(text, filename='voice.mp3'):
    os.remove(filename)
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
    threading.Thread(target=playsound.playsound, args=(filename,)).start()


def asynchronous_speak(text, filename='voice.mp3'):
    os.remove(filename)
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
    playsound.playsound(filename)


def takeCommand():
    r = sr.Recognizer()
    query = ""
    with sr.Microphone() as source:
        var.set("Bim Bim đang lắng nghe bạn...")
        # window.update()
        print("Listening...")
        audio = r.adjust_for_ambient_noise(source,
                                           duration=0.5)  # listen 0.5s for recognizing noise , listen for 0.5 second to calibrate the energy threshold for ambient noise levels
        audio = r.listen(source, timeout=7, phrase_time_limit=10)
        try:
            var.set("Bim Bim đang nhận diện ...")
            # window.update()
            print("Recognizing...")
            query = r.recognize_google(audio, language='vi-VN')
        except Exception as e:
            print('exception in google recognizing ...')
            return "None"
    var1.set("User: " + query)
    # window.update()
    return query


# frames_count = 62
# frames = [PhotoImage(file='virtual_ass.gif', format='gif -index %i' % (i)) for i in range(frames_count)]

# id = 77 to start hello
# frames = [PhotoImage(file='Assistant.gif', format='gif -index %i' % (i)) for i in range(1, 100)]

# Create a photoimage object of the image in the path
# image1 = Image.open("./siri/ass_2.gif")
# test = ImageTk.PhotoImage(image1)
# print(image1.n_frames)
# label_test = tkinter.Label(image=test)
# label_test.image = test

frames_count = 62
frames = [PhotoImage(file="siri/virtual_ass.gif", format=f"gif -index {i}") for i in range(frames_count)]


def get_user_name():
    if not os.path.exists("name.txt"):
        return ""
    file = open("name.txt", "r")
    content = file.readline()
    content = content.strip()
    file.close()
    return content


user_name = get_user_name()

# ind = 0

# def update():
#     global ind
#     if ind == 70:
#         ind = 0
#     frame = frames[ind]
#     ind = (ind + 1) % len(frames)
#     # print(ind)
#     label.configure(image=frame)
#     window.after(30, update)

# count_ = 0
anim = None


def update(count_):
    global anim
    frame = frames[count_]
    # label.configure(image=frame)

    canvas.create_image(0, 0, image=frame, anchor=NW)
    count_ += 1
    if count_ >= frames_count:
        count_ = 0

    anim = window.after(10, lambda: update(count_))


# task function:
def hello():
    global user_name
    var.set(f"Xin chào bạn, tôi là Bim Bim trợ lý ảo của bạn.")
    # window.update()
    global ind
    ind = 77
    if user_name == "":
        var.set("Xin chào bạn, tôi là Bim Bim trợ lý ảo của bạn. \n"
                "Hãy giới thiệu tên để Bim Bim có thể giao tiếp và hỗ trợ bạn nhé.")
        speak(
            "Xin chào bạn, tôi là Bim Bim trợ lý ảo của bạn. Hãy giới thiệu tên để Bim Bim có thể giao tiếp và hỗ trợ bạn nhé.")
    else:
        var.set(f"Chúc {user_name} một ngày tốt lành! Bây giờ Bim Bim có thể giúp gì cho bạn nào?.")
        speak(f"Chúc {user_name} một ngày tốt lành! Bây giờ Bim Bim có thể giúp gì cho bạn nào")


def show_name(name):
    global user_name
    user_name = name
    # Add name
    file = open("name.txt", "w", encoding='utf-8')
    file.write(user_name)
    file.close()
    # Run hello again:
    hello()


def goodbye():
    var.set(f"Tạm biệt {user_name}")
    btn1.configure(bg='SlateBlue4')
    # btn2['state'] = 'normal'
    # window.update()
    global ind
    ind = 77
    speak(f"tạm biệt {user_name}. hẹn gặp lại lần sau nhé.")
    file = open("name.txt", "r+")
    file.truncate(0)
    file.close()


def get_weather(text):
    # Enter your API key here 
    api_key = "4aab97e9a184c620fba4f7f1c7ae3959"

    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name 
    if 'hà nội' in text:
        city_name = "hanoi"
    elif 'đà nẵng' in text:
        city_name = 'danang'
    elif 'huế' in text:
        city_name = 'hue'

    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric" + "&lang=vi"
    response = requests.get(complete_url)
    x = response.json()
    city = x["name"]
    descr = x["weather"][0]["description"]
    temp = x["main"]["temp_min"]
    humid = x["main"]["humidity"]
    pressure = x["main"]["pressure"]
    wind = x['wind']['speed']
    content = f"Dự đoán thời tiết {city} trời {descr}.Nhiệt độ thấp nhất:{temp} độ.Tốc độ gió:{wind} km/h.Áp suất khí quyển:{pressure} Pascal và độ ẩm {humid} phần trăm."
    return content


#
def respond_to_user(ans: str):
    var.set(ans)
    # window.update()
    speak(ans)


def respond_to_user_asynchronous(ans: str):
    var.set(ans)
    # window.update()
    asynchronous_speak(ans)


def open_application(text):
    if "word" in text:
        speak("Mở Microsoft Word")
        os.startfile('C:\Program Files\Microsoft Office\\root\Office16\\WINWORD.EXE')
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        os.startfile('C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE')
    elif "tele" in text:
        os.startfile("C:\\Users\Lenovo\AppData\Roaming\Telegram Desktop\Telegram.exe")
    elif "postman" in text:
        os.startfile("C:\\Users\Lenovo\AppData\Local\Postman\Postman.exe")
    else:
        var.set(f"Ứng dụng chưa tìm thấy. {user_name} hãy thử lại nhé!")
        speak(f"Ứng dụng chưa tìm thấy. {user_name} hãy thử lại nhé!")


def send_email():
    recipient = takeCommand().lower()
    if "gmail" in recipient:
        recipient.replace(' a còng ','@')
        speak('Nội dung bạn muốn gửi là gì')
        content = takeCommand().lower()
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('huyson.scientist@gmail.com', 'mobu1608')
        mail.sendmail('huyson.scientist@gmail.com',
                      recipient, content.encode('utf-8'))
        mail.close()
        speak('Email của bạn vùa được gửi. Hãy kiểm tra lại đề phòng sai sót nha.')

def get_mail():
    recipient = takeCommand().lower()
    recipient.replace(' a còng ', '@')
    return recipient

# activate
def _play():
    # btn2['state'] = 'disabled'
    btn1.configure(bg='SlateBlue4')

    text = takeCommand().lower()
    # text = "hôm nay có tin tức gì  ?"

    tem1, _ = get_news(text)
    # tem2, ans2 = play_hangman(text)

    if 'tìm kiếm youtube' in text:
        end_speech = search_youtube(text)
        respond_to_user(end_speech)
    #
    # elif 'dự báo' in text:
    #     current_weather()

    elif 'ứng dụng' in text:
        open_application(text)

    elif 'tìm kiếm google' in text:
        end_speech = search_google(text)
        respond_to_user(end_speech)
    # bật video trên youtube
    elif 'mở trên youtube' in text:
        end_speech = play(text)
        respond_to_user(end_speech)

    # elif tem2 != "false":  # choi game
    #     respond_to_user(ans2)
    elif 'tạm biệt' in text:
        goodbye()
        window.destroy()

    # elif 'thức dậy' in text:
    #     best_time = get_wakeup_time()
    #     var.set(f"{best_time[0].hour}:{best_time[0].minute} hoặc {best_time[1].hour}:{best_time[1].minute}")
    #     # window.update()
    #     speak(
    #         f"Bạn nên dậy vào {best_time[0].hour} giờ {best_time[0].minute} phút hoặc {best_time[1].hour} giờ {best_time[1].minute} phút")

    elif get_location(text) != "false":
        respond_to_user("" + get_location(text))

    elif get_day(text) != "false":
        respond_to_user("" + get_day(text))

    elif get_time(text) != "false":
        respond_to_user("" + get_time(text))

    elif tem1 != "false":  # get news
        _, news_list = get_news(text)
        for i in range(len(news_list)):
            ans = news_list[i]
            respond_to_user_asynchronous(ans)
        # break    
    elif 'xin chào' in text:
        hello()
    elif 'tên của tôi là' in text:
        id_end = text.find("tên của tôi là") + len("tên của tôi là ")
        show_name(text[id_end:])
    elif 'thời tiết' in text:
        weather_description = get_weather(text)
        respond_to_user(weather_description)
        # open browser
    elif 'mở trình duyệt' in text:
        end_speech = open_browser()
        respond_to_user("Trình duyệt đang được mở")

    elif 'máy ảnh' in text:
        var.set("Mở máy ảnh")
        # window.update()
        subprocess.run('start microsoft.windows.camera:', shell=True)
        speak('Mở máy ảnh')

    elif 'là ai' in text or 'là gì' in text:
        end_speech = answer_wiki(text)
        respond_to_user(end_speech)

    elif 'định nghĩa' in text:
        pos = text.find('định nghĩa')
        query = text[pos+len('định nghĩa'):]
        wikipedia.summary(query, sentences=1)
        respond_to_user(wikipedia.summary(query, sentences=1))

    elif "hình nền" in text:
        image = os.path.join("C:\\Users\Lenovo\Pictures\HuySon\\tcnn.jpg")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
        speak('Hình nền máy tính bạn đã được thay đổi')

    elif "tin tức" in text:
        var.set('sau đây là một số tin tức mới nhất trong ngày')
        speak("sau đây là một số tin tức mới nhất trong ngày")
        var.set('Bộ Y tế công bố thêm 83 ca mắc COVID-19 vào tối 5/6, trong đó có 80 ca trong nước tại 7 tỉnh, thành.')
        speak('Bộ Y tế công bố thêm 83 ca mắc COVID-19 vào tối 5/6, trong đó có 80 ca trong nước tại 7 tỉnh, thành.')
        var.set('MU quyết đấu Chelsea và Man City, săn đàn em Ronaldo giá 1700 tỷ đồng')
        speak('MU quyết đấu Chelsea và Man City, săn đàn em Ronaldo giá 1700 tỷ đồng')
        var.set('5/6, nghệ sĩ Hoài Linh đã đăng tải một video giải thích chi tiết quá trình giải ngân số tiền 14 tỷ đồng từ thiện ủng hộ đồng bào miền Trung.')
        speak('5/6, nghệ sĩ Hoài Linh đã đăng tải một video giải thích chi tiết quá trình giải ngân số tiền 14 tỷ đồng từ thiện ủng hộ đồng bào miền Trung.')

    else:
        var.set('Xin lỗi, Bim Bim chưa nghe rõ yêu cầu của bạn')
        # window.update()
        speak('Xin lỗi, Bim Bim chưa nghe rõ yêu cầu của bạn')


# Press space
def key(event):
    if (repr(event.char) == "' '"):
        _play()


if __name__ == '__main__':
    canvas = Canvas(window, width=800, height=600, bg='black')
    canvas.pack(expand=YES, fill=BOTH)

    # animation gif
    # label = Label(window, image="", width=800, height=600)
    # label.pack()
    window.after(10, update(0))

    label2 = Label(window, textvariable=var1, bg='light cyan')
    label2.config(font=("Helvetica", 9, 'bold'))
    var1.set('User')
    label2.pack()

    label1 = Label(window, textvariable=var, bg='slateGray1')
    label1.config(font=("Helvetica", 9))
    var.set('Xin chào, hãy bấm nút Start để Bim Bim có thể lắng nghe bạn nhé.')
    label1.pack()

    # Position image
    # label_test.place(x=0, y=0)

    btn1 = Button(window, text='START',
                  width=14, command=_play, bg='SlateBlue4', fg='light cyan')
    btn1.config(font=("Lucida Console", 13, 'bold'), borderwidth='5')
    btn1.configure(activebackground="SlateBlue1")
    button1_window = canvas.create_window(200, 500, anchor=NW, window=btn1)
    # btn1.pack()
    #
    btn2 = Button(window, text='CLOSE', width=14, command=window.destroy, bg='SlateBlue4', fg='light cyan')
    btn2.config(font=("Lucida Console", 13, 'bold'), borderwidth='5')
    button2_window = canvas.create_window(430, 500, anchor=NW, window=btn2)

    window.after(500, speak, 'Xin chào, hãy bấm nút Start để Bim Bim có thể lắng nghe bạn nhé')
    window.bind("<Key>", key)
    window.mainloop()
