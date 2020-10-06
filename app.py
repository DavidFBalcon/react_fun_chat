import os
import flask
import flask_socketio
from flask_socketio import SocketIO, send

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

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
