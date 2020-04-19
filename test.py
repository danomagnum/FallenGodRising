import maps.bsp as bsp
import maps.maptools as maptools

SPLITS = 8

#XMAX = 60
#YMAX = 36
#
#def map():
#	return [['.' for x in range(XMAX)] for y in range(YMAX)]
#
#a = b.Tree(0, 0, XMAX - 1, YMAX - 1, 12, 2)
#nosplit = map()
#for leave in a.final_leaves():
#	leave.draw(nosplit, True)
#nosplit = mt.flatten(nosplit, True)
#
#a.split(True)
#one_split = map()
#for leave in a.final_leaves():
#	print(leave.x0, leave.y0, leave.width, leave.height)
#	leave.draw(one_split, True)
#one_split = mt.flatten(one_split, True)
#
#a.split(True)
#two_split = map()
#for leave in a.final_leaves():
#	print(leave.x0, leave.y0, leave.width, leave.height)
#	leave.draw(two_split, True)
#two_split = mt.flatten(two_split, True)
#
#a.split(True)
#three_split = map()
#for leave in a.final_leaves():
#	print(leave.x0, leave.y0, leave.width, leave.height)
#	leave.draw(three_split, True)
#three_split = mt.flatten(three_split, True)
#
#

lev = [['.' for x in range(maptools.MAPSIZE[0])] for y in range(maptools.MAPSIZE[1])]
buildings = bsp.Tree(0, 0, maptools.MAPSIZE[0] - 1, maptools.MAPSIZE[1] - 1, 8, 2)

for split in range(SPLITS):
	buildings.split(True)

for building in buildings.final_nodes():
	building.draw(lev, True)

maptools.flatten(lev, True)
