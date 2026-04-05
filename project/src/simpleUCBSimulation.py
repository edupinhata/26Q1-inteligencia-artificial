from simpleUCB import UCB1
import numpy as np 

np.random.seed(0)

true_probs = [0.2, 0.5, 0.8]  # probabilidades reais (o algoritmo não conhece)
bandit = UCB1(n_arms=3)

for t in range(100):
    arm = bandit.select_arm()

    # recompensa simulada
    reward = 1 if np.random.rand() < true_probs[arm] else 0

    bandit.update(arm, reward)

    print(f"t={t}, arm={arm}, reward={reward}")

print("\nEstimativas finais:", bandit.values)
print("Número de vezes escolhido:", bandit.counts)