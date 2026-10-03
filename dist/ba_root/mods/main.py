# ba_meta require api 9

import babase
from babase import apptimer
from powerups import powerupbox
from bomb import newbomb
from spaz import admin, newspaz
from maps import bstextonmap, playlist
from lobby import bslobby, botspawn, antibetray, cooldown, daily_cash
from config import stats_master as mystats
from chat import coin_system as coin
from chat import endvote, kick
from bascenev1 import _activity
import bascenev1 as bs
import bascenev1

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
    mystats.enable_stats()
    #coin.enable_coinsys() # load coin system from session mods instead!
    botspawn.new_ga_on_begin()
    antibetray.load_anti_betray()
    cooldown.remove_cooldown()
    daily_cash.load_multikill_bonus()
    kick.new_kick()
    playlist.new_playlist()
    clean_expiry_customers()
    start_begin()
    print('✅ Mods loaded and running!')


expiry_timer = None
#
def clean_expiry_customers():
    global expiry_timer
    #
    def check_expiration():
        coin.clean_expired_effects()
        coin.clean_expired_tags()
        #print('✅ Checking Expiration!')
    check_expiration()
    if expiry_timer is None:
        expiry_timer = babase.apptimer(3600, check_expiration, repeat=True)
        
        
old_begin = bs._activity.Activity.on_begin
def update_new_begin(self):
    old_begin(self)
    #print('endvote cleared and working!')
    endvote.reset_vote_state()
    antibetray.nooblist.clear()
    #print('nooblist cleared!')
    
def start_begin():
    #print('✅ Endvote cleared!')
    bs._activity.Activity.on_begin = update_new_begin