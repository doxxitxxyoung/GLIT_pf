# module to test model serving

# works on local server atm

import requests
import sys
import pickle

API_URL = 'http://localhost:5000/glit_predict'

def predict_result(ecfp, gex, dosage, duration, drugname):
    # print(x)
    payload = {'ecfp':ecfp, 'gex': gex, 'dosage': dosage, 'duration': duration, 'drugname': drugname}
    # r = requests.post(API_URL, files=payload)
    r = requests.get(API_URL, data=payload)   

    return r

with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
    sample = pickle.load(f)

sample = sample[0]
ecfp = sample[0]
gex = sample[1]
dosage = sample[2]
duration = sample[3]
drugname = sample[5]


result = predict_result(ecfp, gex, dosage, duration, drugname)
print(result.json())



