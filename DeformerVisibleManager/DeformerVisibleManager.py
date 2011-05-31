#coding:utf-8

"""
DeformerVisibleManager

@author     koichi
@email      sharkattack51@gmail.com
@twitter    @sharkattack51
@version    1.0.0
@date       03/30/2011
"""

import c4d
from c4d.gui import GeDialog

#var
defType = [
    {"Taper":c4d.Otaper},
    {"Bulge":c4d.Obulge},
    {"Formula":c4d.Oformula},
    {"Shear":c4d.Oshear},
    {"Twist":c4d.Otwist},
    {"Bend":c4d.Obend},
    {"Wrap":c4d.Owrap},
    {"FFD":c4d.Offd},
    {"Wind":c4d.Owind},
    {"Spherity":c4d.Ospherify},
    {"SplineRail":c4d.Osplinerail}
]
stateType = [
    "On",
    "Off",
    "Undef",
    "Toggle"
]

#make dialog window
class Dialog(GeDialog):
   
    def __init__(self):
        pass

    def CreateLayout(self):
        self.SetTitle("Visible Manager")
        
        self.GroupBegin(1000,c4d.BFH_CENTER,1,1)
        self.AddStaticText(1100,c4d.BFH_LEFT,0,0,"- Set Visibility on Editor -",c4d.BORDER_NONE)
        self.GroupEnd()
        
        self.AddSeparatorH(0,c4d.BFH_FIT)
        
        self.GroupBegin(2000,c4d.BFH_CENTER,5,1)

        #object type
        self.AddComboBox(2100,c4d.BFH_CENTER)        
        for i in range(0,len(defType)):
            self.AddChild(2100,i,str(defType[i].keys()[0]))
        
        #space
        self.GroupSpace(10,0)
        
        #text "to"
        self.AddStaticText(2200,c4d.BFH_LEFT,0,0,"to",c4d.BORDER_NONE)
        
        #space
        self.GroupSpace(10,0)
        
        #state
        self.AddComboBox(2300,c4d.BFH_CENTER)
        for j in range(0,len(stateType)):
            self.AddChild(2300,j,str(stateType[j]))
        
        self.GroupEnd()
        
        #button
        self.AddButton(3000,c4d.BFH_CENTER,0,0,"Visible!")
        
        return True

    def InitValues(self):
        self.SetLong(2100,0)#obj type
        self.SetLong(2300,0)#visible state
        
        return True

    def Command(self,id,msg):        
        if(id == 3000):
            ChangeVisible(doc.GetObjects(),self.GetLong(2100),self.GetLong(2300))
            self.Close()
        
        return True

#set visibility
def ChangeVisible(olist,otype,vstate):
    for obj in olist:
        state = obj.GetEditorMode()
        if(obj.CheckType(defType[otype].values()[0])):
            if(state == 3):
                if(state != c4d.MODE_UNDEF):
                    if(state == c4d.MODE_OFF):obj.SetEditorMode(c4d.MODE_ON)
                    elif (state == c4d.MODE_ON):obj.SetEditorMode(c4d.MODE_OFF)
            else:
                obj.SetEditorMode(vstate)
        #next serch
        chilren = obj.GetChildren()
        if(chilren):
            ChangeVisible(chilren,otype,vstate)
        else:
            obj = obj.GetNext()

#main
def main():
    c4d.StopAllThreads()

    if not doc.GetObjects():
        print "DeformerVisibleManager: no object"
        return
    
    dialog = Dialog()
    dialog.Open(c4d.DLG_TYPE_MODAL)
    c4d.EventAdd()

if __name__=='__main__':
    main()
