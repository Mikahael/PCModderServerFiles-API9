# ba_meta require api 9

import os
import json
import babase
import _babase
import bascenev1 as bs

# ==============================
# 📁 FILE PATH SETUP
# ==============================

#MODS_DIR = _babase.app.env.python_directory_user
#DATA_DIR = os.path.join(MODS_DIR, "playersdata") #not needed, we can directly inject!
STATS_FILE = 'ba_root/mods/config/player_data.json'


# ==============================
# 📊 RANK SYSTEM
# ==============================

class RankSystem:

    def __init__(self):
        self.data = {}
        #self._ensure_folder()
        self._load()

    # Load stats from file
    def _load(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except:
                print("⚠ Failed to load stats, resetting file.")
                self.data = {}

    # Save stats to file
    def _save(self):
        try:
            with open(STATS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("⚠ Save error:", e)

    # Ensure player exists in database
    def ensure_player(self, account_id):
        if account_id not in self.data:
            self.data[account_id] = {
                "score": 0,
                "kills": 0,
                "deaths": 0,
                "wins": 0,
                "games": 0,
                "rank": 0
            }

    # Add stats after a match
    def add_stats(self, account_id, kills, deaths, score, won):
        self.ensure_player(account_id)

        p = self.data[account_id]
        p["kills"] += kills
        p["deaths"] += deaths
        p["score"] += score
        p["games"] += 1

        if won:
            p["wins"] += 1

        self._update_ranks()
        self._save()

    # Recalculate ranks based on score
    def _update_ranks(self):
        sorted_players = sorted(
            self.data.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )

        for i, (account_id, stats) in enumerate(sorted_players):
            stats["rank"] = i + 1

    # Get player rank
    def get_rank(self, account_id):
        return self.data.get(account_id, {}).get("rank", 0)


# Global instance
rank_sys = RankSystem()


# ==============================
# 📈 COLLECT MATCH STATS
# ==============================

def collect_stats(activity):
    try:
        stats = activity.stats
        if not stats:
            return

        # Get winning players
        winners = set()

        results = getattr(activity, "_game_results", None)
        if results and hasattr(results, "get_sessionteam_info"):
            for team_info in results.get_sessionteam_info():
                if team_info:
                    team = team_info[0]
                    for player in team.players:
                        aid = player.get_v1_account_id()
                        if aid:
                            winners.add(aid)
                    break  # only first team = winner

        # Loop through players
        for record in stats.get_records().values():
            player = record.player
            account_id = player.get_v1_account_id()

            if not account_id:
                continue

            rank_sys.add_stats(
                account_id=account_id,
                kills=record.accum_kill_count,
                deaths=record.accum_killed_count,
                score=record.accumscore,
                won=(account_id in winners)
            )

    except Exception as e:
        print("⚠ Stats collection error:", e)


def enable_stats():

    def start_up():
        print("✅ Stats system loaded")

        import bascenev1._gameactivity as ga

        # -------- Player Spawn Hook --------
        old_spawn = ga.GameActivity.spawn_player_spaz

        def new_spawn(self, player, *args, **kwargs):
            spaz = old_spawn(self, player, *args, **kwargs)

            try:
                aid = player.sessionplayer.get_v1_account_id()
                if aid:
                    rank_sys.ensure_player(aid)
            except Exception as e:
                print("Spawn error:", e)

            return spaz

        ga.GameActivity.spawn_player_spaz = new_spawn

        # -------- Game End Hook --------
        old_end = ga.GameActivity.end

        def new_end(self, results=None, *args, **kwargs):
            try:
                if results:
                    self._game_results = results

                collect_stats(self)

            except Exception as e:
                print("End error:", e)

            return old_end(self, results, *args, **kwargs)

        ga.GameActivity.end = new_end
        
    start_up()