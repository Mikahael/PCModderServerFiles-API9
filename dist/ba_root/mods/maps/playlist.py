#
from __future__ import annotations

import copy
import logging
from typing import Any, TYPE_CHECKING

import babase

if TYPE_CHECKING:
    from typing import Sequence

    from bascenev1._session import Session

from bascenev1 import _playlist
import bascenev1 as bs

PlaylistType = list[dict[str, Any]]

def new_get_default_teams_playlist() -> PlaylistType: # edit default playlist for our epix playlist!
    """Return a default playlist for teams mode."""

    # NOTE: these are currently using old type/map names,
    # but filtering translates them properly to the new ones.
    # (is kinda a handy way to ensure filtering is working).
    # Eventually should update these though.
    return [
        {
            'settings': {
                'Epic Mode': True,
                'Flag Idle Return Time': 30,
                'Flag Touch Return Time': 0,
                'Respawn Times': 1.0,
                'Score to Win': 3,
                'Time Limit': 600,
                'map': 'Bridgit',
            },
            'type': 'bs_capture_the_flag.CTFGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Respawn Times': 1.0,
                'Score to Win': 3,
                'Time Limit': 600,
                'map': 'Rampage',
            },
            'type': 'bs_assault.AssaultGame',
        },
        {
            'settings': {
                'Balance Total Lives': False,
                'Epic Mode': True,
                'Lives Per Player': 3,
                'Respawn Times': 1.0,
                'Solo Mode': True,
                'Time Limit': 600,
                'map': 'The Pad',
            },
            'type': 'bs_elimination.EliminationGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Kills to Win Per Player': 5,
                'Respawn Times': 1.0,
                'Time Limit': 300,
                'map': 'Roundabout',
            },
            'type': 'bs_death_match.DeathMatchGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Kills to Win Per Player': 5,
                'Respawn Times': 1.0,
                'Time Limit': 300,
                'map': 'Football Stadium',
            },
            'type': 'bs_death_match.DeathMatchGame',
        },
        {
            'settings': {
                'Hold Time': 30,
                'Epic Mode': True,
                'Respawn Times': 1.0,
                'Time Limit': 300,
                'map': 'Football Stadium',
            },
            'type': 'bs_keep_away.KeepAwayGame',
        },
        {
            'settings': {
                'Balance Total Lives': False,
                'Epic Mode': True,
                'Lives Per Player': 1,
                'Respawn Times': 1.0,
                'Solo Mode': False,
                'Time Limit': 120,
                'map': 'Courtyard',
            },
            'type': 'bs_elimination.EliminationGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Respawn Times': 1.0,
                'Score to Win': 3,
                'Time Limit': 300,
                'map': 'Step Right Up',
            },
            'type': 'bs_assault.AssaultGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Kills to Win Per Player': 5,
                'Respawn Times': 1.0,
                'Time Limit': 300,
                'map': 'The Pad',
            },
            'type': 'bs_death_match.DeathMatchGame',
        },
        {
            'settings': {'Epic Mode': True, 'map': 'Rampage'},
            'type': 'bs_meteor_shower.MeteorShowerGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Flag Idle Return Time': 30,
                'Flag Touch Return Time': 0,
                'Respawn Times': 1.0,
                'Score to Win': 2,
                'Time Limit': 600,
                'map': 'Roundabout',
            },
            'type': 'bs_capture_the_flag.CTFGame',
        },
        {
            'settings': {
                'Respawn Times': 1.0,
                'Epic Mode': True,
                'Score to Win': 21,
                'Time Limit': 600,
                'map': 'Football Stadium',
            },
            'type': 'bs_football.FootballTeamGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Respawn Times': 0.25,
                'Score to Win': 3,
                'Time Limit': 120,
                'map': 'Bridgit',
            },
            'type': 'bs_assault.AssaultGame',
        },
        {
            'settings': {
                'Hold Time': 30,
                'Epic Mode': True,
                'Respawn Times': 1.0,
                'Time Limit': 300,
                'map': 'The Pad',
            },
            'type': 'bs_king_of_the_hill.KingOfTheHillGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Respawn Times': 1.0,
                'Score to Win': 2,
                'Time Limit': 300,
                'map': 'Zigzag',
            },
            'type': 'bs_assault.AssaultGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Flag Idle Return Time': 30,
                'Flag Touch Return Time': 0,
                'Respawn Times': 1.0,
                'Score to Win': 3,
                'Time Limit': 300,
                'map': 'Rampage',
            },
            'type': 'bs_capture_the_flag.CTFGame',#
        },
        {
            'settings': {
                'Epic Mode': True,
                'Kills to Win Per Player': 5,
                'Respawn Times': 1.0,
                'Time Limit': 300,
                'map': 'Monkey Face',
            },
            'type': 'bs_death_match.DeathMatchGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Hold Time': 30,
                'Respawn Times': 1.0,
                'Time Limit': 300,
                'map': 'Courtyard',
            },
            'type': 'bs_keep_away.KeepAwayGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Flag Idle Return Time': 30,
                'Flag Touch Return Time': 3,
                'Respawn Times': 1.0,
                'Score to Win': 2,
                'Time Limit': 300,
                'map': 'The Pad',
            },
            'type': 'bs_capture_the_flag.CTFGame',
        },
        {
            'settings': {
                'Balance Total Lives': False,
                'Epic Mode': True,
                'Lives Per Player': 3,
                'Respawn Times': 1.0,
                'Solo Mode': False,
                'Time Limit': 300,
                'map': 'Crag Castle',
            },
            'type': 'bs_elimination.EliminationGame',
        },
        {
            'settings': {
                'Epic Mode': True,
                'Respawn Times': 0.25,
                'Time Limit': 120,
                'map': 'Step Right Up',
            },
            'type': 'bs_conquest.ConquestGame',
        },
    ]

def new_playlist():
    bs._playlist.get_default_teams_playlist = new_get_default_teams_playlist