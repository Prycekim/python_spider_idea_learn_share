import subprocess
import requests
import json

#执行sign破解js文件获取执行结果，sign以及timestamp（毫秒）
def call_js_function():
    result = subprocess.run(
        ['node', '网易翻译sign参数.js'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

#得到请求返回的密文，拿到response破解js，解密
def res_js_function(a):
    result = subprocess.run(
        ['node', '网易翻译response破译.js',a],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    return result.stdout.strip()


#发送请求的函数
def tran(sign,word):
    url = 'https://dict.youdao.com/webtranslate'
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'dict.youdao.com',
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com/',
        'Sec-Ch-Ua': 'Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    cookie = {
        'DICT_DOCTRANS_SESSION_ID':'YTc0ZDU2MGEtMzVhNS00Y2RhLThmZjMtYTQwNWMzYTBiZTk3',
        'OUTFOX_SEARCH_USER_ID':'739970345@117.28.134.115',
        'OUTFOX_SEARCH_USER_ID_NCOO':'1599551923.1161582',
    }
    
    data = {
        "i": word,
        "from": "auto",
        "to": "",
        "useTerm": "false",
        "dictResult": 'true',
        "keyid": 'webfanyi',
        "sign": sign[0],
        'client': 'fanyideskweb',
        'product': 'webfanyi',
        'appVersion': '1.0.0',
        'vendor': 'web',
        'pointParam': 'client,mysticTime,product',
        'mysticTime': sign[1],
        'keyfrom': 'fanyi.web',
        'mid': '1',
        'screen': '1',
        'model': '1',
        'network': 'wifi',
        'abtest': '0',
        'yduuid': 'abcdefg',
    }

    res = requests.post(url=url,headers=headers,cookies=cookie,data=data)
    
    return res.text


#程序执行主函数，传参要翻译的word
def wangyi_tran(word):
    print(word)
    sign_result = call_js_function()
    sign_result = eval(sign_result)
    print(sign_result)

    

    sign = sign_result
    a = tran(sign,word)
    print(a)

    resp = res_js_function(a)
    resp = json.loads(resp)
    
    eng = resp['translateResult'][0][0]['tgt']
    print(resp)
    print('翻译结果是:--'+eng)
    
    return eng



#inlet
###########################

if __name__ == '__main__':
    a = wangyi_tran('同声传译')
    print(a)
    
###########################