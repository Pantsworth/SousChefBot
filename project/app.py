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
from flask import Flask, render_template, request, session, current_app
import time
from threading import Thread
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import speech_response, speechtest2


app = Flask(__name__)
app.config['SECRET_KEY'] = "q"
socketio_app = SocketIO(app, async_mode=async_mode)
speech_thread = None
socket_thread = None
url = ""


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

def demo_function():
    print "in the demo function"
    socketio_app.emit('my response',
             {'data': "ew", 'count': 1})
    # with app.test_request_context('/recipe', method='POST', namespace = "/test"):
    # print "app context is: " + current_app.name
    url = "http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"        # acquires URL from form.html
    recipe = parser.parse_recipe(url)
    speech_engine = speech_response.VoiceEngine()
    speech_engine.say_this("This is a recipe for: " + recipe.title)
    result = ""
    response = ""
    # count = 0
    # while True:
    #     time.sleep(3)
    #     count += 1
    #     socketio_app.emit('my response',
    #                   {'data': 'Generated. Sleeping for 3.', 'count': count},
    #                   namespace='/test')
    #

    while ("stop" not in response):
        print "starting speech loop"
 #       socketio_app.emit('my response',
 #            {'data': "starting speech loop", 'count':1}, namespace='/test')
        result = speechtest2.run_speech_rec()
        if result == "Response Failed":
          response = "I'm sorry, I didn't get that. Can you repeat your command?" 
          speech_engine.say_this(response)
          print response
          socketio_app.emit('my response',
              {'data': "SousChefBot: " + response, 'count':4}, namespace='/test')
        else:
            query = result[u'outcomes'][0][u'_text']
            response = speech_response.choose_response(recipe, result, None)
            speech_engine.say_this(response)
            print response
            socketio_app.emit('my response',
                {'data': "You: " + query, 'count':4}, namespace='/test')
            socketio_app.emit('my response',
                {'data': "SousChefBot: " + response, 'count':4}, namespace='/test')
        # result = "stop"
        # response = "stopping"


@app.route('/')
def jsonreq():
    print "index"

    return render_template('form.html')


@app.route('/recipe')
def index():

    global socket_thread
    global speech_thread
    global url

    if socket_thread is None:
        socket_thread = Thread(target=background_thread)
        socket_thread.daemon = True
        socket_thread.start()
        print "started bkg thread"

    if speech_thread is None:
        speech_thread = Thread(target=demo_function)
        speech_thread.daemon = False
        speech_thread.start()
        print "started speech thread"


    print "rendering the page?"
    url = "http://allrecipes.com/recipe/219173/simple-beef-pot-roast/"        # acquires URL from form.html
    recipe_object = parser.parse_recipe(url)     # parse html with our parser

    recipe_title = recipe_object.title
    recipe_yield = recipe_object.servings
    recipe_ingredients = recipe_object.ingredients
    recipe_instructions = recipe_object.instructions

    return render_template('recipe.html', html_title=recipe_title, html_yield=recipe_yield,
                           html_ingredients=recipe_ingredients, html_instructions=recipe_instructions, jsondata="")


@socketio_app.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio_app.on('speech_rec', namespace='/test')
def speech_rec_start(message):
    print "Starting Speech Recognition"
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': "Starting Speech Recognition", 'count': session['receive_count']})
    demo_function()


@socketio_app.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio_app.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio_app.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio_app.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio_app.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio_app.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio_app.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Say "Computer" when you want me to listen! ', 'count': 0})


@socketio_app.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio_app.run(app, debug=True)
