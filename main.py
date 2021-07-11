from math import trunc
import os
import time
import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import fuzz
import datetime

# for index,name in enumerate(sr.Microphone.list_microphone_names()): # код для определения индекса нужного микрофона, нужный с самого верха индекс
#     print("Microphone with name \"{1}\" found for 'Microphone(device_index={0})'".format(index,name))
# with sr.Microphone(device_index=1) as source: # указывать индекс микрофона
#     print('Али слушает')
#     audio=r.listen(source)

# query=r.recognize_google(audio,language='ru-RU')
# print('Брат ты сказал: '+query.lower())
opts={
    "alias": ('али','братуха'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час'),
        "radio": ('включи музыку','воспроизведи радио','включи радио'),
        "stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты')
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
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
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
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    
    # elif cmd == 'radio':
    #     # воспроизвести радио
    #     os.system("D:\\Jarvis\\res\\radio_record.m3u")
    
    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")
    
    else:
        print('Команда не распознана, повторите!')
#Запуск
r=sr.Recognizer()
m=sr.Microphone(device_index=1)
with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine=pyttsx3.init()
voices=speak_engine.getProperty('voices')# обязательно должны стоять голоса для синтеза речи
speak_engine.setProperty('voice',voices[4].id)
speak('Здарова пидрила')
speak('Али на связи')
stop_listening=r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)