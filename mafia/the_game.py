import datetime
from collections import Counter
from random import shuffle

from numpy.random.mtrand import choice


class Game:
    def __init__(self):
        self.players = []
        self.predefined_roles = ['m', 'm', 'm', 'r', 'r', 'r', 'r', 'r', 'r', 's']
        self.current_vote_round = []
        self.votes = []
        self.game_statistics = {
            'who_placed_on_vote_by_who': [],
            'who_vote_who': [],
            'who_wins': '',
            'when_sheriff_killed': 10,
        }
        self.the_game_is_over = False
        self.who_wins = None
        self.day_number = 0
        self.sherif_is_uncovered = False
        shuffle(self.predefined_roles)
        self.game_time = datetime.datetime.now()

    def init_game(self, players_strategies):
        self.create_10_players(players_strategies)

    def create_10_players(self, players_strategies):
        from mafia.player import Player
        [
            self.players.append(Player(p, self.predefined_roles.pop(), self, players_strategies[k]))
            for k, p in enumerate(range(1, 11))
        ]

    def get_players_in_game(self):
        return [p for p in self.players if p.in_game()]

    def red_players(self):
        return [p for p in self.get_players_in_game() if p.is_red()]

    def maf_players(self):
        return [p for p in self.get_players_in_game() if p.is_maf()]

    def kill_player(self, p):
        p.kill()
        if p.is_sheriff():
            self.game_statistics['when_sheriff_killed'] = self.day_number
            self.sherif_is_uncovered = True

    def decide_who_to_kill(self):
        kills_probabilities = [0 for _ in self.red_players()]
        any_maf = self.maf_players()[0]
        for s in any_maf.strategies:
            kills_probabilities = s.apply_killing_strategy(self, any_maf, kills_probabilities)
        kills_probabilities = self.fix_and_align_probabilities(kills_probabilities)
        return choice(self.red_players(), p=kills_probabilities)

    def prepare_vote_round(self):
        for p in self.get_players_in_game():
            p.put_someone_to_vote_if_want()

    def get_players_in_current_vote_round(self):
        return [row[0] for row in self.current_vote_round]

    def put_on_vote(self, someone, me):
        if someone not in self.get_players_in_current_vote_round():
            self.current_vote_round.append((someone, me))
            self.game_statistics['who_placed_on_vote_by_who'].append((someone, me))

    def commit_vote_round(self):
        from mafia.player import Player
        p: Player
        for p in self.get_players_in_game():
            p.vote()
        self.calc_votes()

    def add_vote(self, who_vote, to_whom):
        self.votes.append((who_vote, to_whom))
        self.game_statistics['who_vote_who'].append((who_vote, to_whom))

    def calc_votes(self):
        votes_list = [v[1] for v in self.votes]
        players_counts = Counter(votes_list)
        most_voted_players = players_counts.most_common(2)
        self.is_there_skirmish(most_voted_players)  # Conditional recursion here

        self.finish_round(most_voted_players[0][0])

        return most_voted_players[0]

    def is_there_skirmish(self, most_voted_players):
        if len(most_voted_players) > 1 and (most_voted_players[0][1] == most_voted_players[1][1]):
            self.votes = []
            self.current_vote_round = [
                r for r in self.current_vote_round
                if (r[0] == most_voted_players[0][0]) or (r[0] == most_voted_players[1][0])
            ]
            self.commit_vote_round()

    def finish_round(self, most_voted_player):
        most_voted_player.is_voted = True
        self.current_vote_round = []
        self.votes = []
        self.check_if_game_is_over()

    def check_if_game_is_over(self):
        mafs_count = sum(map(lambda x: x.is_maf(), self.get_players_in_game()))
        reds_count = sum(map(lambda x: x.is_red(), self.get_players_in_game()))
        if mafs_count == reds_count:
            self.the_game_is_over = True
            self.who_wins = 'maf'
            self.game_statistics['who_wins'] = self.who_wins
            return True
        if mafs_count == 0:
            self.the_game_is_over = True
            self.who_wins = 'reds'
            self.game_statistics['who_wins'] = self.who_wins
            return True
        return False

    def __repr__(self):
        mafs_count = sum(map(lambda x: x.is_maf(), self.get_players_in_game()))
        reds_count = sum(map(lambda x: x.is_red(), self.get_players_in_game()))
        return f'Game | Mafs: {mafs_count}, Reds: {reds_count} | Day: {self.day_number}'

    def commit_night_events(self):
        if self.the_game_is_over:
            return
        self.kill_player(self.decide_who_to_kill())
        self.check_if_game_is_over()
        sheriff = self.get_sheriff()
        if sheriff.in_game():
            sheriff.do_check()

    def get_sheriff(self):
        return next(p for p in self.players if p.is_sheriff())

    def commit_day_events(self):
        if self.the_game_is_over:
            return
        self.day_number += 1
        self.sherif_is_decided_to_uncover_himself_or_not()
        self.prepare_vote_round()
        self.commit_vote_round()

    def sherif_is_decided_to_uncover_himself_or_not(self):
        sheriff = self.get_sheriff()
        if self.day_number == 2 or not sheriff.in_game():
            self.sheriff_is_uncovers_himself()

    def sheriff_is_uncovers_himself(self):
        self.sherif_is_uncovered = True

    @staticmethod
    def fix_and_align_probabilities(probs):
        if sum(probs) == 0:
            probs = [v + 0.01 for v in probs]
        probs = [x * (1 / sum(probs)) for x in probs]
        return probs
