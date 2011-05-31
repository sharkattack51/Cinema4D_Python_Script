#coding:utf-8

"""
BillboardChildren
グループ以下の第一階層の子供のオブジェクトをターゲットの向きに
ビルボード処理します。

@author     koichi
@email      sharkattack51@gmail.com
@twitter    @sharkattack51
@version    1.1.0
@date       05/18/2011
"""

import c4d
import math

#######################################

#ターゲットオブジェクト名設定　空の場合ターゲットはレンダーアクティブなカメラになります ("aaa"/"")
targetName = ""

#ピッチ角の固定 (True/False)
holdPitch = True

#######################################

def main():

    #ターゲットオブジェクト取得
    if not targetName:
        #シーンカメラ
        targetObj = doc.GetRenderBaseDraw().GetSceneCamera(doc)
    else:
        #オブジェクトサーチ
        targetObj = doc.SearchObject(targetName)
    if not targetObj:
        return
    
    #ループ処理
    parent = op.GetObject()
    child = parent.GetDown()
    while child:
        #ワールド位置取得
        position = child.GetMg().off
        dirVec = targetObj.GetMg().off - position
        
        #回転計算
        newRot = c4d.utils.VectorToHPB(dirVec)
        if holdPitch:
            newRot.y = 0
        newRot = newRot - parent.GetAbsRot()
        
        #適用 
        child.SetAbsRot(newRot)
        
        #次へ
        child = child.GetNext()
        if not child:
            break