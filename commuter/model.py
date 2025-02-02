import numpy as np
import matplotlib.pyplot as plt
import json


# polynomial regression model
class Predictor:
    def __init__(
        self,
        w: list = [1.0, 1.0, 1.0],
        n: int = 0,
        x_mean: float = 0.0,
        x_var: float = 1.0,
        y_mean: float = 0.0,
        y_var: float = 1.0
    ):
        self.w = np.array(w)

        # for online learning
        self.n = n
        self.x_mean = x_mean
        self.x_var = x_var
        self.y_mean = y_mean
        self.y_var = y_var

    def fit_local(
        self,
        xs: list, 
        ys: list,
        num_of_epochs: int = 100,
        learning_rate: float = 0.05
    ) -> list:
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
        X = np.array([xs**i for i in range(len(self.w))])

        losses = []
        for _ in range(num_of_epochs):
            fs = np.dot(self.w, X)
            for i in range(len(self.w)):
                self.w[i] -= (learning_rate / self.n) * (fs - ys).T.dot(xs**i)
            loss = ((fs - ys)**2).sum()
            losses.append(loss)

        return losses

    def fit_online(
        self,
        x: float,
        y: float,
        num_of_epochs: int = 10,
        learning_rate: float = 0.01
    ) -> list:   
        if self.n == 0:
            self.x_var = 0.0
            self.x_mean = x
            self.y_var = 0.0
            self.y_mean = y
            self.n += 1
            return float('inf')

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
        X = np.array([x**i for i in range(len(self.w))])

        losses = []
        for _ in range(num_of_epochs):
            f = np.dot(self.w, X)
            for i in range(len(self.w)):
                self.w[i] -= learning_rate * (f - y) * x**i
            loss = (f - y)**2
            losses.append(loss)
        
        return losses

    def predict(self, x) -> float:
        x_std = np.sqrt(self.x_var)
        y_std = np.sqrt(self.y_var)
        x = (x - self.x_mean) / x_std
        X = np.array([x**i for i in range(len(self.w))])
        y = np.dot(self.w, X)
        y = y * y_std + self.y_mean
        return y

    def to_json(self):
        return \
            {
                'model': {
                    'w': list(map(float, self.w)),
                    'n': int(self.n),
                    'x_mean': float(self.x_mean),
                    'x_var': float(self.x_var),
                    'y_mean': float(self.y_mean),
                    'y_var': float(self.y_var)
                }
            }


def next_mean(new_value, n: int, mean: float) -> float:
    return (new_value + n * mean) / (n + 1)


def next_var(new_value, n: int, mean: float, var: float) -> float:
    new_mean = next_mean(new_value, n, mean)
    return (new_value**2 + n * (mean**2 + var)) / (n + 1) - new_mean**2


if __name__ == '__main__':
    xs = np.linspace(-5., 5., 50)
    ys = xs**3 - 2.0 * xs + np.random.normal(size=len(xs))

    model = Predictor([1., 1., 1., 1.])
    losses = model.fit_local(xs, ys)
    ys_ = list(map(model.predict, xs))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))
    ax1.plot(xs, ys, '.', color='r', label='actual')
    ax1.plot(xs, ys_, color='b', label='predicted')
    ax1.set_title('actual-predicted')
    ax1.legend(loc='lower left')
    ax2.plot(losses, '.')
    ax2.set_title('loss')
    fig.suptitle(
        r'training polynomial regression model for '
        r'data following y = x$^3 - 2x$ + $\varepsilon$, where $\varepsilon \sim N(0,1)$'
    )

    plt.show()

    print(json.dumps(model.to_json(), indent=4, ensure_ascii=True))