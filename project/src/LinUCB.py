import numpy as np
import processData as ProcessData
from LinUCBArm import LinUCBArm
from ArmsTrainingData import ArmsTrainingData

# Implementation of LinUCB with disjoint linear models, as described 
# in "A Contextual-Bandit Approach to Personalized News 
# Article Recommendation" (https://arxiv.org/abs/1003.0146).
class LinUCB:
    def __init__(self, alpha):
        # The vector x_{t,a} summarizes information of both the user 
        # u_t and arm a_t
        self.simulationArms = {}
        self.alpha = alpha

        # Initialize arms
        data = ProcessData.ArticlesSelectionDataframe()
        for i in range(len(data.allDataframe)):
            arm_features = data.newsDataframe.iloc[i].values
            user_features = data.userDataframe.iloc[i].values
            click = data.clicks.iloc[i]

            arm = LinUCBArm(arm_features, len(user_features))
            armHash = arm.getUniqueArmIdentification()
            if armHash not in self.simulationArms:
                self.simulationArms[armHash] = ArmsTrainingData(arm)
            self.simulationArms[armHash].addSimulationData(user_features, click)
        
    def update(self):
        # Algorithm improves its arm-selection strategy with new observation
        # (X_{t,a_t}, a_t, r_{t,a_t})
        p_max = -np.inf
        u_best = 0
        a_key_best = None

        for a in self.simulationArms.keys():
            arm = self.simulationArms[a].arm
            user_features = self.simulationArms[a].userFeatures
            clicks = self.simulationArms[a].clicks

            for u in range(len(user_features)):
                p =  arm.score_p(self.alpha, user_features[u])
                self.simulationArms[a].p[u] = p
                if (p > p_max):
                    a_key_best = a
                    p_max = p
                    u_best = u

        x_t_a = self.simulationArms[a_key_best].x(u_best)
        arm_best = self.simulationArms[a_key_best].arm
        reward = self.simulationArms[a_key_best].clicks[u_best]

        arm_best.setA(arm_best.A + np.outer(x_t_a, x_t_a))
        arm_best.b += reward * x_t_a
        arm_best.choosenAmount+=1


    def fit(self, iterations):
        print("Training started...")
        for i in range(iterations):
            print(f"Iteration {i+1}/{iterations}\r")
            self.update()
        print("Training finished.")

    def checkResult(self):
        right = 0
        tries = 0

        for a in self.simulationArms.keys():
            armSimulation = self.simulationArms[a]
            user_features = armSimulation.userFeatures
            clicks = armSimulation.clicks

            for u in range(len(user_features)):
                p =  armSimulation.p[u]
                if (p > 0.5 and clicks[u] == 1):
                    right += 1
                elif (p <= 0.5 and clicks[u] == 0):
                    right += 1
                tries += 1

        print(f"Tries: {tries}\nAccuracy: {right/tries}")
        
linUCB = LinUCB(alpha=0.7)        
linUCB.fit(iterations=100)
linUCB.checkResult()