TARGET_NONE = -1
SELF = 0 # User
ENEMY = 1 # Any enemy
ANY = 2 #Any active anemy or user
ALLY = 3 #Any friendly combatant
ACTIVE = 4 # currently active enemy
MULTI_ALLY = 5 # All friendly
MULTI_ENEMY = 6 # all enemies
MULTI_ALL = 7 # everyone
INACTIVE = 8 # One of the non-active enemies
RAND_ENEMY = 9 # Random Enemy
RAND_ALLY = 10 # Random Friendly

WORLD = 50

USER = SELF

EQUIP_HEAD = 100
EQUIP_BODY = 101
EQUIP_RIGHT = 103
EQUIP_LEFT = 104
EQUIP_HANDS = 105
EQUIP_TOKEN = 106

EQUIPPABLE = [EQUIP_HEAD, EQUIP_BODY, EQUIP_RIGHT, EQUIP_LEFT, EQUIP_HANDS, EQUIP_TOKEN]


UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


# Map Info
WALKABLE = '.'

WALL = 120
PLAYER = 121
ENTITY = 122
EMPTY = 123

PHYSTR = 'Phy. Atk.'
PHYDEF = 'Phy. Def.'
SPCSTR = 'Spc. Atk.'
SPCDEF = 'Spc. Def.'
SPEED = 'Speed'
HP = 'HP'
MAXHP = 'Max HP'
ACCURACY = 'Accuracy'
EVASION = 'Evasion'
LUCK = 'Luck'

# Display states
MAP = 0
COMBAT = 1
STATS = 2
STARTMENU = 3
SPLASH = 4
SHOP = 5

CRIT_RATE = 0.02

MOVE_REGEN_TICKS = 1000

DAMAGE_CALC = 1
NEWDIST = True

ATTACK = 0
SWITCH = 1
ITEM = 2
RUN = 3

SAVEDIR = 'saves'

SELECTEDCOLOR = "green"

ACTION_TICK_THRESHOLD = 1000
