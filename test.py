# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 10:19:04 2018

@author: ASUS
"""

import requests
import json

#url='https://mccptester.herokuapp.com/inventory'
#
#body={
#    "sellerid":"1",
#    "purpose":"data"
#        }
#
#response=requests.get(url, params=body)

#url='https://mccptester.herokuapp.com/accountdetails'
#response=requests.get(url)
#
url='https://mccptester.herokuapp.com/testworker'
response=requests.get(url)

print(response.content)