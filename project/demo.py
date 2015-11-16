__author__ = 'DoctorWatson'
from project import parser
from project import speech_response
from project import speechtest2
from project import util
from parser_package import kb


def demo_function(recipe_object):
    recipe = parser.parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/")
    print recipe
    print "test"
    result = ""
    while ("stop" not in result):
        result = speechtest2.run_speech_rec()
        speech_response.choose_response(recipe, result, None)

    print "DEMO IS CONCLUDED"
    return

demo_function(None)