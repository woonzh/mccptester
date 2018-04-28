# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 16:04:42 2018

@author: ASUS
"""

import os
from urllib import parse
import psycopg2 as ps
import pandas as pd

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

def getAccounts():
    query="SELECT acct_name FROM accts"
    result=runquery(query)
    ls=[]
    for line in result:
        ls.append(line[0])
    
    return ls

def getAccountDetails():
    df=pd.DataFrame(columns=['acct_name', 'seller_id', 'ims_api_key', 'tms_api_key'])
    query="SELECT * FROM accts"
    result=runquery(query)
    for line in result:
        ls=list(line)
        df.loc[str(len(df))]=ls
    
    return df

df=getAccountDetails()