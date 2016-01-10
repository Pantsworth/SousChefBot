async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()


import parser
from flask import Flask, render_template, request, session, copy_current_request_context, current_app
import time
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import speech_response, speechtest2
from parser_package import kb


app = Flask(__name__)
app.config['SECRET_KEY'] = "q"
socketio_app = SocketIO(app, async_mode=async_mode)
speech_thread = None
socket_thread = None
recipe = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    """while True:
        time.sleep(5)
        count += 1
        socketio_app.emit('my response',
                      {'data': 'Generated. Sleeping for 5.', 'count': count},
                      namespace='/test')
    """

def provide_response(query):
    response = ""
    print('received json: ' + query)
    # while "computer" in clean_string:
    clean_string = query['data'].replace("computer", "")
    print clean_string
    wit_response = speech_response.wit_call(clean_string)
    print wit_response
    response = speech_response.choose_response(recipe, wit_response, None)
    print response
    emit('saythis', {'data': response})


def demo_function(parsed_recipe, k_base, url):
    # with app.test_request_context('/recipe', method='POST', namespace = "/test"):
    # print "app context is: " + current_app.name
    preamble = False
    global recipe

    if parsed_recipe is not None:
        recipe = parsed_recipe
    else:
        print "Recipe object not found. Generating object."
        recipe = parser.parse_recipe(url, k_base)
    # speech_engine = speech_response.VoiceEngine()
    emit('saythis', {"data": "This is a recipe for: " + recipe.title})
    # speech_engine.say_this("This is a recipe for: " + recipe.title)
    if preamble:
        time.sleep(1)
        # speech_engine.say_this("The first step is: " + recipe.instructions[0])
        emit('saythis', {"data": "The first step is: " + recipe.instructions[0]})
        time.sleep(1)
        emit('saythis', {"data": "Say Computer, Computer, to get me to wake up"})
        # speech_engine.say_this("Say Computer, Computer, to get me to wake up")
        time.sleep(2)

   # while ("stop" not in response):
   #  while True:
   #      emit('saythis', {"data": "Say Computer, Computer, to get me to wake up"})
   #      # speech_engine.say_this("Listening")
   #      # result = speechtest2.run_speech_rec(speech_engine)
   #
   #      if result == "Response Failed":
   #          response = "I'm sorry, I did not get that. Can you repeat your command?"
   #          speech_engine.say_this(response)
   #          socketio_app.emit('my response',
   #            {'data': "SousChefBot: " + response, 'count':4}, namespace='/test')
   #      else:
   #          query = result[u'outcomes'][0][u'_text']
   #          response = speech_response.choose_response(recipe, result, None)
   #          socketio_app.emit('my response',
   #            {'data': "You: " + query, 'count':4}, namespace='/test')
   #          socketio_app.emit('my response',
   #            {'data': "SousChefBot: " + response, 'count':4}, namespace='/test')
   #          speech_engine.say_this(response)
   #
   #          if response == "stopping":
   #              break
   #      eventlet.sleep(0)


@app.route('/')
def jsonreq():
    # print "index"
    return render_template('form.html')


@app.route('/recipe', methods=['POST'])
def index():

    global socket_thread
    global speech_thread
    global recipe

    k_base = kb.KnowledgeBase()
    k_base.load()
    #url = "http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"        # acquires URL from form.html
    url = request.form['url']
    # print "this is url from form " + url
    recipe_object = parser.parse_recipe(url, k_base)     # parse html with our parser
    recipe = recipe_object
    #
    # if speech_thread is None:
    #     eventlet.greenthread.spawn_after(2, demo_function, recipe_object, k_base, url)
    #     print "started speech thread"
        # speech_thread = Thread(target=demo_function)
        # speech_thread.daemon = False
        # speech_thread.spawn_after(5)


    print "Rendering Recipe Page"

    recipe_title = recipe_object.title
    recipe_yield = recipe_object.servings
    recipe_ingredients = recipe_object.ingredients
    recipe_instructions = recipe_object.instructions
    photo_url = recipe_object.photo_url

    return render_template('recipe-speech.html', html_title=recipe_title, html_yield=recipe_yield,
                           html_ingredients=recipe_ingredients, html_instructions=recipe_instructions, jsondata="", html_photo=photo_url)

@socketio_app.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()
#
#
# @socketio_app.on('connect', namespace='/test')
# def test_connect():
#     emit('my response', {'data': 'Say "Computer" when you want me to listen! ', 'count': 0})


@socketio_app.on('audio', namespace='/test')
def find_response(json):
    global recipe
    response = ""
    try:
        if "computer" in json['data']:
            print('received json: ' + json['data'])
            # while "computer" in clean_string:
            clean_string = json['data'].replace("computer", "")
            print clean_string
            wit_response = speech_response.wit_call(clean_string)
            print wit_response
            response = speech_response.choose_response(recipe, wit_response, None)
            print response
            emit('saythis', {'data': response})
    except:
        print "too fast too furious"


@socketio_app.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

def main():
    socketio_app.run(app, debug=True)
#
#
if __name__ == '__main__':
    socketio_app.run(app, debug=False)
