# Data classes (Card, Player, GameState)

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

@dataclass
class Card:
    rank: str
    suit: Suit

    def to_dict(self):
        return {"rank": self.rank, "suit": self.suit.value}

@dataclass
class Player:
    name: str
    score: int = 0
    hand: List[Card] = field(default_factory=list)

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "hand": [c.to_dict() for c in self.hand]
        }

@dataclass
class GameState:
    players: List[Player] = field(default_factory=list)
    current_turn: int = 0
    deck: List[Card] = field(default_factory=list)
    top_card: Optional[Card] = None

    def to_dict(self):
        return {
            "players": [p.to_dict() for p in self.players],
            "current_turn": self.current_turn,
            "deck_size": len(self.deck),
            "top_card": self.top_card.to_dict() if self.top_card else None
        }