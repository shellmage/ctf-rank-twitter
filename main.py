from htmldom import htmldom
from urllib import parse
import twitter
import requests
import json
import time

twitterAPI = twitter.Api(
    consumer_key        = '',
    consumer_secret     = '',
    access_token_key    = '',
    access_token_secret = ''
)

# Delay between API requests
# to avoid HTTP error 429 (Too Many Requests)
# 100ms looks to be enough atm

DELAY       = 0.1
LOGIN       = ''
PASSWORD    = ''
API         = 'https://api.www.root-me.org'

# Shortened URL encoding function
enc = parse.urlencode 

def panic(msg):
    print('Error : {}'.format(msg))
    print('Program will exit.')
    exit(1)

def login(login, password):
    p = { 'login' : login, 'password' : password }
    r = requests.get('{}/login?{}'.format( API, enc(p) ))
    j = json.loads(r.text).pop()

    if j.get('info', False) == False:
        panic('Invalid credentials.')

    return r.cookies

def getUserId(login, cookies):
    time.sleep(DELAY)

    p = { 'nom' : login }
    r = requests.get('{}/auteurs?{}'.format( API, enc(p) ), cookies=cookies)
    j = json.loads(r.text).pop()

    if len(j) == 0:
        panic('No matching user {}'.format(login))
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
def fetchRank(login, cookies):
    time.sleep(DELAY)

    url = '{}/{}?inc=score&lang=fr'.format(
        API.replace('api.', ''),
        login
    )

    dom = htmldom.HtmlDom().createDom(requests.get(url).text)
    span = dom.find('div.medium-4 > span.txxl')[1].html().replace(' ', '').replace('\n', '').split('>')

    myRank = span[1].split('<')[0]
    maxRank = span[2].split('<')[0].replace('/', '')

    return '{}/{}'.format(myRank, maxRank)

def updateTwitterBio(rank, score):
    twitterAPI.UpdateProfile(
        description = 'Root-me rank : {} ({} pts)'.format(rank, score)
    )

    # Should probably handle errors and stuff
    # Feel free to PR

def main():
    cookies = login(LOGIN, PASSWORD)
    userID  = getUserId(LOGIN, cookies)
    score   = fetchScore(userID, cookies)
    rank    = fetchRank(LOGIN, cookies)

    updateTwitterBio(rank, score)

if __name__ == "__main__":
    main()
