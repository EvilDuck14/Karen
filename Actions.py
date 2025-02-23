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



class Action:
    damage = 0
    procsTracer = False

    damageTime = 0
    fullTime = 0
    deltaTime = 0

    cancelledBy = []
    moveStacks = {}

    def __init__(self, damage=0, procsTracer=False, fullTime=0, cancelledBy=[], damageTime=0, moveStacks={}):
        self.damage = damage
        self.procsTracer = procsTracer
        self.damageTime = damageTime
        self.fullTime = fullTime
        self.deltaTime = fullTime - damageTime
        self.cancelledBy = cancelledBy
        self.moveStacks = moveStacks



ACTIONS = {
    JUMP : Action(),
    LAND : Action(),
    PUNCH : Action(damage=25, procsTracer=True),
    KICK : Action(damage=40, procsTracer=True),
    OVERHEAD : Action(damage=50, procsTracer=True),
    TRACER : Action(damage=30),
    SWING : Action(),
    WHIFF : Action(),
    GOH : Action(damage=25),
    GOHT : Action(damage=50),
    UPPERCUT : Action(damage=55, procsTracer=True),
    SYMBIOTE : Action(damage=50)
}