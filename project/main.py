import json
import re
import os
from urllib import parse
from requests_html import HTMLSession
from configparser import ConfigParser
from module.AESCipher import *

# Read config.
config = ConfigParser()
config.read("config/config.ini", encoding="utf-8")

if config.getint("workflow", "enable") == 1:
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    server_chan_enable = os.environ['ENABLE_SERVER_CHAN']
    sckey = os.environ['SCKEY']
else:
    username = config.get("user", "username")
    password = config.get("user", "password")
    server_chan_enable = config.getint("server-chan", "enable")
    sckey = config.get("server-chan", "sckey")


def main():
    code, msg = report(username, password)
    if server_chan_enable == 1:
        session = HTMLSession()
        session.get('https://sc.ftqq.com/' + sckey + '.send', params={
            'text': msg
        })
    else:
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

    print(app_data)

    # Update cookies
    session.post(ehall_update_cookie_url, data={
        'data': json.dumps(app_data)
    })

    # Get last report record
    respond = session.get(ehall_getdata_url)

    # Report Post
    data = respond.json()['datas']
    encode_data = parse.quote_plus(json.dumps(data, ensure_ascii=False))
    respond = session.post(ehall_savedata_url, data='formData=' + encode_data, headers={
        'Content-type': 'application/x-www-form-urlencoded'
    })

    # Validator
    if respond.json()['code'] == '0':
        return 200, username + "  提交成功"
    else:
        return 500, "未知异常"


if __name__ == '__main__':
    main()
