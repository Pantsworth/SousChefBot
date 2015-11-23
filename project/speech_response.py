import pyttsx
from parser_package import kb
import json
import parser
import sys, os

class VoiceEngine:
    """
    Text to speech with pyttsx. Initialized as an object with associated functions.
    """
    def __init__(self):
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 190)
        # print self.engine.getProperty("voice")

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
        # print sys.platform
        if sys.platform == "darwin":
            # print "Mac Speech Synthesizer"
            os.system("say " + phrase)
        else:
            self.engine.say(phrase)
            self.engine.runAndWait()
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

    if wit_input == "Response Failed":
        response = wit_input
        return response

    intent = wit_input[u'outcomes'][0][u'intent']
    print wit_input['outcomes']
    wanted_ingredient = None

    response = ""
    if intent == 'get_end':
        response = "stopping"

    elif intent == 'get_ingredient':
        wanted_ingredient = wit_input[u'outcomes'][0][u'entities'][u'food'][0][u'value']
        if wanted_ingredient == "eggplant":
            response = "An eggplant is the large egg-shaped fruit of an Old World plant, eaten as a vegetable. Its skin is typically dark purple, but the skin of certain cultivated varieties is white or yellow. "
        elif wanted_ingredient == "rosemary":
            response = "Rosemary is an evergreen aromatic shrub of the mint family, native to southern Europe. The narrow leaves are used as a culinary herb, in perfumery, and as an emblem of remembrance."
        else:
            response = wanted_ingredient
    
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
        ingredients_found = ""
        for ingredient in recipe_object.ingredients:
            if wanted_ingredient in ingredient:
                print "Found ingredient: ", wanted_ingredient
                if (ingredient not in ingredients_found) and (ingredients_found is not ""):
                    ingredients_found = ingredient + " AND " + ingredients_found
                else:
                    ingredients_found = ingredient

        response = ingredients_found

    elif intent == 'get_temperature':
        temp_response = ""
        for step in recipe_object.instructions:
            print "here " + step
            if (("degrees" or "farenheit" or "celsius") in step) and (step not in temp_response):
                if step not in temp_response:
                    print "not in response"
                if temp_response == "":
                    temp_response = step
                else:
                    temp_response = temp_response + " and " + step

        if temp_response is "":
            response = "Error"
        else:
            print temp_response
            response = temp_response

    elif intent == 'list_ingredients':
        response = "Reading all ingredients"
        for ing in recipe_object.ingredients:
            response = response + ". " + ing

    elif intent == 'get_time':
        want_time = recipe_object.instructions
        indices = [i for i, s in enumerate(want_time) if 'time' in s]
        if indices:
            response = want_time[indices[0]]
        else:
            response = "could not find time"
            
    elif intent == 'how_to_use_tool':
        tool = wit_input[u'outcomes'][0][u'entities'][u'tool'][0][u'value']
        list_tool = recipe_object.tools
        indices = [i for i, s in enumerate(list_tool) if tool in s]
        if indices:
          response = "Learn how to use " +  list_tool[indices[0]] + " here http://www.wikihow.com/Use-a-Knife"
        else:
            response = "could not find tools"

    elif intent=='ingredient_substitute':
        #TODO
        response = "error"

    # #### NAVIGATION #### #
    elif intent=='navigate_back':
        if recipe_object.current_step is not 0:
            recipe_object.previous_step()
            response = "Previous Step is: " + sanitize_step(recipe_object.instructions[recipe_object.current_step])
        else:
            response = "Already on first step. Step is: " + sanitize_step(recipe_object.instructions[recipe_object.current_step])

    elif intent == 'navigate_forward':
        if recipe_object.current_step is not len(recipe_object.instructions)-1:
            recipe_object.next_step()
            response = "Moving to next step. Next step is " + sanitize_step(recipe_object.instructions[recipe_object.current_step])
        else:
            response = "Already on last step. Step is: " + recipe_object.instructions[recipe_object.current_step]

    elif intent == 'current_step':
        if recipe_object.current_step <= len(recipe_object.instructions) - 1:
          response = "Current step is: " + sanitize_step(recipe_object.instructions[recipe_object.current_step])
        else:
            response = "We've read through all the instructions is there a specific step you would like?"


    elif intent == 'start_up':
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


def sanitize_step(step):
    """
    :param step: takes step string from instructions
    :return: sanitized version for speech
    """
    new_step = step
    bad_char_list = [";", "(", ")"]
    for char in bad_char_list:
        new_step = new_step.replace(char, " ")

    return new_step

def response_test():
    wit_json = {u'outcomes': [{u'entities': {u'food': [{u'suggested': True, u'type': u'value', u'value': u'salt'}, {u'type': u'value', u'value': u'cocoa'}]}, u'confidence': 0.977, u'intent': u'get_ingredient_amount', u'_text': u'how much vegetable oil do i need'}], u'msg_id': u'cd7fa98d-9407-483c-9d7d-746e319a6f0f', u'_text': u'how much vegetable oil do i need'}
    recipe = parser.parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/")
    choose_response(recipe, wit_json, None)
    return

# response_test()
