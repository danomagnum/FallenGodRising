TARGET_NONE = -1
SELF = 0 # User
ENEMY = 1 # Any enemy
ACTIVE = 2 # currently active enemy
MULTI_SELF = 3 # All friendly
MULTI_ENEMY = 4 # all enemies
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
