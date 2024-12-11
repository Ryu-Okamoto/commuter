import json
import numpy as np


# quadratic regression model
class Predictor:
    def __init__(self, _id, w0, w1, w2):
        self.id = _id
        self.w = np.array([w0, w1, w2])

        # for online learning
        self.n = 0
        self.x_mean = 0.0
        self.x_var = 0.0
        self.y_mean = 0.0
        self.y_var = 0.0

    def fit(self, xs, ys):
        n = len(xs)
        xs = (xs - xs.mean()) / xs.std()
        X = np.c_[xs**2, xs, np.ones([n, 1])]
        ys = np.array(ys)

        num_iter = 100
        alpha = 0.05

        for iter in range(num_iter):
            h = np.dot(X, self.w)
            self.w[0] = self.w[0] - (alpha / n) * (h - ys).sum()
            self.w[1] = self.w[1] - (alpha / n) * ((h - ys).T.dot(X))
            self.w[2] = self.w[2] - (alpha / n) * ((h - ys).T.dot(X**2))

        # for online learning
        self.n = n
        self.x_mean = xs.mean()
        self.x_dev = xs.dev()
        self.y_mean = ys.mean()
        self.y_dev = ys.dev()

    def predict(self, x) -> float:
        x_std = np.sqrt(self.x_dev)
        y_std = np.sqrt(self.y_dev)
        x = (x - self.x_mean) / x_std
        y = self.w[0] + self.w[1] * x + self.w[2] * x**2
        y = y * y_std + self.y_mean
        return y

    def to_json(self):
        return \
            {
                'model': {
                    'id': self.id,
                    'w0': self.w[0],
                    'w1': self.w[1],
                    'w2': self.w[2]
                }
            }


if __name__ == '__main__':
    pass
