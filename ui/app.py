import tornado.ioloop
import tornado.web
from os import path
from random import randint
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.antibullybot

def tweet():
    raw_tweet_count = db.raw_tweets.count()
    idx = randint(0,raw_tweet_count-1)        
    rec = db.raw_tweets.find().limit(-1).skip(idx).next()
    return rec


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        rec = tweet()
        self.render("index.html",**rec)


class VoteHandler(tornado.web.RequestHandler):

    def post(self):
        mongo_id = ObjectId(self.get_argument("id"))
        post = {"bully":self.get_argument("bully")}
        db.raw_tweets.update({'_id':mongo_id}, {"$set": post}, upsert=False)
        
        #Check its updated
        foo = db.raw_tweets.find_one({'_id':mongo_id})
        print foo["bully"], foo["text"]
        
        self.redirect('/', permanent=False)



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

