from karen.state import State
from karen.combo import getComboSequence, addAction

def evaluate(inputString):
    warnings = []

    state = State(inputString, warnings)
    comboSequence = getComboSequence(inputString, warnings)

    # TO DO: infers whether target started airborne and/or with overheads

    for i in range(len(comboSequence) - 1):
        addAction(state, comboSequence[i], comboSequence[i + 1], warnings)
    addAction(state, comboSequence[-1], warnings)

    # TO DO: checks for continued burn tracer damage after final action
    if state.burnActiveTimer > 0:
        pass

    warningsCollected = f"```\n{"\n".join(["WARNING: " + x for x in warnings])}\n```"
    output = (warningsCollected if len(warnings) > 0 else "") + f"\n> **{state.sequence}**\n\n**Time:** {round(state.timeTaken / 60, 3)} seconds ({state.timeTaken} frames)\n**Damage:** {state.damageDealt}"
    return output