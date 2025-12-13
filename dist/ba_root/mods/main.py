# ba_meta require api 9

import sys
import os
import bascenev1._hooks
import bascenev1 as bs
import importlib
import _babase
import babase
from spaz import admin, newspaz
from lobby import bslobby
from chat import hooks
from powerups import powerupbox
from bomb import newbomb
from map import bstextonmap



# ba_meta export babase.Plugin

class setup_mods(babase.Plugin):
    def on_app_running(self):
        run_mods()
        print('was sup G')

    def on_app_shutdown(self):
        print("Goodbye!")
        
def run_mods():
    admin.enable_prefix()
    bslobby.enable_lobby()
    powerupbox.enable_pwps()
    newspaz.enable_spaz()
    newbomb.enable_bomb()
    bstextonmap.enable_textonmap()