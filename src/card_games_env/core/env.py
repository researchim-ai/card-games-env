from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class TurnBasedMultiAgentEnv(ABC):
    """Базовый интерфейс пошагового мультиагентного окружения.

    Принципы:
    - В каждый момент времени ровно один текущий игрок делает действие
    - `reset()` возвращает наблюдение текущего игрока
    - `step(action)` применяет действие текущего игрока и возвращает
      наблюдение следующего текущего игрока (или финальное состояние)
    - `rewards` — словарь вознаграждений по агентам при терминальном состоянии
    - `legal_actions` — список допустимых действий для текущего игрока
    """

    num_players: int
    current_player: int

    @abstractmethod
    def reset(self, seed: Optional[int] = None) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def step(self, action: int) -> Tuple[Dict[str, Any], Dict[int, float], bool, Dict[str, Any]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def legal_actions(self) -> List[int]:
        raise NotImplementedError


