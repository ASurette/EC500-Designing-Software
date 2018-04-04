from pymongo import MongoClient
client = MongoClient();
db = client.twitter_mongo_database;
td = db.twitter_data;

def DatabaseUpdate():
    # ask the user for a twitter handle to search for and make it lowercase
    twitter_handle = input("What is the Twitter Handle you want to search for? ").lower();

    from TwitterDownload import TwitterDownload
    outputList = TwitterDownload(twitter_handle);  # the list output of the twitter program

    # the list of the google vision labels
    twitterList = outputList[0];
    # the list of links to the images
    picTweets = outputList[1];

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

#TotalTags gets all the tags from all images from all twitter handles and puts them in a large list
def TotalTags():

    tag_list = [];#this list will hold all the tags and counts how many times a word appears

    for doc in db.td.find({}):
        num_images = doc.get("Number of Images Saved");
        for x in range(0, num_images):
            name = "image" + str(x);
            temp = doc.get(name);
            tag_list = tag_list + temp;

    return tag_list;

#Calculate Tags goes through the tag_list and counts how many times each word or phrase appears and puts them
#in a dict with the format {word/phrase: number of times it appears}
def CalculateTags():
    tag_list = TotalTags();

    #a dict that will hold all the words and how many times they each appeared in all the images
    counted_dict = {};

    #for each word/phrase in the list count how many times it appears
    for word in tag_list:
        #go through the tag_list and find all copies of that word
        indicies = [index for index, value in enumerate(tag_list) if value == word];

        indicies.reverse();#reverse the index list because we need to delete some values later and you can go out of bounds

        #since it returns a list with the indicies of the times it appears then the lenght of that list
        #is the number of times it appears
        times_appeared = len(indicies);

        #add the word adn the number of times it appears into the list
        counted_dict[word] = times_appeared;

        if (len(indicies) != 0):
            for val in indicies:
                del tag_list[val];#delete the words from the list so we don't count the same word over and over again

    return counted_dict;

DatabaseUpdate(); #uncomment this if you want to add to the database
print(CalculateTags());

#db.td.delete_many({});#deletes all documents, used in testing

