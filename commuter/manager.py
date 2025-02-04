from hhmmss import HHMMSS
from model_helper import Model


class User:
    def __init__(self, id: str):
        self.id = id
        self.models = {}

    def create_model(self, id: str):
        self.models[id] = Model(id)

    def get_model(self, id: str) -> Model:
        return self.models[id]

