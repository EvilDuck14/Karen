from karen.state import State
from karen.combo import getComboSequence, addAction

def evaluate(inputString):
    warnings = []

    state = State(inputString, warnings)
    comboSequence = getComboSequence(inputString, warnings)

    for action in comboSequence:
        addAction(state, action, warnings)

    warningsCollected = f"```\n{"\n".join(["WARNING: " + x for x in warnings])}\n```"
    output = (warningsCollected if len(warnings) > 0 else "") + f"\n> **{state.sequence}**\n\n**Time:** {round(state.timeTaken / 60, 3)} seconds ({state.timeTaken} frames)\n**Damage:** {state.damageDealt}"
    return output