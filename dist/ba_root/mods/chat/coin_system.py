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
from maps import bstextonmap
from chat import master_logger as log


correctAnswer = None
answeredBy = None

chatmessage = bs.chatmessage

settings = log.master_load_db("settings")

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
    
    questionsList = settings["questionsList"]

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

    activity = bs.get_foreground_host_activity()
    with activity.context:
        
        # Delete old question node
        if bstextonmap.question_answer:
            bstextonmap.question_answer.delete()

        # Create new node
        bstextonmap.question_answer = bs.newnode(
            'text',
            attrs={
                'text': f"[{question}]",
                'scale': 0.0,
                'position': (-250, -80),
                'maxwidth': 700,
                'flatness': 0.0,
                'shadow': 0.5,
                'h_align': 'center',
                'v_align': 'center',
                'v_attach': 'top',
                'color': (1, 1, 1),
                'opacity': 1.0
            }
        )

        bs.animate(bstextonmap.question_answer, 'scale', {
            0.0: 0.0,
            0.25: 0.25,
            0.45: 0.45,
            0.6: 0.65,
            0.8: 0.85
        })

        bs.animate(bstextonmap.question_answer, 'opacity', {
            7.0: 1.0,
            9.5: 0.0,
        })

        bs.timer(18.5, bstextonmap.question_answer.delete)

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
            f"Already answered by {answeredBy}!",
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
                ticket = babase.charstr(babase.SpecialChar.TICKET)
                bs.broadcastmessage(
                    f"Congratulations {answeredBy}! You won {ticket}25",
                    clients=[client_id], transient=True)
                
                addCoins(account_id, 25)
                #
                if bstextonmap.question_answer: # say who won instead of deleting node
                    bstextonmap.question_answer.text = (f"Congratulations {answeredBy}! You won {ticket}25")
                    #bstextonmap.question_answer.delete()
                #
            except Exception as e:
                print("Reward error:", e)


def addCoins(account_id, amount):
    master = log.master_load_db("player")

    if account_id not in master:
        print(f"[WARN] addCoins: account not found: {account_id}")
        return

    master[account_id]["bank"] += amount

    log.master_save_db("player", master)

    if amount > 0:
        run_in_context(lambda: bs.getsound('cashRegister').play())


def deductCoins(account_id, amount):
    master = log.master_load_db("player")

    if account_id not in master:
        return False

    current = master[account_id]["bank"]

    if current < amount:
        return False

    master[account_id]["bank"] = current - amount

    log.master_save_db("player", master)

    run_in_context(lambda: bs.getsound('cashRegister').play())

    return True

def getCoins(account_id):
    master = log.master_load_db("player")

    if account_id not in master:
        return 0

    return master[account_id]["bank"]


# Start Coin System!
coin_timer = None

def enable_coinsys():
    global coin_timer
    
    questionDelay = settings["questionDelay"]
    
    if settings["enableCoinSystem"]:
        coin_timer = bs.AppTimer(
            questionDelay,
            askQuestion,
            repeat=True
        )
        print("✅ Coin system loaded")
    else:
        print("CoinSys turned off!")