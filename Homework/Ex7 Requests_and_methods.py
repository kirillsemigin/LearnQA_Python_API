import requests
import json


url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
response1 = requests.get(url=url)
print('response =', response1.text,',', 'status_code =', response1.status_code)

response2 = requests.head(url=url)
print('response =', response2.text,',', 'status_code =', response2.status_code)

response3 = requests.post(url=url, data={"method": "POST"})
print('response =', response3.text, ',', 'status_code =', response3.status_code)

types_of_requests = [requests.get, requests.post, requests.put, requests.delete, requests.patch, requests.head, requests.options]
list_of_params = [{"method": "GET"},{"method": "POST"},{"method": "PUT"}, {"method": "DELETE"}, {"method": "PATCH"}, {"method": "HEAD"}, {"method": "OPTIONS"}]


for method in types_of_requests:
    for params in list_of_params:
        param = params['method']
        result = method(url, params=params)
        method_pars = str(method)[10:-23]
        upper_method = str.upper(method_pars)
        key = "success"
        if key in result.text:
            result_s = json.loads(result.text)
            success = result_s['success']
            if param in upper_method:
                if 'GET' in upper_method:
                    if '!' in success:
                        print('param =', param, ',', 'success =', success, ',', 'method =', upper_method, ',',
                              'test true')
                else:
                    if '!' in success:
                        print('param =', param, ',', 'success =', success, ',', 'method =', upper_method, ',',
                              'test false')
        else:
            print('param =', param, ',', result.text, ',', result.status_code, ',', 'method =', upper_method, ',',
                  'test ERROR')
        result = method(url, data=params)
        method_pars = str(method)[10:-23]
        upper_method = str.upper(method_pars)
        key = "success"
        if key in result.text:
            result_s = json.loads(result.text)
            success = result_s['success']
            if param in upper_method:
                if 'GET' in upper_method:
                    if '!' in success:
                        print('data =', param, ',', 'success =', success, ',', 'method =', upper_method, ',',
                              'test false')
                elif '!' in success:
                    print('data =', param, ',', 'success =', success, ',', 'method =', upper_method, ',', 'test true')
            else:
                if '!' in success:
                    print('data =', param, ',', 'success =', success, ',', 'method =', upper_method, ',', 'test false')
        else:
            print('data =', param, ',', result.text, ',', result.status_code, ',', 'method =', upper_method, ',',
                  'test ERROR')

