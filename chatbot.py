import flask_sqlalchemy
from flask_socketio import SocketIO, send
import models
import requests

class CoolBot:
    def __init__(self):
        self.msg=""
        
    def isCommand(self, message):
        ret_data = message
        string_check = ret_data.split()
        if(string_check[0] == "!!"):
            return True
        else:
            return False
        
    def funtranslate(self, ret_data):
            preTranslate = str(ret_data.partition('funtranslate')[2])
            response = requests.get("https://api.funtranslations.com/translate/australian.json?text=" + preTranslate)
            postTranslate = response.json()['contents']['translated']
            self.msg=postTranslate
            return({'message': self.msg, 'user': "Bot"})
            
    def dad(self):
        response=requests.get("https://icanhazdadjoke.com/", headers={'Accept': 'application/json'})
        self.msg=response.json()['joke']
        return({'message': self.msg, 'user': 'Bot'})
        
    def about(self):
        self.msg = "Hi I'm a bot! I may be primitive, but I'm trying my best."
        return({'message': self.msg, 'user': 'Bot'})
        
    def bot_help(self):
        self.msg = "Here are all the commands I know: about, funtranslate, dad, and else."
        return({'message': self.msg, 'user': 'Bot'})
        
    def unknown(self):
        self.msg = "Sorry, I didn't understand that command."
        return({'message': self.msg, 'user': 'Bot'})