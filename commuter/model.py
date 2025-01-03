import numpy as np
import matplotlib.pyplot as plt


# quadratic regression model
class Predictor:
    def __init__(self, _id: int, w0: float, w1: float, w2: float):
        self.id = _id
        self.w = np.array([w0, w1, w2])

        # for online learning
        self.n = 0
        self.x_mean = 0.0
        self.x_var = 1.0
        self.y_mean = 0.0
        self.y_var = 1.0

    def fit(self, xs, ys) -> list:
        xs = np.array(xs)
        ys = np.array(ys)

        # for online learning
        self.n = len(xs)
        self.x_mean = xs.mean()
        self.x_var = xs.var()
        self.y_mean = ys.mean()
        self.y_var = ys.var()

        xs = (xs - xs.mean()) / xs.std()
        ys = (ys - ys.mean()) / ys.std()
        X = np.c_[np.ones([self.n, 1]), xs, xs**2]

        NUM_OF_EPOCH = 100
        LEARNING_RATE = 0.05
        losses = []
        for _ in range(NUM_OF_EPOCH):
            fs = np.dot(X, self.w)
            self.w[0] -= (LEARNING_RATE / self.n) * (fs - ys).sum()
            self.w[1] -= (LEARNING_RATE / self.n) * ((fs - ys).T.dot(xs))
            self.w[2] -= (LEARNING_RATE / self.n) * ((fs - ys).T.dot(xs**2))
            loss = ((fs - ys)**2).sum()
            losses.append(loss)

        return losses

    # MUST: call fit() in advance
    # because var(std) becomes 0, and div0 error occurs
    def fit_online(self, x, y):

        # for (un-)standardizing
        self.x_var = next_var(x, self.n, self.x_mean, self.x_var)
        self.x_mean = next_mean(x, self.n, self.x_mean)
        self.y_var = next_var(y, self.n, self.y_mean, self.y_var)
        self.y_mean = next_mean(y, self.n, self.y_mean)
        self.n += 1

        x_std = np.sqrt(self.x_var)
        y_std = np.sqrt(self.y_var)
        x = (x - self.x_mean) / x_std
        y = (y - self.y_mean) / y_std
        X = np.array([1, x, x**2])

        NUM_OF_EPOCH = 10
        LEARNING_RATE = 0.01
        for _ in range(NUM_OF_EPOCH):
            f = np.dot(X, self.w)
            self.w[0] -= LEARNING_RATE * (f - y)
            self.w[1] -= LEARNING_RATE * (f - y) * x
            self.w[0] -= LEARNING_RATE * (f - y) * x**2

    def predict(self, x) -> float:
        x_std = np.sqrt(self.x_var)
        y_std = np.sqrt(self.y_var)
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


def next_mean(new_value, n: int, mean: float) -> float:
    return (new_value + n * mean) / (n + 1)


def next_var(new_value, n: int, mean: float, var: float) -> float:
    new_mean = next_mean(new_value, n, mean)
    return (new_value**2 + n * (mean**2 + var)) / (n + 1) - new_mean**2


if __name__ == '__main__':
    xs = np.linspace(-5., 5., 50)
    ys = xs**2 + np.random.normal(size=len(xs))

    model = Predictor(0, 0., 0., 0.)
    losses = model.fit(xs, ys)
    ys_ = list(map(model.predict, xs))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))
    ax1.plot(xs, ys, '.', color='r', label='actual')
    ax1.plot(xs, ys_, color='b', label='predicted')
    ax1.set_title('actual-predicted')
    ax1.legend(loc='lower left')
    ax2.plot(losses, '.')
    ax2.set_title('loss')
    fig.suptitle(
        r'training quadratic regression model for '
        r'data following y = x$^2$ + $\varepsilon$, where $\varepsilon \sim N(0,1)$'
    )

    plt.show()
