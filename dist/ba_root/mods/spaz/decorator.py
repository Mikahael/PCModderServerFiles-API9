import babase
import bascenev1 as bs
import bascenev1lib
import random
from spaz import member_id as mid
from bascenev1lib.actor.playerspaz import PlayerSpaz
from typing import Sequence
from bascenev1lib.actor.popuptext import PopupText as pptx
from spaz import admin
from config import stats_master as mystats
import babase
import fire

STATS_FILE = 'ba_root/mods/config/player_data.json'

def all_decorate(self, player):
    acc = player.get_account_id()
    
    if acc in mid.admin:
        if acc not in mid.name:#for tag
            prefix_tag(self, prefix='ADMIN', animation=True, pos=(0, 1.45, 0))
        #glow_effect(self)
        #particle_effect(self)
        
    if acc in mid.owner:
        if acc not in mid.name:
            prefix_tag(self, prefix='BOSS', animation=True, pos=(0, 1.45, 0))
        glow_effect(self)
        particle_effect(self)
        
    if acc in mid.name:
        tag = mid.name[acc]#stored value
        prefix_tag(self, prefix=tag, animation=True, pos=(0, 1.45, 0))
    

    from _bascenev1 import get_client_ping as _get_ping
    client = player.inputdevice.client_id
    if fire.ping_tag:
        ping_tag(self, player)
        
    # rank tag comes here now!
    stats = mystats.rank_sys.data.get(acc)
    rank = stats["rank"]
    score = stats["score"]
    kills = stats["kills"]
    deaths = stats["deaths"]
    if rank == 1:
        icon = u'\ue043' #crown
        #prefix_tag(self, prefix='#'+str(rank), animation=False, pos=(0,2,0))
    elif rank == 2:
        icon = u'\ue048' #dragon
    elif rank == 3:
        icon = u'\ue049'
    elif rank == 4:
        icon = u'\ue00c'
    else:
        icon == u'\ue047'
        
    display = icon + '#' + str(rank) + icon
    if rank:
        prefix_tag(self, prefix=display, animation=False, pos=(0,2,0))
    else:
        pass
    
    
def prefix_tag(self, pos=(1,1,1), scales=0.01, prefix='admin', animation=True):
    if self.node.exists():
        m = bs.newnode('math', owner=self.node, attrs={'input1': pos, 'operation': 'add'})
        self.node.connectattr('position', m, 'input2')
        self._Text = bs.newnode('text',
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
        if animation:
            bs.animate_array(node=self._Text, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)

def ping_tag(self, player):
    if not self.node.exists():
        return

    m = bs.newnode('math', owner=self.node, attrs={
        'input1': (0, -1.0, 0),
        'operation': 'add'
    })

    self.node.connectattr('torso_position', m, 'input2')

    self.txt = bs.newnode('text',
                          owner=self.node,
                          attrs={
                              'text': '',
                              'in_world': True,
                              'shadow': 1.0,
                              'flatness': 1.0,
                              'scale': 0.009,
                              'h_align': 'center'
                          })

    m.connectattr('output', self.txt, 'position')

    client = player.inputdevice.client_id

    # update ping
    def _update_ping():
        if not self.node.exists():
            return

        try:
            ping = _get_ping(client) if client is not None else 0
        except Exception:
            ping = 0

        # Color logic based on ping
        if ping < 80:
            col = (0, 1, 0)
        elif ping < 150:
            col = (1, 1, 0)
        else:
            col = (1, 0, 0)

        self.txt.text = f"{ping} ms"
        self.txt.color = col

    _update_ping()
    bs.Timer(1.0, _update_ping, repeat=True)

def glow_effect(self):
    if self.node.exists():
        bs.animate_array(node=self.node, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)

def particle_effect(self, chunk='sweat'):
    def _run():
        if self.node.exists():
            vel = 4
            bs.emitfx(position=(self.node.torso_position[0]-0.25+random.random()*0.5,self.node.torso_position[1]-0.25+random.random()*0.5,self.node.torso_position[2]-0.25+random.random()*0.5),
                    velocity=((-vel+(random.random()*(vel*2)))+self.node.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.node.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.node.velocity[2]*2),
                    count=10,
                    scale=0.3+random.random()*1.1,
                    spread=0.1,
                    chunk_type=chunk)
    bs.timer(0.1, _run, repeat=True)