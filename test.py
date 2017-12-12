import requests
from bs4 import BeautifulSoup
import time
import datetime


headers = {
    'Cookie':'ASPSESSIONIDSSCRBSBQ=KAGGDDLDGDLEFIGIKOOEEIKL'
}

response = requests.get('http://www.lingtong.info/gb/price.asp?datew=2017-12-4',headers=headers)
print(response.url)
soup = BeautifulSoup(response.text,'lxml')
a = soup.select('div.part3 div.fl.style06 table tr')
print(len(a))