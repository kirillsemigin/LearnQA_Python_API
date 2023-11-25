import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

class TestUserRegister(BaseCase):
    def setup(self):
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f'{base_part}{random_part}@{domain}'

    def test_create_user_succesfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
       email ='vinkotov@example.com'
       data = {
           'password': '123',
           'username': 'learnqa',
           'firstName': 'learnqa',
           'lastName': 'learnqa',
           'email': email
       }

       response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

       Assertions.assert_code_status(response, 400)
       assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
           f'Unexpected response content {response.content}'


    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f'Invalid email format', \
            f'Unexpected response content {response.content}'

    def test_create_user_with_short_name(self):
        shortname = 'l',
        data = {
            'password': '123',
            'username': shortname,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f'Unexpected response content {response.content}'

    def test_create_user_with_long_name(self):
        longname = 'it_is_a_vey_very_long_name_of_a_test_user_to_be_created_it_is_a_vey_very_long_name_of_a_test_user_to_be_created_it_is_a_vey_very_long_name_of_a_test_user_to_be_created_it_is_a_vey_very_long_name_of_a_test_user_to_be_created_it_is_a_vey_very_long_name_of_a_test_user',
        data = {
            'password': '123',
            'username': longname,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f'Unexpected response content {response.content}'
