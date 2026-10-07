import babase
import _bascenev1
import bascenev1
import math

from bascenev1._session import Session


def on_player_request_patch(self, player: bascenev1.SessionPlayer) -> bool:
    """Called when a new player wants to join the session."""

    # Limit player counts *unless* we're in a stress test.
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

    # Rejoin cooldown.
    identifier = player.get_account_id()

    if identifier:

        from spaz import member_id as mid

        # Owners bypass the rejoin cooldown.
        if identifier not in mid.owner:

            leave_time = self._players_on_wait.get(identifier)

            if leave_time:
                diff = str(
                    math.ceil(
                        _g_player_rejoin_cooldown
                        - babase.apptime()
                        + leave_time
                    )
                )

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

        self._player_requested_identifiers[player.id] = identifier

    _bascenev1.getsound('dripity').play()
    return True


def enable_lobby():
    Session.on_player_request = on_player_request_patch
