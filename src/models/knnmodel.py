from sklearn.neighbors import KNeighborsClassifier
from src.models.basemodel import BaseModel


class KNNModel(BaseModel):

    def __init__(self, df):
        super().__init__(df)

    def build(self):
        model = KNeighborsClassifier()
        self.model = model
