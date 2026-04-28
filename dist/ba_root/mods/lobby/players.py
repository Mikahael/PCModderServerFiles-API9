# players.py

from bascenev1 import get_foreground_host_session


def get_players():
    session = get_foreground_host_session()
    result = []

    if not session:
        return result

    for p in session.sessionplayers:
        try:
            if not p.inputdevice:
                continue

            player_data = {
                "name": p.getname(),
                "account_id": p.get_v1_account_id(),
                "client_id": p.inputdevice.client_id,
                "account_name": p.inputdevice.get_v1_account_name(True),
            }

            result.append(player_data)

        except Exception:
            continue

    return result
    print(result)
    
def log_players():
    for p in get_players():
        print(f"{p['account_name']} ---> {p['account_id']} ---> {p['client_id']}")