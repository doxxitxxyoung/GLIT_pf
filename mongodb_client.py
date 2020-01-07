from pymongo import MongoClient
import numpy as np
import pickle
import pprint

HOST = 'localhost'
PORT = 27017

client = MongoClient(HOST, PORT)

db = client['glit-db']

posts = db.posts




with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
    samples = pickle.load(f)

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
    post = {"drugname" : drugname,
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
    post = {"drugname": drugname,
                {
    """

#    posts.insert_one(post)

    if i == 0:

        # test
#        retrieved = posts.findOne({"drugname": drugname})
        find_drugname = drugname
        find_cellline = cellline

#retrieved = posts.find_one({"drugname": drugname})
#pprint.pprint(retrieved['drugname'])
#pprint.pprint(retrieved['cellline'])

retrieved = []
#for i, x in enumerate(posts.find({"drugname": find_drugname})):
selected_doc =  posts.find({"drugname": find_drugname, "cellline": find_cellline})
print('Num of selected docs : ', selected_doc.count())

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

print(len(retrieved))

#   Get length of collections
print('length of docs : ', posts.count_documents({}))


#   Delete all docs
"""
x = posts.delete_many({})
print(x.deleted_count, " documents deleted")
"""



