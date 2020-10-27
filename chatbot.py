'''
Chatbot definition
chatbot.py
'''
# pylint: disable=too-many-return-statements
from jikanpy import Jikan
import requests



class CoolBot:
    '''
    Class definition for bot.
    '''
    def __init__(self):
        self.msg = ""
        self.pfp_url = "<img src=" + '"./botpfp.png">'
        self.command_flag = False

    def funtranslate(self, ret_data):
        '''
        Runs the funtranslate API on message.
        '''
        try:
            pre_translate = str(ret_data.partition("funtranslate")[2])
            if len(pre_translate) == 0:
                raise ValueError()
            response = requests.get(
                "https://api.funtranslations.com/translate/australian.json?text="\
                + pre_translate
                )
            post_translate = response.json()["contents"]["translated"]
            self.msg = post_translate
            return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}
        except ValueError:
            self.msg = "Sorry! You either did not provide anything to translate,\
 or your input was malformed."
            return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}

    def dad(self):
        '''
        Runs the dad-joke API on message.
        '''
        response = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        )
        self.msg = response.json()["joke"]
        return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}

    def about(self):
        '''
        Returns bot bio.
        '''
        self.msg = "Hi I'm a bot! I may be primitive, but I'm trying my best.\
 My about command tells you about me, you can use funtranslate to do some weird\
 translations, I can tell dad jokes, and give you specific anime information\
 with !! anime {your_anime}"
        return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}

    def bot_help(self):
        '''
        Returns bot command list.
        '''
        self.msg = (
            "Here are all the commands I know: about, funtranslate, dad, and anime."
        )
        return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}

    def unknown(self):
        '''
        Unknown commands.
        '''
        self.msg = "Sorry, I didn't understand that command."
        return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}

    def anime_search(self, anime):
        '''
        Runs the jikan MyAnimeList API on message.
        '''
        jikan = Jikan()
        try:
            to_search = str(anime.partition("anime")[2])
            if len(to_search) == 0:
                raise ValueError
            results = jikan.search(search_type="anime", query=to_search)["results"][0]
            if len(results) == 0:
                raise ValueError
            self.msg = (
                "Title: "
                + results["title"]
                + "<br></br>Score: "
                + str(results["score"])
                + "<br></br>Summary: "
                + results["synopsis"][:100]
                + "..."
            )
            return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}
        except ValueError:
            self.msg = "Sorry! We either couldn't find that anime, did not provide\
 an anime at all, or you've provided malformed input."
            return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}

    def img_render(self, img):
        '''
        Renders detected images.
        '''
        img_tag = "<img src=" + '"' + img + '">'
        self.msg = img_tag
        return {"message": self.msg, "user": "Bot", "pfp_url": self.pfp_url}

    def is_command(self, message, img_link):
        '''
        Takes in messages and routes to proper function call.
        '''
        ret_data = message
        string_check = ret_data.split()
        if string_check[0] == "!!":
            self.command_flag = True
            if string_check[1] == "funtranslate":
                return self.funtranslate(message)
            ##ABOUT
            if string_check[1] == "about":
                return self.about()
            ##HELP
            if string_check[1] == "help":
                return self.bot_help()
            ##DAD JOKE API
            if string_check[1] == "dad":
                return self.dad()
            ##anime
            if string_check[1] == "anime":
                return self.anime_search(message)
            ##UNKNOWN COMMAND
            print("Unrecognized command recieved.")
            return self.unknown()
        if img_link != "":
            return self.img_render(img_link)
        return {"message": False, "user": "Bot", "pfp_url": self.pfp_url}
