import json
from airline_ml.business.logic import Dataset

class AirportRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_airports(self, airports):
        with open(self.file_path, 'w') as f:
            json.dump([{"name": airport.name, "country": airport.country} for airport in airports], f)

    def load_airports(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

class Trainer:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def train(self, dataset: Dataset):
        for airport in dataset:
            print(f"Training on: {airport.name}")
        # Add your actual training logic here