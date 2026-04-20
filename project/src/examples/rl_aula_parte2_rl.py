import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

# Código da classe MDP é uma modificação sobre o código utilizado pelo Prof. Denis Fantinato - Inteligência Artificial (2021.Q2)
class MDP:
    def __init__(self):
        S = [(i,j) for i in range(1,5) 
                        for j in range(1,4) if (i,j) != (2,2)]
        self.S = S
            
        acoes = ["UP", "DOWN", "LEFT", "RIGHT"]
        A = {s : acoes for s in S if not self.terminal(s)}
        self.A = A
        
        R = {s : -0.04 for s in S}
        R[(4,3)] =  1
        R[(4,2)] = -1
        self.R = R

        self.P = { (s,a) : self._pvals(s, a, S) for s in S if not self.terminal(s) for a in A[s] }        
       
    def executar_acao(self, s, a):
        ps = self.P[(s, a)]
        probs = list(map(lambda x: x[0], ps))
        estados = list(map(lambda x: x[1], ps))
        idx = np.random.choice(len(estados), p=probs)
        
        s_novo = estados[idx]
        r = self.R[s_novo]
        
        return s_novo, r
    
    def terminal(self, s):
        return (s in [(4,3), (4,2)])
    
    def _succ(self, a):
        return {"UP": "RIGHT", "DOWN": "LEFT", "RIGHT": "DOWN", "LEFT": "UP"}[a]

    def _pred(self, a):
        return {"UP": "LEFT", "DOWN": "RIGHT", "RIGHT": "UP", "LEFT": "DOWN"}[a]

    def _pvals(self, s, a, S):
        return [(0.8, self._move(s, a, S)), (0.1, self._move(s, self._succ(a), S)), (0.1, self._move(s, self._pred(a), S))]

    def _move(self, s, a, S):
        i, j = s
        if a == "UP":
            sp = (i, j+1)
        elif a == "DOWN":
            sp = (i, j-1)
        elif a == "LEFT":
            sp = (i-1, j)
        elif a == "RIGHT":
            sp = (i+1, j)
        elif a is None:
            return s

        if sp in S:
            return sp

        return s
    
    
    
def q_valor(s, a, mdp, U, gamma):
    P = mdp.P
    R = mdp.R
    
    q = 0
    for prob, s_prox in P[(s, a)]:
        q += (prob * (R[s_prox] + gamma * U[s_prox]))
    return q


def iteracao_valor(mdp, gamma = 1, eps = 0.001):
    S = mdp.S
    A = mdp.A
    
    U_linha = {s : 0.0 for s in S}
    
    #grafico
    valores = {s : [0] for s in S}
    
    # tabela iterações
    i = 0
    
    delta = eps * (1 - gamma) / gamma + 1
    while delta > eps * (1 - gamma) / gamma:
        U = deepcopy(U_linha)
        delta = 0
        for s in S: # para cada estado
            if (mdp.terminal(s)):
                continue
            U_linha[s] = max([q_valor(s, a, mdp, U, gamma) for a in A[s]])
            delta = max(delta, abs(U_linha[s] - U[s]))
            valores[s].append(U_linha[s])
        
        # tabela iterações (mostra após 5 iterações)
        if i < 5:
            imprimir_U(mdp, U_linha)
            i += 1
    
    #grafico
    plt.figure()
    for s in S:
        if not mdp.terminal(s):
            plt.plot(valores[s], label=str(s))
    plt.legend()
        
    U = U_linha
    return U
    

def avaliar_politica(mdp, politica, gamma, eps = 0.001):
    S = mdp.S
    
    U_linha = { s : 0.0 for s in S}
    
    delta = eps * (1 - gamma) / gamma + 1
    while delta > eps * (1 - gamma) / gamma:
        U = deepcopy(U_linha)
        delta = 0
        for s in S: # para cada estado
            if (mdp.terminal(s)):
                continue
            a = politica[s]
            U_linha[s] = q_valor(s, a, mdp, U, gamma)
            delta = max(delta, abs(U_linha[s] - U[s]))
    
    U = U_linha
    return U


