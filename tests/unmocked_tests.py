'''
    chatbot_test.py
    
    This file tests all methods in chatbot.py.
'''

import unittest
import chatbot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_LENGTH = "length"
KEY_MESSAGE = "message"
KEY_USER = "user"
KEY_PFP = "pfp_url"

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "Hi I'm a bot! I may be primitive, but I'm trying my best. My about command tells you about me, you can use funtranslate to do some weird translations, I can tell dad jokes, and give you specific anime information with !! anime {your_anime}",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + "\"./botpfp.png\">",
                }
            },
            {
                KEY_INPUT: "!! about",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "Here are all the commands I know: about, funtranslate, dad, and anime.",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + "\"./botpfp.png\">",
                }
            },
            {
                KEY_INPUT: "!! FWEVWIO",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "Sorry, I didn't understand that command.",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + "\"./botpfp.png\">",
                }
            },
            
        ]
        
        self.failure_test_params = [
            # TODO HW13
        ]


    def test_parse_message_success(self):
        for test in self.success_test_params:
            response = chatbot.CoolBot().
    def test_parse_message_failure(self):
        for test in self.failure_test_params:
            print("Test")
            
if __name__ == '__main__':
    unittest.main()