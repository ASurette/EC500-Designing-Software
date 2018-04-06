To use the system you need to have pymongo installed. Both of the files must be in the same directory.
Call the function DatabaseUpdate() and it will ask you for a twitter handle. It will get all the images and save their links into the database.
It will also save the tags into the database. The tags are saved in the format imageX: [tags go here]
Call CalculateTags() and it will run through the entire database, gather all the tags and then save them in a dict with the format
{tag: number of times the tag appears in the database}

If you call the database on a twitter handle already in the database it will look for new pictures and add them to that twitter handle's document.
If there are no new pictures it doesn't add anything.

Note: you need to use this version of TwitterPythonUpdate() because the old version does not work with MongoPythonDB