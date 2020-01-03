# module to test model serving

# works on local server atm
import numpy as np
import requests
import sys
import pickle
import json

API_URL = 'http://localhost:8080/glit_predict'
#API_URL = 'https://glit-server-fast.appspot.com/glit_predict'
#API_URL = 'http://34.97.37.164'

# GET method
"""
def predict_result(ecfp, gex, dosage, duration, drugname):
    # print(x)
    payload = {'ecfp':ecfp, 'gex': gex, 'dosage': dosage, 'duration': duration, 'drugname': drugname}
    r = requests.get(API_URL, data=payload)   

    return r
"""
# POST method
def predict_result(ecfp, gex, dosage, duration, drugname):
    # print(x)
    payload = {'ecfp':ecfp, 'gex': gex, 'dosage': dosage, 'duration': duration, 'drugname': drugname}
    payload = json.dumps(payload)
    r = requests.post(API_URL, json=payload)

    return r

with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
    sample = pickle.load(f)

#sample = sample[0]
"""
# GET method
ecfp = sample[0]
gex = sample[1]
dosage = sample[2]
duration = sample[3]
drugname = sample[5]
"""

# POST method
sample = sample[0]
ecfp = sample[0].tolist()
ecfp = [int(x) for x in ecfp]
#ecfp = [int(x) for x in ecfp]
gex = sample[1].tolist()
gex = [float(x) for x in gex]
dosage = int(sample[2])
duration = float(sample[3])
drugname = sample[5]


result = predict_result(ecfp, gex, dosage, duration, drugname)
print(result.json())



