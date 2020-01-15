from pymongo import MongoClient
import numpy as np
import pickle
import pprint
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--insert', type = bool, default = False)

args = parser.parse_args()


HOST = 'localhost'
PORT = 27017

#   Connection example
"""
mongodb_uri = "mongodb://<my_login>:<my_password>@<mongodb_path>:27017" # format
client = MongoClient(mongodb_uri)
db = client.ctox
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)
"""




# Atlas use
"""
mongodb_uri = "mongodb+srv://doxxitxxyoung:Tele63741@cluster0-9usdz.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(mongodb_uri)
"""

# Local use
client = MongoClient(HOST, PORT) # local use

db = client.glit_db    #   <class 'pymongo.database.Database'>
print(db.list_collection_names())
print('test to mongodb Successed!')


#db = client['glit-db']

#posts = db.posts    #   <class 'pymongo.collection.Collection'>

#   Clear collection at the moment
db.drop_collection("glit_collection")

collection = db.glit_collection    #   <class 'pymongo.collection.Collection'>
print(collection.count())
print('connection to mongodb Successed!')
#serverStatusResult = db.command("serverStatus")
#pprint(serverStatusResult)



#with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
with open('data/labeled_list_woAmbi_92742_70138.pkl', 'rb') as f:
    samples = pickle.load(f)

#   Only use 10000 samples, ATM
samples = samples[:10000]

for i, x in enumerate(samples):
    ecfp = x[0]
    gex = x[1]
    dosage = x[2]
    duration = x[3]
    label = x[4]
    drugname = x[5]
    cellline = x[6]
    smiles = x[7]

    #   Non-nested structure
    doc = {"drugname" : drugname,
            "ecfp": [int(x) for x in ecfp],
            "gex": [float(x) for x in gex],
            "dosage": float(dosage),
            "duration": int(duration),
            "label": label,
            "cellline": cellline,
            "smiles": smiles
            }

    #   Nested structure
    """
    doc = {"drugname" : drugname,
            "label" : label,
            "smiles": smiles,
            "ecfp": [int(x) for x in ecfp],
            "sample" : {
                    "cellline": cellline,
                    "gex": [float(x) for x in gex],
                    "dosage": float(dosage),
                    "duration": int(duration)
                        }
        }
    """

    #   Nested structure 2
    """
    doc = {"drugname" : drugname,
            "label" : label,
            "smiles": smiles,
            "ecfp": [int(x) for x in ecfp],
            "cellline" : {
                    "cellline_name": cellline,
                    "sample": {
                            "gex": gex,
                            "dosage": dosage,
                            "duration": duration
                            }
                        }
        }
    """


    #   Insert docs into DB collection
    collection.insert_one(doc)

    if i == 0:

        # test
#        retrieved = posts.findOne({"drugname": drugname})
        find_drugname = drugname
        find_cellline = cellline

print('Insertion Docs to MongoDB Successed!')

#retrieved = posts.find_one({"drugname": drugname})
#pprint.pprint(retrieved['drugname'])
#pprint.pprint(retrieved['cellline'])

#for i, x in enumerate(posts.find({"drugname": find_drugname})):
selected_doc =  collection.find({"drugname": find_drugname, "cellline": find_cellline})
print('Num of selected docs : ', selected_doc.count())
selected_doc = [x for x in selected_doc][0]


print(selected_doc['drugname'])
print(selected_doc['cellline'])
print(selected_doc['dosage'])
print(selected_doc['duration'])
"""
if selected_doc.count() == 1:
#    selected_doc = selected_doc.__getitem__(0)
    print(selected_doc['drugname'])
    print(selected_doc['cellline'])
    print(selected_doc['dosage'])
    print(selected_doc['duration'])

else:
    for i, x in enumerate(posts.find({"drugname": find_drugname}, {'cellline': find_cellline})):
        retrieved.append(x)
        print(x['drugname'])
        print(x['cellline'])
        print(x['dosage'])
        print(x['duration'])
"""


#   Get length of collections
print('length of docs : ', collection.count_documents({}))


#   Delete all docs
"""
x = posts.delete_many({})
print(x.deleted_count, " documents deleted")
"""



