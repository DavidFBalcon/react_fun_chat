import os
import flask
import flask_socketio
import json
from flask_socketio import SocketIO, send
import requests

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
    #TODO: PROVIDE CHAT HISTORY TO FRESH CONNECTIONS

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    
@socketio.on('retrieve history')
def on_retrieve_history():
    print("Request for chat history recieved.")
    socketio.emit('sent history', {'messages': temp_data})

@socketio.on('new message')
def on_new_message(data):
    print("Recieved new data from client: ", data)
    #TODO: SAVE MESSAGE TO DATABASE, THEN SEND MESSAGE: TEMPORARY STORAGE 
    temp_data.append(data['message'])
    ret_data = data['message']
    print("Sending new data to client.")
    socketio.emit('message display', {'messages': data['message']})
    
    #Checking for bot commands
    command_flag = False
    string_check = ret_data.split()
    #BOT COMMANDS
    if(string_check[0] == "!!"):
        if(string_check[1] == "funtranslate"):
            preTranslate = str(ret_data.partition('funtranslate')[2])
            response = requests.get("https://api.funtranslations.com/translate/australian.json?text=" + preTranslate)
            postTranslate = response.json()['contents']['translated']
            temp_data.append(postTranslate)
            print("Sending data + funtranslation to client.")
            print(postTranslate)
            socketio.emit('message display', {'messages': postTranslate})
        elif(string_check[1] == "about"):
            msg = "Hi I'm a bot!"
            temp_data.append(msg)
            socketio.emit('message display', {'messages': msg})
        elif(string_check[1] == "help"):
            msg = "Here are all the commands I know: about, funtranslate, and placeholder."
            temp_data.append(msg)
            socketio.emit('message display', {'messages': msg})
        else:
            print("Unrecognized command recieved.")
            msg="Sorry, I didn't understand that command."
            temp_data.append(msg)
            socketio.emit('message display', {'messages': msg})
            


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
