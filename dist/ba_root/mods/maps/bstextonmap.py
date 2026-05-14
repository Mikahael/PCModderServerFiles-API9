# bstextonmap.py
from __future__ import annotations
import random
import bascenev1 as bs
from bascenev1 import _map
import fire
from bascenev1lib.gameutils import SharedObjects

endvote_node = None

# Save original Map.__init__ to call it safely

_original_map_init = _map.Map.__init__

def _map_custom_init(self, *args, **kwargs):
    """Custom Map init to add text on map."""
    
    global endvote_node
    
    # Call the original __init__ safely
    
    _original_map_init(self, *args, **kwargs)
    
    #for endvote mod
    endvote_node = bs.newnode(
        'text',
        attrs={
            'text': '',
            'scale': 0.85,
            'position': (500, -120),
            'maxwidth': 500,
            'flatness': 0.0,
            'shadow': 0.5,
            'h_align': 'center',
            'v_align': 'center',
            'v_attach': 'top',
            'color': (1, 1, 1)
        }
    )

    

    def soby():
                # Pick a random message
                messages = [
                        u'\ue048Welcome to the server by PCModder\ue048',
                        u'\ue00cServer version is 1.7.59\ue00c',
                        u'\ue00cA day without laughter is a day wasted\ue00c',
                        u'\ue043Her smile, the promise of heaven itself\ue043',
                        u'\ue043Aspire to inspire before you expire\ue043',
                        u'\ue048Go out with memories, not dreams\ue048'
                ]
                msg = random.choice(messages)

                # Create text node
                node = bs.newnode(
                        'text',
                        attrs={
                                'text': msg,
                                'scale': 0.0,
                                'position': (0, 100),
                                'maxwidth': 700,
                                'flatness': 0.0,
                                'shadow': 0.5,
                                'h_align': 'center',
                                'v_align': 'center',
                                'v_attach': 'bottom',
                                'color': (1, 1, 1),
                                'opacity': 1.0})

                # Bounce-in animation
                bs.animate( node,'scale',{
                         0.0: 0.0,
                         0.25: 0.7,
                         0.45: 1.35,
                         0.6: 1.6,})
                # Fade out
                bs.animate(node,'opacity',{7.0: 1.0, 9.5: 0.0,})
                bs.timer(10.0, node.delete)

        # Show message every 15 seconds
    bs.timer(15, soby, repeat=True)

    # for the time module!    
    self.time_node = bs.newnode('text',
                attrs={
                    'text': '',
                    'scale': 0.85,
                    'position': (500, -80),
                    'maxwidth': 500,
                    'flatness': 0.0,
                    'shadow': 0.5,
                    'h_align': 'center',
                    'v_align': 'center',
                    'v_attach': 'top'
                })
        #bs.animate(self.time_node,'opacity',{0.0: 0.0, 0.35: 1.0})
        #print(bs.animate)


    def update_time():
                import datetime
                e = datetime.datetime.now()
                time_thing = e.strftime("%A, %B %d, %Y") + '\n' + e.strftime("%I:%M:%S %p")
                self.time_node.text = time_thing
    bs.timer(0.5, bs.CallPartial(update_time), repeat=True)
    
    session = bs.get_foreground_host_session()
    if isinstance(session, (bs.FreeForAllSession, bs.DualTeamSession)):
        next_game = bs.get_foreground_host_session().get_next_game_description().evaluate() 
    else:
        next_game = 'NA'
    letext = f"NextGame: {next_game} +_+ PC||MODDER"
    self.text = bs.newnode('text',
                               attrs={
                                   'text': letext,
                                   'scale': 1,
                                   'position': (-45,6),
                                   'maxwidth': 500,
                                   'flatness': 0.0,
                                   'shadow': 0.5,
                                   'h_align': 'right',
                                   'h_attach': 'right',
                                   'v_attach': 'bottom'})

    # snow on map
    def snowfall():
        p = (-10+(random.random()*30),15,-10+(random.random()*30))
        v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
        bs.emitfx(position=p,velocity=v,count=int(5),scale=1+random.random(),spread=0,chunk_type='spark')
        
    #bs.Timer(20,bs.Call(snowfall),repeat = True) no more used. was used for 1.4
    if fire.snow:
        bs.timer(1, bs.CallPartial(snowfall),repeat = True)
        
    if fire.floater:
        if fire.pc_floater:
            special_floater()
        else:
            floaty()


