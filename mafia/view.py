from math import *
import pygame
from mafia.voting_strategies import *

pygame.init()
clock = pygame.time.Clock()

W = 900
H = 700
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mafia Simulation")

run = True

red = (178, 16, 22)
white = (255, 255, 255)
white_yellow = (255, 252, 204)
black = (0, 0, 0)
font = pygame.font.SysFont('C:/Windows/Fonts/Arial.ttf', 22)

win.fill(white_yellow)


typical_tactics = [
    ChancesOfVotingForRedIfRed(0.5),
    ChancesOfVotingForBlackIfRed(0.5),
    AlwaysVoteForBlackCheckedBySheriff(),
    ChancesOfVotingForRedThatIsCheckedBySheriff(0),
    MafiaKillsUncoveredRed(1),
    MafiaKillsUncoveredSheriff(1),
    RedMustPutOnVoteUncoveredBlack(1),
    RedMustAvoidToPutOnVoteUncoveredRed(0),
]
players_strategies = [typical_tactics for _ in range(10)]
players_strategies = [[g_id, typical_tactics] for g_id in range(10)]

game = Game()
game.init_game(players_strategies)
game_cycle = [game.commit_night_events, game.commit_day_events]

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            step = game_cycle.pop(0)
            game_cycle.append(step)
            step()

    center_x = W / 2
    center_y = H / 2
    radius = 250
    pygame.draw.circle(win, white, (center_x, center_y), radius=3)

    for k, player in enumerate(game.players):
        x = radius * cos(radians(360 / 10 * k)) + center_x
        y = radius * sin(radians(360 / 10 * k)) + center_y
        color = black if player.is_maf() else red
        pygame.draw.circle(win, color, (x, y), radius=20)
        text = font.render(f'{player}', True, white_yellow, color)
        win.blit(text, (x-12, y-11))

    game_status_text = font.render(f'{game}', True, black, white_yellow)
    win.blit(game_status_text, (20, 20))

    clock.tick(5)
    pygame.display.update()

pygame.quit()
quit()
