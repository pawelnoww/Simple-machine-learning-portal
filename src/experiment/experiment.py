import copy
import pandas as pd
from src.data.dataframe import DataFrame
from src.models.knnmodel import KNNModel
from src.models.rfcmodel import RFCModel
from src.utils.scoreutils import accuracy


class Experiment:

    def __init__(self, df_path, config):
        self.config = config
        self.df = DataFrame(df_path, config['dataframe'])
        self.model = None

    def preprocess_data(self):
        self.df.preprocess()

    def set_model(self):
        return eval(self.config['experiment']['model'])

    def train(self):
        model_class = self.set_model()
        cfg_model_name = model_class.__name__.lower()
        model = model_class(self.df, params=self.config[cfg_model_name])
        model.train()
        self.model = model

    def evaluate(self):
        y_pred = self.model.predict(self.df.X_test)
        y_true = self.df.y_test
        self.score = accuracy(y_true, y_pred)

        columns = self.df.df_scaled.columns
        target_col_name = columns[-1]
        df_with_predictions = pd.DataFrame()
        for i in range(len(columns) - 1):
            df_with_predictions[columns[i]] = self.df.X_test.iloc[:, i] * self.df.scaling_rates[i]

            if columns[i] in self.df.encoders.keys():
                encoder = self.df.encoders[columns[i]]
                df_with_predictions[columns[i]] = encoder.inverse_transform(df_with_predictions[columns[i]].astype('int64'))

        df_with_predictions[f'{target_col_name}_true'] = y_true
        df_with_predictions[f'{target_col_name}_pred'] = y_pred
        self.df_with_predictions = df_with_predictions

