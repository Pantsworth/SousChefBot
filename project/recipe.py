__author__ = 'Michael Nowakowski'
# Based on code from Adam Snyder, Kristin Amaddio, and Neal Kfoury

class Recipe:

    def __init__(self, title='', servings=0, ingredients=None, instructions=None):
        self.title = title
        self.servings = servings
        self.ingredients = ingredients
        self.instructions = instructions
        self.primary_method = 'none'
        self.methods = []
        self.tools = []
        self.current_step = 0
        # if ingredients:
        #     self.add_ingredients(ingredients)
        # if instructions:
        #     self.add_steps(instructions)

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

    def change_servings(self, new_servings):
        self.servings = new_servings

    def parse_json(self, json):
        self.title = json['title']
        self.ingredients = json['ingredients']
        self.instructions = json['instructions']

    def next_step(self):
        if self.current_step < len(self.instructions):
            self.current_step = self.current_step + 1

    def previous_step(self):
        if self.current_step is not 0:
            self.current_step = self.current_step - 1

    def find_tools(self):
        if self.tools == []:
            return

    def print_recipe(self):
        print "RECIPE OBJECT CREATION: SUCCESS"
        print "TITLE: ", self.title
        print "YIELD: ", self.servings
        print "INGREDIENTS: ", self.ingredients
        print "INSTRUCTIONS: ", self.instructions