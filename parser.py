#
# Code by Charles Cole, Ariel Guo, Christina Kim, and Michael Nowakowski
#

import os
import subprocess
import urllib2

def parse_recipe(url):
    """
    :param url: URL for recipe.
    :return: JSON recipe object, formatted by our delightful PHP library.
    """
    # url = "http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"
    fn = os.path.join(os.path.dirname(__file__), 'RecipeParser/bin/parse_recipe')
    recipe_json = subprocess.call([fn,url,"json"])
    print recipe_json
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


parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/")
parse_recipe("http://www.epicurious.com/recipes/food/views/our-favorite-lasagna-with-sausage-spinach-and-three-cheeses-51253440")


