server files by pcmodder - something simple and different from existings systems
runs on 1.7.63
may be buggy, rushed near the end, easy to fix errors..
do pull requests if yall wanna improve

features - 
1. powerup system ---> 1.4 to 1.7
2. chat system
3. improved chat filter with mute system
4. question answer with powerful shop system, dailycash feature
5. autonight and snowy maps
6. textonmap with tipstext and datetime text
7. anti-betray system and botspawn added
8. removed cooldown for owners - rejoin part
9. unlock all chars - bslobby mod
10. anti-afk mod added - 30s then removed, whitelist added
11. default playlist edited for teams - edit in maps folder - playlist.py
12. added endvote system
13. added master logging to all players - inside party and in gameplay
14. all configurations transitioned from py to .json in config folder
15. all logs added in logs folder

configurations - 

1. edit fire.json to change tipstext, maptext, shop prices and coinsystem configurations
2. go to config folder to change configurations for spaz, powerupbox, bombmodel according to the .json file
3. to add owner or admin/mod, go to spaz folder and edit member_id.py
4. dont edit config_cache.py and stats_master.py in config folder - else big errors
5. for datetime mod, change timezone of server to ur location ---> sudo timedatectl set-timezone Asia/Kolkata

installation - 

1. download server files from github - git clone https://github.com/Mikahael/PCModderServerFiles-API9.git
2. cd folder_name
3. install python3.13-dev via whatever method u want
4. chmod 777 bombsquad_server dist/bombsquad_headless
5. pkill -f tmux
6. tmux
7. ./bombsquad_server

thanks - 

to whom so ever it may concern, all rights reserved to pcmodder, as the license states
thanks to vortex, paradise, anashd(tunisialoveratd)
all thanks to god
