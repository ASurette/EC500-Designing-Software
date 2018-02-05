# EC500-Designing-Software
My repo for EC500C1

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
