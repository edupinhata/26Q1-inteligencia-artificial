import numpy as np

class UCB1:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.counts = np.zeros(n_arms)   # quantas vezes cada braço foi escolhido
        self.values = np.zeros(n_arms)   # média de recompensa de cada braço
        self.t = 0

    def select_arm(self):
        self.t += 1

        # garantir que cada braço seja testado ao menos uma vez
        for arm in range(self.n_arms):
            if self.counts[arm] == 0:
                return arm

        ucb_values = np.zeros(self.n_arms)

        for arm in range(self.n_arms):
            bonus = np.sqrt((2 * np.log(self.t)) / self.counts[arm])
            ucb_values[arm] = self.values[arm] + bonus

        return np.argmax(ucb_values)


    def update(self, arm, reward):
        self.counts[arm] += 1

        n = self.counts[arm]
        value = self.values[arm]

        # atualização incremental da média
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm] = new_value