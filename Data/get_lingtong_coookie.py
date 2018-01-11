import requests
from bs4 import BeautifulSoup
import re

class GetLingTongCookie(object):
    def __init__(self):
        self.path = 'C:\\Users\Amos\PycharmProjects\Data\Data\lingtong_cookie'

    def access_login_page(self):
        url = 'http://lingtong.info/gb/login.asp'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        a = soup.select('script[type="text/javascript"]')[0].get('src')
        cookie = dict(response.cookies.items())
        gt = re.findall(r'gt=(.*?)&', a)[0]
        challenge = re.findall(r'challenge=(.*)', a)[0]
        return {'gt':gt,'challenge':challenge,'cookie':cookie}

    def geetest_cracked(self,gt,challenge):
        params = {
            'user': 'Amos',
            'pass': '379833553',
            'gt': gt,
            'challenge': challenge,
            'referer': 'http://lingtong.info',
            'return': 'json',
            'model': ''
        }

        url_jiyan = 'http://jiyanapi.c2567.com/shibie'
        response1 = requests.get(url_jiyan, params=params, timeout=60)
        geetest_msg = response1.json()
        return geetest_msg

    def get_cookie(self):
        response = self.access_login_page()
        geetest_msg = self.geetest_cracked(gt=response['gt'],challenge=response['challenge'])
        if geetest_msg['status'] == "ok":
            data = {
                'gxurl': '',
                'proid': '',
                'user': 'TQTD',
                'password': '139286',
                'geetest_challenge': geetest_msg['challenge'],
                'geetest_validate': geetest_msg['validate'],
                'geetest_seccode': '%s|jordan' % geetest_msg['validate']
            }
            url_login = 'http://lingtong.info/gb/member_login.asp'
            key = list(response['cookie'].keys())[0]
            headers = {
                'Cookie': '%s=%s' %(key,response['cookie'][key])
            }
            response2 = requests.post(url_login, data=data, headers=headers)
            self.cookie = response['cookie']
            print('获取cookie函数，得到的cookie：',response['cookie'],self.cookie)
            with open(self.path,'w') as f:
                f.write(str(self.cookie))
            print('写入文件完成')
        else:
            self.get_cookie()