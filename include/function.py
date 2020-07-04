import re
import time
import urllib.parse
import requests
import json

from .config import *
from .AESCipher import AESCipher

session = requests.session()


def send(username, password):
    # get login params
    try:
        respond = session.get(LOGIN_URL)
        lt = re.search('name="lt" value="(.*?)"/>', respond.text, re.S).group(1)
        execution = re.search('name="execution" value="(.*?)"/>', respond.text, re.S).group(1)
        aes_key = re.search('pwdDefaultEncryptSalt = "(.*?)";', respond.text, re.S).group(1)
        password_aes = AESCipher(aes_key).encrypt(password)
    except:
        return 500, "用户名或密码错误，请更正后再试"

    # build LOGIN request
    params = {
        'username': username,
        'password': password_aes,
        'lt': lt,
        'dllt': 'userNamePasswordLogin',
        'execution': execution,
        '_eventId': 'submit',
        'rmShown': '1'
    }
    respond = session.post(LOGIN_URL, data=params)

    # get APP_data & update cookie
    try:
        app_data = {
            "APPID": re.search("APPID='(.*?)';", respond.text, re.S).group(1),
            "APPNAME": re.search("APPNAME='(.*?)';", respond.text, re.S).group(1)
        }
    except AttributeError:
        return 500, "用户名或密码错误，请更正后再试"

    session.post(UPDATE_COOKIE_URL, data={
        'data': json.dumps(app_data)
    }, headers=HEADER)

    # get user last report info
    respond = session.post(GET_INFO_POST_URL, data={
        "USER_ID": username
    }, headers=HEADER)

    data = respond.json()['datas']

    # check for duplicate reports
    if data['REPORT_DATE'] != time.strftime("%Y-%m-%d", time.localtime()):
        data.update({"WID": ""})

    data.update(UPDATE_DATA)

    encode_data = urllib.parse.quote_plus(json.dumps(data,ensure_ascii=False))

    # send report
    respond = session.post(SAVE_INFO_POST_URL, data='formData='+encode_data, headers=HEADER_SAVE)

    if respond.text == '{"datas":1,"code":"0"}':
        return 0, "报告完毕"
    else:
        return 500, "填报错误，可能表单已更新"
