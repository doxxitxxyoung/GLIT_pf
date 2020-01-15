from pymongo import MongoClient
import numpy as np
import pickle
import pprint
import argparse

from pymongo_schema.compare import compare_schemas_bases
from pymongo_schema.export import transform_data_to_file
from pymongo_schema.extract import extract_pymongo_client_schema
from pymongo_schema.filter import filter_mongo_schema_namespaces


parser = argparse.ArgumentParser()

parser.add_argument('--insert', type = bool, default = False)

args = parser.parse_args()


#HOST = 'localhost'
#PORT = 27017

#   Connection example
"""
mongodb_uri = "mongodb://<my_login>:<my_password>@<mongodb_path>:27017" # format
client = MongoClient(mongodb_uri)
db = client.ctox
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)
"""




# Atlas use
mongodb_uri = "mongodb+srv://doxxitxxyoung:Tele63741@cluster0-9usdz.gcp.mongodb.net/test?retryWrites=true&w=majority"
#mongodb_uri = "mongodb+srv://doxxitxxyoung:Tele63741@cluster0-9usdz.gcp.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
client = MongoClient(mongodb_uri)
#db = client.test    #   <class 'pymongo.database.Database'>
#db = client.sample_airbnb    #   <class 'pymongo.database.Database'>
db = client.glit_db    #   <class 'pymongo.database.Database'>
print(db.list_collection_names())
print('test to mongodb Successed!')

#client = MongoClient(HOST, PORT) # local use

#db = client['glit-db']

#posts = db.posts    #   <class 'pymongo.collection.Collection'>

#   Clear collection at the moment
#db.drop_collection("glit_collection")

collection = db.glit_collection    #   <class 'pymongo.collection.Collection'>
print(collection.count())
print('connection to mongodb Successed!')
#serverStatusResult = db.command("serverStatus")
#pprint(serverStatusResult)



#with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
with open('data/labeled_list_woAmbi_92742_70138.pkl', 'rb') as f:
    samples = pickle.load(f)

#   Only use 10000 samples, ATM
samples = samples[0]


find_drugname = samples[5]
find_cellline = samples[6]

selected_doc =  collection.find({"drugname": find_drugname, "cellline": find_cellline})
print('Num of selected docs : ', selected_doc.count())
selected_doc = [x for x in selected_doc][0]


print(selected_doc['drugname'])
print(selected_doc['cellline'])
print(selected_doc['dosage'])
print(selected_doc['duration'])


#   Get length of collections
print('length of docs : ', collection.count_documents({}))


#   Use pymongo-schema for schema extraction
schema = extract_pymongo_client_schema(client)
print(schema)

