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
import redis
from rq import Connection, get_failed_queue, Queue, get_current_job
from rq.job import Job
from worker import conn
import os

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
        print("get account details")
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
        print("testworker start")
        q=Queue(connection=conn)
        job=q.enqueue(main.updateInventories2, "1", "false")
        print("testworker ends")
        return str(job.id)
    
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
    
class Failedworkers(Resource):
    def get(self):
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        conn = redis.from_url(redis_url)
        with Connection(conn):
            failed_jobs= get_failed_queue()
            print(failed_jobs.jobs)
            return str(failed_jobs.jobs)
    
class GetJobReport(Resource):
    def get(self):
        jobid = request.args.get("jobid" ,type = str, default="")
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        conn = redis.from_url(redis_url)
        with Connection(conn):
            job = Job.fetch(jobid,conn)
            if job.is_finished:
                ret = job.return_value
            elif job.is_queued:
                ret = {'status':'in-queue'}
            elif job.is_started:
                ret = {'status':'waiting'}
            elif job.is_failed:
                ret = {'status': 'failed'}
        
        return ret

api.add_resource(AccountDetails, '/accountdetails')
api.add_resource(Accounts, '/accounts')
api.add_resource(Inventory, '/inventory')
api.add_resource(Testworker, '/testworker')
api.add_resource(Failedworkers, '/failedworkers')
api.add_resource(GetJobReport, '/jobreport')

#test=Inventory
#res=test.get('')
#print(res.data)

if __name__ == '__main__':
     app.run(debug=True)