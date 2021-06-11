import optuna
import yaml
#from src.app import UserExperiment
from src.utils.configutils import load_config
from flask_login import current_user


class BaseModel:

    def __init__(self, df, params):
        self.df = df
        self.params = params
        self.model = None
        self.optimization_params = None

    def train(self):
        self.model = self.build()
        self.model.fit(X=self.df.X_train, y=self.df.y_train)

    def build(self):
        raise NotImplementedError("build() function is not implemented")

    def set_optimization_params(self):
        raise NotImplementedError("set_optimization_params() function is not implemented")

    def predict(self, X):
        return self.model.predict(X)

    def optimize(self):
        temp_model = self.build()
        optimization_params = self.set_optimization_params()
        clf = optuna.integration.OptunaSearchCV(temp_model,
                                                optimization_params,
                                                n_trials=self.params['max_optimization_iterations'],
                                                timeout=self.params['optimization_time_in_seconds'])
        best_model = clf.fit(X=self.df.X_train, y=self.df.y_train)
        best_params = best_model.best_estimator_.get_params()

        for param in best_params:
            self.params[param] = best_params[param]
