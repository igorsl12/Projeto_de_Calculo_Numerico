import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import LinAlgError

# -------------------------------------------------------------------
# FUNÇÕES DE OBTENÇÃO DE DADOS
# -------------------------------------------------------------------
def obter_dados_gerais():
    """
    Pede ao usuário uma lista de pontos (x, y) e os retorna como arrays numpy.
    Usado pelas opções 1, 2 e 3.
    """
    try:
        x_str = input("Digite os valores de x separados por espaço: ")
        x = np.array([float(val) for val in x_str.split()])
        
        y_str = input("Digite os valores de y separados por espaço: ")
        y = np.array([float(val) for val in y_str.split()])
        
        if len(x) != len(y):
            print("\nErro: As listas de x e y devem ter o mesmo número de pontos.")
            return None, None
            
        if len(x) < 2:
            print("\nErro: Você precisa de pelo menos 2 pontos.")
            return None, None

        return x, y
    except ValueError:
        print("\nErro: Entrada inválida. Por favor, digite apenas números.")
        return None, None

def obter_dois_pontos():
    """
    Pede ao usuário exatamente dois pontos (x0, y0) e (x1, y1).
    Usado pela nova Opção 4.
    """
    try:
        print("\nDigite as coordenadas do primeiro ponto (P0):")
        x0 = float(input("  Digite X0: "))
        y0 = float(input("  Digite Y0: "))
        print("Digite as coordenadas do segundo ponto (P1):")
        x1 = float(input("  Digite X1: "))
        y1 = float(input("  Digite Y1: "))
        
        if np.isclose(x0, x1): # Verifica se x0 é muito próximo de x1
            print("\nErro: X0 e X1 não podem ser iguais (divisão por zero).")
            return None, None, None, None
        
        return x0, y0, x1, y1
    except ValueError:
        print("\nErro: Entrada inválida. Por favor, digite apenas números.")
        return None, None, None, None

# -------------------------------------------------------------------
# FUNÇÕES DE CÁLCULO
# -------------------------------------------------------------------

def calcular_regressao_linear_manual(x, y):
    """
    CÁLCULO MANUAL (OPÇÃO 2): Regressão Linear (Quadrados Mínimos)
    """
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    SS_xy = np.sum((x - x_mean) * (y - y_mean))
    SS_xx = np.sum((x - x_mean)**2)
    
    if SS_xx < 1e-10: 
        return None, 0, 0, 0, np.nan, np.nan, "Erro: Todos os valores de x são idênticos."
        
    B1 = SS_xy / SS_xx
    B0 = y_mean - B1 * x_mean
    
    polinomio = np.poly1d([B1, B0])
    
    y_pred = polinomio(x)
    SQE = np.sum((y - y_pred)**2)
    SQT = np.sum((y - y_mean)**2)
    
    R_quadrado = 0.0
    if SQT > 1e-10:
        R_quadrado = 1 - (SQE / SQT)
    elif SQE < 1e-10:
        R_quadrado = 1.0
        
    df = n - 2
    
    variancia_residuos = np.nan
    desvio_padrao_residuos = np.nan
    
    if df > 0:
        variancia_residuos = SQE / df
        desvio_padrao_residuos = np.sqrt(variancia_residuos)
    elif SQE < 1e-10:
        variancia_residuos = 0.0
        desvio_padrao_residuos = 0.0
            
    return polinomio, B0, B1, R_quadrado, variancia_residuos, desvio_padrao_residuos, None

def calcular_interpolacao_linear_manual(x0, y0, x1, y1):
    """
    CÁLCULO MANUAL (OPÇÃO 4): Interpolação Linear (Fórmula P1(x))
    """
    B1 = (y1 - y0) / (x1 - x0)
    B0 = y0 - B1 * x0
    polinomio = np.poly1d([B1, B0])
    return polinomio, B0, B1

def calcular_polinomio_com_polyfit(x, y, grau):
    """
    CÁLCULO COM BIBLIOTECA (OPÇÕES 1 e 3):
    """
    try:
        coeffs = np.polyfit(x, y, grau, rcond=None, full=False)
        polinomio = np.poly1d(coeffs)
        return polinomio
    except (np.linalg.LinAlgError, ValueError) as e:
        print(f"\nErro ao calcular o polinômio: {e}")
        return None

# -------------------------------------------------------------------
# FUNÇÕES DE PLOTAGEM (MODIFICADO)
# -------------------------------------------------------------------

def plotar_dispersao(x, y):
    """
    NOVA FUNÇÃO: Plota apenas o diagrama de dispersão (os pontos).
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red', label='Pontos Originais', zorder=5)
    plt.title("Diagrama de Dispersão (Apenas Pontos)")
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    print("\nExibindo gráfico de dispersão...")
    plt.show()

def plotar_grafico_completo(x, y, polinomio, titulo):
    """
    Plota os pontos originais E a curva do polinômio.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red', label='Pontos Originais', zorder=5)
    
    x_min, x_max = np.min(x), np.max(x)
    espaco_extra = (x_max - x_min) * 0.1
    if espaco_extra < 0.5: espaco_extra = 0.5
        
    x_plot = np.linspace(x_min - espaco_extra, x_max + espaco_extra, 400)
    
    y_plot = polinomio(x_plot)
    
    plt.plot(x_plot, y_plot, label=f'Curva de Ajuste (Grau {polinomio.order})')
    
    plt.title(titulo)
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    print("\nExibindo gráfico com curva de ajuste...")
    plt.show()

