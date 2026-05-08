import babase
import bascenev1 as bs
import bascenev1lib
import random
from spaz import member_id as mid
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.spazfactory import SpazFactory
from typing import Sequence
from bascenev1lib.actor.popuptext import PopupText as pptx
from spaz import admin
from config import stats_master as mystats
import babase
import fire
from functools import partial

STATS_FILE = 'ba_root/mods/config/player_data.json'

def all_decorate(self, player):
    acc = player.get_account_id()
    
    
    EFFECTS = {
        "spark": {
            "callback" : spark_effect,
            "interval" : 0.1
        },
        "sparkground": {
            "callback" : sparkground_effect,
            "interval" : 0.2
        },
        "sweat": {
            "callback" : sweat_effect,
            "interval" : 0.1
        },
        "sweatground": {
            "callback" : sweatground_effect,
            "interval" : 0.04
        },
        "shine": {
            "callback" : shine_effect,
            "interval" : 3.0
        },
        "highlightshine": {
            "callback" : highlight_effect,
            "interval" : 9.0
        },
        "distortion": {
            "callback" : distortion_effect,
            "interval" : 1.0
        },
        "rainbow": {
            "callback" : rainbow_effect,
            "interval" : 1.0
        },
        "ice": {
            "callback" : ice_effect,
            "interval" : 0.5
        },
        "iceground": {
            "callback" : iceground_effect,
            "interval" : 0.05
        },
        "slime": {
            "callback" : slime_effect,
            "interval" : 0.25
        },
        "metal": {
            "callback" : metal_effect,
            "interval" : 0.25
        },
        "splinter": {
            "callback" : splinter_effect,
            "interval" : 0.75
        },
        "fairydust": {
            "callback" : fairydust_effect,
            "interval" : 0.01
        },
        "fire": {
            "callback" : fire_effect,
            "interval" : 0.1
        },
        "star": {
            "callback" : star_effect,
            "interval" : 0.1
        },
        "newrainbow": {
            "callback" : newrainbow_effect,
            "interval" : 1.2
        },
        "footprint": {
            "callback" : footprint_effect,
            "interval" : 0.15
        },
        "firespark": {
            "callback" : firespark_effect,
            "interval" : 0.1
        },
        "darkmagic": {
            "callback" : darkmagic_effect,
            "interval" : 0.2
        },
    }
    
    # add effects and tags to clients now
    
    if acc in mid.customers:
        purchased_effects = list(mid.customers[acc]["effects"].keys())
        enabled_effects = purchased_effects
        
        #
        tags = mid.customers[acc]["tags"]
        for tag_type, tag_data in tags.items():
            name = tag_data["name"]
            expiry = tag_data["expiry"]
            #
            if tag_type == 'tag1':
                anim = 1
            elif tag_type == 'tag2':
                anim = 2
            elif tag_type == 'tag3':
                anim = 3
            elif tag_type == 'tag4':
                anim = 4
            elif tag_type == 'tag5':
                anim = 5
            color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5)) # let it be rando color instead of red all the time!
            animated_prefix_tag(self, prefix=name, col=(1.0, 0.0, 0.0), anim_id=anim)
        
    
    user_tags = mid.customers.get(acc, {}).get("tags", {})
    if acc in mid.admin:
        if not user_tags and acc not in mid.name:
            prefix_tag(self, prefix='ADMIN', animation=True, pos=(0, 1.45, 0))
        #glow_effect(self)
        #enabled_effects.append("spark")
    
    user_tags = mid.customers.get(acc, {}).get("tags", {})  
    if acc in mid.owner:
        if not user_tags and acc not in mid.name: # only show if custom name or purchased tag doesnt exist!
            # red color for owners!
            animated_prefix_tag(self, prefix="BOSS", col=(1.0, 0.0, 0.0), anim_id=3)
    

    for effect_name in enabled_effects:

        if effect_name not in EFFECTS:
            continue

        effect_data = EFFECTS[effect_name]

        self.add_effect(
            name=effect_name,

            callback=partial(
                effect_data["callback"],
                self
            ),

            interval=effect_data["interval"]
        )
    
    if acc in mid.name:
        if not user_tags: # if u already purchased a tag, dont show!
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

def get_anim_id(tagtype):
    tag_map = {
        'tag1': 1,
        'tag2': 2,
        'tag3': 3,
        'tag4': 4,
        'tag5': 5
    }
    return tag_map.get(tagtype)

