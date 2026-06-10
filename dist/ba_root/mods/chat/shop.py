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
from babase import SpecialChar
from chat import master_logger as log

settings = log.master_load_db("settings")
#
# moved all prices to fire.json for dynamic central pricing!
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
    

    def parse_icons(tag: str) -> str:
        if '\\' not in tag:
            return tag

        replacements = {
        r'\d': '\ue048',
        r'\c': '\ue043',
        r'\h': '\ue049',
        r'\s': '\ue046',
        r'\n': '\ue04b',
        r'\f': '\ue04f',
        }

        for k, v in replacements.items():
            tag = tag.replace(k, v)

        return tag
  
    effects = {
            "spark": settings["effects"]["spark"],
            "sparkground": settings["effects"]["sparkground"],
            "sweat": settings["effects"]["sweat"],
            "sweatground": settings["effects"]["sweatground"],
            "distortion": settings["effects"]["distortion"],
            "rainbow": settings["effects"]["rainbow"],
            "ice": settings["effects"]["ice"],
            "iceground": settings["effects"]["iceground"],
            "slime": settings["effects"]["slime"],
            "metal": settings["effects"]["metal"],
            "splinter": settings["effects"]["splinter"],
            "fairydust": settings["effects"]["fairydust"],
            "star": settings["effects"]["star"],
            "newrainbow": settings["effects"]["newrainbow"],
            "footprint": settings["effects"]["footprint"],
            "fire": settings["effects"]["fire"],
            "firespark": settings["effects"]["firespark"]
    }
    
    tags = ('tag1','tag2','tag3','tag4','tag5','tag6')
    tags_description = (
             f'tag1 - Standard Color Tag - {settings["tags"]["tag1"]}', 
             f'tag2 - Red and Yellow Tag - {settings["tags"]["tag2"]}', 
             f'tag3 - Smooth Color Wave - {settings["tags"]["tag3"]}',
             f'tag4 - Blink Letter Wave - {settings["tags"]["tag4"]}',
             f'tag5 - Rainbow Tag - {settings["tags"]["tag5"]}'
    )
    
    avail_commands = {
        "/spaz": settings["cmds"]["/spaz"],
        "/spaz all": settings["cmds"]["/spaz all"],
        "/inv": settings["cmds"]["/inv"],
        "/inv all": settings["cmds"]["/inv all"],
        "/freeze": settings["cmds"]["/freeze"],
        "/freeze all": settings["cmds"]["/freeze all"],
        "/sleep": settings["cmds"]["/sleep"],
        "/sleep all": settings["cmds"]["/sleep all"],
        "/thaw": settings["cmds"]["/thaw"],
        "/thaw all": settings["cmds"]["/thaw all"],
        "/kill": settings["cmds"]["/kill"],
        "/kill all": settings["cmds"]["/kill all"],
        "/end": settings["cmds"]["/end"],
        "/curse": settings["cmds"]["/curse"],
        "/curse all": settings["cmds"]["/curse all"],
        "/tint": settings["cmds"]["/tint"],
        "/sm": settings["cmds"]["/sm"],
        "/heal": settings["cmds"]["/heal"],
        "/heal all": settings["cmds"]["/heal all"],
        "/shield": settings["cmds"]["/shield"],
        "/shield all": settings["cmds"]["/shield all"],
        "/punch": settings["cmds"]["/punch"],
        "/punch all": settings["cmds"]["/punch all"],
        "/gm": settings["cmds"]["/gm"]
    }
        
    #chatmessage(avail_commands)
    
    def effects_cash(effect_name):
        cash = {
            "spark": settings["effects"]["spark"],
            "sparkground": settings["effects"]["sparkground"],
            "sweat": settings["effects"]["sweat"],
            "sweatground": settings["effects"]["sweatground"],
            "distortion": settings["effects"]["distortion"],
            "rainbow": settings["effects"]["rainbow"],
            "ice": settings["effects"]["ice"],
            "iceground": settings["effects"]["iceground"],
            "slime": settings["effects"]["slime"],
            "metal": settings["effects"]["metal"],
            "splinter": settings["effects"]["splinter"],
            "fairydust": settings["effects"]["fairydust"],
            "star": settings["effects"]["star"],
            "newrainbow": settings["effects"]["newrainbow"],
            "footprint": settings["effects"]["footprint"],
            "fire": settings["effects"]["fire"],
            "firespark": settings["effects"]["firespark"]
        }
        if isinstance(effect_name, str):
            return cash.get(effect_name)
            
        elif isinstance(effect_name, (list, tuple)):
            return {e: cash.get(e) for e in effect_name}
            
    def tags_cash(tag_name): # configure tag price in fire.json
        cash = {
            'tag1': settings["tags"]["tag1"], #Standard Color Tag - 25
            'tag2':settings["tags"]["tag2"], #Red & Yellow Wave - 45
            'tag3': settings["tags"]["tag3"], #Smooth Color Wave - 40
            'tag4':settings["tags"]["tag4"], #Blink Letter Wave - 50
            'tag5': settings["tags"]["tag5"], #Rainbow Tag - 60
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
    ticket = babase.charstr(babase.SpecialChar.TICKET)
    #start
    if msg == '/shop effects':
        lines = [f"{dec:<15} {ticket}{price}" for dec, price in effects.items()]

        # pair into two columns
        pairs = []
        for i in range(0, len(lines), 2):
            left = lines[i]
            right = lines[i+1] if i+1 < len(lines) else ""
            pairs.append(f"{left}   |   {right}")

        # send 5 rows per message
        for i in range(0, len(pairs), 5):
            chatmessage("\n".join(pairs[i:i+5]), clients=[client_id], transient=True)
    elif msg == '/shop tags':
        lines = []

        for tag in tags_description:
            name, desc, price = tag.split(' - ')
            lines.append(f"{name:<6} - {desc:<22} - {ticket}{price}")

        chatmessage('\n'.join(lines), clients=[client_id], transient=True)
    elif msg == '/shop cmds':
        lines = [f"{cmd:<15} {ticket}{price}" for cmd, price in avail_commands.items()]

        # pair into two columns
        pairs = []
        for i in range(0, len(lines), 2):
            left = lines[i]
            right = lines[i+1] if i+1 < len(lines) else ""
            pairs.append(f"{left}   |   {right}")

        # send 5 rows per message
        for i in range(0, len(pairs), 5):
            chatmessage("\n".join(pairs[i:i+5]), clients=[client_id], transient=True)
    elif m == '/buy':
        if not a:
            chatmessage('use /shop', clients=[client_id], transient=True)
            return

        item = a[0]
        name = a[1] if len(a) > 1 else None

        # effect purchase
        if item in effects:
            if item in c_effects:
                chatmessage(f'You already have: {item}!', clients=[client_id], transient=True)
                return

            price = effects_cash(item)
            if user_cash >= price:
                coin.deductCoins(acc, price)
                if add_effect(acc, item):
                    save_to_py()
                chatmessage(f'Purchased Effect: {item}!', clients=[client_id], transient=True)
            else:
                chatmessage(f'Insufficient Funds! Need {ticket}{price - user_cash} more!', clients=[client_id], transient=True)

        # tag purchase
        elif item in tags:
            user_tags = customers.get(acc, {}).get("tags", {})
            
            if user_tags: # only allow client to have one tag at a time or clashing will occur between tags
                chatmessage('You already have a Tag!', clients=[client_id], transient=True)
                return
                
            if acc in mid.name:
                chatmessage('You already have Custom tag!', clients=[client_id], transient=True)
                return

            price = tags_cash(item)
            if user_cash >= price:
                if len(a) > 1: # what to do if client wants to buy tag but havent defined tag name!
                    coin.deductCoins(acc, price)
                    tag = " ".join(a[1:])
                    tag = parse_icons(tag)
                    if add_tag(acc, item,tag_name=tag):
                        save_to_py()
                    chatmessage(f'Purchased Tag: {item}!', clients=[client_id], transient=True)
                else:
                    chatmessage('Specify Tag Name as well!', clients=[client_id], transient=True)
            else:
                chatmessage(f'Insufficient Funds! Need {ticket}{price - user_cash} more!', clients=[client_id], transient=True)

        else:
            chatmessage('Item not available! Use /shop instead!', clients=[client_id], transient=True)