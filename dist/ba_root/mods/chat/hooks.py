import babase
import bascenev1 as ba
from bascenev1 import get_foreground_host_session, get_foreground_host_activity, get_game_roster
import bascenev1 as ba
import bascenev1lib
from spaz import newspaz
import random
from spaz import member_id as mem
import datetime
from typing import Sequence
from config import powerup_config as pwp
from config import bomb_config as bmb
from config import spaz_config as spz


class cheat_options(object):
    def __init__(self):
        self.all = True # just in case
        self.tint = None # needs for /nv
        
    def checkAdmin(self,client_id):
        session = get_foreground_host_session()
        session_players=session.sessionplayers
        for i in session_players:
            if i.inputdevice.client_id==client_id:
                acc = i.get_v1_account_id(True)
            
        if acc in mem.admin or acc in mem.owner:
            ba.broadcastmessage('Command Accepted Sir!', clients=[client_id], transient=True)
            return True
        else:
            ba.broadcastmessage('Command Denied', clients=[client_id], transient=True)
            return False
        
    def checkOwner(self,client_id):
        session = get_foreground_host_session()
        session_players=session.sessionplayers
        for i in session_players:
            if i.inputdevice.client_id==client_id:
                acc = i.get_v1_account_id(True)
            
        if acc in mem.owner:
            ba.broadcastmessage('Command Accepted Owner Sir!', clients=[client_id], transient=True)
            return True
        else:
            ba.broadcastmessage('Command Denied', clients=[client_id], transient=True)
            return False
            
    def _now():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
    def opt(self,client_id,msg):
        nick=client_id
        if True:
          m = msg.split(' ')[0] # command
          a = msg.split(' ')[1:] # arguments
          #
          password = '/'
          #
          session = get_foreground_host_session()
          session_players=session.sessionplayers
          activity = get_foreground_host_activity()
          activity_players=activity.players
          roster = get_game_roster()
          with ba.get_foreground_host_activity().context:
            if m == '/hi':
                    ba.broadcastmessage('helloo!')
            elif m == password+'me':
                if a == []:
                    ba.broadcastmessage('Use /me client_id')
                else:
                    clID = int(a[0])
                    for i in session_players:
                        if i.inputdevice.client_id==clID:
                            acc = i.get_v1_account_id()
                            login = mem.times_joined.count(acc)
                            name = i.getname()
                    if int(a[0]) == clID:
                        try:
                            ba.broadcastmessage(name+' ---> '+acc+' ---> '+str(session_players.index(i))+' --->  client_id ---> '+str(clID))
                            if acc in mem.admin:
                                ba.broadcastmessage('Roles: Admin / Times Joined: '+str(login))
                            elif acc in mem.owner:
                                ba.broadcastmessage('Roles: Owner / Times Joined: '+str(login))
                            else:
                                ba.broadcastmessage('Roles: None / Times Joined: '+str(login))
                        except Exception:
                            ba.broadcastmessage('Player not Found!')
                    else:
                        ba.broadcastmessage('Player Not Found!')
            elif m == password+'list2':
                ba.broadcastmessage('======= List ======')
                for i in session_players:
                    ba.broadcastmessage(i.getname()+' - | -  '+str(session_players.index(i))+'\n')
                if not roster == []:
                    for i in roster:
                        ba.broadcastmessage('======For /kick only======')
                    ba.broadcastmessage(str(i['players'][0]['nam_full'])+'   -   '+str(i['client_id']))
            elif m == password+'list':
                    #string = u'==Name========ClientID====PlayerID==\n'
                    string = u"{0:^16}{1:^15}{2:^10}\n------------------------------------------------------------------------------\n".format('Name','ClientID','PlayerID')
                    lname = None
                    lcid = None
                    lpid = None
                    for i in ba.get_game_roster():
                        if i['players'] == []:
                            lname = str(i['display_string'])
                            lcid = str(i['client_id'])
                            lpid = str('In Lobby')
                            string += u"{0:^16}{1:^15}{2:^10}\n".format(lname, lcid, lpid)
                        else:
                            for lp in i['players']:
                                lname = lp['name_full']
                                lcid = i['client_id']
                                lpid = lp['id']
                                string += u"{0:^16}{1:^15}{2:^10}\n".format(lname, lcid, lpid)
                    ba.broadcastmessage(string)
                    
            elif m == password+'fly':
                if a == []:
                    ba.broadcastmessage('Use /fly index or /fly all')
                elif a[0] == 'all':
                    for i in activity_players:
                        if not i.actor.node.fly == True:
                            i.actor.node.fly = True
                        else:
                            i.actor.node.fly = False
                else:
                    try:
                        if not activity_players[int(a[0])].actor.node.fly == True:
                            activity_players[int(a[0])].actor.node.fly = True
                        else:
                            activity_players[int(a[0])].actor.node.fly = False
                    except:
                        ba.broadcastmessage('Player not Found')
                        pass
                        
            elif m == password+'hug':
                    if a == []:
                        ba.broadcastmessage('Using: /hug all or number of list')
                    else:
                        try:
                            if a[0] == 'all': # not working?
                                if self.checkAdmin(nick):
                                    try:
                                        activity_players[0].actor.node.hold_node = activity_players[1].actor.node
                                    except:
                                        pass
                                    try:
                                        activity_players[1].actor.node.hold_node = activity_players[0].actor.node
                                    except:
                                        pass
                                    try:
                                        activity_players[2].actor.node.hold_node = activity_players[3].actor.node
                                    except:
                                        pass
                                    try:
                                        activity_players[3].actor.node.hold_node = activity_players[2].actor.node
                                    except:
                                        pass
                                    try:
                                        activity_players[4].actor.node.hold_node = activity_players[5].actor.node
                                    except:
                                        pass
                                    try:
                                        activity_players[5].actor.node.hold_node = activity_players[4].actor.node
                                    except:
                                        pass
                                    try:
                                        activity_players[6].actor.node.hold_node = activity_players[7].actor.node
                                    except:
                                        pass
                                    try:
                                        activity_players[7].actor.node.hold_node = activity_players[6].actor.node
                                    except:
                                        pass
                            else:
                                activity_players[int(a[0])].actor.node.hold_node = activity_players[int(a[1])].actor.node
                        except:
                            pass
            elif m == password+'freeze':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /freeze all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.handlemessage(ba.FreezeMessage())
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage(ba.FreezeMessage())
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'kick':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage("Using: /kick [name/ClientID]")
                    else:
                        try:
                            #import _bascenev1
                            clID = int(a[0])
                            for i in session_players:
                                if i.inputdevice.client_id==clID:
                                    acc = i.get_v1_account_id()
                            if acc in mem.owner:
                                ba.broadcastmessage('Not allowed to kick Owner!')
                            else:
                                ba.disconnect_client(int(a[0]))
                        except Exception:
                            ba.broadcastmessage('Player Not Found')                                
            elif m == password+'quit':#fixme
                if self.checkAdmin(nick):
                    babase.quit()
            elif m == password + 'admin':
                #
                if not self.checkOwner(nick):
                    return

                if len(a) < 2:
                    ba.broadcastmessage(
                        'Use: /admin <ID> <add|remove>',
                        clients=[client_id],
                        transient=True
                    )
                    return

                try:
                    clID = int(a[0])
                    action = a[1].lower()
                except ValueError:
                    ba.broadcastmessage(
                        'Invalid client ID.',
                        clients=[client_id],
                        transient=True
                    )
                    return

                target_player = None
                for i in session_players:
                    if i.inputdevice.client_id == clID:
                        target_player = i
                        break

                if target_player is None:
                    ba.broadcastmessage(
                        'Player not found!',
                        clients=[client_id],
                        transient=True
                    )
                    return

                newadmin = target_player.get_v1_account_id(True)
                real = target_player.getname()
                role = m
                #actor = nick
                for i in session_players:
                    if i.inputdevice.client_id==nick:
                        actor = i.get_v1_account_id()

                updated_admins = list(mem.admin)

                log_path = 'ba_root/mods/chat/logged_id.txt'
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # ---------------- ADD ----------------
                if action == 'add':
                    if newadmin in updated_admins:
                        ba.broadcastmessage(
                            real + ' is already an admin!',
                            clients=[client_id],
                            transient=True
                        )
                        return

                    updated_admins.append(newadmin)

                    with open(log_path, 'a') as fi:
                        fi.write(
                            f"[{time}] ADDED | "
                            f"Role: {role} | "
                            f"Name: {real} | "
                            f"PBID: {newadmin} | "
                            f"By: {actor}\n"
                        )

                    ba.broadcastmessage(
                        real + ' added as admin.',
                        transient=True
                    )

                # ---------------- REMOVE ----------------
                elif action == 'remove':
                    if newadmin not in updated_admins:
                        ba.broadcastmessage(
                            real + ' is not an admin!',
                            clients=[client_id],
                            transient=True
                        )
                        return

                    updated_admins.remove(newadmin)

                    with open(log_path, 'a') as fi:
                        fi.write(
                            f"[{time}] REMOVED | "
                            f"Role: {role} | "
                            f"Name: {real} | "
                            f"PBID: {newadmin} | "
                            f"By: {actor}\n"
                        )

                    ba.broadcastmessage(
                        real + ' removed from admins.',
                        transient=True
                    )

                else:
                    ba.broadcastmessage(
                        'Use: /admin <ID> <add|remove>',
                        clients=[client_id],
                        transient=True
                    )
                    return

                # -------- WRITE BACK ADMIN LIST --------
                with open('ba_root/mods/spaz/member_id.py') as file:
                    s = [row for row in file]

                s[4] = 'admin = ' + str(updated_admins) + '\n'

                with open('ba_root/mods/spaz/member_id.py', 'w') as f:
                    for line in s:
                        f.write(line)

                mem.admin = updated_admins

            elif m == password + 'name':
                if not self.checkOwner(nick):
                    return

                if len(a) < 2:
                    ba.broadcastmessage(
                        'Use: /name <ID> <TAG | real>',
                        clients=[client_id],
                        transient=True
                    )
                    return

                try:
                    clID = int(a[0])
                    tag = a[1]
                except ValueError:
                    ba.broadcastmessage(
                        'Invalid client ID.',
                        clients=[client_id],
                        transient=True
                    )
                    return

                target_player = None
                for i in session_players:
                    if i.inputdevice.client_id == clID:
                        target_player = i
                        break

                if target_player is None:
                    ba.broadcastmessage(
                        'Player not found!',
                        clients=[client_id],
                        transient=True
                    )
                    return

                pbid = target_player.get_v1_account_id(True)
                real_name = target_player.getname()
                for i in session_players:
                    if i.inputdevice.client_id==nick:
                        actor = i.get_v1_account_id()
                        
                log_path = 'ba_root/mods/chat/logged_id.txt'
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                updated_names = dict(mem.name)  # COPY

                # -------- RESET TO REAL NAME --------
                if tag.lower() == 'real':
                    if pbid in updated_names:
                        del updated_names[pbid]
                        ba.broadcastmessage(
                            real_name + '\'s name reset.',
                            transient=True
                        )
      
                        with open(log_path, 'a') as fi:
                            fi.write(
                                f"[{time}] NAME REMOVED | "
                                #f"Role: {role} | "
                                f"Name: {real_name} | "
                                #f"PBID: {newadmin} | "
                                f"By: {actor}\n"
                            )
                        
                    else:
                        ba.broadcastmessage(
                            real_name + ' has no custom name.',
                            clients=[client_id],
                            transient=True
                        )
                        return

                # -------- SET CUSTOM NAME --------
                else:
                    updated_names[pbid] = tag
                    ba.broadcastmessage(
                        real_name + ' renamed to ' + tag,
                        transient=True
                    )
                    
                    with open(log_path, 'a') as fi:
                            fi.write(
                                f"[{time}] NAME ADDED | "
                                #f"Role: {role} | "
                                f"Name: {tag} | "
                                #f"PBID: {newadmin} | "
                                f"By: {actor}\n"
                            )
                        

                # -------- WRITE BACK TO FILE --------
                with open('ba_root/mods/spaz/member_id.py') as file:
                    s = [row for row in file]

                s[8] = 'name = ' + str(updated_names) + '\n'

                with open('ba_root/mods/spaz/member_id.py', 'w') as f:
                    for line in s:
                        f.write(line)

                mem.name = updated_names

            elif m == password+'bomb':
                if self.checkOwner(nick):
                    clID = int(a[0])
                    bomb = (a[1])
                    updated_admins=[]
                    updated_admins=mem.bomb_limit
                    for i in session_players:
                        newadmin = i.get_v1_account_id(True)   
                        reg = 'normal'
                    bomb_type = ['normal','ice','sticky','impact']
                    if a[1] in bomb_type:
                        if a[1] == 'normal':
                            mem.bomb_limit[newadmin] = reg
                        else:
                            mem.bomb_limit[newadmin] = bomb
                        with open('ba_root/mods/spaz'+ "/member_id.py") as file:
                            s = [row for row in file]
                            s[9] = 'bomb_limit = '+ str(updated_admins)+ '\n'
                            f = open('ba_root/mods/spaz'+ "/member_id.py",'w')
                            for i in s:
                                f.write(i)
                            f.close()
                    else:
                        ba.broadcastmessage('Available Bombtypes: normal, ice, sticky, impact')
                        
            elif m == password+'thaw':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /thaw all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.handlemessage(ba.ThawMessage())
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage(ba.ThawMessage())
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'kill':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /kill all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.handlemessage(ba.DieMessage())
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage(ba.DieMessage())
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'curse':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /curse all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.handlemessage(ba.PowerupMessage(poweruptype='curse'))
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage(ba.PowerupMessage(poweruptype='curse'))
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'headless':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /headless all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.head_mesh = None
                                        i.actor.node.style = "cyborg"
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.head_mesh = None
                                activity_players[int(a[0])].actor.node.style = "cyborg"
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'shield':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /shield all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.handlemessage(ba.PowerupMessage(poweruptype='shield'))
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage(ba.PowerupMessage(poweruptype='shield'))
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'celebrate':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /celebrate all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.handlemessage(ba.CelebrateMessage())
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage(ba.CelebrateMessage())
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'remove':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /remove all or number of list')
                    else:
                        if a[0]=='all':
                            for i in session_players:
                                try:
                                    i.remove_from_game()
                                except Exception:
                                    pass
                        else:
                            try:
                                session_players[int(a[0])].remove_from_game()
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'end':
                if self.checkAdmin(nick):
                    try:
                        activity.end_game()
                    except Exception:
                        pass
            elif m == password+'gm':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /gm all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.hockey = True
                                        i.actor.node.invincible = True
                                        i.actor._punch_power_scale = 5
                                except Exception:
                                    pass                    
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.hockey = True
                                activity_players[int(a[0])].actor.node.invincible = True
                                activity_players[int(a[0])].actor._punch_power_scale = 5
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'gmno':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /gm all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.hockey = False
                                        i.actor.node.invincible = False
                                        i.actor._punch_power_scale = 0.75
                                except Exception:
                                    pass                    
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.hockey = False
                                activity_players[int(a[0])].actor.node.invincible = False
                                activity_players[int(a[0])].actor._punch_power_scale = 0.75
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'tint':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /tint RBG or /tint r brightspeed')
                    else:
                        if a[0]=='not_avail':
                            m = 1.3 if a[1] is None else float(a[1])
                            s = 1000 if a[2] is None else float(a[2])
                            ba.animate_array(activity.globalsnode, 'tint',3, {0: (1*m,0,0), s: (0,1*m,0),s*2:(1,1,1*m),s*3:(1*m,0,0)},True)
                        else:
                            try:
                                if a[1] is not None:
                                    activity.globalsnode.tint = (float(a[0]),float(a[1]),float(a[2]))
                                else:
                                    ba.broadcastmessage('Error!')
                            except Exception:
                                ba.broadcastmessage('Error')
            elif m == password+'sm':
                if self.checkAdmin(nick):
                    if activity.globalsnode.slow_motion == True:
                        activity.globalsnode.slow_motion=False
                    else:
                        activity.globalsnode.slow_motion=True

            elif m == password+'icy':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use your id, then targets')
                    else:
                        activity_players[int(a[0])].actor.node = activity_players[int(a[1])].actor.node
            elif m == password+'inv':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /celebrate all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.head_mesh = None
                                        i.actor.node.torso_mesh = None
                                        i.actor.node.upper_arm_mesh = None
                                        i.actor.node.forearm_mesh = None
                                        i.actor.node.pelvis_mesh = None
                                        i.actor.node.hand_mesh = None
                                        i.actor.node.toes_mesh = None
                                        i.actor.node.upper_leg_mesh = None
                                        i.actor.node.lower_leg_mesh = None
                                        i.actor.node.style = "cyborg"
                                        i.actor.node.name = ' '
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.head_mesh = None
                                activity_players[int(a[0])].actor.node.torso_mesh = None
                                activity_players[int(a[0])].actor.node.upper_arm_mesh = None
                                activity_players[int(a[0])].actor.node.forearm_mesh = None
                                activity_players[int(a[0])].actor.node.pelvis_mesh = None
                                activity_players[int(a[0])].actor.node.hand_mesh = None
                                activity_players[int(a[0])].actor.node.toes_mesh = None
                                activity_players[int(a[0])].actor.node.upper_leg_mesh = None
                                activity_players[int(a[0])].actor.node.lower_leg_mesh = None
                                activity_players[int(a[0])].actor.node.style = "cyborg"
                                activity_players[int(a[0])].actor.node.name = ' '
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'floor':
                if self.checkAdmin(nick):
                    activity.globalsnode.floor_reflection = activity.globalsnode.floor_reflection == False
            elif m == password+'ac':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /ac RBG or /ac r')
                    else:
                        if a[0] == 'rnotavail':
                            m = 1.3 if a[1] is None else float(a[1])
                            s = 1000 if a[2] is None else float(a[2])
                            ba.animate_array(activity.globalsnode, 'ambient_color',3, {0: (1*m,0,0), s: (0,1*m,0),s*2:(1,1,1*m),s*3:(1*m,0,0)},True)
                        else:
                            try:
                                if a[1] is not None:
                                    activity.globalsnode.ambient_color = (float(a[0]),float(a[1]),float(a[2]))
                                else:
                                    ba.broadcastmessage('Error!')
                            except Exception:
                                ba.broadcastmessage('Error!')
            elif m == password+'heal':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /heal all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.handlemessage(ba.PowerupMessage(poweruptype='health'))
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage(ba.PowerupMessage(poweruptype='health'))
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'punch':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /punch all or number of list')
                    else:
                        if a[0]=='all':
                            for i in activity_players:
                                try:
                                    if i.actor.is_alive():
                                        i.actor.node.handlemessage(ba.PowerupMessage(poweruptype='punch'))
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage(ba.PowerupMessage(poweruptype='punch'))
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'sleep':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /sleep all of number of list')
                    else:
                        if a[0] == 'all':
                            for i in activity_players:
                                try:
                                    i.actor.node.handlemessage('knockout', 5000)
                                except Exception:
                                    pass
                        else:
                            try:
                                activity_players[int(a[0])].actor.node.handlemessage('knockout', 5000)
                            except Exception:
                                ba.broadcastmessage('Player not found!')
            elif m == password+'spaz':#fix
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /spaz all or number of list')
                    else:
                        if a[0]=='all':
                            if a[1] in ['ali','agent','bunny','cyborg','pixie','wizard','bones','zoe','santa','bear','ninja','frosty','kronk','penguin']:
                                for i in activity_players:
                                    try:
                                        i.actor.node.handlemessage(ba.PowerupMessage(poweruptype=a[1]))
                                    except:
                                        pass
                            else:
                                a = ('ali','agent','bunny','cyborg','pixie','kronk','bear','penguin')
                                b = ( 'ninja','frosty','wizard','bones','zoe','santa')
                                ba.broadcastmessage('Use these: '+str(a+b))
                        else:
                            if a[1] in ['ali','agent','bunny','cyborg','pixie','wizard','bones','zoe','santa','bear','ninja','frosty','kronk','penguin']:
                                try:
                                    activity_players[int(a[0])].actor.node.handlemessage(ba.PowerupMessage(poweruptype=a[1]))
                                except Exception:
                                    pass
                            else:
                                a = ('ali','agent','bunny','cyborg','pixie','kronk','bear','penguin')
                                b = ( 'ninja','frosty','wizard','bones','zoe','santa')
                                ba.broadcastmessage('Use these: '+str(a+b))
            elif m == password+'pwp2323':
                if self.checkAdmin(nick):
                    if a == []:
                        ba.broadcastmessage('Use /pwp all (pwp) or /pwp number (pwp)')
                    else:
                        if a[0] == 'sticky':
                            try:
                                ba.broadcastmessage(a[0]+' changed to --> '+a[1]+' change in next round!')
                                powerup_dist(line = 9, pwp_name = 'sticky_bombs', number = a[1])
                                dist.sticky_bombs = a[1]
                            except Exception:
                                ba.broadcastmessage('Error, powerup not changed!')
                        elif a[0] == 'punch':
                            try:
                                ba.broadcastmessage(a[0]+' changed to --> '+a[1]+' change in next round!')
                                powerup_dist(line = 6, pwp_name = 'punch', number = a[1])
                                dist.punch = a[1]
                            except Exception:
                                ba.broadcastmessage('Error, powerup not changed!')
                        elif a[0] == 'curse':
                            try:
                                ba.broadcastmessage(a[0]+' changed to --> '+a[1]+' change in next round!')
                                powerup_dist(line = 12, pwp_name = 'curse', number = a[1])
                                dist.curse = a[1]
                            except Exception:
                                ba.broadcastmessage('Error, powerup not changed!')
                        elif a[0] == 'health':
                            try:
                                ba.broadcastmessage(a[0]+' changed to --> '+a[1]+' change in next round!')
                                powerup_dist(line = 11, pwp_name = 'health', number = a[1])
                                dist.health = a[1]
                            except Exception:
                                ba.broadcastmessage('Error, powerup not changed!')
                        elif a[0] == 'ice':
                            try:
                                ba.broadcastmessage(a[0]+' changed to --> '+a[1]+' change in next round!')
                                powerup_dist(line = 5, pwp_name = 'ice_bombs', number = a[1])
                                dist.ice_bombs = a[1]
                            except Exception:
                                ba.broadcastmessage('Error, powerup not changed!')
                        elif a[0] == 'impact':
                            try:
                                ba.broadcastmessage(a[0]+' changed to --> '+a[1]+' change in next round!')
                                powerup_dist(line = 7, pwp_name = 'impact_bombs', number = a[1])
                                dist.impact_bombs = a[1]
                            except Exception:
                                ba.broadcastmessage('Error, powerup not changed!')
                        elif a[0] == 'shield':
                            try:
                                ba.broadcastmessage(a[0]+' changed to --> '+a[1]+' change in next round!')
                                powerup_dist(line = 10, pwp_name = 'shield', number = a[1])
                                dist.shield = a[1]
                            except Exception:
                                ba.broadcastmessage('Error, powerup not changed!')
                        else:
                            ba.broadcastmessage('Default Pwp only: punch, shield, health, sticky, ice, impact')
            elif m == password+'info':
                ba.broadcastmessage('Server fully modded by PCMODDER or PC||231392')
                ba.broadcastmessage('Special thanks to Pranav and Smoooth!')
            elif m == password+'rules':
                ba.broadcastmessage('Respect is Key here and use ethical manners for speech')
                ba.broadcastmessage('All rights to PCMODDER!')
            elif m == password+'contact':
                ba.broadcastmessage('Contact PCMODDER at StormX or StormSquad')
                ba.broadcastmessage('All rights to PCMODDER!')
                
            elif m == password+'powerupconfig':
                ba.broadcastmessage('powerupname, poweruptimer, poweruplight, powerupshield, powerupflash, powerupbox')
                ba.broadcastmessage('All rights to PCMODDER!')
                
            elif m == password+'spazconfig':
                ba.broadcastmessage('spazglove, spazshield, spazcolor, spazchar, char')
                ba.broadcastmessage('All rights to PCMODDER!')
                
            elif m == password+'bombconfig':
                ba.broadcastmessage('bombname, bombtimer, bomblight, bombshield, bombspike, bombmodel')
                ba.broadcastmessage('All rights to PCMODDER!')
            elif m == password+'config':
                ba.broadcastmessage('bombconfig, powerupconfig, spazconfig')
                ba.broadcastmessage('All rights to PCMODDER!')
                
            elif m == password+'powerupname':
                if self.checkAdmin(nick):
                    if pwp.text == True:
                        pwp.text = False
                    else:
                        pwp.text = True
                    k = pwp.text
                    ba.broadcastmessage('Powerup name turned ---> '+str(k))    
            elif m == password+'poweruptimer':
                if self.checkAdmin(nick):
                    if pwp.expire_text == True:
                        pwp.expire_text = False
                    else:
                        pwp.expire_text = True
                    k = pwp.expire_text
                    ba.broadcastmessage('Powerup timer turned ---> '+str(k))    
            elif m == password+'powerupshield':
                if self.checkAdmin(nick):
                    if pwp.shield == True:
                        pwp.shield = False
                    else:
                        pwp.shield = True
                    k = pwp.shield
                    ba.broadcastmessage('Powerup shield turned ---> '+str(k))   
            elif m == password+'poweruplight':
                if self.checkAdmin(nick):
                    if pwp.light == True:
                        pwp.light = False
                    else:
                        pwp.light = True
                    k = pwp.light
                    ba.broadcastmessage('Powerup light turned ---> '+str(k))   
            elif m == password+'powerupflash':
                if self.checkAdmin(nick):
                    if pwp.flash == True:
                        pwp.flash = False
                    else:
                        pwp.flash = True
                    k = pwp.flash
                    ba.broadcastmessage('Powerup flash turned ---> '+str(k))   
            elif m == password+'powerupbox':
                if self.checkAdmin(nick):
                    if pwp.accept_powerup == True:
                        pwp.accept_powerup = False
                    else:
                        pwp.accept_powerup = True
                    k = pwp.accept_powerup
                    ba.broadcastmessage('Powerup box turned ---> '+str(k)) 
            elif m == password+'bombname':
                if self.checkAdmin(nick):
                    if bmb.bomb_name == True:
                        bmb.bomb_name = False
                    else:
                        bmb.bomb_name = True
                    k = bmb.bomb_name
                    ba.broadcastmessage('Bomb name turned ---> '+str(k)) 
            elif m == password+'bombshield':
                if self.checkAdmin(nick):
                    if bmb.shield == True:
                        bmb.shield = False
                    else:
                        bmb.shield = True
                    k = bmb.shield
                    ba.broadcastmessage('Bomb shield turned ---> '+str(k)) 
            elif m == password+'bomblight':
                if self.checkAdmin(nick):
                    if bmb.light == True:
                        bmb.light = False
                    else:
                        bmb.light = True
                    k = bmb.light
                    ba.broadcastmessage('Bomb light turned ---> '+str(k)) 
            elif m == password+'bombmodel':
                if self.checkAdmin(nick):
                    if bmb.bomb_model == True:
                        bmb.bomb_model = False
                    else:
                        bmb.bomb_model = True
                    k = bmb.bomb_model
                    ba.broadcastmessage('Bomb model turned ---> '+str(k)) 
            elif m == password+'bombspike':
                if self.checkAdmin(nick):
                    if bmb.spike_model == True:
                        bmb.spike_model = False
                    else:
                        bmb.spike_model = True
                    k = bmb.spike_model
                    ba.broadcastmessage('Bomb spike turned ---> '+str(k)) 
            elif m == password+'bombtimer':
                if self.checkAdmin(nick):
                    if bmb.bomb_expire == True:
                        bmb.bomb_expire = False
                    else:
                        bmb.bomb_expire = True
                    k = bmb.bomb_expire
                    ba.broadcastmessage('Bomb timer turned ---> '+str(k))

            elif m == password+'spazglove':
                if self.checkAdmin(nick):
                    if spz.gloves == True:
                        spz.gloves = False
                    else:
                        spz.gloves = True
                    k = spz.gloves
                    ba.broadcastmessage('Spaz gloves turned ---> '+str(k))
            elif m == password+'spazshield':
                if self.checkAdmin(nick):
                    if spz.shield == True:
                        spz.shield = False
                    else:
                        spz.shield = True
                    k = spz.shield
                    ba.broadcastmessage('Spaz shield turned ---> '+str(k))
            elif m == password+'spazcolor':
                if self.checkAdmin(nick):
                    if spz.spaz_color == True:
                        spz.spaz_color = False
                    else:
                        spz.spaz_color = True
                    k = spz.spaz_color
                    ba.broadcastmessage('Spaz color turned ---> '+str(k))
            elif m == password+'spazchar':
                if self.checkAdmin(nick):
                    if spz.spaz_char == True:
                        spz.spaz_char = False
                    else:
                        spz.spaz_char = True
                    k = spz.spaz_char
                    ba.broadcastmessage('Spaz char turned ---> '+str(k))
            
            elif m == password + 'char':
                if not self.checkAdmin(nick):
                    return

                if not a:
                    ba.broadcastmessage(
                        'Use: /char <character>',
                        clients=[client_id],
                        transient=True
                    )
                    return

                chars = ['ninja', 'frosty', 'wizard', 'ali', 'pengu', 'pixie', 'santa']# dont use robot.. buggy
                char = a[0].lower()

                if char not in chars:
                    ba.broadcastmessage(
                        f'Invalid character! - try {chars}',
                        clients=[client_id],
                        transient=True
                    )
                    return

                # make sure all attrs exist
                for c in chars:
                    if not hasattr(spz, c):
                        setattr(spz, c, False)

                # toggle logic
                currently_on = getattr(spz, char)

                if currently_on:
                    # turn OFF current char
                    setattr(spz, char, False)
                    ba.broadcastmessage(
                        f'Spaz {char} turned ---> False',
                        transient=True
                    )
                else:
                    # turn OFF all others
                    for c in chars:
                        setattr(spz, c, False)

                    # turn ON selected
                    setattr(spz, char, True)
                    ba.broadcastmessage(
                        f'Spaz {char} turned ---> True',
                        transient=True
                    )
 
c = cheat_options()
def cmnd(msg,client_id):
    if ba.get_foreground_host_activity() is not None:
        c.opt(client_id,msg)