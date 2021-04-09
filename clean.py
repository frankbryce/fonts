from fontTools.ttLib.ttFont import TTFont
import os

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrztuvwxyz"  # 52 alphanumeric

fontDir = "dataset/train/"  # Directory where .ttf files are stored

def count_glyph(g):
  cnt = 0
  if g.numberOfContours == -1:
    for comp in g.components:
      cnt += count_glyph(font.getGlyphSet()[comp.glyphName]._glyph) + 1
  else:
    cnt += len(g.coordinates) + len(g.endPtsOfContours)
  return cnt
    

directory = os.fsencode(fontDir)
maxLen = 0
maxFnt = None
maxChar = None
lsfiles = os.listdir(directory)
lenfiles = len(lsfiles)
for fontNo, file in enumerate(lsfiles):
  file = file.decode("utf-8")
  print("Font #: %d/%d, %s" % (fontNo+1, lenfiles, file))
  font = TTFont(fontDir + file)
  for c in characters:
    try:
      glyphset = font.getGlyphSet()
    except:
      os.remove(fontDir + file)
      continue
    if c in glyphset:
      cnt = count_glyph(glyphset[c]._glyph)
      if cnt > maxLen:
        maxLen = cnt
        maxFnt = file
        maxChar = c
