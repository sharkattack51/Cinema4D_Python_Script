#coding:utf-8

import c4d

def main():
  rd = doc.GetActiveRenderData()
  w = rd.GetDataInstance()[c4d.RDATA_XRES]
  h = rd.GetDataInstance()[c4d.RDATA_YRES]
  dist = 0.05
  
  # world to camera
  cam = doc.GetRenderBaseDraw().GetSceneCamera(doc)
  cam_mat = op.GetObject().GetMg().off * ~(cam.GetMg())
  
  # camera to screen
  p = c4d.Vector(cam_mat)
  nz = 1.0 / dist if p.z <= 0.0 else 1.0 / (p.z + dist)
  p.x = (((p.x * nz * 2.0) + 1.0) / 2.0) * w
  p.y = (1.0 - ((p.y * nz * (w / h) * 2.0) + 1.0) / 2.0) * h
  
  print p