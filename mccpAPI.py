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
import main
from rq import Queue
from worker import conn

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

class AccountDetails(Resource):        
    def get(self):
        accounts=main.getAccountDetails()
        print(accounts)
        resp = flask.Response(json.dumps(accounts))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

class Accounts(Resource):
    def get(self):
        accts=db.getAccounts()
        print(accts)
                   
        resp = flask.Response(json.dumps(accts))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    
class Testworker(Resource):
    def get(self):
        main.sellerid="1"
        main.recon="false"
        print("testworker starts")
        q=Queue(connection=conn)
        q.enqueue(main.testworker)
        print("testworker ends")
        return "success"
    
class Inventory(Resource):
    def get(self):
        ctype = request.args.get("ctype" ,type = str, default="")
        sellerid = request.args.get("sellerid" ,type = str, default="")
        purpose=request.args.get("purpose", type=str)
        imssku=request.args.get("imssku", type=str, default="")
        mccpsku=request.args.get("mccpsku", type=str, default="")
        
        print("purpose: %s, sellerid: %s, ctype: %s"%(purpose, sellerid, ctype))
        
        if (purpose=="data"):
            result=main.updateInventories2(sellerid, "false")
            print("success")
            print(result)
        else:
            if (ctype=="seller"):
                result=main.updateInventories2(sellerid, "true")
            else:
                result=main.updateSingularSKU(mccpsku, imssku)
        
        resp = flask.Response(json.dumps(result))
        print("json dumps success")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        print("header success")
        return resp
        

api.add_resource(AccountDetails, '/accountdetails')
api.add_resource(Accounts, '/accounts')
api.add_resource(Inventory, '/inventory')
api.add_resource(Testworker, '/testworker')

#test=Inventory
#res=test.get('')
#print(res.data)

if __name__ == '__main__':
     app.run(debug=True)