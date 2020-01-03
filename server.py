import flask
from flask import Flask, jsonify
import logging
import json
from setting import *
#import fastai
#from fastai import *

from model_serve import Model_serve

import time

app = Flask(__name__)

model = Model_serve()

@app.route('/')
def home():
    print('Inference Implementation of GLIT')
    return 'Inference implementation of GLIT'

#    Using GET methods
"""
@app.route('/glit_predict', methods=['GET'])
def glit_predict():

    t = time.time() # get execution time

    if flask.request.method == 'GET':
    

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