# -------------------------------------------------------------------
# MENU PRINCIPAL (MODIFICADO)
# -------------------------------------------------------------------
def menu():
    """
    Exibe o menu principal e gerencia a escolha do usuário.
    """
    while True:
        print("\n--- Análise de Curvas (Interpolação e Regressão) ---")
        print("1. Polinômio Interpolador (passa por TODOS os pontos)")
        print("2. Regressão Linear (Quadrados Mínimos, grau 1)")
        print("3. Regressão Polinomial (Quadrados Mínimos, grau 'm')")
        print("4. Interpolação Linear (Grau 1, entre 2 pontos) ")
        print("0. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        x_para_plotar = None
        y_para_plotar = None
        polinomio = None
        titulo = ""

        if escolha == '0':
            print("Saindo do programa. Até mais!")
            break
        
        elif escolha == '1':
            x, y = obter_dados_gerais()
            if x is None: continue
            
            x_para_plotar, y_para_plotar = x, y
            n_pontos = len(x)
            grau = n_pontos - 1
            print(f"\nCalculando Polinômio Interpolador (Grau {grau})...")
            polinomio = calcular_polinomio_com_polyfit(x, y, grau)
            titulo = "Polinômio Interpolador (Grau $n-1$)"
            
            if polinomio is not None:
                print("\nPolinômio Encontrado:")
                print(polinomio)

        elif escolha == '2':
            x, y = obter_dados_gerais()
            if x is None: continue
            
            x_para_plotar, y_para_plotar = x, y
            print("\nCalculando Regressão Linear (Manual - Quadrados Mínimos)...")
            
            polinomio, B0, B1, R_quadrado, variancia_residuos, desvio_padrao, erro_msg = calcular_regressao_linear_manual(x, y)
            titulo = "Regressão Linear (Quadrados Mínimos)"
            
            if erro_msg:
                print(erro_msg)
                polinomio = None
            
            if polinomio is not None:
                print("\n--- Resultados da Regressão Linear ---")
                print(f"B1 (Coef. Angular): {B1:.6f}")
                print(f"B0 (Coef. Linear):  {B0:.6f}")
                print(f"Equação u(x):       {polinomio}")
                print(f"R² (Coef. Determ.): {R_quadrado:.6f}")
                if not np.isnan(variancia_residuos):
                    print(f"Variância dos Resíduos (s²): {variancia_residuos:.6e}")
                    print(f"Desvio Padrão dos Resíduos (s): {desvio_padrao:.6e}")
                else:
                    print(f"Variância dos Resíduos (s²): Indefinida")
                    print(f"Desvio Padrão dos Resíduos (s): Indefinido")
                print("---------------------------------------")

        elif escolha == '3':
            x, y = obter_dados_gerais()
            if x is None: continue

            x_para_plotar, y_para_plotar = x, y
            n_pontos = len(x)
            try:
                grau_m = int(input(f"Digite o grau 'm' do polinômio (m < {n_pontos}): "))
                if grau_m >= n_pontos:
                    print(f"Erro: O grau {grau_m} é muito alto.")
                    continue
                if grau_m < 1:
                     print("Erro: O grau deve ser pelo menos 1.")
                     continue
                     
                print(f"\nCalculando Regressão Polinomial (Quadrados Mínimos, Grau {grau_m})...")
                polinomio = calcular_polinomio_com_polyfit(x, y, grau_m)
                titulo = f"Regressão Polinomial (Quadrados Mínimos, Grau {grau_m})"
                
                if polinomio is not None:
                    print("\nPolinômio Encontrado:")
                    print(polinomio)
            
            except ValueError:
                print("Erro: Grau inválido.")
                continue

        elif escolha == '4':
            x0, y0, x1, y1 = obter_dois_pontos()
            if x0 is None: continue
            
            x_para_plotar = np.array([x0, x1])
            y_para_plotar = np.array([y0, y1])
            
            print("\nCalculando Interpolação Linear (Manual - 2 Pontos)...")
            polinomio, B0, B1 = calcular_interpolacao_linear_manual(x0, y0, x1, y1)
            titulo = "Interpolação Linear (2 Pontos)"

            if polinomio is not None:
                print("\n--- Resultados da Interpolação Linear ---")
                print(f"B1 (Coef. Angular): {B1:.6f}")
                print(f"B0 (Coef. Linear):  {B0:.6f}")
                print(f"Equação P1(x):       {polinomio}")
                print("---------------------------------------")

        else:
            print("Opção inválida. Tente novamente.")
            continue

        # --- Bloco de plotagem unificado (MODIFICADO) ---
        if polinomio is not None:
            # Pergunta 1: Só os pontos
            if input("\nDeseja plotar o Diagrama de Dispersão (só os pontos)? (s/n): ").strip().lower() == 's':
                plotar_dispersao(x_para_plotar, y_para_plotar)
            
            # Pergunta 2: Pontos + Curva
            if input("\nDeseja plotar o gráfico com a curva de ajuste? (s/n): ").strip().lower() == 's':
                plotar_grafico_completo(x_para_plotar, y_para_plotar, polinomio, titulo)

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    menu()