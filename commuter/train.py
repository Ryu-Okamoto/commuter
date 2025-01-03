from commuter.model import Predictor


def train_models(data_path: str):
    training_data = construct_training_data(data_path)
    models = []
    for user_id, (xs, ys) in training_data.items():
        model = Predictor(0, 1., 1., 1.)
        #model.fit(xs, ys)
        models.append(model)
        print(f'{user_id},{xs},{ys}')
    print(models)


def construct_training_data(data_path: str) -> dict:
    with open(data_path, mode='r') as f:
        lines = f.readlines()
    training_data = {}
    for line in lines:
        user_id, x, y = line.split()
        user_id = int(user_id)
        x = float(x)
        y = float(y)
        if user_id not in training_data:
            training_data[user_id] = ([], [])
        xs, ys = training_data[user_id]
        xs.append(x)
        ys.append(y)
    return training_data


if __name__ == '__main__':
    train_models('')
