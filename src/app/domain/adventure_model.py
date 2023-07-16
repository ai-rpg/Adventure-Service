from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import List
import json

@dataclass
class Conversation:
    role: str
    content: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

@dataclass
class AdventureModel:
    adventure_id: str
    gamelog: list[Conversation] = field(default_factory=list)
    users: list = field(default_factory=list)
