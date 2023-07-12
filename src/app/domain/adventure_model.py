from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import List

@dataclass
class AdventureModel:
    adventure_id: str
    intro_text: str
    history: list = field(default_factory=list)
    users: list = field(default_factory=list)
