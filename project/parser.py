#
# Code by Charles Cole, Ariel Guo, Christina Kim, and Michael Nowakowski
#

import os
import subprocess
import urllib2
import platform
import json
import pprint

def parse_recipe(url):
    """Calls CLI and runs our PHP recipe_parser function. Returns JSON
    :param url: URL for recipe.
    :return: JSON recipe object, formatted by our delightful PHP library.
    """

    if validate_url(url) is None:
        return

    system_type = platform.system()
    # url = "http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"
    if system_type == 'Windows':
        fn = os.path.join(os.path.dirname(__file__), 'RecipeParser/bin/parse_recipe')
        recipe_json = subprocess.check_output(['php.exe', fn, url, "json"])
    else:
        fn = os.path.join(os.path.dirname(__file__), 'RecipeParser/bin/parse_recipe')
        recipe_json = subprocess.check_output([fn, url, "json"])

    parsed_json = json.loads(recipe_json)

    return parsed_json


def validate_url(url):
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
        url_test = urllib2.urlopen(formatted_url).read()
        if url_test:
            return True
        else:
            return None

    except urllib2.URLError:
        print "Invalid URL Request"
        return None


def human_readable(parsed_json):
    # parsed_json = json.loads(recipe_json)
    # print "RECIPE RETRIVAL: SUCCESS"
    # print "TITLE: ", parsed_json['title']
    # print "YIELD: ", parsed_json['yield']
    print "INGREDIENTS: ", parsed_json['ingredients'][0]['list']
    print "INSTRUCTIONS: ", parsed_json['instructions']

    # pprint.pprint(parsed_json)
    return



human_readable(parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"))

# print platform.system()

