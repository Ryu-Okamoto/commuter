import re
from hhmmss import HHMMSS
from model import Predictor


class Model:
    def __init__(self, id: str):
        self.id = id
        self.model = Predictor()

    def predict(self, departure_hhmmss: str) -> str | None:
        pass
    
    def fit_online(self, departure_hhmmss: str, arrival_hhmmss: str):
        pass