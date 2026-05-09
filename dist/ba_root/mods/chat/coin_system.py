import bascenev1 as bs
from bascenev1 import get_foreground_host_session
import babase
import os
import json
from random import randrange
from datetime import datetime
from fire import *
from spaz import member_id as mid
from chat import shop
from bascenev1lib.actor.zoomtext import ZoomText

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

def save_to_py():
    file_path = 'ba_root/mods/spaz/member_id.py'

    with open(file_path, "r") as f:
        content = f.read()

    start = content.find("customers =")
    if start == -1:
        return  # not found, safety

    # Find the first '{' after customers =
    brace_start = content.find("{", start)

    # Now find matching closing brace
    brace_count = 0
    end = brace_start

    for i in range(brace_start, len(content)):
        if content[i] == "{":
            brace_count += 1
        elif content[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                end = i
                break

    # Replace the whole block
    new_block = "customers = " + json.dumps(mid.customers, indent=4)

    new_content = content[:start] + new_block + content[end+1:]

    with open(file_path, "w") as f:
        f.write(new_content)
        
def clean_expired_effects():
    customers = mid.customers
    updated = False

    for acc_id, data in customers.items():
        effects = data.get("effects", {})

        # 🔹 FIX: convert old list → dict
        if isinstance(effects, list):
            effects = {e: datetime.now().strftime('%d-%m-%Y %H:%M:%S') for e in effects}
            data["effects"] = effects
            updated = True

        for effect, expiry_str in list(effects.items()):
            expiry = datetime.strptime(expiry_str, '%d-%m-%Y %H:%M:%S')

            if expiry < datetime.now():
                del effects[effect]
                updated = True

    if updated:
        bs.broadcastmessage('Item has been Expired!')
        save_to_py()
        
def clean_expired_tags():
    customers = mid.customers
    updated = False

    for acc_id, data in customers.items():
        tags = data.get("tags", {})

        # 🔹 convert old list → dict
        if isinstance(tags, list):
            tags = {
                e: {
                    "name": e,
                    "expiry": datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                }
                for e in tags
            }
            data["tags"] = tags
            updated = True

        for tag, val in list(tags.items()):
            
            # 🔹 handle OLD format (string)
            if isinstance(val, str):
                expiry_str = val

                # convert to new format
                tags[tag] = {
                    "name": tag,
                    "expiry": expiry_str
                }
                val = tags[tag]
                updated = True

            # 🔹 NEW format
            expiry_str = val.get("expiry")

            try:
                expiry = datetime.strptime(expiry_str, '%d-%m-%Y %H:%M:%S')
            except Exception:
                # bad data → remove it
                del tags[tag]
                updated = True
                continue

            if expiry < datetime.now():
                del tags[tag]
                updated = True

    if updated:
        bs.broadcastmessage('Item has been Expired!')
        save_to_py()


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

    #chatmessage(question)
    
    activity = bs.get_foreground_host_activity()

    with activity.context:
        global current_question_text

        current_question_text = ZoomText(
            text=question,
            position=(-250, 250),
            shiftposition=(-250, 250),
            shiftdelay=3.0,
            lifespan=3.0,
            flash=False,
            trail=False,
            scale = 0.30,
            color = (1,1,1)
            )
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


def deductCoins(account_id, amount):
    if os.path.exists(bankfile):
        with open(bankfile) as f:
            bank = json.load(f)
    else:
        bank = {}

    current = bank.get(account_id, 0)

    # 🔴 prevent negative balance
    if current < amount:
        print("Not enough coins")
        return False

    bank[account_id] = current - amount

    with open(bankfile, 'w') as f:
        json.dump(bank, f)

    run_in_context(lambda: bs.getsound('cashRegister').play())

    print("Deduction successful")
    coins = getCoins(account_id)
    print(coins)

    return True

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
        print("✅ Coin system loaded")
    else:
        print("CoinSys turned off!")