import tornado.ioloop
import tornado.web
from os import path
from random import randint
from pymongo import MongoClient

class MainHandler(tornado.web.RequestHandler):

    def tweet(self):
        client = MongoClient()
        db = client.antibullybot
        raw_tweet_count = db.raw_tweets.count()
        idx = randint(0,raw_tweet_count)        
        rec = db.raw_tweets.find().limit(-1).skip(idx).next()
        return rec

    def get(self):
        rec = self.tweet()
        self.render("index.html",**rec)

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
],**settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

