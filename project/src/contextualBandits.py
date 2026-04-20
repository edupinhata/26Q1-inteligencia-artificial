import numpy as np
import processData as processData

# Each arm, that represents an article, will have a list of user features and clicks that will be used to train the algorithm.
# This class is used to store the data that will be used to train the algorithm. It will be used to simulate the environment and provide feedback to the algorithm.
class ArmsTrainingData:
    def __init__(self, arm):
        self.arm = arm
        self.userFeatures = []
        self.clicks = []
        self.alreadySimulated = 0

    def addSimulationData(self, userFeatures, clicked):
        self.userFeatures.append(userFeatures)
        self.clicks.append(clicked)

    def getNextSimulation(self):
        simulationNumber = self.alreadySimulated
        features = self.userFeatures[simulationNumber], self.clicks[simulationNumber]
        self.alreadySimulated+=1
        return features

    def canTrain(self):
        return self.alreadySimulated < len(self.userFeatures)

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
        explore = alpha * np.sqrt(self.arm_features @ self.A_inv @ self.arm_features)

        return exploit + explore
        
    def getUniqueArmIdentification(self):
        return hash(tuple(self.arm_features))

class LinUCB:
    def __init__(self):
        # The vector x_{t,a} summarizes information of both the user 
        # u_t and arm a_t
        self.simulationArms = {}

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
        for trial in range(100):
            for i in range(len(self.Arms)):
                arm = self.Arms[i]
                # if arm is new

                p = true_theta @ arm.arm_features + np.sqrt(arm.arm_features @ A_inv @ arm.arm_features)
                arm.choosenAmount+=1
            pass

        
        
    def selectArm(self):
        # No feedback (payoff) is observed for unchosen arms a != a_t
        payoff_r = 0
        return payoff_r

