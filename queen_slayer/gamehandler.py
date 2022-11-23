import pygame
import sys
import chess
from engine_handler import EngineHandler

engine_handler = EngineHandler('model/model3.json', 'model/model3.h5')
gamestate = chess.Board()
board = [['  ' for i in range(8)] for i in range(8)]

class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image


bp = Piece('b', 'p', 'images/bp.png')
wp = Piece('w', 'p', 'images/wp.png')
bk = Piece('b', 'k', 'images/bK.png')
wk = Piece('w', 'k', 'images/wK.png')
br = Piece('b', 'r', 'images/bR.png')
wr = Piece('w', 'r', 'images/wR.png')
bb = Piece('b', 'b', 'images/bB.png')
wb = Piece('w', 'b', 'images/wB.png')
bq = Piece('b', 'q', 'images/bQ.png')
wq = Piece('w', 'q', 'images/wQ.png')
bkn = Piece('b', 'kn', 'images/bN.png')
wkn = Piece('w', 'kn', 'images/wN.png')


starting_order = {(0, 0): pygame.image.load(br.image), (1, 0): pygame.image.load(bkn.image),
                  (2, 0): pygame.image.load(bb.image), (3, 0): pygame.image.load(bq.image),
                  (4, 0): pygame.image.load(bk.image), (5, 0): pygame.image.load(bb.image),
                  (6, 0): pygame.image.load(bkn.image), (7, 0): pygame.image.load(br.image),
                  (0, 1): pygame.image.load(bp.image), (1, 1): pygame.image.load(bp.image),
                  (2, 1): pygame.image.load(bp.image), (3, 1): pygame.image.load(bp.image),
                  (4, 1): pygame.image.load(bp.image), (5, 1): pygame.image.load(bp.image),
                  (6, 1): pygame.image.load(bp.image), (7, 1): pygame.image.load(bp.image),

                  (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                  (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                  (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                  (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                  (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                  (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                  (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                  (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

                  (0, 6): pygame.image.load(wp.image), (1, 6): pygame.image.load(wp.image),
                  (2, 6): pygame.image.load(wp.image), (3, 6): pygame.image.load(wp.image),
                  (4, 6): pygame.image.load(wp.image), (5, 6): pygame.image.load(wp.image),
                  (6, 6): pygame.image.load(wp.image), (7, 6): pygame.image.load(wp.image),
                  (0, 7): pygame.image.load(wr.image), (1, 7): pygame.image.load(wkn.image),
                  (2, 7): pygame.image.load(wb.image), (3, 7): pygame.image.load(wq.image),
                  (4, 7): pygame.image.load(wk.image), (5, 7): pygame.image.load(wb.image),
                  (6, 7): pygame.image.load(wkn.image), (7, 7): pygame.image.load(wr.image),}


def create_board(board):
    board[0] = [Piece('b', 'r', 'b_rook.png'), Piece('b', 'kn', 'b_knight.png'), Piece('b', 'b', 'b_bishop.png'), \
               Piece('b', 'q', 'b_queen.png'), Piece('b', 'k', 'b_king.png'), Piece('b', 'b', 'b_bishop.png'), \
               Piece('b', 'kn', 'b_knight.png'), Piece('b', 'r', 'b_rook.png')]

    board[7] = [Piece('w', 'r', 'w_rook.png'), Piece('w', 'kn', 'w_knight.png'), Piece('w', 'b', 'w_bishop.png'), \
               Piece('w', 'q', 'w_queen.png'), Piece('w', 'k', 'w_king.png'), Piece('w', 'b', 'w_bishop.png'), \
               Piece('w', 'kn', 'w_knight.png'), Piece('w', 'r', 'w_rook.png')]

    for i in range(8):
        board[1][i] = Piece('b', 'p', 'b_pawn.png')
        board[6][i] = Piece('w', 'p', 'w_pawn.png')
    return board


def on_board(position):
    '''
    Returns the input if the input is within the boundaries of the board.
    '''
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True


def deselect():
    '''
    Resets "x's" and killable pieces.
    '''
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass


def select_moves(index, moves):
    '''
    This takes in a piece object and its index
    then checks where that piece can move using
    separately defined functions for each type of piece.
    '''
    def index_to_uci(index):
        columns = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        rows = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
        return f"{columns[index[1]]}{rows[index[0]]}"


    def uci_to_index(uci):
        columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        rows = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        return rows[uci[1]], columns[uci[0]]


    index_uci = index_to_uci(index)
    legal_moves = [uci_to_index(str(i)[2:4]) for i in list(gamestate.legal_moves) if str(i)[:2] == index_uci]

    def piece_moves(legal_moves):
        team = board[index[0]][index[1]].team
        for move in legal_moves:

            if type(board[move[0]][move[1]]) is not str:
                if board[move[0]][move[1]].team != team:
                    board[move[0]][move[1]].killable = True

            else:
                if board[move[0]][move[1]] == '  ':
                    board[move[0]][move[1]] = 'x '

        return board


    def check_team(moves, index):
        row, col = index
        if moves%2 == 0:
            if board[row][col].team == 'w':
                return True
        else:
            if board[row][col].team == 'b':
                return True


    def highlight(board):
        '''
        Returns 2D array containing positions of valid moves.
        '''
        highlighted = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 'x ':
                    highlighted.append((i, j))
                else:
                    try:
                        if board[i][j].killable:
                            highlighted.append((i, j))
                    except:
                        pass
        return highlighted

    if check_team(moves, index):
        return highlight(piece_moves(legal_moves))


WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, WIDTH))

""" This is creating the window that we are playing on, it takes a tuple argument which is the dimensions of the window so in this case 800 x 800px
"""

pygame.display.set_caption("Chess")
WHITE = (222, 241, 252)
GREY = (69, 128, 163)
YELLOW = (204, 204, 0)
BLUE = (252, 158, 149)
BLACK = (0, 0, 0)


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] == None:
                pass
            else:
                WIN.blit(starting_order[(self.row, self.col)], (self.x, self.y))

        """
        For now it is drawing a rectangle but eventually we are going to need it
        to use blit to draw the chess pieces instead
        """


def make_grid(rows, width):
    """
    This is creating the nodes thats are on the board(so the chess tiles)
    I've put them into a 2d array which is identical to the dimesions of the chessboard
    """
    grid = []
    gap = WIDTH // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY
    return grid


def draw_grid(win, rows, width):
    """
    The nodes are all white so this we need to draw the grey lines that separate all the chess tiles
    from each other and that is what this function does
    """
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)


def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE


def do_move(OriginalPos, FinalPos):
    starting_order[FinalPos] = starting_order[OriginalPos]
    starting_order[OriginalPos] = None


def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid


def move_to_uci(col, row, y, x):
    columns = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    rows = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    return f'{columns[col]}{rows[row]}{columns[y]}{rows[x]}'


def uci_to_move(uci):
    columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    rows = {8: 0, 7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 6, 1: 7}
    return columns[uci[0]], rows[int(uci[1])], columns[uci[2]], rows[int(uci[3])]


create_board(board)

def main(WIN, WIDTH):
    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(8, WIDTH)
    while True:
        pygame.time.delay(50) ##stops cpu dying
        for event in pygame.event.get():
            player_made_move = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """This quits the program if the player closes the window"""

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = Find_Node(pos, WIDTH)
                if selected == False:
                    try:
                        possible = select_moves((x,y), moves)
                        for positions in possible:
                            row, col = positions
                            grid[row][col].colour = BLUE
                        piece_to_move = x, y
                        selected = True
                    except:
                        piece_to_move = []

                else:
                    try:
                        if board[x][y].killable == True:
                            row, col = piece_to_move ## coords of original piece
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)
                            do_move((col, row), (y, x))
                            moves += 1
                            move_uci = move_to_uci(col, row, y, x)
                            gamestate.push_uci(move_uci)

                            # CHECK FOR CASTLING MOVES
                            try:
                                if move_uci == 'e1g1' and board[x][y].type == 'k':
                                    board[7][5] = board[7][7]
                                    board[7][7] = '  '
                                    do_move((7, 7), (5, 7))
                            except:
                                pass

                            try:
                                if move_uci == 'e1c1' and board[x][y].type == 'k':
                                    board[7][3] = board[7][0]
                                    board[7][0] = '  '
                                    do_move((0, 7), (3, 7))
                            except:
                                pass

                            player_made_move = True
                        else:
                            deselect()
                            remove_highlight(grid)
                            selected = False
                    except:
                        if board[x][y] == 'x ':
                            row, col = piece_to_move
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)
                            do_move((col, row), (y, x))
                            moves += 1
                            move_uci = move_to_uci(col, row, y, x)
                            gamestate.push_uci(move_uci)

                            # CHECK FOR CASTLING MOVES
                            try:
                                if move_uci == 'e1g1' and board[x][y].type == 'k':
                                    board[7][5] = board[7][7]
                                    board[7][7] = '  '
                                    do_move((7, 7), (5, 7))
                            except:
                                pass

                            try:
                                if move_uci == 'e1c1' and board[x][y].type == 'k':
                                    board[7][3] = board[7][0]
                                    board[7][0] = '  '
                                    do_move((0, 7), (3, 7))
                            except:
                                pass

                            player_made_move = True
                        else:
                            deselect()
                            remove_highlight(grid)
                            selected = False
                    selected = False

            update_display(WIN, grid, 8, WIDTH)

            # ENGINE MOVE
            if player_made_move:
                best_move, eval = engine_handler.predict_move(board=gamestate,
                                                              move_counter=moves)
                gamestate.push_uci(best_move)
                col, row, y, x = uci_to_move(best_move)
                board[x][y] = board[row][col]
                board[row][col] = '  '
                do_move((col, row), (y, x))
                moves += 1

                # CHECK FOR CASTLING MOVES
                try:
                    if move_uci == 'e8g8' and board[x][y].type == 'k':
                        board[0][5] = board[0][7]
                        board[0][7] = '  '
                        do_move((7, 0), (5, 0))
                except:
                    pass

                try:
                    if move_uci == 'e8c8' and board[x][y].type == 'k':
                        board[0][3] = board[0][0]
                        board[0][0] = '  '
                        do_move((7, 0), (3, 0))
                except:
                    pass

                update_display(WIN, grid, 8, WIDTH)


main(WIN, WIDTH)
