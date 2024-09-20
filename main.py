import requests
import json
import os
from datetime import datetime

def send(list):
    headers = {
        'Content-Type' : 'application/json'
    }
    url = os.environ['URL']
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
    'Authorization': 'Bearer ee0fa132-e4d7-4f37-bfdd-5a327373facf'
}
url = 'https://qywx.pharmaron.cn/gateway/att/v1/0/auth-deptss/getTeamAttendanceInfo'
params = {
    'data': datetime.now().strftime('%Y-%m-%d'),
    'office': '%E5%85%A8%E9%83%A8'
}
response = requests.get(url=url,params=params,headers=headers)
text = response.text
if response.status_code == 200 :
    data = json.loads(text)['data']
    userList = []
    for person in data :
        if not person['leave']:
            print('user {} is not checkout'.format(person['userId']))
            userList.append(person['userId'])
    send(userList)
else:
    print('token is expired or invalid')

