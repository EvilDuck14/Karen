from state import State
from combo import getComboSequence, addAction

def evaluate(inputString):
    warnings = []

    state = State(inputString, warnings)
    comboSequence = getComboSequence(inputString, warnings)

    for action in comboSequence:
        addAction(state, action)

    output = "\n".join(["WARNING: " + x for x in warnings]) + f"\n\n{state.sequence}\n\nTime: {round(state.timeTaken / 60, 3)} seconds ({state.timeTaken} frames)\nDamage: {state.damageDealt}"
    return output