import math

import babase
import _bascenev1

from bascenev1._session import Session
from bascenev1._session import _g_player_rejoin_cooldown


def on_player_request_patch(self, player):
    """Called when a new player wants to join the session."""

    if (
        babase.app.classic is not None
        and babase.app.classic.stress_test_update_timer is None
    ):
        if len(self.sessionplayers) >= self.max_players >= 0:

            _bascenev1.getsound('error').play()

            _bascenev1.broadcastmessage(
                babase.Lstr(
                    resource='playerLimitReachedText',
                    subs=[('${COUNT}', str(self.max_players))],
                ),
                color=(0.8, 0.0, 0.0),
                clients=[player.inputdevice.client_id],
                transient=True,
            )
            return False

    from spaz import member_id as mid

    identifier = player.get_v1_account_id()

    if identifier:
        leave_time = self._players_on_wait.get(identifier)

        if leave_time:
            diff = str(
                math.ceil(
                    _g_player_rejoin_cooldown
                    - babase.apptime()
                    + leave_time
                )
            )

            if identifier not in mid.owner:

                _bascenev1.broadcastmessage(
                    babase.Lstr(
                        translate=(
                            'serverResponses',
                            'You can join in ${COUNT} seconds.',
                        ),
                        subs=[('${COUNT}', diff)],
                    ),
                    color=(1, 1, 0),
                    clients=[player.inputdevice.client_id],
                    transient=True,
                )
                return False

            else:
                _bascenev1.broadcastmessage(
                    'Owner Bypass ---> Rejoin Cooldown!',
                    color=(1, 1, 1),
                    clients=[player.inputdevice.client_id],
                    transient=True,
                )

        self._player_requested_identifiers[player.id] = identifier

    _bascenev1.getsound('dripity').play()
    return True

def remove_cooldown():
    Session.on_player_request = on_player_request_patch
    #print('✅ Owner cooldown removed!')