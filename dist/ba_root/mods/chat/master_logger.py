from __future__ import annotations

import json
import os
import time
from datetime import datetime

PLAYER_DB = 'ba_root/mods/config/master_log.json'

DATABASES = {
    "settings": "ba_root/mods/fire.json",
    "pwp": "ba_root/mods/config/pwp.json",
    "spaz": "ba_root/mods/config/spaz.json",
    "bomb": "ba_root/mods/config/bomb.json",
    "player": 'ba_root/mods/config/master_log.json'
}

def master_load_db(name):
    path = DATABASES[name]

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def master_save_db(name, data):
    path = DATABASES[name]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


active_players = {}


def get_time() -> str:
    return datetime.now().strftime("%b %d %Y %H:%M")


def load_db():
    if not os.path.exists(PLAYER_DB):
        return {}

    with open(PLAYER_DB, "r") as f:
        return json.load(f)


def save_db(data):
    with open(PLAYER_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def ensure_player(db, acc, name="Unknown"):
    if acc not in db:
        db[acc] = {}

    defaults = {
        "name": name,
        "names": [name],
        "first_seen": get_time(),
        "last_join": "",
        "last_leave": "",
        "last_claim": "",
        "total_playtime": 0,
        "joins": 0,
        "bank": 0,
    }

    for key, value in defaults.items():
        if key not in db[acc]:
            if key == "names":
                db[acc][key] = [name]
            else:
                db[acc][key] = value

    return db

def player_join(acc: str, name: str) -> None:

    if acc in active_players:
        return

    db = load_db()
    ensure_player(db, acc, name)

    db[acc]["name"] = name

    if name not in db[acc]["names"]:
        db[acc]["names"].append(name)

    db[acc]["last_join"] = get_time()
    db[acc]["joins"] += 1

    save_db(db)

    # Store RAW timestamp for playtime calculation.
    active_players[acc] = {
        "join_time": time.time(),
        "name": name,
    }

    print(f"[JOIN] {name} ({acc})")


def player_leave(acc: str) -> None:

    if acc not in active_players:
        return

    db = load_db()

    leave_timestamp = time.time()

    session_time = int(
        leave_timestamp - active_players[acc]["join_time"]
    )

    if session_time < 0:
        session_time = 0

    if acc in db:

        db[acc]["last_leave"] = get_time()
        db[acc]["total_playtime"] += session_time

    save_db(db)

    del active_players[acc]

    print(
        f"[LEAVE] {acc} "
        f"(session={session_time}s)"
    )

def player_profiles(player):
    db = load_db()

    acc = player.get_v1_account_id()
    name = player.getname(True, False)


    ensure_player(db, acc, name)

    profiles = player.inputdevice.get_player_profiles()

    known = set(db[acc]["names"])

    if db[acc]: # only add if acc is already db else wait till its there and add!
        for profile_name in profiles:
            if (
                profile_name != "__account__"
                and profile_name not in known
                ):
                db[acc]["names"].append(profile_name)
                known.add(profile_name)

    save_db(db)

def chat_commands(msg, client_id):# for logging chat commands only
    #
    from bascenev1 import get_foreground_host_session
    import bascenev1 as bs

    session = get_foreground_host_session()
    session_players=session.sessionplayers
    account_id = None
    name = None
    for i in session_players:
        if i.inputdevice.client_id==client_id:
            account_id = i.get_v1_account_id()
            name = i.getname(True, False)
            break


    cmdlog = 'ba_root/mods/logs/cmdlog.log'
    timestamp = datetime.now().strftime("%b %d %Y %H:%M:%S")

    with open(cmdlog, "a", encoding="utf-8") as f:
        f.write(
            f"[{timestamp}] [{account_id}] [{name}] : {msg}\n"
        )

def filter_chat(msg, cid):
    #
    from bascenev1 import get_foreground_host_session
    import bascenev1 as bs

    session = get_foreground_host_session()
    session_players=session.sessionplayers
    account_id = None
    name = None
    for i in session_players:
        if i.inputdevice.client_id==cid:
            account_id = i.get_v1_account_id()
            name = i.getname(True, False)
            break

    filterlog = 'ba_root/mods/logs/filterlog.log'
    timestamp = datetime.now().strftime("%b %d %Y %H:%M:%S")

    with open(filterlog, "a", encoding="utf-8") as f:
        f.write(
            f"[{timestamp}] [{account_id}] [{name}] : {msg}\n"
        )

def chat_log(msg, client_id):
    #
    from bascenev1 import get_foreground_host_session
    import bascenev1 as bs

    session = get_foreground_host_session()
    session_players=session.sessionplayers
    account_id = None
    name = None
    for i in session_players:
        if i.inputdevice.client_id==client_id:
            account_id = i.get_v1_account_id()
            name = i.getname(True, False)
            break

    chatlog = 'ba_root/mods/logs/chatlog.log'
    timestamp = datetime.now().strftime("%b %d %Y %H:%M:%S")

    with open(chatlog, "a", encoding="utf-8") as f:
        f.write(
            f"[{timestamp}] [{account_id}] [{name}] : {msg}\n"
        )

# TODO : add logging to show who added what roles to playa!