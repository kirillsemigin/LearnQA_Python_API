import requests
import json
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# The first request creates the task.
response = requests.get(url=url)
answer = json.loads(response.text)
token = answer['token']
seconds = answer['seconds']
print("token =", token, "seconds =", seconds)  # This is the result of the first request.
payload = {'token': token}

# The second request before the task is completed (test 1)
response2 = requests.get(url=url, params=payload)
answer2 = json.loads(response2.text)
status = answer2['status']

if 'Job is NOT ready' in status:
    print("status =", status, "test1 is true")
else:
    print("test1 is failed")

time.sleep(seconds)  # Time delay
response3 = requests.get(url=url, params=payload)  # The third request (test 2)
answer3 = json.loads(response3.text)
status2 = answer3['status']
result = answer3['result']
if 'Job is ready' in status2:
    if 'result' in answer3:
        print("status =", status2, "result =", result, "test2 is true")
    else:
        print("test2 is failed")
else:
    print("test2 is failed")

