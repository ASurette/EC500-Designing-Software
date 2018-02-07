# EC500-Designing-Software
My repo for EC500C1

The function takes a Twitter handle as an input and searches the last 100 tweets from that handle for images.
It downloads those images and runs them through Google Vision and gets the labels for each image. These labels
are saved in a list and this list is the final output. It also uses ffmpeg to generate a video of the images and displays
each for 2 seconds. It finds the file path of this video and adds it to the end of the output list. This means that
the number of images is the length of the list-1 and the last value in the list is the file path

(there is a bug where the first image in the video is on screen 3x longer than it should be)

The errors follow the syntax Error XXX: error message

So far it checks if the Twitter handle is viable, if there are any images within the tweets searched
and if ffmpeg created the video

The libraries used for the project are

python-twitter: to get the twitter API into python
https://github.com/bear/python-twitter

urllib.request: to download the images from twitter once I have their URLs
https://docs.python.org/3.0/library/urllib.request.html

subprocess: allows you to run command lines in your script, used to run ffmpeg

os: allows you to modify files on your computer, used to set the path to the Google API JSON key and to save, delete and open the images

io: used to open the images

FFMPEG

This is the guide I used on how to install it
https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg

FFMPEG is used to make the video of all the images

note: there is an issue with the video that the first image appears on screen 3x longer than it should, you can ignore it

Google Vision
This is the tutorial I followed on how to use it
https://www.youtube.com/watch?v=nMY0qDg16y4
On this youtube page there is a comment by Doug Beney with the updated code for Python 3

google.cloud: the library I used to access the Google Vision API
