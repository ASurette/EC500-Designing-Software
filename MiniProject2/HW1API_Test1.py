from HW1API import get_tweets2vid
from HW1API import googlelabels
import os
import time
import json

#deletes the .jpg so that the code works properly
for file in os.listdir():
    if file.endswith('.jpg'):
        os.remove(file)

#Create starting variables to find size before and after
start_size = sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
start_time = time.time()

#Test 1
#This is the test for when everything is correct

#get_tweets2vid(screen_name='@Osama_amasO', number_tweets=15, rate=2)
#output = googlelabels(description_count=2)
#with open('labels.json') as handle:
 #   dictdump = json.loads(handle.read())

#Test 2
#This is the test for when the screen name is not a valid user
#It should error but instead of the error message we get the
#error message from tweepy because the error check makes an error
#but it is not in a try except block

#get_tweets2vid(screen_name='@arlgiasliodfhaslkdfhalsku', number_tweets=2, rate=2)
#output = googlelabels(description_count=2)
#with open('labels.json') as handle:
 #   dictdump = json.loads(handle.read())

#Test 3
#This test is testing for having way too many number_tweets (which is actually number of images to find)
#you should get the API creator's error mesaage "Count is invalid: use a count between 1 and 100"

#get_tweets2vid(screen_name='@Osama_amasO', number_tweets=999999, rate=2)
#output = googlelabels(description_count=2)
#with open('labels.json') as handle:
 #   dictdump = json.loads(handle.read())

#Test 4
#This case has what I believe to be an infinite loop
#I am not 100% sure why but I am assuming it is caused
#by how the API tries to find the correct number of images.

#get_tweets2vid(screen_name='@Osama_amasO', number_tweets=1, rate=2)
#output = googlelabels(description_count=2)
#with open('labels.json') as handle:
#    dictdump = json.loads(handle.read())

#Printing how long the process took
end_time = time.time()
print("The time it took to run is", end_time-start_time, "seconds")

#Printing how large the files downloaded
end_size = sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
print(end_size-start_size, "bytes")

#prints the labels
print(dictdump)