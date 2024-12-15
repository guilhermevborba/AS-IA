import pygame
import random
import os
from typing import Optional, Union
from pygame.event import EventType

from checkers import CheckerBoard, Player, PosType, BoardType
from minimax import Minimax

# Defining window size and colours used for the game
WIN_SIZE = (WIDTH, HEIGHT) = (600, 600)
TILE_SIZE = (WIN_SIZE[0] // 10, WIN_SIZE[1] // 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 156, 0)
BLUE = (1, 212, 180)
GRAY = (127, 127, 127)
BOARD_COLOR = [WHITE, BLACK]
PLAYER_COLOR = [ORANGE, BLUE]

# Define the total time for the game (in seconds)
TOTAL_TIME = 200

def draw_board(surface: pygame.Surface, turn: int) -> None:
    surface.fill(BOARD_COLOR[0])  # Fills entire surface of window with a white
    for i in range(0, WIN_SIZE[0], 2 * TILE_SIZE[0]):
        for j in range(0, WIN_SIZE[1], 2 * TILE_SIZE[1]):
            pygame.draw.rect(surface, BOARD_COLOR[1], (i, j, TILE_SIZE[0], TILE_SIZE[1]))
    for i in range(TILE_SIZE[0], WIN_SIZE[0], 2 * TILE_SIZE[0]):
        for j in range(TILE_SIZE[1], WIN_SIZE[1], 2 * TILE_SIZE[1]):
            pygame.draw.rect(surface, BOARD_COLOR[1], (i, j, TILE_SIZE[0], TILE_SIZE[1]))
    pygame.draw.rect(surface, PLAYER_COLOR[turn - 1], ((0, 0), WIN_SIZE), 3)  # Draw outline with colour of the current player's turn

def draw_timer(surface: pygame.Surface, time_left: int) -> None:
    font = pygame.font.SysFont('Arial', 30)
    time_text = font.render(f'Time Left: {time_left}s', True, (0, 0, 0))
    surface.blit(time_text, (10, 10))

def draw_selected(surface: pygame.Surface, posgrid: PosType, color: str) -> None:
    pygame.draw.rect(surface, color, (
        posgrid[0] * TILE_SIZE[0], posgrid[1] * TILE_SIZE[1],
        TILE_SIZE[0], TILE_SIZE[1],
    ), 3)

def draw_player(surface: pygame.Surface, player: Player) -> None:
    for i in range(10):
        for j in range(10):
            if player.pos_pieces[i, j] == 1:
                centre = (
                    round(i * TILE_SIZE[0] + (TILE_SIZE[0] / 2)),
                    round(j * TILE_SIZE[1] + (TILE_SIZE[1] / 2)),
                )
                radius = round(TILE_SIZE[0] / 2 * (9 / 10))
                pygame.draw.circle(surface, PLAYER_COLOR[player.ply - 1], centre, radius)
            elif player.pos_pieces[i, j] == 2:
                centre = (
                    round(i * TILE_SIZE[0] + (TILE_SIZE[0] / 2)),
                    round(j * TILE_SIZE[1] + (TILE_SIZE[1] / 2)),
                )
                radius = round(TILE_SIZE[0] / 2 * (9 / 10))
                pygame.draw.circle(surface, PLAYER_COLOR[player.ply - 1], centre, radius)
                invcol = (
                    255 - PLAYER_COLOR[player.ply - 1][0],
                    255 - PLAYER_COLOR[player.ply - 1][1],
                    255 - PLAYER_COLOR[player.ply - 1][2],
                )
                radius = round(TILE_SIZE[0] / 2 * (2 / 10))
                pygame.draw.circle(surface, invcol, centre, radius)
                pygame.draw.circle(surface, invcol, (centre[0] + 10, centre[1]), radius)
                pygame.draw.circle(surface, invcol, (centre[0], centre[1] + 10), radius)
                pygame.draw.circle(surface, invcol, (centre[0] - 10, centre[1]), radius)
                pygame.draw.circle(surface, invcol, (centre[0], centre[1] - 10), radius)

def select_piece(player: Player, selected: Optional[PosType], moveto: Optional[PosType], event: EventType) -> Union[bool, PosType]:
    pos = event.dict["pos"]
    posgrid = (pos[0] // TILE_SIZE[0], pos[1] // TILE_SIZE[1])
    if (selected is None) and (moveto is None):
        if player.pos_pieces[posgrid]:
            return posgrid
        return False
    if (selected is not None) and (moveto is None):
        return posgrid
    return False

def copy_board(board: BoardType) -> BoardType:
    copy: BoardType = [[0 for _ in range(10)] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            copy[i][j] = board[i][j]
    return copy

def clear() -> None:
    os.system("cls")

def print_score(ply1: Player, ply2: Player) -> None:
    score_str = ""
    score_str += "+------------------------------+\n"
    score_str += "|                              |\n"
    score_str += "|  SCORE:                      |\n"
    score_str += "|                              |\n"
    score_str += f"|  Player1: {ply1.n_eaten:>2}    Player2: {ply2.n_eaten:>2}  |\n"
    score_str += "|                              |\n"
    score_str += "+------------------------------+\n"
    print(score_str)
    if ply1.n_eaten == 15:
        print("\nPLAYER1 WON!")
    elif ply2.n_eaten == 15:
        print("\nPLAYER2 WON!")

if __name__ == "__main__":

    pygame.display.init()  
    pygame.font.init() 
    pygame.display.set_caption("Checker Minimax")  
    surface = pygame.display.set_mode(WIN_SIZE)
    clock = pygame.time.Clock()

    gameboard = CheckerBoard()
    player1 = Player(1)
    player2 = Player(2)
    ai = Minimax(ply_num=1)

    gameboard.update_board(player1.pos_pieces, player2.pos_pieces)
    board = gameboard.board

    clear()
    print(gameboard)

    selected = None
    moveto = None
    movedfrom = (100, 100)
    lastmove = None
    taken = False
    turn = random.choice([1, 2])

    print_score(player1, player2)
    print(f"Player{turn}'s turn\n. . . . . . . .")

    # Timer initialization
    start_ticks = pygame.time.get_ticks()  # Get the initial time
    time_left = TOTAL_TIME  # Time remaining in seconds

    while True:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Convert milliseconds to seconds
        time_left = max(0, TOTAL_TIME - elapsed_time)  # Update the remaining time

        # End the game if the time runs out
        if time_left == 0:
            print("Time's up! Game over.")
            break  # Exit the game loop

        draw_board(surface, turn)
        draw_player(surface, player1)
        draw_player(surface, player2)
        draw_timer(surface, time_left)  # Draw the remaining time on the screen

        player = player1 if (turn == 1) else player2

        if selected and player.pos_pieces[selected]:
            draw_selected(surface, selected, PLAYER_COLOR[player.ply - 1])
            for i in range(0, 10):
                for j in range(0, 10):
                    if player2.move(selected, (i, j), gameboard.board, taken, lastmove, movedfrom, False):
                        draw_selected(surface, (i, j), GRAY)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selected:
                    tmp = select_piece(player, selected, moveto, event)
                    if tmp != selected:
                        moveto = tmp
                else:
                    selected = select_piece(player, selected, moveto, event)
                    movedfrom = selected

        if player == player1:
            board = copy_board(gameboard.board)
            try:
                _, ai_move = ai.minimax(board, 100, True)
                selected, moveto = ai_move
            except TypeError:
                selected = None
                moveto = None

        if moveto is not None:
            if player == player1:
                check = "ply1"
                tmp = player1.move(selected, moveto, gameboard.board, taken, lastmove, movedfrom, True)
                player2.update_dead(tmp)
            else:
                check = "ply2"
                tmp = player2.move(selected, moveto, gameboard.board, taken, lastmove, movedfrom, True)
                player1.update_dead(tmp)

            forced_moves_before = player.check_forced_move(gameboard.board)
            gameboard.update_board(player1.pos_pieces, player2.pos_pieces)
            if tmp is not False:
                taken = True if abs(movedfrom[0] - moveto[0]) == 2 else False
                clear()
                old_turn = turn
                turn = 1 if (turn == 2) else 2
                if isinstance(tmp, tuple) and player.has_forced_moves(gameboard.board):
                    for move in forced_moves_before:
                        if move[0] == moveto:
                            turn = old_turn
                            break
                taken = False if turn != old_turn else taken
                if old_turn != turn:
                    print(f"Player{turn}'s turn\n. . . . . . . .")
                    old_turn = turn
                print_score(player1, player2)

                lastmove = moveto

            moveto = None
            selected = None

        pygame.display.flip()
        clock.tick(30)  # Control the frame rate to 30 FPS
