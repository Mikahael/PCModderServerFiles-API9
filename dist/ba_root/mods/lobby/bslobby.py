# Released under the MIT License. See LICENSE for details.
#
"""Implements lobby system for gathering before games, char select, etc."""
# pylint: disable=too-many-lines

from __future__ import annotations

import logging
import weakref
from dataclasses import dataclass
from typing import TYPE_CHECKING

from bascenev1 import _lobby
from bascenev1._lobby import Chooser

import bascenev1
import babase
import _bascenev1
from bascenev1._profile import get_player_profile_colors
from bascenev1._gameutils import animate, animate_array
from spaz import afk_checker as afk

if TYPE_CHECKING:
    from typing import Any, Sequence

    import bascenev1

MAX_QUICK_CHANGE_COUNT = 30
QUICK_CHANGE_INTERVAL = 0.05
QUICK_CHANGE_RESET_INTERVAL = 1.0

def new__init__(
        self,
        vpos: float,
        sessionplayer: bascenev1.SessionPlayer,
        lobby: 'Lobby',
    ) -> None:
        self._deek_sound = _bascenev1.getsound('deek')
        self._click_sound = _bascenev1.getsound('click01')
        self._punchsound = _bascenev1.getsound('punch01')
        self._swish_sound = _bascenev1.getsound('punchSwish')
        self._errorsound = _bascenev1.getsound('error')
        self._mask_texture = _bascenev1.gettexture('characterIconMask')
        self._vpos = vpos
        self._lobby = weakref.ref(lobby)
        self._sessionplayer = sessionplayer
        self._inited = False
        self._dead = False
        self._text_node: bascenev1.Node | None = None
        self._profilename = ''
        self._profilenames: list[str] = []
        self._ready: bool = False
        self._character_names: list[str] = []
        self._last_change: Sequence[float | int] = (0, 0)
        self._profiles: dict[str, dict[str, Any]] = {}

        app = babase.app
        assert app.classic is not None

        # Load available player profiles either from the local config or
        # from the remote device.
        self.reload_profiles()

        # Note: this is just our local index out of available teams; *not*
        # the team-id!
        self._selected_team_index: int = self.lobby.next_add_team

        # Store a persistent random character index and colors; we'll use this
        # for the '_random' profile. Let's use their input_device id to seed
        # it. This will give a persistent character for them between games
        # and will distribute characters nicely if everyone is random.
        self._random_color, self._random_highlight = get_player_profile_colors(
            None
        )

        # To calc our random character we pick a random one out of our
        # unlocked list and then locate that character's index in the full
        # list.
        char_index_offset: int = app.classic.lobby_random_char_index_offset
        self._random_character_index = (
            sessionplayer.inputdevice.id + char_index_offset
        ) % len(self._character_names)

        # Attempt to set an initial profile based on what was used previously
        # for this input-device, etc.
        self._profileindex = self._select_initial_profile()
        self._profilename = self._profilenames[self._profileindex]

        self._text_node = _bascenev1.newnode(
            'text',
            delegate=self,
            attrs={
                'position': (-100, self._vpos),
                'maxwidth': 160,
                'shadow': 0.5,
                'vr_depth': -20,
                'h_align': 'left',
                'v_align': 'center',
                'v_attach': 'top',
            },
        )
        animate(self._text_node, 'scale', {0: 0, 0.1: 1.0})
        self.icon = _bascenev1.newnode(
            'image',
            owner=self._text_node,
            attrs={
                'position': (-130, self._vpos + 20),
                'mask_texture': self._mask_texture,
                'vr_depth': -10,
                'attach': 'topCenter',
            },
        )

        animate_array(self.icon, 'scale', 2, {0: (0, 0), 0.1: (45, 45)})

        from bascenev1 import get_foreground_host_session
        import bascenev1 as bs
        session = get_foreground_host_session()
        session_players = session.sessionplayers
        acc_name = self._sessionplayer.inputdevice.get_v1_account_name(True)
        #
        clID = self._sessionplayer.inputdevice.client_id

        #
        acc = None
        name = None
        #
        for i in session_players:
            if i.inputdevice.client_id==clID:
                acc = i.get_v1_account_id()
                name = i.getname(full=True, icon=False)
                break


        from lobby import daily_cash as daily

        if acc is None:
            bs.broadcastmessage("Player details not found! Rejoin!", clients=[clID], transient=True)
            return

        if acc in afk.AFK_REMOVED:
            data = afk.AFK_REMOVED.pop(acc)
            bs.broadcastmessage(f"You were removed for being AFK ({int(data['duration'])}s!)", clients=[clID], transient=True)
        else:
            # moved to daily_cash.py
            daily.add_cash(clID,acc_name)

        # Set our initial name to '<choosing player>' in case anyone asks.
        self._sessionplayer.setname(
            babase.Lstr(resource='choosingPlayerText').evaluate(), real=False
        )

        # Init these to our rando but they should get switched to the
        # selected profile (if any) right after.
        self._character_index = self._random_character_index
        self._color = self._random_color
        self._highlight = self._random_highlight

        self.update_from_profile()
        self.update_position()
        self._inited = True

        self._set_ready(False)

