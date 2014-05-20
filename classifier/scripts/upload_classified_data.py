from pymongo import MongoClient
import argparse
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-r","--remote", help = "Remote host where the database is saved")
parser.add_argument("-c", "--collection", help= "The name of the collection to save the labeled data")
args = parser.parse_args()

c = MongoClient(args.remote or 'localhost')
db = c.antibullybot
db.authenticate('antibullybot','antibully')

if args.collection is None or args.collection == "":
	exit("Need collection name -c collection name")

labeled_data_mongo = db[args.collection]
labeled_data_mongo.drop()


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

			
			text = text.replace("A:","")
			text = text.replace("Q:","")
			text = strip_tags(text)
			bully = False #ideally not bully tweet

			if bully_counts > 2:
				bully = True

			upload_document = {"text": text, "bully":bully}
			cyberbully_text.append(upload_document)


labeled_data_mongo.insert(cyberbully_text)


