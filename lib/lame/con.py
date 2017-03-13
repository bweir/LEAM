from __main__ import __file__
import os

SCRIPT = os.path.dirname(__file__)

FREQ = 10
PERIOD_MS = 1000 // FREQ
PERIOD_S = float(PERIOD_MS) / 1000.0

