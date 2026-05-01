import bascenev1 as bs
from bascenev1 import get_foreground_host_session
import babase
import os
import json
from random import randrange
from datetime import datetime
from fire import *
from spaz import member_id as mid

correctAnswer = None
answeredBy = None

chatmessage = bs.chatmessage

# New proper path
bankfile = 'ba_root/mods/config/bank.json'


def run_in_context(func):
    activity = bs.get_foreground_host_activity()
    if activity:
        with activity.context:
            func()

def checkExpiredItems():
    customers = gph.effectCustomers.copy()
    updated = False

    for key, value in list(customers.items()):
        expiry = datetime.strptime(value['expiry'], '%d-%m-%Y %H:%M:%S')
        if expiry < datetime.now():
            print("Expired item found:", key)
            customers.pop(key)
            updated = True

    if updated:
        file_path = os.path.join(
            babase.app.env.python_directory_user,
            'getPermissionsHashes.py'
        )
        with open(file_path, 'r') as f:
            lines = f.readlines()

        lines[4] = f"effectCustomers = {customers}\n"

        with open(file_path, 'w') as f:
            f.writelines(lines)


def askQuestion():
    global correctAnswer, answeredBy

    keys = list(questionsList.keys())
    question = keys[randrange(len(keys))]
    correctAnswer = questionsList[question]

    if question == 'add':
        a = randrange(100, 999)
        b = randrange(10, 99)
        correctAnswer = str(a + b)
        question = f"What is {a} + {b}?"

    elif question == 'multiply':
        a = randrange(100, 999)
        b = [0, 1, 5, 10][randrange(4)]
        correctAnswer = str(a * b)
        question = f"What is {a} x {b}?"

    chatmessage(question)
    #print(question)
    answeredBy = None

    #checkExpiredItems()
    # check expired items later

def checkAnswer(msg: str, client_id: int):
    global answeredBy

    activity = bs.get_foreground_host_activity()
    if activity is None:
        return

    if msg.strip() != correctAnswer:
        return

    if answeredBy is not None:
        bs.broadcastmessage(
            f"Already answered by {answeredBy}",
            clients=[client_id], transient=True
        )
        return
            
    session = get_foreground_host_session()
    session_players=session.sessionplayers
    for i in session_players:
        if i.inputdevice.client_id==client_id:
            account_id = i.get_account_id()
            answeredBy = i.getname()

            chatmessage(f"{answeredBy}: {msg}")

            try:
                bs.broadcastmessage(
                    f"Congratulations {answeredBy}! You won 🎟10",
                    clients=[client_id], transient=True
                )
                addCoins(account_id, 10)
            except Exception as e:
                print("Reward error:", e)


def addCoins(account_id, amount):
    if os.path.exists(bankfile):
        with open(bankfile) as f:
            bank = json.load(f)
    else:
        bank = {}

    bank[account_id] = bank.get(account_id, 0) + amount

    with open(bankfile, 'w') as f:
        json.dump(bank, f)

    if amount > 0:
        run_in_context(lambda: bs.getsound('cashRegister').play())

    print("Transaction successful")
    coins = getCoins(account_id)
    print(coins)


def getCoins(account_id):
    if os.path.exists(bankfile):
        with open(bankfile) as f:
            bank = json.load(f)
            return bank.get(account_id, 0)
    return 0


# Start Coin System!
coin_timer = None

def enable_coinsys():
    global coin_timer

    if enableCoinSystem:
        coin_timer = bs.AppTimer(
            questionDelay,
            askQuestion,
            repeat=True
        )
        print("Coin system loaded...")
    else:
        print("CoinSys turned off!")