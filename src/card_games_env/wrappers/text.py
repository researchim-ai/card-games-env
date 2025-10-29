from __future__ import annotations

from typing import Any, Dict


def kuhn_observation_to_text(obs: Dict[str, Any]) -> str:
    """Преобразует наблюдение Куна-покера в текст для LLM.

    Пример:
    current_player=0; card=Q; pot=2; history=[CHECK]
    """
    action_names = {0: "CHECK", 1: "BET", 2: "CALL", 3: "FOLD"}
    history = ",".join(action_names[a] for a in obs.get("history", [])) or "-"
    return (
        f"current_player={obs.get('current_player')}\n"
        f"private_card={obs.get('private_card')}\n"
        f"pot={obs.get('pot')}\n"
        f"history=[{history}]"
    )


