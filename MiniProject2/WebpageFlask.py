from flask import Flask, request, render_template, redirect
from HW1API import get_tweets2vid
from HW1API import googlelabels
import json
import os

#this function converts the dict returned by the google api into a list of lists full on descriptions of the images
def label_getter(input_dict):
    label_length = len(input_dict)
    label_list = []  # an empty list to hold lists of labels for each image
    for i in range(1, label_length + 1):
        image = "image" + str(i) + ".jpg"
        var = input_dict.get(image,"image missing")
        list_length = len(var)
        temp_list = [image]  # a temporary list that will hold all the labels and will be added to label_list
        for x in range(0, list_length):
            var2 = var[x]  # index into the list created from the first dict
            var3 = var2.get('description',"description missing")  # var2 is a dict so you need to get it again
            temp_list.append(var3)  # add it to the temporary list
        label_list.append(
            temp_list)  # add the completed temp list to the label list and repeat until there are no more images
    return str(label_list)

app = Flask(__name__)

@app.route('/', methods=["GET"])
def my_form():
        return render_template("layout.html")

@app.route('/', methods=['POST'])
def my_form_post():
        text = request.form['text']
        #removing images and .mp4 so we don't reuse images/vidoes
        for file in os.listdir():
            if file.endswith('.jpg'):
                os.remove(file)
            elif file.endswith('.mp4'):
                os.remove(file)
        #calling the API
        get_tweets2vid(screen_name=text, number_tweets=10, rate=2)
        googlelabels(description_count=2)
        #turning the json from googlelabels into a string of the images and their respective descriptions
        with open('labels.json') as handle:
            dictdump = json.loads(handle.read())
        output = str(label_getter(dictdump))
        #moving the ffmpeg video output.mp4 into the static folder
        #dir_path = os.path.dirname(os.path.realpath(__file__))
        #start_path = dir_path + "/output.mp4"
        #destination_path = dir_path + "/static"
        #os.rename(start_path,destination_path)
        return output #, redirect(destination_path)

if __name__ == "__main__":
    app.run(debug=True)

