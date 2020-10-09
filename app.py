import os
import flask
import flask_socketio
import json
from flask_socketio import SocketIO, send

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

temp_data=[]

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    #TODO: ASSIGN USERNAME AND USER HISTORY TO UPDATE STATE.

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new message')
def on_new_message(data):
    print("Recieved new data from client: ", data)
    #TODO: SAVE MESSAGE TO DATABASE, THEN SEND MESSAGE: TEMPORARY STORAGE 
    temp_data.append(data['message'])
    print("Sending new data to client.")
    socketio.emit('message display', {'messages': temp_data})

@app.route('/')
def hello():
    return flask.render_template('index.html')
    
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
