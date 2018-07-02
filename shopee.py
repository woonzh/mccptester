# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 10:19:02 2018

@author: woon.zhenhao
"""
from hashlib import sha256
from hmac import HMAC

baseurl="https://partner.shopeemobile.com/api/v1/shop/auth_partner?"

pkey=''
redirect="https://mccptester.herokuapp.com/shopeeauth"

baseString=pkey+redirect
#sig=HMAC(bytearray(Secret,'ASCII'), bytearray(baseString, 'ASCII'), sha256).hexdigest()
#sig=HMAC(bytearray(baseString, 'ASCII'), sha256).hexdigest()
sig=""


def extractUrl():
    url="%sid=%s&token=%s&redirect=%s" % (baseurl, pkey, sig, redirect)
    data={
        "url": url
            }
    return data

df=extractUrl()