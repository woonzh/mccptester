# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 10:19:04 2018

@author: ASUS
"""

import requests
import json
import csv
import IMSCall
    
#url='https://mccptester.herokuapp.com/deliverycheck'
#
#body={
#    "increment_id":"256"
#        }
#
#response=requests.get(url, params=body)

url="https://mccptester.herokuapp.com/orderfile2"
apikey='gifPV0jPWpgQeuOQBwH7lXAo2b3iI5PnEG//tNmPnJk='

file=open('sales_report.csv', 'rb')
files={
        'data':file
        }
body={
        "apikey":apikey}

df=requests.post(url,files=files, params=body)
jid=df.content.decode()

file.close

#url='https://mccptester.herokuapp.com/jobreport'
#body={
#      "jobid": jid
#      }
#response=requests.get(url, params=body)

#url='https://mccptester.herokuapp.com/accountdetails'
#response=requests.get(url)
#
#url='https://mccptester.herokuapp.com/testworker'
#response=requests.get(url)
#
#print(response.content)

#result=getResult('73e253f9-f1ac-4183-a042-bda6a98ddf73')
#print(result)