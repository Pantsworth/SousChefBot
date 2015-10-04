#
# Code by Charles Cole, Ariel Guo, Christina Kim, and Michael Nowakowski
#

import os
import subprocess

def parse_recipe(url):
    # url = "http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"
    fn = os.path.join(os.path.dirname(__file__), 'RecipeParser/bin/parse_recipe')
    recipe_json = subprocess.call([fn,url,"json"])
    print recipe_json
    return recipe_json

parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/")



