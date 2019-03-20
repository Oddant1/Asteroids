from proj import *
from ship import *

class HUD(Drawn_Object):

    def __init__(self, player):

        # Get the player info for the HUD
        parent = player