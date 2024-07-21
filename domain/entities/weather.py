from dataclasses import dataclass


@dataclass
class Wheater:
    temperature: float
    metric: str
    city: str
    country: str
