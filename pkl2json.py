import pickle
import json


with open('data/labeled_list_woAmbi_92742_70138.pkl', 'rb') as f:
    samples = pickle.load(f)

samples = samples[:1000]


data = {}
data['samples'] = []
data['drugs'] = []
data['celllines'] = []
drugs = []
cells = []

#   Samples
for i, x in enumerate(samples):
    ecfp = [int(y) for y in x[0]]
    gex = [float(y) for y in x[1]]
    dosage = float(x[2])
    duration = int(x[3])
    label = x[4]
    drugname = x[5]
    cellline = x[6]
    smiles = x[7]

    data['samples'].append({
        'drugname': drugname,
        'ecfp': ecfp, 
        'gex': gex,
        'label': label,
        'cellline': cellline,
        'smiles': smiles,
        'dosage': dosage,
        'duration': duration
    })

#   Drugs




with open('data/labeled_list_woAmbi_92742_70138.json', 'w', encoding = 'utf-8') as f:
    json.dump(data, f)
