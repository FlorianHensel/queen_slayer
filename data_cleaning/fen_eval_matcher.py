import pandas as pd
import numpy as np

class DatasetCreator():
    '''
    Takes list of fens and list of evals to return a combined dataset.
    '''

    def match_fen_to_eval(self, fens, evals):
        '''
        Matches FEN with corresponding eval.
        '''

        print("-------------------\nFEN EVAL MATCHER\n-------------------\nClearing previous games.\nMatching...")
        self.evaluated_positions = []

        game_counter = 1

        for game in fens.items():
            fen_counter = 0

            # COMBINE EACH FEN AND THEIR CORRESPONDING EVAL
            for fen in game[1]:
                evaluated_position = fen

                # IF EVAL AVAILABLE APPEND IT TO OBSERVATION
                try:
                    evaluated_position.append(evals[f'game_{game_counter}'][fen_counter])

                # IF NO EVAL AVAILABLE APPEND NAN
                except Exception as e:
                    evaluated_position.append(np.nan)

                self.evaluated_positions.append(evaluated_position)

                fen_counter += 1
            game_counter += 1


    def create_dataset(self, dropna=True, drop_duplicates=True) -> pd.DataFrame:
        '''
        Returns Pandas DataFrame from matched data.\n
        Dropna to return df excluding games with no evals.\n
        Drop duplicates for unique positions.
        '''

        print('Creating dataset.')
        # GET NUMBER OF FEATURES BASED ON FEN ENCODING
        feature_count = max([len(i) for i in self.evaluated_positions])
        columns = [f"feat_{i}" for i in range(1, feature_count - 2)]

        # QUEEN CAPTURE MOVES ALWAYS RECORDED IN FIRST COLUMN
        columns.insert(0, 'QCM')
        # SIDE TO PLAY ALWAYS RECORDED IN SECOND COLUMN
        columns.insert(1, 'side_to_play')
        # EVALS ALWAYS RECORDED ON LAST COLUMN
        columns.append('eval')

        df = pd.DataFrame(self.evaluated_positions, columns=columns)
        df.dropna(inplace=dropna)
        df.drop_duplicates(inplace=drop_duplicates)

        self.dataset = df
        return df


    def amplify_queen_capture_positions(self,
                                        amplifiers,
                                        amplifier_type=str,
                                        keep_qcm=False,
                                        evals_cap=[-15, 15]) -> pd.DataFrame:
        '''
        Imbalances dataset for queen capture positions.\n
        Amplifier types: addition, multiplication.\n
        Set Keep queen capture moves (keep_qcm)
        to true to keep labeling in df.\n
        '''

        print('Amplifying queen capture positions.')

        try:
            if amplifier_type == 'addition':
                amplified_df = self.dataset
                # IF POSITION IS QCP AND NOT CHECKMATE, AMPLIFY EVAL
                amplified_df['eval'] = amplified_df.apply(lambda x: x['eval'] +
                                                        amplifiers['main'] *
                                                        x['side_to_play']
                                                        if x['QCM'] is True
                                                        and x['eval'] is float
                                                        else x['eval'], axis=1)

            if amplifier_type == 'multiplication':
                amplified_df = self.dataset
                # IF POSITION IS QCP AND NOT CHECKMATE, AMPLIFY EVAL
                amplified_df['eval'] = amplified_df.apply(lambda x: x['eval'] *
                                                        amplifiers['main'] *
                                                        x['side_to_play']
                                                        if x['QCM'] is True
                                                        and x['eval'] is float
                                                        else x['eval'], axis=1)
        except:
            pass

        # AMPLIFY INDIRECT QUEEN CAPTURE POSITIONS
        secondary_amplifiers = [i for i in amplifiers.keys() if i != 'main']
        for amplifier in secondary_amplifiers:
            try:
                if amplifier_type == 'addition':
                    amplified_df = self.dataset
                    # IF POSITION IS QCP AND NOT CHECKMATE, AMPLIFY EVAL
                    amplified_df['eval'] = amplified_df.apply(lambda x: x['eval'] +
                                                            amplifiers[amplifier] *
                                                            x['side_to_play']
                                                            if int(x['QCM']) is int(amplifier)
                                                            and x['eval'] is float
                                                            else x['eval'], axis=1)

                if amplifier_type == 'multiplication':
                    amplified_df = self.dataset
                    # IF POSITION IS QCP AND NOT CHECKMATE, AMPLIFY EVAL
                    amplified_df['eval'] = amplified_df.apply(lambda x: x['eval'] *
                                                            amplifiers[amplifier] *
                                                            x['side_to_play']
                                                            if int(x['QCM']) is int(amplifier)
                                                            and x['eval'] is float
                                                            else x['eval'], axis=1)
            except:
                pass

        if keep_qcm == False:
            amplified_df.drop(columns=['QCM'], inplace=True)

        # CAP EVALUATIONS BETWEEN -15 and +15
        low = evals_cap[0]
        high = evals_cap[1]

        amplified_df['eval'].where(amplified_df['eval'] < low, low)
        amplified_df['eval'].where(amplified_df['eval'] > high, high)

        self.dataset = amplified_df
        return amplified_df