def iteracao_politica(mdp, gamma = 1, eps = 0.001):
    S = mdp.S
    A = mdp.A
    
    # Politica inicial
    pi = {s : A[s][0] for s in S if not mdp.terminal(s)}
    
    i = 0
    
    mudou = True
    while mudou:
        mudou = False
        U = avaliar_politica(mdp, pi, gamma)
        
        #if i < 5:
        #    imprimir_politica(mdp, pi)
        #    i += 1
        
        for s in S:            
            if (mdp.terminal(s)):
                continue
            q_valor_pi_atual = q_valor(s, pi[s], mdp, U, gamma)
            
            melhor_acao = A[s][0]
            melhor_q_valor = float("-inf")
            for a in A[s]:
                q_valor_atual = q_valor(s, a, mdp, U, gamma)
                if q_valor_atual > melhor_q_valor:
                    melhor_acao = a
                    melhor_q_valor = q_valor_atual
                    
            if melhor_q_valor > q_valor_pi_atual:
                pi[s] = melhor_acao
                mudou = True
        
    return pi



def imprimir_U(mdp, U):
    print("------------------------------------------------")
    for y in range(3, 0, -1):
        for x in range(1, 5):
            if (x,y) in U:
                if (not mdp.terminal((x,y))):
                    if U[(x,y)] >= 0:
                        print("|  ", end="")
                    else:
                        print("| ", end="")                    
                    print("{:.4f}  |".format(U[(x,y)]), end="")                    
                else:
                    print("|          |", end="")
            else:
                print("|          |", end="")
        print("")
    print("------------------------------------------------")
        
def imprimir_politica(mdp, pi):
    print("--------------------------------------------")
    for y in range(3, 0, -1):
        for x in range(1, 5):
            if (x,y) in mdp.S:
                if (not mdp.terminal((x,y))):
                    print("|  {:>5}  |".format(pi[(x,y)]), end="")
                else:
                    print("|         |", end="")
            else:
                print("|         |", end="")
        print("") 
    print("--------------------------------------------")
        
        
        
        
        
        
def calcular_utilidade(recompensas, inicio, gamma):
    soma = 0
    for i in range(inicio, len(recompensas)):
        s, r, s_prox = recompensas[i]
        soma += r * (gamma ** (i - inicio))
    return soma
        

def estimativa_direta(mdp, pi, gamma = 1, n_testes = 10000):
    S = mdp.S
    
    s0 = (1,1)   
    
    qtd_visitados = {s : 0 for s in S}
    soma_u_visitados = {s : 0 for s in S}
    
    iteracao = 0
    
    for _ in range(n_testes):
        recompensas = []
        
        s = s0
        while (not mdp.terminal(s)):
            a = pi[s]
            s_prox, r = mdp.executar_acao(s, a)
            recompensas.append( (s, r, s_prox) )
            s = s_prox
            
        for i in range(len(recompensas)):
            s, r, s_prox = recompensas[i]
            u = calcular_utilidade(recompensas, i, gamma)
            qtd_visitados[s] += 1
            soma_u_visitados[s] += u
            
        if iteracao < 5:
            print(recompensas)
            iteracao += 1
    
    U = {s : 0 for s in S}
    for s in S:        
        if qtd_visitados[s] > 0:
            U[s] = soma_u_visitados[s] / qtd_visitados[s]

    return U



from sklearn.linear_model import LinearRegression
from sklearn import tree

def extrair_atributos(s):
    return [s[0], s[1], np.sqrt((s[0] - 4)**2 + (s[1] - 3)**2)]

