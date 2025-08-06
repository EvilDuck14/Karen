from karen.evaluate import evaluate
from karen.classify import CLASSIFICATIONS

COMBO_NAMES = {
    "bnb" : "Bread & Butter (BnB)",
    "bnbplink" : "BnB Long Plink",
    "fishingcombo" : "Fishing Combo / Sekkombo",
    "fish" : "Fishing Combo / Sekkombo",
    "sekkombo" : "Fishing Combo / Sekkombo",
    "sekombo" : "Fishing Combo / Sekkombo",
    "gripkickrip" : "Grip Kick Rip (GKR)",
    "gkr" : "Grip Kick Rip (GKR)",
    "ohburst" : "Overhead Burst",
    "fantastic" : "Fantastic Killer",
    "sapstack" : "Saporen FFAmestack",
    "agnikai" : "Agni-Kai Yo-Yo",
    "bald" : "Bald Slam",

    "bnbburn" : "Burn BnB / Fadeaway",
    "burnb&b" : "Burn BnB / Fadeaway",
    "burnbandb" : "Burn BnB / Fadeaway",
    "burnbreadnbutter" : "Burn BnB / Fadeaway",
    "burnbread&butter" : "Burn BnB / Fadeaway",
    "burnbreadandbutter" : "Burn BnB / Fadeaway",
    "fadeaway" : "Burn BnB / Fadeaway",
    "burnohburst" : "Burn Overhead Burst",
    "burnoverhead" : "Burn Overhead Burst",
    "burnoh" : "Burn Overhead Burst",
    "friedfish" : "Fried Fish / Firehook",
    "fried" : "Fried Fish / Firehook",
    "burnsekkombo" : "Fried Fish / Firehook",
    "burnsekombo" : "Fried Fish / Firehook",
    "firehook" : "Fried Fish / Firehook",
    "innout" : "In And Out",
    "in&out" : "In And Out"
}

def loadComboNames():
    for sequence in CLASSIFICATIONS:
        filterName = CLASSIFICATIONS[sequence].replace(" ", "").replace("-", "").lower()
        COMBO_NAMES[filterName] = CLASSIFICATIONS[sequence]

    for name in COMBO_NAMES.copy():
        if len(name) > 3 and name[:3] == "bnb":
            COMBO_NAMES["b&b" + name[3:]] = COMBO_NAMES[name]
            COMBO_NAMES["bandb" + name[3:]] = COMBO_NAMES[name]
            COMBO_NAMES["breadnbutter" + name[3:]] = COMBO_NAMES[name]
            COMBO_NAMES["bread&butter" + name[3:]] = COMBO_NAMES[name]
            COMBO_NAMES["breadandbutter" + name[3:]] = COMBO_NAMES[name]

    for name in COMBO_NAMES.copy(): 
        if len(name) > 5 and name[-5:] == "combo":
            COMBO_NAMES[name[:-5]] = COMBO_NAMES[name]
        else:
            COMBO_NAMES[name + "combo"] = COMBO_NAMES[name]


def getCombo(name):
    if not "b&b" in COMBO_NAMES:
        loadComboNames()

    filterName = name.replace(" ", "").replace("-", "").lower()

    if not filterName in COMBO_NAMES:
        return "```\nERROR: Combo not found\n```"
    
    for sequence in CLASSIFICATIONS:
        if CLASSIFICATIONS[sequence] == COMBO_NAMES[filterName]:
            output = "\n".join(evaluate(sequence, timeFromDamage=False).split("\n")[:3] + evaluate(sequence, timeFromDamage=True).split("\n")[2:])
            return output
        
def listCombos():
    comboList = []
    sequenceList = []
    maxLength = 0

    for sequence in CLASSIFICATIONS:
        if not CLASSIFICATIONS[sequence] in comboList:
            comboList += [CLASSIFICATIONS[sequence]]
            sequenceList += [sequence]
            maxLength = max(maxLength, len(comboList[-1]))

    return "```\n" + "\n".join([comboList[i] + " " * (maxLength - len(comboList[i])) + " | " + sequenceList[i] for i in range(len(comboList))]) + "\n```"