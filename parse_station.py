# coding: utf-8
import re
import requests
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
response = requests.get(url, verify=False)
#至少匹配一个汉字、英文
sations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
pprint(dict(sations), indent=4)
