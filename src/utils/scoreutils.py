import sklearn.metrics


def accuracy(y_true, y_pred):
    return sklearn.metrics.accuracy_score(y_true, y_pred)