def estimativa_direta_regressao(mdp, pi, gamma = 1, n_testes = 1000):
    S = mdp.S
    
    s0 = (1,1)
    
    dataX = []
    dataY = []
    
    for _ in range(n_testes):
        recompensas = []
        
        s = s0
        while (not mdp.terminal(s)):
            a = pi[s]
            s_prox, r = mdp.executar_acao(s, a)
            recompensas.append( (s, r, s_prox) )
            s = s_prox
            
        for i in range(len(recompensas)):
            s, r, s_prox = recompensas[i]
            u = calcular_utilidade(recompensas, i, gamma)
            dataX.append(extrair_atributos(s))
            dataY.append(u)
    
    #regressor = LinearRegression()
    regressor = tree.DecisionTreeRegressor()
    regressor.fit(dataX, dataY)
    U = {s : 0 for s in S}
    for s in S:        
        U[s] = regressor.predict([extrair_atributos(s)])[0]

    return U


def diferenca_temporal(mdp, pi, alpha = 0.1, gamma = 1, n_testes = 5000):
    S = mdp.S
    
    s0 = (1,1)   
    
    U = {s : 0 for s in S}
    N = {s : 0 for s in S}
    
    #grafico
    valores = {s : [0] for s in S}
    
    for _ in range(n_testes):
        s = s0
        while (not mdp.terminal(s)):
            a = pi[s]
            s_prox, r = mdp.executar_acao(s, a)
            N[s] += 1
            #U[s] = U[s] + alpha * (r + gamma * U[s_prox] - U[s])
            U[s] = U[s] + (60 / (59 + N[s])) * (r + gamma * U[s_prox] - U[s])
            valores[s].append(U[s])
            s = s_prox
            
    #grafico
    plt.figure()
    for s in S:
        if not mdp.terminal(s):
            plt.plot(valores[s], label=str(s))
    plt.legend()
    
    return U



from collections import defaultdict

def get_max_Q(Q, s, A):
    max_q = -float("inf")
    max_a = None
    for a in A[s]:
        q_atual = Q[(s, a)]
        if (q_atual > max_q):
            max_q = q_atual
            max_a = a
    return max_a, max_q

def get_acao_q_learning(N, Q, s, A):
    for a in A[s]:
        if N[(s,a)] < 10:
            return a
    
    max_a, max_q = get_max_Q(Q, s, A)       
    return max_a

def q_learning(mdp, gamma = 0.9, n_testes = 50000):
    S = mdp.S
    A = mdp.A
    
    s0 = (1,1)   
    
    Q = defaultdict(float)
    N = defaultdict(float)
    
    for _ in range(n_testes):
        s = s0
        a = None
        while (not mdp.terminal(s)):
            a = get_acao_q_learning(N, Q, s, A)
            s_prox, r = mdp.executar_acao(s, a)
        
            N[(s,a)] += 1
            if (mdp.terminal(s_prox)):
                max_q_prox = 0
            else:
                max_q_prox = max(Q[(s_prox, a_prox)] for a_prox in A[s_prox])
                
            alpha = (60 / (59 + N[(s,a)]))
            Q[(s,a)] = Q[(s,a)] + alpha * (r + gamma * max_q_prox - Q[(s,a)])
            
            s = s_prox
    
    pi = { s : None for s in S}
    for s in S:
        if not mdp.terminal(s):
            max_a, max_q = get_max_Q(Q, s, A)
            pi[s] = max_a
    
    return pi




    
def main_parte2_estimativa_direta():
    mdp = MDP()
    
    pi = iteracao_politica(mdp)
    
    print("Estimativa Direta:")
    U = estimativa_direta(mdp, pi)
    imprimir_U(mdp, U)
    
    print("Estimativa Direta (com regressão):")
    U = estimativa_direta_regressao(mdp, pi)
    imprimir_U(mdp, U)
    
    
def main_parte2_diferenca_temporal():
    mdp = MDP()
    
    pi = iteracao_politica(mdp)
    
    print("Diferenca temporal:")
    U = diferenca_temporal(mdp, pi)
    imprimir_U(mdp, U)
    
   
def main_parte2_q_learning():
    mdp = MDP()
    
    print("Q-Learning:")
    pi = q_learning(mdp)
    imprimir_politica(mdp, pi)


main_parte2_estimativa_direta()
main_parte2_diferenca_temporal()
main_parte2_q_learning()
