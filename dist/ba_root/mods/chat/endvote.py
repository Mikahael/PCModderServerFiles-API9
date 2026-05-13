import bascenev1 as bs
import _bascenev1 as _bs
import random

votes: dict[str, int] = {}
vote_in_progress = False
vote_timer = None


def get_activity():
    """Get current foreground activity safely."""
    return bs.get_foreground_host_activity()


def get_player_by_client_id(client_id: int):
    """Find player from client id."""
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
            clients=[starter_client_id],
            transient=True
        )
        return

    # Optional minimum player requirement
    if len(activity.players) < 2:
        bs.broadcastmessage(
            "Not enough players for a vote.",
            clients=[starter_client_id],
            color=(1, 0, 0),
            transient=True
        )
        return

    votes = {}
    vote_in_progress = True

    bs.broadcastmessage(
        "Vote to end the match started!\n"
        "Type /vote 1 for YES or /vote 0 for NO")

    vote_timer = bs.AppTimer(
        20.0,
        count_votes
    )


def count_votes():
    global vote_in_progress

    activity = get_activity()

    if activity is None:
        vote_in_progress = False
        return

    total_players = len(activity.players)

    yes_votes = sum(votes.values())
    no_votes = len(votes) - yes_votes

    vote_in_progress = False

    bs.broadcastmessage(
        f"Vote Results | YES: {yes_votes} | NO: {no_votes}",
        color=(1, 1, 1),
        transient=True
    )

    # Majority requirement
    required_yes = max(1, (total_players // 2) + 1)

    if yes_votes >= required_yes:

        bs.broadcastmessage(
            "Vote passed! Ending game...",
            color=(0, 1, 0),
            transient=True
        )

        bs.timer(
            2.0,
            bs.WeakCallPartial(activity.end_game)
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
            clients=[client_id],
            color=(1, 0, 0),
            transient=True
        )
        return

    if vote not in (0, 1):

        bs.broadcastmessage(
            "Use /vote 1 or /vote 0",
            clients=[client_id],
            color=(1, 0, 0),
            transient=True
        )
        return

    player = get_player_by_client_id(client_id)

    if player is None:

        bs.broadcastmessage(
            "Player not found.",
            clients=[client_id],
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
            clients=[client_id],
            transient=True
        )
        return

    # Prevent duplicate voting
    if account_id in votes:

        bs.broadcastmessage(
            "You already voted.",
            clients=[client_id],
            color=(1, 0.5, 0),
            transient=True
        )
        return

    votes[account_id] = vote

    bs.broadcastmessage(
        f"{player_name} voted {'YES' if vote else 'NO'}",
        color=(0, 1, 1),
        transient=True
    )

    # Optional early finish if everyone voted
    activity = get_activity()

    if activity is not None:
        if len(votes) >= len(activity.players):
            count_votes()