def animated_prefix_tag(self, prefix, col, anim_id):
    char_spacing = 0.15
    total_chars = len(prefix)
    start_x = -((total_chars - 1) * char_spacing) / 2

    for i, char in enumerate(prefix):
        # Position each character
        curr_x = start_x + (i * char_spacing)

        m = bs.newnode(
            'math',
            owner=self.node,
            attrs={
                'input1': (curr_x, 1.5, 0),
                'operation': 'add'
            }
        )
        self.node.connectattr('torso_position', m, 'input2')

        # Color handling
        char_col = col
        if anim_id == 6:
            char_col = (
                random.random(),
                random.random(),
                random.random()
            )

        # Create text node
        t = bs.newnode(
            'text',
            owner=self.node,
            attrs={
                'text': char,
                'in_world': True,
                'shadow': 1.0,
                'flatness': 1.0,
                'color': tuple(char_col),
                'scale': 0.01,
                'h_align': 'center'
            }
        )

        m.connectattr('output', t, 'position')

        # Delay per character (wave effect)
        delay = i * 0.15

        # 🔥 ANIMATIONS (must be INSIDE loop)
        if anim_id == 2:
            bs.animate_array(
                t, 'color', 3,
                {
                    0.0: (1, 0, 0),
                    0.5: (1, 1, 0),
                    1.0: (1, 0, 0)
                },
                loop=True,
                offset=delay
            )

            bs.animate_array(
                m, 'input1', 3,
                {
                    0.0: (curr_x, 1.5, 0),
                    0.5: (curr_x, 1.58, 0),
                    1.0: (curr_x, 1.5, 0)
                },
                loop=True,
                offset=delay
            )

        elif anim_id == 3:
            bs.animate(
                t, 'opacity',
                {0.0: 0.3, 0.5: 1.0, 1.0: 0.3},
                loop=True,
                offset=delay
            )

        elif anim_id == 4:
            bs.animate(
                t, 'opacity',
                {0.0: 1.0, 0.2: 0.0, 0.4: 1.0},
                loop=True,
                offset=delay
            )

        elif anim_id == 5:
            bs.animate_array(
                t, 'color', 3,
                {
                    0.0: (1, 0, 0),
                    0.5: (0, 1, 0),
                    1.0: (0, 0, 1),
                    1.5: (1, 0, 0)
                },
                loop=True,
                offset=delay
            )

        elif anim_id == 6:  # Rainbow Wave
            bs.animate_array(
                t, 'color', 3,
                {
                    0.0: (1, 0, 0),
                    0.2: (0, 1, 0),
                    0.4: (0, 0, 1),
                    0.6: (1, 1, 0),
                    0.8: (0, 1, 1),
                    1.0: (1, 0, 0)
                },
                loop=True,
                offset=delay
            )

        elif anim_id == 7:  # Golden Sweep
            bs.animate_array(
                t, 'color', 3,
                {
                    0.0: (1, 0.8, 0),
                    0.2: (1, 1, 0.6),
                    0.4: (1, 0.8, 0)
                },
                loop=True,
                offset=delay
            )

        elif anim_id == 8:  # Neon Pulse
            bs.animate_array(
                t, 'color', 3,
                {
                    0.0: char_col,
                    0.5: (1, 1, 1),
                    1.0: char_col
                },
                loop=True,
                offset=delay
            )

        elif anim_id == 9:  # Vertical Bounce
            bs.animate_array(
                m, 'input1', 3,
                {
                    0.0: (curr_x, 1.5, 0),
                    0.5: (curr_x, 1.65, 0),
                    1.0: (curr_x, 1.5, 0)
                },
                loop=True,
                offset=delay
            )

        elif anim_id == 10:  # Indian Flag
            idx_ratio = i / total_chars

            if idx_ratio < 0.33:
                base_color = (1.0, 0.5, 0.0)
            elif idx_ratio < 0.66:
                base_color = (1.0, 1.0, 1.0)
            else:
                base_color = (0.0, 0.5, 0.0)

            bs.animate_array(
                t, 'color', 3,
                {
                    0.0: base_color,
                    0.5: (0.0, 0.0, 0.5),
                    1.0: base_color
                },
                loop=True,
                offset=delay
            )

        elif anim_id == 11:
            bs.animate_array(
                t, 'color', 3,
                {
                    0.0: (1, 0, 0),
                    0.25: (1, 1, 1),
                    0.5: (0, 0, 1),
                    0.75: (0, 0.8, 1),
                    1.0: (1, 0, 0)
                },
                loop=True,
                offset=delay
            )

            bs.animate_array(
                m, 'input1', 3,
                {
                    0.0: (curr_x, 1.5, 0),
                    0.5: (curr_x, 1.55, 0),
                    1.0: (curr_x, 1.5, 0)
                },
                loop=True,
                offset=delay
            )

        elif anim_id == 12:
            bs.animate_array(
                t, 'color', 3,
                {
                    0.0: (1, 1, 1),
                    0.49: (1, 1, 1),
                    0.5: (1, 1, 0),
                    0.99: (1, 1, 0),
                    1.0: (1, 1, 1)
                },
                loop=True,
                offset=delay
            )

            bs.animate_array(
                m, 'input1', 3,
                {
                    0.0: (curr_x, 1.5, 0),
                    0.5: (curr_x, 1.55, 0),
                    1.0: (curr_x, 1.5, 0)
                },
                loop=True,
                offset=delay
            )

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
    
    
    
