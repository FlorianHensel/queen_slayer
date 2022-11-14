import chess
from engine_handler.engine_handler import EngineHandler

class GameHandler(EngineHandler):
    '''
    Takes care of game flow.\n
    Communicates with EngineHandler to get AI's move.
    '''
    def __init__(self, board) -> None:
        super().__init__(board)
        self.board = chess.Board()


    def start_game():
        pass



if __name__ == '__main__':
    GameHandler().start_game()
