from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://root:root@db:27017/")
mydata = client['chatapp']
mycol = mydata['session_details']


def show_data():
    AllData = []
    data = mycol.find({},{})
    for i in data:
        i['_id'] = str(ObjectId(i['_id']))
        AllData.append(i)
    return AllData

