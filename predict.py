from dataclasses import dataclass
import json
import numpy as np


@dataclass
class Weight:
    w0: float = 1.0
    w1: float = 1.0
    w2: float = 1.0


# quadratic regression model
class Predictor:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.weight = self.load_weight()

    def fit_local(self, data_path: str):
        pass

    def fit_online(self, datetime):
        pass

    def predict(self, now) -> float:
        pass

    def load_weight(self) -> Weight:
        with open('weight.json') as f:
            weight_json = json.load(f)
        users = list(map(lambda obj: obj['user'], weight_json))
        for user in users:
            if self.user_id == user['id']:
                return Weight(user['w0'], user['w1'], user['w2'])
        return Weight()

    def dump_weight(self):
        with open('weight.json') as f:
            weight_json = json.load(f)
        users = list(map(lambda obj: obj['user'], weight_json))
        target_user = None
        for user in users:
            if self.user_id == user['id']:
                target_user = user
                break
        if target_user is None:
            target_user = {'id': self.user_id}
            weight_json.append({'user': target_user})
        target_user['w0'] = self.weight.w0
        target_user['w1'] = self.weight.w1
        target_user['w2'] = self.weight.w2
        with open('weight.json', mode='w') as f:
            json.dump(weight_json, fp=f, indent=2)
