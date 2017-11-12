from ConfigParser import SafeConfigParser
from random import randint
import twitter, time, sys, os, json, pprint, urllib, re, random

random.seed()
pp = pprint.PrettyPrinter(indent=2)

parser = SafeConfigParser()
parser.read('secrets.cfg')

# Twitter credentials
CONSUMER_KEY = parser.get('Twitter', 'CONSUMER_KEY')
CONSUMER_SECRET = parser.get('Twitter', 'CONSUMER_SECRET')
ACCESS_KEY = parser.get('Twitter', 'ACCESS_KEY')
ACCESS_SECRET = parser.get('Twitter', 'ACCESS_SECRET')

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_KEY,
                  access_token_secret=ACCESS_SECRET)

already_captioned = set()

screen_name = '@youtubeartifact'

tweets = api.GetUserTimeline(screen_name=screen_name, count=50)

tweets_with_media = []

for tweet in tweets:
	if tweet.media:
		for media in tweet.media:
			if media['media_url']:
				tweets_with_media.append(tweet)

tweet_of_interest = tweets_with_media[randint(0, len(tweets_with_media)-1)]

pp.pprint(tweet_of_interest.id)

in_reply_to_url = 'https://twitter.com/youtubeartifact/status/' + str(tweet_of_interest.id)


urllib.urlretrieve(tweet_of_interest.media[0]['media_url'], 'tmp.jpg')


output = os.system('sh /Users/prem/Desktop/Development/sandbox/tensorflow-models/models/research/im2txt/run.sh > output.txt')

print('done!')

f = open("output.txt","r")
output = f.read().splitlines()
f.close()

caption_raw = output[randint(0, 2)];

best_guess_caption = re.search(r'\)([^(]+)\(', caption_raw).group(1)


message = best_guess_caption + ' ' + in_reply_to_url

print(message)

status = api.PostUpdate(message, in_reply_to_status_id=tweet_of_interest.id)


'''
for line in api.GetStreamFilter(track=['@LetsBeSapid']):
	status = api.PostUpdate(message)
'''