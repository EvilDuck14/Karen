from Actions import *
from State import *



def getComboSequence(sequence):

    # removes whitespace
    sequence = "".join(sequence.split())

    # removes initial conditions from input string
    if "(" in sequence and ")" in sequence[sequence.find("("):]:
        sequence = sequence[:sequence.find("(")] + sequence[sequence[sequence.find("("):].find(")") + 1:]

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



def evaluate(input):
    state = getInitialState(input)
    comboSequence = getComboSequence(input)