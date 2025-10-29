from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

from ..core.env import TurnBasedMultiAgentEnv


ACTION_CHECK = 0
ACTION_BET = 1
ACTION_CALL = 2
ACTION_FOLD = 3


class KuhnPokerEnv(TurnBasedMultiAgentEnv):
    """Кун-покер (2 игрока, колода из J,Q,K).

    Правила:
    - Каждый игрок анте 1 фишку (общий банк = 2)
    - Игрок 0 ходит первым, доступно: CHECK или BET (ставка 1)
    - Если CHECK, игрок 1 может CHECK (шоудаун) либо BET
    - Если был BET, ответивший может CALL (шоудаун) либо FOLD
    - Выплаты относительно уплаченных анте:
        * CHECK-CHECK: победитель +1 / проигравший -1
        * BET-FOLD: беттор +1 / фолдер -1
        * BET-CALL: победитель +2 / проигравший -2
    Наблюдение: { 'private_card', 'history', 'pot', 'current_player' }
    """

    def __init__(self) -> None:
        self.num_players = 2
        self._rng = random.Random()
        self._cards = ["J", "Q", "K"]
        self.current_player = 0
        self._private_cards: List[str] = ["", ""]
        self._history: List[int] = []
        self._pot = 2  # анте по 1
        self._terminated = False

    def reset(self, seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            self._rng.seed(seed)
        self._terminated = False
        self._history = []
        self._pot = 2
        self.current_player = 0
        cards = self._cards[:]
        self._rng.shuffle(cards)
        self._private_cards = [cards[0], cards[1]]
        return self._make_obs()

    def step(self, action: int) -> Tuple[Dict[str, Any], Dict[int, float], bool, Dict[str, Any]]:
        assert not self._terminated, "Эпизод завершён"
        assert action in self.legal_actions, f"Недопустимое действие: {action}"

        self._history.append(action)

        # Переходы состояний
        rewards: Dict[int, float] = {0: 0.0, 1: 0.0}
        info: Dict[str, Any] = {}

        if action == ACTION_BET:
            self._pot += 1  # беттор добавляет 1
            self.current_player = 1 - self.current_player
        elif action == ACTION_CHECK:
            # Если CHECK второй по очереди -> шоудаун
            if len(self._history) >= 2 and self._history[-2] == ACTION_CHECK and self.current_player == 1:
                # Был CHECK игрока 0, затем CHECK игрока 1
                winner = self._winner()
                if winner == 0:
                    rewards = {0: +1.0, 1: -1.0}
                else:
                    rewards = {0: -1.0, 1: +1.0}
                self._terminated = True
            else:
                self.current_player = 1 - self.current_player
        elif action == ACTION_CALL:
            # Завершение: BET-CALL -> шоудаун, пот уже включает ставку и колл = +1
            self._pot += 1
            winner = self._winner()
            if winner == 0:
                rewards = {0: +2.0, 1: -2.0}
            else:
                rewards = {0: -2.0, 1: +2.0}
            self._terminated = True
        elif action == ACTION_FOLD:
            # Завершение: BET-FOLD -> беттор выигрывает +1
            bettor = 1 - self.current_player  # тот, кто сделал последний BET
            if bettor == 0:
                rewards = {0: +1.0, 1: -1.0}
            else:
                rewards = {0: -1.0, 1: +1.0}
            self._terminated = True
        else:  # pragma: no cover - защитный код
            raise ValueError("Неизвестное действие")

        obs = self._make_obs()
        return obs, rewards if self._terminated else {0: 0.0, 1: 0.0}, self._terminated, info

    @property
    def legal_actions(self) -> List[int]:
        if self._terminated:
            return []
        # Начало раунда
        if len(self._history) == 0:
            return [ACTION_CHECK, ACTION_BET]
        # После CHECK первого игрока
        if len(self._history) == 1 and self._history[0] == ACTION_CHECK:
            return [ACTION_CHECK, ACTION_BET]
        # После BET: ответ CALL или FOLD
        if self._history[-1] == ACTION_BET:
            return [ACTION_CALL, ACTION_FOLD]
        # После CHECK, BET последовательности ходит другой игрок -> CALL/FOLD
        if len(self._history) >= 2 and self._history[-2:] == [ACTION_CHECK, ACTION_BET]:
            return [ACTION_CALL, ACTION_FOLD]
        # Иначе недостижимо
        return []

    def _winner(self) -> int:
        order = {"J": 0, "Q": 1, "K": 2}
        p0 = order[self._private_cards[0]]
        p1 = order[self._private_cards[1]]
        return 0 if p0 > p1 else 1

    def _make_obs(self) -> Dict[str, Any]:
        return {
            "private_card": self._private_cards[self.current_player],
            "history": list(self._history),
            "pot": self._pot,
            "current_player": self.current_player,
        }


