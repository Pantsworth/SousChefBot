from flask import Flask, render_template
import parser
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/json_test', methods=['GET', 'POST'])
def jsonreq():
    """
    Calls recipe parser and generates a response page.
    TODO: Pass URL from frontpage form to this function.
    :return:
    """
    jsondata = parser.parse_recipe("http://allrecipes.com/recipe/219173/simple-beef-pot-roast/")
    recipe_title = jsondata['title']
    recipe_yield = jsondata['yield']
    recipe_ingredients = jsondata['ingredients']
    recipe_steps = jsondata['instructions']

    print recipe_title, " ", recipe_ingredients
    return render_template('json_test.html', html_title=recipe_title, html_yield=recipe_yield,
                           html_ingredients=recipe_ingredients, html_steps=recipe_steps, jsondata=jsondata)


if __name__ == '__main__':
    app.run(debug=True)
