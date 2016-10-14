__author__ = 'crimzoid'
import requests
from bs4 import BeautifulSoup
from dateutil import parser
import datetime
from urllib.parse import urljoin


from settings import NW_LOGIN, NW_PASSWORD


def cli_green(fn):
    def wrapped(*args, **kwargs):
        return "\033[92m" + fn(*args, **kwargs)
    return wrapped


def scrape_topic_page(topic_number):
    if not isinstance(topic_number, (str, int)):
        raise ValueError("Topic number has to be int or basestring")
    soup = BeautifulSoup(
        requests.get(
            'http://netwars.pl/temat/{0!s}'.format(topic_number)
        ).text
    )
    return soup


class NW(object):
    BASE_URL = 'http://netwars.pl/'
    OT_FORUM_NUMBER = '4'

    def __repr__(self):
        return '%s(%r)' % (self.__class__, self.username)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged_in = False
        self.nwsession = None

    @staticmethod
    def _check_login_success(response):
        if 'Logowanie nie' in response.text:
            return False
        else:
            return True

    def login(self):
        payload = dict(tnick=self.username, tpass=self.password)
        nwsession = requests.session()
        login_response = nwsession.post(urljoin(self.BASE_URL, 'login'), payload)
        if self._check_login_success(login_response):
            self.nwsession = nwsession
            self.logged_in = True
            print("Logged in successfully as {0}".format(self.username))
        else:
            print("invalid login details")

    def logout(self):
        self.nwsession.post(urljoin(self.BASE_URL, 'logout'))
        self.logged_in = False

    def topics(self):
        forum = self.nwsession.get(
            self.BASE_URL + 'forum/' + self.OT_FORUM_NUMBER).text
        soup = BeautifulSoup(forum)
        return [topic.text for topic in soup.findAll('td', {'class': 'topic'})]

#
# BASE_URL = 'http://netwars.pl/'
#
# s = requests.session()
# payload = {
#     'tnick': '=SF=Vengeance',
#     'tpass': 'sorcery7'
# }
# print s.post(urljoin(BASE_URL, 'login'), payload).text
#


nw = NW('=SF=Vengeance','sorcery')
nw.login()

import time
def do_shit():

    print('before 2 secs')
    time.sleep(2)
    print('after 2 secs')


import threading

t = threading.Thread(target=do_shit)

t.start()
print('bla')
print('waiting')
time.sleep(2)
print('AFTER')



