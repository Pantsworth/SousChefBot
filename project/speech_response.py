__author__ = 'DoctorWatson'
import pyttsx

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 160)
        print self.engine.getProperty("voice")

    def test(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print "Using voice:", repr(voice)
            self.engine.setProperty('voice', voice.id)
            self.engine.say("Hi there, how's you ?")
            self.engine.say("A B C D E F G H I J K L M")
            self.engine.say("N O P Q R S T U V W X Y Z")
            self.engine.say("0 1 2 3 4 5 6 7 8 9")
            self.engine.say("Sunday Monday Tuesday Wednesday Thursday Friday Saturday")
            self.engine.say("Violet Indigo Blue Green Yellow Orange Red")
            self.engine.say("Apple Banana Cherry Date Guava")
        self.engine.runAndWait()

    def say_this(self, phrase):
        self.engine.say(phrase)
        self.engine.runAndWait()
        return
