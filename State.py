from Actions import *



class State:

    # cooldowns - to avoid floating point innacuracy, using an ability takes charge equal to the number of frames it will take to recharge
    tracerCharge = TRACER_MAX_CHARGES * TRACER_CHARGE_TIME
    tracerCooldown = 0 # tracer firerate cannot be increased by weaving animation cancels
    tracerActiveTimer = 0 # frames remaining until tracer on opponent expires
    swingCharge = SWING_MAX_CHARGES * SWING_CHARGE_TIME
    uppercutCharge = UPPERCUT_MAX_CHARGES * UPPERCUT_CHARGE_TIME
    uppercutCooldown = 0 # frames remaining until uppercut is off cooldown
    gohCharge = GOH_MAX_CHARGES * GOH_CHARGE_TIME
    symbioteCharge = SYMBIOTE_MAX_CHARGES * SYMBIOTE_CHARGE_TIME

    # airborne
    isAirborn = False
    opponentAirborn = False # grounded opponent forces landing after GOHT
    jumpCooldown = 0 # double jump is on a delay from initial jump

    # overheads
    hasDoubleJump = False
    hasJumpOverhead = False
    hasSwingOverhead = False
    whiffTimer = 0 # frames until whiff ends, awarding jump overhead

    # punch sequence
    punchSequence = 0 # 0 & 1 correspond to punches, 2 corresponds to kick
    punchSequenceTimer = 0 # frames remaining until punch sequence resets

    # seasonal boost
    damageMultiplier = 1.1

    # tracking metrics
    damageDealt = 0
    timeTaken = 0

    # sequence output
    sequence = ""



def getInitialState(conditions):
    
    initialState = State()

    # removes input whitespace
    conditions = "".join(conditions.split())

    # if input contains a '(' and a subsequent ')', then extract initial state info
    if "(" in conditions and ")" in conditions[conditions.find("("):]:
        conditions = conditions[conditions.find("(") + 1:]
        conditions = conditions[:conditions.find(")")]

        # handles long-form by converting to list
        if "," in conditions:
            conditions = conditions.split(",")

        # unrecognised conditions
        for unknownCondition in [x for x in conditions if not x.lower() in INITIAL_CONDITION_NAMES]:
            print("Warning: " + unknownCondition + " is not a recognised initial condition")

        # converting conditions to single-letter names
        conditions = [x for x in conditions]
        
        # apply initial conditions to starting state
        if len(conditions) > 1:
            initialState.sequence += "("

        if "t" in conditions:
            initialState.tracerActiveTimer = TRACER_ACTIVE_TIME
            initialState.sequence += "tagged, "

        if "a" in conditions or "j" in conditions or "s" in conditions:
            initialState.isAirborn = True
            initialState.hasDoubleJump = not "j" in conditions
            initialState.sequence += "airborne, "

        if "j" in conditions:    
            initialState.hasJumpOverhead = True
            initialState.sequence += "has jump overhead, "

        if "s" in conditions:
            initialState.hasSwingOverhead = True
            initialState.sequence += "has swing overhead, "

        if "p" in conditions or "k" in conditions:
            initialState.punchSequence = 2 if "k" in conditions else 1
            initialState.punchSequenceTimer = PUNCH_SEQUENCE_MAX_DELAY
            initialState.sequence += "has " + ("kick" if "k" in conditions else "punch b") + " ready, "

        if len(conditions) > 1:
            initialState.sequence = initialState.sequence[:-2] + ") " # removes trailing comma & space
            
    return initialState