"""
@Author  : 孔天宇
@Desc    : 
"""
import base64
import pprint
from encodings.base64_codec import base64_decode

import requests
# execjs Windows中文编码修复
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs


class CrawlData:
    def __init__(self):
        self.response = None
        self.url = 'http://www.spolicy.com/info_api/policyType/showPolicyType'
        self.cookies = {
            'Hm_lvt_6146f11e5afab71309b3accbfc4a932e': '1784794043',
            'HMACCOUNT': '808752F02F03EC57',
            'JSESSIONID': '49490D01FB6D99846E48D289908977AB',
            'Hm_lpvt_6146f11e5afab71309b3accbfc4a932e': '1786268668',
        }
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/octet-stream',
            'Origin': 'http://www.spolicy.com',
            'Pragma': 'no-cache',
            'Referer': 'http://www.spolicy.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            # 'Cookie': 'Hm_lvt_6146f11e5afab71309b3accbfc4a932e=1784794043; HMACCOUNT=808752F02F03EC57; JSESSIONID=49490D01FB6D99846E48D289908977AB; Hm_lpvt_6146f11e5afab71309b3accbfc4a932e=1786268668',
        }

    def encrypt_data(self):
        js = execjs.compile(open('大数据产业平台.js', "r", encoding='utf-8').read())
        payload_data = js.call('payload_data')
        print(payload_data)
        # 将base64编码的格式转化成字节形式
        # base64解码后的字符串的长度是否是4的倍数的解决方案
        # decode_code是解码后的字符串长度处理
        decode_data = payload_data + (4 - (len(payload_data) % 4)) * '=' if len(payload_data) % 4 != 0 else payload_data
        bytes_data = base64.b64decode(decode_data)
        return bytes_data
        # print(bytes(payload_data['data']))
        # return bytes(payload_data['data'])



    def get_data(self):
        self.response = requests.post(
            url=self.url,
            cookies=self.cookies,
            headers=self.headers,
            # data=bytes(self.encrypt_data().get('data', '')),
            data=self.encrypt_data(),
            verify=False,
        )
        return self.response.json()


if __name__ == '__main__':
    # 获取最终的数据
    response_data = CrawlData().get_data()
    pprint.pprint(response_data)
