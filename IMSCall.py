# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 16:40:15 2018

@author: woon.zhenhao
"""

import requests
import json
import pandas as pd
import dbconnector as db
from io import StringIO
import csv

url = "https://staging-ims.urbanfox.asia/graphiql"

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
            
def manualUpdateAPIKey(apikey):
    global header
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
    ls=[]
    sync=[]
    for i in list(range(len(skulist))):
        ls.append("")
        sync.append("")
    skulist['ims qty']=ls
    skulist['match']=sync
        
    data = 'query { listItems(page:1, pageSize:1000) {sku quantity}}' 
    response=requests.post(url, headers=header, data=data)
    df=json.loads(response.content)
    items=df['data']['listItems']

    for i in items:
        imsqty=i['quantity']
        sku=i['sku']
        for j in list(range(len(skulist))):
            imssku=skulist.iloc[j,2]
            mccpqty=skulist.iloc[j,1]
            if (sku==imssku):
                skulist.iloc[j,3]=imsqty
                if str(mccpqty)==str(imsqty):
                    skulist.iloc[j,4]="match"
                else:
                    skulist.iloc[j,4]="mismatch"
           
    return skulist
    
def getSingleIMSInventory(imssku, sellerid):
    getAPIKey(sellerid)
    qty=getinventory(imssku)
    return qty

def sendOrders(body):
    global header
    body=body.replace("'sku'",'sku')
    body=body.replace("'quantity'",'quantity')
    body=body.replace("'",'"')
    print(body)
    try:
        response=requests.post(url, headers=header, data=body)
        df2=json.loads(response.content)
        print(df2)
        
        name=list(df2)[0]
        
        if name=="data":
            msg=df2[name]
            resp={
                    name:msg
                }
            return resp, True, msg
        else:
            msg=df2[name][0]['message']
            resp={
                name:msg
                    }
            return resp, False, msg
            
        print("resp")
        return resp
        
    except:
        return {"error":"error response"}
        print(response.content)

def createOrders(df):
    curOrd=""
    count=0
    body=""
    ordItm=[]
    replies={}
    row=''
    results=pd.DataFrame(columns=['ID', "Success", "Message"])
    
    for i in list(df.index):
        row=df.loc[i]
        
        if row['ID'] != curOrd:
            if count > 0:
                body=body.replace('ordItm', str(ordItm))
                replies[curOrd], success, msg=sendOrders(body)
                results.loc[count]=[curOrd, success, msg]
                ordItm=[]
                
            curOrd = row['ID']
            count+=1
            
            body= """mutation {               
                     createOrder(                                 
                    referenceNumber1: "refnum"
                    remarks: "rem"                                 
                    orderItems: ordItm                
                    billingAddress: {addressLine1:"badd", addressLine2:"", city:"Singapore", country:"SG", name:"bname", phone:"bphone", postalCode:"bpost"}                 
                    shippingAddress: {addressLine1:"sadd", addressLine2:"", city:"Singapore", country:"SG", name:"sname", phone:"sphone", postalCode:"spost"}                 
                    customerAddress: {addressLine1:"cadd", addressLine2:"", city:"Singapore", country:"SG", name:"cname", phone:"cphone", postalCode:"cpost"}               
                    ) {                 
                    referenceNumber1                 
                    remarks                 
                    orderItems {                   
                            sku                   
                            quantity                 
                            }               
                    }             
                }"""
            body=body.replace("refnum", "SM"+str(row['ID']))
            body=body.replace("badd", str(row['Billing Address']))
            body=body.replace("bname", str(row['Customer Name']))
            body=body.replace("bphone", str(row['Billing Contact Number']))
            body=body.replace("bpost", str(row['Billing Postal Code']))
            body=body.replace("sadd", str(row['Shipping Address']))
            body=body.replace("sname", str(row['Customer Name']))
            body=body.replace("sphone", str(row['Shipping Contact Number']))
            body=body.replace("spost", str(row['Shipping Postal Code']))
            body=body.replace("cadd", str(row['Shipping Address']))
            body=body.replace("cname", str(row['Customer Name']))
            body=body.replace("cphone", str(row['Shipping Contact Number']))
            body=body.replace("cpost", str(row['Shipping Postal Code']))
        
        temOrd={
            "quantity":row['Quantity'],
            "sku": row['SKU']
                }
        qty=getinventory(row['SKU'])
        ordItm.append(temOrd)
    
    body=body.replace('ordItm', str(ordItm))
    replies[row['ID']], success, msg=sendOrders(body)
    results.loc[count]=[curOrd, success, msg]
    
    return replies, results

def parseAndCreateOrders(file, apikey):
    manualUpdateAPIKey(apikey)
    file.seek(0)
    file=file.read()
    
    try:
        file1=file.decode()
        print("encoding successful")
    
        file1=StringIO(file1)
        
        df=pd.read_csv(file1)
        replies, results=createOrders(df)
        
        return replies, results
    except:
        return {'error': "not able to decode"}

#replies=createOrders(pd.read_csv('test.csv'),'gifPV0jPWpgQeuOQBwH7lXAo2b3iI5PnEG//tNmPnJk=')

#res=getSingleIMSInventory('merries3', 1)
#print(response.content)