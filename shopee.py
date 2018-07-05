# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 10:19:02 2018

@author: woon.zhenhao
"""
from hashlib import sha256

baseurl="https://partner.shopeemobile.com/api/v1/shop/auth_partner?"

pid='840212'
key='f752aa31ca70b8c87e59d52f6a083e3c53a72e606ff951f6ecae800d0653e576'
redirect="https://mccptester.herokuapp.com/shopeeredirect"

baseString=key+redirect
token=sha256(baseString.encode('ascii')).hexdigest()

def extractUrl():
    url="%sid=%s&token=%s&redirect=%s" % (baseurl, pid, token, redirect)
    data={
        "url": url
            }
    return data

#df=extractUrl()