import re
import time

import requests
import json

from .config import *
from .AESCipher import AESCipher

session = requests.session()


def login(username, password):
    # get login params
    respond = session.get(LOGIN_URL)
    lt = re.search('name="lt" value="(.*?)"/>', respond.text, re.S).group(1)
    execution = re.search('name="execution" value="(.*?)"/>', respond.text, re.S).group(1)
    aes_key = re.search('pwdDefaultEncryptSalt = "(.*?)";', respond.text, re.S).group(1)
    password_aes = AESCipher(aes_key).encrypt(password)

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
    app_data = {
        "APPID": re.search("APPID='(.*?)';", respond.text, re.S).group(1),
        "APPNAME": re.search("APPNAME='(.*?)';", respond.text, re.S).group(1)
    }

    session.post(UPDATE_COOKIE_URL, data={
        'data': json.dumps(app_data)
    }, headers=header)

    # get user last report info
    respond = session.post(GET_INFO_POST_URL, data={
        "USER_ID": username
    }, headers=header)

    data = respond.json()['datas']
    data.update({
        "OPERATE_DATE": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "REPORT_DATE": time.strftime("%Y-%m-%d", time.localtime()), "WID": "", "ZSDZ": "", "SXFS": "", "SFZZSXDWSS": "",
        "FSSJ": "", "FXSJ": "", "FHTJGJ": "", "QTXYSMDJWQK": "", "SSSQ": "", "XSQBDSJ": "", "JSJJGCJTSJ": "",
        "JSJTGCJTSJ": "", "JSJJJTGCYY": "", "STYCZK": "", "STYXZK": ""
    })

    # send report
    respond = session.post(SAVE_INFO_POST_URL, data={'formData': data}, headers=header)
    print(respond.text)