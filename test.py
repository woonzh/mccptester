# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 10:19:04 2018

@author: ASUS
"""

import requests
import json

import redis
import os
from rq import Worker, Queue, Connection, get_failed_queue
from rq.job import Job

def get(jid):
    try:
        conn = redis.from_url('redis://redistogo:a45da5254d1f41c9dd1228b816f79dc4@albacore.redistogo.com:10191/')
        with Connection(conn):
            job = Job.fetch(jid)
            
            if job.is_finished:
                ret = job.return_value
            elif job.is_queued:
                ret = {'status':'in-queue'}
            elif job.is_started:
                ret = {'status':'waiting'}
            elif job.is_failed:
                ret = {'status': 'failed'}
        
        return ret
    except Exception as ex:
        return ex
    
conn = redis.from_url('redis://redistogo:a45da5254d1f41c9dd1228b816f79dc4@albacore.redistogo.com:10191/')
with Connection(conn):
    failed=get_failed_queue()

#url='https://mccptester.herokuapp.com/inventory'
#
#body={
#    "sellerid":"1",
#    "purpose":"data"
#        }
#
#response=requests.get(url, params=body)

#url='https://mccptester.herokuapp.com/accountdetails'
#response=requests.get(url)
#
#url='https://mccptester.herokuapp.com/testworker'
#response=requests.get(url)

#url='https://mccptester.herokuapp.com/failedworkers'
#response=requests.get(url)
##
#print(response.content)