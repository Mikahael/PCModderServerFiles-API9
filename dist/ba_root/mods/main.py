# ba_meta require api 9

import babase
from babase import apptimer
from spaz import admin, newspaz
from lobby import bslobby
from powerups import powerupbox
from bomb import newbomb
from map import bstextonmap
from lobby.ping import start_ping_loop



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
    newbomb.enable_bomb() # pyright: ignore[reportAttributeAccessIssue]
    bstextonmap.enable_textonmap()
    apptimer(5, start_ping_loop)