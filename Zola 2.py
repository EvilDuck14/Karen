from Actions import *

class State:

    # Cooldowns - to avoid floating point innacuracy, using an ability takes charge equal to the number of frames it will take to recharge
    tracerCharge = TRACER_MAX_CHARGES * TRACER_CHARGE_TIME
    tracerCooldown = 0 # tracer firerate cannot be increased by weaving animation cancels
    tracerActiveTimer = 0 # frames remaining until tracer on opponent expires
    swingCharge = SWING_MAX_CHARGES * SWING_CHARGE_TIME
    uppercutCharge = UPPERCUT_MAX_CHARGES * UPPERCUT_CHARGE_TIME
    uppercutCooldown = 0 # frames remaining until uppercut is off cooldown
    gohCharge = GOH_MAX_CHARGES * GOH_CHARGE_TIME
    symbioteCharge = SYMBIOTE_MAX_CHARGES * SYMBIOTE_CHARGE_TIME

    # Airborne
    isAirborn = False
    opponentAirborn = False # grounded opponent forces landing after GOHT
    jumpCooldown = 0 # double jump is on a delay from initial jump

    # Overheads
    hasDoubleJump = False
    hasJumpOverhead = False
    hasSwingOverhead = False
    whiffTimer = 0 # frames until whiff ends, awarding jump overhead

    # Punch Combo
    punchSequence = 0 # 0 & 1 correspond to punches, 2 corresponds to kick
    punchSequenceTimer = 0 # frames remaining until punch sequence resets

    # Seasonal Boost
    damageMultiplier = 1.1

    # Tracking Stats
    damageDealt = 0
    timeTaken = 0
    


def calc(actionList):
    while len(actionList) > 0:
        nextAction = actionList[0]
        actionList = actionList[1:]