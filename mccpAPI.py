# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 17:34:54 2018

@author: woon.zhenhao
"""
import flask
from flask import Flask, request, make_response, render_template
from flask_cors import CORS
from flask_restful import Resource, Api
import json
import dbconnector as db

app = Flask(__name__)
api = Api(app)
CORS(app)

#@app.route('/')
#def hello():
#    return render_template('home.html')
#
#@app.route('/account')
#def account():
#    return render_template('account.html')

class Accounts(Resource):        
    def get(self):
        accounts=db.getAccounts()
        result={}
        i=0
        for acct in accounts:
           result[str(i)]=acct
        
        resp = flask.Response(json.dumps(result))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

api.add_resource(Accounts, '/accounts')

#test=Accounts
#res=test.get('')
#print(res.data)

if __name__ == '__main__':
     app.run(debug=True)