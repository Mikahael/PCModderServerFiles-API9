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
        
        #self.decorate(player)
        afk.afk_main(self, player) #entirely for afk related stuffs
        decorator.all_decorate(self, player) #entire tag/effect related area
        
        # port basic stuff to decorater
        # port these stuff later!
        
        if acc in mem.name:
            k = mem.name[acc]#stored value
            self._prefix_tag(pos=(0, 1.45, 0), scales=0.01, prefix=k)
            
        if acc in mem.bomb_limit:
            k = mem.bomb_limit[acc]
            self.bomb_type = k

        if acc in mem.owner:
            k = self.node.name
            self.node.name = u'\ue048'+k
            self.node.color = (-10,-10,-10)
            self.node.highlight = (-10,-10,-10)    
            self._particles()
            self._glow()
            
            if acc not in mem.name:
                self._prefix_tag(pos=(0, 1.45, 0), scales=0.01, prefix='O|W|N|E|R')
        

def enable_prefix():
    bascenev1lib.actor.playerspaz.PlayerSpaz = SpazPlayer