# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 16:40:15 2018

@author: woon.zhenhao
"""

import requests
import json
import pandas as pd
import dbconnector as db

url = "https://ims.urbanfox.asia/graphiql"

header=None

def getAPIKey(sellerid):
    global header
    query="SELECT seller_id, ims_api_key FROM accts"
    result=db.runquery(query)
    
    for line in result:
        resId=line[0]
        if str(resId)==str(sellerid):
            apikey=line[1]
            header = {
                "Authorization": "Bearer "+apikey,
                "Content-Type": "application/graphql"
                   }

def getinventory(sku):
    global header
    data = 'mutation { createItemReference(sku:"%s") {sku quantity}}' %(sku)
    
    try:
        response=requests.post(url, headers=header, data=data)
        df2=json.loads(response.content)
        qty=df2['data']['createItemReference']['quantity']
        return qty
    except:
        return 0

def getIMSInventory(sellerid, skulist):
    getAPIKey(sellerid)
    ls=[]
    sync=[]
    for i in list(range(len(skulist))):
        imssku=skulist.iloc[i,2]
        mccpqty=skulist.iloc[i,1]
        qty=getinventory(imssku)
        ls.append(qty)
        if str(mccpqty)==str(qty):
            sync.append("match")
        else:
            sync.append("mismatch")
    
    skulist['ims qty']=ls
    skulist['match']=sync
        
    return skulist

def getOrderStatus(refnum):
    t=''
    
def getIMSInventory2(sellerid, skulist):
    getAPIKey(sellerid)
    data = 'query { listItems(page:1, pageSize:1000) {sku quantity}}' 
    response=requests.post(url, headers=header, data=data)
    df=json.loads(response.content)
    items=df['data']['listItems']
    sync=[]
    ls=[]
    for i in items:
        imsqty=i['quantity']
        sku=i['sku']
        for j in list(range(len(skulist))):
            imssku=skulist.iloc[j,2]
            mccpqty=skulist.iloc[j,1]
            if (sku==imssku):
                ls.append(imsqty)
                if str(mccpqty)==str(imsqty):
                    sync.append("match")
                else:
                    sync.append("mismatch")
    skulist['ims qty']=ls
    skulist['match']=sync
           
    return skulist
    

#print(response.content)