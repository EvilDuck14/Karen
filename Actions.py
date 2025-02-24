from ActionData import *

class Action:
    damage = 0
    procsTracer = False

    cancelTime = 0 # number of frames until the damage is dealt / until the non-damaging move is cancellable
    fullTime = 0 # number of frames until another action which doesn't cancel this one can begin
    deltaTime = 0

    cancelledBy = []
    moveStacks = {} # dict maps action which stacks over this move with the time taken to initiate the move stack

    def __init__(self, damage = 0, procsTracer=False, cancelTime=0, fullTime=0, cancelledBy = [], moveStacks={}):
        self.damage = damage
        self.procsTracer = procsTracer
        self.cancelTime = cancelTime
        self.fullTime = fullTime
        self.deltaTime = fullTime - cancelTime
        self.cancelledBy = cancelledBy
        self.moveStacks = moveStacks



ACTIONS = {

    JUMP : Action(),

    LAND : Action(),

    PUNCH : Action(
        damage = 25, 
        procsTracer = True, 
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [OVERHEAD, TRACER, SWING, WHIFF, GOH, GOHT, UPPERCUT, SYMBIOTE],
        moveStacks = { 
            OVERHEAD : 0, # unique 3-hit stack - to be determined
            TRACER : 0, # backflash - to be determined
            GOHT : 0 # saporen tech - to be determined
        }
    ),

    KICK : Action(
        damage = 40, 
        procsTracer = True,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined 
        cancelledBy = [OVERHEAD, TRACER, SWING, WHIFF, GOH, GOHT, UPPERCUT, SYMBIOTE],
        moveStacks = { 
            OVERHEAD : 0, # unique 3-hit stack - to be determined
            TRACER : 0, # backflash - to be determined
            GOHT : 0, # saporen tech - to be determined
            UPPERCUT : 0 # early cancel - to be determined
        }
    ),

    OVERHEAD : Action(
        damage = 50, 
        procsTracer = True, 
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [TRACER, SWING, WHIFF, GOH, GOHT, UPPERCUT, SYMBIOTE],
        moveStacks = {
            GOHT : 0, # saporen tech - to be determined
            UPPERCUT : 0 # early cancel - to be determined
        }
    ),

    TRACER : Action(
        damage = 30, 
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [SWING, WHIFF, GOH, GOHT, UPPERCUT, SYMBIOTE]
    ),

    SWING : Action(
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [TRACER, GOH, GOHT, UPPERCUT, SYMBIOTE],
        moveStacks = {
            GOHT : 0 # goht overhead preserve - to be determined
        }
    ),

    WHIFF : Action(
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [TRACER, GOH, GOHT, UPPERCUT, SYMBIOTE]
    ),

    GOH : Action(
        damage = 25,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [SWING, WHIFF, SYMBIOTE]
    ),

    GOHT : Action(
        damage = 50,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [SWING, WHIFF, SYMBIOTE],
        moveStacks = {
            GOHT : 0 # ffame stack - to be determined
        }
    ),

    UPPERCUT : Action(
        damage = 55, 
        procsTracer = True,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [SWING, WHIFF, SYMBIOTE]
    ),

    SYMBIOTE : Action(
        damage = 50,
        cancelTime = 0, # to be determined
        fullTime = 0, # to be determined
        cancelledBy = [SWING, WHIFF]
    )
}