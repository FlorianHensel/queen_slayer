import pandas as pd

class FEN_Eval_Matcher():
    '''
    Converter that takes .pgn and converts it into FEN.
    '''
    def __init__(self, fens, evals) -> None:
        self.fens = fens
        self.evals = evals
        self.evaluated_positions = []


    def match_fen_to_eval(self):
        '''
        Reads pgn file and creates FENs for each position in a game.\n
        Stored in self.games
        Each run will reset prior games.
        '''

        print("-------------------\nFEN EVAL MATCHER\n-------------------\nClearing previous games.\nMatching...")

        self.evaluated_positions = []
        game_counter = 1
        eval_counter = 0

        for game in self.fens.items():
            for fen in game[1]:
                evaluated_position = fen
                evaluated_position.append(self.evals[eval_counter])
                self.evaluated_positions.append(evaluated_position)
                eval_counter += 1
            game_counter += 1

        print(f"Done.\n")


    def create_dataset(self):
        '''
        Returns Pandas DataFrame from matched data.
        '''
        feature_count = max([len(i) for i in self.evaluated_positions])
        columns = [f"feat_{i}" for i in range(1, feature_count)]
        columns.append('eval')
        df = pd.DataFrame(self.evaluated_positions, columns=columns)
        return df
