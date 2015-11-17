import pyttsx
from parser_package import kb
import recipe
import speechtest2

'''
class VoiceEngine:

    Text to speech with pyttsx. Initialized as an object with associated functions.

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
'''


def Voice(phrase):
        engine = pyttsx.init()
        engine.setProperty('rate', 190)
        engine.say(phrase)
        engine.runAndWait()
        print "it is said"+ phrase
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

    elif intent == 'get_ingredient':  #need database not exist in recipe or maybe can omit, not very valuable questions
        #TODO
        response = "error"

    elif intent == 'get_ingredient_amount':
        wanted_ingredient = wit_input[u'outcomes'][0][u'entities']
        list_ingredient = recipe_object.ingredients
        indices = [i for i, s in enumerate(list_ingredient) if wanted_ingredient in s]
        if indices:
            response = list_ingredient[indices[0]]
        else:
            response = "could not find ingredient"

    elif intent == 'get_temperature':
        want_temperature = recipe_object.instructions
        indices = [i for i, s in enumerate(want_temperature) if 'temperature' in s]
        if indices:
            response = want_temperature[indices[0]]
        else:
            response = "could not find temperature"

    elif intent == 'get_time':
        want_time = recipe_object.instructions
        indices = [i for i, s in enumerate(want_time) if 'time' in s]
        if indices:
            response = want_time[indices[0]]
        else:
            response = "could not find time"

    elif intent=='how_to_use_tool':  #need database, not exist in recipe
        #TODO
        response = "error"

    elif intent=='ingredient_substitute':
        old_ingredient = wit_input[u'outcomes'][0][u'entities']
        new_ingredient = kb_object.find_substitute
        indices = [i for i, s in enumerate(new_ingredient) if old_ingredient in s]
        if indices:
            response = new_ingredient
        else:
            response = "could not find substitute ingredient"

    elif intent=='navigate_back':  #need step number, haven't find
        #TODO
        response = "error"

    elif intent == 'navigate_forward':
        recipe_object.instructions=recipe_object.add_steps(recipe_object.instructions)
        response = recipe_object.instructions

    elif intent == 'read_recipe':
        response = recipe_object.instructions

    elif intent == 'start_up':
        response = "Welcome to SouChefBot"

    elif intent == 'technique_how_to':   #need database, not exist in recipe
        #TODO
        response = "error"

    elif intent == 'which_tool':
        choose_tool = wit_input[u'outcomes'][0][u'entities']
        list_tool = recipe_object.tools
        indices = [i for i, s in enumerate(list_tool) if choose_tool in s]
        if indices:
            response = list_tool[indices[0]]
        else:
            response = "could not find tools"

    else:
        response = "unknown intent"
        print intent
    return response


response = choose_response(recipe_object=recipe, wit_input=speechtest2.wit_call(speechQuery), kb_object=kb)  # where is the input of speechQuery?
Voice(response)






