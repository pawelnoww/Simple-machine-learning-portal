
class BaseModel:

    def __init__(self, df, params):
        self.df = df
        self.params = params
        self.model = None

    def train(self):
        self.build()
        self.model.fit(X=self.df.X_train, y=self.df.y_train)

    def build(self):
        raise NotImplementedError("build() function is not implemented")

    def predict(self, X):
        return self.model.predict(X)
