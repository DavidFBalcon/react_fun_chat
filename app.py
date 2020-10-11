from os.path import join, dirname
from dotenv import load_dotenv
from flask_socketio import SocketIO, send
import os
import flask
import flask_socketio
import flask_sqlalchemy
import json
import requests
import models

app = flask.Flask(__name__)

##BOILER PLATE CODE TO INITIATE SOCKETS
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

#BOILER PLATE CODE TO INSTANTIATE PSQL AND SQLALCHEMY
sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(
    sql_user, sql_pwd)
    
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)

db.init_app(app)
db.app = app
currentUsers = 0

import models

##SENDS CHAT HISTORY TO ALL PARTICIPANTS
def emit_all_history(channel):
    all_history = [{'message': record.plaintext, 'user': record.userName} for record in db.session.query(models.ChatHistory).all()]
    print(all_history)
    socketio.emit(channel, all_history)
    
##SOCKET EVENTS
@socketio.on('connect')
def on_connect():
    global currentUsers
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    currentUsers+=1

@socketio.on('disconnect')
def on_disconnect():
    global currentUsers
    print ('Someone disconnected!')
    currentUsers-=1
    
@socketio.on('retrieve history')
def on_retrieve_history():
    print("Request for chat history recieved.")
    emit_all_history('sent history')

@socketio.on('new message')
def on_new_message(data):
    print("Recieved new data from client: ", data)
    #TODO: SAVE MESSAGE TO DATABASE, THEN SEND MESSAGE
    db.session.add(models.ChatHistory(data['message'], data['user']))
    db.session.commit()
    print("Sending new data to client.")
    socketio.emit('message display', data)
    
    #Checking for bot commands
    ret_data = data['message']
    command_flag = False
    string_check = ret_data.split()
    #BOT COMMANDS
    if(string_check[0] == "!!"):
        if(string_check[1] == "funtranslate"):
            preTranslate = str(ret_data.partition('funtranslate')[2])
            response = requests.get("https://api.funtranslations.com/translate/australian.json?text=" + preTranslate)
            postTranslate = response.json()['contents']['translated']
            db.session.add(models.ChatHistory(postTranslate, "Bot"))
            print("Sending data + funtranslation to client.")
            print(postTranslate)
            socketio.emit('message display', {'message': postTranslate, 'user': "Bot"})
        elif(string_check[1] == "about"):
            msg = "Hi I'm a bot!"
            db.session.add(models.ChatHistory(msg, "Bot"))
            socketio.emit('message display', {'message': msg, 'user': "Bot"})
        elif(string_check[1] == "help"):
            msg = "Here are all the commands I know: about, funtranslate, and placeholder."
            db.session.add(models.ChatHistory(msg, "Bot"))
            socketio.emit('message display', {'message': msg, 'user': "Bot"})
        else:
            print("Unrecognized command recieved.")
            msg="Sorry, I didn't understand that command."
            db.session.add(models.ChatHistory(msg, "Bot"))
            socketio.emit('message display', {'message': msg, 'user': "Bot"})
    db.session.commit()
            


@app.route('/')
def hello():
    models.db.create_all()
    db.session.commit()
    return flask.render_template('index.html')
    
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
