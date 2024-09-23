import requests
import json
import os
from datetime import datetime

def send(list):
    headers = {
        'Content-Type' : 'application/json'
    }
    url = os.environ['HOOK_URL']
    body = {
        'msgtype' : 'text',
        'text' : {
            'content' : '请注意⚠下班未打卡⏰',
            'mentioned_list': list
        }
    }
    response = requests.post(url=url,data=json.dumps(body),headers=headers)
    print(response.text)
headers = {
    'Authorization': 'Bearer {}'.format(os.environ['TOKEN'])
}
url = os.environ['DATE_URL']
response = requests.get(url=url,headers=headers)
if response.status_code != 200 :
    raise SystemError('token is expired or invalid')
data = json.loads(response.text)['data']
if data['type'] != 'weekday':
    raise AssertionError("today is not workday")
url = os.environ['INFOR_URL']
params = {
    'data': datetime.now().strftime('%Y-%m-%d'),
    'office': '%E5%85%A8%E9%83%A8'
}
response = requests.get(url=url,params=params,headers=headers)
if response.status_code != 200 :
    raise SystemError('token is expired or invalid')
text = response.text
data = json.loads(text)['data']
userList = []
for person in data :
    if not person['signOut']:
        print('user {} is not checkout'.format(person['userId']))
        userList.append(person['userId'])
send(userList)

