from __future__ import annotations

import random
import bascenev1 as bs
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor.bomb import Bomb, Blast
from bascenev1lib.actor.popuptext import PopupText as pptx
import math

class ShockWave(bs.Actor):
    """Radial shockwave region that pushes players and objects."""

    def __init__(
        self,
        position: tuple[float, float, float] = (0.0, 1.0, 0.0),
        radius: float = 2.0,
        speed: int = 200,
    ):
        super().__init__()
        self._position = position
        self._radius = radius

        self._material = bs.Material()
        shared = SharedObjects.get()

        # Player collision.
        self._material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self._touched_spaz),
            ),
        )

        # Object collision (non-player).
        self._material.add_actions(
            conditions=(
                ('they_have_material', shared.object_material),
                'and',
                ('they_dont_have_material', shared.player_material),
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self._touched_obj),
            ),
        )

        # Collision region.
        self.node = bs.newnode(
            'region',
            attrs={
                'position': self._position,
                'scale': (0.1, 0.1, 0.1),
                'type': 'sphere',
                'materials': [self._material],
            },
        )

        # Visual shockwave.
        self._visual = bs.newnode(
            'shield',
            attrs={
                'position': self._position,
                'radius': 0.1,
                'color': (0.05, 0.05, 0.1),
            },
        )

        # Animate expansion.
        bs.animate(
            self._visual,
            'radius',
            {0.0: 0.0, speed / 1000.0: self._radius * 2.0},
        )
        bs.animate_array(
            self.node,
            'scale',
            3,
            {
                0.0: (0.0, 0.0, 0.0),
                speed / 1000.0: (self._radius, self._radius, self._radius),
            },
        )

        # Cleanup.
        bs.timer(speed / 1000.0 + 0.01, self._cleanup)

    # ------------------------------------------------------------------

    def _touched_spaz(self) -> None:
        node = bs.getcollision().opposingnode
        if not node or not node.exists():
            return

        spaz = node.getdelegate(Spaz)
        if spaz is None:
            return

        old_scale = getattr(spaz, '_punchPowerScale', 1.0)
        spaz._punchPowerScale = old_scale - 0.3

        def restore() -> None:
            if spaz:
                spaz._punchPowerScale = old_scale

        bs.timer(2.0, restore)
        new_sound = bs.getsound('shatter')
        new_sound.play(3, position=self.node.position)

        node.handlemessage(
            'impulse',
            node.position[0],
            node.position[1],
            node.position[2],
            -node.velocity[0],
            -node.velocity[1],
            -node.velocity[2],
            200,
            200,
            0,
            0,
            -node.velocity[0],
            -node.velocity[1],
            -node.velocity[2],
        )

        flash = bs.newnode(
            'flash',
            attrs={
                'position': node.position,
                'size': 0.7,
                'color': (0.0, 0.4 + random.random(), 1.0),
            },
        )

        explosion = bs.newnode(
            'explosion',
            attrs={
                'position': node.position,
                'velocity': (
                    node.velocity[0],
                    max(-1.0, node.velocity[1]),
                    node.velocity[2],
                ),
                'radius': 0.4,
                'big': True,
                'color': (0.3, 0.3, 1.0),
            },
        )

        bs.timer(0.4, explosion.delete)
        bs.timer(0.06, flash.delete)

        bs.emitfx(
            position=node.position,
            count=20,
            scale=0.5,
            spread=0.5,
            chunk_type='spark',
        )

    # ------------------------------------------------------------------

    def _touched_obj(self) -> None:
        node = bs.getcollision().opposingnode
        if not node or not node.exists():
            return

        new_sound = bs.getsound('shatter')
        new_sound.play(3, position=self.node.position)

        node.handlemessage(
            'impulse',
            node.position[0] + random.uniform(-2, 2),
            node.position[1] + random.uniform(-2, 2),
            node.position[2] + random.uniform(-2, 2),
            -node.velocity[0] + random.uniform(-2, 2),
            -node.velocity[1] + random.uniform(-2, 2),
            -node.velocity[2] + random.uniform(-2, 2),
            100,
            100,
            0,
            0,
            -node.velocity[0],
            -node.velocity[1],
            -node.velocity[2],
        )

        flash = bs.newnode(
            'flash',
            attrs={
                'position': node.position,
                'size': 0.4,
                'color': (0.0, 0.4 + random.random(), 1.0),
            },
        )

        explosion = bs.newnode(
            'explosion',
            attrs={
                'position': node.position,
                'velocity': (
                    node.velocity[0],
                    max(-1.0, node.velocity[1]),
                    node.velocity[2],
                ),
                'radius': 0.4,
                'big': True,
                'color': (0.3, 0.3, 1.0),
            },
        )

        bs.timer(0.4, explosion.delete)
        bs.timer(0.06, flash.delete)

        bs.emitfx(
            position=node.position,
            count=20,
            scale=0.5,
            spread=0.5,
            chunk_type='spark',
        )

    # ------------------------------------------------------------------

    def _cleanup(self) -> None:
        if self.node:
            self.node.delete()
        if self._visual:
            self._visual.delete()



