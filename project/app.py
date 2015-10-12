from flask import Flask, render_template, request
import parser
import json

app = Flask(__name__)


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
    :return:
    """
    url = request.form['url']
    jsondata = parser.parse_recipe(url)

    recipe_title = jsondata['title']
    recipe_yield = jsondata['yield']
    recipe_ingredients = jsondata['ingredients']
    recipe_steps = jsondata['instructions']

    print recipe_title, " ", recipe_ingredients
    return render_template('json_test.html', html_title=recipe_title, html_yield=recipe_yield,
                           html_ingredients=recipe_ingredients, html_steps=recipe_steps, jsondata=jsondata)


if __name__ == '__main__':
    app.run(debug=True)
