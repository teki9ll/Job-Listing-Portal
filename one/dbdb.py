from collections import defaultdict

import pymongo as pymongo
from pymongo.server_api import ServerApi
from django.contrib.auth.hashers import make_password

client = pymongo.MongoClient("mongodb+srv://teki:tekipass@cluster0.xkhiyoi.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.test

c_candidate = db['candidate']
c_jobs = db['jobs']

# update the "applied_candidates" array in a document with a specific heading

c_details = c_candidate.find_one({"username": "tanmay"}, {"applied_jobs": 1, "_id": 0})
all_jobs = c_jobs.find({}, {"heading": 1, "_id": 0})

all_jobs = list(all_jobs)
merged_dict = defaultdict(list)

merged_dict = defaultdict(list)
for d in all_jobs:
    for key, value in d.items():
        merged_dict[key].append(value)


print(c_details["applied_jobs"])
print(dict(merged_dict)["heading"])

not_common = list(set(c_details["applied_jobs"]).symmetric_difference(set(dict(merged_dict)["heading"])))

print("not_common -> ", not_common)