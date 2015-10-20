#
# Code by Charles Cole, Ariel Guo, Christina Kim, and Michael Nowakowski
#

import os
import subprocess
import urllib2
import platform
import json
from parser_package import kb


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
        try:
            recipe_json = subprocess.check_output(['php.exe', fn, url, "json"], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as problem:
            print problem.output
            print problem.returncode
            recipe_json = None

    else:
        fn = os.path.join(os.path.dirname(__file__), 'RecipeParser/bin/parse_recipe')
        print fn
        try:
            recipe_json = subprocess.check_output([fn, url, "json"])
        except subprocess.CalledProcessError as problem:
            print problem.output
            print problem.returncode
            recipe_json = None


    # sometimes the PHP parse_recipe is too verbose. this corrects that issue.
    recipe_json = recipe_json.rpartition('}')
    recipe_json = recipe_json[0] + recipe_json[1]
    print recipe_json
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
    """prints human-readable version of recipe."""
    # parsed_json = json.loads(recipe_json)
    print "RECIPE RETRIVAL: SUCCESS"
    print "TITLE: ", parsed_json['title']
    print "YIELD: ", parsed_json['yield']
    print "INGREDIENTS: ", parsed_json['ingredients'][0]['list']
    print "INSTRUCTIONS: ", parsed_json['instructions']

    return


def find_cooking_tools(steps, knowledge_base):
    """
    finds cooking tools by comparing step string to cooking_wares.txt.
    Avoids duplicates by replacing found items with empty string.
    :param steps:
    :return: list of tools as list of words
    """
    wares = knowledge_base.cooking_wares
    tool_list = []
    for e in steps[0]:
        e = e.lower()
        for tool in wares:
            if tool in e and tool not in tool_list:
                e = e.replace(tool, '')
                tool_list.append(tool)
                print tool
    return tool_list


# def startup():
#     k_base = kb.KnowledgeBase()
#     k_base.load()
#     info = parse_recipe("http://allrecipes.com/recipe/240061/karens-italian-pan-fried-chicken/?internalSource=staff%20pick&referringContentType=home%20page/")
#     human_readable(info)
#     find_cooking_tools(info['instructions'], k_base)
#     return


human_readable(parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"))

# startup()
# print platform.system()

