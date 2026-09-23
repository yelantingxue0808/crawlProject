"""
@Author  : 孔天宇
@Desc    : 
"""
import pprint
import re
import time

import requests
import set_cookie

def crawlData(cookies,csrf_token,**kwargs):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.zjmazhang.gov.cn',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.zjmazhang.gov.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': csrf_token,
        # 'Cookie': 'XSRF-TOKEN=eyJpdiI6Imh3RCtNcXhXVHp1YXRaN09VeXNOYnc9PSIsInZhbHVlIjoiK1BnWURaVHdReDIrMDM5c3RzWWZlUjN0S2U3QzJWbWxGeFZsOVhoREF6UkpMdFU1NlRlUzJkc21uM01FVGZEbyIsIm1hYyI6ImU1YzRhMWU0M2I2ZTJhZWU2MjQzODE3ZjY4NTM0NDcyYzI0NDdjYWYxZWVhZWRiOTFkMDdlNDkyOTdmNTA2MTUifQ%3D%3D; szxx_session=eyJpdiI6IjFkeFVucTMzTXJlZTZxRXJDTXN3cHc9PSIsInZhbHVlIjoicnZvSHUzaVcwTGYrRmd0bnpxRVpSTmNTZjlcL0RjTFA4aU9DSkwxOER2aVhsV1ZLbW5sSUFMNXNpTk16UE5NZmsiLCJtYWMiOiJkNWUyYTU0ZTRlZjU3NGQ0MTBlODVjZmE4MmFjZjUxMzc4ZTY0YzQzODFmYzBlNWRkZjQ0NzhhOWIyZTNlZTNkIn0%3D',
    }
    date1_time = time.mktime(time.strptime('{} 00:00:00'.format(kwargs['date1']), '%Y-%m-%d %H:%M:%S'))
    date2_time = time.mktime(time.strptime('{} 23:59:59'.format(kwargs['date2']), '%Y-%m-%d %H:%M:%S'))
    data = {
        'offset': '0',
        'limit': '20',
        'site_id': '759010',
        'time_from': int(date1_time), # 2025-9-24 00:00:00
        'time_to': int(date2_time) # 2026-09-21 23:59:59
    }
    cookie_dict = {}
    for k, v in cookies.items():
        if k == 'Path':
            continue
        cookie_dict[k] = v
    print(cookie_dict)

    response = requests.post(
        'http://www.zjmazhang.gov.cn/hdjlpt/letter/pubList',
        cookies=cookie_dic,
        headers=headers,
        data=data,
        verify=False,
    )
    return response
if __name__ == '__main__':
    cookie_dic, x_csrf_token = set_cookie.set_cookie()
    datetime = input('想获xxx年xxx月xxx号到xxx年xxx月xxx号的数据：')
    pattern = re.compile(pattern=r'(?P<date1>\d*年\d*月\d*号).*?(?P<date2>\d*年\d*月\d*号)')
    date1 = re.sub(r'[年月号]', '-', pattern.search(datetime).group("date1"))[:-1]
    date2 = re.sub(r'[年月号]', '-', pattern.search(datetime).group("date2"))[:-1]

    response = crawlData(cookie_dic,x_csrf_token,date1=date1,date2=date2)
    # print(response)
    pprint.pprint(response.json())
