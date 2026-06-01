from __future__ import annotations

import json
import os
import time
from datetime import datetime

PLAYER_DB = 'ba_root/mods/config/master_log.json'

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


def player_join(acc: str, name: str) -> None:

    if acc in active_players:
        return

    db = load_db()

    if acc not in db:
        db[acc] = {
            "name": name,
            "names": [name],
            "first_seen": get_time(),
            "last_join": "",
            "last_leave": "",
            "total_playtime": 0,
            "joins": 0,
        }

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
    
def player_profiles(player): # save entire player names
    db = load_db()
    profiles = player.inputdevice.get_player_profiles()

    acc = player.get_account_id()

    known = set(db[acc]["names"])

    for name in profiles:
        if name != "__account__" and name not in known:
            db[acc]["names"].append(name)
            known.add(name)

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
            account_id = i.get_account_id()
            name = i.getname()
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
            account_id = i.get_account_id()
            name = i.getname()
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
            account_id = i.get_account_id()
            name = i.getname()
            break
            
    chatlog = 'ba_root/mods/logs/chatlog.log'
    timestamp = datetime.now().strftime("%b %d %Y %H:%M:%S")
    
    with open(chatlog, "a", encoding="utf-8") as f:
        f.write(
            f"[{timestamp}] [{account_id}] [{name}] : {msg}\n"
        )
        
# TODO : add logging to show who added what roles to playa!