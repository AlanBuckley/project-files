#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import sqlite3

#Twitter API credentials
consumer_key = "FFjHNuDcapXxwlTvE1kCAsZMw"
consumer_secret = "SYSXcHtWDNkqsbWLHf6UV51QFGsPK245CqgThZ310tp00UwPvt"
access_key = "3084274719-eMn9OZzBHQoxh2c0hJKiNxo7EfZcgsdNfVOTcC8"
access_secret = "c7nUCfyNlTSI2WqlwcUQnNp4Bkwfz5IhTHRTvAI5nK6a9"

def to_db(screen_name):
	f=open('%s_tweets.csv' % screen_name,'r') 
	next(f, None) 
	reader = csv.reader(f)

	sql = sqlite3.connect('\\db.sqlite3\fyp_project_tweets')
	cur = sql.cursor()

	cur.execute('''CREATE TABLE IF NOT EXISTS fyp_project_Tweets
            (date datetime, message char)''') 
			 
	for row in reader:
		cur.execute("INSERT INTO fyp_project_Tweets VALUES (? ,? )", row)
	
	f.close()
	sql.commit()
	sql.close()


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name, count=200, include_rts=False)
	#new_tweets = api.user_timeline(screen_name = screen_name,count=340, include_rts=False)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest));
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200, max_id=oldest)
		#new_tweets = api.user_timeline(screen_name = screen_name,count=340,max_id=oldest,tweet_mode = 'extended')
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("%s tweets downloaded" % (len(alltweets)));
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	#outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8").replace('\n', ' ').replace('\r', '')] for tweet in alltweets]
	outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("MrShen_")
	#to_db("afbucker")