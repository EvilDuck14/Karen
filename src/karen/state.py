import data
from actions import INITIAL_CONDITION_NAMES

class State:

    # cooldowns - to avoid floating point innacuracy, using an ability takes charge equal to the number of frames it will take to recharge
    tracerCharge = data.TRACER_MAX_CHARGES * data.TRACER_CHARGE_TIME
    tracerCooldown = 0 # tracer firerate cannot be increased by weaving animation cancels
    tracerActiveTimer = 0 # frames remaining until tracer on opponent expires
    swingCharge = data.SWING_MAX_CHARGES * data.SWING_CHARGE_TIME
    uppercutCharge = data.UPPERCUT_MAX_CHARGES * data.UPPERCUT_CHARGE_TIME
    uppercutCooldown = 0 # frames remaining until uppercut is off cooldown
    gohCharge = data.GOH_MAX_CHARGES * data.GOH_CHARGE_TIME
    symbioteCharge = data.SYMBIOTE_MAX_CHARGES * data.SYMBIOTE_CHARGE_TIME

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

    # initialise using input from evaluate function
    def __init__(self, input):
        
        # removes input whitespace
        input = "".join(input.split())

        # if input contains a '(' and a subsequent ')', then extract initial state info
        if "(" in input and ")" in input[input.find("("):]:
            conditions = input[input.find("(") + 1:input[input.find("(") + 1:].find(")")]

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
                self.sequence += "("

            if "t" in conditions:
                self.tracerActiveTimer = data.TRACER_ACTIVE_TIME
                self.sequence += "tagged, "

            if "a" in conditions or "j" in conditions or "s" in conditions:
                self.isAirborn = True
                self.hasDoubleJump = not "j" in conditions
                self.sequence += "airborne, "

            if "j" in conditions:    
                self.hasJumpOverhead = True
                self.sequence += "has jump overhead, "

            if "s" in conditions:
                self.hasSwingOverhead = True
                self.sequence += "has swing overhead, "

            if "p" in conditions or "k" in conditions:
                self.punchSequence = 2 if "k" in conditions else 1
                self.punchSequenceTimer = data.PUNCH_SEQUENCE_MAX_DELAY
                self.sequence += "has " + ("kick" if "k" in conditions else "punch b") + " ready, "

            if len(conditions) > 1:
                self.sequence = self.sequence[:-2] + ") " # removes trailing comma & space