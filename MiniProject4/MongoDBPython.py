from pymongo import MongoClient
client = MongoClient();
db = client.twitter_mongo_database;
td = db.twitter_data;

#ask the user for a twitter handle to search for and make it lowercase
twitter_handle = input("What is the Twitter Handle you want to search for? ").lower();

from TwitterDownload import TwitterDownload
outputList = TwitterDownload(twitter_handle);#the list output of the twitter program

#the list of the google vision labels
twitterList = outputList[0];
#the list of links to the images
picTweets = outputList[1];

def DatabaseUpdate():
    #a dict it will have all the data that will go in the database saved into it, starts with the user's input as the twitter handle name
    data = {"Twitter Handle": twitter_handle,
            "Image Links": picTweets,
            "Number of Images Saved": 0};

    #Check if we got an error or not
    if(twitterList[0:4:1] == 'Error'):
            print(twitterList);

    else:

        document = db.td.find_one({"Twitter Handle": twitter_handle});

        if( document != None ): #if the twitter handle has been called before and is in the database
            #reference the list of image links and compare the new list to the old list

            potential_new_links_list = [];#an array to save links for new images that are checked against old ones

            saved_images_list = db.td.find_one({"Twitter Handle": twitter_handle}).get("Image Links");

            #go through all the new image links, compare them against the old links, if it is not already in the old links put it in the array
            #this array will then be added to the database

            index_list = [];#an empty list that will be used to store the index of new images

            index_count = 0;# a count so that if there are new picture we can save the index in the list for them, use this to index the tags in the other list
            for val in picTweets:

                count = 0;

                for link in saved_images_list:

                    if(val != link):

                        count = count + 1;

                #end for link in saved_images_list
                if(count == len(saved_images_list)):#if there were no matches
                    potential_new_links_list.append(val);
                    index_list.append(index_count);

                index_count = index_count + 1;
            #end for val in pic tweets

            if(len(potential_new_links_list) == 0):#if no new values
                #do nothing
                print("Now new images found");
                return "No new images found";
            else:#at least one new value
                #add the new images to the end of the saved images list
                links_list = saved_images_list+potential_new_links_list;

                db.td.update_one({"Twitter Handle": twitter_handle}, {'$set': {"Image Links": links_list}});#updates the image links list with the new images

                if(len(index_list) != 0):

                    num_images = db.td.find_one({"Twitter Handle": twitter_handle}).get("Number of Images Saved");

                    for x in range (0, len(index_list)):
                        name = "image" + str(x + num_images);
                        tags = twitterList[index_list[x]];
                        #adds the new imageX and its tags to the document
                        db.td.update_one({"Twitter Handle": twitter_handle}, {'$set': {name: tags}});

                    #end for loop

                    #need to update the number of images as well
                    db.td.update_one({"Twitter Handle": twitter_handle}, {'$set': {"Number of Images Saved": len(links_list)}});

        else:   #brand new value for the database
            list_length = len(twitterList) - 1;#the length of the output -1 because the last element in the list is the filepath to the video
            data["Number of Images Saved"] = list_length;

            for i in range (0, list_length):
                temp_dict = {};#make an empty dict that we will fill with data and merge with data
                temp_name = "image" + str(i);#the first part of the dict which depends on the image number
                temp_name2 = twitterList[i];#index into the output of TwitterDownload which is a list of lists with the google vision data
                temp_dict = {temp_name: temp_name2};#add the image name and the description for them into the temp dict
                data.update(temp_dict);#adds the temp dict to the dict that will be added to the database
                #end of the for loop

        db.td.insert_one(data);

DatabaseUpdate();

#db.td.delete_many({});#deletes all documents, used in testing
