import pytest
import requests

class Test2:
    def test_cookie_method(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(url=url)
        print(dict(response.cookies))  # To find out the cookie and its value
        cookie_value = response.cookies.get('HomeWork')

        assert "HomeWork" in response.cookies, "There is no cookie 'HomeWork' in the response"

        assert cookie_value == 'hw_value', "There is wrong cookie value"



