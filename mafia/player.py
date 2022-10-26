from numpy.random.mtrand import choice

from mafia.the_game import Game


class Player:
    game: Game

    def __init__(self, number, role, game, strategies=None):
        self.game = game
        self.number = number
        self.role = role
        self.is_killed = False
        self.is_voted = False
        self.strategies = strategies or []
        self.checked_by_sheriff = False

    def vote(self):
        vote_probabilities = self.apply_strategies()
        players_putted_to_vote_except_me = self.get_players_putted_to_vote_except_me()
        my_choice = choice(players_putted_to_vote_except_me, p=vote_probabilities)
        self.game.add_vote(self, my_choice)

    def in_game(self):
        return not self.is_killed and not self.is_voted

    def kill(self):
        self.is_killed = True

    def is_red(self):
        return self.role in ['r', 's']

    def is_sheriff(self):
        return self.role in ['s']

    def is_maf(self):
        return self.role in ['m']

    def put_someone_to_vote_if_want(self):
        players_in_vote_list = self.get_players_putted_to_vote_except_me()
        someone = self.decide_who_to_put_to_vote()
        if someone is None:
            return
        if len(players_in_vote_list) == 0:
            self.game.put_on_vote(someone, self)
        if self.am_i_want_and_can_put_someone_to_vote():
            someone = choice(self.get_players_not_putted_to_vote_except_me())
            self.game.put_on_vote(someone, self)

    def get_players_not_putted_to_vote_except_me(self):
        return [
            p for p in self.game.get_players_in_game()
            if p not in self.game.get_players_in_current_vote_round() and p != self
        ]

    def decide_who_to_put_to_vote(self):
        variants = self.get_players_not_putted_to_vote_except_me()
        putting_probabilities = [1/len(variants) for _ in variants]
        if len(variants) == 0:
            return None
        for s in self.strategies:
            putting_probabilities = s.apply_placing_on_vote_strategy(self.game, self, putting_probabilities)
        putting_probabilities = self.game.fix_and_align_probabilities(putting_probabilities)
        return choice(variants, p=putting_probabilities)

    def get_players_putted_to_vote_except_me(self):
        return [
            p for p in self.game.get_players_in_game()
            if p in self.game.get_players_in_current_vote_round() and p != self
        ]

    def am_i_want_and_can_put_someone_to_vote(self):
        am_i_want = choice([0, 1], p=[0.5, 0.5])
        if self.is_sheriff():
            am_i_want = 1
        return am_i_want & len(self.get_players_not_putted_to_vote_except_me())

    def __repr__(self):
        role_to_name = {'m': 'M', 'r': 'R', 's': 'S'}
        status_voted = '|voted' if self.is_voted else ''
        status_killed = '|killed' if self.is_killed else ''
        status_checked = '|checked' if self.checked_by_sheriff else ''
        return f'#{self.number}|{role_to_name[self.role]}{status_voted or status_killed}{status_checked}'

    def apply_strategies(self):
        vote_probabilities = [0 for _ in self.get_players_putted_to_vote_except_me()]
        for s in self.strategies:
            vote_probabilities = s.apply_voting_strategy(self.game, self, vote_probabilities)

        # Here the magic! Sum off all probabilities should be equal to one,
        # so align the result probabilities list
        vote_probabilities = self.game.fix_and_align_probabilities(vote_probabilities)
        return vote_probabilities

    def get_not_checked_players_in_game(self):
        return [p for p in self.game.players if p.in_game() and not p.is_checked() and p is not self]

    def do_check(self):
        not_checked_players = self.get_not_checked_players_in_game()
        if self.role != 's' or len(not_checked_players) == 0:
            return
        player_to_check: Player = choice(not_checked_players)
        player_to_check.checked_by_sheriff = True

    def is_checked(self):
        return self.checked_by_sheriff

    def is_checked_red(self):
        return self.checked_by_sheriff and self.role == 'r'

    def is_checked_maf(self):
        return self.checked_by_sheriff and self.role == 'm'
