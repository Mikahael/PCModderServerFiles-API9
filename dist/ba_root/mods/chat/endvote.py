# endvote.py

import bascenev1 as bs
import _bascenev1 as _bs
import maps.bstextonmap as bstextonmap

votes: dict[str, int] = {}
vote_in_progress = False
vote_timer = None


def get_activity():
    return bs.get_foreground_host_activity()


def update_endvote_text():

    node = bstextonmap.endvote_node

    if node is None:
        return

    if not vote_in_progress:
        node.text = ''
        return

    yes_votes = sum(votes.values())
    no_votes = len(votes) - yes_votes

    node.text = (
        f"[EndVote: YES {yes_votes} | NO {no_votes}]"
    )


def get_player_by_client_id(client_id: int):

    activity = get_activity()

    if activity is None:
        return None

    for player in activity.players:
        try:
            sessionplayer = player.sessionplayer

            if sessionplayer.inputdevice.client_id == client_id:
                return player

        except Exception:
            continue

    return None


def end_vote(starter_client_id: int):

    global votes
    global vote_in_progress
    global vote_timer

    activity = get_activity()

    if activity is None:
        return

    if vote_in_progress:

        bs.broadcastmessage(
            "A vote is already in progress.",
            color=(1, 0, 0),
            transient=True
        )
        return

    if len(activity.players) < 2:

        bs.broadcastmessage(
            "Not enough players for a vote.",
            color=(1, 0, 0),
            transient=True
        )
        return

    votes = {}
    vote_in_progress = True

    update_endvote_text()

    bs.broadcastmessage(
        "Vote to end the match started!\n"
        "Type /vote 1 for YES or /vote 0 for NO",
        color=(1, 1, 0),
        transient=True
    )

    vote_timer = bs.AppTimer(
        20.0,
        count_votes
    )


def count_votes():

    global vote_in_progress

    activity = get_activity()

    if activity is None:
        vote_in_progress = False
        update_endvote_text()
        return

    total_players = len(activity.players)

    yes_votes = sum(votes.values())
    no_votes = len(votes) - yes_votes

    vote_in_progress = False

    update_endvote_text()

    bs.broadcastmessage(
        f"Vote Results | YES: {yes_votes} | NO: {no_votes}",
        color=(1, 1, 1),
        transient=True
    )

    required_yes = max(1, (total_players // 2) + 1)

    if yes_votes >= required_yes:

        bs.broadcastmessage(
            "Vote passed! Ending game...",
            color=(0, 1, 0),
            transient=True
        )

        bs.timer(
            2.0,
            activity.end_game
        )

    else:

        bs.broadcastmessage(
            f"Vote failed! Need {required_yes} YES votes.",
            color=(1, 0, 0),
            transient=True
        )


def handle_vote(client_id: int, vote: int):

    global votes

    if not vote_in_progress:

        bs.broadcastmessage(
            "No vote is currently active.",
            color=(1, 0, 0),
            transient=True
        )
        return

    if vote not in (0, 1):

        bs.broadcastmessage(
            "Use /vote 1 or /vote 0",
            color=(1, 0, 0),
            transient=True
        )
        return

    player = get_player_by_client_id(client_id)

    if player is None:

        bs.broadcastmessage(
            "Player not found.",
            color=(1, 0, 0),
            transient=True
        )
        return

    try:
        account_id = player.sessionplayer.get_account_id()
        player_name = player.getname(full=True)

    except Exception:

        bs.broadcastmessage(
            "Failed to identify player.",
            transient=True
        )
        return

    if account_id in votes:

        bs.broadcastmessage(
            "You already voted.",
            color=(1, 0.5, 0),
            transient=True
        )
        return

    votes[account_id] = vote

    update_endvote_text()

    bs.broadcastmessage(
        f"{player_name} voted {'YES' if vote else 'NO'}",
        color=(0, 1, 1),
        transient=True
    )

    activity = get_activity()

    if activity is not None:
        if len(votes) >= len(activity.players):
            count_votes()