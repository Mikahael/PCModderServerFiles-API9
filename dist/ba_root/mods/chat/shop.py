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
    tags = ('neon', 'regular', 'cool')
    
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
            
    def tags_cash(tag_name):
        cash = {
            'neon': 20,
            'regular':20,
            'cool': 20
            }
        if isinstance(tag_name, str):
            return cash.get(tag_name)
            
        elif isinstance(tag_name, (list, tuple)):
            return {e: cash.get(e) for e in tag_name}
    
    
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
        
    def add_tag(acc_id, tag, tag_name):
        customers = mid.customers
        customers.setdefault(acc_id, {"tags": {}, "effects": {}})
    
        tags = customers[acc_id]["tags"]

        if tag not in tags:
            expiry_time = datetime.now() + timedelta(hours=6)

            tags[tag] = {
                "name": tag_name if tag_name else tag,
            "expiry": expiry_time.strftime('%d-%m-%Y %H:%M:%S')
            }

            return True
        return False
        
    def remove_effect(acc_id, effect):
        customers = mid.customers
        if acc_id in customers and effect in customers[acc_id]["effects"]:
            customers[acc_id]["effects"].remove(effect)
            return True
        return False
        
    a = msg.split(' ')[1:] # arguments
    m = msg.split(' ')[0]
    customers = mid.customers
    data = customers.setdefault(acc, {"tags": {}, "effects": {}})
    c_effects = data["effects"]
    c_tags = data["tags"]
    #start
    if msg == '/shop effects':
        chatmessage(f'Available Effects: {effects_cash(effects)}')
    elif msg == '/shop tags':
        chatmessage(f'Available Tags: {tags_cash(tags)}')
    elif m == '/buy':
        if not a:
            chatmessage('use /shop')
            return

        item = a[0]
        name = a[1] if len(a) > 1 else None

        # effect purchase
        if item in effects:
            if item in c_effects:
                chatmessage(f'You already have: {item}!')
                return

            price = effects_cash(item)
            if user_cash >= price:
                coin.deductCoins(acc, price)
                if add_effect(acc, item):
                    save_to_py()
                chatmessage(f'Purchased Effect: {item}!')
            else:
                chatmessage(f'Insufficient Funds! Need {price - user_cash} more!')

        # tag purchase
        elif item in tags:
            user_tags = customers.get(acc, {}).get("tags", {})
            
            if user_tags: # only allow client to have one tag at a time or clashing will occur between tags
                chatmessage('You already have a Tag!')
                return

            price = tags_cash(item)
            if user_cash >= price:
                if len(a) > 1: # what to do if client wants to buy tag but havent defined tag name!
                    coin.deductCoins(acc, price)
                    if add_tag(acc, item,tag_name=a[1]):
                        save_to_py()
                    chatmessage(f'Purchased Tag: {item}!')
                else:
                    chatmessage('Specify Tag Name as well!')
            else:
                chatmessage(f'Insufficient Funds! Need {price - user_cash} more!')

        else:
            chatmessage('Item not available! Use /shop instead!')