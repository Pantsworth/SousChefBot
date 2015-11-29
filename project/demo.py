__author__ = 'DoctorWatson'
import parser
import speech_response
import speechtest2
import util
from parser_package import kb
import util

def demo_function(recipe_object):

    k_base = kb.KnowledgeBase()
    k_base.load()

    # preamble for human-friendly opening
    preamble = False

    result = ""
    recipe = parser.parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/", k_base)
    # recipe = parser.parse_recipe("http://allrecipes.com/recipe/235653/crispy-chicken-nuggets/")
    recipe.print_recipe()

    # ********** PREAMBLE ********* #

    speech_engine = speech_response.VoiceEngine()
    speech_engine.say_this("This is a recipe for: " + recipe.title)

    if preamble:
        speech_engine.say_this("Here is a list of the ingredients")

        for ing in recipe.ingredients:
            speech_engine.say_this(ing)

        speech_engine.say_this("The first step is: " + util.sanitize_step(recipe.instructions[recipe.current_step]))

        speech_engine.say_this("Feel free to ask me any questions. Just say computer, computer to get me to wake up. After I say yes, ask me your question.")
        speech_engine.say_this("I am listening now.")

    # ********** END OF PREAMBLE ********* #

    question_collector = []
    answer_collector = []

    while ("stop" not in result):

        speech_engine.say_this("Listening.")

        result = speechtest2.run_speech_rec(speech_engine)
        response = speech_response.choose_response(recipe, result, k_base)

        question_collector.append(result)
        answer_collector.append(response)

        if response:
            speech_engine.say_this(response)
            if response == "stopping":
                break

    print "DEMO IS CONCLUDED"
    return

def main():
  demo_function(None)
  return

if __name__ == '__main__':
  main()
