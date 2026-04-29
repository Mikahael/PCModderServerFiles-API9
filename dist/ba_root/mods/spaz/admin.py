import babase
import bascenev1 as bs
import bascenev1lib
import random
from spaz import member_id as mem
from bascenev1lib.actor.playerspaz import PlayerSpaz
from typing import Sequence
from bascenev1lib.actor.popuptext import PopupText as pptx
from spaz import afk_checker as afk

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
        
        player = self._player._sessionplayer
        acc = player.get_account_id()
        
        #self.decorate(player)
        afk.afk_main(self, player) #entirely for afk related stuffs
        
        if acc in mem.name:
            k = mem.name[acc]#stored value
            self._prefix_tag(pos=(0, 1.45, 0), scales=0.01, prefix=k)
            
        if acc in mem.bomb_limit:
            k = mem.bomb_limit[acc]
            self.bomb_type = k

        if acc in mem.admin:
            self._glow()
            if acc not in mem.name:
                self._prefix_tag(pos=(0, 1.45, 0), scales=0.01, prefix=u'\ue047ADMIN\ue047')

        if acc in mem.owner:
            k = self.node.name
            self.node.name = u'\ue048'+k
            self.node.color = (-10,-10,-10)
            self.node.highlight = (-10,-10,-10)    
            self._particles()
            self._glow()
            
            if acc not in mem.name:
                self._prefix_tag(pos=(0, 1.45, 0), scales=0.01, prefix='O|W|N|E|R')
    
    
    def decorate(self, player):
        import bascenev1 as bs
        import babase

        p = player.get_account_id()
        timeout = 60
        self.last_change_time = bs.time()
        self._warned = set()

        def afk_checker(to): #improved with PCModder
            t = bs.time()
            inactive = t - self.last_change_time

            if self.is_alive():
                for w in (30, 40, 50):
                    if inactive >= w and w not in self._warned:
                        self._warned.add(w)
                        #bs.broadcastmessage(f"{player.getname()} is AFK ({int(inactive)}s)")
                        pptx(f"AFK ({int(inactive)}s)",color=(1, 0, 0), scale=1.5,position=self.node.position,).autoretain()

                if inactive >= to:
                    bs.broadcastmessage(
                        f"Removing {player.getname()} for being AFK for more than {to} seconds"
                    )
                    player.remove_from_game()

        self.afk_timer = bs.Timer(1.0, babase.CallStrict(afk_checker, timeout), repeat=True)

    def _prefix_tag(self, pos=(1,1,1), scales=0.008, prefix='admin'):
        import bascenev1 as ba
        if self.node.exists():
            m = ba.newnode('math', owner=self.node, attrs={'input1': pos, 'operation': 'add'})
            self.node.connectattr('position', m, 'input2')
            self._Text = ba.newnode('text',
                                owner=self.node,
                                attrs={
                                    'text': prefix,
                                    'in_world': True,
                                    'shadow': 1.0,
                                    'flatness': 1.0,
                                    'color': (1, 1, 1),
                                    'scale': scales,
                                    'h_align': 'center'})
            m.connectattr('output', self._Text, 'position')
            ba.animate_array(node=self._Text, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)
        
        
    def _particles(self):
        import bascenev1, random
        def _run():
            if self.node.exists():
                vel = 4
                bascenev1.emitfx(position=(self.node.torso_position[0]-0.25+random.random()*0.5,self.node.torso_position[1]-0.25+random.random()*0.5,self.node.torso_position[2]-0.25+random.random()*0.5),
                    velocity=((-vel+(random.random()*(vel*2)))+self.node.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.node.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.node.velocity[2]*2),
                    count=10,
                    scale=0.3+random.random()*1.1,
                    spread=0.1,
                    chunk_type='sweat')
        bascenev1.timer(0.1, _run, repeat=True)
        
        
    def _glow(self):
        import bascenev1, random
        if self.node.exists():
            bascenev1.animate_array(node=self.node, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)


def enable_prefix():
    bascenev1lib.actor.playerspaz.PlayerSpaz = SpazPlayer