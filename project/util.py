import os


def relative_path(path):
    """
    Get file path relative to calling script's directory
    :param path: filename or file path
    :return: full path name, relative to script location
    """
    return os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), path)


def sanitize_step(step):
    """
    :param step: takes step string from instructions
    :return: sanitized version for speech
    """
    new_step = step
    bad_char_list = [";", "(", ")"]
    for char in bad_char_list:
        new_step = new_step.replace(char, " ")

    return new_step


def handle_fractions(string):
    """

    :param string: string of some kind
    :return: string with all fractions replaced with natural language equivalents
    """
    index = string.find('/')
    result = string

    while index is not -1:
        denominator = index+1
        result = result.replace(result[index:index+2], denom(result[denominator]))
        index = result.find('/')
        # print index
        # print result
    return result


def denom(x):
    return {
        '2': " half",
        '3': " third",
        '4': " fourth",
        '5': " fifth",
        '6': " sixth",
        '7': " seventh"
    }.get(x, " ")

handle_fractions("1/2 cup tomatoes, 1/4 tsp")
