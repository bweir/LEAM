import readline # optional, will allow Up/Down/History in the console
import code

import threading

def terminal():
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

term = threading.Thread(target=terminal)

def start():
    term.start()
