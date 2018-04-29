# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 16:40:15 2018

@author: woon.zhenhao
"""

import requests
import json
import pandas as pd
import MPCall
import IMSCall
import dbconnector as db
import time
from rq import Queue
from worker import conn
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def dataFrameToJsonConverter(df):
    columns=list(df)
    length=len(df)
    result={}
    
    for i in list(range(length)):
        line=df.iloc[[i]]
        lineres={}
        j=0
        
        for tit in columns:
            lineres[tit]=str(line.iloc[0,j])
            j=j+1
            
        result[str(i)]=lineres
    
    return result
    
def updateOrders():
    path="orderupdate.csv"
    df=pd.read_csv(path)
    MPCall.updateOrders(df)

def updateInventories(sellerid, recon):
    start = time.time()
    skulist=MPCall.getMCCPInventories(sellerid)
    end1 = time.time()
    print("skulist completed: "+ str(end1-start))
    collatedinven=IMSCall.getIMSInventory(sellerid, skulist)
    end2 = time.time()
    print("collated inven completed: "+ str(end2-start))
    if (recon=="true"):
        reconResult=MPCall.reconInven(sellerid, collatedinven)
        result=dataFrameToJsonConverter(reconResult)
        print("return recon result")
        return result
    else:
        result=dataFrameToJsonConverter(collatedinven)
        print("return collated inven")
        return result
    
def updateInventories2(sellerid, recon):
    print("seller id: " + sellerid)
    skulist=MPCall.getMCCPInventories(sellerid)
    collatedinven=IMSCall.getIMSInventory2(sellerid, skulist)
    if (recon=="true"):
        reconResult=MPCall.reconInven(sellerid, collatedinven)
        result=dataFrameToJsonConverter(reconResult)
        print("return recon result")
#        return result
    else:
        result=dataFrameToJsonConverter(collatedinven)
        print("return collated inven")
        print(result)
#        return result

def updateSingularSKU(mccpsku, imssku):
    IMSCall.getAPIKey()
    qty=IMSCall.getSingleIMSInventory(imssku)
    sellerid=mccpsku[:(len(mccpsku)-len(imssku)-1)]
    result=MPCall.updateInven(imssku, qty, sellerid)
    return result

def getAccountDetails():
    df=db.getAccountDetails()
    result=dataFrameToJsonConverter(df)
    return result

def testworker():
    print("test worker ")

#df=getAccountDetails()
#df=updateInventories2('1', "false")
#skulist=list(df['sku'])