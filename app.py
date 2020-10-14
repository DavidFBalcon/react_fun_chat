from os.path import join, dirname
from dotenv import load_dotenv
from flask_socketio import SocketIO, send
import os
import flask
import flask_socketio
import flask_sqlalchemy
import json
import requests
from google.oauth2 import id_token
from google.auth.transport import requests

app = flask.Flask(__name__)

##BOILER PLATE CODE TO INITIATE SOCKETS
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

#BOILER PLATE CODE TO INSTANTIATE PSQL AND SQLALCHEMY

database_uri = os.environ['DATABASE_URL']
    
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)

db.init_app(app)
db.app = app
currentUsers = 0

import models
import chatbot

##SENDS CHAT HISTORY TO ALL PARTICIPANTS
def emit_all_history(channel):
    all_history = [{'message': record.plaintext, 'user': record.userName} for record in db.session.query(models.ChatHistory).all()]
    socketio.emit(channel, all_history)
    
def push_new_user_to_db(id, name, email):
    db.session.add(models.AuthUser(id, name, email));
    db.session.commit();
    
##SOCKET EVENTS
@socketio.on('connect')
def on_connect():
    global currentUsers
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })

@socketio.on('disconnect')
def on_disconnect():
    global currentUsers
    print ('Someone disconnected!')
    currentUsers-=1
    socketio.emit('user change', currentUsers)
    
@socketio.on('user update')
def on_user_update():
    global currentUsers
    print(currentUsers)
    socketio.emit('user change', currentUsers)
    
@socketio.on('new google user')
def on_new_google_user(data):
    global currentUsers
    print("Beginning to authenticate data: ", data)
    try:
        idinfo = id_token.verify_oauth2_token(data['idtoken'], requests.Request(), "698177391473-sfucar7t4qoum5rpt14mso7vkbuh1lao.apps.googleusercontent.com")
        userid = idinfo['sub']
        print("Verified user. Proceeding to check database.")
        exists = db.session.query(models.AuthUser.id).filter_by(id=userid).scalar() is not None
        if(not exists):
            push_new_user_to_db(userid, data['name'], data['email'])
        currentUsers+=1
        socketio.emit('Verified', data['name'])
    except ValueError:
    # Invalid token
        print("Could not verify token.")
        pass
    
@socketio.on('retrieve history')
def on_retrieve_history():
    print("Request for chat history recieved.")
    emit_all_history('sent history')
    

#SOCKET EVENT FOR A NEW MESSAGE
@socketio.on('new message')
def on_new_message(data):
    print("Recieved new data from client: ", data)
    
    #SAVING MESSAGE TO DATABASE AND SENDING TO CLIENT FOR DISPLAY
    db.session.add(models.ChatHistory(data['message'], data['user']))
    db.session.commit()
    print("Sending new data to client.")
    socketio.emit('message display', data)
    
    #CHECKING IF BOT COMMAND IS TRUE AND INITIALIZING BOT
    funbot = chatbot.CoolBot()
    ret_data = data['message']
    string_check = ret_data.split()
    to_emit = {}
    #BOT COMMANDS
    if(funbot.isCommand(data['message'])):
        ##FUNTRANSLATE
        if(string_check[1] == "funtranslate"):
            funbot.funtranslate(ret_data)
            to_emit = funbot.funtranslate(ret_data)
        ##ABOUT
        elif(string_check[1] == "about"):
            funbot.about()
            to_emit = funbot.about()
        ##HELP
        elif(string_check[1] == "help"):
            funbot.bot_help()
            to_emit = funbot.bot_help()
        ##DAD JOKE API
        elif(string_check[1] == "dad"):
            funbot.dad()
            to_emit=funbot.dad()
        elif(string_check[1] == "anime"):
            funbot.anime_search(ret_data)
            to_emit=funbot.anime_search(ret_data)
        ##UNKNOWN COMMAND
        else:
            print("Unrecognized command recieved.")
            funbot.unknown()
            to_emit = funbot.unknown()
        
        #COMMIT AND SEND
        db.session.add(models.ChatHistory(funbot.msg, "Bot"))
        db.session.commit()
        socketio.emit('message display', to_emit)


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
