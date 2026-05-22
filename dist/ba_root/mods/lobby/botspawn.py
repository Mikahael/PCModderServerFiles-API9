# mypatch.py

from typing import override
from random import randint
import random

import babase
import _bascenev1
import bascenev1 as bs
import fire

from bascenev1._gameactivity import GameActivity
from bascenev1._multiteamsession import MultiTeamSession
from bascenev1 import _map
from maps import bstextonmap

from bascenev1lib.actor.spazbot import (
    SpazBotSet,
    ChargerBot,
    BomberBot,
    BomberBotPro,
    BomberBotProShielded,
    BrawlerBot,
    BrawlerBotPro,
    BouncyBot,
    TriggerBotPro,
    StickyBot,
    ExplodeyBot,
)

# Save original
_old_on_begin = GameActivity.on_begin


@override
def new_on_begin(self) -> None:
    # Call original first
    _old_on_begin(self) #TODO: add the extra mods here like nightmode and snowymap
    
    MapBounds = self.map.get_def_bound_box("map_bounds")
    spawnpoint = self.map.get_def_points('spawn')
    
    def snowymap():
        for i in range(5):
            pos = (random.uniform(MapBounds[0], MapBounds[3]),
                   MapBounds[4] - random.uniform(0, 0.3),
                   random.uniform(MapBounds[2], MapBounds[5]))
            
            vel = (0, 0, 0) 
            bs.emitfx(position=pos,
                      velocity=vel,
                      count=5,
                      scale=0.5,
                      spread=0.2,chunk_type='ice')
    if fire.snow:
        bs.timer(1, snowymap, repeat = True)
        

    def light() -> None:
        lightnode = bs.newnode(
            'light',
            attrs={
                'position': (0, 10, 0),
                'color': (0.2, 0.2, 0.4),
                'volume_intensity_scale': 1.0,
                'radius': 10,
            },
        )

        bs.animate(
            lightnode,
            'intensity',
            {
                0.0: 1,
                0.05: 10,
                0.15: 5,
                0.25: 0,
                0.26: 10,
                0.41: 5,
                0.51: 0,
            },
        )

        # Random delay between 5 and 20 seconds.
        delay = randint(5, 20)

        # Call again later.
        bs.timer(delay, light)

    def nightymode():
        import datetime
        now = datetime.datetime.now()
        activity = bs.get_foreground_host_activity()
        if now.hour >= 19 or now.hour <= 7:
            activity.globalsnode.tint = (0.5, 0.7, 1)
            light()
            fire.night = True
        else:
            fire.night = False

    nightymode()

    try:
        self._bots = SpazBotSet() # thx to lawgic, ported to 1.8 by PCModder!

        self.bot_types = [
            ChargerBot,
            BomberBot,
            BomberBotPro,
            BomberBotProShielded,
            BrawlerBot,
            BrawlerBotPro,
            BouncyBot,
            TriggerBotPro,
            StickyBot,
            ExplodeyBot,
        ]

        def btspawn():
            if len(self.players) == 1:
                try:
                    if not self._bots.have_living_bots():

                        player = self.players[0]

                        if (
                            player.actor is not None
                            and player.actor.node
                            and player.actor.node.exists()
                        ):
                            pos = player.actor.node.position

                            pt = (
                                pos[0],
                                pos[1] + 2,
                                pos[2],
                            )

                            self._bots.spawn_bot(
                                random.choice(self.bot_types),
                                pos=pt,
                                spawn_time=0.5,
                            )

                except Exception as e:
                    print(f'Bot spawn error: {e}')

            else:
                if hasattr(self, "botTimer"):
                    self.botTimer = None

        self.botTimer = bs.Timer(
            1.0,
            btspawn,
            repeat=True,
        )

        # Extra analytics if needed
        if len(self.players) == 1:
            bs.broadcastmessage(u"Solo mode detected: bots enabled!", color=(1,1,1)) # add later ffa and coop

    except Exception as e:
        print(f"Monkeypatch on_begin failed: {e}")


def new_ga_on_begin():
    GameActivity.on_begin = new_on_begin
    print('✅ Session mods running!')