class BlackHole(bs.Actor): # add next
    """A black hole that sucks in objects and players, can grow and explode."""

    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 1.0, 0.0),
        autoExpand: bool = True,
        scale: float = 1.0,
        doNotRandomize: bool = False,
        infinity: bool = False,
        owner: Optional[bs.Actor] = None,
    ):
        super().__init__()
        self.shields: List[bs.NodeActor] = []
        self.suckObjects: List[bs.NodeActor] = []
        self.owner = owner

        if not doNotRandomize:
            self.position = (
                position[0] - 2 + random.random() * 4,
                position[1] + random.random() * 2,
                position[2] - 2 + random.random() * 4,
            )
        else:
            self.position = position

        self.scale = scale

        # Materials
        shared = SharedObjects.get()

        self.blackHoleMaterial = bs.Material()
        self.blackHoleMaterial.add_actions(
            conditions=(
                ('they_dont_have_material', shared.object_material),
                'and',
                ('they_have_material', shared.player_material),
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self._touched_spaz)))

        self.blackHoleMaterial.add_actions(
            conditions=(
                ('they_dont_have_material', shared.player_material),
                'and',
                ('they_have_material', shared.object_material),
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self._touched_obj)))

        self.suckMaterial = bs.Material()
        self.suckMaterial.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self._touched_obj_suck)))


        # Nodes
        self.node = bs.newnode(
            'region',
            attrs={
                'position': self.position,
                'scale': (self.scale, self.scale, self.scale),
                'type': 'sphere',
                'materials': [self.blackHoleMaterial],
            },
        )

        self.suckRadius = bs.newnode(
            'region',
            attrs={
                'position': self.position,
                'scale': (self.scale, self.scale, self.scale),
                'type': 'sphere',
                'materials': [self.suckMaterial],
            },
        )

        # Distortion BG effect
        def dist():
            if self.node.exists():
                bs.emitfx(
                    position=self.position,
                    emit_type='distortion',
                    spread=6.0,
                    count=100,
                )
                bs.timer(1.0, dist)

        dist()

        if not infinity:
            self._dieTimer = bs.Timer(25.0, bs.CallPartial(self.explode))

        # Initial shields
        for _ in range(20):
            self.shields.append(
                bs.newnode(
                    'shield',
                    attrs={
                        'color': (random.random(), random.random(), random.random()),
                        'radius': self.scale * 2,
                        'position': self.position,
                    },
                )
            )

        # Play sound
        def play_sound():
            new_sound = bs.getsound('blackHole')
            new_sound.play(3, position=self.node.position)

        play_sound()
        if infinity:
            self.sound2 = bs.Timer(25.0, bs.Call(play_sound), repeat=infinity)

        # Animate node and suck radius
        bs.animate_array(self.node, 'scale', 3, {0.0: (0.0, 0.0, 0.0), 0.3: (self.scale, self.scale, self.scale)})
        bs.animate_array(self.suckRadius, 'scale', 3, {0: (0, 0, 0), 0.3: (self.scale * 8, self.scale * 8, self.scale * 8)})

    # ------------------------------------------------------------------
    def addMass(self):
        self.scale += 0.15
        if self.node.exists():
            self.node.scale = (self.scale, self.scale, self.scale)
        for _ in range(2):
            self.shields.append(
                bs.newnode(
                    'shield',
                    attrs={
                        'color': (random.random(), random.random(), random.random()),
                        'radius': self.scale + 0.15,
                        'position': self.position,
                    },
                )
            )

    # ------------------------------------------------------------------
    def explode(self):
        bs.emitfx(position=self.position, count=500, scale=1, spread=1.5, chunk_type='spark')
        for shield in self.shields:
            bs.animate(shield, 'radius', {0: 0, 0.2: shield.radius * 5})
        #bs.Blast(position=self.position, blast_radius=10).auto_retain()
        Blast(position=self.node.position,
                    blast_radius=10.0,
                    blast_type='normal').autoretain()
        for shield in self.shields:
            shield.delete()
        if self.node.exists():
            self.node.delete()
        if self.suckRadius.exists():
            self.suckRadius.delete()

    # ------------------------------------------------------------------
    def _touched_spaz(self):
        node = bs.getcollision().opposingnode
        if not node or not node.exists():
            return
        #bs.Blast(position=node.position, blast_type='turret').auto_retain()
        Blast(position=self.node.position,blast_type='normal').autoretain()
        spaz = node.getdelegate(bs.Actor)  # could refine to Spaz if needed
        if spaz and self.owner:
            node.handlemessage(bs.HitMessage(magnitude=1000.0, source_player=self.owner.getdelegate(bs.Actor)))
            node.handlemessage(bs.DieMessage())
            bs.shake_camera(2)
        else:
            node.handlemessage(bs.DieMessage())
        self.addMass()

    # ------------------------------------------------------------------
    def _touched_obj(self):
        node = bs.getcollision().opposingnode
        if node and node.exists():
            Blast(position=self.node.position,blast_type='normal').autoretain()
            node.handlemessage(bs.DieMessage())

    # ------------------------------------------------------------------
    def _touched_obj_suck(self):
        node = bs.getcollision().opposingnode
        if node and node.exists() and node.getnodetype() in ['prop', 'bomb']:
            self.suckObjects.append(node)

        for obj in self.suckObjects:
            if obj.exists():
                if getattr(obj, 'sticky', False):
                    obj.sticky = False
                    obj.extra_acceleration = (0, 10, 0)
                else:
                    obj.extra_acceleration = (
                        (self.position[0] - obj.position[0]) * 8,
                        (self.position[1] - obj.position[1]) * 25,
                        (self.position[2] - obj.position[2]) * 8,
                    )

    # ------------------------------------------------------------------
    def handlemessage(self, m: Any):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
            if self.suckRadius.exists():
                self.suckRadius.delete()
            self.suckObjects.clear()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handlemessage(bs.DieMessage())


