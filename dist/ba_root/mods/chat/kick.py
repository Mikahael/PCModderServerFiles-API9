#

from __future__ import annotations

import babase
import bascenev1 as bs
import _babase

from spaz import member_id as mid
import fire

banned: list[str] = []
checked_clients: set[int] = set() # so infinite timer wont check people already in roster


def run() -> None:
    try:
        global banned
        global checked_clients

        roster = bs.get_game_roster()
        current_clients: set[int] = set()

        banned = mid.ban_list

        for i in roster:

            name = i['display_string']
            client_id = i['client_id']
            acc = i['account_id']

            current_clients.add(client_id)

            # Already checked this player.
            if client_id in checked_clients: # if client already in roster, skip
                continue

            checked_clients.add(client_id)

            # Kick banned players.
            if acc in banned:

                bs.broadcastmessage(
                    "You have been banned! Contact Server Admins!",
                    color=(1, 1, 1),
                    clients=[client_id],
                    transient=True,
                )

                if client_id != -1:
                    bs.disconnect_client(client_id)

                continue

            # Whitelist check.
            if fire.whitelist:

                # Owners bypass whitelist.
                if acc not in mid.whitelist and acc not in mid.owner:

                    bs.broadcastmessage(
                        "Whitelist is active, Please join later!",
                        color=(1, 1, 1),
                        clients=[client_id],
                        transient=True,
                    )

                    if client_id != -1:
                        bs.disconnect_client(client_id)

        # Remove disconnected clients.
        checked_clients &= current_clients # removes players who left the server from the roster list.

    except Exception as e:
        print(e)

    babase.apptimer(2.0, run)


def new_kick():
    babase.apptimer(2.0, run)
    print('✅ Ban list running')
    

