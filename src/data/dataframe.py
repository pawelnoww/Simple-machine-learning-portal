import copy

import pandas as pd


class DataFrame:

    def __init__(self, df_path):
        self.df = pd.read_csv(df_path)
        self.df_scaled = None
        self.scaling_rates = None

    def scale_data(self):
        scaling_rates = []
        df_scaled = copy.deepcopy(self.df)

        for column in df_scaled.columns:
            scaling_rate = max(df_scaled[column])
            df_scaled[column] /= scaling_rate
            scaling_rates.append(scaling_rate)

        self.scaling_rates = scaling_rates
        self.df_scaled = df_scaled
