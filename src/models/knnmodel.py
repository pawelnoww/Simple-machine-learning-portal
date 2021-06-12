from sklearn.neighbors import KNeighborsClassifier
from src.models.basemodel import BaseModel
import optuna


class KNNModel(BaseModel):

    def __init__(self, df, params):
        super().__init__(df, params)

    def build(self):
        model = KNeighborsClassifier(n_neighbors=self.params['n_neighbors'],
                                     weights=self.params['weights'],
                                     algorithm=self.params['algorithm'],
                                     leaf_size=self.params['leaf_size'],
                                     p=self.params['p'],
                                     metric=self.params['metric'],
                                     metric_params=self.params['metric_params'],
                                     n_jobs=self.params['n_jobs'])
        return model

    def set_optimization_params(self):
        params = {}
        n_rows_train = len(self.df.X_train)
        params['n_neighbors'] = optuna.distributions.IntUniformDistribution(low=1, high=min(n_rows_train//4, 200))
        params['weights'] = optuna.distributions.CategoricalDistribution(['uniform', 'distance'])
        params['algorithm'] = optuna.distributions.CategoricalDistribution(['auto', 'ball_tree', 'kd_tree', 'brute'])
        params['leaf_size'] = optuna.distributions.IntUniformDistribution(low=1, high=150)
        return params
