#code written by Adam Surette for EC500C1

def TwitterDownload(twitterHandler):

    import twitter          #the twitter api
    import urllib.request   #used to actually download the images and save them
    import subprocess       #runs command lines in program, used to run ffmpeg
    import os               #this library if for operating os things such as removing files and adding the google app credentials
    import io               #used for reading the images we saved so we can send them to google vision
    from google.cloud import vision
    from google.cloud.vision import types

    #setting up the Google API/Vision API
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "PATH/TO/GOOGLE/JSON/AUTH" #sets up the GOOGLE_APPLICATION_CREDENTIALS as an enviornment variable

    vision_client = vision.ImageAnnotatorClient() #setting up the image annotator client for Google Vision

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

    # -----------------Twitter Section----------------------------------------------
    # This section uses the twitter api to download pictures from the Twitter handle the user inputs
    # It checks the number of tweets the user inputs

    try:
        status = api.GetUserTimeline(screen_name=twitterHandler, count=100)#the twitter user and how many tweets to check
    except:
        return 'Error 001: This Twitter handle is not valid'

    picTweets = [] #this is a list that will hold all the image urls for download later

    length = len(status)#how many tweets there are in status

    for i in range(0, length):#for each of the tweets grabbed
        #a try except block because if you try to read the media of a tweet that doesn't have media you get an error
        try:
            if status[i].media[0].type == 'photo':   #is there an image attached to the tweet
                picTweets.append(status[i].media[0].media_url) #add the media url to the picsTweets list
        except: #if we would error, meaning the tweet doesn't have the correct media, do nothing
            pass

    picTweetsLength = len(picTweets) #gets the length of the pic tweets list for a for loop
    imgList = [] #a list of the name of all the images that will be saved

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
        imgList.append(string) #adding the name of the file to the list of images

        # Checking if any images were found within the 100 tweets scanned, if there are none then there is an error
        # returned as the output
    if len(imgList) == 0:
        return 'Error 002: There are no images found'

    #--------------------------Google Vision-----------------------------------------------------
    #I used this tutorial below to figure out how it works
    #https://www.youtube.com/watch?v=nMY0qDg16y4
    #Thanks to Doug Beney in the comments for showing the updated code for python 3

    imageLabels = [] #a list that will hold the labels of each image, will be the final output

    #for all the images we downloaded open the image, run it through google vision and
    for i in range (0,len(imgList)):                    #for all the images we downloaded
        with io.open(imgList[i], 'rb') as image_file:   #open
            content = image_file.read()

        image = types.Image(content=content)
        response = vision_client.label_detection(image=image)
        labels = response.label_annotations

        tempList = [] #temporary list to save all the labels in one list then save that list in the imageLabels list
        for label in labels:
            tempList.append(label.description)

        imageLabels.append(tempList) #add the list to imageLabels

    # ---------------------------FFMPEG--------------------------------------
    #this part creates the movies out of the images downloaded
    #change the number after framerate to change how long each image is on screen
    #1/2 means each image is on screen for 2 seconds, 1/5 5 seconds etc

    #note that there is a bug that the first image stays on screen 3x longer than it should
    #prof said to ignore it
    subprocess.run('ffmpeg -framerate 1/2 -i twitterImage%03d.jpg output.mp4')

    #getting the file path of the video, adds it to the end of the labels for the images
    if os.path.isfile('output.mp4'):
        videoPath = os.getcwd()
        videoPath += '/output.mp4'
        imageLabels.append(videoPath)
    else:
        return 'Error 003: ffmpeg could not create the video properly'

    return imageLabels #return the labels of all the functions as the final output
    #end of function

#calling the function
output = TwitterDownload(twitterHandler='')
print(output)

