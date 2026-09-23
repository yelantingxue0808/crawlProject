import pprint
import re

import requests

def set_cookie():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    }

    params = {
        'via': 'pc',
    }

    response = requests.get('http://www.zjmazhang.gov.cn/hdjlpt/published', params=params, headers=headers,
                            verify=False)
    # print(response.status_code)

    pattern = re.compile(pattern=r"_CSRF = '(.*?)'")
    x_csrf_token = pattern.search(response.text).group(1)

    set_cookies = dict(response.cookies)
    return set_cookies,x_csrf_token


if __name__ == '__main__':
    pprint.pprint(set_cookie())