# begin spaz effects from ashx files - thx to him for giving!

def spark_effect(self):
    bs.emitfx(
        position=self.node.position,
        velocity=self.node.velocity,
        count=random.randint(1, 10),
        scale=0.5,
        spread=0.2,
        chunk_type="spark"
    )
    
def sparkground_effect(self):
        bs.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 5),
            scale=0.2,
            spread=0.1,
            chunk_type="spark",
            emit_type="stickers",
        )
        
def sweat_effect(self):
        velocity = 4.0
        calculate_position = lambda \
            torso_position: torso_position - 0.25 + random.uniform(0, 0.5)
        calculate_velocity = lambda node_velocity, multiplier: random.uniform(
            -velocity, velocity) + node_velocity * multiplier
        position = tuple(calculate_position(coordinate)
                         for coordinate in self.node.torso_position)
        velocity = (
            calculate_velocity(self.node.velocity[0], 2),
            calculate_velocity(self.node.velocity[1], 4),
            calculate_velocity(self.node.velocity[2], 2),
        )
        bs.emitfx(
            position=position,
            velocity=velocity,
            count=10,
            scale=random.uniform(0.3, 1.4),
            spread=0.1,
            chunk_type="sweat",
        )
   
def sweatground_effect(self):
        velocity = 1.2
        calculate_position = lambda \
            torso_position: torso_position - 0.25 + random.uniform(0, 0.5)
        calculate_velocity = lambda node_velocity, multiplier: random.uniform(
            -velocity, velocity) + node_velocity * multiplier
        position = tuple(calculate_position(coordinate)
                         for coordinate in self.node.torso_position)
        velocity = (
            calculate_velocity(self.node.velocity[0], 2),
            calculate_velocity(self.node.velocity[1], 4),
            calculate_velocity(self.node.velocity[2], 2),
        )
        bs.emitfx(
            position=position,
            velocity=velocity,
            count=10,
            scale=random.uniform(0.1, 1.2),
            spread=0.1,
            chunk_type="sweat",
            emit_type="stickers",
        )
   
def distortion_effect(self):
        bs.emitfx(
            position=self.node.position,
            spread=1.0,
            emit_type="distortion"
        )
        bs.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 5),
            emit_type="tendrils",
            tendril_type="smoke",
        )
        
def shine_effect(self):
        shine_factor = 1.2
        dim_factor = 0.90

        default_color = self.node.color
        shiny_color = tuple(channel * shine_factor for channel in default_color)
        dimmy_color = tuple(channel * dim_factor for channel in default_color)
        animation = {
            0: default_color,
            1: dimmy_color,
            2: shiny_color,
            3: default_color,
        }
        bs.animate_array(self.node, "color", 3, animation)
        
def highlight_effect(self):
        self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
  
def rainbow_effect(self):
        bs.animate_array(node=self.node, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)
  
def glowy_effect(self):
        glowing_light = bs.newnode(
            "light",
            attrs={
                "color": (1.0, 0.4, 0.5),
                "height_attenuated": False,
                "radius": 0.4}
        )
        self.node.connectattr("position", glowing_light, "position")
        bs.animate(
            glowing_light,
            "intensity",
            {0: 0.0, 1: 0.2, 2: 0.0},
            loop=True)
        self.add_node(glowing_light)
        
def scorch_effect(self):
        scorcher = bs.newnode(
            "scorch",
            attrs={
                "position": self.node.position,
                "size": 1.00,
                "big": True}
        )
        self.node.connectattr("position", scorcher, "position")
        animation = {
            0: (1, 0, 0),
            1: (0, 1, 0),
            2: (1, 0, 1),
            3: (0, 1, 1),
            4: (1, 0, 0),
        }
        bs.animate_array(scorcher, "color", 3, animation, loop=True)
        self.add_node(scorch_effect)
        
def ice_effect(self):
        bs.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(2, 8),
            scale=0.4,
            spread=0.2,
            chunk_type="ice",
        )
        
