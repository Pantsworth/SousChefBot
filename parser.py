#
# Code by Charles Cole, Ariel Guo, Christina Kim, and Michael Nowakowski
#

import os
import subprocess

def parse_recipe():

    url = "http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"

    fn = "" + os.path.join(os.path.dirname(__file__), 'RecipeParser/bin/parse_recipe')
    print fn
    called_command = fn + " " + url + " " + "json"
    subprocess.call(['fn'])
    print called_command
    # json_object = subprocess.call(called_command,)


    # print json_object
    return

parse_recipe()



