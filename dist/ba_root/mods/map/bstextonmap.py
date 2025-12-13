# bstextonmap.py
from __future__ import annotations
import random
import bascenev1 as bs
from bascenev1 import _map

# Save original Map.__init__ to call it safely

_original_map_init = _map.Map.__init__

def _map_custom_init(self, *args, **kwargs):
    """Custom Map init to add text on map."""
    
    # Call the original __init__ safely
    
    _original_map_init(self, *args, **kwargs)

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
        
    next_game = bs.get_foreground_host_session().get_next_game_description().evaluate()
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


def enable_textonmap():
    """Enable text-on-map for all maps."""
    _map.Map.__init__ = _map_custom_init
