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

DELAY       = 0.1
LOGIN       = Settings.ROOTME_LOGIN
PASSWORD    = Settings.ROOTME_PASSWORD
API         = 'https://api.www.root-me.org'

# Shortened URL encoding function
enc = parse.urlencode


def panic(msg):
    print('Error : {}'.format(msg))
    print('Program will exit.')
    exit(1)


def login():
    p = { 'login': LOGIN, 'password': PASSWORD }
    r = requests.get('{}/login?{}'.format( API, enc(p) ))
    j = json.loads(r.text).pop()

    if j.get('info', False) == False:
        panic('Invalid credentials 1.')

    return r.cookies


def getUserId(cookies):
    time.sleep(DELAY)

    p = { 'nom' : LOGIN }
    r = requests.get('{}/auteurs?{}'.format( API, enc(p) ), cookies=cookies)
    j = json.loads(r.text).pop()

    if len(j) == 0:
        panic('No matching user {}'.format(LOGIN))
    elif len(j) != 1:
        print('Several users found with login [{}].'.format(login))
        print('Will take a random one.')

    _, value = j.popitem()

    return value.get('id_auteur')


def fetchScore(userid, cookies):
    time.sleep(DELAY)

    r = requests.get(API + '/auteurs/{}'.format(userid), cookies=cookies)
    j = json.loads(r.text)

    return j.get('score')


# Dirty stuff, you should better not read that
def fetchRank(cookies):
    time.sleep(DELAY)

    url = '{}/{}?inc=score&lang=fr'.format(
        API.replace('api.', ''),
        LOGIN
    )

    dom = htmldom.HtmlDom().createDom(requests.get(url).text)
    span = dom.find('div.medium-4 > span.txxl')[1].html().replace(' ', '').replace('\n', '').split('>')

    myRank = span[1].split('<')[0]
    maxRank = span[2].split('<')[0].replace('/', '')

    return '{}/{}'.format(myRank, maxRank)
