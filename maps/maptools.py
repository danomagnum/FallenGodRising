def Random_Map_Insert(zone, entity):
	pos = zone.find_empty_position()
	e1 = entity(x=pos[0], y=pos[1])
	zone.add_entity(e1)

def Positional_Map_Insert(zone, entity, id):
	for y in range(zone.height):
		for x in range(zone.width):
			if zone.map[y][x] == str(id):
				e1 = entity(x=x, y=y)
				zone.add_entity(e1)
				return
