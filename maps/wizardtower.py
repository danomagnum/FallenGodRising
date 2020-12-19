import main, battle, zone, entities, moves, elements, items
from constants import *
import random
import maps.maptools as maptools
import maps.cellular
import maps.buildings
import os
import mobs
import utility
ZONENAME = 'WizardTower'

class ThisZone(zone.LinearZone):
	def config(self):
		self.music = 'wizard.mid'
		self.mob_list = [mobs.imp.Imp, mobs.sorcerer.Sorcerer, mobs.sorcerer.Wizard, mobs.sorcerer.Archmage]
		self.mob_list = set(self.mob_list)
		#battle AI to use, #world AI to use, name, *mobs
		self.mobchoices = [(1, [battle.Random_AI, entities.BasicAI1, 'imp', mobs.imp.Imp]),
		                   (2, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Sorcerer]),
		                   (3, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Sorcerer, mobs.imp.Imp]),
		                   (5, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Sorcerer, mobs.sorcerer.Wizard]),
		                   (9, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Wizard, mobs.sorcerer.Sorcerer, mobs.sorcerer.Sorcerer]),
		                   (13, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Sorcerer, mobs.sorcerer.Sorcerer, mobs.sorcerer.Wizard]),
		                   (17, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Wizard, mobs.sorcerer.Wizard, mobs.sorcerer.Archmage])]
	def level_019(self):
		gen_level = 1
		if self.game.player is not None:
			gen_level = self.game.player.level
		newitem = items.gen_gear(self.game, gen_level + 3)
		maptools.Random_Map_Insert(self, entities.Treasure(self.game, [newitem,]))
	
	def moblist(self, depth):
		intersectors = []
		if depth < 0.1:
			#choose one trash mob or one okay mob per group
			if random.random() < 0.5:
				intersectors = [mobs.trash]
			else:
				intersectors = [mobs.okay]
		elif depth < 0.2:
			#choose one okay mob or one okay and one trash mob per group.
			if random.random() < 0.5:
				intersectors = [mobs.okay]
			else:
				intersectors = [mobs.okay, mobs.trash]
		elif depth < 0.3:
			#choose one trash and one okay or two okay mobs per group or three trash
			rv = random.random
			if rv < 0.33:
				intersectors = [mobs.okay, mobs.trash]
			elif rv < 0.66:
				intersectors = [mobs.okay, mobs.okay]
			else:
				intersectors = [mobs.trash, mobs.trash, trash]
		elif depth < 0.6:
			#two okay mobs per group  or two okay and one trash
			rv = random.random
			if rv < 0.5:
				intersectors = [mobs.okay, mobs.okay]
			else:
				intersectors = [mobs.okay, mobs.okay, mobs.trash]
		elif depth < 0.7:
			#two okay mobs per group or one good mob and two trash
			rv = random.random
			if rv < 0.5:
				intersectors = [mobs.okay, mobs.okay]
			else:
				intersectors = [mobs.good, mobs.trash, mobs.trash]
		elif depth < 0.8:
			#two good mobs per group or one good mob and two okay
			rv = random.random
			if rv < 0.5:
				intersectors = [mobs.good, mobs.good]
			else:
				intersectors = [mobs.good, mobs.okay, mobs.okay]
		elif depth < 0.9:
			#two good or three good
			rv = random.random
			if rv < 0.5:
				intersectors = [mobs.good, mobs.good]
			else:
				intersectors = [mobs.good, mobs.good, mobs.good]
		else:
			#three good or two good and one okay
			rv = random.random
			if rv < 0.5:
				intersectors = [mobs.good, mobs.good, mobs.okay]
			else:
				intersectors = [mobs.good, mobs.good, mobs.good]
		return intersectors


	def level_populate(self, level, visit_no):
		gen_level = 1
		if self.game.player is not None:
			gen_level = self.game.player.combatants[0].level
		gen_level += self.game.get_var('GLO')

		# a metric for how far we are into the dungeon
		depth = level / self.levels


		if visit_no < 2:
			#if I only want to populate on the first visit
			item_count = random.randint(0,2)
			for i in range(item_count):
				chance = random.random()
				if chance < 0.05:
					newitem = items.gen_gear(self.game, gen_level)
				elif chance < 0.3:
					newitem = items.scrolls.gen_movescroll(self.game)
				else:
					newitem = items.gen_base_item(self.game)
				maptools.Random_Map_Insert(self, entities.Treasure(self.game, [newitem,]))

			mob_min = random.randint(0,2)
			mob_max = random.randint(5,7)
			mob_count = random.randint(mob_min, mob_max)

			for m in range(mob_count):
				intersectors = self.moblist(depth)
				mob_party = []
				for i in intersectors:
					mob = self.mob_list.intersection(i)
					if mob:
						mob_party.append(random.sample(mob, 1)[0])
						
				if mob_party:
					moblist = utility.select_by_level(level, self.mobchoices)
					entity = maptools.Random_Map_Insert(self, mobs.party(self.game, moblist[0], moblist[1], gen_level, mob_party, mob_party[0].__name__))


#####################
# populate the zone with entities
#####################

def genzone(game):

	# generate maps
	map_list = []

	for l in range(20):
		game.progress()
		lev = maps.buildings.building_octagon(maptools.MAPSIZE[1], maptools.MAPSIZE[1])
		if l == 0:
			#maptools.add_stairs(lev, down=False)
			#maptools.add_stairs(lev, up=False)
			#maptools.add_stairs(lev)
			maptools.add_stairs(lev, up=False)
		elif l == 19:
			maptools.add_stairs(lev, down=False)
		else:
			maptools.add_stairs(lev)
		lev = maptools.flatten(lev)
		map_list.append(maptools.flatten(lev))
	#maze = maptools.maze(16, 16)
		# Create zone
	zone = ThisZone(ZONENAME, game, maps=map_list)
	#zone.grid_width = 16
	zone.change_level(0)

	alter = entities.Alter(game)
	backpack = items.Backpack(game)
	for x in range(random.randint(2,6)):
		p = items.boosts.ArcStrBoost(game)
		backpack.store(p)
	alter.backpack = backpack
	maptools.Random_Map_Insert(zone, alter, 19)
	game.get_var('Alters').append(alter)


	# Populate zone with entities
	maptools.Stair_Handler(zone)
	maptools.Door_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	maps.maptools.overworld_inject(game, zone, newchar='w', mask=maps.buildings.building_octagon(maptools.MAPSIZE[0], maptools.MAPSIZE[1], padding=5,outside_door=True))
	zone.fast_travel_options[0] = main.FastTravel('Entrance', 0)

	return zone