class AimForOpponent(bs.Actor):
    """Makes a bomb seek the nearest enemy player."""

    def __init__(self, bomb: bs.Node, owner: bs.Node):
        super().__init__()

        self.bomb = bomb
        self.owner = owner
        self.target: bs.Node | None = None

        shared = SharedObjects.get()

        self.aim_zone_material = bs.Material()
        self.aim_zone_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self._touched_spaz),
            ),
        )

        bs.timer(0, self._look_for_spaz)

    # ------------------------------------------------------------------

    def _look_for_spaz(self) -> None:
        if not self.bomb or not self.bomb.exists():
            return

        self.bomb.extra_acceleration = (0, 20, 0)

        self.node = bs.newnode(
            'region',
            attrs={
                'position': self.bomb.position,
                'scale': (0.0, 0.0, 0.0),
                'type': 'sphere',
                'materials': [self.aim_zone_material],
            },
        )

        bs.animate_array(
            self.node,
            'scale',
            3,
            {
                0.0: (0.0, 0.0, 0.0),
                0.05: (60.0, 60.0, 60.0),
                0.10: (90.0, 90.0, 90.0),
            },
        )

        bs.timer(0.15, self.node.delete)
        bs.timer(0.151, self._check_target)

    # ------------------------------------------------------------------

    def _check_target(self) -> None:
        if self.target is not None:
            self._begin_seek()

    # ------------------------------------------------------------------

    def _begin_seek(self) -> None:
        if not self.bomb or not self.bomb.exists():
            return

        # Strong upward force once target is locked.
        self.bomb.extra_acceleration = (0, 200, 0)
        self._seek()

    # ------------------------------------------------------------------

    def _seek(self) -> None: # improved locking..
        if (
            self.target is None
            or not self.target.exists()
            or not self.bomb
            or not self.bomb.exists()
        ):
            return

        bx, by, bz = self.bomb.position
        tx, ty, tz = self.target.position
        ty -= 1  # chest-level lock

        dx = tx - bx
        dy = ty - by
        dz = tz - bz

        vx, vy, vz = self.bomb.velocity

        strength = 2.15 # fine tuned!

        self.bomb.velocity = (
            vx * 0.8 + dx * strength,
            vy * 0.8 + dy * strength,
            vz * 0.8 + dz * strength,
        )

        bs.timer(0.01, self._seek)


    # ------------------------------------------------------------------

    def _touched_spaz(self) -> None:
        collision = bs.getcollision()
        node = collision.opposingnode

        if not node or not node.exists():
            return

        spaz = node.getdelegate(Spaz)
        owner_spaz = self.owner.getdelegate(Spaz) if self.owner else None

        if not spaz or not spaz.is_alive():
            return

        owner_player = owner_spaz.source_player if owner_spaz else None
        target_player = spaz.source_player

        if owner_player and target_player and owner_player.team == target_player.team:
            return

        self.target = node

        if self.node and self.node.exists():
            self.node.delete()

