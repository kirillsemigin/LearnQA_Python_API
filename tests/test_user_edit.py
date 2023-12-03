import json
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Editing cases")
class TestUserEdit(BaseCase):
    @allure.description("This test checks the abilty to edit user after creation")
    @allure.feature('POSITIVE')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #GET

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    @allure.description("This test checks the ability to edit user without authorization")
    @allure.feature('NEGATIVE')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_change_user_without_authorization(self):
        new_name = "Changed Name"
        user_id = 1

        response = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name})

        Assertions.assert_code_status(response, 400)
        assert response.text == f'Auth token not supplied', 'Unauthorized user tries to edit'

    @allure.description("This test checks the ability to edit user being authorized under another user")
    @allure.feature('NEGATIVE')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_change_user_under_different_account(self):
        # REGISTER_FIRST_USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        first_user_email = register_data['email']
        first_name = register_data['firstName']
        first_user_password = register_data['password']
        first_user_id = self.get_json_value(response1, 'id')

        # print(first_user_id)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN_FIRST_USER
        login_data = {
            'email': first_user_email,
            'password': first_user_password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        first_user_auth_sid = self.get_cookie(response2, "auth_sid")
        first_user_token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_code_status(response2, 200)

        # GET_FIRST_USER
        response3 = MyRequests.get(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": first_user_token},
            cookies={"auth_sid": first_user_auth_sid}
        )

        old_name = self.get_json_value(response3, 'firstName')
        # print(old_name)
        Assertions.assert_code_status(response3, 200)

        # REGISTER_SECOND_USER
        register_data = self.prepare_registration_data()
        response4 = MyRequests.post("/user/", data=register_data)

        second_user_email = register_data['email']
        second_user_first_name = register_data['firstName']
        second_user_password = register_data['password']
        second_user_id = self.get_json_value(response4, 'id')

        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_has_key(response4, "id")

        # print(second_user_id)

        # LOGIN_SECOND_USER
        login_data = {
            'email': second_user_email,
            'password': second_user_password
        }
        response5 = MyRequests.post("/user/login", data=login_data)

        second_user_auth_sid = self.get_cookie(response5, "auth_sid")
        second_user_token = self.get_header(response5, "x-csrf-token")

        Assertions.assert_code_status(response2, 200)

        # GET_SECOND_USER
        response6 = MyRequests.get(
            f"/user/{second_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # EDIT_FIRST_USER
        new_name = "Kirill"

        response7 = MyRequests.put(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response7, 200)

        # GET_FIRST_USER
        response8 = MyRequests.get(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": first_user_token},
            cookies={"auth_sid": first_user_auth_sid}
        )
        Assertions.assert_code_status(response8, 200)
        Assertions.assert_json_value_by_name(response8, 'firstName', old_name,
                                             'Wrong name! Name has been changed by another user')

    @allure.description("This test checks the ability to change on the invalid one")
    @allure.feature('NEGATIVE')
    @allure.severity(allure.severity_level.NORMAL)
    def test_change_invalid_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        user_token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_code_status(response2, 200)

        # EDIT
        new_email = "learnqaexample.com"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": user_token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response3, 400)
        assert response3.text == "Invalid email format", "WARNING! It should be impossible to use this email format"

    @allure.description("This test checks the ability to change user name on a short one ")
    @allure.feature('POSITIVE')
    @allure.severity(allure.severity_level.NORMAL)
    def test_change_short_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        user_token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_code_status(response2, 200)

        # EDIT
        new_name = "K"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": user_token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        error_text = json.loads(response3.text)['error']

        Assertions.assert_code_status(response3, 400)
        assert error_text == "Too short value for field firstName", "This is fail. " \
                                                                    "It should be impossible to use such a short name "








