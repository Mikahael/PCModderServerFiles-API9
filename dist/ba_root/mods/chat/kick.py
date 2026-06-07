from __future__ import annotations

import babase
import bascenev1 as bs
import random

from spaz import member_id as mid
from chat import master_logger as log # for master logger!
import fire

banned: list[str] = []

def run() -> None:
    try:
        global banned

        roster = bs.get_game_roster()

        current_accounts: set[str] = set()

        banned = mid.ban_list
        
        settings = log.master_load_db("settings")

        for i in roster:

            name = i['display_string']
            client_id = i['client_id']
            acc = i['account_id']

            if not acc:
                continue

            current_accounts.add(acc)

            # New account detected.
            if acc not in log.active_players:
                if client_id != -1: #ignore server
                    log.player_join(acc, name)

                # Ban check.
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

                # Whitelist check - fire.json
                if settings["whitelist"]:

                    if acc not in mid.whitelist and acc not in mid.owner:

                        bs.broadcastmessage(
                            "Whitelist is active, Please join later!",
                            color=(1, 1, 1),
                            clients=[client_id],
                            transient=True,
                        )

                        if client_id != -1:
                            bs.disconnect_client(client_id)

                        continue

                # Welcome message.
                if client_id != -1:

                    bs.broadcastmessage(
                        u'\ue043Welcome to the server by PCModder!\ue043',
                        color=(
                            random.random(),
                            random.random(),
                            random.random()
                        ),
                        clients=[client_id],
                        transient=True,
                    )

        # Detect leaves.
        for acc in list(log.active_players.keys()):

            if acc not in current_accounts:
                log.player_leave(acc)

    except Exception as e:
        print(f"[Master Log] {e}")

    babase.apptimer(2.0, run)


def new_kick():
    babase.apptimer(2.0, run)
    print('✅ Master Log running!')