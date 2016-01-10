import urllib2, json

# class VoiceEngine:
#     """
#     Text to speech with pyttsx. Initialized as an object with associated functions.
#     """
#     def __init__(self):
#         death_to_pyttsx = True
#         if death_to_pyttsx:
#             self.engine = None
#             print "Going without pyttsx. If you're not on a Mac, this will fail (set death_to_pyttsx to False)."
#         else:
#             try:
#                 import pyttsx
#                 self.engine = pyttsx.init()
#                 self.engine.setProperty('rate', 190)
#
#             except ImportError:
#                 self.engine = None
#                 print "Pyttsx import failed - Using Mac System Voice."
#                 # print self.engine.getProperty("voice")
#
#     def test(self):
#         voices = self.engine.getProperty('voices')
#         for voice in voices:
#             print "Using voice:", repr(voice)
#             self.engine.setProperty('voice', voice.id)
#             self.engine.say("Hi there, how's you ?")
#             self.engine.say("A B C D E F G H I J K L M")
#             self.engine.say("N O P Q R S T U V W X Y Z")
#             self.engine.say("0 1 2 3 4 5 6 7 8 9")
#         self.engine.runAndWait()
#         return
#
#     def say_this(self, phrase):
#         # print sys.platform
#         if sys.platform == "darwin":
#             # print "Mac Speech Synthesizer"
#             os.system("say " + phrase)
#         else:
#             self.engine.say(phrase)
#             self.engine.runAndWait()
#         return

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
            response = "response failed"
            return response
        else:
            wanted_ingredient = wit_input[u'outcomes'][0][u'entities'][u'food'][0][u'value']
            if wanted_ingredient == {}:
                print "Could not find ingredient."
                return "No Ingredient Found"
        try:
            wanted_ingredient = wit_input[u'outcomes'][0][u'entities'][u'food'][0][u'value']
        except KeyError:
            # wanted_ingredient = wit_input[u'outcomes'][0][u'entities'][u'food'][0]
            wanted_ingredient = None
            print "Could not find ingredient."
            return "No Ingredient Found"

        print "Wanted Ingredient is: ", wanted_ingredient

        ingredients_found = ""
        for ingredient in recipe_object.ingredients:
            if wanted_ingredient in ingredient:
                print "Found ingredient: ", wanted_ingredient
                if (ingredient not in ingredients_found) and (ingredients_found is not ""):
                    ingredients_found = ingredient + " AND " + ingredients_found
                else:
                    ingredients_found = ingredient
        if ingredients_found == "":
            response = "Could not find ingredient"
        else:
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
            for i in indices:
                if list_tool[i] == 'knife':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Use-a-Knife"
                elif list_tool[i] == 'spring form':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Remove-Cheesecake-from-a-Springform-Pan"
                elif list_tool[i] == 'blender':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Use-a-Blender"
                elif list_tool[i] == 'garlic press':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Crush-Garlic#Using_a_Garlic_Press_sub"
                elif list_tool[i] == 'hand mixer':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Use-a-Hand-Mixer"
                elif list_tool[i] == 'food processor':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Use-a-Food-Processor"
                elif list_tool[i] == 'vegetable peeler':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Peel-a-Carrot#Using_a_Vegetable_Peeler_sub"
                elif list_tool[i] == 'food processor':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Use-a-Food-Processor"
                elif list_tool[i] == 'oven':
                    response = "Learn how to use " +  list_tool[indices[i]] + " here http://www.wikihow.com/Use-an-Oven"
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
            response = "Next step is " + sanitize_step(recipe_object.instructions[recipe_object.current_step])
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

    elif intent == "first_step":
        response = "First step is: " + recipe_object.instructions[0]

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

