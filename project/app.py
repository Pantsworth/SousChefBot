import sys
import os

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import parser
from flask import Flask, render_template, request
import speech_response

app = Flask(__name__)

    #text input

@app.route('/')
def index():
    return render_template('form.html')


@app.route('/hello')
def hello():
    return render_template('hello.html')



@app.route('/json_test', methods=['GET', 'POST'])
def jsonreq():
    """
    Calls recipe parser and generates a response page.
    :return: an html page containing scraped recipe info
    """
    url = request.form['url']               # acquires URL from form.html
    recipe_object = parser.parse_recipe(url)     # parse html with our parser

    recipe_title = recipe_object.title
    recipe_yield = recipe_object.servings
    recipe_ingredients = recipe_object.ingredients
    recipe_instructions = recipe_object.instructions

    print recipe_object.ingredients
    print recipe_object.instructions
    #
    # query = request.json_test['query-text']
    # print query


    # print url
    # print recipe_title, " ", recipe_ingredients
    return render_template('json_test.html', html_title=recipe_title, html_yield=recipe_yield,
                           html_ingredients=recipe_ingredients, html_instructions=recipe_instructions, jsondata="")


if __name__ == '__main__':
    app.run(debug=True)
