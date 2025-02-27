from actions import ACTION_NAMES

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
    warnings += [unknownAction + " is not a recognised action" for unknownAction in sequence if not unknownAction.lower() in ACTION_NAMES]
    
    # converts to a list of correctly formatted keys in ACTION_NAMES
    sequence = [(x if x in ACTION_NAMES else x.lower()) for x in sequence if (x.lower() in ACTION_NAMES)] 

    return sequence