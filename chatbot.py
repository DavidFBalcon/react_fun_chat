import requests
import json
from pprint import pprint
from jikanpy import Jikan

class CoolBot:
    def __init__(self):
        self.msg=""
        self.pfp_url="<img src=" + "\"./botpfp.png\">"
        self.commandFlag = False
        
    def funtranslate(self, ret_data):
        try:
            preTranslate = str(ret_data.partition('funtranslate')[2])
            if(len(preTranslate)==0):
                self.msg="Please input a sentence to translate after 'funtranslate.'"
            else:
                response = requests.get("https://api.funtranslations.com/translate/australian.json?text=" + preTranslate)
                postTranslate = response.json()['contents']['translated']
                self.msg=postTranslate
            return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
        except:
            self.msg = "Sorry! You either did not provide anything to translate, or your input was malformed."
            return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
            
    def dad(self):
        response=requests.get("https://icanhazdadjoke.com/", headers={'Accept': 'application/json'})
        self.msg=response.json()['joke']
        return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
        
    def about(self):
        self.msg = "Hi I'm a bot! I may be primitive, but I'm trying my best. My about command tells you about me, you can use funtranslate to do some weird translations, I can tell dad jokes, and give you specific anime information with !! anime {your_anime}"
        return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
        
    def bot_help(self):
        self.msg = "Here are all the commands I know: about, funtranslate, dad, and anime."
        return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
        
    def unknown(self):
        self.msg = "Sorry, I didn't understand that command."
        return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
        
    def anime_search(self, anime):
        jikan = Jikan()
        try:
            toSearch = str(anime.partition('anime')[2])
            if(len(toSearch)==0):
                raise Exception()
            results = jikan.search(search_type="anime", query=toSearch)['results'][0]
            if(len(results)==0):
                raise Exception()
            self.msg = "Title: " + results['title'] + "<br></br>Score: " + str(results['score']) + "<br></br>Summary: " + results['synopsis'][:100] + "..."
            return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
        except:
            self.msg = "Sorry! We either couldn't find that anime, did not provide an anime at all, or you've provided malformed input."
            return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
            
    def img_render(self, img):
        img_tag = "<img src=" + "\"" + img + "\">"
        self.msg = img_tag
        return({'message': self.msg, 'user': "Bot", 'pfp_url': self.pfp_url})
        
    def isCommand(self, message, imgLink):
        ret_data = message
        string_check = ret_data.split()
        if(string_check[0] == "!!"):
            self.commandFlag = True
            if(string_check[1] == "funtranslate"):
                return self.funtranslate(message)
            ##ABOUT
            elif(string_check[1] == "about"):
                return self.about()
            ##HELP
            elif(string_check[1] == "help"):
                return self.bot_help()
            ##DAD JOKE API
            elif(string_check[1] == "dad"):
                return self.dad()
            ##anime
            elif(string_check[1] == "anime"):
                return self.anime_search(message)
            ##UNKNOWN COMMAND
            else:
                print("Unrecognized command recieved.")
                return self.unknown()
        elif(imgLink != ""):
                return self.img_render(imgLink)
        else:
            return False
    