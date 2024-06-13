
import requests
import unittest
class baidu(unittest.TestCase):
    def setUp(self):
        self.url = "http://www.baidu.com/s?"

        self.params = {"wd":"python","fr":"search"}

        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
        }

        self.r = requests.get(self.url,params=self.params,headers = self.headers)

    def test_baidu(self):
        print("开始测试百度搜索接口")
        respones = self.r.text
        self.assertEqual(self.r.status_code,200)
        self.assertIn('python',respones)
        # print(self.r.status_code)
        print("测试通过")

    def tearDown(self):
        print("执行完成！！！")

if __name__ == '__main__':
    unittest.main()
