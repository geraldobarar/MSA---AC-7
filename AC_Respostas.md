# Avaliação Continuada 7: Respostas

Este arquivo contém as respostas para a atividade prática com MASPY e Aprendizagem por Reforço.

## 1. Metodologia SART

A seguir, são detalhados os componentes da metodologia SART (States, Actions, Rewards, Transitions) para o cenário proposto.

### Estados (States)

O estado do sistema é definido pela localização de cada um dos dois objetos (Objeto1, Objeto2). Cada objeto pode estar em uma de quatro localizações: na prateleira (P), ou em uma das três caixas (C1, C2, C3).

Com isso, o sistema possui `4 x 4 = 16` estados possíveis. Podemos representar um estado como um par `(loc_obj1, loc_obj2)`.

A lista de todos os estados é:
- **(P, P)** - Estado inicial
- (P, C1)
- (P, C2)
- (P, C3)
- (C1, P)
- (C1, C1)
- (C1, C2)
- (C1, C3)
- (C2, P)
- (C2, C1)
- (C2, C2)
- (C2, C3)
- (C3, P)
- (C3, C1)
- (C3, C2)
- (C3, C3)

### Ações (Actions)

O agente pode realizar 6 ações distintas para mover um objeto da prateleira para uma das caixas:
1.  `alocar(Obj1, C1)`: Mover Objeto 1 para a Caixa 1.
2.  `alocar(Obj1, C2)`: Mover Objeto 1 para a Caixa 2.
3.  `alocar(Obj1, C3)`: Mover Objeto 1 para a Caixa 3.
4.  `alocar(Obj2, C1)`: Mover Objeto 2 para a Caixa 1.
5.  `alocar(Obj2, C2)`: Mover Objeto 2 para a Caixa 2.
6.  `alocar(Obj2, C3)`: Mover Objeto 2 para a Caixa 3.

Uma ação de alocação de um objeto que já foi alocado é considerada inválida.

### Recompensas (Rewards)

As recompensas são atribuídas quando o agente executa uma ação que move um objeto da prateleira para uma caixa.

- `alocar(Obj1, C1)` → **r = +5**
- `alocar(Obj1, C2)` → **r = -5**
- `alocar(Obj1, C3)` → **r = +7**
- `alocar(Obj2, C1)` → **r = -5**
- `alocar(Obj2, C2)` → **r = +5**
- `alocar(Obj2, C3)` → **r = -2**

O objetivo do agente de aprendizagem é encontrar uma sequência de ações (política) que maximize a soma total das recompensas. A política ótima é alocar o **Objeto 1 na Caixa 3 (r=+7)** e o **Objeto 2 na Caixa 2 (r=+5)**, resultando em uma recompensa total de **+12**.