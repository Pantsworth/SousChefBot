#
# Code by Charles Cole, Ariel Guo, Christina Kim, and Michael Nowakowski
#

import os
import subprocess
import urllib2
import platform
import json
from parser_package import kb
import recipe
import util


def parse_recipe(url, k_base):
    """Calls CLI and runs our PHP recipe_parser function. Returns JSON
    :param url: URL for recipe.
    :return: JSON recipe object, formatted by our delightful PHP library.
    """
    if k_base == None:
        k_base = kb.KnowledgeBase()
        k_base.load()

    step_list = []
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
        # print fn
        try:
            recipe_json = subprocess.check_output([fn, url, "json"])
        except subprocess.CalledProcessError as problem:
            print problem.output
            print problem.returncode
            recipe_json = None

    # sometimes the PHP parse_recipe is too verbose. this corrects that issue.
    recipe_json = recipe_json.rpartition('}')
    recipe_json = recipe_json[0] + recipe_json[1]
    # print recipe_json
    parsed_json = json.loads(recipe_json)
    print parsed_json

    # clean up the ingredients formatting
    if parsed_json['ingredients'][0] is not None:
        parsed_json['ingredients'] = parsed_json['ingredients'][0]['list']
        print parsed_json['ingredients']

    if parsed_json['instructions'][0]['list'] is not None:
        parsed_json['instructions'] = parsed_json['instructions'][0]['list']
        for step in parsed_json['instructions']:
            for sent in find_sentences(step):
                step_list.append(util.sanitize_step(util.handle_fractions(sent.encode(encoding='ascii', errors='ignore'))))

    new_title = util.sanitize_step(parsed_json['title']).encode('ascii','ignore')
    new_recipe = recipe.Recipe(new_title, parsed_json['yield'], parsed_json['ingredients'], step_list, parsed_json['photo_url'])
    new_recipe.tools = find_cooking_tools(new_recipe.instructions, k_base)
    new_recipe.methods = find_cooking_methods(new_recipe.instructions, k_base)

    for i in range(len(new_recipe.ingredients)):
        new_recipe.ingredients[i] = util.sanitize_step(util.handle_fractions(new_recipe.ingredients[i].encode(encoding='utf-8', errors='ignore')))

    for i in range(len(new_recipe.instructions)):
        new_recipe.instructions[i] = util.sanitize_step(new_recipe.instructions[i])

    # find_temps(new_recipe.instructions, k_base)
    # print new_recipe.title, new_recipe.ingredients, new_recipe.instructions
    # print parsed_json['title']
    return new_recipe


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
    print "INGREDIENTS: ", parsed_json['ingredients']
    print "INSTRUCTIONS: ", parsed_json['instructions']

    return

def human_readable_object(recipe_object):
    """prints human-readable version of recipe."""
    # parsed_json = json.loads(recipe_json)
    print "RECIPE OBJECT CREATION: SUCCESS"
    print "TITLE: ", recipe_object.title
    print "YIELD: ", recipe_object.servings
    print "INGREDIENTS: ", recipe_object.ingredients
    print "INSTRUCTIONS: ", recipe_object.instructions
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
    for e in steps:
        e = e.lower()
        for tool in wares:
            if tool in e and tool not in tool_list:
                # print tool
                e = e.replace(tool, '')
                tool_list.append(tool)
    # print tool_list
    return tool_list


def find_cooking_methods(steps, knowledge_base):
    """
    finds cooking methods by comparing step string to cooking_terms.txt.
    Avoids duplicates by replacing matched methods with empty string.
    :param steps:
    :return: method list as list of words
    """
    verbiage = knowledge_base.cooking_terms
    method_list = []
    for step in steps:
        step = step.lower()
        for method in verbiage:
            if method in step and method not in method_list:
                step = step.replace(method, '')
                method_list.append(method)
    # print method_list
    return method_list



def find_sentences(paragraph):
    end = True
    sentences = []
    while end > -1:
        end = find_sentence_end(paragraph)
        if end > -1:
            sentences.append(paragraph[end:].strip())
            paragraph = paragraph[:end]
    sentences.append(paragraph)
    sentences.reverse()

    combined_sent = []
    while sentences:
        if len(sentences[0]) > 120:
            combined_sent.append(sentences[0])
            sentences.remove(sentences[0])
        elif (len(sentences[0]) < 120) and len(sentences) > 1:
            if (len(sentences[0]) < 120) and (len(sentences[1]) < 120):
                combined_sent.append(sentences[0] + " " + sentences[1])
                sentences.remove(sentences[1])
                sentences.remove(sentences[0])
            else:
                combined_sent.append(sentences[0])
                sentences.remove(sentences[0])
        else:
            combined_sent.append(sentences[0])
            sentences.remove(sentences[0])
    return combined_sent


def find_sentence_end(paragraph):
    abbreviations = {'dr.': 'doctor', 'mr.': 'mister', 'bro.': 'brother', 'bro': 'brother', 'mrs.': 'mistress', 'ms.': 'miss', 'jr.': 'junior', 'sr.': 'senior',
                 'i.e.': 'for example', 'e.g.': 'for example', 'vs.': 'versus'}
    terminators = ['.', '!', '?']
    wrappers = ['"', "'", ')', ']', '}']
    [possible_endings, contraction_locations] = [[], []]
    contractions = abbreviations.keys()
    sentence_terminators = terminators + [terminator + wrapper for wrapper in wrappers for terminator in terminators]
    for sentence_terminator in sentence_terminators:
        t_indices = list(find_all(paragraph, sentence_terminator))
        possible_endings.extend(([] if not len(t_indices) else [[i, len(sentence_terminator)] for i in t_indices]))
    for contraction in contractions:
        c_indices = list(find_all(paragraph, contraction))
        contraction_locations.extend(([] if not len(c_indices) else [i + len(contraction) for i in c_indices]))
    possible_endings = [pe for pe in possible_endings if pe[0] + pe[1] not in contraction_locations]
    if len(paragraph) in [pe[0] + pe[1] for pe in possible_endings]:
        max_end_start = max([pe[0] for pe in possible_endings])
        possible_endings = [pe for pe in possible_endings if pe[0] != max_end_start]
    possible_endings = [pe[0] + pe[1] for pe in possible_endings if sum(pe) > len(paragraph) or (sum(pe) < len(paragraph) and paragraph[sum(pe)] == ' ')]
    end = (-1 if not len(possible_endings) else max(possible_endings))
    return end


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)

# def find_temps(steps, knowledge_base):
#     """
#     find oven temps
#     :param steps:
#     :param knowledge_base:
#     :return:
#     """
#     for step in steps:
#         if ("preheat" and "oven") in step:
#             word_list = step.split()
#             for i in range(len(word_list)):
#                 if word_list[i+1] == "degrees":
#                     print word_list[i]
#     return

# def startup():
#     k_base = kb.KnowledgeBase()
#     k_base.load()
#     info = parse_recipe("http://allrecipes.com/recipe/19400/lasagna-alfredo/?internalSource=hn_carousel%2002_Lasagna%20Alfredo&referringId=502&referringContentType=recipe%20hub&referringPosition=carousel%2002")
#     human_readable(info)
#     find_cooking_tools(info['instructions'], k_base)
#     find_cooking_methods(info['instructions'], k_base)
#     return
#
# startup()

# human_readable_object(parse_recipe("http://allrecipes.com/recipe/139726/microwave-mexican-manicotti/", None))

