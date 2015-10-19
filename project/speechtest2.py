__author__ = 'DoctorWatson'

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import re

# obtain audio from the microphone
def start_speech_rec():
    """
    Once the bot hears our magic word, we can call this to listen for a particular command.
    :return: google_response is what google thought we said. wit_ai_response is what wit.ai thought.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    google_response = ""
    wit_ai_response = ""
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        google_response = ("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        google_response = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        google_response = ("Could not request results from Google Speech Recognition service; {0}".format(e))

    print google_response
    # recognize speech using Wit.ai
    WIT_AI_KEY = "AXIII6X7MAX2KW6FD27UFMT3VVQXM6WO" # Wit.ai keys are 32-character uppercase alphanumeric strings
    try:
        wit_ai_response = "Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY)
    except sr.UnknownValueError:
        wit_ai_response = "Wit.ai could not understand audio"
    except sr.RequestError as e:
        wit_ai_response = "Could not request results from Wit.ai service; {0}".format(e)

    print wit_ai_response

    return google_response, wit_ai_response


def background_listen():
    """
    Listens for our magic word(s) and returns True if it hears them within a certain amount of time.
    :return: Boolean
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    magic_word_status = False
    # google_response = ""
    # wit_ai_response = ""
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        google_response = "Google Speech Recognition could not understand audio"
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        google_response = ("Could not request results from Google Speech Recognition service; {0}".format(e))

    # recognize speech using Wit.ai
    WIT_AI_KEY = "AXIII6X7MAX2KW6FD27UFMT3VVQXM6WO" # Wit.ai keys are 32-character uppercase alphanumeric strings
    try:
        print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

    if re.compile(r'\bsous chef\b', flags=re.IGNORECASE).search(r.recognize_wit(audio, key=WIT_AI_KEY)):
        magic_word_status = True
    else:
        magic_word_status = False

    return magic_word_status

# if 'sous chef' in r.recognize_wit(audio, key='AXIII6X7MAX2KW6FD27UFMT3VVQXM6WO'):
#     print('yes')
# else:
#     print("no")

# # recognize speech using IBM Speech to Text
# IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE" # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
# IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE" # IBM Speech to Text passwords are mixed-case alphanumeric strings
# try:
#     print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
# except sr.UnknownValueError:
#     print("IBM Speech to Text could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from IBM Speech to Text service; {0}".format(e))
#
# # recognize speech using AT&T Speech to Text
# ATT_APP_KEY = "INSERT AT&T SPEECH TO TEXT APP KEY HERE" # AT&T Speech to Text app keys are 32-character lowercase alphanumeric strings
# ATT_APP_SECRET = "INSERT AT&T SPEECH TO TEXT APP SECRET HERE" # AT&T Speech to Text app secrets are 32-character lowercase alphanumeric strings
# try:
#     print("AT&T Speech to Text thinks you said " + r.recognize_att(audio, app_key=ATT_APP_KEY, app_secret=ATT_APP_SECRET))
# except sr.UnknownValueError:
#     print("AT&T Speech to Text could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from AT&T Speech to Text service; {0}".format(e))