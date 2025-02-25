from actions import ACTION_NAMES

def getComboSequence(input):

    # removes whitespace
    input = "".join(input.split())

    # removes initial conditions from input string
    sequence = input
    if "(" in input and ")" in input[input.find("("):]:
        sequence = input[:input.find("(")] + input[input[input.find("("):].find(")") + 1:]

    # handles long-form by converting to list
    if ">" in sequence:
        sequence = sequence.replace("+", ">+>").split(">") # make sure '+' characters are split out as their own entries
        sequence = [x for x in sequence if x != ""] # removes empty entries caused by double '>' characters
    
    # unrecognised conditions
    for unknownAction in [x for x in sequence if not x.lower() in ACTION_NAMES]:
        print("Warning: " + unknownAction + " is not a recognised action")
    
    # converts to a list of correctly formatted keys in ACTION_NAMES
    sequence = [(x if x in ACTION_NAMES else x.lower()) for x in sequence if (x.lower() in ACTION_NAMES)] 

    return sequence