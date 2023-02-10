#This file deals with the scraping and filtering of Twitter data, but after inspection of the returned data,
#I decided against it's inclusion in the automated email due to the inconsistent and irrelevant results.   

import snscrape.modules.twitter as sntwitter
import pandas as pd
import json
from datetime import date, timedelta



Tweets_Information = []
Tweet_List = []



# Using TwitterSearchScraper to scrape data and append tweets to list
TimeDeltaDays = timedelta(days = 5)
previousDay = date.today() - TimeDeltaDays
print(previousDay)
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'#innovation since:{previousDay} until:{date.today()} ').get_items()):   #since:2021-01-01 until:2021-05-31
    if i>1000:
        break
    # Tweets_Information.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username])
    if (tweet.likeCount > 10 or tweet.retweetCount > 10) and tweet.lang == 'en': 
        Tweets_Information.append({
            # 'RawTweet': tweet.rawContent, 
            'RenderedTweet': tweet.renderedContent, 
            'TweetLikes': tweet.likeCount, 
            'TweetRetweets': tweet.retweetCount,
            'TweetURl': tweet.url,
            'Language': tweet.lang,
            'Date': tweet.date.strftime('%F')
            })
        Tweet_List.append(tweet.renderedContent)
# Creating a dataframe from the tweets list above
# tweets_df2 = pd.DataFrame(Tweets_Information, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# print(tweets_list1)
print(json.dumps(Tweets_Information))
print(Tweet_List)





