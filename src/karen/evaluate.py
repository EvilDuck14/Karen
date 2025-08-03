from karen.state import State
from karen.combo import getComboSequence, addAction
from karen.classify import classify
from math import floor
from karen.actions import *

def evaluate(inputString):
    warnings = []

    state = State()
    comboSequence = getComboSequence(inputString, warnings) + [""]

    # infer initial state being airborne/having overhead
    state.inferInitialState(comboSequence, warnings)

    for i in range(len(comboSequence) - 1):
        nextAction = [j for j in comboSequence[i+1:] if not j in ["j", "l"]][0]
        addAction(state, comboSequence[i], nextAction, warnings)

    # TO DO: checks for continued burn tracer damage after final action
    burnTracerBonusDamage = ""
    if state.burnActiveTimer > 12:
        burnTracerBonusDamage = "(plus " + str(int(floor((state.burnActiveTimer - 1) / 12) * BURN_TRACER_DPS / 5)) +" burn over time)"

    comboName = classify("".join(comboSequence))

    warningsCollected = f"```\n{"\n".join(["WARNING: " + x for x in warnings])}\n```"
    output = f"**{comboName}**\n> {state.sequence}\n**Time:** {round(state.timeTaken / 60, 3)} seconds ({state.timeTaken} frames)\n**Damage:** {state.damageDealt} {burnTracerBonusDamage}" + ("\n" + warningsCollected if len(warnings) > 0 else "")
    return output