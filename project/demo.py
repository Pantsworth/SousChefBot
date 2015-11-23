__author__ = 'DoctorWatson'
import parser
import speech_response
import speechtest2
import util
from parser_package import kb


def demo_function(recipe_object):
    recipe = parser.parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/")
    # print recipe
    result = ""
    while ("stop" not in result):
        result = speechtest2.run_speech_rec()
        response = speech_response.choose_response(recipe, result, None)

        if response:
            if response == "stopping":
                break
            else:
                speech_engine = speech_response.VoiceEngine()
                speech_engine.say_this(response)

    print "DEMO IS CONCLUDED"
    return

# def speechDemo(phrase):
#     test_engine = speech_response.VoiceEngine()
#     test_engine.say_this(phrase)
#     return

demo_function(None)
# speechDemo("yes master?")
def main():
  demo_function(None)

if __name__ == '__main__':
  main()
