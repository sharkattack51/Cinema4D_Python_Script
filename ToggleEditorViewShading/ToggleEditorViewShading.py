#coding:utf-8

"""
ToggleEditorViewShading

@author     koichi
@email      sharkattack51@gmail.com
@twitter    @sharkattack51
@version    1.0.0
@date       03/29/2011
"""

import c4d

#toggle
def ToggleShading():
    #get data
    bd = doc.GetActiveBaseDraw()
    currentShade = bd.GetParameterData(c4d.BASEDRAW_DATA_SDISPLAYACTIVE)
    
    #change shading
    if(currentShade == c4d.BASEDRAW_SDISPLAY_GOURAUD):#from GOURAUD
        bd[c4d.BASEDRAW_DATA_SDISPLAYACTIVE] = c4d.BASEDRAW_SDISPLAY_GOURAUD_WIRE#to GOURAUD_WIRE
    elif(currentShade == c4d.BASEDRAW_SDISPLAY_GOURAUD_WIRE):#from GOURAUD_WIRE
        bd[c4d.BASEDRAW_DATA_SDISPLAYACTIVE] = c4d.BASEDRAW_SDISPLAY_NOSHADING#to WIRE
    elif(currentShade == c4d.BASEDRAW_SDISPLAY_NOSHADING):#from WIRE
        bd[c4d.BASEDRAW_DATA_SDISPLAYACTIVE] = c4d.BASEDRAW_SDISPLAY_GOURAUD#to GOURAUD

#main
def main():
    #c4d.StopAllThreads()
    ToggleShading()
    c4d.EventAdd()

if __name__=='__main__':
    main()
    