import pymongo
import TwitterDownload

from pymongo import MongoClient
client = MongoClient();
db = client.twitter_mongo_database;
td = db.twitter_data;

#data = {"code": x, y: z};
#td.insert_one(data);
#print(td.find_one({}));

#td.delete_many({"code": "XXX"});

from gridfs import GridFS

#ask the user for a twitter handle to search for and make it lowercase
twitter_handle = input("What is the Twitter Handle you want to search for? ").lower();

from TwitterDownload import TwitterDownload
twitterList = TwitterDownload(twitter_handle);#the list output of the twitter program

#a dict it will have all the data that will go in the database saved into it, starts with the user's input as the twitter handle name
data = {"Twitter Handle": twitter_handle};

#Check if we got an error or not
if(twitterList[0:4:1] == 'Error'):
        print(twitterList);
else:
    #check if that handle is in the database already, if so delete it so we can make a new one
    if( td.find_one({"Twitter Handle": twitter_handle}) != 'None'):
        td.delete_many({"Twitter Handle": twitter_handle})

    list_length = len(twitterList) - 1;#the length of the output -1 because the last element in the list is the filepath to the video

    for i in range (0, list_length):
        temp_dict = {};#make an empty dict that we will fill with data and merge with data
        temp_name = "image" + str(i);#the first part of the dict which depends on the image number
        temp_name2 = twitterList[i];#index into the output of TwitterDownload which is a list of lists with the google vision data
        temp_dict = {temp_name: temp_name2};#add the image name and the description for them into the temp dict

        #find out how to save images and put it here

        data.update(temp_dict);#adds the temp dict to the dict
        #end of the for loop

    td.insert_one(data);

print(td.find_one({"Twitter Handle": "wizards_magic"}));