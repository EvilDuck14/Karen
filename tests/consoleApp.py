from karen.evaluate import evaluate
from karen.getCombo import *

while True:

    inputString = input(">> ") + " " # space added so that commands with no arguments are easily handled
    while len(inputString) > 0 and inputString[0] in " !":
        inputString = inputString[1:]
    print("")

    if len(inputString) > 4 and inputString[:5] == "help ":
        print("!eval [combo]: evaluates the given combo")
        print("!exit : closes the terminal")

    elif len(inputString) > 4 and inputString[:5] == "eval ":
        evaluate(inputString[5:], simpleMode=True).printToConsole()

    elif len(inputString) > 5 and inputString[:6] == "evala ":
        evaluate(inputString[6:]).printToConsole()

    elif len(inputString) > 5 and inputString[:6] == "evaln ":
        evaluate(inputString[6:], printWarnings=False).printToConsole()

    elif len(inputString) > 5 and inputString[:6] == "combo ":
        getCombo(inputString[6:]).printToConsole()

    elif len(inputString) > 5 and inputString[:7] == "combos ":
        listCombos(inputString[7:]).printToConsole()

    elif len(inputString) > 4 and inputString[:5] == "exit ":
        break

    else:
        print("Command not recognised, use '!help' to see a list of commands")

    print("\n")