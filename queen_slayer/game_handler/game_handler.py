import chess
from engine_handler.engine_handler import EngineHandler

class GameHandler(EngineHandler):
    '''
    Takes care of game flow.\n
    Communicates with EngineHandler to get AI's move.
    '''
    def __init__(self, model) -> None:
        super().__init__(model)
        self.board = chess.Board()


    def start_game(self):
        pass



if __name__ == '__main__':
    GameHandler(model='model').start_game()
