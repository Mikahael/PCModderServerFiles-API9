import json
import os
import random
from datetime import date
import bascenev1 as bs
import random

import babase
import _bascenev1

from bascenev1._stats import PlayerRecord, PlayerScoredMessage
from chat import coin_system as coin
from chat import master_logger as log

master = log.master_load_db("player")

#DAILY_FILE = relocated to master_log.json


def load_daily():
    if os.path.exists(DAILY_FILE):
        with open(DAILY_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_daily(data):
    with open(DAILY_FILE, 'w') as f:
        json.dump(data, f)


def add_cash(clID, acc_name):

    today = str(date.today())

    from bascenev1 import get_foreground_host_session
    import babase

    ticket = babase.charstr(babase.SpecialChar.TICKET)

    session = get_foreground_host_session()
    session_players = session.sessionplayers

    acc = None
    name = None

    for i in session_players:
        if i.inputdevice.client_id == clID:
            acc = i.get_account_id()
            name = i.getname()
            break

    if acc is None:
        return
        
    master = log.master_load_db("player")
    log.ensure_player(master, acc, name)
    master = log.master_load_db("player")

    # Always reload latest database
    master = log.master_load_db("player")

    # Create/repair player entry if needed
    log.ensure_player(master, acc, name)

    last_claim = master[acc]["last_claim"]

    # Already claimed today
    if last_claim == today:
        bs.broadcastmessage(
            f'Welcome to the Server! {acc_name} | {acc} | {clID}',
            clients=[clID],
            transient=True
        )
        return

    # Give reward
    cash_amount = random.choice([25, 50, 15, 10])
    coin.addCoins(acc, cash_amount)

    master = log.master_load_db("player")
    master[acc]["last_claim"] = today
    log.master_save_db("player", master)

    bs.broadcastmessage(
        f'Welcome to the Server! {acc_name} | {acc} | {clID}\n'
        f'Daily Login Cash: {ticket}{cash_amount}!',
        clients=[clID],
        transient=True
    )

def submit_kill_patch(self, showpoints: bool = True) -> None:
    """Submit a kill for this player entry."""

    self._multi_kill_count += 1
    stats = self._stats()
    assert stats

    ticket = babase.charstr(babase.SpecialChar.TICKET)
    clID = self.player.inputdevice.client_id

    if self._multi_kill_count == 1:
        score = 0
        name = None
        delay = 0.0
        color = (0.0, 0.0, 0.0, 1.0)
        scale = 1.0
        sound = None
        # give some like 5 cash per kill!
        account_id = self.player.get_account_id()
        coin.addCoins(account_id, 5)

    elif self._multi_kill_count == 2:
        score = 20
        name = babase.Lstr(resource='twoKillText')
        color = (0.1, 1.0, 0.0, 1)
        scale = 1.0
        delay = 0.0
        sound = stats.orchestrahitsound1
        # give some like 5 cash per kill!
        account_id = self.player.get_account_id()
        coin.addCoins(account_id, 5)

    elif self._multi_kill_count == 3:
        score = 40
        name = babase.Lstr(resource='threeKillText')
        color = (1.0, 0.7, 0.0, 1)
        scale = 1.1
        delay = 0.3
        sound = stats.orchestrahitsound2

        account_id = self.player.get_account_id()
        player_name = self.getname()
        # give some cash for kill
        coin.addCoins(account_id, 25)
        #
        _bascenev1.broadcastmessage(
            f'Well played {player_name}! {ticket}25 bonus!',
            color=(1, 1, 1),
            clients=[clID],
            transient=True,
        )

    elif self._multi_kill_count == 4:
        score = 60
        name = babase.Lstr(resource='fourKillText')
        color = (1.0, 1.0, 0.0, 1)
        scale = 1.2
        delay = 0.6
        sound = stats.orchestrahitsound3

        account_id = self.player.get_account_id()
        player_name = self.getname()
        #
        coin.addCoins(account_id, 50)
        #
        _bascenev1.broadcastmessage(
            f'Well played {player_name}! {ticket}50 bonus!',
            color=(1, 1, 1),
            clients=[clID],
            transient=True,
        )

    elif self._multi_kill_count == 5:
        score = 80
        name = babase.Lstr(resource='fiveKillText')
        color = (1.0, 0.5, 0.0, 1)
        scale = 1.3
        delay = 0.9
        sound = stats.orchestrahitsound4

        account_id = self.player.get_account_id()
        player_name = self.getname()
        # big cash bonus
        coin.addCoins(account_id, 75)
        #
        _bascenev1.broadcastmessage(
            f'Well played {player_name}! {ticket}75 bonus!',
            color=(1, 1, 1),
            clients=[clID],
            transient=True,
        )

    else:
        score = 100
        name = babase.Lstr(
            resource='multiKillText',
            subs=[('${COUNT}', str(self._multi_kill_count))],
        )
        color = (1.0, 0.5, 0.0, 1)
        scale = 1.3
        delay = 1.0
        sound = stats.orchestrahitsound4

    def _apply(
        name2,
        score2,
        showpoints2,
        color2,
        scale2,
        sound2,
    ) -> None:
        from bascenev1lib.actor.popuptext import PopupText

        our_pos = None

        if self._sessionplayer:
            if self._sessionplayer.activityplayer is not None:
                try:
                    our_pos = self._sessionplayer.activityplayer.position
                except babase.NotFoundError:
                    pass

        if our_pos is None:
            return

        our_pos = babase.Vec3(
            our_pos[0] + (random.random() - 0.5) * 2.0,
            our_pos[1] + (random.random() - 0.5) * 2.0,
            our_pos[2] + (random.random() - 0.5) * 2.0,
        )

        activity = self.getactivity()

        if activity is not None:
            PopupText(
                babase.Lstr(
                    value=(('+' + str(score2) + ' ')
                           if showpoints2 else '')
                    + '${N}',
                    subs=[('${N}', name2)],
                ),
                color=color2,
                scale=scale2,
                position=our_pos,
            ).autoretain()

        if sound2:
            sound2.play()

        self.score += score2
        self.accumscore += score2

        if score2 != 0 and activity is not None:
            activity.handlemessage(
                PlayerScoredMessage(score=score2)
            )

    if name is not None:
        _bascenev1.timer(
            0.3 + delay,
            babase.CallStrict(
                _apply,
                name,
                score,
                showpoints,
                color,
                scale,
                sound,
            ),
        )

    self._multi_kill_timer = _bascenev1.Timer(
        1.0,
        self._end_multi_kill,
    )


def load_multikill_bonus():
    PlayerRecord.submit_kill = submit_kill_patch