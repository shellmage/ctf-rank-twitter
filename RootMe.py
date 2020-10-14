from htmldom import htmldom
from urllib import parse

import twitter
import requests
import json
import time
import Settings

# Delay between API requests
# to avoid HTTP error 429 (Too Many Requests)
# 100ms looks to be enough atm

DELAY = 0.1
API   = 'https://api.www.root-me.org'

# Shortened URL encoding function
encode = parse.urlencode

class RootMe:

    def __init__(self, login, password):
        self._login = login
        self._password = password

        self.session = requests.Session()
        self.login()

    # -- Log user in API endpoint
    def login(self):
        params = encode({ 
            'login'    : self._login, 
            'password' : self._password 
        })

        request = self.session.get( f'{API}/login?{params}' )

        JSON = json.loads( request.text ).pop()

        if 'info' not in JSON:
            self.panic('Invalid credentials.')
            
    # -- Resolve user ID based on username
    def getUserId(self):
        time.sleep(DELAY)

        params = encode({ 
            'nom' : self._login 
        })

        request = self.session.get( f'{API}/auteurs?{params}' )

        JSON = json.loads( request.text ).pop()

        if len(JSON) == 0:
            self.panic( f'No matching user [{self._login}]' )
            
        elif len(JSON) != 1:
            self.panic( f'Several users found with login [{self._login}].' )

        _, value = JSON.popitem()

        return value.get('id_auteur')

    # -- Fetch user score
    def fetchScore(self):
        time.sleep(DELAY)

        userid  = self.getUserId()
        request = self.session.get( f'{API}/auteurs/{userid}' )
        JSON    = json.loads( request.text )

        if 'score' not in JSON:
            self.panic('Unknown error fetching user score.')

        return JSON.get('score')

    # -- Fetch user rank
    # Dirty stuff, you should better not read that
    def fetchRank(self):
        time.sleep(DELAY)

        url = '{}/{}?inc=score&lang=fr'.format(
            API.replace('api.', ''),
            self._login
        )

        dom = htmldom.HtmlDom().createDom(requests.get(url).text)
        span = dom.find('div.medium-4 > span.txxl')[1].html().replace(' ', '').replace('\n', '').split('>')

        myRank = span[1].split('<')[0]
        maxRank = span[2].split('<')[0].replace('/', '')

        return f'{myRank}/{maxRank}'

    # -- Pretty print
    def pprint(self):
        return f'Root-me rank : {self.fetchRank()} ({self.fetchScore()} pts)\n'

    def panic(self, msg):
        print(f'Error : {msg}')
        print('Program will exit.')
        exit(1)