# Alocador de Objetos com Aprendizagem por Reforço (Q-Learning)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MASPY](https://img.shields.io/badge/Library-MASPY-green)
![Status](https://img.shields.io/badge/Status-Concluído-success)

Este repositório contém a implementação de um projeto que consiste em um agente inteligente que utiliza **Aprendizagem por Reforço (Q-Learning)** para aprender a alocar objetos em caixas específicas, maximizando a recompensa acumulada.

## 📋 Descrição do Cenário

O ambiente simula um robô alocador que deve mover **2 objetos** (inicialmente em uma prateleira) para uma de **3 caixas** disponíveis (Caixa 1, Caixa 2 ou Caixa 3)[cite: 11, 12].

O objetivo do agente é descobrir, através de tentativa e erro (treinamento), qual caixa oferece a maior recompensa para cada objeto.

### Tabela de Recompensas

[cite_start]As regras de pontuação definidas para o ambiente são:

| Ação (Alocar) | Destino: Caixa 1 | Destino: Caixa 2 | Destino: Caixa 3 |
| :--- | :---: | :---: | :---: |
| **Objeto 1** | +5 | -5 | **+7 (Ótimo)** |
| **Objeto 2** | -5 | **+5 (Ótimo)** | -2 |

O comportamento ótimo esperado é que o agente aprenda a colocar o **Objeto 1 na Caixa 3** e o **Objeto 2 na Caixa 2**, totalizando uma recompensa de **12**.

## 🧠 Metodologia SART

A modelagem do problema seguiu a metodologia SART (*States, Actions, Rewards, Transitions*), conforme detalhado no arquivo `AC_Respostas.md`:

* **Estados:** 16 estados possíveis (combinação das 4 posições possíveis para cada um dos 2 objetos).
* **Ações:** 6 ações de movimento (mover Objeto 1 ou 2 para C1, C2 ou C3).
* **Algoritmo:** Q-Learning (implementado via biblioteca `maspy`).
* **Treinamento:** 15.000 episódios para garantir a convergência da tabela Q.

## 🚀 Como Executar

### Pré-requisitos
* Python 3.x instalado.
* Biblioteca `maspy` (certifique-se de que a pasta `maspy` esteja no diretório raiz ou instalada no ambiente).

### Saída Esperada
O script executará duas fases:
1.  **Fase de Treinamento:** O agente explora o ambiente por 15.000 episódios para preencher a Q-Table.
2.  **Fase de Execução (Inferência):** O agente utiliza a política aprendida ("cérebro") para realizar a alocação ótima em tempo real.

Exemplo de log no terminal:
```text
============================================================
DATA E HORA DA EXECUÇÃO: DD/MM/AAAA HH:MM:SS
ALUNO: Geraldo e Romário
============================================================

>>> INICIANDO TREINAMENTO (Q-LEARNING)...
>>> TREINAMENTO CONCLUÍDO.

>>> EXECUTANDO O AGENTE TREINADO (Modo Inferência)...
Robo_Alocador: Mover Objeto 2 -> CX 2 | Recompensa: 5 | (Decisão Ótima? SIM)
Robo_Alocador: Mover Objeto 1 -> CX 3 | Recompensa: 7 | (Decisão Ótima? SIM)

```

## 📝 Metodologia SART

A metodologia SART (States, Actions, Rewards, Transitions) foi utilizada para modelar o problema:

* **States (Estados):** 16 combinações possíveis de localização dos dois objetos (Prateleira, C1, C2, C3).
* **Actions (Ações):** 6 movimentos possíveis (Mover Obj1 ou Obj2 para uma das 3 caixas).
* **Rewards (Recompensas):** Valores atribuídos conforme a tabela de pontuação, variando de -5 a +7.
* **Transitions (Transições):** Lógica determinística que atualiza o estado do ambiente após cada ação.

Para a documentação completa e detalhada, consulte o arquivo [AC_Respostas.md](./AC_Respostas.md).
