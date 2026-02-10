- [Exercícios](#exercicios)
	- [Exercício 3.1](#exercicio-3.1)
	- [Exercício 3.2](#exercicio-3.2)

# Resumo

No Russell:

- **Objetivo** → condição desejada
- **Estado objetivo** → estado que satisfaz essa condição
- **Solução** → sequência de ações/estados que leva ao estado objetivo


# Exercícios

### Exercício 3.1  
**Defina com suas próprias palavras os termos a seguir:**
- **Estados:** dado um problema, um estado é uma descrição de um conjuntos de propriedades relevantes que representa uma configuração possível do mundo naquele momento. A partir de um estado, a execução de uma ação válida leva o sistema a outro estado, conforme definido pelo modelo de transição do problema.
  Por exemplo, em um problema de navegação entre cidades, cada cidade (ou posição no mapa) pode ser representada por um estado. Uma ação corresponde deslocar-se de uma cidade para outra conectada, fazendo com que o agente transite de um estado para outro.
  A solução para o problema não é um estado, mas uma sequência de ações (ou estados) que leva do **estado inicial** ao **estado objetivo**.
- **Espaço de Estados:** é o conjunto de todos os estados possíveis que podem ser alcançado a partir do estado inicial por meio das ações permitidas, considerando apenas as propriedades relevantes para a definição e a resolução do problema.
- **Árvore de Busca:** é uma estrutura em forma de árvore gerada a partir do estado inicial, na qual cada nó representa um estado alcançável e cada aresta representa a aplicação de uma ação. A árvore é construída pela aplicação recursiva de todas as ações possíveis a partir de cada estado, podendo conter múltiplos nós que representam o mesmo estado do espaço de estados. 
- **Objetivo:** é a condição que determina quais estados  do espaço de estados são considerados satisfatórios para o problema. Um estado que satisfaz essa condição é chamado de estado objetivo, e uma solução é o caminho que leva do estado inicial ao estado objetivo.
- **Ação:** É uma operação disponível ao agente em um determinado estado que, quando executada, provoca uma transição para outro estado, alterando a configuração do mundo conforme o modelo de transição do problema.
- **Função sucessor:** Dado um estado, a função sucessor retorna o conjunto de pares _(ação, estado resultante)_ que podem ser obtidos pela aplicação de cada ação válida naquele estado.
- **Fator de Ramificação:** é o número de ações disponíveis em um estado, ou equivalentemente, o número de pares (ação, estado resultante) que a função sucessor pode retornar para um estado.

### Exercício 3.2
**Explique por que a formulação do problema deve seguir a formulação do objetivo.**

A formulação do problema deve seguir a formulação do objetivo porque **o objetivo define quais estados do espaço de estados são desejáveis.** O objetivo não é uma sequência de estados ou ações, mas uma condição que caracteriza os estados objetivo. 
Para que uma solução possa ser encontrada, a formulação do problema deve representar o mundo por meio de estados que permitam verificar essa condição. Caso contrário, o agente pode buscar soluções ótimas para uma formulação que não corresponde ao objetivo desejado.
🔑 **O objetivo define o que é desejável; a formulação define o que é possível.**

### Exercício 3.3
**Suponha que AÇÕES-VÁLIDAS(s) denote o conjunto de ações válidas no estado s, e que RESULTADO(a, s) denote o estado que resulta da execução de uma ação válida *a* no estado *s*. Defina SUCESSOR em termos de AÇÕES VÁLIDAS e RESULTADO, e vice-versa.**
$$ SUCESSOR(s) = \{(a_0, {RESULTADO}(a_0, s)) | a_0 \in {AÇÕES-VÁLIDAS}(s)\} $$

