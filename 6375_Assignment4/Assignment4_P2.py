import json

class Tweet(object):
	def __init__ (self, id, content):
		self.id = id
		self.text = content

	def __repr__ (self):
		return 'Tweet (id=%s, text=%s)' % (self.id, self.text)
	def get_id(self):
		return self.id

def json_tweet_reader(file):
	# instantiate list of tweets
	tweets = []
	# create a tweet object from each line
	for line in open(file, mode="r"):
		t = json.loads(line)
		tweet = Tweet(id = t['id'], content = t['text'])
		tweets.append(tweet)
	return tweets

def txt_seed_reader(file):
	seeds = []
	for line in open(file, mode="r"):
		seed = line.replace(',', '').replace('\n', '')
		seeds.append(seed)
	print seeds
	print len(seeds)
	return seeds

def get_seed_tweets(seed_ids, tweets):
	seed_tweets = []
	for tweet_id in seed_ids:
		# print('*************')
		# print (tweet_id)
		for tweet in tweets:
			# print (tweet.get_id())
			if str(tweet.get_id()) == str(tweet_id):
				seed_tweets.append(tweet)
				break

	# print(seed_tweets)
	return seed_tweets


def get_clusters(tweets, seeds):
	for tweet in tweets:
		for seed in seeds:
			compute_jaccard(tweet, seed)


tweets = json_tweet_reader('Tweets.json')
seed_ids = txt_seed_reader('InitialSeeds.txt')
seed_tweets = get_seed_tweets(seed_ids, tweets)
get_clusters(tweets, seed_tweets)