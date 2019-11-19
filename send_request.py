import requests
import sys
import pickle

API_URL = 'http://localhost:5000/glit_predict'

def predict_result(x):
    payload = {'file':x}
    r = requests.post(API_URL, files=payload)

    return r

with open('data/sample_labeled_list_woAmbi_92742_70138_191119.pkl', 'rb') as f:
    sample_input_list = pickle.load(f)

sample_input_list = [sample_input_list[0]]


result = predict_result(sample_input_list)
print(result.json())
# print(result)


