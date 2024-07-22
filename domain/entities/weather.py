from dataclasses import dataclass


@dataclass
class Weather:
    temperature: float
    metric: str
    city: str
    country: str