class Flyer(bs.Actor):
    """A floating flyer prop that reacts when picked up and drops naturally."""

    def __init__(self, position: tuple[float, float, float] = (0, 1, 0)):
        super().__init__()

        color = (random.random(), random.random(), random.random())
        shared = SharedObjects.get()

        # Create prop node
        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'body': 'sphere',
                'mesh': bs.getmesh('frostyPelvis'),
                'color_texture': bs.gettexture('crossOutMask'),
                'shadow_size': 0.44,
                'reflection': 'powerup',
                'reflection_scale': color,
                'materials': [shared.object_material],
                'light_model': bs.getmesh('frostyPelvis'),  # optional; can remove
            },
        )

    # ------------------------------------------------------------------
    def handlemessage(self, m: bs.Message) -> None:
        if isinstance(m, bs.DieMessage) or isinstance(m, bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()

        elif isinstance(m, bs.PickedUpMessage):
            if self.node.exists():
                # Gentle upward float while held
                self.node.extra_acceleration = (0, 60, 0)

        elif isinstance(m, bs.DroppedMessage):
            if self.node.exists():
                # Return to normal physics when dropped
                self.node.extra_acceleration = (0, 0, 0)

        else:
            super().handlemessage(m)
            

class BeachBall(bs.Actor):
    """A bouncy ball that explodes lightly on touch."""

    def __init__(self, position=(0, 1, 0)):
        super().__init__()

        shared = SharedObjects.get()
        color = (random.random(), random.random(), random.random())

        # Ball node
        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'body': 'sphere',
                'mesh': bs.getmesh('frostyPelvis'),
                'color_texture': bs.gettexture('gameCircleIcon'),
                'shadow_size': 0.44,
                'reflection': 'powerup',
                'reflection_scale': color,
                'materials': [shared.object_material, shared.player_material],
            },
        )

    # ------------------------------------------------------------------
    def handlemessage(self, m: bs.Message) -> None:
        if isinstance(m, (bs.DieMessage, bs.OutOfBoundsMessage)):
            if self.node.exists():
                self.node.delete()

        elif isinstance(m, bs.PickedUpMessage):
            # optional: ball gets a slight upward boost
            if self.node.exists():
                self.node.extra_acceleration = (0, 20, 0)

        elif isinstance(m, bs.DroppedMessage):
            if self.node.exists():
                # fall naturally
                self.node.extra_acceleration = (0, 0, 0)

        # Whenever a player touches the ball, explode lightly
        elif isinstance(m, bs.CollisionMessage):
            node = m.source
            if node.exists() and node.getdelegate(Spaz):
                # Create a small blast at the player's position
                Blast(position=node.position, blast_radius=1.0, blast_type='normal').autoretain()

        else:
            super().handlemessage(m)
            
            
class BotFactory:
    def __init__(self):
        self.bot_model = bs.getmesh('impactBomb')
        self.bot_texture = bs.gettexture('crossOutMask')


# ---------------------------------------------------------
# Bot Actor
# ---------------------------------------------------------

