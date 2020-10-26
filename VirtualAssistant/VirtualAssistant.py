import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import json
import requests
import ctypes
import cv2
import sys
import numpy as np
import psutil
import tkinter
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading
import PySimpleGUI as sg

######################## H.U.E AI Assistant ########################
voiceInt = 0
userName = ""
wakePhrase = "hey hugh" or "hey hue"
hueTalking = False

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[voiceInt].id)
engine.startLoop

def speak(text):
    hueTalking = True
    engine.say(text)
    engine.runAndWait()
    hueTalking = False

def wishMe():
    hour=datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good morning, When you need me say, Hey Hue.")
        print("Good morning, When you need me say, Hey Hue.")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon, When you need me say, Hey Hue.")
        print("Good afternoon, When you need me say, Hey Hue.")
    else:
        speak("Good evening, When you need me say, Hey Hue.")
        print("Good evening, When you need me say, Hey Hue.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.....')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio,language='en-in')
            print(f'user said:{statement}\n')
        except Exception as e:
            print(e)
            return "None"
        return statement

def loadHUE():
    userName = "default"

    if voiceInt == 0:
        name = "hue"
    else:
        name = "rue"

    print("Booting " + name + " up")
    speak("Booting " + name + " up")

    if userName == "default":
        speak("You can change your name by saying, My name is, and then your name.")
        print("You can change your name by saying, My name is, and then your name.")

    wishMe()

    #print(takeCommand())

    if __name__=='__main__':
        while True:
            statementWake = takeCommand().lower() #Listens for the commands from user

            if statementWake.count(wakePhrase) > 0: #Checks once for the phrase

                if userName != 'default':
                    speak("How can I help you " + userName + "?")
                    print("How can I help you " + userName + "?")
                else:
                    speak("How can I help?")
                    print("How can I help?")

            while statementWake.count(wakePhrase) > 0: #Loops after the phrase is said until break

                statement = takeCommand().lower() #Listens for the commands from user

                # This is where you define commands
                if statement == '':
                    speak("How can I help?")
                    print("How can I help?")
                    continue

                ######################## Greetings ########################
                if ("goodbye " + name) in statement or ("bye " + name) in statement or "stop" == statement or "no" == statement:
                    speak("Good bye " + userName + ".")
                    print("Good bye " + userName + ".")
                    break

                if "thank you" in statement or "thanks" in statement:
                    speak("You are welcome. Anything else?")
                    print("You are welcome. Anything else?")
                    continue

                if "how are you" in statement:
                    speak("I can not feel, I am a robot. But if I could have feelings I would be shocked. Is there anything else?")
                    print("I can not feel, I am a robot. But if I could have feelings I would be shocked. Is there anything else?")
                    continue

                ######################## About H.U.E ########################
                if 'who are you' in statement or 'what can you do' in statement:
                    speak('I am ' + name + ' and I am your personal AI assistant. You can ask me to search, time, open (google, youtube, or gmail), wikipedia a topic, and more. To get a full run down check online or on the tab on the GUI. Did you need something else?')
                    print('I am ' + name + ' and I am your personal AI assistant. You can ask me to search, time, open (google, youtube, or gmail), wikipedia a topic, and more. To get a full run down check online or on the tab on the GUI. Did you need something else?')
                    continue

                ######################## Web ########################
                if 'wikipedia' in statement:
                    speak('Searching wikipedia...')
                    statement = statement.replace('wikipedia', '')
                    results = wikipedia.summary(statement, sentences=3)
                    speak("Ah yes, acording to wikipedia")
                    print(results)
                    speak(results + " Anything else I can help you with?")
                    continue

                if 'open youtube' in statement:
                    webbrowser.open_new_tab("https://www.youtube.com")
                    speak("YouTube is now open, Anything else?")
                    continue

                if 'open google' in statement:
                    webbrowser.open_new_tab("https://www.google.com")
                    speak("google is now open, Anything else?")
                    continue

                if 'open gmail' in statement:
                    webbrowser.open_new_tab("https://www.gmail.com")
                    speak("Gmail is now open, Anything else?")
                    continue

                if 'search' in statement:
                    statement = statement.replace('search', '')
                    webbrowser.open_new_tab(statement)
                    continue

                ######################## Computer System ########################
                if 'current time' in statement:
                    strTime=datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f'the time is {strTime}')
                    print(strTime)
                    speak("Anything else I can help with?")
                    print("Anything else I can help with?")
                    continue

                if 'lock computer' in statement:
                    speak("OK, your PC will now lock.")
                    print("OK, your PC will now lock.")
                    ctypes.windll.user32.LockWorkStation()
                    break

                if 'shut down computer' in statement:
                    speak("OK, your PC will now shutdown.")
                    print("OK, your PC will now shutdown.")
                    os.system("shutdown /s /t 1")
                    break

                if 'system information' in statement:
                    speak("CPU usage is at " + str(psutil.cpu_percent()) + " percent. RAM being used is at " + str(psutil.virtual_memory().percent) + " percent. Anything else?")
                    print("CPU usage is at " + str(psutil.cpu_percent()) + " percent. RAM being used is at " + str(psutil.virtual_memory().percent) + " percent. Anything else?")
                    continue

                ######################## Human Recognition ########################
                if 'my name is' in statement:
                    statement = statement.replace('my name is', '')
                    userName = statement

                    file = open("UserInformation", "r+")
                    file.close()

                    print(file)

                    speak('Hello ' + userName + '. Can I help you with anything?')
                    continue

                if 'capture camera' in statement or 'take a photo' in statement:
                    fileNum = 1

                    while (os.path.isfile("People/" + userName + "_" + str(fileNum) + ".png")):
                        fileNum += 1

                    ec.capture(0, "robo camera", "People/" + userName + "_" + str(fileNum) + ".png")
                    speak('Anything else?')
                    continue

                if 'scan face' in statement:
                    speak('Currently in development. Anything else I can help you with?')
                    print('Currently in development. Anything else I can help you with?')
                    continue

                if 'play playlist' in statement:
                    statement = statement.replace('play playlist', '')

                    SpotifyOAuth.client_id = 'f2f549ec1c0b44fb9135033107ed1a9c'
                    SpotifyOAuth.client_secret = '70dba96a0b6040158d5852e31bc6509e'
                    SpotifyOAuth.redirect_uri = 'https://google.com'

                    scope = 'user-library-read'

                    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
                    sp.search(q=statement, type='playlist')

