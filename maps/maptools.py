def Random_Map_Insert(zone, entity):
	pos = zone.find_empty_position()
	e1 = entity(x=pos[0], y=pos[1])
	zone.add_entity(e1)
