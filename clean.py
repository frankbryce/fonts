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
    

directory = os.fsencode(fontDir)
maxLen = 0
maxFnt = None
maxChar = None
lsfiles = os.listdir(directory)
lenfiles = len(lsfiles)
buckets = [0] * int(math.log2(10000000))
for fontNo, file in enumerate(lsfiles):
  file = file.decode("utf-8")
  print("Font #: %d/%d, %s" % (fontNo+1, lenfiles, file))
  font = TTFont(fontDir + file)
  foundChar = False
  for c in characters:
    try:
      glyphset = font.getGlyphSet()
    except:
      os.remove(fontDir + file)
      continue
    if c in glyphset:
      cnt = count_glyph(glyphset[c]._glyph)
      if cnt <= 100:
        foundChar = True
      if cnt > maxLen:
        maxLen = cnt
        maxFnt = file
        maxChar = c
      buckets[int(math.log2(cnt))] += 1

  if not foundChar:
    os.remove(fontDir + file)

print(list(map(lambda b,i: f"{math.pow(2,i)}: {b}", buckets,
    range(len(buckets)))))
print(f"Max Len: {maxLen}")
print(f"Max Fnt: {maxFnt}")
print(f"Max Char: {maxChar}")
