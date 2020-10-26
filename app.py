'''
Python Appeasment
'''
import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_socketio
import flask_sqlalchemy
import requests
import validators
from google.oauth2 import id_token
from google.auth.transport import requests

app = flask.Flask(__name__)

##BOILER PLATE CODE TO INITIATE SOCKETS
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

# BOILER PLATE CODE TO INSTANTIATE PSQL AND SQLALCHEMY

database_uri = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)

db.init_app(app)
db.app = app
CURRENT_USERS = 0

import models
import chatbot

##SENDS CHAT HISTORY TO ALL PARTICIPANTS
def emit_all_history(channel):
    '''
    Emits all history along channel
    '''
    all_history = [
        {
            "message": record.plaintext,
            "user": record.userName,
            "pfp_url": record.pfp_url,
        }
        for record in db.session.query(models.ChatHistory).all()
    ]
    socketio.emit(channel, all_history)

def push_new_user_to_db(ident, name, email):
    '''
    Pushes new user to database.
    '''
    db.session.add(models.AuthUser(ident, name, email))
    db.session.commit()


def check_images(to_check, img_array):
    '''
    Checks if valid image in message.
    '''
    extensions = [".jpg", ".png", ".gif"]
    has_image = False
    i=0
    for word in to_check:
        if validators.url(word):
            has_image = True
            if word[-4:] in extensions:
                img_array.append(word)
            to_check[i] = "<a href=" + '"' + to_check[i] + '">' + to_check[i] + "</a>"
            i+=1
    return has_image


##SOCKET EVENTS
@socketio.on("connect")
def on_connect():
    '''
    Runs on connect.
    '''
    print("Someone connected!")
    socketio.emit("connected", {"test": "Connected"})


@socketio.on("disconnect")
def on_disconnect():
    '''
    Runs on disconnect.
    '''
    global CURRENT_USERS
    print("Someone disconnected!")
    if CURRENT_USERS > 0:
        CURRENT_USERS -= 1
    socketio.emit("user change", CURRENT_USERS)


@socketio.on("user update")
def on_user_update():
    '''
    Generates a user count update and emits.
    '''
    global CURRENT_USERS
    socketio.emit("user change", CURRENT_USERS)


@socketio.on("new google user")
def on_new_google_user(data):
    '''
    Runs verification on google token.
    '''
    global CURRENT_USERS
    print("Beginning to authenticate data: ", data)
    sid = flask.request.sid
    try:
        idinfo = id_token.verify_oauth2_token(
            data["idtoken"],
            requests.Request(),
            "698177391473-sfucar7t4qoum5rpt14mso7vkbuh1lao.apps.googleusercontent.com",
        )
        userid = idinfo["sub"]
        print("Verified user. Proceeding to check database.")
        exists = (
            db.session.query(models.AuthUser.id).filter_by(id=userid).scalar()
            is not None
        )
        if not exists:
            push_new_user_to_db(userid, data["name"], data["email"])
        print("Updating CURRENT_USERS ", CURRENT_USERS)
        CURRENT_USERS += 1
        print("Current users in room: ", CURRENT_USERS)
        socketio.emit("Verified", data["name"], room=sid)
        return True
    except ValueError:
        # Invalid token
        print("Could not verify token.")
        return False


@socketio.on("retrieve history")
def on_retrieve_history():
    '''
    Listens for history requests from front-end.
    '''
    print("Request for chat history recieved.")
    emit_all_history("sent history")


# SOCKET EVENT FOR A NEW MESSAGE
@socketio.on("new message")
def on_new_message(data):
    '''
    Runs on recieving new message to process.
    '''
    print("Recieved new data from client: ", data)
    # URL VALIDATION
    ret_data = data["message"]
    string_check = ret_data.split()
    img = []
    check_images(string_check, img)
    ret_data = " ".join(string_check)
    # SAVING MESSAGE TO DATABASE AND SENDING TO CLIENT FOR DISPLAY
    db.session.add(models.ChatHistory(ret_data, data["user"], data["pfp_url"]))
    db.session.commit()
    print("Sending new data to client.")
    socketio.emit(
        "message display",
        {"message": ret_data, "user": data["user"], "pfp_url": data["pfp_url"]},
    )

    # CHECKING IF BOT COMMAND IS TRUE AND INITIALIZING BOT
    funbot = chatbot.CoolBot()
    # CHECKING FOR BOT COMMANDS
    to_emit = funbot.is_command(ret_data, "")
    # COMMIT AND SEND
    if funbot.command_flag:
        db.session.add(models.ChatHistory(funbot.msg, "Bot", funbot.pfp_url))
        db.session.commit()
        socketio.emit("message display", to_emit)
    # CHECKING FOR ANY IMAGES TO DISPLAY AND DISPLAYS THEM ALL WITH BOT
    elif len(img) != 0:
        for link in img:
            to_emit = funbot.is_command(ret_data, link)
            db.session.add(models.ChatHistory(funbot.msg, "Bot", funbot.pfp_url))
            db.session.commit()
            socketio.emit("message display", to_emit)


@app.route("/")
def hello():
    '''
    Runs at page-load.
    '''
    models.db.create_all()
    db.session.commit()
    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
    