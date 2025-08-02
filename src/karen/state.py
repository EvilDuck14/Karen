from karen.actions import *

class Charge:
    maxCharges = 0
    currentCharge = 0
    rechargeTime = 0
    cooldownTime = 0
    currentCooldownLevel = 0
    activeTimer = 0 # cooldown refresh= doesn't start until icon is no longer yellow

    def __init__(self, maxCharges, rechargeTime, cooldownTime = 0):
        self.maxCharges = maxCharges
        self.currentCharge = maxCharges * rechargeTime
        self.rechargeTime = rechargeTime
        self.cooldownTime = cooldownTime


class State:

    # charges/cooldowns - to avoid floating point innacuracy, using an ability takes charge equal to the number of frames it will take to recharge
    charges = {
        "t" : Charge(
            maxCharges = 5, 
            rechargeTime = 2.5 * 60,
            cooldownTime = 0.5 * 60
        ),
        "s" : Charge(
            maxCharges = 3, 
            rechargeTime = 6 * 60
        ),
        "g" : Charge(
            maxCharges = 1, 
            rechargeTime = 8 * 60
        ),
        "u" : Charge(
            maxCharges = 2, 
            rechargeTime = 6 * 60,
            cooldownTime = 2 * 60
        ),
        "b" : Charge(
            maxCharges = 1, 
            rechargeTime = 12 * 60
        )
    }
    tracerActiveTimer = 0 # frames remaining until tracer on opponent expires
    burnTracerActiveTimer = 0
    burnActiveTimer = 0 # timer for while burn tracer deals damage after procced
    gohtWaitTime = 0 # countdown from when tracer fired at unmarked target to when goht can be used

    # airborne
    isAirborn = False

    # overheads
    hasDoubleJump = True
    hasJumpOverhead = False
    hasSwingOverhead = False
    removeSwingOnEnd = False

    # punch sequence
    punchSequence = 0 # 0 & 1 correspond to punches, 2 corresponds to kick
    punchSequenceTimer = 0 # frames remaining until punch sequence resets

    # seasonal boost
    damageMultiplier = 1

    # tracking metrics
    damageDealt = 0
    timeTaken = 0

    # sequence output
    sequence = ""

    # initialise using inputString from evaluate function
    def __init__(self, inputString="", warnings=[]):
        
        # removes inputString whitespace
        inputString = "".join(inputString.split())

        # if inputString contains a '(' and a subsequent ')', then extract initial state info
        if "(" in inputString and ")" in inputString[inputString.find("("):]:
            conditions = inputString[inputString.find("(") + 1:]
            conditions = conditions[:conditions.find(")")]

            # handles long-form by converting to list
            if "," in conditions:
                conditions = conditions.split(",")

            # unrecognised conditions
            for unknownCondition in [x for x in conditions if not x.lower() in INITIAL_CONDITION_NAMES]:
                warnings += [f"{unknownCondition} is not a recognised initial condition"]

            # converting conditions to single-letter names
            conditions = [(INITIAL_CONDITION_NAMES[x] if x in INITIAL_CONDITION_NAMES else INITIAL_CONDITION_NAMES[x.lower()]) for x in conditions if x.lower() in INITIAL_CONDITION_NAMES]
            
            print(conditions)

            # apply initial conditions to starting state
            if len(conditions) > 0:
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

            if len(conditions) > 0:
                self.sequence = self.sequence[:-2] + ") " # removes trailing comma & space
        
        # infer initial state being airborne/having overhead
        else:
            pass # TO DO

    def incrementTime(self, frames, warnings):

        if frames <= 0:
            return
        
        self.timeTaken += frames

        if self.charges["s"].activeTimer > 0 and self.charges["s"].activeTimer <= frames:
            self.endSwing()

        for chargeType in self.charges:
            self.charges[chargeType].currentCharge = min(self.charges[chargeType] + frames, self.charges[chargeType].maxCharges * self.charges[chargeType].rechargeTime)
            self.charges[chargeType].cooldownTime = max(self.charges[chargeType] - frames, 0)

            if self.charges[chargeType].activeTimer > 0 and self.charges[chargeType].activeTimer <= frames:
                excessTime = frames - self.charges[chargeType].activeTimer
                self.endAction(self, chargeType)
                self.charges[chargeType].currentCharge -= excessTime

        if self.tracerActiveTimer > 0 and self.tracerActiveTimer <= frames:
           warnings += ["tracer expired without proc after " + self.sequence]
        if self.burnTracerActiveTimer > 0 and self.burnTracerActiveTimer <= frames:
           warnings += ["burn tracer expired without proc after " + self.sequence]    

        self.tracerActiveTimer = max(self.tracerActiveTimer - frames, 0)
        self.burnTracerActiveTimer = max(self.burnTracerActiveTimer - frames, 0)
        self.gohtWaitTime = max(self.gohtWaitTime - frames, 0)

        self.punchSequenceTimer = max(self.punchSequenceTimer, 0)
        if self.punchSequenceTimer == 0:
            self.punchSequence = 0

    def endAction(self, action): # ends current action and takes away the associated cooldown charge
        self.charges[action].activeTimer = 0
        if action != "s" or self.removeSwingOnEnd:
            self.charges[action].currentCharge -= self.charges[action].rechargeTime
        if action == "s":
            self.hasSwingOverhead |= self.isAirborn and self.hasDoubleJump
            self.hasJumpOverhead |= self.isAirborn and not self.hasDoubleJump