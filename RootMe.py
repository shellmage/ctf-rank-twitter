from urllib import parse
from lxml import html

import requests
import time

# Delay between API requests
# to avoid HTTP error 429 (Too Many Requests)
# 500ms looks to be a good compromize

DELAY = 0.5

RM_URL_ROOT  = 'https://www.root-me.org'

# Shortened URL encoding function
encode = parse.urlencode

class RootMe:

    def __init__(self, login):
        self._login = login

    # -- Unified api compliant get method
    def get(self, url):
        time.sleep(DELAY)

        response = requests.get( url )

        if not response.ok:
            self.panic(f'HTTP Error on ({ url })[{ response.status_code }]')
        
        return response

    def fetchInfo(self):

        url = f'{ RM_URL_ROOT }/{ self._login }'

        tree = html.fromstring( self.get( url ).text )
        rank = tree.xpath('//div/span[(text() = "Place")]/preceding-sibling::h3').pop().text_content().strip()
        points = tree.xpath('//div/span[(text() = "Points")]/preceding-sibling::h3').pop().text_content().strip()

        return f'#{rank} ({points}pts)'

    # -- Pretty print
    def pprint(self):
        return f'Root-me rank : { self.fetchInfo() }'

    def panic(self, msg):
        print(f'Error : {msg}')
        exit(1)
