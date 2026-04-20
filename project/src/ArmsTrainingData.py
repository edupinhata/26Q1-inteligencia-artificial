import numpy as np

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
        # transform the user features and arm features into a single vector 
        # that will be used to calculate the estimated reward for the arm.
        return np.concatenate((self.arm.arm_features, self.userFeatures[user]))
