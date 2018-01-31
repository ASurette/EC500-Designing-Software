#Adam Surette
#Twitter API is python-twitter at https://github.com/bear/python-twitter

import twitter        #the twitter api
import urllib.request #used to actually download the images and save them
import subprocess     #runs command lines in program, used to run ffmpeg
import os             #this library if for operating os things such as removing files

#setting up the twitter API
api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

#this deletes all the .jpg in the current folder in case you run the program multiple times in a row
#for each file in the current directory (where the downloaded images will be) if it is a .jpg delete it
for file in os.listdir():
    if file.endswith('.jpg'):
        os.remove(file)

#if you ran the program before delete the old video
if os.path.isfile('output.mp4'):
    os.remove('output.mp4')

status = api.GetUserTimeline(screen_name='realDonaldTrump', count=100)#the twitter user and how many tweets to check

picTweets = [] #this is a list that will hold all the image urls for download later

length = len(status)#how many tweets there are in status

for i in range(0, length):#for each of the tweets grabbed
    #a try except block because if you try to read the media of a tweet that doesn't have media you get an error
    try:
        if status[i].media[0].type == 'photo':   #is there an image attached to the tweet
            picTweets.append(status[i].media[0].media_url) #add the media url to the picsTweets list
    except: #if we would error, meaning the tweet doesn't have the correct media, do nothing
        pass

#print(picTweets)#prints the list of tweets

picTweetsLength = len(picTweets) #gets the length of the pic tweets list for a for loop

#this for loop goes through the urls we found for the images and saves them to the local files as JPEGs
for x in range(0,picTweetsLength):
    string = 'twitterImage'
    stringNum = str(x)
    #the following if statements find the digits in the current photo so that it can add a correct number of
    #leading 0s to the name of the file, for example the stringNum is 1 so we need it to be 001, 10 we need 010 etc.
    if len(stringNum) == 1:
        string += '00'
        string += stringNum
    elif len(stringNum) == 2:
        string += '0'
        string += stringNum
    elif len(stringNum) == 3: #example 100 so no leading zeroes
        string += stringNum
    string += '.jpg'
    urllib.request.urlretrieve(picTweets[x], string) #downloads the image and saves it as twitterImageXXX.jpg

subprocess.run('ffmpeg -framerate 1/2 -i twitterImage%03d.jpg output.mp4')
