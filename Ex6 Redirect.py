import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
answer = response.history
number_of_redirects = len(answer)
answer2 = response.url

print(number_of_redirects)
print(answer2)
