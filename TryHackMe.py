import requests
import json
from lxml import html
import Settings

THM_LOGIN    = Settings.THM_LOGIN
THM_PASSWORD = Settings.THM_PASSWORD
THM_USERNAME = Settings.THM_USERNAME
THM_WEBSITE  = 'https://tryhackme.com'


def getTryHackMeRankAndUsersCount():
   #Log into the platform
   session = requests.Session()
   response = session.get(THM_WEBSITE + "/login")
   tree = html.fromstring(response.text)
   csrf_token = tree.xpath('//input[@name="_csrf"]/@value')
   response = session.post(THM_WEBSITE + "/login", data = {"email": THM_LOGIN, "password": THM_PASSWORD, "_csrf": csrf_token[0]})

   #Get global stats
   response = session.get(THM_WEBSITE + "/api/getstats")
   globalStats = json.loads(response.text)

   #Get user stats
   response = session.get(THM_WEBSITE + "/api/usersRank/" + THM_USERNAME)
   userStats =  json.loads(response.text)

   return str(userStats['userRank']), str(globalStats['totalUsers'])