def floaty():
    def path():
        try:
            shared = SharedObjects.get()
            p = bs.newnode(
                'prop',
                attrs={
                    'body': 'sphere',
                    'position': (1.830377363, 4.228850685, 3.803988636),
                    'mesh': bs.getmesh('frostyHead'),
                    'body_scale': 0.0,
                    'mesh_scale': 4.0,
                    'gravity_scale': 0,
                    'shadow_size': 0.0,
                    'color_texture': bs.gettexture('frostyIcon'),
                    'reflection': 'powerup',
                    'reflection_scale': [1.0],
                    'density': 9999999,
                    'materials': (shared.footing_material, shared.footing_material)
                }
            )

            bs.animate_array(
                p, "position", 3,
                {
                    0:(1.830377363,4.228850685,3.803988636),
                    10:(4.148493267,4.429165244,-6.588618549),
                    20:(-5.422572086,4.228850685,2.803988636),
                    25:(-6.859406739,4.429165244,-6.588618549),
                    30:(-6.859406739,4.429165244,-6.588618549),
                    35:(3.148493267,4.429165244,-6.588618549),
                    40:(1.830377363,4.228850685,2.803988636),
                    45:(-5.422572086,4.228850685,2.803988636),
                    50:(-5.422572086,4.228850685,2.803988636),
                    55:(1.830377363,4.228850685,2.803988636),
                    60:(3.148493267,4.429165244,-6.588618549),
                    70:(1.830377363,4.228850685,2.803988636),
                    75:(3.148493267,4.429165244,-6.588618549),
                    80:(-5.422572086,4.228850685,2.803988636),
                    90:(-6.859406739,4.429165244,-6.588618549),
                    95:(-6.859406739,4.429165244,-6.588618549)},loop=True)
        except Exception as e:
            print("Floater error:", e)
    bs.timer(1, bs.CallPartial(path))
    
def special_floater():
    def path():
        try:
            flash = bs.newnode("flash",
            #owner=node,
            attrs={'position': (1.830377363, 4.228850685, 3.803988636),
                   'size':1.5,
                   'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
            bs.animate_array(node=flash, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)
            bs.animate_array(flash, "position", 3, {
                            0:(1.830377363,4.228850685,3.803988636),
                            10:(4.148493267,4.429165244,-6.588618549),
                            20:(-5.422572086,4.228850685,2.803988636),
                            25:(-6.859406739,4.429165244,-6.588618549),
                            30:(-6.859406739,4.429165244,-6.588618549),
                            35:(3.148493267,4.429165244,-6.588618549),
                            40:(1.830377363,4.228850685,2.803988636),
                            45:(-5.422572086,4.228850685,2.803988636),
                            50:(-5.422572086,4.228850685,2.803988636),
                            55:(1.830377363,4.228850685,2.803988636),
                            60:(3.148493267,4.429165244,-6.588618549),
                            70:(1.830377363,4.228850685,2.803988636),
                            75:(3.148493267,4.429165244,-6.588618549),
                            80:(-5.422572086,4.228850685,2.803988636),
                            90:(-6.859406739,4.429165244,-6.588618549),
                            95:(-6.859406739,4.429165244,-6.588618549)},loop=True)    

            nodeShield = bs.newnode('shield', attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                    'position':(1.830377363, 4.228850685, 3.803988636),
                                    'radius': 1.5})
            #bs.animate_array(node=self.flash, attr='color', size=3, keys={0.2: (2, 0, 2),0.4: (2, 2, 0),0.6: (0, 2, 2),0.8: (2, 0, 2),1.0: (1, 1, 0),1.2: (0, 1, 1),1.4: (1, 0, 1)}, loop=True)
            bs.animate_array(nodeShield, "position", 3,{
                            0:(1.830377363,4.228850685,3.803988636),
                            10:(4.148493267,4.429165244,-6.588618549),
                            20:(-5.422572086,4.228850685,2.803988636),
                            25:(-6.859406739,4.429165244,-6.588618549),
                            30:(-6.859406739,4.429165244,-6.588618549),
                            35:(3.148493267,4.429165244,-6.588618549),
                            40:(1.830377363,4.228850685,2.803988636),
                            45:(-5.422572086,4.228850685,2.803988636),
                            50:(-5.422572086,4.228850685,2.803988636),
                            55:(1.830377363,4.228850685,2.803988636),
                            60:(3.148493267,4.429165244,-6.588618549),
                            70:(1.830377363,4.228850685,2.803988636),
                            75:(3.148493267,4.429165244,-6.588618549),
                            80:(-5.422572086,4.228850685,2.803988636),
                            90:(-6.859406739,4.429165244,-6.588618549),
                            95:(-6.859406739,4.429165244,-6.588618549)},loop=True)
        except Exception as e:
            print("Special Floater error:", e)
    bs.timer(1, bs.CallPartial(path))

def enable_textonmap():
    """Enable text-on-map for all maps."""
    _map.Map.__init__ = _map_custom_init
    