import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from user_data import *


class TwitterClient(object): 

	def __init__(self): 

		try: 
			self.auth = OAuthHandler(user_key, user_secret) 
			self.auth.set_access_token(access_token_main, access_token_secret) 
			self.my_api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 

		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 

		analysis = TextBlob(self.clean_tweet(tweet)) 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count=10): 

		twts = [] 

		try: 
			tweets_fetched = self.my_api.search(q=query, count=count) 

			for tweet in tweets_fetched: 
				parsed_tweet = {} 

				parsed_tweet['text'] = tweet.text 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				if tweet.retweet_count > 0: 
					if parsed_tweet not in twts: 
						twts.append(parsed_tweet) 
				else: 
					twts.append(parsed_tweet) 

			return twts 

		except tweepy.TweepError as e: 
			print("Error : " + str(e)) 


def main(): 
	my_api = TwitterClient() 
	twts = my_api.get_tweets(query='Google', count=200) 
	pos_twts = [tweet for tweet in twts if tweet['sentiment'] == 'positive'] 
	print("Positive tweets percentage: {} %".format(100 * len(pos_twts) / len(twts))) 
	neg_twts = [tweet for tweet in twts if tweet['sentiment'] == 'negative'] 
	print("Negative tweets percentage: {} %".format(100 * len(neg_twts) / len(twts))) 
	print("Neutral tweets percentage: {} % \
     ".format(100 * (len(twts) - (len(neg_twts) + len(pos_twts))) / len(twts))) 
	print("\n\nPositive twts:") 
	for tweet in pos_twts[:10]: 
		print(tweet['text']) 
	print("\n\nNegative twts:") 
	for tweet in neg_twts[:10]: 
		print(tweet['text']) 


if __name__ == "__main__": 
	main() 
