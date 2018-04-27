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
    
def updateOrders():
    path="orderupdate.csv"
    df=pd.read_csv(path)
    MPCall.updateOrders(df)

def updateInventories(sellerid):
    skulist=MPCall.getMCCPInventories(sellerid)
    collatedinven=IMSCall.getIMSInventory(sellerid, skulist)
    reconResult=MPCall.reconInven(sellerid, collatedinven)
    return reconResult

df=updateInventories(1)
#skulist=list(df['sku'])