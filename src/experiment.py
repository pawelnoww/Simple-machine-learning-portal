from src.data.dataframe import DataFrame

class Experiment:

    def __init__(self, df_path):
        self.df = DataFrame(df_path)

    def scale_data(self):
        self.df.scale_data()

    def train(self):
        print("Tu bedzie trenowane")
