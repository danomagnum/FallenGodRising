import main, battle, characters, zone, entities, moves, elements, items
from constants import *
import random
import maps.maptools as maptools
import maps.cellular
import os
import mobs
import utility
ZONENAME = 'GoblinCave'

class WarpIn(entities.ZoneWarp):
	def config(self):
		self.char = '>'
		self.new_x = None
		self.new_y = None
		self.new_zone = None
#entities.DownStaris()
#entities.UpStairs()

#####################
# The characters subclasses are how you create enemies.
# You can used "canned" ones or create your own.
#####################

#####################
# The entities subclasses are items that will appear in the world.
# You can used "canned" ones or create your own.
# This is also where you set up battle groups by inheriting entities.Battler and
# assigning combatants
#####################
#class Rat(entities.RandWalker, entities.Battler):
class MonoGoblin(battle.Random_AI,entities.BasicAI1):
	# example basic enemy
	def config(self):
		self.name = 'MonoGoblin'
		self.combatants.append(mobs.Goblin(self.game, level=1))
		self.char = 'g'

class MonoGoblin(battle.Random_AI,entities.BasicAI1):
	# example basic enemy
	def config(self):
		self.name = 'MonoGoblin'
		self.combatants.append(mobs.Goblin(self.game, level=1))
		self.char = 'g'




#####################
# load the map file(s)
#####################

filename = os.path.split(__file__)[-1]
#__file__[:-3]
path = os.path.dirname(os.path.realpath(__file__))
#+ '.map'

files = []
for i in os.listdir(path):
	if os.path.isfile(os.path.join(path,i)) and filename[:-3] in i:
		if i[-3:] == 'map':
			files.append(os.path.join(path, i))
		

class ThisZone(zone.Zone):
	def level_populate(self, level, visit_no):
		gen_level = 1
		if self.game.player is not None:
			gen_level = self.game.player.level

		if visit_no < 2:
			#if I only want to populate on the first visit
			item_count = random.randint(0,2)
			for i in range(item_count):
				chance = random.random()
				if chance < 0.05:
					newitem = items.gen_gear(self.game, gen_level)
				elif chance < 0.3:
					newitem = items.gen_movescroll(self.game)
				else:
					newitem = items.gen_base_item(self.game)
				maptools.Random_Map_Insert(self, entities.Treasure(self.game, [newitem,]))
			mob_count = random.randint(0, 6)
			mobchoices = [(1, [mobs.Goblin]),
			              (3, [mobs.Goblin, mobs.Goblin]),
				      (5, [mobs.Goblin, mobs.Hobgoblin]),
				      (7, [mobs.Goblin, mobs.Goblin, mobs.Hobgoblin])]
			for m in range(mob_count):
				moblist = utility.select_by_level(level, mobchoices)
				maptools.Random_Map_Insert(self, mobs.party(self.game, battle.Random_AI, entities.BasicAI1, level, moblist, 'goblin')(self.game))

	def level_023(self):
		pass # this is another way to do something special on specific levels.

#####################
# populate the zone with entities
#####################

def genzone(game):

	# generate maps
	map_list = []

	for l in range(10):
		lev = maps.cellular.gen_cellular(gens=4)
		if l == 0:
			#maptools.add_stairs(lev, down=False)
			#maptools.add_stairs(lev, up=False)
			#maptools.add_stairs(lev)
			maptools.add_stairs(lev, up=False)
		elif l == 9:
			maptools.add_stairs(lev, down=False)
		else:
			maptools.add_stairs(lev)
		map_list.append(maptools.flatten(lev))
	#maze = maptools.maze(16, 16)
		# Create zone
	zone = ThisZone(ZONENAME, game, maps=map_list)
	#zone.grid_width = 16
	zone.change_level(0)

	# Populate zone with entities
	maptools.Stair_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	return zone
