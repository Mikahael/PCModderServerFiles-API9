from __future__ import annotations

import random
import logging
from typing import TYPE_CHECKING, override
#
import bascenev1lib
import bascenev1 as bs
import os, shutil
import babase
from bascenev1lib.actor import spaz
from bascenev1lib.actor.spaz import Spaz, SpazFactory, BombDiedMessage, CurseExplodeMessage, PunchHitMessage, PickupMessage
#
#
from bascenev1lib.actor.bomb import Bomb, Blast
from bascenev1lib.actor.popuptext import PopupText as pptx
from bascenev1lib.actor.powerupbox import PowerupBoxFactory, PowerupBox
from bascenev1lib.actor.spazfactory import SpazFactory
from bascenev1lib.gameutils import SharedObjects
#
from config import spaz_config as spz
#
screenmessage = bs.broadcastmessage
#
POWERUP_WEAR_OFF_TIME = 20000

# Obsolete - just used for demo guy now.
BASE_PUNCH_POWER_SCALE = 1.2
BASE_PUNCH_COOLDOWN = 400

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable #updated to api 9
   
   
oldSpazInit = Spaz.__init__
def newSpazInit(self, *args, **kwargs):
    oldSpazInit(self, *args, **kwargs)
    #if True:
        #k = self.node.name# the module works but this code not working
        #self.node.name = u'\ue048'+k
    self.ice_impact_count = 0
    self.curse_impact_count = 0
    self.tele_impact_count = 0
    self.curse_mine_count = 0
    self.ice_mine_count = 0
    self.shock_count = 0
    self.boom_bomb_count = 0
    self.headache_count = 0
    self.bomb_count = 2
    if spz.gloves: self.equip_boxing_gloves()
    if spz.shield: self.equip_shields()
    #
    # for ezy char pull
    #
    
    def pull_char(char):
        char = char  
        tex = bs.gettexture
        get = bs.getmesh       
        self.node.head_mesh = get(char+'Head')
        self.node.color_texture = tex(char+'Color')   
        self.node.color_mask_texture = tex(char+'ColorMask')  
        self.node.torso_mesh = get(char+'Torso')               
        self.node.hand_mesh = get(char+'Hand')
        self.node.upper_arm_mesh = get(char+'UpperArm')
        self.node.lower_leg_mesh = get(char+'LowerLeg')
        self.node.upper_leg_mesh = get(char+'UpperLeg')
        self.node.forearm_mesh = get(char+'ForeArm')
        self.node.toes_mesh = get(char+'Toes')
        if char =='santa':
            self.node.pelvis_mesh = get('kronkPelvis')  
        else:
            self.node.pelvis_mesh = get(char+'Pelvis')
        self.node.style = char  

    if spz.ninja: pull_char(char='ninja')
    if spz.frosty: pull_char(char='frosty')
    if spz.wizard: pull_char(char='wizard')
    if spz.ali: pull_char(char='ali')
    if spz.santa: pull_char(char='santa')
    if spz.robot: pull_char(char='robot')
    if spz.pengu: pull_char(char='pengu')
    if spz.pixie: pull_char(char='pixie')
    
    self.random_bombs = False #for rando bombs
    self.random_colors = False #for rando colors
    self.random_characters = False #for rando chars
    self.fall_protect = False #for fall protection
    self.allow_powerup = True #config to allow players accept pwp
        
        
