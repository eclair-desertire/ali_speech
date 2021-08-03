from math import trunc
import os
import time
import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import fuzz
import datetime
import random
for index,name in enumerate(sr.Microphone.list_microphone_names()): # код для определения индекса нужного микрофона, нужный с самого верха индекс
    print("Microphone with name \"{1}\" found for 'Microphone(device_index={0})'".format(index,name))
# with sr.Microphone(device_index=1) as source: # указывать индекс микрофона
#     print('Али слушает')
#     audio=r.listen(source)

# query=r.recognize_google(audio,language='ru-RU')
# print('Брат ты сказал: '+query.lower())
opts={
    "alias": ('али','братуха','братан','брат','алле'),
    # "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "cmds": {
        "radio": ('включи музыку','воспроизведи радио','включи радио','включи моргенштерна','влкючи моргена','включи классный музон'),
        "stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты'),
        "tips": ('как убить врага','как замочить его'),
    }
}
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer,audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)
    
        if voice.startswith(opts["alias"]):
            # обращаются к Али
            cmd = voice
 
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            # for x in opts['tbr']:
            #     cmd = cmd.replace(x, "").strip()
            
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC

def execute_cmd(cmd):
    # if cmd == 'ctime':
    #     # сказать текущее время
    #     now = datetime.datetime.now()
    #     speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    
    # elif cmd == 'radio':
    #     # воспроизвести радио
    #     os.system("") # путь до музыки
    if cmd=='tips':
        speak('Мочи его ногами')

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")
    
    else:
        print('Команда не распознана, повторите!')
#Запуск
def record_volume():
    r = sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        print('Настраиваюсь.')
        r.adjust_for_ambient_noise(source, duration=0.5) #настройка посторонних шумов
        print('Слушаю...')
        audio = r.listen(source)
    print('Услышала.')
    try:
        query = r.recognize_google(audio, language = 'ru-RU')
        text = query.lower()
        print(f'Вы сказали: {query.lower()}')
        callback(r,audio)
    except:
        print('Error')

speak_engine=pyttsx3.init()
speak('Здарова братуха, как житуха')
speak('Али на связи')
while True:
    record_volume()


# voices=speak_engine.getProperty('voices')# обязательно должны стоять голоса для синтеза речи
# speak_engine.setProperty('voice',voices[0].id)

r=sr.Recognizer()
m=sr.Microphone(device_index=1)

while True:
  with m as source:
    audio = r.listen(source)
  callback(r, audio)