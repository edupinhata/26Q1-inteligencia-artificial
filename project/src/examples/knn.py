import pandas as pd
from math import sqrt
from sklearn.neighbors import KNeighborsClassifier

ds = pd.read_csv("iris.data", sep=",", header=None)
ds_treino = ds.sample(100, random_state=42)
ds_teste = ds.drop(ds_treino.index)

class KNN():
    def __init__(self, ds_treino):
        self.ds_treino = ds_treino
        
    def predizer(self, exemplo, k = 5):
        def calcular_distancia(e1, e2):
            soma = 0
            for i in range(len(exemplo)):
                soma += (e1[i] - e2[i]) ** 2
            return sqrt(soma)
        
        dist = [0] * len(self.ds_treino)
        for i in range(len(self.ds_treino)):
            exemplo_treino = self.ds_treino.iloc[i]
            dist[i] = calcular_distancia(exemplo, exemplo_treino)
            
        coluna_dist = 5
        coluna_classe = 4
        self.ds_treino[coluna_dist] = dist
        ds_predicao = self.ds_treino.sort_values(by=[coluna_dist])
        ds_predicao = ds_predicao.iloc[:k]
        return ds_predicao[coluna_classe].value_counts().idxmax()        
        

knn = KNN(ds_treino)
sk_knn = KNeighborsClassifier()
sk_knn.fit(ds_treino.values[:,:-1], ds_treino.values[:,-1])


acertos = 0
for i in range(len(ds_teste)):
    exemplo = ds_teste.iloc[i]
    classe_verdadeira = exemplo[4]
    del exemplo[4]
    #classe_predita = knn.predizer(exemplo)
    classe_predita = sk_knn.predict([exemplo])[0]
    if classe_predita == classe_verdadeira:
        acertos += 1
        
print("Acuracia =", acertos / len(ds_teste))