def iceground_effect(self):
        bs.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 2),
            scale=random.uniform(0, 0.5),
            spread=1.0,
            chunk_type="ice",
            emit_type="stickers",
        )
        
def slime_effect(self):
        bs.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 10),
            scale=0.4,
            spread=0.2,
            chunk_type="slime",
        )
        
def metal_effect(self):
        bs.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 4),
            scale=0.4,
            spread=0.1,
            chunk_type="metal",
        )
        
def splinter_effect(self):
        bs.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 5),
            scale=0.5,
            spread=0.2,
            chunk_type="splinter",
        )
        
def fairydust_effect(self):
        velocity = 2
        calculate_position = lambda torso_position: torso_position - 0.25 + random.uniform(0, 0.5)
        calculate_velocity = lambda node_velocity, multiplier: random.uniform(-velocity, velocity) + node_velocity * multiplier
        position = tuple(calculate_position(coordinate) for coordinate in self.node.torso_position)
        velocity = (
                    calculate_velocity(self.node.velocity[0], 6),
                    calculate_velocity(self.node.velocity[1], 8),
                    calculate_velocity(self.node.velocity[2], 8),
    )
        bs.emitfx(
                position=position,
                velocity=velocity,
                count=random.randint(100,200),
                spread=8.5,
                emit_type="fairydust",
    )
    
def fire_effect(self) -> None:
        if not self.node.exists():
            self._cm_effect_timer = None
        else:
            bs.emitfx(position=self.node.position,
            scale=3,count=50*2,spread=0.3,
            chunk_type='sweat')


def star_effect(self) -> None:
        def die(node: bs.Node) -> None:
            if node:
                m = node.mesh_scale
                bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
                bs.timer(0.1, node.delete)

        if not self.node.exists() or self._dead:
            self._cm_effect_timer = None
        else:
            c = 0.3
            pos_list = [
                (c, 0, 0), (0, 0, c),
                (-c, 0, 0), (0, 0, -c)]
            
            for p in pos_list:
                m= 1.5
                np = self.node.position
                pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
                vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

                texs = ['bombStickyColor', 'aliColor', 'aliColorMask', 'eggTex3']
                tex = bs.gettexture(random.choice(texs))
                mesh = bs.getmesh('flash')
                factory = SpazFactory.get()

                mat = bs.Material()
                mat.add_actions(
                    conditions=('they_have_material', factory.punch_material),
                    actions=(
                        ('modify_part_collision', 'collide', False),
                        ('modify_part_collision', 'physical', False),
                    ))
                node = bs.newnode('prop',
                                owner=self.node,
                                attrs={'body': 'sphere',
                                       'position': pos,
                                        'velocity': vel,
                                        'mesh': mesh,
                                        'mesh_scale': 0.1,
                                        'body_scale': 0.0,
                                        'shadow_size': 0.0,
                                        'gravity_scale': 0.5,
                                        'color_texture': tex,
                                        'reflection': 'soft',
                                        'reflection_scale': [1.5],
                                        'materials': [mat]})
                light = bs.newnode('light',
                                   owner=node,
                                   attrs={
                                       'intensity': 0.3,
                                       'volume_intensity_scale': 0.5,
                                       'color': (random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5)),
                                        'radius': 0.035})
                node.connectattr('position', light, 'position')
                bs.timer(0.25, babase.CallPartial(die, node))
                
def newrainbow_effect(self) -> None:
        animate = {
             0.0: (2.0, 0.0, 0.0),
             0.2: (2.0, 1.5, 0.5),
             0.4: (2.0, 2.0, 0.0),
             0.6: (0.0, 2.0, 0.0),
             0.8: (0.0, 2.0, 2.0),
             1.0: (0.0, 0.0, 2.0)
        }
        keys = {
             0.0: (2.0, 0.0, 0.0),
             0.2: (2.0, 1.5, 0.5),
             0.4: (2.0, 2.0, 0.0),
             0.6: (0.0, 2.0, 0.0),
             0.8: (0.0, 2.0, 2.0),
             1.0: (0.0, 0.0, 2.0),
            }.items()
        
        def _changecolor(color: Sequence[float]) -> None:
            if self.node.exists():
                self.node.color = color

        for time, color in keys:
            bs.animate_array(self.node, "highlight", 3, animate, loop=True)
            bs.timer(time, babase.CallPartial(_changecolor, color))
            
