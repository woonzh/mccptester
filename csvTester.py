# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 21:40:01 2018

@author: ASUS
"""

import csv
import string
import math
from io import StringIO

#files=[('data/'+x) for x in os.listdir('data')]
#fname=files[0]

strLst=string.printable
chars=string.ascii_uppercase

def checkStr(tem):
    return all((i in strLst) for i in tem)

def getCell(row,col):
    if col >25:
        mul=chars[math.floor(col/26)]
    else:
        mul=''
    ones=chars[col%26]
    
    val=mul+ones+str(row+1)
    
    return val

def findErrors(file):
    store={}
    file.seek(0)
    file=file.read()
    file=file.decode("utf-8")
    
    file=StringIO(file)
    
    reader=csv.reader(file, delimiter=",")
    
    for idx, row in enumerate(reader):
        for idx2, cell in enumerate(row):
            if checkStr(str(cell))==False:
                print(str(idx)+ " " +str(idx2))
                store[getCell(idx, idx2)]=cell
                  
    return store