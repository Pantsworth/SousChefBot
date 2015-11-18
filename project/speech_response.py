import pyttsx
from parser_package import kb
import json
import parser

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
    print wit_input['outcomes']
    wanted_ingredient = None

    response = ""
    if intent == 'get_end':
        response = "stopping"

    elif intent == 'get_ingredient':
        #TODO
        response = "error"

    elif intent == 'get_ingredient_amount':
        if not wit_input[u'outcomes'][0][u'entities']:
            return response
        else:
            wanted_ingredient = wit_input[u'outcomes'][0][u'entities'][u'food'][0][u'value']

        try:
            wanted_ingredient = wit_input[u'outcomes'][0][u'entities'][u'food'][0][u'value']
        except KeyError:
            # wanted_ingredient = wit_input[u'outcomes'][0][u'entities'][u'food'][0]
            wanted_ingredient = None
            return False

        print "Wanted Ingredient is: ", wanted_ingredient
        ingredients_found = None
        for ingredient in recipe_object.ingredients:
            if wanted_ingredient in ingredient:
                print "Found ingredient: ", wanted_ingredient
                if ingredients_found:
                    ingredients_found = ingredient + " AND " + ingredients_found
                else:
                    ingredients_found = ingredient
        response = ingredients_found

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
            
    elif intent=='how_to_use_tool':
        #TODO
        response = "error"
    elif intent=='ingredient_substitute':
        #TODO
        response = "error"
    elif intent=='navigate_back':
        #TODO
        response = "previous step"

    elif intent == 'navigate_forward':
        recipe_object.next_step()
        print recipe_object.instructions[recipe_object.current_step]
        response = "Moving to next step. Next step is " + recipe_object.instructions[recipe_object.current_step]

    elif intent=='read_recipe':
        #TODO
        response = "error"
    elif intent=='start_up':
        #TODO
        response = "error"
    elif intent=='technique_how_to':
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
        #TODO
        response = "unknown intent"
        print intent
    return response



def response_test():
    wit_json = {u'outcomes': [{u'entities': {u'food': [{u'suggested': True, u'type': u'value', u'value': u'salt'}, {u'type': u'value', u'value': u'cocoa'}]}, u'confidence': 0.977, u'intent': u'get_ingredient_amount', u'_text': u'how much vegetable oil do i need'}], u'msg_id': u'cd7fa98d-9407-483c-9d7d-746e319a6f0f', u'_text': u'how much vegetable oil do i need'}
    recipe = parser.parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/")
    choose_response(recipe, wit_json, None)
    return

# response_test()