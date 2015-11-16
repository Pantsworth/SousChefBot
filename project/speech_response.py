import pyttsx
from parser_package import kb

class VoiceEngine:
    """
    Text to speech with pyttsx. Initialized as an object with associated functions.
    """
    def __init__(self):
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 190)
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
        return

    def say_this(self, phrase):
        self.engine.say(phrase)
        self.engine.runAndWait()
        print "it is said"
        return




def choose_response(recipe_object, wit_input, kb_object):
    """
    Charlie and Jingming
    Start with reading ingredient amounts, work up to how_to

    :param recipe_object: recipe object with state
    :param wit_input: json object from wit
        ex. {u'outcomes': [{u'entities': {}, u'confidence': 0.742, u'intent': u'get_time', u'_text': u'Wit.ai thinks you
         said: yeah'}], u'msg_id': u'5262a8bf-a25a-4183-bc42-a4cd1807e20e', u'_text': u'Wit.ai thinks you said: yeah'}
    :param kb_object: our knowledge base
    :return: string that is an appropriate speech response
    """
    #wit_input = {u'outcomes': [{u'entities': {}, u'confidence': 0.742, u'intent': u'get_time', u'_text': u'Wit.ai thinks you said: yeah'}], u'msg_id': u'5262a8bf-a25a-4183-bc42-a4cd1807e20e', u'_text': u'Wit.ai thinks you said: yeah'}
    intent = wit_input[u'outcomes'][0][u'intent']
    response = ""
    if intent == 'get_end':
        response = "stopping"
    elif intent == 'get_ingredient':
        #TODO
        response = "error"

    elif intent == 'get_ingredient_amount':
        wanted_ingredient = wit_input[u'outcomes'][0][u'entities']
        print "Wanted Ingredient is: ", wanted_ingredient
        list_ingredient = recipe_object.ingredients
        indices = [i for i, s in enumerate(list_ingredient) if wanted_ingredient in s]
        if indices:
            response = list_ingredient[indices[0]]
        else:
            response = "could not find ingredient"
    elif intent == 'get_temperature':
        #TODO
        response = "error"
    elif intent == 'get_time':
        #TODO
        response = "error"
    elif intent=='how_to_use_tool':
        #TODO
        response = "error"
    elif intent=='ingredient_substitute':
        #TODO
        response = "error"
    elif intent=='navigate_back':
        #TODO
        response = "error"
    elif intent=='navigate_forward':
        #TODO
        response = "error"
    elif intent=='read_recipe':
        #TODO
        response = "error"
    elif intent=='start_up':
        #TODO
        response = "error"
    elif intent=='technique_how_to':
        #TODO
        response = "error"
    elif intent=='which_tool':
        #TODO
        response = "error"
    else:
        #TODO
        response = "unknown intent"
        print intent
    return response
