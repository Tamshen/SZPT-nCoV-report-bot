import datetime
import json
import os
import re
from configparser import ConfigParser
from urllib import parse

import pytz
from requests.adapters import HTTPAdapter
from requests_html import HTMLSession

from module.AESCipher import *

# Read config.
config = ConfigParser()
config.read("config/config.ini", encoding="utf-8")

if config.getint("workflow", "enable") == 1:
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    server_chan_enable = int(os.environ['ENABLE_SERVER_CHAN'])
    sckey = os.environ['SCKEY']
    telegram_bot_enable = int(os.environ['ENABLE_TELEGRAM'])
    telegram_bot_token = os.environ['BOT_TOKEN']
    telegram_chat_id = os.environ['CHAT_ID']
else:
    username = config.get("user", "username")
    password = config.get("user", "password")
    server_chan_enable = config.getint("server-chan", "enable")
    sckey = config.get("server-chan", "sckey")
    telegram_bot_enable = config.getint("telegram", "enable")
    telegram_bot_token = config.get("telegram", "bot_token")
    telegram_chat_id = config.get("telegram", "chat_id")


def main():
    code, msg = report(username, password)
    session = HTMLSession()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))
    if server_chan_enable == 1:
        session.get('http://api.tamshen.com:222/v1/?c=workwxsend&id=' + sckey, params={
            'text': msg
        }, timeout=5)
    if telegram_bot_enable == 1:
        session.get('https://api.telegram.org/bot' + telegram_bot_token + '/sendMessage', params={
            'chat_id': telegram_chat_id,
            'text': msg
        })
    print(msg)


def report(username, password):
    ehall_url = config.get("url", "ehall_url")
    login_domain = config.get("url", "login_domain")
    ehall_getdata_url = config.get("url", "ehall_getdata_url")
    ehall_savedata_url = config.get("url", "ehall_savedata_url")
    ehall_update_cookie_url = config.get("url", "ehall_update_cookie_url")

    # Start a new session.
    session = HTMLSession()
    respond = session.get(ehall_url)

    # Parse login page.
    salt = respond.html.find('input#pwdDefaultEncryptSalt', first=True).attrs["value"]
    post_url = 'https://' + login_domain + respond.html.find('form#casLoginForm', first=True).attrs["action"]

    # Construct parameters
    params = {
        'dllt': 'userNamePasswordLogin',
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rmShown': 1,
        'username': username,
        'lt': respond.html.find('input[name="lt"]', first=True).attrs["value"],
        'password': AESCipher(salt).encrypt(password)
    }

    # Login post
    session.post(post_url, data=params)

    try:
        respond = session.post(ehall_url)
        app_data = {
            "APPID": re.search("APPID='(.*?)';", respond.text, re.S).group(1),
            "APPNAME": re.search("APPNAME='(.*?)';", respond.text, re.S).group(1)
        }
    except AttributeError:
        return 500, "用户名或密码错误，请更正后再试"

    # Update cookies
    session.post(ehall_update_cookie_url, data={
        'data': json.dumps(app_data)
    })

    # Get last report record
    respond = session.get(ehall_getdata_url)

    # Report Post
    data = respond.json()['datas']

    # Fix null value
    if data['OPERATE_DATE'][:10] != datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d"):
        data.update({'WID': ''})

    fixer = {
        "ZSDZ": "", "SXFS": "", "SFZZSXDWSS": "",
        "FSSJ": "", "FXSJ": "", "FHTJGJ": "", "QTXYSMDJWQK": "", "SSSQ": "", "XSQBDSJ": "", "JSJJGCJTSJ": "",
        "JSJTGCJTSJ": "", "JSJJJTGCYY": "", "STYCZK": "", "STYXZK": "", "QYTZWTW": "", "QYTWSTW": "", "DTZSTW": ""
    }
    data.update(fixer)

    encode_data = parse.quote_plus(json.dumps(data, ensure_ascii=False))
    respond = session.post(ehall_savedata_url, data='formData=' + encode_data, headers={
        'Content-type': 'application/x-www-form-urlencoded'
    })

    # Validator
    if respond.json()['code'] == '0':
        return 200, username + "  提交成功"
    else:
        return 500, respond.json()


if __name__ == '__main__':
    main()
