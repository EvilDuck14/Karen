from karen.evaluate import evaluate
from karen.output import Output
from karen.parameters import Parameters
from copy import deepcopy

def compare(inputString, params=Parameters(), warnings=[]):
    if not "," in inputString:
        return Output(error="Comparison command must include at least one comma to separate combos")
    
    if params.breakdown:
        warnings.append("Comparison command does not support breakdown parameter")

    proxyParams = deepcopy(params)
    proxyParams.compareTime = True
    proxyParams.compareTimeFromDamage = True
    proxyParams.compareDamage = True

    comboStrings = inputString.split(",")
    outputs = [evaluate(comboString, proxyParams, warnings) for comboString in comboStrings]
    
    outputCombo = [f"{i+1}. {outputs[i].combo}" for i in range(len(outputs))]

    outputDescriptions = [output.description.split("\n") for output in outputs]
    for i in range(len(outputDescriptions)):
        if len(outputDescriptions[i]) == 2:
            outputDescriptions[i] = [outputDescriptions[i][0], "**Time From Damage:** 0 seconds (0 frames)", outputDescriptions[i][1]]

    comboTimes = [int(description[0].split(" ")[3][1:].split("-")[0]) for description in outputDescriptions]
    comboTimesFromDamage = [int(description[1].split(" ")[5][1:].split("-")[0]) for description in outputDescriptions]
    comboDamages = [float(description[2].split(" ")[1].split("-")[0]) for description in outputDescriptions]
    comboDamages = [int(x) if x - int(x) == 0 else x for x in comboDamages]
    comboDPSs = [int(comboDamages[i] / max(1/60, comboTimesFromDamage[i]/60)) for i in range(len(comboDamages))]

    fastestTime = [i+1 for i in range(len(comboTimes)) if comboTimes[i] == min(comboTimes)]
    fastestTimeFromDamage = [i+1 for i in range(len(comboTimesFromDamage)) if comboTimesFromDamage[i] == min(comboTimesFromDamage)]
    mostDamage = [i+1 for i in range(len(comboDamages)) if comboDamages[i] == max(comboDamages)]
    mostDPS = [i+1 for i in range(len(comboDPSs)) if comboDPSs[i] == max(comboDPSs)]

    description = []

    if params.compareTime:
        description.append(f"\n**Time:** Combo{"s" if len(fastestTime) > 1 else ""} {" & ".join([str(x) for x in fastestTime])}\n`{" vs ".join([f"{"🟢" if i+1 in fastestTime else "🟥"} {comboTimes[i]}f" for i in range(len(comboTimes))])}`")
    
    if params.compareTimeFromDamage:
        description.append(f"\n**Time From Damage:** Combo{"s" if len(fastestTimeFromDamage) > 1 else ""} {" & ".join([str(x) for x in fastestTimeFromDamage])}\n`{" vs ".join([f"{"🟢" if i+1 in fastestTimeFromDamage else "🟥"} {comboTimesFromDamage[i]}f" for i in range(len(comboTimesFromDamage))])}`")
    
    if params.compareDamage:
        description.append(f"\n**Damage:** Combo{"s" if len(mostDamage) > 1 else ""} {" & ".join([str(x) for x in mostDamage])}\n`{" vs ".join([f"{"🟢" if i+1 in mostDamage else "🟥"} {comboDamages[i]}" for i in range(len(comboDamages))])}`")
    
    if params.compareDPS:
        description.append(f"\n**DPS:** Combo{"s" if len(mostDPS) > 1 else ""} {" & ".join([str(x) for x in mostDPS])}\n`{" vs ".join([f"{"🟢" if i+1 in mostDPS else "🟥"} {comboDPSs[i]}" for i in range(len(comboDPSs))])}`")

    description = "\n".join(description)

    if params.noWarnings:
        warnings = []

    return Output(title="Combo Comparison", combo=outputCombo, description=description, warnings=warnings)