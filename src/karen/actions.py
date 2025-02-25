import data

INITIAL_CONDITION_NAMES = {
    "t" : "t", "tagged" : "t", "tag" : "t",
    "a" : "a", "isairborne" : "a", "airborne" : "a", "air" : "a",
    "s" : "s", "hasswingoverhead" : "s",
    "j" : "j", "hasjumpoverhead" : "j",
    "A" : "A", "opponentairborne" : "A",
    "p" : "p", "haspunchb" : "p", "openpunchb" : "p",
    "k" : "k", "haskick" : "k", "openkick" : "k"
}

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
        damage = data.PUNCH_DAMAGE, 
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
        damage = data.KICK_DAMAGE, 
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
        damage = data.OVERHEAD_DAMAGE, 
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
        damage = data.TRACER_DAMAGE, 
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
        damage = data.GOH_DAMAGE,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w", "S"]
    ),

    "G" : Action (
        name = "Get Over Here Targetting",
        damage = data.GOHT_DAMAGE,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w", "S"],
        moveStacks = {
            "G" : 0 # ffame stack - to be determined
        }
    ),

    "u" : Action (
        name = "Uppercut",
        damage = data.UPPERCUT_DAMAGE, 
        procsTracer = True,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w", "S"]
    ),

    "S" : Action (
        name = "Symbiote",
        damage = data.SYMBIOTE_DAMAGE,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = ["s", "w"]
    )
}