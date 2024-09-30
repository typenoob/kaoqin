import requests
import json
import os
from datetime import datetime

def send(list):
    content= "请注意⚠下班未打卡⏰"
    if len(list) == 0 : content = "所有人都已打卡✌"
    headers = {
        'Content-Type' : 'application/json'
    }
    url = os.environ['HOOK_URL']
    body = {
        'msgtype' : 'text',
        'text' : {
            'content' : content,
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
if data['type'] != 'weekday' and data['type'] != 'workday':
    raise AssertionError("today is not weekday or workday")
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
    if 'signOut' in person and not person['signOut']:
        print('user {} is not checkout'.format(person['userId']))
        userList.append(person['userId'])
send(userList)

