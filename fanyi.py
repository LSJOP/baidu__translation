import requests
import json
import sys


class fanyi(object):
    """模拟百度翻译"""
    def __init__(self, words):
        # 请求头
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                                      " AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/54.0.2840.99 Safari/537.36"}
        # 获取输入的词汇
        self.words = words
        # 输入词汇的语言
        self.lan = "zh"
        self.to = "en"

    def LangDetect(self):
        """检测输入的语言"""
        url = "http://fanyi.baidu.com/langdetect"
        data = {"query": self.words}
        response = requests.post(url=url, headers=self.headers, data=data)
        lan = response.content.decode()   # {"error":0,"msg":"success","lan":"zh"}  # 返回的是json字符串
        lan = json.loads(lan)  # 转换成字典
        self.lan = lan['lan']  # 拿到检查到的语言类型
        if self.lan == 'en':
            # 如果输入的是英文则翻译为英文
            self.to = 'zh'

    def FanYi(self):
        """翻译"""
        url = "http://fanyi.baidu.com/v2transapi"
        data = {"from": self.lan, "to": self.to, "query": self.words, "transtype": "realtime", "simple_means_flag": "3"}
        response = requests.post(url=url, headers=self.headers, data=data)
        result_dict = json.loads(response.content.decode())  # 将拿到的json字符串转换成字典
        result_words = result_dict['trans_result']['data'][0]['dst']  # 拿到翻译的词汇
        return result_words

    def run(self):
        """开始翻译"""
        self.LangDetect()          # 检测输入词汇的语言
        words = self.FanYi()       # 拿到翻译的词汇
        return words


if __name__ == '__main__':
    input_words = sys.argv[1]
    fanyi = fanyi(input_words)
    words = fanyi.run()
    print(input_words+' 翻译为:'+words)




