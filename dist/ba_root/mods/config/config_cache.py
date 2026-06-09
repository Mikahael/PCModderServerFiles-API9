#
#
# cache configurations for instant reload!
# for settings only!
#

from chat import master_logger as log

powerup = log.master_load_db("pwp")
bomby = log.master_load_db("bomb")
spazy = log.master_load_db("spaz")

def save_powerup():
    log.master_save_db("pwp", powerup)
    
def save_bomb():
    log.master_save_db("bomb", bomby)
    
def save_spaz():
    log.master_save_db("spaz", spazy)