from pymongo import MongoClient
import json
# linking
port = input("enter the port number: ")
client = MongoClient('mongodb://localhost:' + port)
# create/open a db
db = client['291db']
# create/open a collection
clt = db['dblp']
# flush the collection
clt.delete_one({})
# insert the json data
filename = input('enter the file name: ')
with open (filename, 'r') as infile:
    while True:
        info = infile.readline()
        if info:
            # casting
            info = json.loads(info)
            clt.insert_one(info)
        else:
            break
# ending
client.close()