def new_reload_profiles(self) -> None:
        """Reload all player profiles."""

        app = babase.app
        assert app.classic is not None

        # Re-construct our profile index and other stuff since the profile
        # list might have changed.
        input_device = self._sessionplayer.inputdevice
        is_remote = input_device.is_remote_client
        is_test_input = input_device.is_test_input

        # Pull this player's list of unlocked characters.
        if is_remote:
            # TODO: Pull this from the remote player.
            # (but make sure to filter it to the ones we've got).
            self._character_names = ['Spaz','Grumbledorf','Zoe','Mel','Santa Claus','Frosty','Bones','Bernard','Pixel','Pascal','Taobao Mascot','Agent Johnson','B-9000','Easter Bunny','Kronk','Snake Shadow','Jack Morgan']
        else:
            self._character_names = ['Spaz','Grumbledorf','Zoe','Mel','Santa Claus','Frosty','Bones','Bernard','Pixel','Pascal','Taobao Mascot','Agent Johnson','B-9000','Easter Bunny','Kronk','Snake Shadow','Jack Morgan']

        # If we're a local player, pull our local profiles from the config.
        # Otherwise ask the remote-input-device for its profile list.
        if is_remote:
            self._profiles = input_device.get_player_profiles()
        else:
            self._profiles = app.config.get('Player Profiles', {})

        # These may have come over the wire from an older
        # (non-unicode/non-json) version.
        # Make sure they conform to our standards
        # (unicode strings, no tuples, etc)
        self._profiles = app.classic.json_prep(self._profiles)

        # Filter out any characters we're unaware of.
        for profile in list(self._profiles.items()):
            if (
                profile[1].get('character', '')
                not in app.classic.spaz_appearances
            ):
                profile[1]['character'] = 'Spaz'

        # Add in a random one so we're ok even if there's no user profiles.
        self._profiles['_random'] = {}

        # In kiosk mode we disable account profiles to force random.
        variant = babase.app.env.variant
        vart = type(variant)
        arcade_or_demo = variant is vart.ARCADE or variant is vart.DEMO

        if arcade_or_demo:
            if '__account__' in self._profiles:
                del self._profiles['__account__']

        # For local devices, add it an 'edit' option which will pop up
        # the profile window.
        if not is_remote and not is_test_input and not arcade_or_demo:
            self._profiles['_edit'] = {}

        # Build a sorted name list we can iterate through.
        self._profilenames = list(self._profiles.keys())
        self._profilenames.sort(key=lambda x: x.lower())

        if self._profilename in self._profilenames:
            self._profileindex = self._profilenames.index(self._profilename)
        else:
            self._profileindex = 0
            self._profilename = self._profilenames[self._profileindex]

def get_players():
    from bascenev1 import get_foreground_host_session
    import bascenev1 as bs

    session = get_foreground_host_session()

    if session:
        for p in session.sessionplayers:
            try:
                name = p.getname(full=True, icon=False)
                acc = p.get_v1_account_id()
                client_id = p.inputdevice.client_id
                account_name = p.inputdevice.get_v1_account_name(True)

                print(f"{account_name} ---> {acc} ---> {client_id}")
            except Exception:
                pass

def enable_lobby():
    Chooser.__init__ = new__init__
    Chooser.reload_profiles = new_reload_profiles