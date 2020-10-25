'''
    api_mocks.py
    
    This file tests twitter_query.py.
'''

import unittest
import unittest.mock as mock
from chatbot import CoolBot
from dotenv import load_dotenv
import os
from os.path import join, dirname

KEY_INPUT = "arg1"
KEY_INPUT2 = "arg2"
KEY_EXPECTED = "expected"
KEY_MESSAGE = "message"
KEY_USER = "user"
KEY_PFP = "pfp_url"

class MockedDadResponse:
    def __init__(self, id, joke, status):
        self.id = id
        self.joke = joke
        self.status = status

class BotQueryTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
              KEY_INPUT: "!! dad",
                KEY_INPUT2: "",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "My dog used to chase people on a bike a lot. It got so bad I had to take his bike away.",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + "\"./botpfp.png\">",
                }
            }
        ]
        
    def mocked_random_choice(self, values):
        return values[0]
    
    def mocked_api_search(self, q, count):
        return [
            MockedSearchResponse(
                "mocked tweet",
                "triciascot99",
                "http://twitter.com/download/iphone",
                datetime.datetime.strptime("10/15/2020, 21:24", "%m/%d/%Y, %H:%M")),
            MockedSearchResponse(
                "aslfdjasdf",
                "sadfasdfas",
                "asfjkaldfjad",
                datetime.datetime.strptime("10/19/2020, 21:01", "%m/%d/%Y, %H:%M")),
            ]

    def test_get_random_tweet_success(self):
        for test_case in self.success_test_params:
            with mock.patch('tweepy.API.search', self.mocked_api_search):
                relevant_tweets = get_relevant_tweets(
                    query = test_case[KEY_INPUT],
                    access_token = TWITTER_ACCESS_TOKEN,
                    access_token_secret = TWITTER_ACCESS_TOKEN_SECRET,
                    key = TWITTER_KEY,
                    key_secret = TWITTER_KEY_SECRET,
                    count = 3)
                
            with mock.patch('random.choice', self.mocked_random_choice):
                random_tweet = get_random_tweet(relevant_tweets)
                
            expected = test_case[KEY_EXPECTED]
            
            self.assertDictEqual(random_tweet, expected)
        
if __name__ == '__main__':
    unittest.main()
