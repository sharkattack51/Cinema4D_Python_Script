#coding:utf-8

"""
RenameTexture

@version    1.0.1
@date       2011/04/08
"""


import c4d,os
from c4d import utils,gui
from c4d.gui import GeDialog


#var
matlist = []
chlist = []
seachText = ""
replaceText = ""

#make dialog
class Dialog(GeDialog):

    def __init__(self):
        pass
    
    def CreateLayout(self):
        self.SetTitle("RenameTexture")

        self.GroupBegin(1000,c4d.BFV_FIT,3,1)
        
        self.GroupBegin(1100,c4d.BFV_FIT,1,11)
        self.AddCheckbox(1110,c4d.BFH_LEFT,150,10,"Color")
        self.AddCheckbox(1120,c4d.BFH_LEFT,150,10,"Diffusion")
        self.AddCheckbox(1130,c4d.BFH_LEFT,150,10,"Luminance")
        self.AddCheckbox(1140,c4d.BFH_LEFT,150,10,"Transparency")
        self.AddCheckbox(1150,c4d.BFH_LEFT,150,10,"Reflection")
        self.AddCheckbox(1160,c4d.BFH_LEFT,150,10,"Enviroment")
        self.AddCheckbox(1170,c4d.BFH_LEFT,150,10,"Bump")
        self.AddCheckbox(1180,c4d.BFH_LEFT,150,10,"Normal")
        self.AddCheckbox(1190,c4d.BFH_LEFT,150,10,"Alpha")
        self.AddCheckbox(1191,c4d.BFH_LEFT,150,10,"SpecularColor")
        self.AddCheckbox(1192,c4d.BFH_LEFT,150,10,"Displacement")
        self.GroupEnd()
        
        self.AddSeparatorV(0,c4d.BFV_FIT)
        
        self.GroupBegin(1200,c4d.BFV_CENTER,1,3)
        self.GroupBegin(1210,c4d.BFV_FIT,1,2)
        self.AddStaticText(1211,c4d.BFH_LEFT,200,10,"Search Text :",0);
        self.AddEditText(1212,c4d.BFH_LEFT,400,12)
        self.GroupEnd()
        self.AddStaticText(1220,c4d.BFH_CENTER,20,10,"to",0);
        self.GroupBegin(1230,c4d.BFV_FIT,1,2)
        self.AddStaticText(1231,c4d.BFH_LEFT,200,10,"Replace Text :",0);
        self.AddEditText(1232,c4d.BFH_LEFT,400,12)
        self.GroupEnd()
        self.GroupEnd()
        
        self.GroupEnd()
        
        self.AddSeparatorH(0,c4d.BFH_FIT)

        self.AddButton(1300,c4d.BFH_CENTER,0,40,"Rename Texture!")
        
        return True
    
    def InitValues(self):
        self.SetBool(1110,False)
        self.SetBool(1120,False)
        self.SetBool(1130,False)
        self.SetBool(1140,False)
        self.SetBool(1150,False)
        self.SetBool(1160,False)
        self.SetBool(1170,False)
        self.SetBool(1180,False)
        self.SetBool(1190,False)
        self.SetBool(1191,False)
        self.SetBool(1192,False)
        self.SetString(1212,"")
        self.SetString(1232,"")

        return True
    
    def Command(self,id,msg):
        global chlist
        global seachText
        global replaceText
        
        if(id == 1300):
            #set data
            chlist.append(self.GetBool(1110)) #Color
            chlist.append(self.GetBool(1120)) #Diffusion
            chlist.append(self.GetBool(1130)) #Luminance
            chlist.append(self.GetBool(1140)) #Transparency
            chlist.append(self.GetBool(1150)) #Reflection
            chlist.append(self.GetBool(1160)) #Enviroment
            chlist.append(self.GetBool(1170)) #Bump
            chlist.append(self.GetBool(1180)) #Normal
            chlist.append(self.GetBool(1190)) #Alpha
            chlist.append(self.GetBool(1191)) #SpecularColor
            chlist.append(self.GetBool(1192)) #Displacement
            seachText = self.GetString(1212)
            replaceText = self.GetString(1232)
            
            #exec
            Exec()
            
            self.Close()
            
        return True

