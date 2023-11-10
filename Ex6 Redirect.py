import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
answer = response.history
answer2 = response.url

print(answer)
print(answer2)
