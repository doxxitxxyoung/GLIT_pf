# module to test model serving

# works on local server atm

import requests
#from starlette import requests
from starlette.testclient import TestClient
from pydantic import BaseModel
import sys
import pickle
import json

from typing import List

#API_URL = 'http://localhost:5000/glit_predict'
#API_URL = 'http://127.0.0.1:8000/glit_predict'
#API_URL = 'http://0.0.0.0:8044/glit_predict'
#API_URL = 'http://127.0.0.1:8044/glit_predict'
#API_URL = 'http://localhost:8000/glit_predict'
#API_URL = 'http://127.0.0.1:8000/glit_predict'
API_URL = 'http://localhost:8080/glit_predict'

#API_URL = 'http://34.97.50.3/glit_predict'

#API_URL = 'http://34.97.37.164'

"""
def predict_result(ecfp, gex, dosage, duration, drugname):

#    payload = {'ecfp':ecfp, 'gex': gex, 'dosage': dosage, 'duration': duration, 'drugname': drugname}
    payload = {'dosage': float(dosage)}
#    r = requests.get(API_URL, data=payload)   
    r = requests.post(API_URL, files=payload)   
#    r = requests.Request.form(API_URL, data=payload)   

    return r
"""
class InputData(BaseModel):
    ecfp: List[float]
    gex: List[float]
    dosage: float
    duration: int
    drugname: str


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

def predict_result(ecfp, gex, dosage, duration, drugname):

    json_dict = InputData(
            ecfp=ecfp.tolist(),
            gex = gex.tolist(),
            dosage = float(dosage),
            duration = int(duration),
            drugname = drugname
            )

#    payload = json.dumps(json_dict)
    payload = json_dict.dict()

    r = requests.post(API_URL, json=payload)   

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



