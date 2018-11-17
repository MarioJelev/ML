# Mario Jelev, mvj140030
# Assignment 4, Part 2

import json
import sys

class Tweet(object):
	def __init__ (self, id, content):
		self.id = id
		self.text = content

	def __repr__ (self):
		return 'Tweet (id=%s, text=%s)' % (self.id, self.text)
	def get_id(self):
		return int(self.id)
	def get_text(self):
		return self.text

def json_tweet_reader(file):
	# instantiate list of tweets
	tweets = []
	# create a tweet object from each line
	for line in open(file, mode="r"):
		t = json.loads(line)
		tweet = Tweet(id = t['id'], content = t['text'].encode('utf-8'))
		tweets.append(tweet)
	return tweets

def txt_seed_reader(file):
	seeds = []
	for line in open(file, mode="r"):
		seed = line.replace(',', '').replace('\n', '')
		seeds.append(seed)
	return seeds

def get_seed_tweets(seed_ids, tweets):
	seed_tweets = []
	for tweet_id in seed_ids:
		for tweet in tweets:
			if str(tweet.get_id()) == str(tweet_id):
				seed_tweets.append(tweet)
				break
	return seed_tweets

def compute_jaccard(tweet1, tweet2):
	t1_list = tweet1.split(' ')
	t2_list = tweet2.split(' ')
	intersect = list(set(t1_list) & set(t2_list))
	union = list(set(t1_list) | set(t2_list))
	distance = 1 - (float(len(intersect)) / len(union))
	return distance

def compute_new_centroids(clusters):
	recomputedClusters = {}
	for cluster in clusters:
		tweetsInCluster = clusters[cluster]
		# mean = tweet with smallest average distance to other clusters
		avgDistance = {}
		for tweet1 in tweetsInCluster:
			totDistance = 0
			for tweet2 in tweetsInCluster:
				dist = compute_jaccard(tweet1.get_text(), tweet2.get_text())
				totDistance += dist
			avgDistanceFromOtherTweets = float(totDistance)/len(tweetsInCluster)
			avgDistance[tweet1] = avgDistanceFromOtherTweets
		# get the new center
		cluster_center = min(avgDistance, key=avgDistance.get)
		recomputedClusters[cluster_center] = tweetsInCluster
	return recomputedClusters
		
def print_clusters(cluster):
	for center in cluster:
		print (center.get_id(), [tweet.get_id() for tweet in cluster[center]])
		print('---')

def get_clusters(tweets, centers, clusters):
	newClusters = {}
	for tweet in tweets:
		distanceToSeeds = {}
		for seed in centers:
			# find the distance between the tweet and the center
			dist = compute_jaccard(tweet.get_text(), seed.get_text())
			distanceToSeeds[seed] = dist

		# assignment phase - assign a tweet to its 'cluster', ie the center that it is closest to
		tweet_cluster = min(distanceToSeeds, key=distanceToSeeds.get)
		if tweet_cluster not in newClusters:
			newClusters[tweet_cluster] = [tweet]
		else:
			newClusters[tweet_cluster].append(tweet)

	# if there was no change after reassignment, terminate the algorithm; otherwise, recompute centers of the clusters
	if newClusters == clusters:
		return newClusters
	else:
		newClusters = compute_new_centroids(newClusters)

		return get_clusters(tweets, newClusters.keys(), newClusters)

def compute_sse(clusters):
	sse = 0
	for center in clusters:
		tweets = clusters[center]
		for tweet in tweets:
			dist = compute_jaccard(center.get_text(), tweet.get_text())
			sse += (dist**2)
	return sse



def output_to_file(clusters, error, outfile):
	file = open(outfile, "w")
	clusterId = 1
	for cluster in clusters:
		file.write(str(clusterId) + ':\t' + str([tweet.get_id() for tweet in clusters[cluster]]) + '\n')
		clusterId += 1
	file.write('\n\nSSE: ' + str(error))


# read command line arguments
# default values
if len(sys.argv) == 1:
	numClusters = 25
	initialSeedsFile = 'InitialSeeds.txt'
	tweetsDataFile = 'Tweets.json'
	outputfile = 'output.txt'

else:	
	numClusters = sys.argv[1]
	initialSeedsFile = sys.argv[2]
	tweetsDataFile = sys.argv[3]
	outputfile = sys.argv[4]

tweets = json_tweet_reader(tweetsDataFile)
seed_ids = txt_seed_reader(initialSeedsFile)
seed_tweets = get_seed_tweets(seed_ids, tweets)

#initialize dictionary with the keys as the seeds (centers)
clusters = {}
for seed_tweet in seed_tweets:
	clusters[seed_tweet] = []
final_clusters = get_clusters(tweets, seed_tweets, clusters)
sse = compute_sse(final_clusters)

print ('************************\nFINAL CLUSTER')
print_clusters(final_clusters)

try:
	output_to_file(final_clusters, sse, outputfile)
	print("Successfully printed to file")
except:
	print("Unable to print to file")