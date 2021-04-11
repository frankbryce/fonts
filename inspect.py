from fontTools.ttLib.ttFont import TTFont
import math
import os

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrztuvwxyz"  # 52 alphanumeric

fontDir = "dataset/validate/"  # Directory where .ttf files are stored

def count_glyph(g):
  cnt = 0
  if g.numberOfContours == -1:
    for comp in g.components:
      cnt += count_glyph(font.getGlyphSet()[comp.glyphName]._glyph) + 1
  else:
    cnt += len(g.coordinates) + len(g.endPtsOfContours)
  return cnt

def bounding_box(g, xOffset=0.0, yOffset=0.0):
  minx, maxx, miny, maxy = math.inf, -math.inf, math.inf, -math.inf
  def update(new_minx, new_maxx, new_miny, new_maxy):
      nonlocal minx
      nonlocal maxx
      nonlocal miny
      nonlocal maxy
      if new_minx < minx:
          minx = new_minx
      if new_miny < miny:
          miny = new_miny
      if new_maxx > maxx:
          maxx = new_maxx
      if new_maxy > maxy:
          maxy = new_maxy
  if g.numberOfContours == -1:
    for comp in g.components:
       update(*bounding_box(font.getGlyphSet()[comp.glyphName]._glyph,
           comp.x,
           comp.y))
  else:
      for coord in g.coordinates:
          minx = min(minx, coord[0])
          miny = min(miny, coord[1])
          maxx = max(maxx, coord[0])
          maxy = max(maxy, coord[1])
  return minx, maxx, miny, maxy


directory = os.fsencode(fontDir)
maxLen = 0
maxFnt = None
maxChar = None
lsfiles = os.listdir(directory)
lenfiles = len(lsfiles)
buckets = [0] * int(math.log2(10000000))
minx,maxx,miny,maxy = 0,0,0,0
for fontNo, file in enumerate(lsfiles):
  file = file.decode("utf-8")
  print("Font #: %d/%d, %s" % (fontNo+1, lenfiles, file))
  font = TTFont(fontDir + file)
  print(vars(font))
  print(vars(font.reader))
  foundChar = False
  for c in characters:
    try:
      glyphset = font.getGlyphSet()
    except:
      os.remove(fontDir + file)
      continue
    if c in glyphset:
      box = bounding_box(glyphset[c]._glyph)
      minx = min(minx, box[0])
      maxx = max(maxx, box[1])
      miny = min(miny, box[2])
      maxy = max(maxy, box[3])
      print(f"  bounding box: {box}")
print(f"total bounding box: {minx},{maxx},{miny},{maxy}")
