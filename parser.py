#
# Code by Charles Cole, Ariel Guo, Christina Kim, and Michael Nowakowski
#

import os
import subprocess
import urllib2
import platform
import json

def parse_recipe(url):
    """Calls CLI and runs our PHP recipe_parser function. Returns JSON
    :param url: URL for recipe.
    :return: JSON recipe object, formatted by our delightful PHP library.
    """
    system_type = platform.system()
    # url = "http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"
    if system_type == 'Windows':
        fn = os.path.join(os.path.dirname(__file__), 'RecipeParser/bin/parse_recipe')
        recipe_json = subprocess.check_output(['php.exe', fn, url, "json"])
    else:
        fn = os.path.join(os.path.dirname(__file__), 'RecipeParser/bin/parse_recipe')
        recipe_json = subprocess.check_output([fn, url, "json"])

    return recipe_json


def get_html(url):
    """
    Retrieves html text from a string-formatted url
    :param url: web url string
    :return: html text
    """
    if '://' not in url:
        formatted_url = 'http://' + url
    else:
        formatted_url = url
    try:
        return urllib2.urlopen(formatted_url).read()
    except urllib2.URLError:
        print "Invalid URL Request"
        return None


def human_readable(recipe_json):
    parsed_json = json.loads(recipe_json)
    print "SUCCESS"
    print "TITLE: ", parsed_json['title']
    print "INGREDIENTS: ", parsed_json['ingredients']
    return




human_readable(parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"))
# parse_recipe("http://www.epicurious.com/recipes/food/views/our-favorite-lasagna-with-sausage-spinach-and-three-cheeses-51253440")

# print platform.system()

