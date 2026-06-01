import babase
import bascenev1 as bs
import bascenev1lib
import random
from spaz import member_id as mem
from bascenev1lib.actor.playerspaz import PlayerSpaz
from typing import Sequence
from bascenev1lib.actor.popuptext import PopupText as pptx
from spaz import afk_checker as afk
from spaz import decorator
from chat import master_logger as log

class SpazPlayer(PlayerSpaz):
    """
    esta clase decora la clase PlayerSpaz la usaremos para aplicar nuestras modificaciones
    sin alterar la orginal
    """
    def __init__(self,
                 player: bs.Player,
                 color: Sequence[float] = (1.0, 1.0, 1.0),
                 highlight: Sequence[float] = (0.5, 0.5, 0.5),
                 character: str = 'Spaz',
                 powerups_expire: bool = True,):
        
        super().__init__(player=player,
                         color=color,
                         highlight=highlight,
                         character=character,
                         powerups_expire=powerups_expire,)


        from bascenev1 import get_foreground_host_session
        session = get_foreground_host_session()
        session_players=session.sessionplayers
        
        player_id = self.source_player.node.playerID #thanx to friedfighter
        
        
        player1 = self.source_player
        player = self._player._sessionplayer
        
        acc = player.get_account_id()
        clid = player1.node.playerID #havent run this in afk or decorator yet!
        
        roster = bs.get_game_roster()
        
        k = player.inputdevice.get_player_profiles()
        k2 = player1.getname()
        
        profiles = player.inputdevice.get_player_profiles()
        
        #client = player.inputdevice.client_id #for clientid using player instead of player1
        #print(client)


        self.active_effects = [] # for master timer system!
        self.active_nodes = []

        self._effect_timer = bs.Timer(
            0.1,
            babase.CallStrict(self._effect_tick),
            repeat=True
        )

        afk.afk_main(self, player) #entirely for afk related stuffs
        decorator.all_decorate(self, player) #entire tag/effect related area
        log.player_profiles(player) # for master log of playas
        
        # port basic stuff to decorater
        # port these stuff later!
        
    def _effect_tick(self): # as for this, even i forgot how it works lol but it works

        if (
            self is None
            or not self.is_alive()
            or not hasattr(self, 'node')
            or not self.node
            or not self.node.exists()
        ):
            self.active_effects.clear()
            self.clear_nodes()
            return

        current_time = bs.time()

        for effect_data in self.active_effects[:]:

            try:

                if (
                    current_time - effect_data["last_run"]
                    >= effect_data["interval"]
                ):

                    effect_data["callback"]()

                    effect_data["last_run"] = current_time

            except Exception as e:
                print(f'[Effect Error] {effect_data["name"]}: {e}')

    # =========================================================
    # EFFECT MANAGEMENT
    # =========================================================

    def add_effect(
        self,
        name,
        callback,
        interval=0.1
    ):

        # Prevent duplicates
        for effect in self.active_effects:

            if effect["name"] == name:
                return

        self.active_effects.append({
            "name": name,
            "callback": callback,
            "interval": interval,
            "last_run": 0
        })

    def remove_effect(self, name):

        self.active_effects = [

            effect
            for effect in self.active_effects

            if effect["name"] != name
        ]

    def has_effect(self, name):

        return any(
            effect["name"] == name
            for effect in self.active_effects
        )
        
    def add_node(self, node):
        self.active_nodes.append(node)

    def clear_nodes(self):

        for node in self.active_nodes[:]:

            try:
                if node.exists():
                    node.delete()

            except:
                pass

        self.active_nodes.clear()

def enable_prefix():
    bascenev1lib.actor.playerspaz.PlayerSpaz = SpazPlayer