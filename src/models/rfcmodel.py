from sklearn.ensemble import RandomForestClassifier
from src.models.basemodel import BaseModel
import optuna


class RFCModel(BaseModel):

    def __init__(self, df, params):
        super().__init__(df, params)

    def build(self):
        model = RandomForestClassifier(n_estimators=self.params['n_estimators'],
                                       criterion=self.params['criterion'],
                                       max_depth=self.params['max_depth'],
                                       min_samples_split=self.params['min_samples_split'],
                                       min_samples_leaf=self.params['min_samples_leaf'],
                                       min_weight_fraction_leaf=self.params['min_weight_fraction_leaf'],
                                       max_features=self.params['max_features'],
                                       max_leaf_nodes=self.params['max_leaf_nodes'],
                                       min_impurity_decrease=self.params['min_impurity_decrease'],
                                       min_impurity_split=self.params['min_impurity_split'],
                                       bootstrap=self.params['bootstrap'],
                                       oob_score=self.params['oob_score'],
                                       n_jobs=self.params['n_jobs'],
                                       random_state=self.params['random_state'],
                                       verbose=self.params['verbose'],
                                       warm_start=self.params['warm_start'],
                                       class_weight=self.params['class_weight'],
                                       ccp_alpha=self.params['ccp_alpha'],
                                       max_samples=self.params['max_samples'])
        return model

    def set_optimization_params(self):
        params = {}
        params['n_estimators'] = optuna.distributions.IntUniformDistribution(low=1, high=300)
        params['min_samples_split'] = optuna.distributions.UniformDistribution(low=0.001, high=1.0)
        params['min_samples_leaf'] = optuna.distributions.IntUniformDistribution(low=1, high=10)
        params['min_weight_fraction_leaf'] = optuna.distributions.UniformDistribution(low=0.0, high=0.5)
        return params
