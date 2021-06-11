from src.data.dataframe import DataFrame


class Experiment:

    def __init__(self, df_path, config):
        self.config = config
        self.df = DataFrame(df_path, config['dataframe'])

    def preprocess_data(self):
        self.df.preprocess()

    def train(self):
        print("Tu bedzie trenowane")
