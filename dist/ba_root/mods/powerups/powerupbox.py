# Released under the MIT License. See LICENSE for details.
#
"""Defines Actor(s)."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, override

import bascenev1 as bs
import bascenev1lib
from bascenev1lib.actor import powerupbox
from bascenev1lib.actor.powerupbox import PowerupBox, PowerupBoxFactory
from bascenev1 import get_foreground_host_activity

from bascenev1lib.gameutils import SharedObjects
from bascenev1._gameutils import animate, animate_array
from bascenev1 import _powerup
from bascenev1._gameactivity import GameActivity
import babase
import _babase
from config import powerup_config as pwp

if TYPE_CHECKING:
    from typing import Any, Sequence

DEFAULT_POWERUP_INTERVAL = 8.0


class _TouchedMessage: # updated to latest api 9
    pass


class NewPowerupBoxFactory:
    """A collection of media and other resources used by bs.Powerups.

    A single instance of this is shared between all powerups
    and can be retrieved via bs.Powerup.get_factory().
    """

    mesh: bs.Mesh
    """The bs.Mesh of the powerup box."""

    mesh_simple: bs.Mesh
    """A simpler bs.Mesh of the powerup box, for use in shadows, etc."""

    tex_bomb: bs.Texture
    """Triple-bomb powerup bs.Texture."""

    tex_punch: bs.Texture
    """Punch powerup bs.Texture."""

    tex_ice_bombs: bs.Texture
    """Ice bomb powerup bs.Texture."""

    tex_sticky_bombs: bs.Texture
    """Sticky bomb powerup bs.Texture."""

    tex_shield: bs.Texture
    """Shield powerup bs.Texture."""

    tex_impact_bombs: bs.Texture
    """Impact-bomb powerup bs.Texture."""

    tex_health: bs.Texture
    """Health powerup bs.Texture."""

    tex_land_mines: bs.Texture
    """Land-mine powerup bs.Texture."""

    tex_curse: bs.Texture
    """Curse powerup bs.Texture."""

    health_powerup_sound: bs.Sound
    """bs.Sound played when a health powerup is accepted."""

    powerup_sound: bs.Sound
    """bs.Sound played when a powerup is accepted."""

    powerdown_sound: bs.Sound
    """bs.Sound that can be used when powerups wear off."""

    powerup_material: bs.Material
    """bs.Material applied to powerup boxes."""

    powerup_accept_material: bs.Material
    """Powerups will send a bs.PowerupMessage to anything they touch
       that has this bs.Material applied."""

    _STORENAME = bs.storagename()

    def __init__(self) -> None:
        """Instantiate a PowerupBoxFactory.

        You shouldn't need to do this; call Powerup.get_factory()
        to get a shared instance.
        """
        from bascenev1 import get_default_powerup_distribution

        shared = SharedObjects.get()
        self._lastpoweruptype: str | None = None
        self.mesh = bs.getmesh('powerup')
        self.mesh_simple = bs.getmesh('powerupSimple')
        self.tex_bomb = bs.gettexture('powerupBomb')
        self.tex_punch = bs.gettexture('powerupPunch')
        self.tex_ice_bombs = bs.gettexture('powerupIceBombs')
        self.tex_sticky_bombs = bs.gettexture('powerupStickyBombs')
        self.tex_shield = bs.gettexture('powerupShield')
        self.tex_impact_bombs = bs.gettexture('powerupImpactBombs')
        self.tex_health = bs.gettexture('powerupHealth')
        self.tex_land_mines = bs.gettexture('powerupLandMines')
        self.tex_curse = bs.gettexture('powerupCurse')
        #
        #new powerups
        #
        self.tex_slow = bs.gettexture('night')
        self.tex_champ = bs.gettexture('achievementBoxer')
        self.tex_speed = bs.gettexture('achievementGotTheMoves')
        self.tex_spunch = bs.gettexture('achievementSuperPunch')
        self.tex_radius = bs.gettexture('achievementOnslaught')
        self.tex_multibomb = bs.gettexture('crossOutMask')
        self.tex_xtraLife = bs.gettexture('achievementStayinAlive')
        self.tex_lowLife = bs.gettexture('star')
        self.tex_martyrdom = bs.gettexture('achievementCrossHair')
        self.tex_tnt = bs.gettexture('achievementTNT')
        self.tex_ice_impact = bs.gettexture('gameCircleIcon')
        self.tex_sticky_ice = bs.gettexture('eggTex2')
        self.tex_glue_bomb = bs.gettexture('logo')
        self.tex_curse_mine = bs.gettexture('achievementInControl')
        self.tex_ice_mine = bs.gettexture('egg2')
        self.tex_blackhole = bs.gettexture('circleOutlineNoAlpha')
        self.tex_curse_impact = bs.gettexture('powerupCurse')
        self.tex_tele_impact = bs.gettexture('achievementOnslaught')
        self.tex_shock_bomb = bs.gettexture('heart')
        self.tex_weed_bomb = bs.gettexture('levelIcon')
        self.tex_blast_bomb = bs.gettexture('crossOutMask')
        self.tex_boom_bomb = bs.gettexture('settingsIcon')
        self.tex_cursy_bomb = bs.gettexture('powerupCurse')
        self.tex_revenge_bomb = bs.gettexture('menuButton')
        self.tex_headhache = bs.gettexture('achievementEmpty')
        self.tex_flyer = bs.gettexture('buttonPickUp')
        self.tex_beach_ball = bs.gettexture('achievementFootballShutout')
        self.health_powerup_sound = bs.getsound('healthPowerup')
        self.powerup_sound = bs.getsound('powerup01')
        self.powerdown_sound = bs.getsound('powerdown01')
        self.drop_sound = bs.getsound('boxDrop')

        # Material for powerups.
        self.powerup_material = bs.Material()

        # Material for anyone wanting to accept powerups.
        self.powerup_accept_material = bs.Material()

        # Pass a powerup-touched message to applicable stuff.
        self.powerup_material.add_actions(
            conditions=('they_have_material', self.powerup_accept_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('message', 'our_node', 'at_connect', _TouchedMessage()),
            ),
        )

        # We don't wanna be picked up.
        self.powerup_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'collide', False),
        )

        self.powerup_material.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=('impact_sound', self.drop_sound, 0.5, 0.1),
        )

        self._powerupdist: list[str] = []
        for powerup, freq in get_default_powerup_distribution():
            for _i in range(int(freq)):
                self._powerupdist.append(powerup)

    def get_random_powerup_type(
        self,
        forcetype: str | None = None,
        excludetypes: list[str] | None = None,
    ) -> str:
        """Returns a random powerup type (string).

        See bs.Powerup.poweruptype for available type values.

        There are certain non-random aspects to this; a 'curse' powerup,
        for instance, is always followed by a 'health' powerup (to keep things
        interesting). Passing 'forcetype' forces a given returned type while
        still properly interacting with the non-random aspects of the system
        (ie: forcing a 'curse' powerup will result
        in the next powerup being health).
        """
        if excludetypes is None:
            excludetypes = []
        if forcetype:
            ptype = forcetype
        else:
            # If the last one was a curse, make this one a health to
            # provide some hope.
            if self._lastpoweruptype == 'curse':
                ptype = 'health'
            else:
                while True:
                    ptype = self._powerupdist[
                        random.randint(0, len(self._powerupdist) - 1)
                    ]
                    if ptype not in excludetypes:
                        break
        self._lastpoweruptype = ptype
        return ptype

    @classmethod
    def get(cls) -> PowerupBoxFactory:
        """Return a shared bs.PowerupBoxFactory object, creating if needed."""
        activity = bs.getactivity()
        if activity is None:
            raise bs.ContextError('No current activity.')
        factory = activity.customdata.get(cls._STORENAME)
        if factory is None:
            factory = activity.customdata[cls._STORENAME] = PowerupBoxFactory()
        assert isinstance(factory, PowerupBoxFactory)
        return factory


class NewPowerupBox(bs.Actor):
    """A box that grants a powerup.

    This will deliver a :class:`~bascenev1.PowerupMessage` to anything
    that touches it which has the
    :class:`~PowerupBoxFactory.powerup_accept_material` applied.
    """

    #: The string powerup type. This can be 'triple_bombs', 'punch',
    #: 'ice_bombs', 'impact_bombs', 'land_mines', 'sticky_bombs',
    #: 'shield', 'health', or 'curse'.
    poweruptype: str

    node: bs.Node
    """The 'prop' node representing this box."""

    def __init__(
        self,
        position: Sequence[float] = (0.0, 1.0, 0.0),
        poweruptype: str = 'triple_bombs',
        expire: bool = True,
    ):
        """Create a powerup-box of the requested type at the given position.

        see bs.Powerup.poweruptype for valid type strings.
        """

        super().__init__()
        shared = SharedObjects.get()
        factory = PowerupBoxFactory.get()
        self.poweruptype = poweruptype
        self._powersgiven = False

        if poweruptype == 'triple_bombs':
            tex = factory.tex_bomb
            name = "TripleBombs"
        elif poweruptype == 'punch':
            tex = factory.tex_punch
            name = "Punch"
        elif poweruptype == 'ice_bombs':
            tex = factory.tex_ice_bombs
            name = "IceBombs"
        elif poweruptype == 'impact_bombs':
            tex = factory.tex_impact_bombs
            name = "ImpactBombs"
        elif poweruptype == 'land_mines':
            tex = factory.tex_land_mines
            name = "LandMines"
        elif poweruptype == 'sticky_bombs':
            tex = factory.tex_sticky_bombs
            name = "StickyBombs"
        elif poweruptype == 'shield':
            tex = factory.tex_shield
            name = "Shield"
        elif poweruptype == 'health':
            tex = factory.tex_health
            name = "Health"
        elif poweruptype == 'curse':
            tex = factory.tex_curse
            name = "Curse"
        #
        #new pwps
        #
        elif poweruptype == 'slow':
            tex = factory.tex_slow
            name = 'SlowMo'
        elif poweruptype == 'champ':
            tex = factory.tex_champ
            name = 'Champ'
        elif poweruptype == 'speed':
            tex = factory.tex_speed
            name = 'Speed'
        elif poweruptype == 'spunch':
            tex = factory.tex_spunch
            name = 'Spunch'
        elif poweruptype == 'radius':
            tex = factory.tex_radius
            name = 'Radius'
        elif poweruptype == 'multi_bomb':
            tex = factory.tex_multibomb
            name = 'MultiBombs'
        elif poweruptype == 'xtraLife':
            tex = factory.tex_xtraLife
            name = 'XtraLyfe'
        elif poweruptype == 'lowLife':
            tex = factory.tex_lowLife
            name = random.choice(['Health', 'Potion', 'XtraLyfe','Champ']) #let it be unpredictable
        elif poweruptype == 'martyrdom':
            tex = factory.tex_martyrdom
            name = 'Martyrdom'
        elif poweruptype == 'tnt':
            tex = factory.tex_tnt
            name = 'Tnt'
        elif poweruptype == 'ice_impact':
            tex = factory.tex_ice_impact
            name = 'IceImpact'
        elif poweruptype == 'sticky_ice':
            tex = factory.tex_sticky_ice
            name = 'StickyIce'
        elif poweruptype == 'curse_mine':
            tex = factory.tex_curse_mine
            name = 'CurseMine'
        elif poweruptype == 'ice_mine':
            tex = factory.tex_ice_mine
            name = 'IceMine'
        elif poweruptype == 'blackhole':
            tex = factory.tex_blackhole
            name = 'Blackhole'
        elif poweruptype == 'curse_impact':
            tex = factory.tex_curse_impact
            name = 'CurseImpact'
        elif poweruptype == 'tele_impact':
            tex = factory.tex_tele_impact
            name = 'Tele-Impact'
        elif poweruptype == 'shock_bomb':
            tex = factory.tex_shock_bomb
            name = 'ShockBomb'
        elif poweruptype == 'glue_bomb':
            tex = factory.tex_glue_bomb
            name = 'GlueBomb'
        elif poweruptype == 'weed_bomb':
            tex = factory.tex_weed_bomb
            name = 'WeedBomb'
        elif poweruptype == 'blast_bomb':
            tex = factory.tex_blast_bomb
            name = 'BlastBomb'
        elif poweruptype == 'boom_bomb':
            tex = factory.tex_boom_bomb
            name = 'BoomBomb'
        elif poweruptype == 'cursy_bomb':
            tex = factory.tex_cursy_bomb
            name = 'CursyBomb'
        elif poweruptype == 'revenge_bomb':
            tex = factory.tex_revenge_bomb
            name = 'Revenge'
        elif poweruptype == 'headache':
            tex = factory.tex_headhache
            name = 'Headlock'
        elif poweruptype == 'flyer':
            tex = factory.tex_flyer
            name = 'Flyer'
        elif poweruptype == 'beachball':
            tex = factory.tex_beach_ball
            name = 'BotMod'
        else:
            name = "INVALID"
            raise ValueError('invalid poweruptype: ' + str(poweruptype))

        if len(position) != 3:
            raise ValueError('expected 3 floats for position')

        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'body': 'box',
                'position': position,
                'mesh': factory.mesh,
                'light_mesh': factory.mesh_simple,
                'shadow_size': 0.5,
                'color_texture': tex,
                'reflection': 'powerup',
                'reflection_scale': [1.0],
                'materials': (factory.powerup_material, shared.object_material),
            },
        )
        
        # global configs  --> port to mighty fire.py soon
        
        # text on powerup
        if pwp.text:
            text = bs.newnode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})        
            self.node.connectattr('position', text, 'input2')
            self.spazText = bs.newnode('text',
                             owner=self.node,
                             attrs={
                                'text': str(name),
                                'in_world': True,
                                'color': (1,1,1),
                                'shadow': 1.0,
                                'flatness': 1.0,
                                'scale': 0.012,
                                'h_align': 'center',
                             })
            text.connectattr('output', self.spazText, 'position')
            bs.animate(self.spazText, 'scale', {0:0, 0.2:0, 0.6:0.014, 0.8:0.010})
            if pwp.light:
                bs.animate_array(node=self.spazText, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)
       
        
        
        # shield on powerup
        if pwp.shield:
            self.shield = bs.newnode('shield',
                                 owner=self.node,
                                 attrs={
                                     'color': ((0+random.random()*5.0),(0+random.random()*5.0),(0+random.random()*5.0)),
                                     'radius': 1.2})
            self.node.connectattr('position', self.shield, 'position')
            if pwp.light:
                bs.animate_array(node=self.shield, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)


        # pwp expiration text
        if pwp.expire_text:
            if pwp.text:
                # if pwp text on, go a bit higher
                text = bs.newnode('math', owner=self.node, attrs={'input1': (0, 1.15, 0), 'operation': 'add'})  
            else:
                # come down to pwp text lvl if pwp text is off
                text = bs.newnode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})  
            self.node.connectattr('position', text, 'input2')
            self.spazText = bs.newnode('text',
                             owner=self.node,
                             attrs={
                                'text': '',
                                'in_world': True,
                                'color': (1,1,1),
                                'shadow': 1.0,
                                'flatness': 1.0,
                                'scale': 0.012,
                                'h_align': 'center',
                             })
            text.connectattr('output', self.spazText, 'position')
            bs.animate(self.spazText, 'scale', {0:0, 0.2:0, 0.6:0.014, 0.8:0.010})
            # timer logic
            self._pwp_time_left = int(DEFAULT_POWERUP_INTERVAL-1)
            def _update_powerup_timer():
                if not self.spazText or not self.spazText.exists():
                     # Node might be gone (player died, powerup removed, etc)
                    return 
                    
                if self._pwp_time_left <= 0:
                    self.spazText.text = ''
                    return
                    
                self.spazText.text = f'{self._pwp_time_left}'
                self._pwp_time_left -= 1
                
            _update_powerup_timer()
            bs.timer(1.0, _update_powerup_timer, repeat=True)
        
        # pwp gravity - raises pwp by a bit, for fun i guess
        if pwp.grav:
            self.node.gravity_scale = 0
            
        # pwp explosive start
        if pwp.explo:        
            velocity=(0, 0, 0)
            explosion = bs.newnode("explosion", attrs={
                'position': self.node.position,
                'color': ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                'velocity': (velocity[0], max(-1.0, velocity[1]), velocity[2]),
                'radius': (1.3)})

        # extra pwp flash animation --> improved compared to 1.4
        if pwp.flash:        
            m = bs.newnode('math', owner=self.node, attrs={'input1': (0, 0.0, 0), 'operation': 'add'})
            self.node.connectattr('position', m, 'input2')
            self.flash = bs.newnode("flash",
                        owner=self.node,
                        attrs={'position':self.node.position,
                               'size':0.7,
                               'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
            m.connectattr('output', self.flash, 'position') 
            bs.animate_array(node=self.flash, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)
            
            def flash_timer():
                if self.flash and self.flash.exists():
                    self.flash.delete()
                    # del after 7 sec
            bs.timer(7, flash_timer)

        # Animate in.
        if pwp.flash: # make the box invisible only when flash enabled
            curve = bs.animate(self.node, 'mesh_scale', {0: 0, 0.14: 0, 0.2: 0})
        else:
            curve = bs.animate(self.node, 'mesh_scale', {0: 0, 0.14: 1.6, 0.2: 1})
        bs.timer(0.2, curve.delete)

        if expire:
            bs.timer(
                DEFAULT_POWERUP_INTERVAL - 2.5,
                bs.WeakCallStrict(self._start_flashing),
            )
            bs.timer(
                DEFAULT_POWERUP_INTERVAL - 1.0,
                bs.WeakCallStrict(self.handlemessage, bs.DieMessage()),
            )

    def _start_flashing(self) -> None:
        if self.node:
            self.node.flashing = True

    @override
    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired

        if isinstance(msg, bs.PowerupAcceptMessage):
            factory = PowerupBoxFactory.get()
            assert self.node
            if self.poweruptype == 'health':
                factory.health_powerup_sound.play(
                    3, position=self.node.position
                )

            factory.powerup_sound.play(3, position=self.node.position)
            activity=get_foreground_host_activity()
            if self.poweruptype == 'slow': # first pwp to be added
                if activity.globalsnode.slow_motion==True:
                    activity.globalsnode.slow_motion=False
                    activity.globalsnode.tint=(1, 1, 1)
                    bs.broadcastmessage('Slow motion turned off!')
                else:
                    activity.globalsnode.slow_motion=True
                    activity.globalsnode.tint=(0.5, 0.7, 1.0)
                    bs.broadcastmessage('Slow motion turned on!')
            self._powersgiven = True
            self.handlemessage(bs.DieMessage())

        elif isinstance(msg, _TouchedMessage):
            if pwp.accept_powerup:
                if not self._powersgiven:
                    node = bs.getcollision().opposingnode
                    node.handlemessage(
                        bs.PowerupMessage(self.poweruptype, sourcenode=self.node)
                    )

        elif isinstance(msg, bs.DieMessage):
            if self.node:
                if msg.immediate:
                    self.node.delete()
                else:
                    if pwp.flash: # dont even show a bit for flash on death
                        bs.animate(self.node, 'mesh_scale', {0: 0, 0.1: 0})
                    else:
                        bs.animate(self.node, 'mesh_scale', {0: 0, 0.1: 0})
                    bs.timer(0.1, self.node.delete)

        elif isinstance(msg, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage())

        elif isinstance(msg, bs.HitMessage):
            # Don't die on punches (that's annoying).
            if msg.hit_type != 'punch':
                self.handlemessage(bs.DieMessage())
        else:
            return super().handlemessage(msg)
        return None

def new_get_default_powerup_distribution():
    """Standard set of powerups."""
    return (
        ('triple_bombs', 3),
        ('ice_bombs', 2),
        ('punch', 2),
        ('impact_bombs', 2),
        ('land_mines', 2),
        ('sticky_bombs', 2),
        ('shield', 2),
        ('health', 1),
        ('curse', 1),
        #
        #new pwp
        #
        ('slow', 2),
        ('champ', 2),
        ('speed', 2),
        ('spunch',2),
        ('radius', 2),
        ('multi_bomb',2),
        ('xtraLife',2),
        ('lowLife',2),
        ('martyrdom',2),
        ('tnt',2),
        ('blackhole',2),
        ('flyer',2),
        ('beachball',2), # turned to BotMod!
        #
        # new bombs
        #
        ('ice_impact',2),
        ('sticky_ice',2),
        ('curse_mine',2),
        ('ice_mine',2),
        ('curse_impact',2),
        ('tele_impact',2),
        ('shock_bomb',2),
        ('glue_bomb',2),
        ('weed_bomb',2),
        ('blast_bomb',2),
        ('boom_bomb',2),
        ('cursy_bomb',2),
        ('revenge_bomb',2),
        ('headache',0), #not working due to huge bug !
    )

def enable_pwps():
    powerupbox.PowerupBox = NewPowerupBox
    powerupbox.PowerupBoxFactory = NewPowerupBoxFactory
    bs.get_default_powerup_distribution = new_get_default_powerup_distribution
    bs._powerup.get_default_powerup_distribution = new_get_default_powerup_distribution