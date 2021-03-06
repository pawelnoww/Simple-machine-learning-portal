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
        self.drop_columns(transformed_df)
        self.scale_data(transformed_df)
        self.X_train, self.X_test, self.y_train, self.y_test = self.split_data()

    def fill_nan_values(self, df):
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)

    def drop_columns(self, df):
        if self.params['drop_columns'] is None:
            return

        cols = self.params['drop_columns'].strip('[').strip(']').strip("'").split(',')
        print(cols)

        df.drop(cols, axis=1, inplace=True)

    def scale_data(self, df):
        scaling_rates = []
        df_scaled = copy.deepcopy(df)

        for column in df_scaled.columns[:-1]:
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
        transformed_df = self.change_column_position()
        self.fill_nan_values(transformed_df)
        for column in transformed_df.columns[:-1]:
            type = transformed_df[column].dtype
            if type == 'int64' or type == 'float64':
                pass
            elif type == 'bool':
                transformed_df[column] = transformed_df[column].astype('int64')
            elif type == 'object':
                # Check n of unique values
                n_unique = transformed_df[column].nunique()
                if n_unique > 10:
                    transformed_df.drop([column], axis=1, inplace=True)
                    print(f'WARNING ::: column {column} has been dropped in case of too many unique values for categorical feature (10 vs {n_unique}).')
                else:
                    encoder = LabelEncoder()
                    transformed_df[column] = encoder.fit_transform(transformed_df[column])
                    self.encoders[column] = encoder
            elif type == 'datetime64' or type == 'timedelta[ns]':
                transformed_df.drop([column], axis=1, inplace=True)
                print(f'WARNING ::: type "{type}" is not supported. Column {column} has been dropped.')

        return transformed_df
        # TODO handling category??

    def change_column_position(self):
        df = copy.deepcopy(self.df)
        if self.params['target_column'] is not None:
            df.drop([self.params['target_column']], axis=1, inplace=True)
            df[self.params['target_column']] = self.df[self.params['target_column']]
        return df