def footprint_effect(self) -> None:
        if not self.node.exists():
            self._cm_effect_timer = None
        else:
            loc = bs.newnode('locator', owner=self.node,
              attrs={
                     'position': self.node.position,
                     'shape': 'circle',
                     'color': (random.uniform(0.5, 1.5),
                               random.uniform(0.5, 1.5),
                               random.uniform(0.5, 1.5)),
                     'size': [0.2],
                     'draw_beauty': False,
                     'additive': False})
            bs.animate(loc, 'opacity', {0: 1.0, 1.9: 0.0})
            bs.timer(2.0, loc.delete)
            
def firespark_effect(self) -> None:
        def die(node: bs.Node) -> None:
            if node:
                m = node.mesh_scale
                bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
                bs.timer(0.1, node.delete)

        if not self.node.exists() or self._dead:
            self._cm_effect_timer = None
        else:
            c = 0.3
            pos_list = [
                (c, 0, 0), (0, 0, c),
                (-c, 0, 0), (0, 0, -c)]
            
            for p in pos_list:
                m= 1.5
                np = self.node.position
                pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
                vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

                tex = bs.gettexture('null')
                mesh = None
                factory = SpazFactory.get()

                mat = bs.Material()
                mat.add_actions(
                    conditions=('they_have_material', factory.punch_material),
                    actions=(
                        ('modify_part_collision', 'collide', False),
                        ('modify_part_collision', 'physical', False),
                    ))
                node = bs.newnode('bomb',
                                owner=self.node,
                                attrs={'body': 'sphere',
                                       'position': pos,
                                        'velocity': vel,
                                        'mesh': mesh,
                                        'mesh_scale': 0.1,
                                        'body_scale': 0.0,
                                        'color_texture': tex,
                                        'fuse_length': 0.1,
                                        'materials': [mat]})
                light = bs.newnode('light',
                                   owner=node,
                                   attrs={
                                       'intensity': 0.2,
                                       'volume_intensity_scale': 0.4,
                                       'color': (random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5)),
                                        'radius': 0.025})
                node.connectattr('position', light, 'position')
                bs.timer(0.25, babase.CallPartial(die, node)) 
                
def darkmagic_effect(self) -> None:
        def die(node: bs.Node) -> None:
            if node:
                m = node.mesh_scale
                bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
                bs.timer(0.1, node.delete)

        if not self.node.exists() or self._dead:
            self._cm_effect_timer = None
        else:
            c = 0.3
            pos_list = [
                (c, 0, 0), (0, 0, c),
                (-c, 0, 0), (0, 0, -c)]
            
            for p in pos_list:
                m= 1.5
                np = self.node.position
                pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
                vel = (random.uniform(-m, m), 30.0, random.uniform(-m, m))

                tex = bs.gettexture('impactBombColor')
                mesh = bs.getmesh('impactBomb')
                factory = SpazFactory.get()

                mat = bs.Material()
                mat.add_actions(
                    conditions=('they_have_material', factory.punch_material),
                    actions=(
                        ('modify_part_collision', 'collide', False),
                        ('modify_part_collision', 'physical', False),
                    ))
                node = bs.newnode('prop',
                                owner=self.node,
                                attrs={'body': 'sphere',
                                       'position': pos,
                                        'velocity': vel,
                                        'mesh': mesh,
                                        'mesh_scale': 0.4,
                                        'body_scale': 0.0,
                                        'shadow_size': 0.0,
                                        'gravity_scale': 0.5,
                                        'color_texture': tex,
                                        'reflection': 'soft',
                                        'reflection_scale': [0.0],
                                        'materials': [mat]})
                light = bs.newnode('light',
                                   owner=node,
                                   attrs={
                                       'intensity': 0.8,
                                       'volume_intensity_scale': 0.5,
                                       'color': (0.5, 0.0, 1.0),
                                       'radius': 0.035})
                node.connectattr('position', light, 'position')
                bs.timer(0.25, babase.CallPartial(die, node)) 
                
                
def aure_effect(self) -> None:
        def anim(node: bs.Node) -> None:
            bs.animate_array(node, 'color', 3,
                {0: (1,1,0), 0.1: (0,1,0),
                 0.2: (1,0,0), 0.3: (0,0.5,1),
                 0.4: (1,0,1)}, loop=True)
            bs.animate_array(node, 'size', 1,
                {0: [1.0], 0.2: [1.5], 0.3: [1.0]}, loop=True)

        attrs = ['torso_position', 'position_center', 'position']
        for i, pos in enumerate(attrs):
            loc = bs.newnode('locator', owner=self.node,
                  attrs={'shape': 'circleOutline',
                         'color': self.node.color,
                         'opacity': 1.0,
                         'draw_beauty': True,
                         'additive': False})
            self.node.connectattr(pos, loc, 'position')
            bs.timer(0.1 * i, babase.Call(anim, loc))