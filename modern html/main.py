import httpx
from dataclasses import dataclass

@dataclass
class Data:
	title: str
	
	price: str
	rating: str
