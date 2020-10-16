from urllib import parse
from lxml import html

import requests
import time

# Delay between API requests
# to avoid HTTP error 429 (Too Many Requests)
# 500ms looks to be a good compromize

DELAY = 0.5

RM_URL_ROOT  = 'https://www.root-me.org'
RM_URL_API   = 'https://api.www.root-me.org'

# Shortened URL encoding function
encode = parse.urlencode

class RootMe:

    # -- Inner challenge class
    class RootMeChall:
        def __init__(self, data):
            self.name       = data.get('titre')
            self.type       = data.get('rubrique')
            self.subt       = data.get('soustitre')
            self.score      = data.get('score')
            self.url        = data.get('url_challenge')
            self.difficulty = data.get('difficulte')
            self.author     = data.get('auteurs')

    # -- Init function
    def __init__(self, login, password):
        self._login = login
        self._password = password

        self.session = requests.Session()
        self.login()
        self.update()

    # -- Log user in API endpoint
    def login(self):
        params = encode({ 
            'login'    : self._login, 
            'password' : self._password 
        })

        self.get( f'{ RM_URL_API }/login?{ params }' )

    # -- Update local data
    def update(self):
        self.rank  = self.fetchRank()
        self.score = self.fetchScore()
        self.solve = self.fetchChalls()

    # -- Unified api compliant get method
    def get(self, url):
        time.sleep(DELAY)

        response = self.session.get( url )

        if not response.ok:
            self.panic(f'HTTP Error on ({ url })[{ response.status_code }]')
        
        return response
            
    # -- Resolve user ID based on username
    def getUserId(self):

        params = encode({ 
            'nom' : self._login
        })

        response = self.get( f'{ RM_URL_API }/auteurs?{ params }' ).json()[0]

        for v in response.values():
            if v.get('nom') == self._login:
                return v.get('id_auteur')
        
        self.panic( f'No matching user [{self._login}]' )

    # -- Fetch user score
    def fetchScore(self):

        response = self.get( f'{ RM_URL_API }/auteurs/{ self.getUserId() }' ).json()

        return response.get('score')

    # -- Fetch user rank
    # Cannot properly use root-me api atm
    def fetchRank(self):

        url = f'{ RM_URL_ROOT }/{ self._login }?inc=score&lang=fr'

        tree = html.fromstring( self.get( url ).text )
        score = tree.xpath('//span[contains(@class, "txxl") ]/span[@class = "gris"]').pop()

        myRank = score.getparent().text.strip()
        maxRank = score.text

        return f'{myRank}{maxRank}'

    # -- Fetch challenge(s) id(s) solved
    def fetchChalls(self):

        response = self.get( f'{ RM_URL_API }/auteurs/{ self.getUserId() }' ).json()

        return sorted( [ x.get('id_challenge') for x in response.get('validations') ] )

    # -- Fetch challenge info by id
    def fetchChallInfo(self, id):

        return self.RootMeChall( self.get( f'{ RM_URL_API }/challenges/{ id }' ).json() )

    # -- Get freshly solved challenges
    def getNewSolve(self):

        return [self.fetchChallInfo( x ) for x in self.fetchChalls() if x not in self.solve]

    # -- User solved new chall since last check ?
    def hasNewSolve(self):

        return self.fetchChalls() != self.solve

    # -- User hase new rank since last check ?
    def hasNewRank(self):

        return self.fetchRank() != self.rank

    # -- User hase new rank since last check ?
    def hasNewScore(self):

        return self.fetchScore() != self.score

    # -- Pretty print twitter bio
    def pprint(self):
        return f'Root-me rank : { self.fetchRank() } ({ self.fetchScore() } pts)\n'

    def panic(self, msg):
        print(f'Error : {msg}')
        exit(1)

        