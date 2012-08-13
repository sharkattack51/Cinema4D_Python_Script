#coding:utf-8

"""
ToggleObjectShading

@author     koichi
@email      sharkattack51@gmail.com
@twitter    @sharkattack51
@version    1.0.0
@date       03/31/2011
"""

import c4d

#shading
def ToggleObjectShading():
    tag = op.GetTag(c4d.Tdisplay)
    if not tag:
        #create display tag
        op.MakeTag(c4d.Tdisplay)
        tag = op.GetTag(c4d.Tdisplay)
    
    #chage shading
    tag[c4d.DISPLAYTAG_AFFECT_DISPLAYMODE] = True
    if(tag[c4d.DISPLAYTAG_SDISPLAYMODE] == c4d.DISPLAYTAG_SDISPLAY_GOURAUD):#from GOURAUD
        tag[c4d.DISPLAYTAG_SDISPLAYMODE] = c4d.DISPLAYTAG_SDISPLAY_GOURAUD_WIRE#to GOURAUD_WIRE
    elif(tag[c4d.DISPLAYTAG_SDISPLAYMODE] == c4d.DISPLAYTAG_SDISPLAY_GOURAUD_WIRE):#from GOURAUD_WIRE
        tag[c4d.DISPLAYTAG_SDISPLAYMODE] = c4d.DISPLAYTAG_SDISPLAY_NOSHADING#to WIRE
    elif(tag[c4d.DISPLAYTAG_SDISPLAYMODE] == c4d.DISPLAYTAG_SDISPLAY_NOSHADING):#from WIRE
        tag[c4d.DISPLAYTAG_SDISPLAYMODE] = c4d.DISPLAYTAG_SDISPLAY_GOURAUD#to GOURAUD

#main
def main():
    #c4d.StopAllThreads()

    if not op:
        print "ToggleObjectShading: no select object"
        return
        
    try:
        ToggleObjectShading()
    except:
        print "ToggleObjectShading: error"
        return
    
    c4d.EventAdd()

if __name__=='__main__':
    main()