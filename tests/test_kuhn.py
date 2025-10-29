import random
from card_games_env.envs.kuhn_poker import (
    KuhnPokerEnv,
    ACTION_CHECK,
    ACTION_BET,
    ACTION_CALL,
    ACTION_FOLD,
)


def test_episode_runs_and_terminates():
    env = KuhnPokerEnv()
    obs = env.reset(seed=123)
    steps = 0
    while True:
        legal = env.legal_actions
        assert len(legal) > 0
        obs, rewards, terminated, _ = env.step(legal[0])
        steps += 1
        if terminated:
            assert rewards[0] == -rewards[1]
            break
        assert steps < 10


def test_random_policy_zero_sum_many_episodes():
    env = KuhnPokerEnv()
    rng = random.Random(1)
    returns = [0.0, 0.0]
    for _ in range(200):
        env.reset(seed=rng.randint(0, 10**9))
        while True:
            a = rng.choice(env.legal_actions)
            _, r, term, _ = env.step(a)
            if term:
                returns[0] += r[0]
                returns[1] += r[1]
                break
    assert abs(returns[0] + returns[1]) < 1e-6