def new_handlemessage(self, msg: Any) -> Any:
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        assert not self.expired

        if isinstance(msg, bs.PickedUpMessage):
            if self.node:
                self.node.handlemessage('hurt_sound')
                self.node.handlemessage('picked_up')

            # This counts as a hit.
            self._num_times_hit += 1

        elif isinstance(msg, bs.ShouldShatterMessage):
            # Eww; seems we have to do this in a timer or it wont work right.
            # (since we're getting called from within update() perhaps?..)
            # NOTE: should test to see if that's still the case.
            bs.timer(0.001, bs.WeakCallStrict(self.shatter))

        elif isinstance(msg, bs.ImpactDamageMessage):
            # Eww; seems we have to do this in a timer or it wont work right.
            # (since we're getting called from within update() perhaps?..)
            bs.timer(0.001, bs.WeakCallStrict(self._hit_self, msg.intensity))

        elif isinstance(msg, bs.PowerupMessage):
            if self._dead or not self.node:
                return True
            if self.allow_powerup == False:
                # show message only once
                if not hasattr(self, '_shown_msg'):
                    self._shown_msg = True
                    pptx('No PWP for U!',color=(1, 1, 1), scale=1.0,position=self.node.position,).autoretain()
                return None
            if self.pick_up_powerup_callback is not None:
                self.pick_up_powerup_callback(self)
            if spz.popuptext:
                if msg.poweruptype == 'headache':
                    pptx("Random Bombs!",
                        color=(1, 1, 1),
                        scale=1.0,
                        position=self.node.position,
                    ).autoretain()      
                elif msg.poweruptype == 'glowy':
                    pptx("Press Punch!",
                        color=(1, 1, 1),
                        scale=1.0,
                        position=self.node.position,
                    ).autoretain()            
                elif msg.poweruptype == 'rchar':
                    pptx("Press Pickup!",
                        color=(1, 1, 1),
                        scale=1.0,
                        position=self.node.position,
                    ).autoretain()                       
                else:
                    pptx(msg.poweruptype.upper() + "!",
                        color=(1, 1, 1),
                        scale=1.0,
                        position=self.node.position,
                    ).autoretain()
            if spz.lightning:
                self.light = bs.newnode('light', attrs={'position': self.node.position, 'color': (1.2, 1.2, 1.4), 'volume_intensity_scale': 2.35, 'intensity': 0.0})
                bs.animate(self.light, 'intensity', {0.0: 0.0, 0.07: 0.5, 0.35: 0.0})
                bs.timer(0.5, self.light.delete)

            if msg.poweruptype == 'triple_bombs':
                tex = PowerupBoxFactory.get().tex_bomb
                self._flash_billboard(tex)
                self.set_bomb_count(3)
                if self.powerups_expire:
                    self.node.mini_billboard_1_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_1_start_time = t_ms
                    self.node.mini_billboard_1_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._multi_bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._multi_bomb_wear_off_flash),
                    )
                    self._multi_bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._multi_bomb_wear_off),
                    )
            elif msg.poweruptype == 'land_mines':
                self.set_land_mine_count(min(self.land_mine_count + 3, 3))
            elif msg.poweruptype == 'impact_bombs':
                self.bomb_type = 'impact'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'sticky_bombs':
                self.bomb_type = 'sticky'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'punch':
                tex = PowerupBoxFactory.get().tex_punch
                self._flash_billboard(tex)
                self.equip_boxing_gloves()
                if self.powerups_expire and not self.default_boxing_gloves:
                    self.node.boxing_gloves_flashing = False
                    self.node.mini_billboard_3_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_3_start_time = t_ms
                    self.node.mini_billboard_3_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._boxing_gloves_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._gloves_wear_off_flash),
                    )
                    self._boxing_gloves_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._gloves_wear_off),
                    )
            elif msg.poweruptype == 'shield':
                factory = SpazFactory.get()

                # Let's allow powerup-equipped shields to lose hp over time.
                self.equip_shields(decay=factory.shield_decay_rate > 0)
            elif msg.poweruptype == 'curse':
                self.curse()
            elif msg.poweruptype == 'ice_bombs':
                self.bomb_type = 'ice'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'sticky_ice':
                self.bomb_type = 'sticky_ice'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'glue_bomb':
                self.bomb_type = 'glue_bomb'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'revenge_bomb':
                self.bomb_type = 'revenge_bomb'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'cursy_bomb':
                self.bomb_type = 'cursy_bomb'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'weed_bomb':
                self.bomb_type = 'weed_bomb'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'blast_bomb':
                self.bomb_type = 'blast_bomb'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = int(bs.time() * 1000.0)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = bs.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000) / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off_flash),
                    )
                    self._bomb_wear_off_timer = bs.Timer(
                        POWERUP_WEAR_OFF_TIME / 1000.0,
                        bs.WeakCallStrict(self._bomb_wear_off),
                    )
            elif msg.poweruptype == 'health':
                if self._cursed:
                    self._cursed = False

                    # Remove cursed material.
                    factory = SpazFactory.get()
                    for attr in ['materials', 'roller_materials']:
                        materials = getattr(self.node, attr)
                        if factory.curse_material in materials:
                            setattr(
                                self.node,
                                attr,
                                tuple(
                                    m
                                    for m in materials
                                    if m != factory.curse_material
                                ),
                            )
                    self.node.curse_death_time = 0
                self.hitpoints = self.hitpoints_max
                self._flash_billboard(PowerupBoxFactory.get().tex_health)
                self.node.hurt = 0
                self._last_hit_time = None
                self._num_times_hit = 0
                
            elif msg.poweruptype == 'heal':# for boom bomb
                if self._cursed:
                    self._cursed = False

                    # Remove cursed material.
                    factory = SpazFactory.get()
                    for attr in ['materials', 'roller_materials']:
                        materials = getattr(self.node, attr)
                        if factory.curse_material in materials:
                            setattr(
                                self.node,
                                attr,
                                tuple(
                                    m
                                    for m in materials
                                    if m != factory.curse_material
                                ),
                            )
                    self.node.curse_death_time = 0
                self.hitpoints = self.hitpoints_max
                #self._flash_billboard(PowerupBoxFactory.get().tex_health)
                self.node.hurt = 0
                self._last_hit_time = None
                self._num_times_hit = 0
                
            elif msg.poweruptype == 'champ':
                self.equip_boxing_gloves()
                self.equip_shields()
                self.node.handlemessage('knockout', 500.0)
            elif msg.poweruptype == 'speed':
                if self.blast_radius != 5.5 and self._punch_cooldown != 130 and self.node.hockey == False:
                    screenmessage('Speed turned on')
                    self.node.hockey = True

                    SPEED_INTERVAL = 15
                    self._speed_time_left = SPEED_INTERVAL

                    # Remove old text
                    if hasattr(self, 'spazText') and self.spazText.exists():
                        self.spazText.delete()

                    text_math = bs.newnode(
                        'math',
                        owner=self.node,
                        attrs={'input1': (0, 0.7, 0), 'operation': 'add'}
                    )
                    self.node.connectattr('position', text_math, 'input2')

                    self.spazText = bs.newnode(
                        'text',
                        owner=self.node,
                        attrs={
                            'text': str(self._speed_time_left),
                            'in_world': True,
                            'color': (1, 1, 1),
                            'shadow': 1.0,
                            'flatness': 1.0,
                            'scale': 0.012,
                            'h_align': 'center',
                        }
                    )
                    text_math.connectattr('output', self.spazText, 'position')

                    def _speed_tick():
                        # Player gone or speed already off
                        if not self.node or not self.node.hockey:
                            return

                        self._speed_time_left -= 1

                        if self._speed_time_left <= 0:
                            self.spazText.text = ''
                            self.node.hockey = False
                            screenmessage('Speed turned off')
                            return

                        self.spazText.text = str(self._speed_time_left)

                        # Schedule next tick (ONE-SHOT)
                        bs.timer(1.0, _speed_tick)

                    # Start countdown
                    bs.timer(1.0, _speed_tick)
                else:
                    if self.blast_radius == 5.5:
                        screenmessage('Already have radius!')
                    elif self._punch_cooldown == 130:
                        screenmessage('Already have spunch!')
                    elif self.node.hockey == True:
                        screenmessage('Already have speed!')
            elif msg.poweruptype == 'spunch':
                if self.node.hockey == False and self.blast_radius != 5.5 and self._punch_cooldown != 130:
                    screenmessage('Spunch turned on')
                    self._punch_power_scale = 0.75
                    self._punch_cooldown = 130
                    SPUNCH_INTERVAL = 15
                    self._spunch_time_left = SPUNCH_INTERVAL

                    # Remove old text
                    if hasattr(self, 'spazText') and self.spazText.exists():
                        self.spazText.delete()

                    text_math = bs.newnode(
                        'math',
                        owner=self.node,
                        attrs={'input1': (0, 0.7, 0), 'operation': 'add'}
                    )
                    self.node.connectattr('position', text_math, 'input2')

                    self.spazText = bs.newnode(
                        'text',
                        owner=self.node,
                        attrs={
                            'text': str(self._spunch_time_left),
                            'in_world': True,
                            'color': (1, 1, 1),
                            'shadow': 1.0,
                            'flatness': 1.0,
                            'scale': 0.012,
                            'h_align': 'center',
                        }
                    )
                    text_math.connectattr('output', self.spazText, 'position')

                    def _spunch_tick():
                        # Player gone or speed already off
                        if not self.node or not self.spazText.exists():
                            return

                        self._spunch_time_left -= 1

                        if self._spunch_time_left <= 0:
                            self.spazText.text = ''
                            factory = SpazFactory.get()
                            self._punch_power_scale = factory.punch_power_scale
                            self._punch_cooldown = factory.punch_cooldown
                            screenmessage('Speed turned off')
                            return

                        self.spazText.text = str(self._spunch_time_left)
                        #
                        bs.timer(1.0, _spunch_tick)
                    bs.timer(1.0, _spunch_tick)
                else:
                    if self.node.hockey == True:
                        screenmessage('Already have boots')
                    elif self.blast_radius == 5.5:
                        screenmessage('Already have radius')
                    elif self._punch_cooldown == 130:
                        screenmessage('Already have spunch!')
            elif msg.poweruptype == 'radius':
                if self.node.hockey == False and self._punch_cooldown != 130 and self.blast_radius != 5.5:
                    screenmessage('BlastRadius increased')
                    self.blast_radius = 5.5
                    RADIUS_INTERVAL = 15
                    self._radius_time_left = RADIUS_INTERVAL

                    # Remove old text
                    if hasattr(self, 'spazText') and self.spazText.exists():
                        self.spazText.delete()

                    text_math = bs.newnode(
                        'math',
                        owner=self.node,
                        attrs={'input1': (0, 0.7, 0), 'operation': 'add'}
                    )
                    self.node.connectattr('position', text_math, 'input2')

                    self.spazText = bs.newnode(
                        'text',
                        owner=self.node,
                        attrs={
                            'text': str(self._radius_time_left),
                            'in_world': True,
                            'color': (1, 1, 1),
                            'shadow': 1.0,
                            'flatness': 1.0,
                            'scale': 0.012,
                            'h_align': 'center',
                        }
                    )
                    text_math.connectattr('output', self.spazText, 'position')

                    def _radius_tick():
                        # Player gone or speed already off
                        if not self.node or not self.spazText.exists():
                            return

                        self._radius_time_left -= 1

                        if self._radius_time_left <= 0:
                            self.spazText.text = ''
                            self.blast_radius = 2.0
                            screenmessage('Radius turned off')
                            return

                        self.spazText.text = str(self._radius_time_left)
                        #
                        bs.timer(1.0, _radius_tick)
                    bs.timer(1.0, _radius_tick)
                else:
                    if self.node.hockey == True:
                        screenmessage('Already have speed boots!')
                    elif self._punch_cooldown == 130:
                        screenmessage('Already have spunch!')
                    elif self.blast_radius == 5.5:
                        screenmessage('Already have radius!')
            elif msg.poweruptype == 'multi_bomb':
                # hehe perm
                self.set_bomb_count(999)
            elif msg.poweruptype == 'xtraLife':                
                self.hitpoints += 800
                self.node.hurt = (1.0 - float(self.hitpoints) / self.hitpoints_max)
                screenmessage('+800 HP')
            elif msg.poweruptype == 'lowLife':                
                #self.hitpoints -= 500
                #self.node.hurt = (1.0 + float(self.hitpoints) / self.hitpoints_max)
                #screenmessage('-500 HP')
                def drop_bomb():
                    from bomb.newbomb import NewBomby
                    bomb = NewBomby(
                        position=(self.node.position),
                        velocity=(self.node.velocity),
                        bomb_type='sticky',
                        blast_radius=self.blast_radius,
                        source_player=self.source_player,
                        owner=self.node,
                        ).autoretain()
                drop_bomb()
            elif msg.poweruptype == 'martyrdom': #ported to 1.9 :)
                    self._martyrdom_dropped = False
                    def drop_bomb():
                        from bomb.newbomb import NewBomby

                        x, y, z = self.last_death_pos
                        offsets = (
                            (0.43, 4, -0.25),
                            (-0.43, 4, -0.25),
                            (0.0, 4, 0.5),
                        )

                        for ox, oy, oz in offsets:
                            NewBomby(
                                position=(x + ox, y + oy, z + oz),
                                velocity=(0, -6, 0),
                                bomb_type='sticky',
                                blast_radius=self.blast_radius,
                                source_player=self.source_player,
                                owner=self.node,
                            ).autoretain()

                    def valid_killer():
                        return (
                            (self.last_player_held_by is not None
                             and self.last_player_held_by.exists())
                            or
                            (self.last_player_attacked_by is not None
                             and self.last_player_attacked_by.exists()
                             and bs.time() - self.last_attacked_time < 4.0)
                        )

                    def check_dead():
                        if self._martyrdom_dropped:
                            return

                        if self.hitpoints > 0:
                            return

                        if not valid_killer():
                            return

                        try:
                            self.last_death_pos = self.node.position
                        except Exception:
                            return

                        if self.last_player_attacked_by == self.node:
                            return

                        self._martyrdom_dropped = True
                        drop_bomb()

                        if self.dropss is not None:
                            self.dropss = None

                    def check_val():
                        if not self.is_alive():
                            return
                        text_math = bs.newnode(
                            'math',
                            owner=self.node,
                            attrs={'input1': (0, 1.3, 0), 'operation': 'add'}
                        )
                        self.node.connectattr('position', text_math, 'input2')
                        activated_text = pptx(
                            text="Activated",
                            offset=(0,-1,0),
                            color=(1, 1, 1),
                            scale=1.0
                        ).autoretain()
                        text_math.connectattr('output', activated_text.node, 'position')
                        self.is_dropped = True
                        self.dropss = bs.timer(0.1, check_dead, repeat=True)

                    check_val()
            elif msg.poweruptype == "tnt": #hehe why not for fun!
                from bomb.newbomb import NewBomby
                p = self.node.position_forward
                bomb = NewBomby(
                        position=(p[0]+0.43,p[1]+4,p[2]-0.25),
                        velocity=(0,-6,0),
                        bomb_type='tnt',
                        bomb_scale=1.25,
                        blast_radius=self.blast_radius,
                        source_player=self.source_player,
                        owner=self.node,
                        ).autoretain()
            elif msg.poweruptype == 'shock': # hehe ported shockwave
                def drop():
                    from spaz import define_objects as obj
                    obj.ShockWave(position = (self.node.position[0],self.node.position[1]-0.5,self.node.position[2]))
                bs.timer(0.1, drop, repeat=False)
                bs.timer(0.3, drop, repeat=False)
                bs.timer(0.5, drop, repeat=False)
                
            elif msg.poweruptype == 'blackhole': # for blackhole
                from spaz import define_objects as obj
                p = self.node.position_forward
                obj.BlackHole((p[0],p[1]+2,p[2])).autoretain()
                
            elif msg.poweruptype == 'ice_impact':
                self.set_ice_impact_count(min(self.ice_impact_count + 3, 3))
            elif msg.poweruptype == 'tele_impact':
                self.set_tele_impact_count(min(self.tele_impact_count + 2, 2))
            elif msg.poweruptype == 'curse_impact':
                self.set_curse_impact_count(min(self.curse_impact_count + 3, 3))
            elif msg.poweruptype == 'curse_mine':
                self.set_curse_mine_count(min(self.curse_mine_count + 3, 3))
            elif msg.poweruptype == 'ice_mine':
                self.set_ice_mine_count(min(self.ice_mine_count + 3, 3))
            elif msg.poweruptype == 'shock_bomb':
                self.set_shock_count(min(self.shock_count + 5, 5))
            elif msg.poweruptype == 'headache':
                self.random_bombs = True #random bombs equipped
                if not spz.popuptext:
                    pptx('Random Bombs!',color=(1, 1, 1), scale=1.0,position=self.node.position,).autoretain()
            elif msg.poweruptype == 'glowy':
                self.random_colors = True #random colors at punch
                if not spz.popuptext:
                    pptx('Press Punch!',color=(1, 1, 1), scale=1.0,position=self.node.position,).autoretain()
            elif msg.poweruptype == 'rchar':
                self.random_characters = True #random characters at pickup
                if not spz.popuptext:
                    pptx('Press Pickup!',color=(1, 1, 1), scale=1.0,position=self.node.position,).autoretain()
            elif msg.poweruptype == 'weed':
                def weed():
                    if self.is_alive():
                        self.node.handlemessage('knockout', 10000)

                for t in (2.0, 5.5, 8.5):
                    bs.timer(t, weed)

                def hiccups():
                    if self.is_alive():
                        node = self.node
                        bs.emitfx(
                            position=(node.position[0], node.position[1] - 1.2, node.position[2]),
                            velocity=(0, 0.05, 0),
                            count=random.randrange(100, 270),
                            scale=1.0 + random.random(),
                            spread=0.71,
                            chunk_type='sweat',
                        )

                for t in (1.0, 2.5, 5.0, 7.5):
                    bs.timer(t, hiccups)

                def popup(text, scale, times):
                    for t in times:
                        bs.timer(
                            t,
                            lambda txt=text, sc=scale: (
                                self.is_alive()
                                and pptx(
                                    txt,
                                    color=(1, 1, 1),
                                    scale=sc,
                                    random_offset=0.2,
                                    position=(
                                        self.node.position[0],
                                        self.node.position[1] - 1.2,
                                        self.node.position[2],
                                    ),
                                ).autoretain()
                            ),
                        )

                popup('high', 0.7, (1.5, 3.0, 8.0))
                popup('OO', 0.75, (1.46, 2.96, 5.46, 7.96))
                
            elif msg.poweruptype == 'boom':
                p = self.node.position_forward
                Blast(
                    position=(p[0], p[1] - 1.0, p[2]),
                    velocity=(0, 1, 0),
                    blast_radius=2.0,
                    blast_type='impact',
                    source_player=None,
                    hit_type='punch',
                ).autoretain()

                self.node.handlemessage(bs.PowerupMessage(poweruptype='heal'))

                def boom_heal():
                    if self.is_alive():
                        self.node.handlemessage(bs.PowerupMessage(poweruptype='heal'))
                        pptx(
                            'Healed up!',
                            color=(1, 1, 1),
                            scale=1.0,
                            position=self.node.position,
                        ).autoretain()

                for t in (1.0, 1.5, 2.5):
                    bs.timer(t, boom_heal)

            elif msg.poweruptype == 'boom_bomb':
                self.set_boom_bomb_count(min(self.boom_bomb_count + 5, 5))
                
            elif msg.poweruptype == 'cursy':
                def apply_curse():
                    if not self.is_alive():
                        return

                    self.node.handlemessage(
                        bs.PowerupMessage(
                            poweruptype=random.choice(('curse', 'health'))
                        )
                    )
                # repeating timer (stored so it can be cancelled if needed)
                self._cursy_timer = bs.Timer(0.35, apply_curse, repeat=True)
                
            elif msg.poweruptype == 'revenge_hit':
                def popup(text):
                    if self.is_alive():
                        pptx(
                            text,
                            color=(1, 1, 1),
                            scale=1.0,
                            position=self.node.position,
                        ).autoretain()
                        bs.emitfx(position=self.node.position, count=20, scale=0.5, spread=0.5, chunk_type='spark')

                popup('4 Sec to Revenge!')

                # countdown popups
                for i in range(1, 4):
                    bs.timer(
                        i,
                        lambda t=4 - i: popup(str(t)+' Sec left!'),
                    )

                def revenge():
                    if not self.is_alive():
                        return
                    self.node.handlemessage(bs.DieMessage())
                    #bs.emitfx(position=self.position, count=20, scale=0.5, spread=0.5, chunk_type='spark')
                    popup('Revenged!')
                bs.timer(4.0, revenge)
                
            elif msg.poweruptype == 'flyer':
                p = self.node.position_forward
                from spaz import define_objects as obj
                obj.Flyer((p[0],p[1]+2,p[2])).autoretain()
                
            elif msg.poweruptype == 'slip':
                self.node.handlemessage("impulse", self.node.position[0], self.node.position[1],
                               self.node.position[2], self.node.velocity[0], 3,
                               self.node.velocity[2], 45, 45, 0, 0,
                               self.node.velocity[0], 3, self.node.velocity[2])
                               
            elif msg.poweruptype == 'beachball':
                p = self.node.position_forward
                from spaz import define_objects as obj
                obj.Bot(position=(0, 2, 0), source_player=self.source_player).autoretain()

                       
            self.node.handlemessage('flash')
            if msg.sourcenode:
                msg.sourcenode.handlemessage(bs.PowerupAcceptMessage())
            return True

        elif isinstance(msg, bs.FreezeMessage):
            if not self.node:
                return None
            if self.node.invincible:
                SpazFactory.get().block_sound.play(
                     1.0,
                    position=self.node.position,
                )
                return None
            if self.shield:
                return None
            if not self.frozen:
                self.frozen = True
                self.node.frozen = True
                bs.timer(
                    msg.time,
                    bs.WeakCallStrict(self.handlemessage, bs.ThawMessage()),
                )
                # Instantly shatter if we're already dead.
                # (otherwise its hard to tell we're dead).
                if self.hitpoints <= 0:
                    self.shatter()

        elif isinstance(msg, bs.ThawMessage):
            if self.frozen and not self.shattered and self.node:
                self.frozen = False
                self.node.frozen = False

        elif isinstance(msg, bs.HitMessage):
            if not self.node:
                return None
            if self.node.invincible:
                SpazFactory.get().block_sound.play(
                    1.0,
                    position=self.node.position,
                )
                return True

            # If we were recently hit, don't count this as another.
            # (so punch flurries and bomb pileups essentially count as 1 hit).
            local_time = int(bs.time() * 1000.0)
            assert isinstance(local_time, int)
            if (
                self._last_hit_time is None
                or local_time - self._last_hit_time > 1000
            ):
                self._num_times_hit += 1
                self._last_hit_time = local_time

            mag = msg.magnitude * self.impact_scale
            velocity_mag = msg.velocity_magnitude * self.impact_scale
            damage_scale = 0.22

            # If they've got a shield, deliver it to that instead.
            if self.shield:
                if msg.flat_damage:
                    damage = msg.flat_damage * self.impact_scale
                else:
                    # Hit our spaz with an impulse but tell it to only return
                    # theoretical damage; not apply the impulse.
                    assert msg.force_direction is not None
                    self.node.handlemessage(
                        'impulse',
                        msg.pos[0],
                        msg.pos[1],
                        msg.pos[2],
                        msg.velocity[0],
                        msg.velocity[1],
                        msg.velocity[2],
                        mag,
                        velocity_mag,
                        msg.radius,
                        1,
                        msg.force_direction[0],
                        msg.force_direction[1],
                        msg.force_direction[2],
                    )
                    damage = damage_scale * self.node.damage

                assert self.shield_hitpoints is not None
                self.shield_hitpoints -= int(damage)
                self.shield.hurt = (
                    1.0
                    - float(self.shield_hitpoints) / self.shield_hitpoints_max
                )

                # Its a cleaner event if a hit just kills the shield
                # without damaging the player.
                # However, massive damage events should still be able to
                # damage the player. This hopefully gives us a happy medium.
                max_spillover = SpazFactory.get().max_shield_spillover_damage
                if self.shield_hitpoints <= 0:
                    # FIXME: Transition out perhaps?
                    self.shield.delete()
                    self.shield = None
                    SpazFactory.get().shield_down_sound.play(
                        1.0,
                        position=self.node.position,
                    )

                    # Emit some cool looking sparks when the shield dies.
                    npos = self.node.position
                    bs.emitfx(
                        position=(npos[0], npos[1] + 0.9, npos[2]),
                        velocity=self.node.velocity,
                        count=random.randrange(20, 30),
                        scale=1.0,
                        spread=0.6,
                        chunk_type='spark',
                    )

                else:
                    SpazFactory.get().shield_hit_sound.play(
                        0.5,
                        position=self.node.position,
                    )

                # Emit some cool looking sparks on shield hit.
                assert msg.force_direction is not None
                bs.emitfx(
                    position=msg.pos,
                    velocity=(
                        msg.force_direction[0] * 1.0,
                        msg.force_direction[1] * 1.0,
                        msg.force_direction[2] * 1.0,
                    ),
                    count=min(30, 5 + int(damage * 0.005)),
                    scale=0.5,
                    spread=0.3,
                    chunk_type='spark',
                )

                # If they passed our spillover threshold,
                # pass damage along to spaz.
                if self.shield_hitpoints <= -max_spillover:
                    leftover_damage = -max_spillover - self.shield_hitpoints
                    shield_leftover_ratio = leftover_damage / damage

                    # Scale down the magnitudes applied to spaz accordingly.
                    mag *= shield_leftover_ratio
                    velocity_mag *= shield_leftover_ratio
                else:
                    return True  # Good job shield!
            else:
                shield_leftover_ratio = 1.0

            if msg.flat_damage:
                damage = int(
                    msg.flat_damage * self.impact_scale * shield_leftover_ratio
                )
            else:
                # Hit it with an impulse and get the resulting damage.
                assert msg.force_direction is not None
                self.node.handlemessage(
                    'impulse',
                    msg.pos[0],
                    msg.pos[1],
                    msg.pos[2],
                    msg.velocity[0],
                    msg.velocity[1],
                    msg.velocity[2],
                    mag,
                    velocity_mag,
                    msg.radius,
                    0,
                    msg.force_direction[0],
                    msg.force_direction[1],
                    msg.force_direction[2],
                )

                damage = int(damage_scale * self.node.damage)
            self.node.handlemessage('hurt_sound')

            # Play punch impact sound based on damage if it was a punch.
            if msg.hit_type == 'punch':
                self.on_punched(damage)

                # If damage was significant, lets show it.
                if damage >= 350:
                    assert msg.force_direction is not None
                    bs.show_damage_count(
                        '-' + str(int(damage / 10)) + '%',
                        msg.pos,
                        msg.force_direction,
                        self._dead,
                    )

                # Let's always add in a super-punch sound with boxing
                # gloves just to differentiate them.
                if msg.hit_subtype == 'super_punch':
                    SpazFactory.get().punch_sound_stronger.play(
                        1.0,
                        position=self.node.position,
                    )
                if damage >= 500:
                    sounds = SpazFactory.get().punch_sound_strong
                    sound = sounds[random.randrange(len(sounds))]
                elif damage >= 100:
                    sound = SpazFactory.get().punch_sound
                else:
                    sound = SpazFactory.get().punch_sound_weak
                sound.play(1.0, position=self.node.position)

                # Throw up some chunks.
                assert msg.force_direction is not None
                bs.emitfx(
                    position=msg.pos,
                    velocity=(
                        msg.force_direction[0] * 0.5,
                        msg.force_direction[1] * 0.5,
                        msg.force_direction[2] * 0.5,
                    ),
                    count=min(10, 1 + int(damage * 0.0025)),
                    scale=0.3,
                    spread=0.03,
                )

                bs.emitfx(
                    position=msg.pos,
                    chunk_type='sweat',
                    velocity=(
                        msg.force_direction[0] * 1.3,
                        msg.force_direction[1] * 1.3 + 5.0,
                        msg.force_direction[2] * 1.3,
                    ),
                    count=min(30, 1 + int(damage * 0.04)),
                    scale=0.9,
                    spread=0.28,
                )

                # Momentary flash.
                hurtiness = damage * 0.003
                punchpos = (
                    msg.pos[0] + msg.force_direction[0] * 0.02,
                    msg.pos[1] + msg.force_direction[1] * 0.02,
                    msg.pos[2] + msg.force_direction[2] * 0.02,
                )
                flash_color = (1.0, 0.8, 0.4)
                light = bs.newnode(
                    'light',
                    attrs={
                        'position': punchpos,
                        'radius': 0.12 + hurtiness * 0.12,
                        'intensity': 0.3 * (1.0 + 1.0 * hurtiness),
                        'height_attenuated': False,
                        'color': flash_color,
                    },
                )
                bs.timer(0.06, light.delete)

                flash = bs.newnode(
                    'flash',
                    attrs={
                        'position': punchpos,
                        'size': 0.17 + 0.17 * hurtiness,
                        'color': ((0+random.random()*5.0),(0+random.random()*5.0),(0+random.random()*5.0)),
                    },
                )
                #bs.timer(0.06, flash.delete)
                if spz.punch_flash:
                    bs.timer(0.2, flash.delete)
                else:
                    bs.timer(0.06, flash.delete)

            if msg.hit_type == 'impact':
                assert msg.force_direction is not None
                bs.emitfx(
                    position=msg.pos,
                    velocity=(
                        msg.force_direction[0] * 2.0,
                        msg.force_direction[1] * 2.0,
                        msg.force_direction[2] * 2.0,
                    ),
                    count=min(10, 1 + int(damage * 0.01)),
                    scale=0.4,
                    spread=0.1,
                )
            if self.hitpoints > 0:
                # It's kinda crappy to die from impacts, so lets reduce
                # impact damage by a reasonable amount *if* it'll keep us alive.
                if msg.hit_type == 'impact' and damage >= self.hitpoints:
                    # Drop damage to whatever puts us at 10 hit points,
                    # or 200 less than it used to be whichever is greater
                    # (so it *can* still kill us if its high enough).
                    newdamage = max(damage - 200, self.hitpoints - 10)
                    damage = newdamage
                self.node.handlemessage('flash')

                # If we're holding something, drop it.
                if damage > 0.0 and self.node.hold_node:
                    self.node.hold_node = None
                self.hitpoints -= damage
                self.node.hurt = (
                    1.0 - float(self.hitpoints) / self.hitpoints_max
                )

                # If we're cursed, *any* damage blows us up.
                if self._cursed and damage > 0:
                    bs.timer(
                        0.05,
                        bs.WeakCallStrict(
                            self.curse_explode, msg.get_source_player(bs.Player)
                        ),
                    )

                # If we're frozen, shatter.. otherwise die if we hit zero
                if self.frozen and (damage > 200 or self.hitpoints <= 0):
                    self.shatter()
                elif self.hitpoints <= 0:
                    self.node.handlemessage(
                        bs.DieMessage(how=bs.DeathType.IMPACT)
                    )

            # If we're dead, take a look at the smoothed damage value
            # (which gives us a smoothed average of recent damage) and shatter
            # us if its grown high enough.
            if self.hitpoints <= 0:
                damage_avg = self.node.damage_smoothed * damage_scale
                if damage_avg >= 1000:
                    self.shatter()

        elif isinstance(msg, BombDiedMessage):
            self.bomb_count += 1

        elif isinstance(msg, bs.DieMessage):
            wasdead = self._dead
            self._dead = True
            self.hitpoints = 0
            if msg.immediate:
                if self.node:
                    self.node.delete()
            elif self.node:
                if not wasdead:
                    self.node.hurt = 1.0
                    if self.play_big_death_sound:
                        SpazFactory.get().single_player_death_sound.play()
                    self.node.dead = True
                    bs.timer(2.0, self.node.delete)

        elif isinstance(msg, bs.OutOfBoundsMessage):
            #
            if self.fall_protect:
                pos = self.activity.map.get_ffa_start_position(self.activity.players)
                #self.node.position = pos #doesnt work with spaz node
                self.node.handlemessage(bs.StandMessage(pos))
                #bs.broadcastmessage('Saved by fall protection! - Logic')
                pptx('Fall-Protection!',color=(1, 1, 1), scale=1.0,position=self.node.position,).autoretain()
            else:
                self.handlemessage(bs.DieMessage(how=bs.DeathType.FALL))

        elif isinstance(msg, bs.StandMessage):
            self._last_stand_pos = (
                msg.position[0],
                msg.position[1],
                msg.position[2],
            )
            if self.node:
                self.node.handlemessage(
                    'stand',
                    msg.position[0],
                    msg.position[1],
                    msg.position[2],
                    msg.angle,
                )

        elif isinstance(msg, CurseExplodeMessage):
            self.curse_explode()

        elif isinstance(msg, PunchHitMessage):
            if not self.node:
                return None
            node = bs.getcollision().opposingnode

            # Don't want to physically affect powerups.
            if node.getdelegate(PowerupBox):
                return None

            # Only allow one hit per node per punch.
            if node and (node not in self._punched_nodes):
                punch_momentum_angular = (
                    self.node.punch_momentum_angular * self._punch_power_scale
                )
                punch_power = self.node.punch_power * self._punch_power_scale

                # Ok here's the deal:  we pass along our base velocity for use
                # in the impulse damage calculations since that is a more
                # predictable value than our fist velocity, which is rather
                # erratic. However, we want to actually apply force in the
                # direction our fist is moving so it looks better. So we still
                # pass that along as a direction. Perhaps a time-averaged
                # fist-velocity would work too?.. perhaps should try that.

                # If its something besides another spaz, just do a muffled
                # punch sound.
                if node.getnodetype() != 'spaz':
                    sounds = SpazFactory.get().impact_sounds_medium
                    sound = sounds[random.randrange(len(sounds))]
                    sound.play(1.0, position=self.node.position)

                ppos = self.node.punch_position
                punchdir = self.node.punch_velocity
                vel = self.node.punch_momentum_linear

                self._punched_nodes.add(node)
                node.handlemessage(
                    bs.HitMessage(
                        pos=ppos,
                        velocity=vel,
                        magnitude=punch_power * punch_momentum_angular * 110.0,
                        velocity_magnitude=punch_power * 40,
                        radius=0,
                        srcnode=self.node,
                        source_player=self.source_player,
                        force_direction=punchdir,
                        hit_type='punch',
                        hit_subtype=(
                            'super_punch'
                            if self._has_boxing_gloves
                            else 'default'
                        ),
                    )
                )

                # Also apply opposite to ourself for the first punch only.
                # This is given as a constant force so that it is more
                # noticeable for slower punches where it matters. For fast
                # awesome looking punches its ok if we punch 'through'
                # the target.
                mag = -400.0
                if self._hockey:
                    mag *= 0.5
                if len(self._punched_nodes) == 1:
                    self.node.handlemessage(
                        'kick_back',
                        ppos[0],
                        ppos[1],
                        ppos[2],
                        punchdir[0],
                        punchdir[1],
                        punchdir[2],
                        mag,
                    )
        elif isinstance(msg, PickupMessage):
            if not self.node:
                return None

            try:
                collision = bs.getcollision()
                opposingnode = collision.opposingnode
                opposingbody = collision.opposingbody
            except bs.NotFoundError:
                return True

            # Don't allow picking up of invincible dudes.
            try:
                if opposingnode.invincible:
                    return True
            except Exception:
                pass

            # If we're grabbing the pelvis of a non-shattered spaz, we wanna
            # grab the torso instead.
            if (
                opposingnode.getnodetype() == 'spaz'
                and not opposingnode.shattered
                and opposingbody == 4
            ):
                opposingbody = 1

            # Special case #1 - if we're holding a flag, don't replace it
            # Special case #2 - corpses should have lower priority
            # (hmm - should make this customizable or more low level).
            held = self.node.hold_node
            if held:
                spaz = opposingnode.getdelegate(Spaz)
                if held.getnodetype() == 'flag' or (
                    spaz and not spaz.is_alive()
                ):
                    return True

            # Note: hold_body needs to be set before hold_node.
            self.node.hold_body = opposingbody
            self.node.hold_node = opposingnode
        elif isinstance(msg, bs.CelebrateMessage):
            if self.node:
                self.node.handlemessage('celebrate', int(msg.duration * 1000))
        return None
        
