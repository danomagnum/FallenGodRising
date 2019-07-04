import main

def Random_Map_Insert(zone, entity, level=0):
	pos = zone.find_empty_position(level)
	e1 = entity(x=pos[0], y=pos[1])
	zone.add_entity(e1)

def map_search(zone, id, level=0):
	for y in range(len(zone.maps[level]) - 2):
		for x in range(len(zone.maps[level][0]) - 2):
			if zone.maps[level][y][x] == str(id):
				return x, y
	return None, None

def Positional_Map_Insert(zone, entity, id, level=0):
	result = map_search(zone, id, level)
	if result[0] is not None:
		e1 = entity(x=result[0], y=result[1])
		zone.add_entity(e1)

def Stair_Handler(zone, dir=0):
	levels = len(zone.maps)
	if levels > 1:
		for level in range(levels - 1):
			if dir == 0:
				down_pos = map_search(zone, '\\', level)
				up_pos = map_search(zone, '/', level + 1)
			else:
				down_pos = map_search(zone, '\\', level + 1)
				up_pos = map_search(zone, '/', level)
			
			up = main.UpStairs()
			up.new_x = down_pos[0]
			up.new_y = down_pos[1]
			up.x = up_pos[0]
			up.y = up_pos[1]
			down = main.DownStairs()
			down.new_x = up_pos[0]
			down.new_y = up_pos[1]
			down.x = down_pos[0]
			down.y = down_pos[1]

			if dir == 0:
				zone.level_entities[level].append(down)
				zone.level_entities[level + 1].append(up)
			else:
				zone.level_entities[level].append(up)
				zone.level_entities[level + 1].append(down)

