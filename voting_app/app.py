import tornado.ioloop
import tornado.web
from os import path
from random import randint
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(host = "aaditpatel.com")
db = client["antibullybot"]
db.authenticate("antibullybot", "antibully")


def tweet():
    raw_tweet_count = db.tweets.count()
    idx = randint(0,raw_tweet_count-1)        
    rec = db.tweets.find().limit(-1).skip(idx).next()
    return rec


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        rec = tweet()
        self.render("index.html",**rec)


class VoteHandler(tornado.web.RequestHandler):

    def post(self):
        mongo_id = ObjectId(self.get_argument("id"))

        label = self.get_argument("bully")


        if label =='0' or label == '1':
            post = {"bullying_label": label}
            db.tweets.update({'_id':mongo_id}, {"$set": post}, upsert=False)
            foo = db.tweets.find_one({'_id':mongo_id})
            print foo["bullying_label"], foo["text"]
        
        self.redirect('/', permanent=False)

    def get(self):
        self.redirect('/',permanent=False)



root = path.abspath('.')
settings = {
        "static_path": path.join(root, "static"),
        "template_path": path.join(root, "template"),
        "globals": {
            "project_name": "AntiBullyBot"
        },
        "flash_policy_port": 843,
        "flash_policy_file": path.join(root, 'flashpolicy.xml'),
        
    }

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/vote", VoteHandler)
],**settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

