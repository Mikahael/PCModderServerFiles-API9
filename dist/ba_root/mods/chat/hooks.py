import babase
import bascenev1 as ba
from bascenev1 import get_foreground_host_session, get_foreground_host_activity, get_game_roster
import bascenev1 as ba
import bascenev1lib
import random
from spaz import member_id as mem
from typing import Sequence



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
            elif m == password+'admin':
                if self.checkOwner(nick):
                    if a == []:
                        ba.broadcastmessage('Use: /admin ID add')
                    else:
                        try:
                            clID = int(a[0])
                            updated_admins=[]
                            updated_admins=mem.admin
                            for i in session_players:
                                if i.inputdevice.client_id==clID:
                                    newadmin = i.get_v1_account_id(True)   
                                    real = i.getname()
                                if a[1] == 'add':
                                    if newadmin in mem.admin:
                                        ba.broadcastmessage(newadmin+' already in the hashes!', clients=[client_id], transient=True)
                                    else:
                                        updated_admins.append(newadmin)
                                        with open('ba_data/python/bascenev1lib/actor'+ "/logged_id.py",'a') as fi:
                                            fi.write(real +' || '+newadmin +'\n')
                                            fi.close()
                                elif a[1] == 'remove':
                                    if newadmin in mem.admin:
                                        updated_admins.remove(newadmin)
                                    else:
                                        ba.broadcastmessage(newadmin+' not in the hashes!', clients=[client_id], transient=True)
                            if True:
                                with open('ba_root/mods/spaz'+ "/member_id.py") as file:
                                    s = [row for row in file]
                                    s[4] = 'admin = '+ str(updated_admins)+ '\n'
                                    f = open('ba_root/mods/spaz'+ "/member_id.py",'w')
                                    for i in s:
                                        f.write(i)
                                    f.close()
                            else:
                                pass
                        except Exception:
                            ba.broadcastmessage('Player not found!')
            elif m == password+'name':
                if self.checkOwner(nick):
                    if a == []:
                        ba.broadcastmessage('Use /name 113 TAG, to remove use /name 113 real')
                    else:
                        try:
                            clID = int(a[0])
                            name = (a[1])
                            updated_admins=[]
                            updated_admins=mem.name
                            for i in session_players:
                                if i.inputdevice.client_id==clID:
                                    newadmin = i.get_v1_account_id(True)   
                                    real = i.getname()
                            if True:
                                if a[1] == 'real':#for actual name
                                    if newadmin in updated_admins:
                                        updated_admins.pop(newadmin)
                                else:#for the nickname
                                    mem.name[newadmin] = name
                                with open('ba_root/mods/spaz'+ "/member_id.py") as file:
                                    s = [row for row in file]
                                    s[8] = 'name = '+ str(updated_admins)+ '\n'
                                    f = open('ba_root/mods/spaz'+ "/member_id.py",'w')
                                    for i in s:
                                        f.write(i)
                                    f.close()
                            else:
                                pass
                        except Exception:
                            ba.broadcastmessage('Player not found!')

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
            elif m == password+'pwp':
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
  
c = cheat_options()
def cmnd(msg,client_id):
    if ba.get_foreground_host_activity() is not None:
        c.opt(client_id,msg)