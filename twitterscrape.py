#
# # import tweepy
# # import csv
# # import pandas as pd
# # ####input your credentials here
# consumer_key = '323LP8BZSk47j19y30jwYeahH'
# consumer_secret = 'sG3ivjos4byGUwOs9OjEMJIN0k1BZ4lL9ucOWT2Ymp3hOlMYFk'
# access_token = '2852604626-LiBayEga0rBTXGywQYskxPGtDjse5DD91XQEG4a'
# access_token_secret = '4ZI6tq9TnNScdFKwqJ69ehrtwCebJvFUIsFAyk2gB4o9b'
# #
# # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# # auth.set_access_token(access_token, access_token_secret)
# # api = tweepy.API(auth,wait_on_rate_limit=True)
# # #####United Airlines
# # # Open/Create a file to append data
# # csvFile = open('ua.csv', 'a')
# # #Use csv Writer
# # csvWriter = csv.writer(csvFile)
# #
# # for tweet in tweepy.Cursor(api.search,q="#unitedAIRLINES",count=100,
# #                            lang="en",
# #                            since="2017-04-03").items():
# #     print (tweet.created_at, tweet.text)
# #     csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
#
# import re
# import tweepy
# from tweepy import OAuthHandler
# from textblob import TextBlob
#
# class MyStreamListener(tweepy.StreamListener):
#
#     def on_status(self, status):
#         print("hi")
#         print(status.text)
#
# class TwitterClient(object):
#     '''
#     Generic Twitter Class for sentiment analysis.
#     '''
#     def __init__(self):
#         '''
#         Class constructor or initialization method.
#         '''
#         # keys and tokens from the Twitter Dev Console
#         consumer_key = '323LP8BZSk47j19y30jwYeahH'
#         consumer_secret = 'sG3ivjos4byGUwOs9OjEMJIN0k1BZ4lL9ucOWT2Ymp3hOlMYFk'
#         access_token = '2852604626-LiBayEga0rBTXGywQYskxPGtDjse5DD91XQEG4a'
#         access_token_secret = '4ZI6tq9TnNScdFKwqJ69ehrtwCebJvFUIsFAyk2gB4o9b'
#
#         # attempt authentication
#         try:
#             # create OAuthHandler object
#             self.auth = OAuthHandler(consumer_key, consumer_secret)
#             # set access token and secret
#             self.auth.set_access_token(access_token, access_token_secret)
#             # create tweepy API object to fetch tweets
#             self.api = tweepy.API(self.auth)
#
#             print("GOT HERE")
#         except:
#             print("Error: Authentication Failed")
#
#     def clean_tweet(self, tweet):
#         '''
#         Utility function to clean tweet text by removing links, special characters
#         using simple regex statements.
#         '''
#         return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
#
#     def get_tweet_sentiment(self, tweet):
#         '''
#         Utility function to classify sentiment of passed tweet
#         using textblob's sentiment method
#         '''
#         # create TextBlob object of passed tweet text
#         analysis = TextBlob(self.clean_tweet(tweet))
#         # set sentiment
#         if analysis.sentiment.polarity > 0:
#             return 'positive'
#         elif analysis.sentiment.polarity == 0:
#             return 'neutral'
#         else:
#             return 'negative'
#
#     def get_tweets(self, query, count = 10):
#         '''
#         Main function to fetch tweets and parse them.
#         '''
#         # empty list to store parsed tweets
#         tweets = []
#
#         try:
#             # call twitter api to fetch tweets
#             fetched_tweets = self.api.search(q = query, count = count)
#
#             # parsing tweets one by one
#             for tweet in fetched_tweets:
#                 # empty dictionary to store required params of a tweet
#                 parsed_tweet = {}
#
#                 # saving text of tweet
#                 parsed_tweet['text'] = tweet.text
#                 # saving sentiment of tweet
#                 parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
#
#                 # appending parsed tweet to tweets list
#                 if tweet.retweet_count > 0:
#                     # if tweet has retweets, ensure that it is appended only once
#                     if parsed_tweet not in tweets:
#                         tweets.append(parsed_tweet)
#                 else:
#                     tweets.append(parsed_tweet)
#
#             # return parsed tweets
#             return tweets
#
#         except tweepy.TweepError as e:
#             # print error (if any)
#             print("Error : " + str(e))
#
# def main():
#     # creating object of TwitterClient Class
#     api = TwitterClient()
#     # calling function to get tweets
#     tweets = api.get_tweets(query = 'bitcoin', count = 10000)
#
#     # picking positive tweets from tweets
#     ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
#     # percentage of positive tweets
#     print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
#     # picking negative tweets from tweets
#     ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
#     # percentage of negative tweets
#     print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
#     # percentage of neutral tweets
#     print("Neutral tweets percentage: {} % \
#         ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
#
#     # printing first 5 positive tweets
#     print("\n\nPositive tweets:")
#     for tweet in ptweets[:10]:
#         print(tweet['text'])
#
#     # printing first 5 negative tweets
#     print("\n\nNegative tweets:")
#     for tweet in ntweets[:10]:
#         print(tweet['text'])
#
# if __name__ == "__main__":
#     # calling main function
#     main()

import tweepy

consumer_key = '323LP8BZSk47j19y30jwYeahH'
consumer_secret = 'sG3ivjos4byGUwOs9OjEMJIN0k1BZ4lL9ucOWT2Ymp3hOlMYFk'
access_token = '2852604626-LiBayEga0rBTXGywQYskxPGtDjse5DD91XQEG4a'
access_token_secret = '4ZI6tq9TnNScdFKwqJ69ehrtwCebJvFUIsFAyk2gB4o9b'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

results = api.search(q="cancer", since_id=518857118838181000, max_id=518857136202194000)

for result in results:
    print(result.text)
