from karen.actions import *
from karen.state import State

def getComboSequence(inputString="", warnings=[]):

    if not ("G+u" in ACTIONS):
        loadMoveStacks()

    # removes whitespace
    inputString = "".join(inputString.split())

    # removes initial conditions from inputString string
    sequence = inputString
    if "(" in inputString and ")" in inputString[inputString.find("("):]:
        sequence = inputString[:inputString.find("(")] + inputString[inputString[inputString.find("("):].find(")") + inputString.find("(") + 1:]

    # infers whether the combo is long form or letter notation
    longForm = ">" in sequence
    if not longForm:
        for char in sequence:
            if not (char in ACTION_NAMES):
                for name in ACTION_NAMES:
                    if len(name) > 1 and name in sequence:
                        longForm = True
                        break
                break

    # handles long-form by converting to list
    if longForm:
        sequence = sequence.replace("+", ">+>").split(">") # make sure '+' characters are split out as their own entries
        sequence = [x for x in sequence if x != ""] # removes empty entries caused by double '>' characters
    
    # unrecognised conditions
    for unknownAction in [x for x in sequence if not x.lower() in ACTION_NAMES]:
        print(f"Warning: {unknownAction} is not a recognised action")
    warnings += [unknownAction + " is not a recognised action" for unknownAction in sequence if not unknownAction.lower() in ACTION_NAMES]
    
    # converts to a list of correctly formatted keys in ACTION_NAMES
    sequence = [(ACTION_NAMES[x] if x in ACTION_NAMES else x.lower()) for x in sequence if (x.lower() in ACTION_NAMES)] 
    sequence = list("".join(sequence))

    # folds movestack indicators into actions
    foldSequence = []
    for i in range(len(sequence)):
        if len(foldSequence) > 0 and sequence[i-1] == "+":
            if foldSequence[-1] + "+" + sequence[i] in ACTIONS:
                foldSequence[-1] += "+" + sequence[i]
                continue
            else:
                warnings += [foldSequence[-1] + "+" + sequence[i] + " is not a regocnised movestack"]
        if sequence[i] != "+":
            foldSequence.append(sequence[i])

    return foldSequence

def addAction(state=State(), action="", nextAction="", warnings=[]):

    if not ("G+u" in ACTIONS):
        loadMoveStacks()

    # awaits required cooldowns
    for a in ACTIONS[action].awaitCharges:
        state.incrementTime(state.charges[a].activeTimer, warnings)
        state.incrementTime(state.charges[a].cooldownTime - ACTIONS[action].awaitCharges[a], warnings)
        state.incrementTime(max(0, state.charges[a].rechargeTime - state.charges[a].currentCharge) - ACTIONS[action].awaitCharges[a], warnings)

    # awaits tracer register for GOHT
    if "g" in ACTIONS[action].awaitCharges:
        state.incrementTime(state.gohtWaitTime - ACTIONS[action].awaitCharges["g"], warnings)

    # awaits kick expiration for punch
    if "p" in action and state.punchSequence == 2:
        state.incrementTime(state.punchSequenceTimer, warnings)

    # awaits whiff end for overhead
    if "o" in action and (not state.hasJumpOverhead) and (not state.hasSwingOverhead) and state.charges["s"].activeTimer > 0:
        state.incrementTime(state.charges["s"].activeTimer, warnings)

    if "k" in action and state.punchSequence < 2:
        warnings += ["uses impossible kick after " + state.sequence]
    
    if "G" in action and state.tracerActiveTimer < ACTIONS[action].awaitCharges["g"]:
        warnings += ["uses GOHT on nonxistent or expired tracer after " + state.sequence]

    
    # processes overhead logic
    if "o" in action and (not state.hasSwingOverhead) and (not state.hasJumpOverhead):
        warnings += ["uses impossible overhead after " + state.sequence]

    if action == "l":
        state.hasDoubleJump = True
        state.hasSwingOverhead = False
        state.hasJumpOverhead = False
   
    if action == "j" and state.isAirborn:
        if not state.hasDoubleJump: 
            warnings += ["uses impossible double jump after " + state.sequence]
        state.hasDoubleJump = False
        state.hasJumpOverhead = True

    elif action == "j" or "u" in action:
        state.isAirborn = True

    if action in ["o", "G", "G+u", "p+G", "k+G", "p+G+u", "k+G+u", "p+G+u", "k+G+u", "o+t", "p+o", "k+o"]:
        if state.hasSwingOverhead:
            state.hasSwingOverhead = False
        else:
            state.hasJumpOverhead = False
    if action in ["o+G", "o+G+u"]:
        state.hasSwingOverhead = False
        state.hasJumpOverhead = False
    if action == "u+w+G":
        state.hasSwingOverhead = True
        state.hasJumpOverhead = False

    if action in ["s", "b"] or "u" in action:
        state.hasDoubleJump = True
        state.hasJumpOverhead = False
    
    if action == "b":
        state.hasSwingOverhead = True

    # ends current cancellable actions
    for cancelCharge in ACTIONS[action].endActivations:
        if state.charges[cancelCharge].activeTimer > 0:
            state.endAction(cancelCharge)


    # activating actions/consuming cooldowns
    # TO DO
    if action == "s":
        state.removeSwingOnEnd = True
    if "w" in action:
        state.removeSwingOnEnd = False
        

    # adding tracer tags
    if action in ["t", "b"] and state.tracerActiveTimer == 0 and state.burnTracerActiveTimer == 0:
        state.gohtWaitTime = TRACER_MARK_TIME
    if action == "t":
        state.tracerActiveTimer = TRACER_ACTIVE_TIME + TRACER_MARK_TIME
    if action == "b":
        state.burnTracerActiveTimer = BURN_TRACER_ACTIVE_TIME + TRACER_MARK_TIME       

    # proccing tracers
    if ACTIONS[action].procsTracer and state.tracerActiveTimer >= ACTIONS[action].procTime or action in ["p+t", "k+t", "o+t"]:
        state.damageDealt += TRACER_PROC_DAMAGE
        state.tracerActiveTimer = 0
    if ACTIONS[action].procsTracer and state.burnTracerActiveTimer >= ACTIONS[action].procTime:
        state.burnActiveTimer = BURN_TRACER_BURN_TIME
        state.burnTracerActiveTimer = 0

    state.damageDealt += ACTIONS[action].damage
    state.incrementTime(ACTIONS[action].damageTime if nextAction == "" else ACTIONS[action].cancelTimes[nextAction], warnings)

    state.sequence += ("" if state.sequence == "" else " > ") + {ACTIONS[action].name}