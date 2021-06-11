import copy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from src.utils.solutionutils import get_solution_dir


class DataFrame:

    def __init__(self, df_path, params):
        self.params = params
        self.df = pd.read_csv(df_path)
        self.df_scaled = None
        self.scaling_rates = None
        self.target_column = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.encoders = {}

    def preprocess(self):
        transformed_df = self.transform_data()
        self.scale_data(transformed_df)
        self.X_train, self.X_test, self.Y_train, self.Y_test = self.split_data()


    def scale_data(self, df):
        scaling_rates = []
        df_scaled = copy.deepcopy(df)

        for column in df_scaled.columns:
            scaling_rate = max(df_scaled[column])
            df_scaled[column] /= scaling_rate
            scaling_rates.append(scaling_rate)

        self.scaling_rates = scaling_rates
        self.df_scaled = df_scaled

    def split_data(self):
        X = self.df_scaled.iloc[:, :-1]
        y = self.df_scaled.iloc[:, -1]
        return train_test_split(X, y, train_size=self.params['train_size'], shuffle=self.params['shuffle'])

    def transform_data(self):
        transformed_df = copy.deepcopy(self.df)
        for column in transformed_df.columns:
            type = transformed_df[column].dtype
            if type == 'int64' or type == 'float64':
                pass
            elif type == 'bool':
                transformed_df[column] = transformed_df[column].astype('int64')
            elif type == 'object':
                encoder = LabelEncoder()
                transformed_df[column] = encoder.fit_transform(transformed_df[column])
                self.encoders[column] = encoder
            elif type == 'datetime64' or type == 'timedelta[ns]':
                transformed_df.drop([column], axis=1, inplace=True)
                print(f'WARNING ::: type "{type}" is not supported. Column {column} has been dropped.')

        return transformed_df
        # TODO handling category??
