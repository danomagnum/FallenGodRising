def Random_Map_Insert(zone, entity, level=0):
	pos = zone.find_empty_position(level)
	e1 = entity(x=pos[0], y=pos[1])
	zone.add_entity(e1)

def Positional_Map_Insert(zone, entity, id, level=0):
	for y in range(zone.height):
		for x in range(zone.width):
			if zone.maps[level][y][x] == str(id):
				e1 = entity(x=x, y=y)
				zone.add_entity(e1)
				return
