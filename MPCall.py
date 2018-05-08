# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 16:40:15 2018

@author: woon.zhenhao
"""

import requests
import json
import pandas as pd

header=None

mainurl='https://www.urbanfox.store/rest/all/V1/'

def getHeader():
    global header
    if (header==None):
        url=mainurl+'integration/admin/token'
        
        body={
                "username": "ims",
                "password": "urbanfox2018"
                }
        
        response = requests.post(url, params = body)
        
        key = json.loads(response.content)
        
        header2={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer "+key
                }
        
        header=header2
    
#getHeader()

def updateOrder(refNum, trNum, width, height, length, weight):
    global header
    url=mainurl+'order/readytoship'
    body={
        "referenceNumber": refNum,
        "trackingNumber": trNum,
        "width": width,
        "height": height,
        "length": length,
        "weight": weight
            }
    response=requests.post(url, headers = header, params = body)
    
    df=json.loads(response.content)
    
    print(df)
    
def updateInven(sku, qty, sellerid):
    global header
    url=mainurl+'inventory/update'
    body={
        "sku": sku,
        "qty": qty,
        "seller": sellerid,
        }
    response=requests.post(url, headers=header, params=body)
    df=json.loads(response.content)
    return df
    
def getMCCPInventory(sku):
    global header
    url=mainurl+('stockItems/%s' %(sku))
    response=requests.get(url, headers=header)
    df=json.loads(response.content)
    return df["qty"]

def getUncompletedDeliveries():
    getHeader()
    result=pd.DataFrame(columns=['shipmend increment id','Tracking number', 'status'])
    global header
    url=mainurl+'shipments?searchCriteria[filterGroups][0][filters][0][field]=seller_id&searchCriteria[filterGroups][0][filters][0][value]=1'
#    url=mainurl+'shipments?searchCriteria[filterGroups][0][filters][0][field]=status&searchCriteria[filterGroups][0][filters][0][value]=new order'
    
    response=requests.get(url,headers=header)
    df=json.loads(response.content)['items']
    
    for ship in df:
        shipId=ship['increment_id']
        try:
            tracking=ship['shipping_label']
        except:
            tracking="N.A"
        status='new order'
        ls=[shipId, tracking, status]
        result.loc[len(result)]=ls
    
    return result

contc=getUncompletedDeliveries()
#print(contc)   
    
def updateOrders(df):
    getHeader()
    for i in list(range(len(df))):
        line=df.iloc[i]
        trnum=line["tracking number"]
        refnum=line["reference number"]
        width=line["width"]
        length=line["length"]
        height=line["height"]
        weight=line["weight"]
        updateOrder(header, refnum, trnum, width, height, length, weight)
        print(refnum + " updated")
        
def getMCCPProductList(sellerid):
    global header
    getHeader()
    url=mainurl+('products?searchCriteria[filter_groups][0][filters][0][field]=seller_id&searchCriteria[filter_groups][0][filters][0][value]='+str(sellerid))
    response=requests.get(url, headers=header)
    df=json.loads(response.content)
    items=df['items']
    ls=[]
    
    #remove seller id suffic and only for simple products
    for i in list(range(len(items))):
        itm=items[i]
        if itm['type_id']=='simple':
            sku=itm['sku']
            sku=sku[:-(len(str(sellerid))+1)]
            ls.append(sku)
    
    
    return ls
    
def getMCCPInventories(sellerid):
    result=pd.DataFrame(columns=['mccp sku','mccp qty', 'ims sku'])
    items=getMCCPProductList(sellerid)
    for imssku in items:
        mccpsku=imssku+"-"+str(sellerid)
        qty=getMCCPInventory(mccpsku)
        ls=[mccpsku,qty, imssku]
        result.loc[len(result)]=ls
            
    return result
        
def reconInven(sellerid, invenlist):
    result=[]
    for i in list(range(len(invenlist))):
        mccpqty=invenlist.iloc[i,1]
        imsqty=invenlist.iloc[i,3]
        if (int(mccpqty)!=int(imsqty)):
            imssku=invenlist.iloc[i,2]
            res=updateInven(imssku, imsqty, sellerid)
            result.append(res)
        else:
            result.append("N.A")
            
    invenlist['recon result']=result
    
    return invenlist
