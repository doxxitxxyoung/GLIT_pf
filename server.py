#import libaries
# from flask import Flask, request, jsonify, render_template
import flask
from flask import Flask, jsonify
import logging
from setting import *
import fastai
from fastai import *

from model_serve import Model_serve

import time

app = Flask(__name__)

model = Model_serve()

@app.route('/')
def home():
    return 'Hello world'

# @app.route('/predict', methods=['GET'])
# def predict():

#     url = request.args['url']
#     app.logger.info("Classifying sample %s" % (url),)
#     response = request.get(url)
#     sample = BytesIO(response.content)

#     t = time.time()
#     pred_class, pred_idx, outputs = learn.predict(sample)

#     dt = time.time()-t
#     app.logger.info("Execution time : %0.02f seconds" % (dt))
#     app.logger.info("Sample %s classified as %s"%(url, pred_class))

#     return jsonify(pred_class)

"""
@app.route('/glit_predict', methods=['GET'])
def glit_predict():

    data = {'success':False}
    if flask.request.files.get("sample"):
        sample = flask.request.files["sample"]
        result = model.predict(sample)

        data['response'] = result
        data['success'] = True

    return jsonify(data)


@app.route('/glit_predict', methods=['GET'])
def glit_predict():

    data = {'success':False}
    if flask.request.files.get("sample"):
        sample = flask.request.form.get('item')
        result = model.predict(sample)

        data['response'] = result
        data['success'] = True

    return jsonify(data)
"""
@app.route('/glit_predict', methods=['POST'])
def glit_predict():
    if flask.request.method == 'POST':
        file = flask.request.files['file']

        result = model.predict(file)

    return jsonify({'pred_proba': result})


if __name__ == '__main__':
    # app.run(host = '0.0.0.0', debug = True, port = PORT)
    # app.run(host = '0.0.0.0')
    app.run()

# FLASK_ENV=development FLASK_APP=server.py flask run

# needs to modify flask.request.files to somthing that encodes python list