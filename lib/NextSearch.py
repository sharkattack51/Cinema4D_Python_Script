#coding:utf-8

import c4d

def main():
    parent = op[c4d.ID_USERDATA, 1]
    nextSearch(parent,eachFunction)
    
def nextSearch(obj,func):
    children = obj.GetChildren()
    if not children:
        return
    else:
        for child in children:
            func(child)
            nextSearch(child,func)

def eachFunction(obj):
    print obj.GetName()