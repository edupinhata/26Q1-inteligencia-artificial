import numpy as np

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
