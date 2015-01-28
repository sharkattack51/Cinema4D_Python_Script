#coding:utf-8

###
# 選択オブジェクトのアニメーションをjsonで出力する
###

import os
import json
import c4d
from c4d import storage

def main():
  
  animTable = {}
  
  if not op:
    print 'no selection object...'  
    return
  
  # Bake Objects...
  c4d.CallCommand(465001219)
  bakedOp = op.GetNext()
  
  # Bake済みを対象
  for track in bakedOp.GetCTracks():
    name = track.GetName()
    curve = track.GetCurve()
    key_count = curve.GetKeyCount()
    keys = []
    for key_id in xrange(key_count):
      key = curve.GetKey(key_id)
      value = key.GetValue()
      keys.append(value)
    animTable[name] = keys
  
  # リストを保存
  path = storage.SaveDialog(title = 'save animation data')
  if path != '' and path != None:
    f = open(path, 'w')
    f.write(json.dumps(animTable))
    f.close()
    print 'save file as ' + path
  
  bakedOp.Remove()
  c4d.EventAdd()

if __name__ == '__main__':
  main()