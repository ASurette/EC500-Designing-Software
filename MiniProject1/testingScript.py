# Python testing script for TwitterImageDownload.py

from TwitterImageDownload import TwitterDownload
print ("Running TwitterImageDownload with a nonexistent username: ")
print (TwitterDownload('18293NotaUsername48271'))
print ("\nRunning TwitterImageDownload with no pictures in it tweet: ")
print (TwitterDownload('abbottn3'))
print ("\nNo way to throw error 003\n")
print ("Running TwitterImageDownload on Twitter handle with many images (long wait time): ")
print (TwitterDownload('BarstoolSports'))