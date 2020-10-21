# Chess piece images provided by Wikimedia Commons. I claim no credit for the png files
# https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

import pygame
from pygame import Color
from piece import Piece
from pygame import Rect
import operator
from util import round_to_position

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
WINDOW_SCREEN = (WINDOW_WIDTH, WINDOW_HEIGHT)

GAME_WIDTH = 800
GAME_HEIGHT = 800
GAME_SCREEN = (GAME_WIDTH, GAME_HEIGHT)


class Display:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(WINDOW_SCREEN)
        self.game_screen = pygame.Surface(GAME_SCREEN)

        self.game_loop = True

        self.whites = []
        self.blacks = []

        self.is_white_turn = True

        self.available_positions = []
        self.selected_piece = None

        # load images
        self.bPawnPng = pygame.image.load('assets/b_pawn.png')
        self.wPawnPng = pygame.image.load('assets/w_pawn.png')
        self.bBishopPng = pygame.image.load('assets/b_bishop.png')
        self.wBishopPng = pygame.image.load('assets/w_bishop.png')
        self.bKnightPng = pygame.image.load('assets/b_knight.png')
        self.wKnightPng = pygame.image.load('assets/w_knight.png')
        self.bRookPng = pygame.image.load('assets/b_rook.png')
        self.wRookPng = pygame.image.load('assets/w_rook.png')
        self.bQueenPng = pygame.image.load('assets/b_queen.png')
        self.wQueenPng = pygame.image.load('assets/w_queen.png')
        self.bKingPng = pygame.image.load('assets/b_king.png')
        self.wKingPng = pygame.image.load('assets/w_king.png')

        self.white_square = Color(181, 38, 62)
        self.white_square_faded = Color(60, 13, 21)
        self.black_square = Color(255, 223, 223)
        self.black_square_faded = Color(85, 74, 74)

        self.stop = False
        self.gameover = False
        self.winner = ''

        self.gameover_screen = None
        self.gameover_text = None
        self.start_new_game_text = None
        self.start_new_game_box = None

        self.clock = pygame.time.Clock()

    def display_gameover(self):
        self.gameover_screen = pygame.Surface((WINDOW_WIDTH, 300), pygame.SRCALPHA)
        self.gameover_screen.fill((0, 0, 0, 216))

        font = pygame.font.SysFont(None, 48)
        self.gameover_text = font.render('{} wins the game!'.format(self.winner), True, Color(255, 255, 255))

    def display_new_game(self, underline=False, font_size=56):
        font = pygame.font.SysFont(None, font_size)
        font.set_underline(underline)
        self.start_new_game_text = font.render('New Game', True, Color(255, 255, 255))

    def is_mouseover_new_game(self, pos):
        """
        Checks for mouseover on the New Game button
        """
        if self.start_new_game_box is None:
            False
        if self.start_new_game_box.collidepoint(pos):
            self.display_new_game(True)
            return True
        else:
            self.display_new_game()

    def get_screen_adjusted_mouse_pos(self, screen):
        if screen == self.game_screen:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0] - ((WINDOW_WIDTH - GAME_WIDTH) / 2)
            y = mouse_pos[1] - ((WINDOW_HEIGHT - GAME_HEIGHT) / 2)
            pos = (x, y)
            return pos
        elif screen == self.gameover_screen:
            print('gameover screen is not configured for mouse input')
        elif screen == self.display:
            print('display is not configured for mouse input')

    def get_setup_piece_for_pos(self, pos):
        isWhite = True if pos[0] <= 1 else False
        if (pos[0] == 1 or pos[0] == 6):
            img = self.wPawnPng if isWhite else self.bPawnPng
            return Piece('pawn', pos, isWhite, img)
        elif (pos[1] == 0 or pos[1] == 7):
            img = self.wRookPng if isWhite else self.bRookPng
            return Piece('rook', pos, isWhite, img)
        elif (pos[1] == 1 or pos[1] == 6):
            img = self.wKnightPng if isWhite else self.bKnightPng
            return Piece('knight', pos, isWhite, img)
        elif (pos[1] == 2 or pos[1] == 5):
            img = self.wBishopPng if isWhite else self.bBishopPng
            return Piece('bishop', pos, isWhite, img)
        elif (pos[1] == 3):
            img = self.wQueenPng if isWhite else self.bQueenPng
            return Piece('queen', pos, isWhite, img)
        elif (pos[1] == 4):
            img = self.wKingPng if isWhite else self.bKingPng
            return Piece('king', pos, isWhite, img)

    def draw_information(self):
        for square in range(0, 8):
            font = pygame.font.SysFont(None, 26)
            font.set_bold(False)
            number_text = font.render(str(square + 1), True, Color(255, 255, 255))
            letter_text = font.render(chr(square + 65), True, Color(255, 255, 255))

            # 1-8
            self.display.blit(number_text, (((WINDOW_WIDTH - GAME_WIDTH) / 2) - 30, ((WINDOW_HEIGHT - GAME_HEIGHT) / 2) + 44 + (square * 100)))
            self.display.blit(number_text, (WINDOW_WIDTH - ((WINDOW_WIDTH - GAME_WIDTH) / 2) + 20, ((WINDOW_HEIGHT - GAME_HEIGHT) / 2) + 44 + (square * 100)))
            # A-H
            self.display.blit(letter_text, (((WINDOW_WIDTH - GAME_WIDTH) / 2) + 40 + (square * 100), ((WINDOW_HEIGHT - GAME_HEIGHT) / 2) - 36))
            self.display.blit(letter_text, (((WINDOW_WIDTH - GAME_WIDTH) / 2) + 40 + (square * 100), WINDOW_HEIGHT - ((WINDOW_HEIGHT - GAME_HEIGHT) / 2) + 28))

    def draw(self):
        for y in range(0, 8):
            for x in range(0, 8):
                color = self.white_square if (y + x) % 2 != 0 else self.black_square
                if self.selected_piece is None or self.selected_piece.pos in self.available_positions:
                    color = self.white_square if (y + x) % 2 != 0 else self.black_square
                else:
                    if (self.available_positions is None or len(self.available_positions) <= 0) or (y, x) not in self.available_positions:
                        color = self.white_square_faded if (y + x) % 2 != 0 else self.black_square_faded
                pygame.draw.rect(self.game_screen, color, (x * 100, y * 100, 100, 100))

        for piece in self.whites:
            self.game_screen.blit(piece.img, ((piece.pos[1] * 100) + 18, (piece.pos[0] * 100) + 18))
        for piece in self.blacks:
            self.game_screen.blit(piece.img, ((piece.pos[1] * 100) + 18, (piece.pos[0] * 100) + 18))

        if self.selected_piece:
            # draw available position outlines
            pygame.draw.rect(self.game_screen, Color(255, 255, 255), (self.selected_piece.pos[1] * 100, self.selected_piece.pos[0] * 100, 100, 100), 3)

        if self.gameover:
            if self.gameover_screen is not None:
                self.game_screen.blit(self.gameover_screen, (0, 250))
                self.game_screen.blit(self.gameover_text, ((GAME_WIDTH / 2) - (self.gameover_text.get_width() / 2), 325 - (self.gameover_text.get_height() / 2)))

                if self.start_new_game_box is None:
                    # Adjust new game position
                    x = GAME_WIDTH - (self.start_new_game_text.get_width() * 1.3)
                    y = 485 - (self.start_new_game_text.get_height() / 2)
                    self.start_new_game_box = Rect(x, y, self.start_new_game_text.get_width(), self.start_new_game_text.get_height())
                self.game_screen.blit(self.start_new_game_text, (self.start_new_game_box.left, self.start_new_game_box.top))

        self.draw_information()
        self.display.blit(self.game_screen, ((WINDOW_WIDTH - GAME_WIDTH) / 2, (WINDOW_HEIGHT - GAME_HEIGHT) / 2))

    def get_piece(self, pos):
        """
        Gets the piece or None based on position (y, x)
        """
        for piece in self.whites:
            if piece.pos == pos:
                return piece
        for piece in self.blacks:
            if piece.pos == pos:
                return piece
        return None

    def kill_piece(self, piece):
        """
        Kills the provided piece and checks for win condition
        """
        is_king = piece.type == 'king'
        if piece.isWhite is True:
            for pieces in self.whites:
                if pieces == piece:
                    self.whites.remove(piece)
                    if is_king:
                        self.gameover = True
                        self.winner = 'Black'
                    return
        elif piece.isWhite is False:
            for pieces in self.blacks:
                if pieces == piece:
                    self.blacks.remove(piece)
                    if is_king:
                        self.gameover = True
                        self.winner = 'White'
                    return

    def move_seleceted_piece(self, pos):
        """
        Moves the currently selected piece to the given pos (y, x). Checks for en passage movement
        """
        for index in range(0, len(self.whites)):
            if self.whites[index] == self.selected_piece:
                target_piece = self.get_piece(pos)
                if target_piece is not None:
                    self.kill_piece(target_piece)
                else:
                    if self.selected_piece.type == 'pawn':
                        if self.selected_piece.pos[1] != pos[1]:
                            target_piece = self.get_piece((self.selected_piece.pos[0], pos[1]))
                            if target_piece is None:
                                print('OK BUG')
                            self.kill_piece(target_piece)
                self.whites[index].move_to(pos)
                return

        for index in range(0, len(self.blacks)):
            if self.blacks[index] == self.selected_piece:
                target_piece = self.get_piece(pos)
                if target_piece is not None:
                    self.kill_piece(target_piece)
                else:
                    if self.selected_piece.type == 'pawn':
                        if self.selected_piece.pos[1] != pos[1]:
                            target_piece = self.get_piece((self.selected_piece.pos[0], pos[1]))
                            if target_piece is None:
                                print('OK BUG')
                            self.kill_piece(target_piece)
                self.blacks[index].move_to(pos)
                return

    def new_turn(self):
        """
        Remove selected piece, currently available positions and advances turn. Updates en passage movement
        """
        for index in range(0, len(self.whites)):
            if self.whites[index] == self.selected_piece:
                continue
            if self.whites[index].en_passant is True:
                self.whites[index].en_passant = False
        for index in range(0, len(self.blacks)):
            if self.blacks[index] == self.selected_piece:
                continue
            if self.blacks[index].en_passant is True:
                self.blacks[index].en_passant = False
        self.is_white_turn = operator.not_(self.is_white_turn)
        self.selected_piece = None
        self.available_positions = []

    def init_new_game(self):
        """
        Resets required game variables to their original state
        """
        self.whites = []
        self.blacks = []

        self.available_positions = []
        self.selected_piece = None

        self.is_white_turn = True
        self.stop = False
        self.gameover = False
        self.winner = ''

        self.gameover_screen = None

    def run(self):
        while self.game_loop:
            for y in range(0, 2):
                for x in range(0, 8):
                    self.whites.append(self.get_setup_piece_for_pos((y, x)))
            for y in range(6, 8):
                for x in range(0, 8):
                    self.blacks.append(self.get_setup_piece_for_pos((y, x)))

            while not self.gameover:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop = True
                        self.gameover = True
                        self.game_loop = False

                click = pygame.mouse.get_pressed()
                if click[0] is True:
                    mouse_pos = self.get_screen_adjusted_mouse_pos(self.game_screen)
                    chess_pos = round_to_position(mouse_pos)
                    if self.selected_piece is not None and chess_pos in self.available_positions:
                        self.move_seleceted_piece(chess_pos)
                        self.new_turn()
                    else:
                        piece = self.get_piece(chess_pos)
                        if piece is not None and piece.isWhite is self.is_white_turn:
                            self.selected_piece = piece
                            self.available_positions = self.selected_piece.can_move_to(self.whites, self.blacks)

                    pygame.time.wait(250)

                self.draw()

                pygame.display.update()
                self.clock.tick(60)

            if self.gameover and self.game_loop:
                self.display_gameover()
                self.display_new_game()

            while self.gameover and not self.stop:
                self.draw()
                pygame.display.update()
                self.clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_loop = False
                        self.stop = True

                if self.is_mouseover_new_game(self.get_screen_adjusted_mouse_pos(self.game_screen)):
                    click = pygame.mouse.get_pressed()
                    if click[0] is True:
                        self.init_new_game()


if __name__ == '__main__':
    a = Display()
    a.run()
