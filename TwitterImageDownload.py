#Adam Surette
#Twitter API is python-twitter at https://github.com/bear/python-twitter

import twitter

#setting up the twitter API
api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

status = api.GetUserTimeline(screen_name='realDonaldTrump', count=20)#the twitter user and how many tweets to check

picTweets = [] #this is a list that will hold all the images

length = len(status)#how many tweets there are in status

for i in range(0, length):#for each of the tweets grabbed
    #a try except block because if you try to read the media of a tweet that doesn't have media you get an error
    try:
        if status[i].media[0].type == 'photo':   #is there an image attached to the tweet
            picTweets.append(status[i].media[0]) #add the media to the picsTweets list
    except: #if we would error, meaning the tweet doesn't have the correct media, do nothing
        pass

print(picTweets)#prints the list of tweets

print(picTweets[0])




