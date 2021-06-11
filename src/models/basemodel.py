
class BaseModel:

    def __init__(self, df):
        self.df = df
        self.model = None

    def train(self):
        self.model.fit(self.df.X_train)

    def build(self):
        raise NotImplementedError("build() function is not implemented")

    def predict(self, X):
        return self.model.predict(X)
