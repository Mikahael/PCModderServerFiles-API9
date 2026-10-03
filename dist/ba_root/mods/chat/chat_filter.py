import bascenev1 as bs
#import settings
from bascenev1 import get_foreground_host_session
import fire
from spaz import member_id as mem
import time
from chat import master_logger as log
import json


# account_id -> unmute_timestamp
muted_accounts = {}

MUTE_DURATION = 600  # 10 minutes (seconds)

BAD_WORDS = {
    'cum', 'cumshot', 'boob', 'boobies', 'tit', 'titz',
    'fuck', 'fucker', 'shit', 'shithead', 'pussy',
    'fucked', 'bitch', 'bitches', 'bietch',
    'sex', 'bastard'
}

# client_id -> warnings
warn_dict = {}


# ==============================
# Player lookup (API 9)
# ==============================

def is_owner(account_id):
    return account_id in mem.owner

def is_muted(account_id):
    if account_id not in muted_accounts:
        return False

    # Auto-unmute if time passed
    if time.time() >= muted_accounts[account_id]:
        muted_accounts.pop(account_id, None)
        return False

    return True


def mute_account(account_id):
    muted_accounts[account_id] = time.time() + MUTE_DURATION


def get_player_from_cid(client_id):
    session = get_foreground_host_session()
    if not session:
        return None, None, None

    for i in session.sessionplayers:
        try:
            if i.inputdevice and i.inputdevice.client_id == client_id:
                name = i.getname(True, False)
                account_id = i.get_v1_account_id()
                return i, name, account_id
        except Exception:
            pass

    return None, None, None


def ensure_client(client_id):
    warn_dict.setdefault(client_id, 0)


# ==============================
# Core logic
# ==============================

def handle_violation(cid, acc, name):
    ensure_client(cid)

    # First offense → warning
    if warn_dict[cid] == 0:
        warn_dict[cid] = 1
        bs.broadcastmessage(
            "⚠ Warning! Next violation will mute you for 10 minutes",
            color=(1, 0.8, 0),
            transient=True,
            clients=[cid]
        )
        return

    # Second offense → mute
    mute_account(acc)
    warn_dict.pop(cid, None)

    bs.broadcastmessage(
        f"[{name}] | [{acc}] : muted for 10 minutes (chat abuse)",
        color=(1, 1, 1),
        transient=True
    )



def check_message(cid, message):
    settings = log.master_load_db("settings")
    if not settings["chat_filter"]:
        return True  # allow chat

    player, name, acc = get_player_from_cid(cid)
    if not player or not acc:
        return True

    # 🚫 Owner bypass
    if is_owner(acc):
        return True

    # 🔇 Muted player → block message
    if is_muted(acc):
        remaining = int((muted_accounts[acc] - time.time()) / 60) + 1
        bs.broadcastmessage(
            f"You are muted for {remaining} more minute(s)",
            color=(1, 0.3, 0.3),
            transient=True,
            clients=[cid]
        )
        return False  # 🚨 THIS is what actually blocks chat

    msg = message.lower()
    for word in BAD_WORDS:
        if word in msg:
            handle_violation(cid, acc, name)
            log.filter_chat(msg, cid)
            log.chat_log(msg, cid)
            return False  # 🚨 block bad message

    return True  # allow clean messages
