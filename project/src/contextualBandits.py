import numpy as np


class LinUCBArm:
    def __init__(self, d: int):
        self.d = d
        self.A = np.eye(d)          # matriz d x d
        self.b = np.zeros(d)        # vetor d

    def theta(self) -> np.ndarray:
        return np.linalg.solve(self.A, self.b)

    def score(self, x: np.ndarray, alpha: float) -> float:
        A_inv = np.linalg.inv(self.A)
        theta_hat = self.theta()

        exploit = theta_hat @ x
        explore = alpha * np.sqrt(x @ A_inv @ x)

        return exploit + explore

    def update(self, x: np.ndarray, reward: float) -> None:
        self.A += np.outer(x, x)
        self.b += reward * x


class LinUCB:
    def __init__(self, n_arms: int, d: int, alpha: float = 1.0):
        self.n_arms = n_arms
        self.d = d
        self.alpha = alpha
        self.arms = [LinUCBArm(d) for _ in range(n_arms)]

    def select_arm(self, x: np.ndarray) -> int:
        scores = [arm.score(x, self.alpha) for arm in self.arms]
        return int(np.argmax(scores))

    def update(self, arm_index: int, x: np.ndarray, reward: float) -> None:
        self.arms[arm_index].update(x, reward)


def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + np.exp(-z))


if __name__ == "__main__":
    np.random.seed(42)

    d = 3
    n_arms = 2
    alpha = 0.7
    T = 100

    agent = LinUCB(n_arms=n_arms, d=d, alpha=alpha)

    # "Mundo real" escondido: cada braço tem um vetor verdadeiro
    true_theta = [
        np.array([0.9, 0.2, -0.1]),
        np.array([0.3, 0.8,  0.4])
    ]

    total_reward = 0.0

    for t in range(1, T + 1):
        # contexto atual
        x = np.random.rand(d)

        # escolhe ação
        chosen_arm = agent.select_arm(x)

        # gera recompensa binária simulada
        expected_reward = true_theta[chosen_arm] @ x
        click_prob = sigmoid(expected_reward)
        reward = 1.0 if np.random.rand() < click_prob else 0.0

        # atualiza
        agent.update(chosen_arm, x, reward)
        total_reward += reward

        print(
            f"t={t:03d} | x={np.round(x, 3)} | "
            f"arm={chosen_arm} | reward={reward:.0f}"
        )

    print("\nParâmetros aprendidos:")
    for i, arm in enumerate(agent.arms):
        print(f"Braço {i}: theta_hat = {np.round(arm.theta(), 4)}")

    print(f"\nRecompensa total: {total_reward}")