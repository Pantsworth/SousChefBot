__author__ = 'DoctorWatson'
# -- coding: utf-8 --

import re
import urllib2
import json
import time
import sys
import os

import speech_recognition as sr

import speech_rec_testing as srt
from audio_ding import play_audio

# # deprecated version of background listening
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
        play_audio.play_ding()

    else:
        magic_word_status = False

    return magic_word_status


# def new_speech_recording():
#     r = srt.Recognizer()
#     m = srt.Microphone()
#     mac = False
#     if sys.platform == "darwin":
#         mac = True
#
#     while True:
#         print("Say something!")
#         if mac:
#             os.system("say Say Something")
#         time.sleep(0.5)
#         with m as source:
#             audio = r.listen(source)
#         print("Got it! Now to recognize it...")
#         if mac:
#             os.system("say -v victoria Got it! Now to recognize it")
#         time.sleep(0.75)
#         try:
#             text = r.recognize(audio)
#             print("You said " + text)
#             if mac:
#                 os.system("say  -v vicki "+ text)
#             time.sleep(1)
#             if text == 'exit':
#                 print "I am gonna EXIT bye bye"
#                 if mac:
#                     os.system("say I am gonna exit Bye Bye  ")
#                 time.sleep(0.5)
#                 exit()
#
#         except LookupError:
#             print("Oops! Didn't catch that")
#             if mac:
#                 os.system("say -v Alex Oops Didnt catch that")
#             time.sleep(1)



# speech recognition
def start_speech_rec(speech_engine):
    """
    Once the bot hears our magic word, we can call this to listen for a particular command.
    :return: what wit.ai thought we said
    """
    r = sr.Recognizer()
    r.pause_threshold = 0.3
    r.non_speaking_duration= 0.3


    with sr.Microphone() as source:
        print("*** Yes master? ***")
        audio = r.listen(source)
    wit_ai_response = ""

    # recognize speech using Wit.ai
    WIT_AI_KEY = "AXIII6X7MAX2KW6FD27UFMT3VVQXM6WO" # Wit.ai keys are 32-character uppercase alphanumeric strings
    try:
        speech_engine.say_this("Processing")
        wit_ai_response = r.recognize_wit(audio, key=WIT_AI_KEY)
    except sr.UnknownValueError:
        wit_ai_response = "Wit.ai could not understand audio"
    except sr.RequestError as e:
        wit_ai_response = "Could not request results from Wit.ai service; {0}".format(e)

    # print google_response
    print "Wit.ai thinks you said: " + wit_ai_response

    return wit_ai_response


def wit_call(speechQuery):
    """
      expects a string with the parsed query
      ex: "how do you mash potatoes?"
      returns json object with info
    """
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



# better version of background listening using Google Speech Recognition
def new_background_listen(speech_engine):
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
        # time.sleep(1)
        pass

    if "computer" in text:
        magic_word_status = True
        # play_audio.play_ding()

        # speech_engine = speech_response.VoiceEngine()
        # speech_engine.say_this("Yes?")
    else:
        magic_word_status = False

    return magic_word_status

# speech recognition function
def run_speech_rec(speech_engine):
    background = False
    while not background:
        background = new_background_listen(speech_engine)
        print "Magic Word Status: ", background
        if background:
            speech_engine.say_this("Yes?")
            break

    command = start_speech_rec(speech_engine)

    result = wit_call(command)

    if result == "Response Failed":
        return result

    # print result
    # print result['_text']

    # if result:
    #     test_engine = speech_response.VoiceEngine()
    #     test_engine.say_this(result['_text'])
    return result
