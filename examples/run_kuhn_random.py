import random
from card_games_env.envs.kuhn_poker import KuhnPokerEnv


def main() -> None:
    env = KuhnPokerEnv()
    rng = random.Random(42)
    total = [0.0, 0.0]

    for _ in range(10):
        obs = env.reset(seed=rng.randint(0, 10**9))
        while True:
            action = rng.choice(env.legal_actions)
            obs, rewards, terminated, _ = env.step(action)
            if terminated:
                total[0] += rewards[0]
                total[1] += rewards[1]
                break

    print("Total:", total)


if __name__ == "__main__":
    main()


