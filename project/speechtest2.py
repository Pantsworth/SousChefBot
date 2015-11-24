__author__ = 'DoctorWatson'
# -- coding: utf-8 --
# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import speech_rec_testing as srt
import re
import speech_response
import urllib2
import json
import time, sys

import sys, os, pyaudio

# obtain audio from the microphone
def start_speech_rec():
    """
    Once the bot hears our magic word, we can call this to listen for a particular command.
    :return: what wit.ai thought we said
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("*** Yes master? ***")
        audio = r.listen(source)
    wit_ai_response = ""

    # recognize speech using Wit.ai
    WIT_AI_KEY = "AXIII6X7MAX2KW6FD27UFMT3VVQXM6WO" # Wit.ai keys are 32-character uppercase alphanumeric strings
    try:
        wit_ai_response = r.recognize_wit(audio, key=WIT_AI_KEY)
    except sr.UnknownValueError:
        wit_ai_response = "Wit.ai could not understand audio"
    except sr.RequestError as e:
        wit_ai_response = "Could not request results from Wit.ai service; {0}".format(e)

    # print google_response
    print "Wit.ai thinks you said: " + wit_ai_response

    return wit_ai_response


def background_listen():
    """
    Listens for our magic word(s) and returns True if it hears them within a certain amount of time.
    :return: Boolean
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("*** Background Listening ***")
        audio = r.listen(source)

    magic_word_status = False
    # wit_ai_response = ""

    # recognize speech using Wit.ai
    WIT_AI_KEY = "AXIII6X7MAX2KW6FD27UFMT3VVQXM6WO" # Wit.ai keys are 32-character uppercase alphanumeric strings

    try:
        print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

    if re.compile(r'\bcomputer\b', flags=re.IGNORECASE).search(r.recognize_wit(audio, key=WIT_AI_KEY)):
        magic_word_status = True
    else:
        magic_word_status = False

    return magic_word_status


def wit_call(speechQuery):
    '''
      expects a string with the parsed query 
      ex: "how do you mash potatoes?"
      returns json object with info
    '''
    s = urllib2.quote(speechQuery)
    url = "https://api.wit.ai/message?v=20151102&q=" + s
    auth_token = "4PRXFOGEMZFETD7BCQ56YDMC5MV4FXVZ"
    req = urllib2.Request(url, None, {"Authorization": "Bearer %s" %auth_token})
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError:
        response = []
        return "Response Failed"

    html = response.read()
    json_obj = json.loads(html)
    return json_obj


def run_speech_rec():
    background = False
    while not background:
        background = new_background_listen()
        print "Magic Word Status: ", background
        if background:
            break
    command = start_speech_rec()

    result = wit_call(command)

    if result == "Response Failed":
        return result

    # print result
    # print result['_text']

    # if result:
    #     test_engine = speech_response.VoiceEngine()
    #     test_engine.say_this(result['_text'])
    return result



def new_speech_recording():
    r = srt.Recognizer()
    m = srt.Microphone()
    mac = False
    if sys.platform == "darwin":
        mac = True

    while True:
        print("Say something!")
        if mac:
            os.system("say Say Something")
        time.sleep(0.5)
        with m as source:
            audio = r.listen(source)
        print("Got it! Now to recognize it...")
        if mac:
            os.system("say -v victoria Got it! Now to recognize it")
        time.sleep(0.75)
        try:
            text = r.recognize(audio)
            print("You said " + text)
            if mac:
                os.system("say  -v vicki "+ text)
            time.sleep(1)
            if text == 'exit':
                print "I am gonna EXIT bye bye"
                if mac:
                    os.system("say I am gonna exit Bye Bye  ")
                time.sleep(0.5)
                exit()

        except LookupError:
            print("Oops! Didn't catch that")
            if mac:
                os.system("say -v Alex Oops Didnt catch that")
            time.sleep(1)


def new_background_listen():
    """
    Listens for our magic word(s) and returns True if it hears them within a certain amount of time.
    :return: Boolean
    """
    r = srt.Recognizer()
    with srt.Microphone() as source:
        print("*** Background Listening ***")
        audio = r.listen(source)

    text = ""
    magic_word_status = False
    try:
        text = r.recognize(audio)
        print("You said " + text)

    except LookupError:
        # print("Oops! Didn't catch that")
        time.sleep(1)

    if "computer" in text:
        magic_word_status = True
        speech_engine = speech_response.VoiceEngine()
        speech_engine.say_this("Yes?")
        # time.sleep(1)
    else:
        magic_word_status = False

    return magic_word_status

# run_speech_rec()