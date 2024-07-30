import requests
import json
import time
import subprocess
from ua_info import ua_list
import random

#时间戳获取
timestamp = int(time.time() * 1000)  # 将秒转换为毫秒
print(timestamp)

#进入并执行js文件，查询的单词进行传参，再返回结果(主要是sign的破解算法)
def call_js_function(word):
    result = subprocess.run(
        ['node', '百度翻译参数破译.js',word],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

#发送请求方法
def tran(word,js_res,timestamp):
    cookies = {
        'BIDUPSID': '4FD4308EC7FE26351606B171AF6BB234',
        'PSTM': '1717406317',
        'BAIDUID': '4FD4308EC7FE26359BFAA02C8DE44430:FG=1',
        'MCITY': '-60880%3A194%3A',
        'delPer': '0',
        'BAIDUID_BFESS': '4FD4308EC7FE26359BFAA02C8DE44430:FG=1',
        'ZFY': 'JM5WMQp8SQNgbcuXwGsVGyEt1l36gtNkkX0ErJAWMaw:C',
        'H_WISE_SIDS': '60448_60360_60452_60466_60441',
        'H_PS_PSSID': '60448_60360_60452_60466_60441_60492_60498',
        'PSINO': '7',
        'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
        'BA_HECTOR': '8h002480a48ga08k20a521a40hl2lf1j9rcc01u',
        'BCLID': '11133934466993760698',
        'BCLID_BFESS': '11133934466993760698',
        'BDSFRCVID': '1RPOJexroG3aT7rtwEihM2xkjzky-p7TDYLEOwXPsp3LGJLVYm5TEG0Ptq58Eh4b6j3eogKK3mOTHR8F_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
        'BDSFRCVID_BFESS': '1RPOJexroG3aT7rtwEihM2xkjzky-p7TDYLEOwXPsp3LGJLVYm5TEG0Ptq58Eh4b6j3eogKK3mOTHR8F_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
        'H_BDCLCKID_SF': 'tbC8VCDKJDD3H48k-4QEbbQH-UnLq-FtBgOZ04n-ah05Hf-6KR8Bj6_yXH5Oa-TE25KLQI3m3UTdsq76Wh35K5tTQP6rLqcLJGn4KKJxbPDhbh5dj-K-M6t8hUJiB5JLBan7bDnIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC8lejuaj65LeU5eetjK2CntsJOOaCvi8DnOy4oWK441DUQntbjJfRcEohC-Mnv8JRvwqJ0b3M04X-o9-hvT-54e2p3FBUQZDD52Qft20b0LjH74aT3aJDLe0R7jWhk5Dq72yhKWQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJ6F8tRFqoCvt-5rDHJTg5DTjhPrMKfrrWMT-MTryKKOqQI3KfKIC26OYDRkfMl6WhCrjJanRhlRNB-3iV-OxDUvnyxAZWfFtLUQxtNRJQCKy3RPMHCQFDPoobUPUDUc9LUvNfgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtKDBbDDCj6L3-RJH-xQ0KnLXKKOLVM3bfp7ketn4hUt5-q3WKl88tqOEBRrOBbcL2-IVqK32QhrdQf4WWb3ebTJr32Qr-fTEJxbpsIJM5bLheMLJjMKqajJ-aKviaKOEBMb1VCnDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6JLeHuDtjKDfKresJoq2RbhKROvhj4a0l8gyxoObtRxtK6n_-o2bh5EjhC42-R824P-qq0fLU3kBgT9LMnx--t58h3_XhjZhjL7QttjQn3DJRb4BIbtJJF5eJ7TyU45hf47ybKO0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRQ2QJ8BtD-KbfK',
        'H_BDCLCKID_SF_BFESS': 'tbC8VCDKJDD3H48k-4QEbbQH-UnLq-FtBgOZ04n-ah05Hf-6KR8Bj6_yXH5Oa-TE25KLQI3m3UTdsq76Wh35K5tTQP6rLqcLJGn4KKJxbPDhbh5dj-K-M6t8hUJiB5JLBan7bDnIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC8lejuaj65LeU5eetjK2CntsJOOaCvi8DnOy4oWK441DUQntbjJfRcEohC-Mnv8JRvwqJ0b3M04X-o9-hvT-54e2p3FBUQZDD52Qft20b0LjH74aT3aJDLe0R7jWhk5Dq72yhKWQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJ6F8tRFqoCvt-5rDHJTg5DTjhPrMKfrrWMT-MTryKKOqQI3KfKIC26OYDRkfMl6WhCrjJanRhlRNB-3iV-OxDUvnyxAZWfFtLUQxtNRJQCKy3RPMHCQFDPoobUPUDUc9LUvNfgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtKDBbDDCj6L3-RJH-xQ0KnLXKKOLVM3bfp7ketn4hUt5-q3WKl88tqOEBRrOBbcL2-IVqK32QhrdQf4WWb3ebTJr32Qr-fTEJxbpsIJM5bLheMLJjMKqajJ-aKviaKOEBMb1VCnDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6JLeHuDtjKDfKresJoq2RbhKROvhj4a0l8gyxoObtRxtK6n_-o2bh5EjhC42-R824P-qq0fLU3kBgT9LMnx--t58h3_XhjZhjL7QttjQn3DJRb4BIbtJJF5eJ7TyU45hf47ybKO0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRQ2QJ8BtD-KbfK',
        'smallFlowVersion': 'old',
        'RT': f'"z=1&dm=baidu.com&si=f8401b89-efbd-4724-9dc1-770fce5c6382&ss=lywaillv&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=3v7uwj&ul=2qp&hd=2u6"',
        'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1721610631',
        'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574': '1721610631',
        'REALTIME_TRANS_SWITCH': '1',
        'FANYI_WORD_SWITCH': '1',
        'HISTORY_SWITCH': '1',
        'SOUND_SPD_SWITCH': '1',
        'SOUND_PREFER_SWITCH': '1',
        'ab_sr': '1.0.1_MDFjZWI3Mzk1OTU3ZjhiN2M2ZTA2YmE4MDM5M2Q1ZjkyNmY4Zjk1YzVmZTI0Yjk1M2JkMWRjNTUzMDRjNjRlZDIzYjdmZDMyZGY5YTMwOTE3OGYwMjI1YWQwMWM3YTNiYTE4ZDc4YjE1OWE3MWNhM2UyZmE1MDVkNWVkY2FhOGY2OTJkY2QwOTA0MzlkOTdmODIwZDg5YTQ0NjY0ZTY3YQ==',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://fanyi.baidu.com',
        'Referer': "https://fanyi.baidu.com/?aldtype=16047",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',

    }

    params = {
        'from': 'zh',
        'to': 'en',
    }

    data = {
        'from': 'zh',
        'to': 'en',
        'query': word,
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': js_res,
        'token': 'd00baeca2247e76549934b1a565212e5',
        'domain': 'common',
        'ts': timestamp,
    }

    response = requests.post('https://fanyi.baidu.com/v2transapi', params=params, cookies=cookies, headers=headers, data=data)

    res = response.text

    res = json.loads(res)
    res = res['trans_result']['data'][0]['dst']
    
    return res
    
    
#cookie可以通过请求百度首页拿到，注意user-agent
def get_():
    headers = {'User-Agent':random.choice(ua_list)}
    
    url = 'https://www.baidu.com'
    
    res = requests.get(url=url,headers=headers)
    
    cookies = res.cookies
    
    return cookies


#程序执行的主函数，传参要翻译的word
def baidu_tran(word):
    print("查询:--"+word+"--")
    js_res = call_js_function(word)

    print(js_res)

    response= tran(word,js_res,timestamp)

    print(response)
    
    return response
    
    
#inlet
##################################
if __name__ == '__main__':
    baidu_tran(word = '同声传译')
##################################
