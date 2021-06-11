from src.data.dataframe import DataFrame

class Experiment:

    def __init__(self, df_path):
        self.df = DataFrame(df_path)

    def preprocess_data(self):
        self.df.preprocess()

    def train(self):
        print("Tu bedzie trenowane")
