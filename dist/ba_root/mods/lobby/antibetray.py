import logging
import random

import babase
import _bascenev1

from bascenev1._stats import Stats

nooblist = []


def player_was_killed_patch(
    self,
    player,
    killed=False,
    killer=None,
):
    name = player.getname()
    prec = self._player_records[name]
    prec.streak = 0

    if killed:
        prec.accum_killed_count += 1
        prec.killed_count += 1

    try:
        if killed:

            if killer is player:

                # Suicide tracking.
                if not hasattr(player, 'suicide_count'):
                    player.suicide_count = 0

                player.suicide_count += 1

                if player.suicide_count == 3:
                    try:
                        account_id = (
                            player.sessionplayer.get_account_id()
                        )

                        if account_id not in nooblist:
                            nooblist.append(account_id)
                            # basically if u kill urself 3x - u get a special tag called noob, but it does reset every round..

                    except Exception:
                        logging.exception(
                            'Failed to add player to noob list.'
                        )

                if _bascenev1.getactivity().announce_player_deaths:
                    _bascenev1.broadcastmessage(
                        babase.Lstr(
                            resource='nameSuicideText',
                            subs=[('${NAME}', name)]
                        ),
                        top=True,
                        color=player.color,
                        image=player.get_icon(),
                    )

                suicide_messages = [
                    '{} rage quit against the map.',
                    '{} eliminated themselves professionally.',
                    '{} pressed the self-destruct button.',
                    '{} became their own worst enemy.',
                    '{} sacrificed themselves for absolutely nothing.',
                    '{} disconnected from life temporarily.',
                    '{} skill-issued themselves.',
                    '{} thought they were immortal.',
                    '{} speedran dying.',
                    '{} entered spectator mode early.',
                ]

                message = random.choice(
                    suicide_messages
                ).format(name)

                import fire

                if fire.suicide_messages:
                    _bascenev1.broadcastmessage(
                        message,
                        color=(1, 1, 1),
                    )

            elif killer is not None:

                if killer.team is player.team:

                    if not hasattr(killer, 'betray_count'):
                        killer.betray_count = 0

                    killer.betray_count += 1

                    clID = (
                        killer.sessionplayer
                        .inputdevice.client_id
                    )

                    _bascenev1.broadcastmessage(
                        f'Warning, Please dont betray! | '
                        f'{killer.getname()}! '
                        f'({killer.betray_count}/3)',
                        color=(1, 1, 1),
                        clients=[clID],
                        transient=True,
                    )

                    if killer.betray_count >= 3:

                        _bascenev1.broadcastmessage(
                            f'{killer.getname()} was kicked '
                            f'for betrayal! Play fair!',
                            color=(1, 1, 1),
                        )

                        try:
                            client_id = (
                                killer.sessionplayer
                                .inputdevice.client_id
                            )

                            _bascenev1.disconnect_client(
                                client_id
                            )

                        except Exception:
                            logging.exception(
                                'Failed to disconnect client.'
                            )

                        return

                    if _bascenev1.getactivity().announce_player_deaths:
                        _bascenev1.broadcastmessage(
                            babase.Lstr(
                                resource='nameBetrayedText',
                                subs=[
                                    ('${NAME}', killer.getname()),
                                    ('${VICTIM}', name),
                                ],
                            ),
                            top=True,
                            color=killer.color,
                            image=killer.get_icon(),
                        )

                else:

                    if _bascenev1.getactivity().announce_player_deaths:
                        _bascenev1.broadcastmessage(
                            babase.Lstr(
                                resource='nameKilledText',
                                subs=[
                                    ('${NAME}', killer.getname()),
                                    ('${VICTIM}', name),
                                ],
                            ),
                            top=True,
                            color=killer.color,
                            image=killer.get_icon(),
                        )

            else:

                if _bascenev1.getactivity().announce_player_deaths:
                    _bascenev1.broadcastmessage(
                        babase.Lstr(
                            resource='nameDiedText',
                            subs=[('${NAME}', name)],
                        ),
                        top=True,
                        color=player.color,
                        image=player.get_icon(),
                    )

    except Exception:
        logging.exception('Error announcing kill.')


def load_anti_betray():
    Stats.player_was_killed = player_was_killed_patch
    print('✅ Antibetray loaded!')