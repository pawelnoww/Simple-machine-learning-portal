from sklearn.svm import SVC
from src.models.basemodel import BaseModel
import optuna


class SVCModel(BaseModel):

    def __init__(self, df, params):
        super().__init__(df, params)

    def build(self):
        model = SVC(C=self.params['C'],
                    kernel=self.params['kernel'],
                    degree=self.params['degree'],
                    gamma=self.params['gamma'],
                    coef0=self.params['coef0'],
                    shrinking=self.params['shrinking'],
                    probability=self.params['probability'],
                    tol=self.params['tol'],
                    cache_size=self.params['cache_size'],
                    verbose=self.params['verbose'],
                    max_iter=self.params['max_iter'],
                    decision_function_shape=self.params['decision_function_shape'],
                    break_ties=self.params['break_ties'],
                    random_state=self.params['random_state'])
        return model

    def set_optimization_params(self):
        params = {}
        params['C'] = optuna.distributions.UniformDistribution(low=0.9, high=1.0)
        params['kernel'] = optuna.distributions.CategoricalDistribution(['poly', 'rbf'])
        params['gamma'] = optuna.distributions.CategoricalDistribution(['scale', 'auto'])
        params['tol'] = optuna.distributions.UniformDistribution(low=0.0005, high=0.002)
        params['cache_size'] = optuna.distributions.UniformDistribution(low=100.0, high=500.0)
        params['coef0'] = optuna.distributions.UniformDistribution(low=0.0, high=0.1)
        return params
