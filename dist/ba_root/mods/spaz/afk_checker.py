import babase
import bascenev1 as bs
import bascenev1lib
import random
from spaz import member_id as mem
from bascenev1lib.actor.playerspaz import PlayerSpaz
from typing import Sequence
from bascenev1lib.actor.popuptext import PopupText as pptx
from spaz import admin
import babase

# add strike system later
# 3x afk = kick

AFK_REMOVED = {}

def afk_main(self, player):
    p = player.get_account_id()
    timeout = 60
    self.last_change_time = bs.time()
    self._warned = set()

    def afk_checker(to):  # inspiration by logic, improved by PCModder
        t = bs.time()
        inactive = t - self.last_change_time

        if p not in mem.owner:# owner bypass!
         if self.is_alive():
            for w in (30, 50, 50):
                if inactive >= w and w not in self._warned:
                    self._warned.add(w)
                    pptx(
                        f"AFK ({int(inactive)}s)",
                        color=(1, 0, 0),
                        scale=1.5,
                        position=self.node.position,
                    ).autoretain()

            if inactive >= to:
                acc = player.get_account_id()

                AFK_REMOVED[acc] = {
                    "time": t,
                    "duration": inactive
                }
                bs.broadcastmessage(
                    f"Removing {player.getname()} for being AFK for more than {to} seconds"
                )
                player.remove_from_game()
    self.afk_timer = bs.Timer(1.0, babase.CallStrict(afk_checker, timeout), repeat=True)