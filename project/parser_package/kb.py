__author__ = 'DoctorWatson'
import util
import os


class KnowledgeBase:
    def __init__(self):
        self.foods = []
        self.cooking_terms = set()
        self.cooking_wares = set()
        self.measurements = {}
        self.common_substitutions = []
        self.italian_spices_subs = []
        self.asian_spices_subs = []
        self.mexican_spices_subs = []
        self.italian_spices_list = []
        self.mexican_spices_list = []
        self.asian_spices_list = []
        self.italian_to_mexican_list = []
        self.italian_to_asian_list = []
        self.asian_to_italian_list = []
        self.asian_to_mexican_list = []
        self.mexican_to_italian_list = []
        self.mexican_to_asian_list = []
        self.neutral_to_asian_list = []
        self.neutral_to_mexican_list = []
        self.neutral_to_italian_list = []
        self.vegetarian_substitutions = []
        self.vegan_substitutions = []

    def load(self):
        """
        Loads parsed knowledge base data from modifiable data text files into global fields
        Typically called right after object initialization
        """
        # self._load_foods()
        # util.vprint('Loading cooking terminology')
        self._load_cooking_terms()
        self._load_cooking_wares()
        # self._load_measurements()
        # self._load_common_substitutions()
        # self._load_style_tags()
        # self._load_style_substitutions()

    def _load_cooking_terms(self):
        self.cooking_terms = set(read_txt_lines_into_list('kb_data/cooking_terms.txt'))

    def _load_cooking_wares(self):
        self.cooking_wares = set(read_txt_lines_into_list('kb_data/cooking_wares.txt'))



def read_txt_lines_into_list(file_name):
    """
    Given a filename, returns a list with each cell being a line from the file
    Lines that have no content or begin with a '#' (comments) are skipped
    Converts to lowercase
    :param file_name: filename of source
    :return: list of file lines
    """
    result = []
    with open(util.relative_path(file_name)) as source_file:
        source_lines = source_file.readlines()
        for line in source_lines:
            if len(line) and line[-1] == '\n':
                line = line[:-1]
            if len(line) and line[0] != '#':
                result.append(line.lower())
    return result


def read_specific_lines(file_name, start, end):
    """
    Given a filename, returns a list with each cell being a line from the file
    starting with start tag and ending with end tag
    Converts to lowercase
    :param file_name: filename of source
    :return: list of file lines
    """
    result = []
    read = False
    with open(util.relative_path(file_name)) as source_file:
        source_lines = source_file.readlines()
        for line in source_lines:
            if len(line) and line[-1] == '\n':
                line = line[:-1]
            if line == start:
                read = True
            if line == end:
                read = False
                break
            if len(line) and line[0] != '#' and read:
                result.append(line.lower())
    return result


