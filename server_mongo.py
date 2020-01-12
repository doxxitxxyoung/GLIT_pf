import flask
from flask import Flask, jsonify, request
import logging
import json
from setting import *
#import fastai
#from fastai import *

from model_serve import Model_serve

import time
import numpy as np


app = Flask(__name__)

model = Model_serve()


# Connect to mongo db, get item by drugname and cellline 
from pymongo import MongoClient

#   Local approach
#HOST = 'localhost'
#PORT = 27017
#client = MongoClient(host = HOST, port = PORT)
#db = client['glit-db']
#posts = db.posts # posts == collection

# Atlas use
mongodb_uri = "mongodb+srv://doxxitxxyoung:Tele63741@cluster0-9usdz.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(mongodb_uri)
db = client.glit_db
collection = db.glit_collection


@app.route('/')
def home():
    print('Inference Implementation of GLIT w/ MongoDB')
    return 'Inference implementation of GLIT w/ MongoDB'

#    Using GET methods
@app.route('/glit_predict', methods=['GET'])
def glit_predict():


    if flask.request.method == 'GET':
    
        drugname = request.args.get('drugname')
        cellline = request.args.get('cellline')

        selected_doc = collection.find({'drugname': drugname, 'cellline': cellline})

        #   Only select single doc, ATM.
        selected_doc = selected_doc.__getitem__(0)

        ecfp = selected_doc['ecfp']
        gex = selected_doc['gex']
        dosage = selected_doc['dosage']
        duration = selected_doc['duration']
        label = selected_doc['label']

        """
        ecfp = np.frombuffer(client.hget(name, 'ecfp'), dtype = np.int64)
        gex = np.frombuffer(client.hget(name, 'gex'), dtype = np.float64)
        dosage = client.hget(name, 'dosage')
        duration = client.hget(name, 'duration')
        label = client.hget(name, 'label')
        """

        result = model.predict(ecfp, gex, dosage, duration)
        result = float(result[0][1])
        

#    dt = time.time() - t
#    app.logger.info("Execution time: %0.02f seconds" % (dt))

#    return jsonify({'ecfp': ecfp[0], 'gex':gex[0], 'dosage':dosage, 'duration':duration, 'drugname':drugname, 'predicted_prob':result})
    return jsonify({'dosage':str(dosage), 'duration': str(duration), 'drugname':str(drugname), 'predicted_prob':result})
#    return jsonify({'drugname':drugname, 'cellline':cellline, 'predicted_prob':result})

"""
#    Using POST method
@app.route('/glit_predict', methods=['POST'])
def glit_predict():

    t = time.time() # get execution time

    if flask.request.method == 'POST':
        payload = json.loads(flask.request.get_json())

        ecfp = payload['ecfp']
        gex = payload['gex']
        dosage = payload['dosage']
        duration = payload['duration']
        drugname = payload['drugname']

        result = model.predict(ecfp, gex, dosage, duration)
        result = float(result[0][1])
        

    dt = time.time() - t
    app.logger.info("Execution time: %0.02f seconds" % (dt))


    return jsonify({'ecfp': ecfp[0], 'gex':gex[0], 'dosage':dosage, 'duration':duration, 'drugname':drugname, 'predicted_prob':result})
"""

@app.errorhandler(404)
def url_error(e):
    return """
    'Wrong URL.
    <pre>{}</pre>""".format(e), 404

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
#    HOST='127.0.0.1'
    HOST='0.0.0.0'
    PORT=8080

    app.run(HOST, PORT, debug=True)

# FLASK_ENV=development FLASK_APP=server.py flask run
