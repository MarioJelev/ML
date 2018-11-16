import json

class Tweet(object):
	def __init__ (self, id, content):
		self.id = id
		self.text = content

	def __repr__ (self):
		return 'Tweet (id=%s, text=%s)' % (self.id, self.text)
	def get_id(self):
		return self.id
	def get_text(self):
		return self.text

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

def compute_jaccard(tweet1, tweet2):
	t1_list = tweet1.split(' ')
	t2_list = tweet2.split(' ')
	intersect = list(set(t1_list) & set(t2_list))
	union = list(set(t1_list) | set(t2_list))
	distance = 1 - (float(len(intersect)) / len(union))
	return distance

def computeNewCentroids(clusters):
	for cluster in clusters:
		tweetsInCluster = clusters[cluster]
		

def get_clusters(tweets, seeds, clusters):
	newClusters = {}
	for tweet in tweets:
		distanceToSeeds = {}
		for seed in seeds:
			# find the distance between the tweet and the seed
			dist = compute_jaccard(tweet.get_text(), seed.get_text())
			distanceToSeeds[seed.get_id()] = dist

		tweet_cluster = min(distanceToSeeds, key=distanceToSeeds.get)
		if tweet_cluster not in newClusters:
			newClusters[tweet_cluster] = [tweet.get_id]
		else:
			newClusters[tweet_cluster].append(tweet.get_id)
	if newClusters == clusters:
		return newClusters
	else:
		newClusters = computeNewCentroids(newClusters)
		# print (tweet.get_id(), distanceToSeeds)
	# compute_jaccard('the long march', 'ides of march')


tweets = json_tweet_reader('Tweets.json')
seed_ids = txt_seed_reader('InitialSeeds.txt')
seed_tweets = get_seed_tweets(seed_ids, tweets)
#initialize dictionary with the keys as the seeds
clusters = {}
for id in seed_ids:
	clusters[id] = []
get_clusters(tweets, seed_tweets, clusters)