class Bot(bs.Actor):

    def __init__(
        self,
        position: tuple[float, float, float] = (0.0, 1.0, 0.0),
        source_player: bs.Player | None = None,
    ):
        super().__init__()

        shared = SharedObjects.get()
        factory = self.get_factory()

        self.source_players: list[bs.Player] = (
            [source_player] if source_player else []
        )

        # ---------------- Node ----------------

        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'body': 'sphere',
                'position': position,
                'velocity': (0.0, 0.0, 1.0),  # NEVER zero this
                'mesh': factory.bot_model,
                'color_texture': factory.bot_texture,
                'reflection': 'powerup',
                'reflection_scale': (1, 1, 1),
                'shadow_size': 0.5,
                'extra_acceleration': (0, 20, 0),
                'mesh_scale': 0,
                'materials': [shared.object_material],
            },
        )

        # ---------------- Probe (pathfinding) ----------------

        self._probe_material = bs.Material()
        self._probe_material.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=(('call', 'at_connect', self._on_probe_hit),),
        )

        self._probe = bs.newnode(
            'region',
            attrs={
                'position': position,
                'scale': (0.6, 0.6, 0.6),
                'type': 'box',
                'materials': [self._probe_material],
            },
        )

        if True: # like a cool animation to it
            shieldy = bs.newnode('math', owner=self.node, attrs={'input1': (0, -0.03, 0), 'operation': 'add'}) 
            self.node.connectattr('position', shieldy, 'input2')
            self.shield = bs.newnode('shield',
                                 owner=self.node,
                                 attrs={
                                     'color': ((0+random.random()*5.0),(0+random.random()*5.0),(0+random.random()*5.0)),    
                                     'radius': 0.5125,
                                     'position': (self.node.position[0],self.node.position[1],self.node.position[2] + 0.5)})
            self.node.connectattr('position', self.shield, 'position')
            shieldy.connectattr('output', self.shield, 'position')
            #
            m = bs.newnode('math', owner=self.node, attrs={'input1': (0, 0.0, 0), 'operation': 'add'})
            self.node.connectattr('position', m, 'input2')
            self.flash = bs.newnode("flash",
                        owner=self.node,
                        attrs={'position':self.node.position,
                               'size':0.3,
                               'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
            m.connectattr('output', self.flash, 'position') 
            bs.animate_array(node=self.flash, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)

        # ---------------- Timers ----------------

        bs.timer(30.0, bs.CallPartial(self.handlemessage, bs.DieMessage()))
        self._update_timer = bs.Timer(0.5, bs.CallPartial(self._update), repeat=True)

    # -----------------------------------------------------

    def _update(self) -> None:
        if not self.node.exists():
            return

        ox, oy, oz = self.node.position
        vx, vy, vz = self.node.velocity

        # Move probe forward
        self._probe.position = (
            ox + vx * 0.15,
            oy,
            oz + vz * 0.15,
        )

        closest_spaz: Spaz | None = None
        closest_dist = 9999.0

        activity = bs.getactivity()
        if not activity:
            return

        # ---------------- Find enemy ----------------

        for player in activity.players:
            if not self._is_enemy(player):
                continue

            spaz = player.actor
            if not isinstance(spaz, Spaz):
                continue
            if not spaz.node.exists():
                continue

            tx, ty, tz = spaz.node.position
            dist = math.sqrt(
                (tx - ox) ** 2 +
                (ty - oy) ** 2 +
                (tz - oz) ** 2
            )

            if dist < closest_dist:
                closest_dist = dist
                closest_spaz = spaz

        if not closest_spaz or closest_dist > 8.0:
            return

        # ---------------- Chase ----------------

        tx, ty, tz = closest_spaz.node.position

        vel = (
            5.0 if tx > ox else -5.0,
            5.0 if ty > oy else -5.0,
            5.0 if tz > oz else -5.0,
        )

        source = self.source_players[0] if self.source_players else None

        Blast(
            position=self.node.position,
            blast_radius=1.2,
            blast_type='punch',
            source_player=source,
        ).autoretain()

        self.node.velocity = vel

    # -----------------------------------------------------

    def _on_probe_hit(self) -> None:
        """Obstacle avoidance (raycast replacement)."""
        if not self.node.exists():
            return

        vx, vy, vz = self.node.velocity

        # Turn sideways instead of getting stuck
        self.node.velocity = (
            -vz * 0.8,
            vy,
            vx * 0.8,
        )

    # -----------------------------------------------------

    def _is_enemy(self, player: bs.Player) -> bool:
        if not player.exists():
            return False

        if player in self.source_players:
            return False

        if self.source_players:
            src = self.source_players[0]
            if src.exists() and player.team is src.team:
                return False

        return True

    # -----------------------------------------------------

    def handlemessage(self, msg: Any) -> None:
        if isinstance(msg, bs.DieMessage):
            if self.node.exists():
                pptx(
                    'Goodbye!',
                    position=self.node.position,
                ).autoretain()
                self.node.delete()

            if self._probe.exists():
                self._probe.delete()

            self._update_timer = None

        elif isinstance(msg, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage())

        else:
            super().handlemessage(msg)

    # -----------------------------------------------------

    @classmethod
    def get_factory(cls) -> BotFactory:
        activity = bs.getactivity()
        if not hasattr(activity, '_bot_factory'):
            activity._bot_factory = BotFactory()
        return activity._bot_factory

