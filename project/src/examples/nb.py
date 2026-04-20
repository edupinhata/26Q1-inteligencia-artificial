import pandas as pd
from sklearn.naive_bayes import GaussianNB, CategoricalNB
from sklearn.preprocessing import KBinsDiscretizer
from math import inf
import numpy as np

def discretizar(ds_treino, ds_teste):
    kbins = KBinsDiscretizer(n_bins=3, 
                             encode="ordinal", 
                             strategy="uniform")
    
    ds_treino.reset_index(inplace=True, drop=True)
    ds_teste.reset_index(inplace=True, drop=True)
    
    temp = ds_treino.values[:,:-1]
    kbins.fit(temp)
    temp = kbins.transform(temp)
    temp = pd.DataFrame(temp)
    temp[4] = ds_treino[4]
    ds_treino_d = temp
    
    temp = ds_teste.values[:,:-1]
    temp = kbins.transform(temp)
    temp = pd.DataFrame(temp)
    temp[4] = ds_teste[4]
    ds_teste_d = temp
    
    return ds_treino_d, ds_teste_d


class NaiveBayesCategorico():
    def __init__(self, ds_treino):
        coluna_classe = 4
        self.classes = list(ds_treino[coluna_classe].unique())
        self.atributos = list(ds_treino.columns)
        del self.atributos[coluna_classe]
        
        # chave: classe -> p
        self.p_classe = {}
        
        # chave: (v, a, classe) -> p
        self.p_atributo_classe = {}
        
        for c in self.classes:
            ds_classe = ds_treino[ds_treino[coluna_classe] == c]
            p = len(ds_classe) / len(ds_treino)
            self.p_classe.update({ c : p})
            
            for a in self.atributos:
                valores = ds_treino[a].unique()
                d = len(valores)
                for v in valores:
                    ds_atributo = ds_classe[ds_classe[a] == v]
                    #p = len(ds_atributo) / len(ds_classe)
                    p = (len(ds_atributo) + 1) / (len(ds_classe) + d)
                    self.p_atributo_classe.update({ (v, a, c) : p})
                
    
    def predizer(self, exemplo):
        classe_predita = None
        maior_p = -inf        
        for c in self.classes:
            #p = self.p_classe[c]
            p = np.log(self.p_classe[c])
            for a in self.atributos:
                #p *= self.p_atributo_classe[(exemplo[a], a, c)]
                p += np.log(self.p_atributo_classe[(exemplo[a], a, c)])
            if p > maior_p:
                classe_predita = c
                maior_p = p
                
        return classe_predita
    
    
    
class NaiveBayesGaussiano():
    def __init__(self, ds_treino):
        coluna_classe = 4
        self.classes = list(ds_treino[coluna_classe].unique())
        self.atributos = list(ds_treino.columns)
        del self.atributos[coluna_classe]
        
        # chave: classe -> p
        self.p_classe = {}
        
        # chave: (a, classe) -> (media, var)
        self.p_atributo_classe = {}
        
        for c in self.classes:
            ds_classe = ds_treino[ds_treino[coluna_classe] == c]
            p = len(ds_classe) / len(ds_treino)
            self.p_classe.update({ c : p})
            
            for a in self.atributos:
                media = ds_classe[a].mean()
                variancia = ds_classe[a].var(ddof=0)
                self.p_atributo_classe.update({ (a, c) : (media, variancia) })
                
    
    def predizer(self, exemplo):
        def funcao_gausssiana(v, media, variancia):
            r = 1 / np.sqrt(2 * np.pi * variancia)
            r *= np.exp(-1 * (v - media)**2 / (2 * variancia))
            return r
            
        classe_predita = None
        maior_p = -inf        
        for c in self.classes:
            #p = self.p_classe[c]
            p = np.log(self.p_classe[c])
            for a in self.atributos:
                media, variancia = self.p_atributo_classe[(a, c)]
                p_a = funcao_gausssiana(exemplo[a], media, variancia)                
                #p *= p_a
                p += np.log(p_a)
            if p > maior_p:
                classe_predita = c
                maior_p = p
                
        return classe_predita
    
    

ds = pd.read_csv("iris.data", sep=",", header=None)
ds_treino = ds.sample(100, random_state=3)
ds_teste = ds.drop(ds_treino.index)

ds_treino_d, ds_teste_d = discretizar(ds_treino, ds_teste)

sk_nb_g = GaussianNB(var_smoothing=0)
sk_nb_g.fit(ds_treino.values[:,:-1], ds_treino.values[:,-1])
sk_nb_c = CategoricalNB()
sk_nb_c.fit(ds_treino_d.values[:,:-1], ds_treino_d.values[:,-1])

nb_c = NaiveBayesCategorico(ds_treino_d)
nb_g = NaiveBayesGaussiano(ds_treino)

acertos = 0
for i in range(len(ds_teste)):
    exemplo = ds_teste.iloc[i]
    classe_verdadeira = exemplo[4]
    del exemplo[4]
    #classe_predita = sk_nb_c.predict([exemplo])[0]
    classe_predita = nb_g.predizer(exemplo)
    if classe_predita == classe_verdadeira:
        acertos += 1
        
print("Acuracia =", acertos / len(ds_teste))