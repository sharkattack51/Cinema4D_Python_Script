#coding:utf-8

"""
CreateImagePlane
create plane object from selected materials

@author     koichi
@email      sharkattack51@gmail.com
@twitter    @sharkattack51
@version    1.0.0
@date       2011/04/02
"""


import c4d,os
from c4d import utils,gui
from c4d.gui import GeDialog
from c4d.bitmaps import BaseBitmap


#var
ChannelList = ["Color","Luminance","Alpha"]
TypeList = ["Primitive","Polygon"]
DirList = ["Up","Front"]
AposList = ["Center","Bottom"]

matlist = []
parentObj = None
tgtChannel = ""
planeType = ""
direction = ""
axisPos = ""


#dialog
class Dialog(GeDialog):
    
    def __init__(self):
        pass
    
    def CreateLayout(self):
        self.SetTitle("CreateImagePlane")
        
        self.GroupBegin(1000,c4d.BFV_FIT,2,1)
        
        self.GroupBegin(1100,c4d.BFV_FIT,1,4)
        self.AddStaticText(1110,c4d.BFH_LEFT,0,15,"Target Channel :",c4d.BORDER_NONE)
        self.AddStaticText(1120,c4d.BFH_LEFT,0,15,"Plane Type :",c4d.BORDER_NONE)
        self.AddStaticText(1130,c4d.BFH_LEFT,0,15,"Direction :",c4d.BORDER_NONE)
        self.AddStaticText(1140,c4d.BFH_LEFT,0,15,"Axis Pos (polygon only) :",c4d.BORDER_NONE)
        self.GroupEnd()
        
        self.GroupBegin(1200,c4d.BFV_FIT,1,4)
        self.AddComboBox(1210,c4d.BFH_LEFT,30,0,True)
        self.AddChild(1210,0,"Color")
        self.AddChild(1210,1,"Luminance")
        self.AddChild(1210,2,"Alpha")
        self.AddComboBox(1220,c4d.BFH_LEFT,30,0,True)
        self.AddChild(1220,0,"Primitive")
        self.AddChild(1220,1,"Polygon")
        self.AddComboBox(1230,c4d.BFH_LEFT,30,0,True)
        self.AddChild(1230,0,"Up")
        self.AddChild(1230,1,"Front")
        self.AddComboBox(1240,c4d.BFH_LEFT,30,0,True)
        self.AddChild(1240,0,"Center")
        self.AddChild(1240,1,"Bottom")
        self.GroupEnd()
        
        self.GroupEnd()
        
        self.AddSeparatorH(0,c4d.BFH_FIT)

        self.AddButton(1300,c4d.BFH_CENTER,0,40,"Create Plane!")
        
        return True
    
    def InitValues(self):
        self.SetLong(1210,0)
        self.SetLong(1220,0)
        self.SetLong(1230,0)
        self.SetLong(1240,0)
        
        return True
    
    def Command(self,id,msg):
        global tgtChannel
        global planeType
        global direction
        global axisPos

        if(id == 1300):
            tgtChannel = ChannelList[self.GetLong(1210)]
            planeType = TypeList[self.GetLong(1220)]
            direction = DirList[self.GetLong(1230)]
            axisPos = AposList[self.GetLong(1240)]
            
            self.Close()
        
        return True


