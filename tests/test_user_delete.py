import requests
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Removal cases")
class TestUserDelete(BaseCase):
    @allure.description("This test checks the ability to delete user with ID = 2")
    @allure.feature('POSITIVE')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_delete_id2(self):
        # REGISTER
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        # ATTEMPT TO DELETE USER WITH ID = 2
        user_id = 2
        response2 =requests.delete(f'https://playground.learnqa.ru/api/user/{user_id}',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
                                )
        expected_message = 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'
        actual_message = response2.text
        Assertions.assert_code_status(response2, 400)
        assert actual_message == expected_message, f'Message in response is not equal to {expected_message}. ' \
                                                   f'Actual message = {actual_message}'

    @allure.description("This test checks to delete user after authorization")
    @allure.feature('POSITIVE')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_authorize_delete(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # ATTEMPT TO DELETE USER

        response3 = requests.delete(f'https://playground.learnqa.ru/api/user/{user_id}',
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )
        Assertions.assert_code_status(response3, 200)

        # GET DELETED USER
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.text == 'User not found', f'User is found and was not deleted'

    @allure.description("This test checks the ability to delete user being authorized under another user")
    @allure.feature('NEGATIVE')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_under_different_account(self):
        # REGISTER USER 1
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN USER 1
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # REGISTER USER 2
        register_data = self.prepare_registration_data()
        response3 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        email2 = register_data['email']
        first_name2 = register_data['firstName']
        password2 = register_data['password']
        user_id2 = self.get_json_value(response3, "id")

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        # ATTEMPT TO DELETE USER 2
        response4 = requests.delete(f'https://playground.learnqa.ru/api/user/{user_id2}',
                    headers={"x-csrf-token": token},
                    cookies={"auth_sid": auth_sid}
                                )

        Assertions.assert_code_status(response4, 200)


        # GET USER 2
        response5 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id2}"
        )
        Assertions.assert_code_status(response5, 200)
        assert response5.text != "User not found", f'User 2 was deleted by another user'












