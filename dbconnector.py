# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 16:04:42 2018

@author: ASUS
"""

import os
from urllib import parse
import psycopg2 as ps
import pandas as pd
import datetime
import random
import string

def connectToDatabase():
    url='postgres://nrarbplrmncopz:83c8824b40049266f138346faf865fb3dfa9055b05a6cab130cf7a295cd40198@ec2-54-83-204-6.compute-1.amazonaws.com:5432/d43d4knqc74pv2'

    os.environ['DATABASE_URL'] = url
               
    parse.uses_netloc.append('postgres')
    url=parse.urlparse(os.environ['DATABASE_URL'])
    
    conn=ps.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
    
    cur=conn.cursor()
    
    return cur, conn

def runquery(query):
    cur, conn=connectToDatabase()
    result=None
    try:
        cur.execute(query)
        result=list(cur)
    except:
        result=['error']
        
    cur.close()
    conn.commit()
    return result

def idgenerator():
    result=''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
    return result

def addWorkerLine(calltype):
    timestart=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    wid=idgenerator()
    query="INSERT INTO worker (wid, calltype, reply, starttime) VALUES('%s', '%s', '%s', '%s')" %(wid,calltype,"generating", timestart)
    result=runquery(query)
    return wid
    
def updateWorkerLine(wid, reply):
    endtime=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    query="UPDATE worker SET reply='%s', endtime='%s' WHERE wid='%s'" %(reply, endtime, wid)
    result=runquery(query)
    return result

def getAccounts():
    query="SELECT seller_id, acct_name FROM accts"
    result=runquery(query)
    ret={}
    i=0
    for line in result:
        ls={
            "seller_id":line[0],
            "acct_name":line[1]
                }
        ret[str(i)]=ls
        i+=1
    
    return ret

def getAccountDetails():
    df=pd.DataFrame(columns=['acct_name', 'seller_id', 'ims_api_key', 'tms_api_key'])
    query="SELECT * FROM accts"
    result=runquery(query)
    for line in result:
        ls=list(line)
        df.loc[str(len(df))]=ls
    
    return df

