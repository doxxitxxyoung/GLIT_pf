from elasticsearch import Elasticsearch
import pickle

HOST = 'localhost'
PORT = 9200
es = Elasticsearch([{'host':HOST, 'port': PORT}])

path = '../GLIT_pf/data/sample_labeled_list_woAmbi_92742_70138_191119.pkl'
with open(path, 'rb') as f:
    samples = pickle.load(f)

#   Insertion
for i, x in enumerate(samples):
    ecfp = x[0]
    gex = x[1]
    dosage = x[2]
    duration = x[3]
    label = x[4]
    drugname = x[5]
    cellline = x[6]
    smiles = x[7]
    doc = {
        'drugname': drugname,
        'cellline': cellline,
        'smiles': smiles,
        'dosage': float(dosage),
        'duration': int(duration),
        'ecfp': [int(x) for x in ecfp],
        'gex': [float(x) for x in gex],
        'label': label
    }
    res = es.index(
        index = '_'.join([drugname.lower(), cellline.lower(), str(dosage), str(duration)]), 
        doc_type = 'sample',
        id = i,
        body = doc
    )
    if res['created'] != True:
        print(i, ' not created')

#   Retrieval

res = es.get(
        index = '_'.join([drugname.lower(), cellline.lower(), str(dosage), str(duration)]), 
        doc_type = 'sample',
        id = i
)
print(res['_source'])

