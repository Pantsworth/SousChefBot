__author__ = 'Michael Nowakowski'
# Based on code from Adam Snyder, Kristin Amaddio, and Neal Kfoury

class Recipe:

    def __init__(self, title='', ingredients=None, instructions=None):
        self.title = title
        self.ingredients = []
        self.instructions = []
        self.primary_method = 'none'
        self.methods = []
        self.tools = []
        self.current_step = 0
        if ingredients:
            self.add_ingredients(ingredients)
        if instructions:
            self.add_steps(instructions)

    def add_ingredients(self, ingredients_list):
        self.ingredients.extend(ingredients_list)

    def modify_ingredients(self, new_ingredients_list):
        self.ingredients = new_ingredients_list

    def modify_steps(self, new_steps):
        self.instructions = new_steps

    def replace_ingredient_in_steps(self, old_food_name, new_food_name):
        for step_num in range(len(self.instructions)):
            self.instructions[step_num] = self.instructions[step_num].lower()
            self.instructions[step_num] = self.instructions[step_num].replace(old_food_name, new_food_name)

    def add_steps(self, steps_list):
        self.instructions.extend(steps_list)

    def change_title(self, new_title):
        self.title = new_title

    def parse_json(self, json):
        self.title = json['title']
        self.ingredients = json['ingredients']
        self.instructions = json['instructions']
