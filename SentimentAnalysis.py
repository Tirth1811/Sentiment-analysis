import sys
import csv
import tweepy
import matplotlib.pyplot as plt

from collections import Counter
from aylienapiclient import textapi

if sys.version_info[0] < 3:
input = raw_input
consumer_key = "fce1PJS1lyI8x1YRZDVaXjBDj"
consumer_secret = "2Yb3r5GLooNdC9gQX6hkTK1vZ9Yp9jiW3kySLQaeaJzTm5dgN3"
access_token = "806435921465905152-AzlOT50HLj3ZGQaLje4SLFxcObJmnEH"
access_token_secret = "mxq1RKuVXdinOZziQntdJxvAJpyX5MrwS77fEcYJsgt2h"

application_id = "13a33a30"
application_key = "b0921f8fcb29e21015ee36259ace1da4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
client = textapi.Client(application_id, application_key)
query = input("What subject do you want to analyze for this example? \n")
number = input("How many Tweets do you want to analyze? \n")

results = api.search(
   lang="en",
   q=query + " -rt",
   count=number,
   result_type="recent",
   geocode="22.20775,76.97021,200km",
   since_id='2014-06-01',
   until_id='2014-06-30'
)

print("--- Gathered Tweets \n")
file_name = 'bjp_march_14.csv'

with open(file_name, 'w', newline='') as csvfile:
   csv_writer = csv.DictWriter(
       f=csvfile,
       fieldnames=["created_at","user_name","Tweet","location", "Sentiment"]
   )
  csv_writer.writeheader()

  print("--- Opened a CSV file to store the results of your sentiment analysis... \n")


for c, result in enumerate(results, start=1):
       tweet = result.text
       tidy_tweet = tweet.strip().encode('ascii', 'ignore')

       if len(tweet) == 0:

           print('Empty Tweet')
           continue

       response = client.Sentiment({'text': tidy_tweet})
       csv_writer.writerow({
           'user_name':result.user.name.encode('utf-8'),
           'Tweet': response['text'],
           'location':result.user.location.encode('utf-8'),
           'Sentiment': response['polarity'],
           'created_at':result.created_at
           
       })

       print("Analyzed Tweet {}".format(c))


with open(file_name, 'r') as data:
   counter = Counter()
   for row in csv.DictReader(data):
       counter[row['Sentiment']] += 1

   positive = counter['positive']
   negative = counter['negative']
   neutral = counter['neutral']
