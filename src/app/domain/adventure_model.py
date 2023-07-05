from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import List

@dataclass
class AdventureModel:
    adventure_id: str
    intro_text: str
    history: str
    users: list = field(default_factory=list)
