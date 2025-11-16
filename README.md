# Projeto de Cálculo Numérico

> Projeto acadêmico desenvolvido em Python, abordando os principais algoritmos e métodos numéricos estudados na disciplina de Cálculo Numérico.

Este projeto centraliza, através de um menu principal (`main.py`), diversas ferramentas de cálculo numérico. Cada arquivo `.py` funciona como um módulo independente que resolve um conjunto específico de problemas.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **NumPy:** Para cálculos matriciais e manipulação de arrays.
* **Matplotlib:** Para a plotagem dos gráficos de ajuste de curvas.
* **SymPy:** Para o cálculo simbólico da derivada no limite do erro de truncamento.

## 🏃 Como Executar

1.  Clone este repositório para sua máquina local.
2.  Certifique-se de ter as bibliotecas necessárias instaladas:
    ```bash
    pip install numpy matplotlib sympy
    ```
3.  Execute o arquivo principal no seu terminal:
    ```bash
    python main.py
    ```
4.  Siga as instruções do menu para escolher o módulo e o método desejado.

## 📖 Módulos e Funcionalidades

O projeto é dividido nos seguintes módulos:

### 1. Ajustes de Curvas (`Ajustes_de_curvas.py`)
Módulo focado em encontrar curvas que melhor se ajustam a um conjunto de pontos.

* **Regressão Linear (Grau 1):** Cálculo manual pelos Mínimos Quadrados.
* **Regressão Polinomial (Grau 'm'):** Ajuste polinomial de grau 'm' usando `numpy.polyfit`.
* **Interpolação Linear (2 pontos):** Cálculo da reta que passa por dois pontos exatos.
* **Plotagem:** Geração de gráficos de dispersão e da curva ajustada.

### 2. Resolução de Sistemas Lineares (`Decomposicao.py`)
Módulo para encontrar a solução de sistemas lineares `Ax = b`.

* **Eliminação de Gauss:** Com e sem pivotação parcial.
* **Decomposição LU:** Com e sem pivotação parcial (método Doolittle).
* **Cálculo de Resíduo:** Verifica a precisão da solução encontrada (`b - Ax`).

### 3. Interpolação Polinomial (`Interpolacao.py`)
Módulo para encontrar o polinômio que passa exatamente por um conjunto de pontos.

* **Método de Lagrange**
* **Método de Newton (Diferenças Divididas):** Para pontos com espaçamento qualquer.
* **Método de Gregory-Newton (Diferenças Finitas):** Otimizado para pontos igualmente espaçados.
* **Cálculo do Limite do Erro:** Calcula automaticamente o limite superior do erro de truncamento usando a derivada (n+1) da função original (via SymPy).