#create plane
def CreateImagePlane(mat):
    global parentObj
    global tgtChannel
    global planeType
    global direction
    global axisPos
    
    texturePathList = []
    pixelSize = [0,0]
    fileName = ""
    
    #get texture name
    tex = c4d.BaseList2D(c4d.Onull)
    if mat.CheckType(c4d.Mmaterial):
        #switch channel
        if(tgtChannel == "Color"):
            if mat[c4d.MATERIAL_USE_COLOR] and mat[c4d.MATERIAL_COLOR_SHADER]:
                tex = mat[c4d.MATERIAL_COLOR_SHADER]
            else:
                print "CreateImagePlane: no Bitmap ["+mat.GetName()+"]"
                return
        elif(tgtChannel == "Luminance"):
            if mat[c4d.MATERIAL_USE_LUMINANCE] and mat[c4d.MATERIAL_LUMINANCE_SHADER]:
                tex = mat[c4d.MATERIAL_LUMINANCE_SHADER]
            else:
                print "CreateImagePlane: no Bitmap ["+mat.GetName()+"]"
                return
        elif(tgtChannel == "Alpha"):
            if mat[c4d.MATERIAL_USE_ALPHA] and mat[c4d.MATERIAL_ALPHA_SHADER]:
                tex = mat[c4d.MATERIAL_ALPHA_SHADER]
            else:
                print "CreateImagePlane: no Bitmap ["+mat.GetName()+"]"
                return
        
        #check shader type
        if(tex.GetTypeName() == "Bitmap"):
            tex_bc = tex.GetData()
            fileName = tex_bc.GetData(c4d.BITMAPSHADER_FILENAME)
        else:
            print "aaaa"
            print "CreateImagePlane: no Bitmap ["+mat.GetName()+"]"
            return
    else:
        print "CreateImagePlane: no Chennel or Texture ["+mat.GetName()+"]"
        return
    
    #get texture path
    absPathSplit = os.path.split(fileName)
    if(absPathSplit[0]):
        texturePathList.append(absPathSplit[0]) #texturePath[0] abs path
        fileName = absPathSplit[1]
    
    texturePathList.append(doc.GetDocumentPath()) #texturePath[1] document path
    
    texturePathList.append(os.path.join(texturePathList[0],"tex")) #texturePath[2] document/tex

    for i in range(0,10): #texturePath[3]-[13] texture path
        if(c4d.GetGlobalTexturePath(i)):
            texturePathList.append(c4d.GetGlobalTexturePath(i))
    
    #get texture size
    ckFlg = False
    for j in range(0,len(texturePathList)):
        path = os.path.join(texturePathList[j],fileName)
        bmp = BaseBitmap(path)
        result,ismovie = bmp.InitWith(path)
        if result == c4d.IMAGERESULT_OK:
            pixelSize[0],pixelSize[1] = bmp.GetSize()
            ckFlg = True
    if not ckFlg:
        print "CreateImagePlane: no texture [",fileName,"] in ["+mat.GetName()+"]"
        return

    #create plane object
    plane = c4d.BaseObject(c4d.Oplane)
    plane.SetName("Plane["+fileName+"]")
    plane_bc = c4d.BaseContainer()
    plane_bc.SetData(c4d.PRIM_PLANE_WIDTH,pixelSize[0]/10.0)
    plane_bc.SetData(c4d.PRIM_PLANE_HEIGHT,pixelSize[1]/10.0)
    plane_bc.SetData(c4d.PRIM_PLANE_SUBW,1)
    plane_bc.SetData(c4d.PRIM_PLANE_SUBH,1)
    if(direction == "Up"):dir_num = 2
    elif(direction == "Front"):dir_num = 5
    plane_bc.SetData(c4d.PRIM_AXIS,dir_num)#set direction 2:+Y 5:-Z
    plane.SetData(plane_bc)
    
    #set texture
    tag_tex = c4d.BaseTag(c4d.Ttexture)
    tag_tex.SetMaterial(mat)
    tag_tex[c4d.TEXTURETAG_PROJECTION] = c4d.P_UVW
    plane.InsertTag(tag_tex)
    
    #add scene(primitive plane)
    doc.InsertObject(plane,parentObj,None,True)
    
    #convert polygon
    if(planeType == "Polygon"):
        #Make editable
        command = c4d.MCOMMAND_MAKEEDITABLE
        olist = [plane]
        mode = c4d.MODELINGCOMMANDMODE_ALL
        bc = c4d.BaseContainer()
        plane = utils.SendModelingCommand(command,olist,mode,bc,doc)[0]#return list
        plane.Message(c4d.MSG_UPDATE)
        
        #re add scene(polygon plane)
        doc.InsertObject(plane,parentObj,None,True)
        
        #move axis
        if(axisPos == "Bottom"):
            if isinstance(plane,c4d.PointObject):
                points = plane.GetAllPoints()
                for k in range(len(points)):
                    points[k] += c4d.Vector(0,plane.GetRad().y,0)
                plane.SetAllPoints(points)
                plane.Message(c4d.MSG_UPDATE)


#create null object
def CreateGroup():
    global parentObj
    
    parentObj = c4d.BaseObject(c4d.Onull)
    parentObj.SetName("ImagePlanes")
    doc.InsertObject(parentObj)


#execute
def Exec():
    global matlist
    
    try:
        #set group
        CreateGroup()
        #create plane
        for mat in matlist:
            CreateImagePlane(mat)
    except:
        print "CreateImagePlane: error"
        return


#main
def main():
    global matlist
    
    matlist = doc.GetActiveMaterials()
    if not matlist:
        gui.MessageDialog("no select materials.",c4d.GEMB_OK)
        print "CreateImagePlane: no select materials"
        return
    
    dlg = Dialog()
    dlg.Open(c4d.DLG_TYPE_MODAL)
    
    Exec()
    c4d.EventAdd()


if __name__=='__main__':
    main()