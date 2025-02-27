from actions import *

class State:

    # charges/cooldowns - to avoid floating point innacuracy, using an ability takes charge equal to the number of frames it will take to recharge
    charges = {
        "t" : ACTIONS["t"].maxChargeCost,
        "s" : ACTIONS["s"].maxChargeCost,
        "g" : ACTIONS["g"].maxChargeCost,
        "u" : ACTIONS["u"].maxChargeCost,
        "S" : ACTIONS["S"].maxChargeCost
    }
    cooldowns = {
        "j" : 0, # double jump is on a delay from initial jump
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0
    }
    tracerActiveTimer = 0 # frames remaining until tracer on opponent expires

    # airborne
    isAirborn = False
    opponentAirborn = False # grounded opponent forces landing after GOHT

    # overheads
    hasDoubleJump = False
    hasJumpOverhead = False
    hasSwingOverhead = False
    overheadOnSwingEnd = False # swing cooldown caused by tracer/uppercut doesn't award swing overhead

    # punch sequence
    punchSequence = 0 # 0 & 1 correspond to punches, 2 corresponds to kick
    punchSequenceTimer = 0 # frames remaining until punch sequence resets

    # seasonal boost
    damageMultiplier = 1.1

    # tracking metrics
    damageDealt = 0
    timeTaken = 0

    # calculating cancel/stack times
    currentAnimation = "none"

    # sequence output
    sequence = ""

    # initialise using inputString from evaluate function
    def __init__(self, inputString="", warnings=[]):
        
        # removes inputString whitespace
        inputString = "".join(inputString.split())

        # if inputString contains a '(' and a subsequent ')', then extract initial state info
        if "(" in inputString and ")" in inputString[inputString.find("("):]:
            conditions = inputString[inputString.find("(") + 1:inputString[inputString.find("(") + 1:].find(")")]

            # handles long-form by converting to list
            if "," in conditions:
                conditions = conditions.split(",")

            # unrecognised conditions
            for unknownCondition in [x for x in conditions if not x.lower() in INITIAL_CONDITION_NAMES]:
                warnings += [f"{unknownCondition} is not a recognised initial condition"]

            # converting conditions to single-letter names
            conditions = [x for x in conditions]
            
            # apply initial conditions to starting state
            if len(conditions) > 1:
                self.sequence += "("

            if "t" in conditions:
                self.tracerActiveTimer = TRACER_ACTIVE_TIME
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
                self.punchSequenceTimer = PUNCH_SEQUENCE_MAX_DELAY
                self.sequence += f"has {"kick" if "k" in conditions else "punch b"} ready, "

            if len(conditions) > 1:
                self.sequence = self.sequence[:-2] + ") " # removes trailing comma & space

    def incrementCooldowns(self, frames):
        
        # awards swing overhead on swing end
        if self.overheadOnSwingEnd and self.cooldowns["s"] <= frames:
            self.overheadOnSwingEnd = False
            self.hasSwingOverhead = self.isAirborn

        for key in self.charges.keys:
            self.charges[key] = min(self.charges[key] + frames, ACTIONS[key].maxChargeCost)
        
        for key in self.cooldowns.keys:
            self.cooldowns[key] = max(self.charges[key] - frames, 0)

        self.tracerActiveTimer = max(self.tracerActiveTimer, 0)

        self.punchSequenceTimer = max(self.punchSequenceTimer, 0)
        if self.punchSequenceTimer == 0:
            self.punchSequence = 0