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

def updateInventories(sellerid, jsontype):
    skulist=MPCall.getMCCPInventories(sellerid)
    collatedinven=IMSCall.getIMSInventory(sellerid, skulist)
    reconResult=MPCall.reconInven(sellerid, collatedinven)
    if jsontype:
        return dataFrameToJsonConverter(reconResult)
    else:
        return reconResult
    
def getAccountDetails():
    df=db.getAccountDetails()
    result=dataFrameToJsonConverter(df)
    return result

#df2=getAccountDetails()

#df=updateInventories(1)
#skulist=list(df['sku'])