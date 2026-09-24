import requests
import re
import execjs


def get_cookie():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    url = 'https://xueqiu.com/today'
    response = requests.get(url, headers=headers)
    arg1 = re.findall("var arg1='(.*?)';", response.text)[0]
    acw_tc = response.cookies.get('acw_tc')
    return arg1, acw_tc



def get_data():
    arg1, acw_tc = get_cookie()
    with open('02-阿里cookie解析.js', encoding='utf-8')as f:
        js_code = f.read()
    js = execjs.compile(js_code)
    arg2 = js.call('get_cookie', arg1)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    cookies = {
        'acw_tc': acw_tc,
        'acw_sc__v2': arg2
    }
    print(cookies)
    url = 'https://xueqiu.com/today'
    res = requests.get(url, headers=headers, cookies=cookies)
    print(res.text)


get_data()
