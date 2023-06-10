from dataclasses import dataclass


@dataclass
class AdventureModel:
    adventure_id: str
    users: []
    intro_text: str
    game_log: str
