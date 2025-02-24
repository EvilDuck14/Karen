PUNCH_SEQUENCE_MAX_DELAY = 0 * 60 # to be determined

JUMP_COOLDOWN = 0 * 60 # to be determined

TRACER_MAX_CHARGES = 5
TRACER_CHARGE_TIME = 2.5 * 60
TRACER_COOLDOWN_TIME = 0.5 * 60
TRACER_ACTIVE_TIME = 4 * 60
TRACER_PROC_DAMAGE = 45

SWING_MAX_CHARGES = 3
SWING_CHARGE_TIME = 6 * 60
WHIFF_REWARD_TIME = 0 * 60 # to be determined

GOH_MAX_CHARGES = 1
GOH_CHARGE_TIME = 8 * 60

UPPERCUT_MAX_CHARGES = 2
UPPERCUT_CHARGE_TIME = 6 * 60
UPPERCUT_COOLDOWN_TIME = 2 * 60

SYMBIOTE_MAX_CHARGES = 1
SYMBIOTE_CHARGE_TIME = 40 * 60



ACTION_NAMES = {
    "j" : "j", "jump" : "j", "dj" : "j",
    "l" : "l", "land" : "l",
    "p" : "p", "punch" : "p", "puncha" : "p",  "punchb" : "p", "meleepunch" : "p",  "meleepuncha" : "p",  "meleepunchb" : "p",
    "k" : "k", "kick" : "k",  "meleekick" : "k",
    "o" : "o", "overheadslam" : "o",  "overhead" : "o",  "oh" : "o",  "meleeoverhead" : "o",  "slam" : "o",
    "t" : "t", "tracer" : "t",  "webtracer" : "t",  "cluster" : "t",  "webcluster" : "t",
    "s" : "s", "swing" : "s", "webswing" : "s",  "highswing" : "s",  "lowswing" : "s",
    "w" : "w", "whiff" : "w", "webwhiff" : "w", "swingwhiff" : "w",
    "g" : "g", "getoverhere" : "g", "goh" : "g",
    "G" : "G", "getoverheretargetting" : "G", "goht" : "G",
    "u" : "u", "uppercut" : "u", "upper" : "u", "amazingcombo" : "u",
    "S" : "S", "symbiote" : "S", "symbiot" : "S",
    "+" : "+"
}

INITIAL_CONDITION_NAMES = {
    "t" : "t", "tagged" : "t", "tag" : "t",
    "a" : "a", "isairborne" : "a", "airborne" : "a", "air" : "a",
    "s" : "s", "hasswingoverhead" : "s",
    "j" : "j", "hasjumpoverhead" : "j",
    "A" : "A", "opponentairborne" : "A",
    "p" : "p", "haspunchb" : "p", "openpunchb" : "p",
    "k" : "k", "haskick" : "k", "openkick" : "k"
}



class Action:
    name = ""

    damage = 0
    procsTracer = False

    cancelTime = 0 # number of frames until the damage is dealt / until the non-damaging move is cancellable
    fullTime = 0 # number of frames until another action which doesn't cancel this one can begin
    deltaTime = 0

    cancelledBy = []
    moveStacks = {} # dict maps action which stacks over this move with the time taken to initiate the move stack

    def __init__(self, name, damage = 0, procsTracer=False, cancelTime=0, fullTime=0, cancelledBy = [], moveStacks={}):
        self.name = name
        self.damage = damage
        self.procsTracer = procsTracer
        self.cancelTime = cancelTime
        self.fullTime = fullTime
        self.deltaTime = fullTime - cancelTime
        self.cancelledBy = cancelledBy
        self.moveStacks = moveStacks



ACTIONS = {

    "j" : Action (
        name = "Jump"
    ),

    "l" : Action (
        name = "Land"
    ),

    "p" : Action (
        name = "Punch",
        damage = 25, 
        procsTracer = True, 
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["o", "t", "s", "w", "g", "G", "u", "S"],
        moveStacks = { 
            "o" : 0, # unique 3-hit stack - to be determined
            "t" : 0, # backflash - to be determined
            "G" : 0 # saporen tech - to be determined
        }
    ),

    "k" : Action (
        name = "Kick",
        damage = 40, 
        procsTracer = True,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined 
        cancelledBy = ["o", "t", "s", "w", "g", "G", "u", "S"],
        moveStacks = { 
            "o" : 0, # unique 3-hit stack - to be determined
            "t" : 0, # backflash - to be determined
            "G" : 0, # saporen tech - to be determined
            "u" : 0 # early cancel - to be determined
        }
    ),

    "o" : Action (
        name = "Overhead",
        damage = 50, 
        procsTracer = True, 
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["t", "s", "w", "g", "G", "u", "S"],
        moveStacks = {
            "G" : 0, # saporen tech - to be determined
            "u" : 0 # early cancel - to be determined
        }
    ),

    "t" : Action (
        name = "Tracer",
        damage = 30, 
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w", "g", "G", "u", "S"]
    ),

    "s" : Action (
        name = "Swing",
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["t", "g", "G", "u", "S"],
        moveStacks = {
            "G" : 0 # goht overhead preserve - to be determined
        }
    ),

    "w" : Action (
        name = "Whiff",
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["t", "g", "G", "u", "S"]
    ),

    "g" : Action (
        name = "Get Over Here",
        damage = 25,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w", "S"]
    ),

    "G" : Action (
        name = "Get Over Here Targetting",
        damage = 50,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w", "S"],
        moveStacks = {
            "G" : 0 # ffame stack - to be determined
        }
    ),

    "u" : Action (
        name = "Uppercut",
        damage = 55, 
        procsTracer = True,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w", "S"]
    ),

    "S" : Action (
        name = "Symbiote",
        damage = 50,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w"]
    )
}