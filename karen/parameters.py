PARAMETER_NAMES = {
    "" : "input", "input" : "input", "i" : "input",
    "a" : "advanced", "advanced" : "advanced",
    "n" : "noWarnings", "nowarnings" : "noWarnings", "nw" : "noWarnings", "nowarn" : "nowarnings",
}

class Parameters:
    advanced = False
    noWarnings = False

def splitParameters(inputString, warnings):
    while "---" in inputString:
        inputString = inputString.replace("---", "--")
    inputString = "-- " + inputString

    sequence = ""
    params = Parameters()

    for parameterString in inputString.split("--"):
        parameter = parameterString.split(" ")[0].lower()
        value = " ".join(parameterString.split(" ")[1:])

        if not parameter in PARAMETER_NAMES:
            warnings += [f"{parameter} is not a recognised parameter"]
            sequence += value
            continue

        if PARAMETER_NAMES[parameter] == "input":
            sequence += str(value)

        if PARAMETER_NAMES[parameter] == "advanced":
            params.advanced = True
            sequence += value # this parameter takes no arguments - parse as regular input

        if PARAMETER_NAMES[parameter] == "noWarnings":
            params.noWarnings = True
            sequence += value # this parameter takes no arguments - parse as regular input

    return sequence, params