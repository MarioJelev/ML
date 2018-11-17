Mario Jelev, mvj140030
Assignment 4, Part 2

README
This program was written with Python 3.6 in a Windows 10 environment. It does not use any external machine learning libraries or packages, so it should be runnable on any system without additional installations.

To execute this program, please type one of the following into the command line:
		python tweets-k-means.py <numberOfClusters> <initialSeedsFile> <TweetsDataFile> <outputFile>
		python tweets-k-means.py
Example invocation:
		python tweets-k-means.py 25 InitialSeeds.txt Tweets.json output.txt

When no arguments are provided, default values of 25, InitialSeeds.txt, Tweets.json, and output.txt are used for the respective parameters.

Note:
		After the program terminates, the centroids of the clusters (and all of the clusters' contents) are displayed in the terminal. In the file output, instead of displaying the centroids of the clusters, a cluster ID is shown, followed by  the contents of that cluster.




