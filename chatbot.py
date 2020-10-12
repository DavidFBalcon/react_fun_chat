import flask_sqlalchemy
from flask_socketio import SocketIO, send
import models
import requests
from pprint import pprint
from jikanpy import Jikan

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
        try:
            preTranslate = str(ret_data.partition('funtranslate')[2])
            response = requests.get("https://api.funtranslations.com/translate/australian.json?text=" + preTranslate)
            postTranslate = response.json()['contents']['translated']
            self.msg=postTranslate
            return({'message': self.msg, 'user': "Bot"})
        except:
            self.msg = "Sorry! You either did not provide anything to translate, or your input was malformed."
            return({'message': self.msg, 'user': 'Bot'})
            
    def dad(self):
        response=requests.get("https://icanhazdadjoke.com/", headers={'Accept': 'application/json'})
        self.msg=response.json()['joke']
        return({'message': self.msg, 'user': 'Bot'})
        
    def about(self):
        self.msg = "Hi I'm a bot! I may be primitive, but I'm trying my best. My about command tells you about me, you can use funtranslate to do some weird translations, I can tell dad jokes, and give you specific anime information with !! anime {your_anime}"
        return({'message': self.msg, 'user': 'Bot'})
        
    def bot_help(self):
        self.msg = "Here are all the commands I know: about, funtranslate, dad, and anime."
        return({'message': self.msg, 'user': 'Bot'})
        
    def unknown(self):
        self.msg = "Sorry, I didn't understand that command."
        return({'message': self.msg, 'user': 'Bot'})
        
    def anime_search(self, anime):
        jikan = Jikan()
        try:
            toSearch = str(anime.partition('anime')[2])
            results = jikan.search(search_type="anime", query=toSearch)['results'][0]
            if(len(results)==0):
                self.msg = "Sorry, we couldn't find that anime!"
                return({'message': self.msg, 'user': 'Bot'})
            self.msg = "Title: " + results['title'] + "<br></br>Score: " + str(results['score']) + "<br></br>Summary: " + results['synopsis'][:100] + "..."
            return({'message': self.msg, 'user': 'Bot'})
        except:
            self.msg = "Sorry! We either couldn't find that anime, did not provide an anime at all, or you've provided malformed input."
            return({'message': self.msg, 'user': 'Bot'})