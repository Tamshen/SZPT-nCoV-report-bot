import time

DEBUG_MODE = False
BIND_HOST = '0.0.0.0'
BIND_PORT = 8848
"""
请求地址，一般不用更改
"""
LOGIN_URL = 'https://authserver.szpt.edu.cn/authserver/login?service=https%3A%2F%2Fehall.szpt.edu.cn%3A443%2Fpublicappinternet%2Fsys%2Fszptpubxsjkxxbs%2F*default%2Findex.do#/'
UPDATE_COOKIE_URL = 'https://ehall.szpt.edu.cn/publicappinternet/sys/itpub/MobileCommon/getMenuInfo.do'
GET_INFO_POST_URL = 'https://ehall.szpt.edu.cn/publicappinternet/sys/szptpubxsjkxxbs/mrxxbs/getSaveReportInfo.do'
SAVE_INFO_POST_URL = 'https://ehall.szpt.edu.cn/publicappinternet/sys/szptpubxsjkxxbs/mrxxbs/saveReportInfo.do'

"""
时间相关
"""
CRON_TIMEZONE = 'Asia/Shanghai'
CRON_HOUR = 7
CRON_MINUTE = 30

CRON_HOUR_RE = 8
CRON_MINUTE_RE = 0

"""
请求头，一般不用更改
"""
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'ehall.szpt.edu.cn'
}

HEADER_SAVE = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
    'Content-type': 'application/x-www-form-urlencoded'
}

"""
需要更新的请求数据，按情况更改
"""
UPDATE_DATA = {
        "OPERATE_DATE": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "REPORT_DATE": time.strftime("%Y-%m-%d", time.localtime()), "ZSDZ": "", "SXFS": "", "SFZZSXDWSS": "",
        "FSSJ": "", "FXSJ": "", "FHTJGJ": "", "QTXYSMDJWQK": "", "SSSQ": "", "XSQBDSJ": "", "JSJJGCJTSJ": "",
        "JSJTGCJTSJ": "", "JSJJJTGCYY": "", "STYCZK": "", "STYXZK": "","QYTZWTW": "", "QYTWSTW": "", "DTZSTW": ""
    }