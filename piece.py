def is_enemy_in_pos(pos, enemies, friends):
    for piece in enemies:
        if piece.pos == pos:
            return piece
    for piece in friends:
        if piece.pos == pos:
            return False
    return None


class Piece:

    def __init__(self, type, pos, isWhite, img):
        self.type = type
        self.pos = pos
        self.isWhite = isWhite
        self.img = img

        self.first_move = True if type == 'pawn' else False
        self.en_passant = False

    def __eq__(self, other):
        return self.pos == other.pos

    def move_to(self, pos):
        if self.type == 'pawn':
            if self.en_passant is True:
                self.en_passant = False

            if self.first_move is True:
                if abs(pos[0] - self.pos[0]) == 2:
                    self.en_passant = True
                self.first_move = False

        self.pos = pos

    def can_move_to(self, whites, blacks):
        if self.type is None:
            return None

        enemies = blacks if self.isWhite else whites
        friends = whites if self.isWhite else blacks

        if (self.type == 'pawn'):
            return self.pawn_can_move_to(enemies, friends)
        elif (self.type == 'bishop'):
            return self.bishop_can_move_to(enemies, friends)
        elif (self.type == 'knight'):
            return self.knight_can_move_to(enemies, friends)
        elif (self.type == 'rook'):
            return self.rook_can_move_to(enemies, friends)
        elif (self.type == 'queen'):
            return self.queen_can_move_to(enemies, friends)
        elif (self.type == 'king'):
            return self.king_can_move_to(enemies, friends)

    def pawn_can_move_to(self, enemies, friends):
        positions = []
        dir = 1 if self.isWhite is True else -1

        if (self.pos[0] + dir <= 7 or self.pos[0] + dir >= 0):
            enemy = is_enemy_in_pos((self.pos[0] + dir, self.pos[1]), enemies, friends)
            if enemy is None:
                positions.append((self.pos[0] + dir, self.pos[1]))
                if self.first_move:
                    if is_enemy_in_pos((self.pos[0] + (dir * 2), self.pos[1]), enemies, friends) is None:
                        positions.append((self.pos[0] + (dir * 2), self.pos[1]))
            if (self.pos[1] - 1 >= 0):
                enemy = is_enemy_in_pos((self.pos[0], self.pos[1] - 1), enemies, friends)
                en_passant_possible = isinstance(enemy, Piece) and enemy.en_passant
                if isinstance(is_enemy_in_pos((self.pos[0] + dir, self.pos[1] - 1), enemies, friends), Piece) is True or en_passant_possible:
                    positions.append((self.pos[0] + dir, self.pos[1] - 1))
            if (self.pos[1] + 1 <= 7):
                enemy = is_enemy_in_pos((self.pos[0], self.pos[1] + 1), enemies, friends)
                en_passant_possible = isinstance(enemy, Piece) and enemy.en_passant
                if isinstance(is_enemy_in_pos((self.pos[0] + dir, self.pos[1] + 1), enemies, friends), Piece) is True or en_passant_possible:
                    positions.append((self.pos[0] + dir, self.pos[1] + 1))
        return positions

    def bishop_can_move_to(self, enemies, friends):
        positions = []

        minPos = min(self.pos[0], self.pos[1])
        maxPos = max(self.pos[0], self.pos[1])

        diagonally_top_left = []
        diagonally_bottom_right = []
        diagonally_bottom_left = []
        diagonally_top_right = []

        # diagonally towards bottom right
        piece_pos = (self.pos[0] - minPos, self.pos[1] - minPos)

        for pos in range(0, 8 - (maxPos - minPos)):
            enemy = is_enemy_in_pos(piece_pos, enemies, friends)
            if piece_pos[0] < self.pos[0]:
                if enemy is not None:
                    diagonally_top_left = []
                if enemy is not False:
                    diagonally_top_left.append(piece_pos)
            elif piece_pos[0] > self.pos[0]:
                if enemy is not False:
                    diagonally_bottom_right.append(piece_pos)
                if enemy is not None:
                    break
            piece_pos = (piece_pos[0] + 1, piece_pos[1] + 1)

        positions.extend(diagonally_top_left)
        positions.extend(diagonally_bottom_right)

        # diagonally towards top right
        y = 7 if (self.pos[0] + self.pos[1]) >= 7 else (self.pos[0] + self.pos[1])
        x = 0 if (self.pos[0] + self.pos[1]) <= 7 else (self.pos[0] + self.pos[1]) % 7

        piece_pos = (y, x)
        for pos in range(0, (y + 1) - x):
            enemy = is_enemy_in_pos(piece_pos, enemies, friends)
            if piece_pos[0] > self.pos[0]:
                if enemy is not None:
                    print(piece_pos)
                    diagonally_bottom_left = []
                if enemy is not False:
                    diagonally_bottom_left.append(piece_pos)
            elif piece_pos[0] < self.pos[0]:
                if enemy is not False:
                    diagonally_top_right.append(piece_pos)
                if enemy is not None:
                    break
            piece_pos = (piece_pos[0] - 1, piece_pos[1] + 1)

        positions.extend(diagonally_bottom_left)
        positions.extend(diagonally_top_right)

        return positions

    def knight_can_move_to(self, enemies, friends):
        positions = []

        def append_if_not_false(pos, enemies, friends):
            enemy = is_enemy_in_pos(pos, enemies, friends)
            if enemy is not False:
                positions.append(pos)

        if (self.pos[1] - 2 >= 0):
            if (self.pos[0] - 1 >= 0):
                append_if_not_false((self.pos[0] - 1, self.pos[1] - 2), enemies, friends)
            if (self.pos[0] + 1 <= 7):
                append_if_not_false((self.pos[0] + 1, self.pos[1] - 2), enemies, friends)
        if (self.pos[1] - 1 >= 0):
            if (self.pos[0] - 2 >= 0):
                append_if_not_false((self.pos[0] - 2, self.pos[1] - 1), enemies, friends)
            if (self.pos[0] + 2 <= 7):
                append_if_not_false((self.pos[0] + 2, self.pos[1] - 1), enemies, friends)
        if (self.pos[1] + 1 <= 7):
            if (self.pos[0] - 2 >= 0):
                append_if_not_false((self.pos[0] - 2, self.pos[1] + 1), enemies, friends)
            if (self.pos[0] + 2 <= 7):
                append_if_not_false((self.pos[0] + 2, self.pos[1] + 1), enemies, friends)
        if (self.pos[1] + 2 <= 7):
            if (self.pos[0] - 1 >= 0):
                append_if_not_false((self.pos[0] - 1, self.pos[1] + 2), enemies, friends)
            if (self.pos[0] + 1 <= 7):
                append_if_not_false((self.pos[0] + 1, self.pos[1] + 2), enemies, friends)

        return positions

    def rook_can_move_to(self, enemies, friends):
        positions = []

        left = []
        right = []
        up = []
        down = []

        # left
        for index in range(0, self.pos[1]):
            enemy = is_enemy_in_pos((self.pos[0], index), enemies, friends)
            if enemy is not None:
                left = []
            if enemy is not False:
                left.append((self.pos[0], index))
        # right
        for index in range(self.pos[1] + 1, 8):
            enemy = is_enemy_in_pos((self.pos[0], index), enemies, friends)
            if enemy is not False:
                right.append((self.pos[0], index))
            if enemy is not None:
                break
        # up
        for index in range(0, self.pos[0]):
            enemy = is_enemy_in_pos((index, self.pos[1]), enemies, friends)
            if enemy is not None:
                up = []
            if enemy is not False:
                up.append((index, self.pos[1]))
        # down
        for index in range(self.pos[0] + 1, 8):
            enemy = is_enemy_in_pos((index, self.pos[1]), enemies, friends)
            if enemy is not False:
                down.append((index, self.pos[1]))
            if enemy is not None:
                break

        positions.extend(left)
        positions.extend(right)
        positions.extend(up)
        positions.extend(down)

        return positions

    def queen_can_move_to(self, enemies, friends):
        positions = []

        positions.extend(self.bishop_can_move_to(enemies, friends))
        positions.extend(self.rook_can_move_to(enemies, friends))

        return positions

    def king_can_move_to(self, enemies, friends):
        positions = []

        def append_if_not_false(pos, enemies, friends):
            enemy = is_enemy_in_pos(pos, enemies, friends)
            if enemy is not False:
                positions.append(pos)

        # y positions above
        if (self.pos[0] - 1 >= 0):
            append_if_not_false((self.pos[0] - 1, self.pos[1]), enemies, friends)
            if (self.pos[1] - 1 >= 0):
                append_if_not_false((self.pos[0] - 1, self.pos[1] - 1), enemies, friends)
            if (self.pos[1] + 1 <= 7):
                append_if_not_false((self.pos[0] - 1, self.pos[1] + 1), enemies, friends)
        # y positions below
        if (self.pos[0] + 1 <= 7):
            append_if_not_false((self.pos[0] + 1, self.pos[1]), enemies, friends)
            if (self.pos[1] - 1 >= 0):
                append_if_not_false((self.pos[0] + 1, self.pos[1] - 1), enemies, friends)
            if (self.pos[1] + 1 <= 7):
                append_if_not_false((self.pos[0] + 1, self.pos[1] + 1), enemies, friends)
        # x position to the left
        if (self.pos[1] - 1 >= 0):
            append_if_not_false((self.pos[0], self.pos[1] - 1), enemies, friends)
        # x position to the right
        if (self.pos[1] + 1 <= 7):
            append_if_not_false((self.pos[0], self.pos[1] + 1), enemies, friends)

        return positions
