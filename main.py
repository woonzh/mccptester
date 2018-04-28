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

def dataFrameToJsonConverter(df):
    columns=list(df)
    length=len(df)
    result={}
    
    for i in list(range(length)):
        line=df.loc[str(i)]
        lineres={}
        j=0
        
        for tit in columns:
            lineres[tit]=line[j]
            j=j+1
            
        result[str(i)]=lineres
    
    return result
    
def updateOrders():
    path="orderupdate.csv"
    df=pd.read_csv(path)
    MPCall.updateOrders(df)

def updateInventories(sellerid, recon):
    skulist=MPCall.getMCCPInventories(sellerid)
    collatedinven=IMSCall.getIMSInventory(sellerid, skulist)
    if (recon=="true"):
        reconResult=MPCall.reconInven(sellerid, collatedinven)
        return dataFrameToJsonConverter(reconResult)
    else:
        return dataFrameToJsonConverter(collatedinven)

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

#df2=getAccountDetails()

#df=updateInventories(1)
#skulist=list(df['sku'])