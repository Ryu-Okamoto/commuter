import re
from hhmmss import HHMMSS
from commuter.model_raw import Predictor


class Model:
    def __init__(self, id: str):
        self.id = id
        self.model = Predictor()

    def predict(self, departure_time: HHMMSS) -> HHMMSS | None:
        departure_seconds = departure_time.to_seconds()
        predicted_seconds = self.model.predict(departure_seconds)
        if predicted_seconds in [float('nan'), float('inf')]:
            return None
        return HHMMSS.from_seconds(predicted_seconds)
    
    def fit_local(self, departure_times: list[HHMMSS], arrival_times: list[HHMMSS]):
        departure_seconds_list = list(map(HHMMSS.to_seconds, departure_times))
        arrival_seconds_list = list(map(HHMMSS.to_seconds, arrival_times))
        travel_seconds_list = [d - a for (d, a) 
                               in zip(departure_seconds_list, arrival_seconds_list)]
        self.model.fit_local(departure_seconds_list, travel_seconds_list)
    
    def fit_online(self, departure_time: HHMMSS, arrival_time: HHMMSS):
        departure_seconds = departure_time.to_seconds()
        arrival_seconds = arrival_time.to_seconds()
        travel_seconds = arrival_seconds - departure_seconds
        self.model.fit_online(departure_seconds, travel_seconds)

    def to_json(self):
        parameters = self.model.to_json()['parameters']
        return \
            {
                'model': {
                    'id': self.id,
                    'parameters': parameters
                }
            }