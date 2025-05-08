import unittest

from mafia.voting_strategies import *
from mafia.the_game import Game


class TestMafiaSimulation(unittest.TestCase):

    def test_get_average_delivered_for_partner(self):

        typical_tactics = [
            ChancesOfVotingForRed(0.5),
            ChancesOfVotingForBlack(0.5),
            AlwaysVoteForBlackCheckedBySheriff(),
            ChancesOfVotingForRedThatIsCheckedBySheriff(0),
            MafiaKillsUncoveredRed(1),
            MafiaKillsUncoveredSheriff(1),
            RedMustPutOnVoteUncoveredBlack(1),
            RedMustAvoidToPutOnVoteUncoveredRed(0),
        ]
        players_strategies = [typical_tactics for _ in range(10)]

        for i in range(10):
            game = Game()
            game.init_game(players_strategies)
            while True:
                game.commit_night_events()
                if game.the_game_is_over:
                    break
                game.commit_day_events()
                if game.the_game_is_over:
                    break
            players_in_game = game.get_players_in_game()
            self.assertIsNotNone(players_in_game)
