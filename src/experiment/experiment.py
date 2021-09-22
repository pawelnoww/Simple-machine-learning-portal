import pandas as pd
from src.data.dataframe import DataFrame
from src.models.knnmodel import KNNModel
from src.models.rfcmodel import RFCModel
from src.models.svcmodel import SVCModel
from src.models.mlpmodel import MLPModel
from src.utils.scoreutils import accuracy


class Experiment:

    def __init__(self, df_path, config):
        self.config = config
        self.df = DataFrame(df_path, config['dataframe'])
        self.model = None
        self.df_with_predictions = None
        self.auto_ml_scores = None

    def preprocess_data(self):
        self.df.preprocess()

    def get_model(self):
        return eval(self.config['experiment']['model'])

    def set_model(self):
        model_class = self.get_model()
        cfg_model_name = model_class.__name__.lower()
        model = model_class(self.df, params=self.config[cfg_model_name])
        self.model = model

    def train(self):
        if self.model is None:
            self.set_model()

        self.model.train()

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

    def choose_best_model(self):
        models = [KNNModel, SVCModel, RFCModel, MLPModel]
        self.auto_ml_scores = {}

        for model_class in models:
            model_name = model_class.__name__
            self.config['experiment']['model'] = model_name
            self.set_model()
            self.model.optimize()
            self.train()
            self.evaluate()
            self.auto_ml_scores[model_name] = self.score
            self.config[model_name.lower()] = self.model.params

        best_model = max(self.auto_ml_scores, key=self.auto_ml_scores.get)
        self.config['experiment']['model'] = best_model

        self.set_model()
        self.train()
        self.evaluate()

        auto_ml_scores_dict = {}
        auto_ml_scores_dict['model'] = list(self.auto_ml_scores.keys())
        auto_ml_scores_dict['score'] = list(self.auto_ml_scores.values())
        self.auto_ml_scores_df = pd.DataFrame(data=auto_ml_scores_dict)
