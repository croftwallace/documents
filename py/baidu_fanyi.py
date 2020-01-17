import requests
import json
import random
import hashlib
import sys

class BaiduTranslate(object):
    def __init__(self, text):
        self.text = text
        self.params = {'query': text}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
        pass

    def langdetect(self):
        url = 'https://fanyi.baidu.com/langdetect'
        response = requests.post(url, headers=self.headers, params=self.params)
        res = json.loads(response.content.decode())
        return res['lan']

    def translate(self):
        appid = '20151113000005349'
        secretKey = 'osubCEzlGjzvw8qdQc41'
        q = self.text
        from_lang = self.langdetect()
        if from_lang == 'en':
            to_lang = 'zh'
        else:
            to_lang = 'en'
        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        url = 'http://fanyi-api.baidu.com/api/trans/vip/translate?appid=' + appid + '&q=' + q + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(
            salt) + '&sign=' + sign
        response = requests.post(url, headers=self.headers)
        res = json.loads(response.content.decode())
        # print(res)
        print(res['trans_result'][0]['dst'])


if __name__ == '__main__':
    text = "I've been putting new stuff in this course every month, and I continue to plan to do that through 2019."
    for item in range(1, len(sys.argv)):
        text += sys.argv[item] + " "
    baidu_translate = BaiduTranslate(text)
    baidu_translate.translate()