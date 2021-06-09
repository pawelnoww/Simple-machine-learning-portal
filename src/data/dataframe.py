import pandas as pd

class DataFrame:

    def __init__(self, df_path):
        self.df = pd.read_csv(df_path)
        self.df_scaled = None

    def scale_data(self):
        print("Hi tu bedzie skalowane")
