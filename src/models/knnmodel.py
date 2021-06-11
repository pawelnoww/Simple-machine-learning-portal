from sklearn.neighbors import KNeighborsClassifier
from src.models.basemodel import BaseModel


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
        self.model = model