#rename
def RenameTexture(mat):
    global chlist
    global seachText
    global replaceText
    
    #check standard material
    if mat.CheckType(c4d.Mmaterial):
        #chaannel loop
        for ch_use in range(len(chlist)):
            #check bool
            if(chlist[ch_use] == True):
                file_name = ""
                tex = c4d.BaseList2D(c4d.Xbitmap)
                
                #switch ch
                if(ch_use == 0):
                    tex = mat[c4d.MATERIAL_COLOR_SHADER]
                elif(ch_use == 1):
                    tex = mat[c4d.MATERIAL_DIFFUSION_SHADER]
                elif(ch_use == 2):
                    tex = mat[c4d.MATERIAL_LUMINANCE_SHADER]
                elif(ch_use == 3):
                    tex = mat[c4d.MATERIAL_TRANSPARENCY_SHADER]
                elif(ch_use == 4):
                    tex = mat[c4d.MATERIAL_REFLECTION_SHADER]
                elif(ch_use == 5):
                    tex = mat[c4d.MATERIAL_ENVIRONMENT_SHADER]
                elif(ch_use == 6):
                    tex = mat[c4d.MATERIAL_BUMP_SHADER]
                elif(ch_use == 7):
                    tex = mat[c4d.MATERIAL_NORMAL_SHADER]
                elif(ch_use == 8):
                    tex = mat[c4d.MATERIAL_ALPHA_SHADER]
                elif(ch_use == 9):
                    tex = mat[c4d.MATERIAL_SPECULAR_SHADER]
                elif(ch_use == 10):
                    tex = mat[c4d.MATERIAL_DISPLACEMENT_SHADER]
                
                #check shader type
                if(tex and ((tex.GetTypeName() == "Bitmap") or (tex.GetTypeName() == "ビットマップ"))):
                    #rename
                    tex_bc = tex.GetData()
                    file_name = tex_bc.GetData(c4d.BITMAPSHADER_FILENAME)
                    file_name = file_name.replace(seachText,replaceText)
                    
                    #set data
                    if(ch_use == 0):
                        mat[c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 1):
                        mat[c4d.MATERIAL_DIFFUSION_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 2):
                        mat[c4d.MATERIAL_LUMINANCE_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 3):
                        mat[c4d.MATERIAL_TRANSPARENCY_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 4):
                        mat[c4d.MATERIAL_REFLECTION_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 5):
                        mat[c4d.MATERIAL_ENVIRONMENT_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 6):
                        mat[c4d.MATERIAL_BUMP_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 7):
                        mat[c4d.MATERIAL_NORMAL_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 8):
                        mat[c4d.MATERIAL_ALPHA_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 9):
                        mat[c4d.MATERIAL_SPECULAR_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    elif(ch_use == 10):
                        mat[c4d.MATERIAL_DISPLACEMENT_SHADER][c4d.BITMAPSHADER_FILENAME] = file_name
                    
                    #update material
                    mat.Message(c4d.MSG_UPDATE)
                    mat.Update(True, True)
    
    else:
        print "RenameTexture: not standard material ["+mat.GetName()+"]" 
        return

#execute
def Exec():
    global matlist
    
    try:
        for mat in matlist:
            RenameTexture(mat)
    
    except:
        print "RenameTexture: error"
        return

#main
def Main():
    global matlist
    
    matlist = doc.GetActiveMaterials()
    if not matlist:
        gui.MessageDialog("no select materials.",c4d.GEMB_OK)
        print "RenameTexture: no select materials"
        return
    
    dlg = Dialog();
    dlg.Open(c4d.DLG_TYPE_MODAL)

    c4d.EventAdd()

if __name__=='__main__':
    Main()