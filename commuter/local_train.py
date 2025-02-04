import json
import matplotlib.pyplot as plt
import numpy as np

from commuter.model_raw import Predictor
from commuter.model import Model


def main(data_path: str, weights_path: str):
    with open(data_path, mode='r') as f:
        data = json.load(fp=f)
    with open(weights_path, mode='r') as f:
        weights = json.load(fp=f)
    
    for user_data in data:
        user_id = user_data['user_id']
        commuting_data = user_data['commuting_data']
        # returning_data = user_data['returning_data']

        model_weight = {}
        for weight in weights:
            if weight['id'] == user_id:
                model_weight = weight['model']

        model = Predictor() if model_weight == {} \
            else Predictor(
                model_weight['w'],
                model_weight['n'],
                model_weight['x_mean'],
                model_weight['x_var'],
                model_weight['y_mean'],
                model_weight['y_var'],
            )
        
        xs = list(map(serialize, [d['departure_time'] for d in commuting_data]))
        ys = list(map(serialize, [d['minutes_required'] for d in commuting_data]))

        losses = model.fit_local(xs, ys)

        max_x = max(xs)
        min_x = min(xs)
        xs_ = np.linspace(min_x, max_x)
        ys_ = list(map(model.predict, xs_))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))
        ax1.plot(xs, ys, '.', color='r', label='actual')
        ax1.plot(xs_, ys_, color='b', label='predicted')
        ax1.set_title('actual-predicted')
        ax1.legend(loc='lower left')
        ax2.plot(losses, '.')
        ax2.set_title('loss')
        plt.show()

        for v in ['064400', '065032', '065540', '070012', '070555', '071000']:
            v_ = v
            v = deserialize(int(model.predict(float(serialize(v)))))
            print(f'出発： {v_[:2]}時間 {v_[2:4]}分 {v_[4:]}秒 → 所要時間： {v[:2]}時間 {v[2:4]}分 {v[4:]}秒')


if __name__ == '__main__':
    main('local_data/test.json', 'commuter/weights.json')