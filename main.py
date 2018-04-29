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
    skulist=MPCall.getMCCPInventories(sellerid)
    print("skulist completed")
    collatedinven=IMSCall.getIMSInventory(sellerid, skulist)
    print("collated inven completed")
    if (recon=="true"):
        reconResult=MPCall.reconInven(sellerid, collatedinven)
        return dataFrameToJsonConverter(reconResult)
    else:
        return dataFrameToJsonConverter(collatedinven)
        print("return collated inven")

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

#df=getAccountDetails()
df=updateInventories(1, "false")
#skulist=list(df['sku'])