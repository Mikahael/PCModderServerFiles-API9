# ba_meta require api 9

import babase
from babase import apptimer
from powerups import powerupbox
from bomb import newbomb
from spaz import admin, newspaz
from maps import bstextonmap
from lobby import bslobby, players
from config import stats_master as mystats
from chat import coin_system as coin

# ba_meta export babase.Plugin

class setup_mods(babase.Plugin):
    def on_app_running(self):
        run_mods()
        print('was sup G')

    def on_app_shutdown(self):
        print("Goodbye!")

def run_mods():
    powerupbox.enable_pwps()
    admin.enable_prefix()
    newspaz.enable_spaz()
    newbomb.enable_bomb()
    bstextonmap.enable_textonmap()
    bslobby.enable_lobby()
    players.log_players()
    mystats.enable_stats()
    coin.enable_coinsys()
    print('mods loaded and running!')
