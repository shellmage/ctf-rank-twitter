import twitter

import TryHackMe
import RootMe
import Settings

twitterAPI = twitter.Api(
    consumer_key        = Settings.TWITTER_CONSUMER_KEY,
    consumer_secret     = Settings.TWITTER_CONSUMER_SECRET,
    access_token_key    = Settings.TWITTER_TOKEN_KEY,
    access_token_secret = Settings.TWITTER_TOKEN_SECRET
)


def updateTwitterBio(rootMeDesc, ThmDesc):
    twitterAPI.UpdateProfile(description = rootMeDesc + '\n' + ThmDesc)


def main():
    #RootMe management
    cookies = RootMe.login()
    userID  = RootMe.getUserId(cookies)
    score   = RootMe.fetchScore(userID, cookies)
    rank    = RootMe.fetchRank(cookies)
    print('Root-me rank : {} ({} pts)'.format(rank, score))

    #ThyHackMe management
    thm_user_rank, thm_total_users = TryHackMe.getTryHackMeRankAndUsersCount()
    print('TryHackMe rank : ' + thm_user_rank + '/' + thm_total_users)

    #Twitter description update
    updateTwitterBio('Root-me rank : {} ({} pts)'.format(rank, score), 'TryHackMe rank : ' + thm_user_rank + '/' + thm_total_users)
    print("Twitter update successful")

if __name__ == "__main__":
    main()
