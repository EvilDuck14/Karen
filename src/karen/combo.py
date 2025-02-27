from actions import *
from state import State

def getComboSequence(inputString="", warnings=[]):

    # removes whitespace
    inputString = "".join(inputString.split())

    # removes initial conditions from inputString string
    sequence = inputString
    if "(" in inputString and ")" in inputString[inputString.find("("):]:
        sequence = inputString[:inputString.find("(")] + inputString[inputString[inputString.find("("):].find(")") + 1:]

    # handles long-form by converting to list
    if ">" in sequence:
        sequence = sequence.replace("+", ">+>").split(">") # make sure '+' characters are split out as their own entries
        sequence = [x for x in sequence if x != ""] # removes empty entries caused by double '>' characters
    
    # unrecognised conditions
    for unknownAction in [x for x in sequence if not x.lower() in ACTION_NAMES]:
        print(f"Warning: {unknownAction} is not a recognised action")
    warnings += [unknownAction + " is not a recognised action" for unknownAction in sequence if not unknownAction.lower() in ACTION_NAMES]
    
    # converts to a list of correctly formatted keys in ACTION_NAMES
    sequence = [(x if x in ACTION_NAMES else x.lower()) for x in sequence if (x.lower() in ACTION_NAMES)] 

    # folds movestack indicators into actions
    for i in len(sequence):
        if i > 0 and sequence[i-1] == "+":
            sequence[i] = "+" + sequence[i]
    sequence = [x for x in sequence if x != "+"]

    return sequence

def addAction(state=State(), actionName="", warnings=[]):

    # checks movestack indicator
    moveStack = actionName[0] == "+"
    if moveStack:
        actionName = actionName[1:]

    # using the single shorthand name for most operations
    action = ACTION_NAMES[actionName]

    # bad movestack flag
    if moveStack and not action in ACTIONS[state.currentAnimation].moveStacks.keys:
        warnings += [f"attempted nonexistant movestack {state.currentAnimation}+{action}"]
        moveStack = False

    # measures the time between the cancel time of the previous action and the start time of the current one
    # the first reason this could be nonzero is if the current animation isn't simply cancelled
    waitTime = 0
    if moveStack:
        waitTime = ACTIONS[state.currentAnimation].cancelTime - ACTIONS[state.currentAnimation].moveStacks[action] #negative number
    elif not action in ACTIONS[state.currentAnimation].cancelledBy:
        waitTime = ACTIONS[state.currentAnimation].deltaTime   

    # it could also happen if the action being added is on cooldown
    actionEquivalent = ACTION_EQUIVALENCE[action]
    if state.cooldowns[actionEquivalent] > max(0, waitTime) and not moveStack: # movestack cooldown detetion is done on the previous action
        waitTime = state.cooldowns[actionEquivalent]
    if state.charges[action] < ACTIONS[action].chargeTime:
        waitTime = max(waitTime, ACTIONS[action].chargeTime - state.charges[action])
        if (moveStack):
            warnings += [f"attempted to movestack {state.currentAnimation}+{action} while {action} is on cooldown"]

    # TO DO: if next move is a movestack which will still be on cooldown, throw a warning