######################## H.U.E GUI ########################
def loadGUI():
    sg.theme('DarkBlue12') 

    layout = [  [sg.Button('X', key='_exit_', pad=((265, 0), (0,0)))],
                [sg.Text('------------------------------------------------', key='_animate_mouth_', pad=((40, 0), (35, 0)))],
                [sg.Button('Speech to Text +', key='_speech_to_text_', pad=((0, 0), (40,0))), sg.Button('Commands +', key='_commands_', pad=((90, 0), (40,0)))]
    ]

    layoutCommandList = [   [sg.Text('Say "System Information" for CPU and RAM \nusage.')],
                            [sg.Text('Say "Lock Computer" to lock your computer.')],
                            [sg.Text('Say "Shutdown Computer" to shutdown your \ncomputer.')],
                            [sg.Text('Say "Current Time" to get the current time.')],
                            [sg.Text('Say "How are you?" See what the AI says.')],
                            [sg.Text('Say "Capture camera" or "Take a photo" to \ntake a photo using the web camera.')],
                            [sg.Text('Say "Wikipedia and then a topic" to get a \nsummary of the topic.')]
    ]

    layoutCommands = [  [sg.Text('H.U.E Command List:')],
                [sg.Column(layoutCommandList, scrollable=True, vertical_scroll_only=True, size=(350, 120), grab=False)]
    ]

    layoutSpeechToText = [  [sg.Text('H.U.E Speech To Text')],
                [sg.Text('H.U.E: ')],
                [sg.Text('User: ')]
    ]

    window = sg.Window('Personal Assistant | H.U.E', layout, no_titlebar=True, alpha_channel=.85, grab_anywhere=True, size=(300, 150), finalize=True)

    windowCommands = sg.Window('Commands | H.U.E', layoutCommands, no_titlebar=True, alpha_channel=.9, grab_anywhere=True, size=(350, 150))

    windowSpeechToText = sg.Window('Speech To Text | H.U.E', layoutSpeechToText, no_titlebar=True, alpha_channel=.9, grab_anywhere=True, size=(350, 150))

    while True:
        event, values = window.read(timeout=0)

        if event == sg.WIN_CLOSED or event == '_exit_':
            break

        if event == '_commands_':
            windowCommands.read(timeout=0)
            continue

        if event == '_speech_to_text_':
            windowSpeechToText.read(timeout=0)
            continue
        

        #This runs H.U.E
        threading.Thread(target= loadHUE(), daemon= True).start()

    window.close()
    windowCommands.close()

########################### H.U.E Run ########################
threading.Thread(target= loadGUI()).start()