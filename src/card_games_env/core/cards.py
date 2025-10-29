from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence


RANKS_52 = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
SUITS_52 = ["h", "d", "c", "s"]


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class Deck:
    """Универсальная колода.

    По умолчанию формирует стандартные 52 карты. Можно подать произвольный список
    строк для специализированных игр (например, ["J","Q","K"] для Куна).
    """

    def __init__(self, cards: Sequence[str] | None = None, *, seed: int | None = None) -> None:
        if cards is None:
            self._cards: List[str] = [f"{r}{s}" for r in RANKS_52 for s in SUITS_52]
        else:
            self._cards = list(cards)
        self._rng = random.Random(seed)

    def shuffle(self) -> None:
        self._rng.shuffle(self._cards)

    def draw(self, n: int = 1) -> List[str]:
        assert n <= len(self._cards), "Недостаточно карт в колоде"
        out = self._cards[:n]
        self._cards = self._cards[n:]
        return out

    def __len__(self) -> int:  # pragma: no cover - тривиально
        return len(self._cards)

    def remaining(self) -> List[str]:  # pragma: no cover - для отладки
        return list(self._cards)

    @staticmethod
    def from_iterable(cards: Iterable[str], *, seed: int | None = None) -> "Deck":
        return Deck(list(cards), seed=seed)


