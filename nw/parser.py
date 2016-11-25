

import datetime
from typing import List
from urllib.parse import urljoin

from dateutil import parser
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from nw.loggers import logger


class NwBase:
    BASE_URL = 'http://netwars.pl/'
    BASE_URL_TOPIC = 'http://netwars.pl/temat/{!s}'
    OT_FORUM_NUMBER = '4'

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.logged_in = False

    def login(self):
        if not self.username or not self.password:
            raise ValueError('No cred')

        payload = {
            'tnick': self.username,
            'tpass': self.password
        }

        nwsession = requests.session()
        nwsession.post(urljoin(self.BASE_URL, 'login'), payload)
        self.nwsession = nwsession
        self.logged_in = True

    def logout(self):
        self.nwsession.post(urljoin(self.BASE_URL, 'logout'))
        self.logged_in = False


class NwParser(NwBase):
    def __repr__(self):
        return '%s(%r)' % (self.__class__, self.username)

    @staticmethod
    def _url_to_soup(url: str):
        return BeautifulSoup(requests.get(url).text, 'lxml')

    @staticmethod
    def _nw_datetime_to_real_datetime(nw_date_string, scrape_date=datetime.date.today()):
        if 'Wczoraj' in nw_date_string:
            real_datetime = nw_date_string.replace('Wczoraj,', str(scrape_date))
        elif 'Dzisiaj' in nw_date_string:
            real_datetime = nw_date_string.replace('Dzisiaj,', str(scrape_date))
        else:
            real_datetime = nw_date_string
        return parser.parse(real_datetime)

    @staticmethod
    def topic_differences(old: dict, new: dict) -> dict:
        """
        Return topics that changed between two scrapes
        """
        return dict((set(new.items()) - set(old.items()))).keys()

    @staticmethod
    def live_user_differences(old: list, new: list) -> bool:
        """

        :param old: old version of nw-meta to be compared against
        :param new:
        :return:
        """
        return set(old) == set(new)

    @staticmethod
    def _topic_soup_to_json(soup: BeautifulSoup) -> (list, dict):

        if 'Nie znaleziono' in soup.text:
            raise ValueError('Topic does not exist')

        topic_number = list(filter(
            lambda x: 'topic_' in x, [
                d.get('id', 'not-relevant')
                for d in soup.findAll('div')
                ]
        ))

        topic_id = int(topic_number[0].split('_')[-1])
        navi_list = [a for a in soup.findAll('ul', {'class': 'forum_navi'})][0].findAll('li')
        forum_id = navi_list[1].a['href']
        topic_name = navi_list[2].text

        ids = soup.findAll('div', {'class': 'post'})
        dates = soup.findAll('div', {'class': 'p2_data'})
        nicks = soup.findAll('div', {'class': 'p2_nick'})
        bodies = soup.findAll('div', {'class': 'post_body'})

        dates = map(lambda x: x.text, dates)
        post_bodies = process_post_bodies(bodies)
        user_hrefs = map(lambda x: x.a['href'], nicks)
        user_names = map(lambda x: x.a.text, nicks)
        ids = map(lambda x: x['id'].split('_')[-1], ids)

        posts_list = [
            {
                'topic_id': topic_id,
                'forum_id': forum_id,
                'post_id': post_id,
                'post_date': NwParser._nw_datetime_to_real_datetime(post_date),
                'user_href': href,
                'user_name': uname,
                'post_body': body,
                'cites': cites,
                'unique_post_id': '{!s}.{!s}'.format(topic_id, post_id)

            } for post_id, post_date, href, uname, (body, cites) in
            zip(ids, dates, user_hrefs, user_names, post_bodies)
            ]

        topic_meta = {
            'forum_id': forum_id,
            'topic_id': topic_id,
            'topic_name': topic_name,
            'topic_created_at': posts_list[0]['post_date']
        }

        return posts_list, topic_meta

    def topic_to_json(self, topic_number: int) -> List[object]:
        logger.debug('parsing topic number {!s}'.format(topic_number))
        soup = self._url_to_soup(self.BASE_URL_TOPIC.format(topic_number))
        return self._topic_soup_to_json(soup)

    @staticmethod
    def _list_of_active_users(base_soup):
        return [a['href'] for a in base_soup.findAll(
            'div', attrs={'id': 'footer'}
        )[0].findAll('a')][2:]

    @staticmethod
    def _topics_and_post_number(base_soup):
        topic_ids = [int(z.a['href'].split('/')[-1]) for z in base_soup.findAll('td', {'class': 'topic'})]
        number_of_posts = [int(z.text) for z in base_soup.findAll('td', {'class': 'posts'})]
        return dict(zip(topic_ids, number_of_posts))

    def home_page_status(self) -> (dict, list):
        soup = self._url_to_soup(self.BASE_URL)
        topics = self._topics_and_post_number(soup)
        users = self._list_of_active_users(soup)
        return topics, users


def process_post_bodies(bodies: List[Tag]) -> (str, list):
    for body in bodies:
        cites = list()
        cited = body.findAll('div', {'class': 'cite'})
        if cited:
            cites = [c['name'] for c in cited]
        collect_text = []
        for tag in body:
            if tag.name not in ('div', 'p'):
                if hasattr(tag, 'text'):
                    collect_text.append(tag.text)
                elif isinstance(tag, NavigableString):
                    collect_text.append(str(tag))
                else:
                    collect_text.append('\n')
        else:
            yield ''.join(collect_text), cites


if __name__ == '__main__':
    nw = NwParser()
    res = nw.topic_to_json(173452)
    print(res[0][10])
    topics, users = nw.home_page_status()
    print(topics)
    print(users)
