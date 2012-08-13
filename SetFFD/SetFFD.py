#coding:utf-8

"""
SetFFD
Auto Set the FFD Object

@author     koichi
@email      sharkattack51@gmail.com
@twitter    @sharkattack51
@version    1.0.0
@date       03/28/2011
"""

import c4d
from c4d import utils
from c4d.gui import GeDialog

#member
m_sub = c4d.Vector(0)
m_margin = c4d.Vector(0)

#dialog
class Dialog(GeDialog):
    def __init__(self):
        pass
    
    def CreateLayout(self):
        self.SetTitle("Set FFD Setting")
        
        #subdivide
        self.GroupBegin(1000,c4d.BFH_CENTER,1,1)
        
        self.AddStaticText(1100,c4d.BFH_CENTER,0,0,"- FFD Subdivide -",c4d.BORDER_NONE)
        
        self.AddSeparatorH(0,c4d.BFH_FIT)
        
        self.GroupBegin(1200,c4d.BFH_CENTER,6,1)
        self.AddStaticText(1210,c4d.BFH_LEFT,0,0,"X",c4d.BORDER_NONE)
        self.AddEditNumberArrows(1220,c4d.BFH_LEFT)
        self.AddStaticText(1230,c4d.BFH_LEFT,0,0,"Y",c4d.BORDER_NONE)
        self.AddEditNumberArrows(1240,c4d.BFH_LEFT)
        self.AddStaticText(1250,c4d.BFH_LEFT,0,0,"Z",c4d.BORDER_NONE)
        self.AddEditNumberArrows(1260,c4d.BFH_LEFT)
        self.GroupEnd()
        
        self.GroupEnd()
        
        #space
        self.GroupSpace(0,10)
        
        #margin
        self.GroupBegin(2000,c4d.BFH_CENTER,1,1)
        
        self.AddStaticText(2100,c4d.BFH_CENTER,0,0,"- Margin Size -",c4d.BORDER_NONE)
        
        self.AddSeparatorH(0,c4d.BFH_FIT)
        
        self.GroupBegin(2200,c4d.BFH_CENTER,6,1)
        self.AddStaticText(2210,c4d.BFH_LEFT,0,0,"X",c4d.BORDER_NONE)
        self.AddEditNumberArrows(2220,c4d.BFH_LEFT)
        self.AddStaticText(2230,c4d.BFH_LEFT,0,0,"Y",c4d.BORDER_NONE)
        self.AddEditNumberArrows(2240,c4d.BFH_LEFT)
        self.AddStaticText(2250,c4d.BFH_LEFT,0,0,"Z",c4d.BORDER_NONE)
        self.AddEditNumberArrows(2260,c4d.BFH_LEFT)
        self.GroupEnd()
        
        self.GroupEnd()
        
        #space
        self.GroupSpace(0,10)
        
        #button
        self.AddButton(3000,c4d.BFH_CENTER,0,0,"SetFFD!")
        
        return True
    
    def InitValues(self):
        self.SetReal(1220,3)#sub x
        self.SetReal(1240,3)#sub y
        self.SetReal(1260,3)#sub z
        self.SetReal(2220,0)#margin x
        self.SetReal(2240,0)#margin y
        self.SetReal(2260,0)#margin z
        
        return True
    
    def Command(self,id,mnsg):
        if(id==3000):
            m_sub.x = self.GetReal(1220)
            m_sub.y = self.GetReal(1240)
            m_sub.z = self.GetReal(1260)
            
            m_margin.x = self.GetReal(2220)
            m_margin.y = self.GetReal(2240)
            m_margin.z = self.GetReal(2260)
            
            self.Close()

        return True
    
#set FFD
def SetFFD():
    #get op data
    obj = op
    size = (obj.GetRad()*10*2)+(m_margin*2)
    pos = op.GetMp()
    
    #new FFD
    c4d.CallCommand(5108)#create FFD
    ffd = doc.GetActiveObject()
    
    #set pos
    ffd.SetAbsPos(pos)
    
    #set ffd_size
    ffd.SetAbsScale(size /(ffd.GetRad()*10*2).x)
    
    ffd[c4d.FFDOBJECT_SIZE] = c4d.Vector(
        ffd.GetRad().x*ffd.GetAbsScale().x,
        ffd.GetRad().y*ffd.GetAbsScale().y,
        ffd.GetRad().z*ffd.GetAbsScale().z)*2
    
    #set scale
    command = c4d.MCOMMAND_RESETSYSTEM
    list = [ffd]
    mode = c4d.MODELINGCOMMANDMODE_ALL
    bc = c4d.BaseContainer()
    bc.SetData(c4d.MDATA_RESETSYSTEM_COMPENSATE,True)
    bc.SetData(c4d.MDATA_RESETSYSTEM_RECURSIVE,True)
    utils.SendModelingCommand(command,list,mode,bc,doc)#Reset System
    
    #set ffd_sub
    ffd[c4d.FFDOBJECT_XSUB] = int(m_sub.x)
    ffd[c4d.FFDOBJECT_YSUB] = int(m_sub.y)
    ffd[c4d.FFDOBJECT_ZSUB] = int(m_sub.z)
    
    #insert object
    ffd.Remove()
    doc.InsertObject(ffd,op)
    
#main
def main():
    c4d.StopAllThreads()
    if not op:
        print "SetFFD: no select object"
        return
    
    dlg = Dialog()
    dlg.Open(c4d.DLG_TYPE_MODAL)
    
    try:
        SetFFD()
    except:
        print "SetFFD: error"
        return
    
    c4d.EventAdd()

if __name__=='__main__':
    main()