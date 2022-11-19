"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""
import pygame as p
import ChessEngine, ChessAI
import sys
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    #print(game_state) # Julio , first game_state
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = True  # if a hyman is playing white, then this will be True, else False --- Changed to True from False,
    m = 1
    q = 0
    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        #print(move) # Julio adding print 
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = []
                                f = open('/home/piche-traful/code/Chessinterface3/chess-engine-master/chess/movedpieces2.pgn','a') # Julio adding code to save to a file
                                if q == 0:
                                    f.write(str(m)+'. ')
                                    f.write(str(move.getChessNotation()+' ')) # Julio
                                    q += 1
                                else:
                                    #f.write(str(m)+'. ')
                                    f.write(str(move.getChessNotation()+' ')) # Julio
                                    #f.close() # Julio
                                    q = 0
                                    #f.close() # Julio
                                #f.write(str(m)+'. ' )
                                #f.write(str(move.getChessNotation())+' ') # Julio
                                #f.close() # Julio
                                
                                print(move.getChessNotation()) #Julio adding print---- Better print out
                                #print('hello')
                                m = (m + 1 - q)
                                f.close()   
                                
                        if not move_made:
                            player_clicks = [square_selected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    # print('Hello valid_moves') # Julio adding print
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    #f = open('/home/piche-traful/code/pgnToFen-master/movedpieces2.pgn','a') # Julio adding code to save to a file
                    #f.write(str(move.getChessNotation())) # Julio
                    #f.close() # Julio
                    #print(move.getChessNotation()) #Julio adding print---- Better print out
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                # need to to read PGN/FEN call to the Online Model, then extract the start/end position and padd to the Process down below
                #  ********
                start_position = (1,4) #start_position_tuple
                print(type(start_position))
                end_position = (3, 4) # end_position_tuple
                valid_moves2 = []
                valid_moves2.append(ChessEngine.Move(start_position, end_position, game_state.board))
                print("hello Neal") # Neal adding print
                print(valid_moves2) # Neal adding print
                print("hello Neal2") # Neal adding print
                #start_position = (1,0)
                #end_position = (2, 0)
                #valid_moves2.append(ChessEngine.Move(start_position, end_position, game_state.board))
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves2, return_queue)) # original line, changing valid_move to valid_moves2
                #valid_moves3 = []
                #start_position = (1,0)
                #end_position = (2, 0)
                #valid_moves2.append(ChessEngine.Move(start_position2, end_position2, game_state.board))
                # move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves2, return_queue))
                #  *****
                # print(move_finder_process) -- Julio adding print
                #move_finder_process = a3 #Process(target=ChessAI.findBestMove) #, args=(game_state, valid_moves, return_queue)) # julio modifying line
                #print(valid_moves) # Julio addding print
                move_finder_process.start()
                print(valid_moves) # Julio adding print
                print(game_state) # --- Julio adding print
                print(return_queue) # --- Julio adding print

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = ChessAI.findRandomMove(valid_moves2) #changing from valid_moves to valid_moves2 -- Julio/Nour
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                # print(game_state.move_log[-1]) # Julio adding print
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            print('Hello valid moves on AI') # Julio adding print
            # print(valid_moves) # -- Juio adding print
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if not game_over:
            #next_best_move = 'Hello Julio'
            infile = open("hello_test.pgn",'r')
            next_best_move = (infile.read())
            infile.close()
            drawMoveLog(screen, game_state, move_log_font, next_best_move)
        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                

def drawMoveLog(screen, game_state, font, next_best_move):
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    #print(str(move_log)) # Julio adding print
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)
        move_texts.append(next_best_move + ' ')
        

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]
        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
