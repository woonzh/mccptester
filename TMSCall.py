# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 16:40:15 2018

@author: woon.zhenhao
"""

import requests
import json

url = "https://deliver-stag.urbanfox.asia/api/u/woonzh/wKAo_sz3uTXdmoYQFpA97saYsuw/gql"

header={
        "Content-Type": "application/graphql"
           }
    
def getStatus(track):
    global header
        
    data = 'query _ { my_transaction_info(ref_no: "%s") {ref_no external_track_no create_date delivr_date pickup_date dst_addr dst_postcode activity} }' % (track)
    response=requests.post(url, headers=header, data=data)
    df=json.loads(response.content)
           
    return df

df=getStatus('ML1493688')