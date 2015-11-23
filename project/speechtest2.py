__author__ = 'DoctorWatson'
# -- coding: utf-8 --
# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import re
import speech_response
import urllib2
import json
import sys

# obtain audio from the microphone
def start_speech_rec():
    """
    Once the bot hears our magic word, we can call this to listen for a particular command.
    :return: google_response is what google thought we said. wit_ai_response is what wit.ai thought.
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
    response = urllib2.urlopen(req)
    html = response.read()
    json_obj = json.loads(html)
    return json_obj


def run_speech_rec():
    background = False
    while not background:
        background = background_listen()
        print "Magic Word Status: ", background
        if background:
            break
    command = start_speech_rec()
    result = wit_call(command)
    print result
    print result['_text']
    # if result:
    #     test_engine = speech_response.VoiceEngine()
    #     test_engine.say_this(result['_text'])
    return result

# run_speech_rec()