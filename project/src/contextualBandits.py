import numpy as np
import processData as processData

# Each arm, that represents an article, will have a list of user features and clicks that will be used to train the algorithm.
# This class is used to store the data that will be used to train the algorithm. It will be used to simulate the environment and provide feedback to the algorithm.
class ArmsTrainingData:
    def __init__(self, arm):
        self.arm = arm
        self.userFeatures = []
        self.clicks = []
        # estimated reward for the arm, that will be used to select the arm
        # in the next iteration. 
        # It will be updated after each iteration with the new estimated reward.
        self.p = [] 


    def addSimulationData(self, userFeatures, clicked):
        self.userFeatures.append(userFeatures)
        self.clicks.append(clicked)
        self.p.append(0)

    def x(self, user):
        return np.concatenate((self.arm.arm_features, self.userFeatures[user]))

class LinUCBArm:
    # In the context of article recommendation, articles in the pool are arms

    def __init__(self, arm_features, user_features_length):
        self.d = len(arm_features) + user_features_length
        self.arm_features = arm_features

        self.A = np.eye(self.d)          # matriz d x d
        self.A_inv = np.eye(self.d)      # matriz d x d (inversa de A)
        self.b = np.zeros(self.d)        # vetor d

        self.choosenAmount = 0
        

    def setA(self, A):
        self.A = A
        self.A_inv = np.linalg.inv(A)

    def thetha(self):
        return self.A_inv @ self.b

    def score_p(self, alpha, user_features):
        x_a = np.concatenate((self.arm_features, user_features))
        theta_T = self.thetha().T

        exploit = theta_T @ x_a
        explore = alpha * np.sqrt(x_a.T @ self.A_inv @ x_a)

        return exploit + explore
        
    def getUniqueArmIdentification(self):
        return hash(tuple(self.arm_features))

class LinUCB:
    def __init__(self, alpha):
        # The vector x_{t,a} summarizes information of both the user 
        # u_t and arm a_t
        self.simulationArms = {}
        self.alpha = alpha

        # Initialize arms
        data = processData.ArticlesSelectionDataframe()
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
        p_max = 0
        u_max = 0

        for a in self.simulationArms.keys():
            arm = self.simulationArms[a].arm
            user_features = self.simulationArms[a].userFeatures
            clicks = self.simulationArms[a].clicks

            for u in range(len(user_features)):
                p =  arm.score_p(self.alpha, user_features[u])
                self.simulationArms[a].p[u] = p
                if (p > p_max):
                    p_max = p
                    u_max = u

            x_t_a = self.simulationArms[a].x(u_max)
            reward = clicks[u_max]

            arm.setA(arm.A + x_t_a @ x_t_a.T)
            arm.b += reward * x_t_a

            arm.choosenAmount+=1

    def fit(self, iterations):
        print("Training started...")
        for i in range(iterations):
            print(f"Iteration {i+1}/{iterations}\t")
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

        print(f"Accuracy: {right/tries}")
        
linUCB = LinUCB(alpha=0.7)        
linUCB.fit(iterations=100)
linUCB.checkResult()