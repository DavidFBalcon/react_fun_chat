"""
    api_mocks.py
    This file tests twitter_query.py.
"""
import unittest
import unittest.mock as mock
import sys
import os

sys.path.append(os.path.abspath(os.path.join("..")))
import chatbot

KEY_INPUT = "arg1"
KEY_INPUT2 = "arg2"
KEY_EXPECTED = "expected"
KEY_MESSAGE = "message"
KEY_USER = "user"
KEY_PFP = "pfp_url"

# MOCKING REQUESTS.GET IN DAD
def mocked_requests_get_dad(*args, **kwargs):
    """
    Creates mocked request for dad api.
    """

    class MockedDadResponse:
        """
        Defines MockedDadResponse.
        """

        def __init__(self, json_data, status):
            self.json_data = json_data
            self.status = status

        def json(self):
            return self.json_data

    if args[0] == "https://icanhazdadjoke.com/":
        return MockedDadResponse(
            {
                "joke": "My dog used to chase people \
on a bike a lot. It got so bad I had to take his bike away."
            },
            200,
        )
    return MockedDadResponse(None, 404)


def mocked_requests_funtranslate(*args, **kwargs):
    """
    Creates mocked request for funtranslate api.
    """

    class MockedFunResponse:
        """
        Defines MockedFunResponse.
        """

        def __init__(self, json_data, status):
            self.json_data = json_data
            self.status = status

        def json(self):
            return self.json_data

    return MockedFunResponse({"contents": {"translated": "Welcome to Macca's"}}, 200)


def mocked_requests_anime(*args, **kwargs):
    """
    Creates mocked request for jikan API.
    """

    class MockedAnimeResponse:
        """
        Defines MockedAnimeResponse.
        """

        def __init__(self, dict_data, status):
            self.dict_data = dict_data
            self.status = status

        def ret_data(self):
            return self.dict_data

    return MockedAnimeResponse(
        {
            "results": [
                {
                    "title": "Shoujo Shuumatsu Ryokou",
                    "score": 8.19,
                    "synopsis": "Amid the desolate remains of a once-thriving city, \
only the rumbling of a motorbike breaks the cold ",
                }
            ]
        },
        200,
    ).ret_data()


class DadQueryTestCase(unittest.TestCase):
    """
    Sets up test cases for dad api.
    """

    def setUp(self):
        """
        Sets up paramters for dad cases.
        """
        self.success_test_params = [
            {
                KEY_INPUT: "!! dad",
                KEY_INPUT2: "",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "My dog used to chase people on \
a bike a lot. It got so bad I had to take his bike away.",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + '"./botpfp.png">',
                },
            }
        ]

    def test_chatbot_dad_success(self):
        """
        Success cases for dad.
        """
        for test_case in self.success_test_params:
            with mock.patch("requests.get", mocked_requests_get_dad):
                response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
            expected = test_case[KEY_EXPECTED]
            self.assertDictEqual(response, expected)


class FunQueryTestCase(unittest.TestCase):
    """
    Creates test cases for funtranslate api.
    """

    def setUp(self):
        """
        Sets up parameters for cases.
        """
        self.success_test_params = [
            {
                KEY_INPUT: "!! funtranslate Welcome to McDonald's",
                KEY_INPUT2: "",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "Welcome to Macca's",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + '"./botpfp.png">',
                },
            }
        ]
        self.failure_test_params = [
            {
                KEY_INPUT: "!! funtranslate",
                KEY_INPUT2: "",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "Welcome to Macca's",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + '"./botpfp.png">',
                },
            }
        ]

    def test_chatbot_fun_success(self):
        """
        Success cases for funtranslate
        """
        for test_case in self.success_test_params:
            with mock.patch("requests.get", mocked_requests_funtranslate):
                response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
            expected = test_case[KEY_EXPECTED]
            self.assertDictEqual(response, expected)

    def test_chatbot_fun_failure(self):
        """
        Failure cases for funtranslate
        """
        for test_case in self.failure_test_params:
            with mock.patch("requests.get", mocked_requests_funtranslate):
                response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
            expected = test_case[KEY_EXPECTED]
            self.assertNotEqual(response, expected)


class AnimeQueryTestCase(unittest.TestCase):
    """
    Creates test cases for jikan API.
    """

    def setUp(self):
        """
        Sets up parameters for cases.
        """
        self.success_test_params = [
            {
                KEY_INPUT: "!! anime Girl's Last Tour",
                KEY_INPUT2: "",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "Title: "
                    + "Shoujo Shuumatsu Ryokou"
                    + "<br></br>Score: "
                    + "8.19"
                    + "<br></br>Summary: "
                    + "Amid the desolate remains of a once-thriving city, \
only the rumbling of a motorbike breaks the cold "
                    + "...",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + '"./botpfp.png">',
                },
            }
        ]
        self.failure_test_params = [
            {
                KEY_INPUT: "!! anime",
                KEY_INPUT2: "",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "Title: "
                    + "Shoujo Shuumatsu Ryokou"
                    + "<br></br>Score: "
                    + "8.19"
                    + "<br></br>Summary: "
                    + "Amid the desolate remains of a once-thriving city, \
only the rumbling of a motorbike breaks the cold "
                    + "...",
                    KEY_USER: "Bot",
                    KEY_PFP: "<img src=" + '"./botpfp.png">',
                },
            }
        ]

    def test_chatbot_anime_success(self):
        """
        Success cases for Jikan.
        """
        for test_case in self.success_test_params:
            with mock.patch("jikanpy.Jikan.search", mocked_requests_anime):
                response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
            expected = test_case[KEY_EXPECTED]
            self.assertDictEqual(response, expected)

    def test_chatbot_anime_failure(self):
        """
        Failure cases for Jikan.
        """
        for test_case in self.failure_test_params:
            with mock.patch("jikanpy.Jikan.search", mocked_requests_anime):
                response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
            expected = test_case[KEY_EXPECTED]
            self.assertNotEqual(response, expected)


# class GoogleAuthQueryTestCase(unittest.TestCase):
# def setUp(self):
#  self.success_test_params = [
# {
#    KEY_INPUT: {'name': 'Koomi', 'email': 'baconatoring@gmail.com', 'idtoken':\
#'mock_token'},
#    KEY_EXPECTED: True
# }
# ]
# def test_chatbot_dad_success(self):
# for test_case in self.success_test_params:
# with mock.patch('requests.get', mocked_requests_get_dad):
#   response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
# expected = test_case[KEY_EXPECTED]
# self.assertDictEqual(response, expected)
if __name__ == "__main__":
    unittest.main()
