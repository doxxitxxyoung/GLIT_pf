# module to test model serving

# works on local server atm
import numpy as np
import requests
import sys
import pickle
import json

import argparse
import time


parser = argparse.ArgumentParser()

parser.add_argument('--method', type = str, default = 'gke')
parser.add_argument('--type', type = str, default = 'get')

args = parser.parse_args()

if args.method == 'local':
    API_URL = 'http://localhost:8080/glit_predict'
elif args.method == 'gae':
    API_URL = 'https://glit-server-fast.appspot.com/glit_predict' # for Google App Engine
else:
    API_URL = 'http://34.97.190.179/glit_predict' # for Google Kubernetes Engine

# GET method
if args.type == 'get':
    """
    def predict_result(ecfp, gex, dosage, duration, drugname):
        # print(x)
        payload = {'ecfp':ecfp, 'gex': gex, 'dosage': dosage, 'duration': duration, 'drugname': drugname}
        r = requests.get(API_URL, data=payload)   
     
        return r
    """
    def predict_result(api_url, drugname, cellline):
        params = {'drugname' : drugname, 'cellline' : cellline}
        r = requests.get(api_url, params = params)
#        r = requests.get(API_URL, params = params)

#        api_url = api_url+'?drugname='+drugname+'&cellline='+cellline
#        r = requests.get(api_url)

        return r


# POST method
else:
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

sample = sample[0]

# GET method
if args.type == 'get':
    drugname = sample[5]
    cellline = sample[6]
    print(type(cellline))

    t = time.time()
    result = predict_result(API_URL, drugname, cellline)
    print(result.json())
    dt = time.time() - t
    print("Execution time : %0.02f seconds"%(dt))

# POST method
elif args.type == 'post':
    ecfp = sample[0].tolist()
    ecfp = [int(x) for x in ecfp]
    #ecfp = [int(x) for x in ecfp]
    gex = sample[1].tolist()
    gex = [float(x) for x in gex]
    dosage = int(sample[2])
    duration = float(sample[3])
    drugname = sample[5]

    t = time.time()
    result = predict_result(ecfp, gex, dosage, duration, drugname)
    print(result.json())
    dt = time.time() - t
    print("Execution time : %0.02f seconds"%(dt))



