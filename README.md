# card-games-env

Мультиагентные окружения карточных игр (Кун-покер и др.) для обучения моделей RL и LLM.

## Возможности (v0)
- Базовый интерфейс пошагового мультиагентного окружения
- Окружение Куна-покера (2 игрока)
- CLI для запуска эпизодов со случайными агентами
- Текстовый wrapper для LLM-наблюдений

## Установка

```bash
pip install -e .
```

Требуется Python 3.9+.

## Быстрый старт (CLI)

```bash
cge-run kuhn --episodes 10 --seed 42
```

## Использование в Python

```python
from card_games_env.envs.kuhn_poker import KuhnPokerEnv

env = KuhnPokerEnv()
obs = env.reset(seed=42)
while True:
    legal = env.legal_actions
    import random
    action = random.choice(legal)
    obs, rewards, terminated, info = env.step(action)
    if terminated:
        print("rewards:", rewards)
        break
```

## Дальнейшие планы
- Техасский Холд'ем на базе eval7
- Совместимый слой с PettingZoo
- Дополнительные карточные игры (Блэкджек, Ледюк-покер)

Лицензия: см. `LICENSE`.
