import argparse
import random
from typing import Optional

from .envs.kuhn_poker import KuhnPokerEnv


def run_kuhn(episodes: int, seed: Optional[int]) -> None:
    env = KuhnPokerEnv()
    rng = random.Random(seed)
    total_returns = [0.0, 0.0]

    for ep in range(episodes):
        obs = env.reset(seed=None if seed is None else rng.randint(0, 10**9))
        while True:
            legal = env.legal_actions
            action = rng.choice(legal)
            obs, rewards, terminated, info = env.step(action)
            if terminated:
                total_returns[0] += rewards.get(0, 0.0)
                total_returns[1] += rewards.get(1, 0.0)
                break

    print(f"Episodes: {episodes}")
    print(f"Total returns P0: {total_returns[0]:.1f}  P1: {total_returns[1]:.1f}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="cge-run", description="Card Games Env CLI")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    p_kuhn = subparsers.add_parser("kuhn", help="Run random agents on Kuhn Poker")
    p_kuhn.add_argument("--episodes", type=int, default=10)
    p_kuhn.add_argument("--seed", type=int, default=None)

    args = parser.parse_args()

    if args.cmd == "kuhn":
        run_kuhn(episodes=args.episodes, seed=args.seed)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()


