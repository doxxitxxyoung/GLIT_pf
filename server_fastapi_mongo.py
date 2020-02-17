import uvicorn
from fastapi import FastAPI, APIRouter, Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

import server_fastapi_router
from fastapi import File, Form, UploadFile

import time

from model_serve import Model_serve

model = Model_serve()

#connect to mongo db, get item by drugname and cellline
from pymongo import MongoClient

client = MongoClient(host = 'localhost', port = 27017)
db = client['glit-db']
posts = db.posts


class InputData(BaseModel):
    ecfp: List[float]
    gex: List[float]
    dosage: float
    duration: int
    drugname: str


app = FastAPI()
#app.include_router(server_fastapi_router, prefix='/glit')


"""
@app.get("/healthcheck", status_code=200)
async def root():
    return "Inference implementation of GLIT on FastAPI"
"""

@app.get("/")
def root():
    return "Inference implementation of GLIT on FastAPI"

#   Using GET method, gather drugname and cellline

@app.get('/glit_predict')

async def glit_predict(drugname, cellline):
    selected_doc = posts.find({'drugname': drugname, 'cellline': cellline})

    #   Only choose 1st record, ATM
    selected_doc = selected_doc.__getitem__(0)

    ecfp = selected_doc['ecfp']
    gex = selected_doc['gex']
    dosage = selected_doc['dosage']
    duration = selected_doc['duration']
    label = selected_doc['label']

    result = model.predict(ecfp, gex, dosage, duration)
    result = float(result[0][1])

    return {'ecfp': ecfp[0], 'gex':gex[0], 'dosage':dosage, 'duration':duration, 'drugname':drugname, 'cellline': cellline, 'predicted_prob':result}

"""
@app.post('/glit_predict')
#@app.route('/glit_predict')
#@app.route('/glit_predict', method=['GET', 'POST'])
#def glit_predict(request: dict):

def glit_predict(request: InputData):
    request_dict = request.dict()

    t = time.time() # get execution time
    
    ecfp = request_dict['ecfp']
    gex = request_dict['gex']
    dosage = request_dict['dosage']
    duration = request_dict['duration']
    drugname = request_dict['drugname']

    result = model.predict(ecfp, gex, dosage, duration)
    result = float(result[0][1])


    dt = time.time() - t
#    app.logger.info("Execution time: %0.02f seconds" % (dt))

#    return jsonify({'ecfp': ecfp[0], 'gex':gex[0], 'dosage':dosage, 'duration':duration, 'drugname':drugname, 'predicted_prob':result})
#    return JSONResponse(content = {'ecfp': ecfp[0], 'gex':gex[0], 'dosage':dosage, 'duration':duration, 'drugname':drugname, 'predicted_prob':result})
    return {'ecfp': ecfp[0], 'gex':gex[0], 'dosage':dosage, 'duration':duration, 'drugname':drugname, 'predicted_prob':result}
"""




"""
def glit_predict(request: InputData):
    
    print(request)

    print(request.body())
    print(request.json())
    print(request.form())

#    json_compatible_item_data = jsonable_encoder(Request)
    json_compatible_item_data = jsonable_encoder(request.json())
    print(json_compatible_item_data)

    return JSONResponse(content=json_compatible_item_data)
"""




"""
#@app.post('/glit_predict')
@app.get('/glit_predict')
#@app.route('/glit_predict', method=['GET', 'POST'])
#def glit_predict(request: dict):
def glit_predict(request: Request):
    print(request)
    json_compatible_item_data = jsonable_encoder(Request)
    print(json_compatible_item_data)

    return JSONResponse(content=json_compatible_item_data)
"""
    
     

"""
def glit_predict(ecfp: ):
    t = time.time() # get execution time

#    if flask.request.method == 'GET':
    
    ecfp = flask.request.form.getlist('ecfp')
    gex = flask.request.form.getlist('gex')
    dosage = flask.request.form.get('dosage')
    duration = flask.request.form.get('duration')
    drugname = flask.request.form.get('drugname')

    result = model.predict(ecfp, gex, dosage, duration)
    result = float(result[0][1])


    dt = time.time() - t
    app.logger.info("Execution time: %0.02f seconds" % (dt))

    return jsonify({'ecfp': ecfp[0], 'gex':gex[0], 'dosage':dosage, 'duration':duration, 'drugname':drugname, 'predicted_prob':result})
"""

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8080

    uvicorn.run(app, host = HOST, port = PORT)
