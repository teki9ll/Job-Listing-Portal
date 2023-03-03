import pymongo as pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("YOUR MONGODB ATLAS CONNECTION STRING", server_api=ServerApi('1'))
db = client.test

c_candidate = db['candidate']
c_jobs = db['jobs']

document = {"username": "admin", "password": "password"}
c_jobs.insert_one(document)
