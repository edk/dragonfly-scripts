import sys

from dragonfly import (
    Function,
    MappingRule,
    IntegerRef,
    Grammar,
    Dictation,
    Choice
)

aeneaPath = r"E:\dev\projects\aenea\util"  # ToDo: move to configuration.
if not aeneaPath in sys.path:
    sys.path.insert(0, aeneaPath)

try:
    from proxy_nicknames import Key
#     from proxy_actions import communication
    import aenea
except:
    pass


def window_direction(winDirection):
    try:
        Key("ctrl:down, alt:down").execute()
        Key("%s/5" % winDirection).execute()
    finally:  # Make sure to release the modifier keys.
        Key("alt:up, ctrl:up").execute()


windowDirections = {
    "(top|up) left": "KP_Home",
    "(top|up)": "KP_Up",
    "(top|up) right": "KP_Prior",
    "left": "KP_Left",
    "(middle|center)": "KP_Begin",
    "right": "KP_Right",
    "(bottom|down) left": "KP_End",
    "(bottom|down)": "KP_Down",
    "(bottom|down) right": "KP_Next",
}


def workspace_direction(wsDirection1, wsDirection2=None):
    try:
        Key("ctrl:down, alt:down, %s/5" % wsDirection1).execute()
        if wsDirection2:
            Key("%s/5" % wsDirection2).execute()
    finally:  # Make sure to release the modifier keys.
        Key("alt:up, ctrl:up").execute()

2
workspaceDirections = {
    "up": "up",
    "down": "down",
    "right": "right",
    "left": "left"
}


rules = MappingRule(
    mapping={
        # Commands and keywords:
        "workspace <wsDirection1> [<wsDirection2>]": Function(workspace_direction),  # @IgnorePep8
        "show launcher": Key("a-f1"),
        "show hud": Key("win"),
        "toggle panel menu": Key("a-f10"),
        "toggle desktop": Key("cw-d"),
        "toggle spread mode": Key("w-w"),
        "toggle expo mode": Key("w-s"),
        # Window control
        "close window": Key("a-f4"),
        "minimize window": Key("ca-KP_Insert"),
        "maximize window": Key("cw-up"),
        "restore window": Key("cw-down"),
        "move window": Key("a-f7"),
        "resize window": Key("a-f8"),
        # Window placement.
        "place window <winDirection>": Function(window_direction),
#         "": Key(""),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("wsDirection1", workspaceDirections),
        Choice("wsDirection2", workspaceDirections),
        Choice("winDirection", windowDirections),
    ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Unity desktop control grammar", context=aenea.global_context)
grammar.add_rule(rules)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None