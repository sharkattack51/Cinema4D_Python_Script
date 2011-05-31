#coding:utf-8

"""
BillboardChildren
�O���[�v�ȉ��̑��K�w�̎q���̃I�u�W�F�N�g���^�[�Q�b�g�̌�����
�r���{�[�h�������܂��B

@author     koichi
@email      sharkattack51@gmail.com
@twitter    @sharkattack51
@version    1.1.0
@date       05/18/2011
"""

import c4d
import math

#######################################

#�^�[�Q�b�g�I�u�W�F�N�g���ݒ�@��̏ꍇ�^�[�Q�b�g�̓����_�[�A�N�e�B�u�ȃJ�����ɂȂ�܂� ("aaa"/"")
targetName = ""

#�s�b�`�p�̌Œ� (True/False)
holdPitch = True

#######################################

def main():

    #�^�[�Q�b�g�I�u�W�F�N�g�擾
    if not targetName:
        #�V�[���J����
        targetObj = doc.GetRenderBaseDraw().GetSceneCamera(doc)
    else:
        #�I�u�W�F�N�g�T�[�`
        targetObj = doc.SearchObject(targetName)
    if not targetObj:
        return
    
    #���[�v����
    parent = op.GetObject()
    child = parent.GetDown()
    while child:
        #���[���h�ʒu�擾
        position = child.GetMg().off
        dirVec = targetObj.GetMg().off - position
        
        #��]�v�Z
        newRot = c4d.utils.VectorToHPB(dirVec)
        if holdPitch:
            newRot.y = 0
        newRot = newRot - parent.GetAbsRot()
        
        #�K�p 
        child.SetAbsRot(newRot)
        
        #����
        child = child.GetNext()
        if not child:
            break