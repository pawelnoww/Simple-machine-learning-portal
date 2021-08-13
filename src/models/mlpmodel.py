from sklearn.neural_network import MLPClassifier
from src.models.basemodel import BaseModel
import optuna

class MLPModel(BaseModel):

    def __init__(self, df, params):
        super().__init__(df, params)

    def build(self):
        if type(self.params['hidden_layer_sizes']) is not tuple:
            self.params['hidden_layer_sizes'] = eval(self.params['hidden_layer_sizes'])

        model = MLPClassifier(hidden_layer_sizes=self.params['hidden_layer_sizes'],
                              activation=self.params['activation'],
                              solver=self.params['solver'],
                              alpha=self.params['alpha'],
                              batch_size=self.params['batch_size'],
                              learning_rate=self.params['learning_rate'],
                              learning_rate_init=self.params['learning_rate_init'],
                              power_t=self.params['power_t'],
                              max_iter=self.params['max_iter'],
                              shuffle=self.params['shuffle'],
                              random_state=self.params['random_state'],
                              tol=self.params['tol'],
                              verbose=self.params['verbose'],
                              nesterovs_momentum=self.params['nesterovs_momentum'],
                              early_stopping=self.params['early_stopping'],
                              validation_fraction=self.params['validation_fraction'],
                              beta_1=self.params['beta_1'],
                              beta_2=self.params['beta_2'],
                              epsilon=self.params['epsilon'],
                              n_iter_no_change=self.params['n_iter_no_change'],
                              max_fun=self.params['max_fun'])
        return model

    def set_optimization_params(self):
        params = {}
        params['hidden_layer_sizes'] = optuna.distributions.CategoricalDistribution(
            [(8,), (16,), (32,), (64,), (128,), (256,),                                                # 1 hidden layer
             (8, 4,), (16, 8,), (32, 16,), (64, 32,), (128, 64,), (256, 128,),                         # 2 hidden layers
             (8, 4, 2,), (16, 8, 4,), (32, 16, 8,), (64, 32, 16,), (128, 64, 32,), (256, 128, 64,),    # 3 hidden layers
             (128, 64, 32, 16), (256, 128, 64, 32)])                                                   # 4 hidden layers
        return params
