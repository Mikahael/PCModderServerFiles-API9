from bascenev1 import get_foreground_host_session, get_foreground_host_activity, get_game_roster
import bascenev1 as bs
import babase, _babase
import os, json
from chat import hooks
from spaz import member_id as mid
from spaz import admin
from spaz import decorator
from chat import coin_system as coin
from datetime import datetime, timedelta
#
#
#

def main_shop_function(msg, client_id):
    #
    session = get_foreground_host_session()
    session_players=session.sessionplayers
    for i in session_players:
        if i.inputdevice.client_id==client_id:
            acc = i.get_account_id()
            name = i.getname()
    chatmessage = bs.broadcastmessage
    
    user_cash = coin.getCoins(acc)
    
    
    effects = ('glow', 'particles', 'fallpro')
    
    def effects_cash(effect_name):
        cash = {
            'glow': 20,
            'particles':20,
            'fallpro': 20
            }
        if isinstance(effect_name, str):
            return cash.get(effect_name)
            
        elif isinstance(effect_name, (list, tuple)):
            return {e: cash.get(e) for e in effect_name}
    
    
    def save_to_py():
        file_path = 'ba_root/mods/spaz/member_id.py'

        with open(file_path, "r") as f:
            content = f.read()

        start = content.find("customers =")
        if start == -1:
            return

        brace_start = content.find("{", start)

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

        new_block = "customers = " + json.dumps(mid.customers, indent=4)

        new_content = content[:start] + new_block + content[end+1:]

        with open(file_path, "w") as f:
            f.write(new_content)
    
    def add_effect(acc_id, effect):
        customers = mid.customers
        customers.setdefault(acc_id, {"tags": {}, "effects": {}})
        effects = customers[acc_id]["effects"]
        if effect not in effects:
            expiry_time = datetime.now() + timedelta(hours=6)
            effects[effect] = expiry_time.strftime('%d-%m-%Y %H:%M:%S')
            return True
        return False
        
    def remove_effect(acc_id, effect):
        customers = mid.customers
        if acc_id in customers and effect in customers[acc_id]["effects"]:
            customers[acc_id]["effects"].remove(effect)
            return True
        return False
        
    a = msg.split(' ')[1:] # arguments
    customers = mid.customers
    data = customers.setdefault(acc, {"tags": {}, "effects": {}})
    c_effects = data["effects"]
    #start
    if msg == '/shop effects':
        chatmessage(f'Available Effects: {effects_cash(effects)}')
    elif msg == '/shop tags':
        tags = 'rainbow, regular, etc'
        chatmessage(f'Available Tags: {tags}')
    elif msg == '/shop glow':
        if a[0] not in c_effects:
            if user_cash > effects_cash(a[0]):
                chatmessage(f'Purchased Effect: {a[0]}!')
                #deduct coins!
                coin.deductCoins(acc, effects_cash(a[0]))
                #add the effect now
                if add_effect(acc, a[0]):
                    save_to_py() #hardcode save
            else:
                needed = (effects_cash(a[0]) - user_cash)
                chatmessage(f'Insufficient Funds! Need {str(needed)} more!')
        else:
            chatmessage(f'You already have: {a[0]}!')