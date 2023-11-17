import pytest
import requests

class Test3:
    def test_header_method(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url=url)
        # print(response.headers) To find out headers and its values
        header_value = response.headers.get('x-secret-homework-header') # To get the value of the header

        assert "x-secret-homework-header" in response.headers, "There is no header 'x-secret-homework-header' in the response"

        assert header_value == "Some secret value", "There is wrong header value"
