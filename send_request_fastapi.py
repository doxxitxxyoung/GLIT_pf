# module to test model serving

# works on local server atm

import requests
from requests.exceptions import ConnectionError
#from starlette import requests
from starlette.testclient import TestClient
from pydantic import BaseModel
import sys
import pickle
import json

from typing import List
import time

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, default = 'local')
parser.add_argument('--type', type=str, default = 'post')

args = parser.parse_args() 

if args.method == 'local':
    API_URL = 'http://localhost:8080/glit_predict'
else:
    API_URL = 'http://34.97.171.244/glit_predict'
    
#API_URL = 'http://localhost:8000/glit_predict'
#API_URL = 'http://localhost:80/glit_predict/'

#API_URL = 'http://34.97.50.3/glit_predict'

#API_URL = 'http://34.97.37.164'

class InputData(BaseModel):
    ecfp: List[float]
    gex: List[float]
    dosage: float
    duration: int
    drugname: str
    cellline: str

"""
python list to dict
M = dict(zip(range(1, len(ddd) + 1), ddd))
M = dict(list(enumerate(ddd, start=1)))
returns '{"1": "norm9_ab1", "2": "dataset-hdf", "3": "audio", ...
"""

def predict_result(ecfp, gex, dosage, duration, drugname, cellline):
    json_dict = InputData(
            ecfp=ecfp.tolist(),
            gex = gex.tolist(),
            dosage = float(dosage),
            duration = int(duration),
            drugname = drugname,
            cellline = cellline
            )
    """
    json_dict = {
        'ecfp': ecfp.tolist(),
        'gex': gex.tolist(),
        'dosage': float(dosage),
        'duration': int(duration),
        'drugname': drugname,
        'cellline': cellline
    }
    """

#    payload = json.dumps(json_dict)
    payload = json_dict.dict()
#    print(payload)

#    r = requests.post(API_URL, data=payload)    #   {'detail': 'There was an error parsing the body'}
    r = requests.post(API_URL, json=payload)   
#    r = retry_on_connectionerror(requests.post(API_URL, json=payload))

    return r

def retry_on_connectionerror(f, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            return f()
        except ConnectionError:
            retries += 1
    raise Exception("Maximum retries exceeded")


with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
    sample = pickle.load(f)

sample = sample[0]
ecfp = sample[0]
gex = sample[1]
dosage = sample[2]
duration = sample[3]
drugname = sample[5]
cellline = sample[6]
smiles = sample[7]

t = time.time()
result = predict_result(ecfp, gex, dosage, duration, drugname, cellline)
#result = retry_on_connectionerror(predict_result(ecfp, gex, dosage, duration, drugname, cellline))
print(result.json())
dt = time.time() - t
print("Execution time : %0.02f seconds"%(dt))


"""
def predict_result(ecfp, gex, dosage, duration, drugname):

#    payload = {'ecfp':ecfp, 'gex': gex, 'dosage': dosage, 'duration': duration, 'drugname': drugname}
    payload = {'dosage': float(dosage)}
#    r = requests.get(API_URL, data=payload)   
    r = requests.post(API_URL, files=payload)   
#    r = requests.Request.form(API_URL, data=payload)   

    return r
"""


"""
def predict_result(ecfp, gex, dosage, duration, drugname):
    json_dict = {}
    json_dict['ecfp'] = ecfp.tolist()
    json_dict['gex'] = gex.tolist()
    json_dict['dosage'] = float(dosage)
    json_dict['duration'] = int(duration)
    json_dict['drugname'] = drugname

#    payload = json.dumps(json_dict)
    payload = json_dict.json()

    r = requests.post(API_URL, json=payload)   

    return r
"""
