from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import eval7  # type: ignore

from ..core.env import TurnBasedMultiAgentEnv


class TexasHoldemEnv(TurnBasedMultiAgentEnv):
    """Заготовка окружения Техасского Холдема (2 игрока).

    Примечание: это скелет для последующей реализации логики ставок и улиц.
    На данном этапе окружение отдаёт только раздачу карт в reset().
    """

    def __init__(self, num_players: int = 2) -> None:
        assert num_players == 2, "Сейчас поддерживаются только 2 игрока"
        self.num_players = num_players
        self.current_player = 0
        self._deck = list(eval7.Deck())
        self._hands: List[List[str]] = [[] for _ in range(num_players)]
        self._board: List[str] = []
        self._terminated = False

    def reset(self, seed: Optional[int] = None) -> Dict[str, Any]:
        d = eval7.Deck()
        if seed is not None:
            d.shuffle(seed)
        else:
            d.shuffle()
        self._deck = list(d)
        self._hands = [[str(self._deck.pop()), str(self._deck.pop())] for _ in range(self.num_players)]
        self._board = []
        self._terminated = False
        self.current_player = 0
        return {
            "hole_cards": list(self._hands[self.current_player]),
            "board": list(self._board),
            "round": "preflop",
            "current_player": self.current_player,
        }

    def step(self, action: int) -> Tuple[Dict[str, Any], Dict[int, float], bool, Dict[str, Any]]:
        raise NotImplementedError("Логика ставок и переходов пока не реализована")

    @property
    def legal_actions(self) -> List[int]:
        # Заглушка: действий нет до полной реализации логики
        return []


