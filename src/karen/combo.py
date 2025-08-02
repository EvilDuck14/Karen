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

def addAction(state=State(), action="", warnings=[]):

    if not ("G+u" in ACTIONS):
        loadMoveStacks()

    # awaits cooldowns
    if action in state.charges:
        state.incrementCooldowns(state.charges[action].activeTimer)
        state.incrementCooldowns(state.charges[action].cooldownTime)
        state.incrementCooldowns(max(0, 1 - state.charges[action].currentCharges))

    # movestack cooldown awaiting calculations
    if "+" in action:
        pass
    


    state.sequence += "> " + {ACTIONS[action].name}