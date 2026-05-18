import json
import os
import random
from datetime import date
import bascenev1 as bs

#DAILY_FILE = 'daily_rewards.json'
DAILY_FILE = 'ba_root/mods/lobby/daily_rewards.json'


def load_daily():
    if os.path.exists(DAILY_FILE):
        with open(DAILY_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_daily(data):
    with open(DAILY_FILE, 'w') as f:
        json.dump(data, f)


def add_cash(clID,acc_name):
    from chat import coin_system as coin

    today = str(date.today())  # Example: 2026-05-18
    daily_data = load_daily()
    
    from bascenev1 import get_foreground_host_session
    import babase
    ticket = babase.charstr(babase.SpecialChar.TICKET)
    session = get_foreground_host_session()
    session_players = session.sessionplayers
    
    acc = None
    name = None
    #
    for i in session_players:
        if i.inputdevice.client_id==clID:
            acc = i.get_account_id()
            name = i.getname()
            break

    # Get last claimed date for this account
    last_claim = daily_data.get(acc)

    # Already claimed today
    if last_claim == today:
        bs.broadcastmessage(f'Welcome to the Server! {acc_name} | {acc} | {str(clID)}', clients=[clID], transient=True)
        return

    # Give reward
    cash_amount = random.choice([25, 50, 15, 10])
    coin.addCoins(acc, cash_amount)

    # Save today's claim
    daily_data[acc] = today
    save_daily(daily_data)
    bs.broadcastmessage(f'Welcome to the Server! {acc_name} | {acc} | {str(clID)}\n Daily Login Cash: {ticket}{cash_amount}!', 
        clients=[clID], transient=True
    )
