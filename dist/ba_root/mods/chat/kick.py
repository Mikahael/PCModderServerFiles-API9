# Released under the MIT License. See LICENSE for details.

from __future__ import annotations

import babase
import bascenev1 as bs
import _bascenev1 as _bs
import _babase

from spaz import member_id as mid
import fire

banned: list[str] = []


def run() -> None:
    try:
        global banned

        roster = bs.get_game_roster()
        banned = mid.ban_list

        for i in roster:

            name = i['display_string']
            client_id = i['client_id']
            acc = i['account_id']

            # Kick banned players.
            if acc in banned:

                bs.broadcastmessage(
                    "You have been banned! Contact Server Admins!",
                    color=(1, 1, 1),
                    clients=[client_id], transient=True,
                )

                if client_id != -1:
                    bs.disconnect_client(client_id)
            
            if fire.whitelist:
                
                if acc not in mid.whitelist and acc not in mid.owner: # owners not allowed to be kicked even in whitelist
                    bs.broadcastmessage(
                        "Whitelist is active, Please join later!",
                        color=(1, 1, 1),
                        clients=[client_id], transient=True,
                    )

                    if client_id != -1:
                        bs.disconnect_client(client_id)

    except Exception as e:
        print(e)

    babase.apptimer(2.0, run)


def new_kick():
    babase.apptimer(2.0, run)
    print('✅ Ban list running')