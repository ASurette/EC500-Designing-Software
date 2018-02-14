This project involves code reviewing a randomly assigned teammate who also completely MiniProject1. My assigned teammate's GitHub is at
https://github.com/Lilyxiuxiuxiu/EC500

HW1API is my modified version of their project (only small things like adding an easier way to autheticate Google vision and fixing a hardcoding issue that made the user's inputs meaningless)

HW1API_Test1 are my test cases for the code. It has 4 cases, just comment one and uncomment another. It times how long it takes to run and how many bytes it downloads. 

I have added multiple issues there and a code review. I will also add the that code review here.

The datapath:

First it checks if it has an @ at the beginning of the user name and if it doesn't then it errors (I think it should just add the @ so that the user doesn't need to rerun the program). Next it tries to get the timeline of the user to check if it is a valid handle (this needs to be in a try except block to work). Then it repeatedly gets the user's timeline until it has enough pictures. Once it does it downloads all the images from the URLs it found and saves them in the format imageX.jpg where x is the image number. Then it makes an ffmpeg command and runs it using subprocess. It returns the list of URLs. Then you can call the googlelabels function. It opens the files that it saved before and runs them through Google Vision. It creates a json file in the format of mid, description, score, topicality.

number_tweets is a misleading variable name. I assumed it would be the number of tweets the program looks through but it is actually the number of images that the program goes and finds. The easiest solution is just call it number_images.

The readability of the code is pretty good but there are a few confusing variables or sections that probably need comments to explain their purpose. For example the rate varaible. It is not explained what this variable does and it is only assigned in the argv block at the bottom of the script. This block seems to involve variable number of input arguments but there are no comments explaining what exactly it is doing. If a variable number of arguments is something you want the API to be capable of then you need to explain what each number of variables should be used for.
