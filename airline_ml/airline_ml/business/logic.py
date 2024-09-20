from dataclasses import dataclass
from typing import List, Iterator

@dataclass
class Airport:
    name: str
    country: str

class Dataset:
    def __init__(self, airports: List[Airport]):
        self.airports = airports
        self.american_airports = None

    def filter_american_airports(self):
        self.american_airports = [airport for airport in self.airports if self._is_in_america(airport)]
        return Dataset(self.american_airports)

    def _is_in_america(self, airport):
        return airport.country.lower() in ['usa', 'united states', 'america']

    def build(self) -> "Dataset":
        return self.filter_american_airports()

    def __iter__(self) -> Iterator[Airport]:
        return iter(self.airports)

    def __len__(self):
        return len(self.airports)

class DatasetRepository:
    @staticmethod
    def load_from_path(path: str) -> Dataset:
        import json
        import os

        airports = []
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(os.path.join(path, filename), 'r') as f:
                    data = json.load(f)
                    airports.append(Airport(name=data['name'], country=data['country']))
        
        return Dataset(airports)

    @staticmethod
    def save_to_path(dataset: Dataset, path: str):
        import json
        import os

        os.makedirs(path, exist_ok=True)
        for i, airport in enumerate(dataset):
            with open(os.path.join(path, f"airport_{i}.json"), 'w') as f:
                json.dump({"name": airport.name, "country": airport.country}, f)

