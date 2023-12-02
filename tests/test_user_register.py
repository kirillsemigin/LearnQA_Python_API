from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    values = [
        (None, 'learnqa', 'learnqa', 'learnqa', 'vinkotov@example.com'),
        ('123', None, 'learnqa', 'learnqa', 'vinkotov@example.com'),
        ('123', 'learnqa', None, 'learnqa', 'vinkotov@example.com'),
        ('123', 'learnqa', 'learnqa', None, 'vinkotov@example.com'),
        ('123', 'learnqa', 'learnqa', 'learnqa', None)
    ]

    def test_create_user_succesfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
       email ='vinkotov@example.com'
       data = self.prepare_registration_data(email)

       response = MyRequests.post("/user/", data=data)

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

        response = MyRequests.post("/user/", data=data)

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

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f'Unexpected response content {response.content}'

    def test_create_user_with_long_name(self):
        longname = ('very_long_name' * 20),
        data = {
            'password': '123',
            'username': longname,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f'Unexpected response content {response.content}'

    @pytest.mark.parametrize('password, username, firstName, lastName, email', values)
    def test_create_user_without_one_parameter(self, password, username, firstName, lastName, email):
        data = {
            'password': password,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'email': email
        }
        response = MyRequests.post("/user/", data=data)
        answer = response.text[42:]
        Assertions.assert_code_status(response, 400)
        assert response.text == f'The following required params are missed: {answer}'
