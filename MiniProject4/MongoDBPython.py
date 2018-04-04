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

        document = td.find_one({"Twitter Handle": twitter_handle});

        if( document != None ): #if the twitter handle has been called before and is in the database
            #reference the list of image links and compare the new list to the old list

            potential_new_links_list = [];#an array to save links for new images that are checked against old ones

            saved_images_list = td.find_one({"Twitter Handle": twitter_handle}).get("Image Links");

            #go through all the new image links, compare them against the old links, if it is not already in the old links put it in the array
            #this array will then be added to the database
            for val in picTweets:

                count = 0;

                for link in saved_images_list:

                    if(val != link):

                        count = count + 1;

                #end for link in x
                if(count == len(saved_images_list)):#if there were no matches
                    potential_new_links_list.append(val);

            #end for val in pic tweets

            print(potential_new_links_list);

            if(len(potential_new_links_list) == 0):#if no new values
                #do nothing
                return "No new images found";
            else:#at least one new value
                #add the new images to the end of the saved images list
                links_list = saved_images_list+potential_new_links_list;

                print("Links list is: ", links_list);



        else:   #brand new value for the database
            list_length = len(twitterList) - 1;#the length of the output -1 because the last element in the list is the filepath to the video

            for i in range (0, list_length):
                temp_dict = {};#make an empty dict that we will fill with data and merge with data
                temp_name = "image" + str(i);#the first part of the dict which depends on the image number
                temp_name2 = twitterList[i];#index into the output of TwitterDownload which is a list of lists with the google vision data
                temp_dict = {temp_name: temp_name2};#add the image name and the description for them into the temp dict
                data.update(temp_dict);#adds the temp dict to the dict
                #end of the for loop

        data["Number of Images Saved"] = list_length;
        print(data);
        td.insert_one(data);


DatabaseUpdate();