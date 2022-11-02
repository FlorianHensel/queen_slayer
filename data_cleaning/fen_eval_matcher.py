import pandas as pd
import numpy as np

class FEN_Eval_Matcher():
    '''
    Takes list of fens and list of evals to return a combined dataset.
    '''
    def __init__(self, fens, evals) -> None:
        self.fens = fens
        self.evals = evals

    def match_fen_to_eval(self):
        '''
        Matches FEN with corresponding eval.
        '''

        print("-------------------\nFEN EVAL MATCHER\n-------------------\nClearing previous games.\nMatching...")
        self.evaluated_positions = []

        game_counter = 1

        for game in self.fens.items():
            fen_counter = 0

            # COMBINE EACH FEN AND THEIR CORRESPONDING EVAL
            for fen in game[1]:
                evaluated_position = fen

                # IF EVAL AVAILABLE APPEND IT TO OBSERVATION
                try:
                    evaluated_position.append(self.evals[f'game_{game_counter}'][fen_counter])

                # IF NO EVAL AVAILABLE APPEND NAN
                except Exception as e:
                    evaluated_position.append(np.nan)

                self.evaluated_positions.append(evaluated_position)

                fen_counter += 1
            game_counter += 1

        print(f"Done.\n")


    def create_dataset(self):
        '''
        Returns Pandas DataFrame from matched data.
        Excludes games without evals.
        '''
        feature_count = max([len(i) for i in self.evaluated_positions])
        columns = [f"feat_{i}" for i in range(1, feature_count)]
        columns.append('eval')
        df = pd.DataFrame(self.evaluated_positions, columns=columns)
        df.dropna(inplace=True)
        return df
