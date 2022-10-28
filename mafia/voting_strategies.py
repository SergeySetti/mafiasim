from abc import abstractclassmethod

from mafia.player import Player
from mafia.the_game import Game


class AbstractStrategy:

    @classmethod
    def apply_voting_strategy(cls, game: Game, player: Player, vote_probabilities: list):
        return vote_probabilities

    @classmethod
    def apply_killing_strategy(cls, game: Game, player: Player, kills_probabilities: list):
        return kills_probabilities

    @classmethod
    def apply_placing_on_vote_strategy(cls, game: Game, player: Player, placing_on_vote_probabilities: list):
        return placing_on_vote_probabilities


class ChancesOfVotingForRedIfRed(AbstractStrategy):
    def __init__(self, probability=0.5):
        self.probability = probability

    def apply_voting_strategy(self, game: Game, player: Player, vote_probabilities: list):
        on_vote = player.get_players_putted_to_vote_except_me()
        p: Player
        for k, p in enumerate(on_vote):
            if p.is_red() and player.is_red():
                vote_probabilities[k] = self.probability
        return vote_probabilities


class ChancesOfVotingForRedIfBlack(AbstractStrategy):
    def __init__(self, probability=0.5):
        self.probability = probability

    def apply_voting_strategy(self, game: Game, player: Player, vote_probabilities: list):
        on_vote = player.get_players_putted_to_vote_except_me()
        p: Player
        for k, p in enumerate(on_vote):
            if p.is_red() and player.is_maf():
                vote_probabilities[k] = self.probability
        return vote_probabilities


class ChancesOfVotingForBlackIfRed(AbstractStrategy):
    def __init__(self, probability=0.5):
        self.probability = probability

    def apply_voting_strategy(self, game: Game, player: Player, vote_probabilities: list):
        on_vote = player.get_players_putted_to_vote_except_me()
        p: Player
        for k, p in enumerate(on_vote):
            if p.is_maf() and player.is_red():
                vote_probabilities[k] = self.probability
        return vote_probabilities


class ChancesOfVotingForBlackIfBlack(AbstractStrategy):
    def __init__(self, probability=0.5):
        self.probability = probability

    def apply_voting_strategy(self, game: Game, player: Player, vote_probabilities: list):
        on_vote = player.get_players_putted_to_vote_except_me()
        p: Player
        for k, p in enumerate(on_vote):
            if p.is_maf() and player.is_maf():
                vote_probabilities[k] = self.probability
        return vote_probabilities


class AlwaysVoteForBlackCheckedBySheriff(AbstractStrategy):
    def apply_voting_strategy(self, game: Game, player: Player, vote_probabilities: list):
        on_vote = player.get_players_putted_to_vote_except_me()
        p: Player
        for k, p in enumerate(on_vote):
            if p.is_checked_maf() and game.sherif_is_uncovered:
                vote_probabilities = [0 for _ in vote_probabilities]
                vote_probabilities[k] = 1
        return vote_probabilities


class ChancesOfVotingForRedThatIsCheckedBySheriff(AbstractStrategy):
    def __init__(self, probability=0):
        self.probability = probability

    def apply_voting_strategy(self, game: Game, player: Player, vote_probabilities: list):
        on_vote = player.get_players_putted_to_vote_except_me()
        p: Player
        for k, p in enumerate(on_vote):
            if p.is_checked_red() and game.sherif_is_uncovered:
                vote_probabilities[k] = self.probability
        return vote_probabilities


class MafiaKillsUncoveredSheriff(AbstractStrategy):
    def __init__(self, probability=1):
        self.probability = probability

    def apply_killing_strategy(self, game: Game, player: Player, kills_probabilities: list):
        candidates_to_die = game.red_players()
        p: Player
        for k, p in enumerate(candidates_to_die):
            if p.is_sheriff() and game.sherif_is_uncovered:
                kills_probabilities = [0 for _ in kills_probabilities]
                kills_probabilities[k] = self.probability
        return kills_probabilities


class MafiaKillsUncoveredRed(AbstractStrategy):
    def __init__(self, probability=1):
        self.probability = probability

    def apply_killing_strategy(self, game: Game, player: Player, kills_probabilities: list):
        candidates_to_die = game.red_players()
        p: Player
        for k, p in enumerate(candidates_to_die):
            if p.is_checked_red() and game.sherif_is_uncovered:
                kills_probabilities = [0 for _ in kills_probabilities]
                kills_probabilities[k] = self.probability
        return kills_probabilities


class RedMustPutOnVoteUncoveredBlack(AbstractStrategy):
    def __init__(self, action_probability=1):
        self.action_probability = action_probability

    def apply_placing_on_vote_strategy(self, game: Game, player: Player, action_probabilities: list):
        candidates_for_vote = player.get_players_not_putted_to_vote_except_me()
        p: Player
        for k, p in enumerate(candidates_for_vote):
            if (p.is_checked_maf() and game.sherif_is_uncovered) or (player.is_sheriff() and p.is_checked_maf()):
                action_probabilities = [0 for _ in action_probabilities]
                action_probabilities[k] = self.action_probability
        return action_probabilities


class RedMustAvoidToPutOnVoteUncoveredRed(AbstractStrategy):
    def __init__(self, action_probability=0):
        self.action_probability = action_probability

    def apply_placing_on_vote_strategy(self, game: Game, player: Player, action_probabilities: list):
        candidates_for_vote = player.get_players_not_putted_to_vote_except_me()
        p: Player
        for k, p in enumerate(candidates_for_vote):
            if (p.is_checked_red() and game.sherif_is_uncovered) or \
                    (player.is_sheriff() and p.is_checked_red()) or \
                    (p.is_sheriff() and game.sherif_is_uncovered):
                action_probabilities[k] = self.action_probability
        return action_probabilities