def new_drop_bomb(self) -> Bomb | None:
        """
        Tell the spaz to drop one of his bombs, and returns
        the resulting bomb object.
        If the spaz has no bombs or is otherwise unable to
        drop a bomb, returns None.
        """

        if (self.land_mine_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        elif (self.ice_impact_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        elif (self.shock_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        elif (self.curse_impact_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        elif (self.tele_impact_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        elif (self.curse_mine_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        elif (self.ice_mine_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        elif (self.boom_bomb_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        elif (self.headache_count <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        assert self.node
        pos = self.node.position_forward
        vel = self.node.velocity

        if self.land_mine_count > 0:
            dropping_bomb = False
            self.set_land_mine_count(self.land_mine_count - 1)
            bomb_type = 'land_mine'
        elif self.curse_mine_count > 0:
            dropping_bomb = False
            self.set_curse_mine_count(self.curse_mine_count - 1)
            bomb_type = 'curse_mine'
        elif self.ice_mine_count > 0:
            dropping_bomb = False
            self.set_ice_mine_count(self.ice_mine_count - 1)
            bomb_type = 'ice_mine'
        elif self.ice_impact_count > 0:
            dropping_bomb = False
            self.set_ice_impact_count(self.ice_impact_count - 1)
            bomb_type = 'ice_impact'
        elif self.curse_impact_count > 0:
            dropping_bomb = False
            self.set_curse_impact_count(self.curse_impact_count - 1)
            bomb_type = 'curse_impact'
        elif self.tele_impact_count > 0:
            dropping_bomb = False
            self.set_tele_impact_count(self.tele_impact_count - 1)
            bomb_type = 'tele_impact'
        elif self.shock_count > 0:
            dropping_bomb = False
            self.set_shock_count(self.shock_count - 1)
            bomb_type = 'shock_bomb'
        elif self.boom_bomb_count > 0:
            dropping_bomb = False
            self.set_boom_bomb_count(self.boom_bomb_count - 1)
            bomb_type = 'boom_bomb'
        elif self.headache_count > 0:
            dropping_bomb = False
            self.set_headache_count(self.headache_count - 1)
            bomb_type = 'headache'
        else:
            dropping_bomb = True
            if self.random_bombs:
                bomb_type = random.choice([
                        'ice', 'impact', 'sticky', 'tnt','ice_impact',
                        'sticky_ice','curse_mine','ice_mine','curse_impact','tele_impact',
                        'shock_bomb','glue_bomb','weed_bomb','cursy_bomb','revenge_bomb'])
            else:
                bomb_type = self.bomb_type

        from bomb.newbomb import NewBomby
        bomb = NewBomby(
            position=(pos[0], pos[1] - 0.0, pos[2]),
            velocity=(vel[0], vel[1], vel[2]),
            bomb_type=bomb_type,
            blast_radius=self.blast_radius,
            source_player=self.source_player,
            owner=self.node,
        ).autoretain()

        assert bomb.node
        if dropping_bomb:
            self.bomb_count -= 1
            bomb.node.add_death_action(
                bs.WeakCallStrict(self.handlemessage, BombDiedMessage())
            )
        self._pick_up(bomb.node)

        for clb in self._dropped_bomb_callbacks:
            clb(self, bomb)

        return bomb
        
def set_ice_impact_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.ice_impact_count = count
        if self.node:
            if self.ice_impact_count != 0:
                self.node.counter_text = 'x' + str(self.ice_impact_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_ice_impact
                )
            else:
                self.node.counter_text = ''
                
def set_headache_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.headache_count = count
        if self.node:
            if self.headache_count != 0:
                self.node.counter_text = 'x' + str(self.headache_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_ice_impact
                )
            else:
                self.node.counter_text = ''
                
def set_boom_bomb_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.boom_bomb_count = count
        if self.node:
            if self.boom_bomb_count != 0:
                self.node.counter_text = 'x' + str(self.boom_bomb_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_ice_impact
                )
            else:
                self.node.counter_text = ''
                
def set_shock_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.shock_count = count
        if self.node:
            if self.shock_count != 0:
                self.node.counter_text = 'x' + str(self.shock_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_ice_impact
                )
            else:
                self.node.counter_text = ''
                
def set_curse_impact_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.curse_impact_count = count
        if self.node:
            if self.curse_impact_count != 0:
                self.node.counter_text = 'x' + str(self.curse_impact_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_curse_impact
                )
            else:
                self.node.counter_text = ''
                
def set_curse_mine_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.curse_mine_count = count
        if self.node:
            if self.curse_mine_count != 0:
                self.node.counter_text = 'x' + str(self.curse_mine_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_curse_mine
                )
            else:
                self.node.counter_text = ''
                
def set_ice_mine_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.ice_mine_count = count
        if self.node:
            if self.ice_mine_count != 0:
                self.node.counter_text = 'x' + str(self.ice_mine_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_ice_mine
                )
            else:
                self.node.counter_text = ''
                
def set_tele_impact_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.tele_impact_count = count
        if self.node:
            if self.tele_impact_count != 0:
                self.node.counter_text = 'x' + str(self.tele_impact_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_ice_mine
                )
            else:
                self.node.counter_text = ''
        
def new_get_bomb_type_tex(self) -> bs.Texture:
        factory = PowerupBoxFactory.get()
        if self.bomb_type == 'sticky':
            return factory.tex_sticky_bombs
        if self.bomb_type == 'ice':
            return factory.tex_ice_bombs
        if self.bomb_type == 'impact':
            return factory.tex_impact_bombs
        if self.bomb_type == 'ice_impact':
            return factory.tex_ice_impact
        if self.bomb_type == 'sticky_ice':
            return factory.tex_sticky_ice
        if self.bomb_type == 'glue_bomb':
            return factory.tex_glue_bomb
        if self.bomb_type == 'revenge_bomb':
            return factory.tex_revenge_bomb
        if self.bomb_type == 'cursy_bomb':
            return factory.tex_cursy_bomb
        if self.bomb_type == 'curse_mine':
            return factory.tex_curse_mine
        if self.bomb_type == 'curse_impact':
            return factory.tex_curse_impact
        if self.bomb_type == 'tele_impact':
            return factory.tex_tele_impact
        if self.bomb_type == 'shock_count':
            return factory.tex_shock_bomb
        if self.bomb_type == 'weed_bomb':
            return factory.tex_weed_bomb
        if self.bomb_type == 'blast_bomb':
            return factory.tex_blast_bomb
        if self.bomb_type == 'boom_bomb':
            return factory.tex_boom_bomb
        if self.bomb_type == 'headache':
            return factory.tex_headache
        raise ValueError('invalid bomb type')

def new_on_punch_press(self) -> None:
        """
        Called to 'press punch' on this spaz;
        used for player or AI connections.
        """
        if not self.node or self.frozen or self.node.knockout > 0.0:
            return
        t_ms = int(bs.time() * 1000.0)
        assert isinstance(t_ms, int)
        if t_ms - self.last_punch_time_ms >= self._punch_cooldown:
            if self.punch_callback is not None:
                self.punch_callback(self)
            self._punched_nodes = set()  # Reset this.
            self.last_punch_time_ms = t_ms
            if spz.spaz_color:
                self.node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
                self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
            elif self.random_colors: #for d pwp
                self.node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
                self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
            self.node.punch_pressed = True
            if not self.node.hold_node:
                bs.timer(
                    0.1,
                    bs.WeakCallStrict(
                        self._safe_play_sound,
                        SpazFactory.get().swish_sound,
                        0.8,
                    ),
                )
        self._turbo_filter_add_press('punch')
        
def new_on_pickup_press(self) -> None:
        """
        Called to 'press pick-up' on this spaz;
        used by player or AI connections.
        """
        if not self.node:
            return
        t_ms = int(bs.time() * 1000.0)
        assert isinstance(t_ms, int)
        if t_ms - self.last_pickup_time_ms >= self._pickup_cooldown:
            if spz.spaz_char:
                tex = bs.gettexture
                get = bs.getmesh
                char = random.choice(['frosty','wizard','santa','pixie','cyborg','ninja','agent','bear','ali'])                
                self.node.head_mesh = get(char+'Head')
                self.node.color_texture = tex(char+'Color')   
                self.node.color_mask_texture = tex(char+'ColorMask')  
                self.node.torso_mesh = get(char+'Torso')               
                self.node.hand_mesh = get(char+'Hand')
                self.node.upper_arm_mesh = get(char+'UpperArm')
                self.node.lower_leg_mesh = get(char+'LowerLeg')
                self.node.upper_leg_mesh = get(char+'UpperLeg')
                self.node.forearm_mesh = get(char+'ForeArm')
                self.node.toes_mesh = get(char+'Toes')
                if char =='santa':
                    self.node.pelvis_mesh = get('kronkPelvis')  
                else:
                    self.node.pelvis_mesh = get(char+'Pelvis')
                self.node.style = char  
            elif self.random_characters:
                tex = bs.gettexture
                get = bs.getmesh
                char = random.choice(['frosty','wizard','santa','pixie','cyborg','ninja','agent','bear','ali'])                
                self.node.head_mesh = get(char+'Head')
                self.node.color_texture = tex(char+'Color')   
                self.node.color_mask_texture = tex(char+'ColorMask')  
                self.node.torso_mesh = get(char+'Torso')               
                self.node.hand_mesh = get(char+'Hand')
                self.node.upper_arm_mesh = get(char+'UpperArm')
                self.node.lower_leg_mesh = get(char+'LowerLeg')
                self.node.upper_leg_mesh = get(char+'UpperLeg')
                self.node.forearm_mesh = get(char+'ForeArm')
                self.node.toes_mesh = get(char+'Toes')
                if char =='santa':
                    self.node.pelvis_mesh = get('kronkPelvis')  
                else:
                    self.node.pelvis_mesh = get(char+'Pelvis')
                self.node.style = char  
            self.node.pickup_pressed = True
            self.last_pickup_time_ms = t_ms
        self._turbo_filter_add_press('pickup')


def enable_spaz():
    Spaz.handlemessage = new_handlemessage
    Spaz.on_punch_press = new_on_punch_press
    Spaz.on_pickup_press = new_on_pickup_press
    Spaz.drop_bomb = new_drop_bomb
    Spaz._get_bomb_type_tex = new_get_bomb_type_tex
    Spaz.set_ice_impact_count = set_ice_impact_count
    Spaz.set_curse_mine_count = set_curse_mine_count
    Spaz.set_curse_impact_count = set_curse_impact_count
    Spaz.set_ice_mine_count = set_ice_mine_count
    Spaz.set_tele_impact_count = set_tele_impact_count
    Spaz.set_shock_count = set_shock_count
    Spaz.set_boom_bomb_count = set_boom_bomb_count
    Spaz.set_headache_count = set_headache_count
    Spaz.__init__ = newSpazInit