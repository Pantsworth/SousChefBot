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