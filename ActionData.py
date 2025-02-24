JUMP = 0
LAND = 1
PUNCH = 2
KICK = 3
OVERHEAD = 4
TRACER = 5
SWING = 6
WHIFF = 7
GOH = 8
GOHT = 9
UPPERCUT = 10
SYMBIOTE = 11



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



NAMES = {
    "j" : JUMP,
    "l" : LAND,
    "p" : PUNCH,
    "k" : KICK,
    "o" : OVERHEAD,
    "t" : TRACER,
    "s" : SWING,
    "w" : WHIFF,
    "g" : GOH,
    "G" : GOHT,
    "u" : UPPERCUT,
    "S" : SYMBIOTE
}

ALT_NAMES = {
    "jump" : JUMP,
    "dj" : JUMP,
    "land" : LAND,
    "punch" : PUNCH,
    "puncha" : PUNCH, 
    "punchb" : PUNCH,
    "meleepunch" : PUNCH, 
    "meleepuncha" : PUNCH, 
    "meleepunchb" : PUNCH,
    "kick" : KICK, 
    "meleekick" : KICK,
    "overheadslam" : OVERHEAD, 
    "overhead" : OVERHEAD, 
    "oh" : OVERHEAD, 
    "meleeoverhead" : OVERHEAD, 
    "slam" : OVERHEAD,
    "tracer" : TRACER, 
    "webtracer" : TRACER, 
    "cluster" : TRACER, 
    "webcluster" : TRACER,
    "swing" : SWING, 
    "webswing" : SWING, 
    "highswing" : SWING, 
    "lowswing" : SWING,
    "whiff" : WHIFF, 
    "webwhiff" : WHIFF, 
    "swingwhiff" : WHIFF,
    "getoverhere" : GOH, 
    "goh" : GOH,
    "getoverheretargetting" : GOHT, 
    "goht" : GOHT,
    "uppercut" : UPPERCUT, 
    "upper" : UPPERCUT, 
    "amazingcombo" : UPPERCUT,
    "symbiote" : SYMBIOTE, 
    "symbiot" : SYMBIOTE
}



INITIAL_CONDITION_NAMES = {
    "tagged" : "t",
    "tag" : "t",
    "isairborne" : "a",
    "airborne" : "a",
    "air" : "a",
    "hasswingoverhead" : "s",
    "hasjumpoverhead" : "j",
    "opponentairborne" : "A",
    "openpunchb" : "p",
    "openkick" : "k"
}