from src.data.dataframe import DataFrame

class Experiment:

    def __init__(self, df_path):
        self.df = DataFrame(df_path)

    def train(self):
        print("Tu bedzie trenowane")
