from RootMe import RootMe
from TryHackMe import TryHackMe

import twitter
import Settings

twitterAPI = twitter.Api(
    consumer_key        = Settings.TWITTER_CONSUMER_KEY,
    consumer_secret     = Settings.TWITTER_CONSUMER_SECRET,
    access_token_key    = Settings.TWITTER_TOKEN_KEY,
    access_token_secret = Settings.TWITTER_TOKEN_SECRET
)

def updateTwitterBio(rm_client, thm_client, htb_client):
    bio = ''

    if rm_client != None:
        bio += rm_client.pprint()

    if thm_client != None:
        bio += thm_client.pprint()

    if htb_client != None:
        bio += htb_client.pprint()

    twitterAPI.UpdateProfile( description = bio )

def main():
    # Init root-me client
    rm = RootMe (
        Settings.ROOTME_LOGIN,
    )

    # Init tryhackme client
    thm =  TryHackMe (
        Settings.THM_LOGIN,
        Settings.THM_PASSWORD,
        Settings.THM_USERNAME
    )

    # Twitter description update
    updateTwitterBio(rm, thm, None)

    print("Twitter update successful")

if __name__ == "__main__":
    main()
