# Zola 2.0

> Zola's algorithm evaluates people's past to predict their future

Likewise, Zola 2.0 is an algorithm that evaluate's a combo's damage and execution time to predict your ranked opponents' future pain. This python script is designed to quickly, easily, and accurately analyse Spider-Man's combos in Marvel Rivals.

## Installation

Installation instructions will be provided once basic functionality has been acheived

## Usage

Zola evaluates combos given to it by the **!eval** command:

```
    !eval tGusto
```

The above evaluates the combo **tracer > get over here targetting > uppercut > swing > tracer > overhead slam**. Each action in a combo is assigned a single letter for maximum efficiency, but a combo can also be given in long-form by breaking up actions with instances of "**>**" - so the following is another valid way of writing the same command:

```
    !eval tracer > goht > upper > swing > tracer > oh
```

Note that shortened names are still used; in this format, single letter, shorthand names, or full names can be used to refer to each action. The full list is given below:

| Action | Letter | Other Names |
| :---: | :---: | :---:|
| Jump | j | jump <br> dj |
| Land | l | land |
| Punch | p | punch <br> punchA <br> punchB <br> meleePunch <br> meleePunchA <br> meleePunchB |
| Kick | k | kick <br> meleeKick |
| Overhead Slam | o | overheadSlam <br> overhead <br> oh <br> meleeOverhead <br> slam |
| Tracer | t | tracer <br> webTracer <br> cluster <br> webCluster |
| Swing | s | swing <br> webSwing <br> highSwing <br> lowSwing |
| Whiff | w | whiff <br> webWhiff <br> swingWhiff |
| Get Over Here | g | getOverHere <br> goh |
| Get Over Here Targetting | G | getOverHereTargetting <br> goht |
| Uppercut | u | uppercut <br> upper <br> amazingCombo |
| Symbiote | S | symbiote <br> symbiot |

> [!TIP]
> The single letter names of actions are case sensetive, while all of the longer-form versions of names ignore case and spaces, so *"MELEE punch a"* will be interpreted as a punch.

> [!WARNING]
> Certain names such as *"dj"* and *"meleePunchB"* imply that the actions occur in contexts that aren't strictly enforced by the evaluation function - in these cases, the evaluation will come with a warning that the combo isn't being executed in the way that the user likely intended.

### Initial State

Some combos involve a setup that you don't want to list as a part of the combo - this setup can be detailed in brackets before the combo. For example;

```
    !eval (tA)Gjo
```

The above combo has the initial conditions of the opponent being tagged with a tracer, and the opponent being airborne. This means that goht is able to be used right away, and that the user is airborn after doing so, meaning the jump is a double jump, granting a jump overhead. Initial conditions can also be written in long-form:

```
    !eval (tagged, targetAirborne) goht > dj > oh
```

The full list of initial conditions is given below:

| Initial Condition | Letter | Other Names |
| :---: | :---: | :---: |
| Opponent tagged with tracer | t | tagged <br> tag|
| Player is airborne | a | isAirborne <br> airborne <br> air |
| Player is airborne with swing overhead | s | hasSwingOverhead |
| Player is airborne with jump overhead | j | hasJumpOverhead |
| Opponent is airborne | A | opponentAirborne |
| Punch sequence is up to punch B | p | openPunchB |
| Punch sequence is up to kick | k | openKick |

### Move Stacks

A movestack is indicated by a "**+**" - for example, a FFAme stack would be written as follows:

```
    !eval (t)G+u
```

In long-form commands, the "**>**" separator can be entirely replaced by a "**+**", or they can be used in conjunction. If the command contains no instaces of the "**>**" character, it will not be recognised as a command, so the following are valid:

```
    !eval (tag) goht >+ upper
```

```
    !eval tracer > goht + upper
```

But the following will not work, as Zola will not recognise the command as being long-form, since no "**>**" characters are present:

```
    !eval (tag) goht + upper
```

All movestacks are listed below:

|Name | Sequence(/s) |
| :---: | :---: |
| FFAme Stack | G+u | 
| Saporen Tech | (t) o+G <br> (t) p+G <br> (t) k+G |
| Backflash | p+t <br> k+t <br> o+t |
| Unique 3-Hit Stack | p+o <br> k+o |
| GOHT Overhead Preserve | (t) s+G |
| Early Animation Cancels | o+u <br> k+u |

## Roadmap

- [ ] Add parsing of commands in all formats
- [ ] Measure & record all action timings
- [ ] Add evaluation function
- [ ] Add error detection & warnings
- [ ] Add discord bot functionality
- [ ] Add combo generator
- [ ] Optimise combo generator by removing unneeded actions