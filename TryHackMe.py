from lxml import html

import requests
import json
import Settings

THM_WEBSITE  = 'https://tryhackme.com'

class TryHackMe:

   def __init__(self, login, password, username):
      self._login = login
      self._password = password
      self._username = username

      self.session = requests.Session()
      self.login()

   def login(self):
      response = self.session.get(f'{ THM_WEBSITE }/login')
      tree = html.fromstring(response.text)
      csrf_token = tree.xpath('//input[@name="_csrf"]/@value')
      response = self.session.post(f'{ THM_WEBSITE }/login', data = {'email': self._login, 'password': self._password, '_csrf': csrf_token[0]})

   def getTotalUsers(self):
      response = self.session.get(f'{ THM_WEBSITE }/api/getstats')
      globalStats = json.loads(response.text)

      return str( globalStats['totalUsers'] )

   def getUserRank(self):
      response = self.session.get(f'{ THM_WEBSITE }/api/usersRank/{ self._username }')
      userStats =  json.loads(response.text)

      return str(userStats['userRank'])

   def getUserScore(self):
      response = self.session.get(f'{ THM_WEBSITE }/api/user/{ self._username }')
      userScore =  json.loads(response.text)

      return str(userScore['points'])

   def pprint(self):
      return f'TryHackMe rank : {self.getUserRank()}/{self.getTotalUsers()} ({self.getUserScore()} pts)\n'