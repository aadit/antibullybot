from pymongo import MongoClient
import argparse
import xml.etree.ElementTree as ET


#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-r","--remote", help = "Remote host where the database is saved")
parser.add_argument("-c", "--collection", help= "The raw tweets collection name you'd like stats for")
args = parser.parse_args()

c = MongoClient(args.remote or 'localhost')
db = c.antibullybot
db.authenticate('antibullybot','antibully')

if args.collection is None or args.collection == "":
	exit("Need collection name -c collection name")

labeled_data_mongo = db[args.collection]



tree = ET.parse('../labeled_data/formspring_labeled.xml')


root = tree.getroot()

#Weird looping based on structure of data. Each comment is labeled manually by 3 people
#If two out of the three labels are "Yes", then we say that text is cyberbully.
#Kind of messy...

cyberbully_text = []
for user in root:
	for child in user:
		if child.tag == "POST":
			post = child
			bully_counts = 0
			text = ""
			for thing in post:
				if thing.tag == "TEXT":
					text = thing.text

				if thing.tag == "LABELDATA":
					if thing[0].text == "Yes":
						bully_counts += 1

			if bully_counts > 2:
				text = text.replace("A:","")
				text = text.replace("Q:","")
				upload_document = {"text": text}
				cyberbully_text.append(upload_document)


labeled_data_mongo.insert(cyberbully_text)


