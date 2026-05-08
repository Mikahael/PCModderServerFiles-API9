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
    
    
    effects = {
            "spark": 300,
            "sparkground": 350,
            "sweat": 300,
            "sweatground": 350,
            "distortion": 300,
            "rainbow": 300,
            "ice": 300,
            "iceground": 350,
            "slime": 300,
            "metal": 200,
            "splinter": 200,
            "fairydust": 300,
            "star": 350,
            "newrainbow": 350,
            "footprint": 125,
            "fire": 400,
            "firespark": 450
            }
    
    tags = ('tag1','tag2','tag3','tag4','tag5','tag6')
    tags_description = (f'tag1 - Standard Color Tag - 25', 
             'tag2 - Red and Yellow Tag - 45', 
             'tag3 - Smooth Color Wave - 40',
             'tag4 - Blink Letter Wave - 50',
             'tag5 - Rainbow Tag - 60')
    
    avail_commands = {
            '/spaz': 50, '/spaz all': 100, '/inv': 40, '/inv all': 80,
            '/freeze': 600, '/freeze all': 1000, '/sleep': 400, '/sleep all': 800,
            '/thaw': 500, '/thaw all': 700, '/kill': 800, '/kill all': 1500,
            '/end': 250, '/curse': 550, '/curse all': 1000,
            '/tint': 190, '/sm': 100,
            '/heal': 150, '/heal all': 170,
            '/shield': 150, '/shield all': 150, '/punch': 150, '/punch all': 150,
            '/gm': 900
        }
        
    #chatmessage(avail_commands)
    
    def effects_cash(effect_name):
        cash = {
            "spark": 300,
            "sparkground": 350,
            "sweat": 300,
            "sweatground": 350,
            "distortion": 300,
            "rainbow": 300,
            "ice": 300,
            "iceground": 350,
            "slime": 300,
            "metal": 200,
            "splinter": 200,
            "fairydust": 300,
            "star": 350,
            "newrainbow": 350,
            "footprint": 125,
            "fire": 400,
            "firespark": 450
            }
        if isinstance(effect_name, str):
            return cash.get(effect_name)
            
        elif isinstance(effect_name, (list, tuple)):
            return {e: cash.get(e) for e in effect_name}
            
    def tags_cash(tag_name): # special thx to ashx for cool tags!
        cash = {
            'tag1': 25, #Standard Color Tag - 25
            'tag2':45, #Red & Yellow Wave - 45
            'tag3': 40, #Smooth Color Wave - 40
            'tag4':50, #Blink Letter Wave - 50
            'tag5': 60, #Rainbow Tag - 60
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
        lines = [f"{dec:<15} {price}💰" for dec, price in effects.items()]

        # pair into two columns
        pairs = []
        for i in range(0, len(lines), 2):
            left = lines[i]
            right = lines[i+1] if i+1 < len(lines) else ""
            pairs.append(f"{left}   |   {right}")

        # send 5 rows per message
        for i in range(0, len(pairs), 5):
            chatmessage("\n".join(pairs[i:i+5]))
    elif msg == '/shop tags':
        for tag in tags_description:
            name, desc, price = tag.split(' - ')
            chatmessage(f"{name:<6} - {desc:<22} - {price}💰")
    elif msg == '/shop cmds':
        lines = [f"{cmd:<15} {price}💰" for cmd, price in avail_commands.items()]

        # pair into two columns
        pairs = []
        for i in range(0, len(lines), 2):
            left = lines[i]
            right = lines[i+1] if i+1 < len(lines) else ""
            pairs.append(f"{left}   |   {right}")

        # send 5 rows per message
        for i in range(0, len(pairs), 5):
            chatmessage("\n".join(pairs[i:i+5]))
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
                
            if acc in mid.name:
                chatmessage('You already have Custom tag!')
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