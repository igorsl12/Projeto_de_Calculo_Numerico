import numpy as np
import math
import sympy # <-- Nova importação

# -------------------------------------------------------------------
# MÉTODO 1: INTERPOLAÇÃO DE LAGRANGE
# -------------------------------------------------------------------
def interpolacao_lagrange(x, y, xi):
    """
    Calcula a interpolação de Lagrange para um dado conjunto de pontos.
    """
    n = len(x)
    yi = 0.0
    for i in range(n):
        L_i = 1.0
        for j in range(n):
            if i != j:
                L_i *= (xi - x[j]) / (x[i] - x[j])
        yi += y[i] * L_i
    return yi

# -------------------------------------------------------------------
# MÉTODO 2: MÉTODO PRÁTICO (SISTEMA LINEAR)
# -------------------------------------------------------------------
def metodo_pratico(x, y, xi):
    """
    Calcula a interpolação resolvendo o sistema linear para encontrar
    os coeficientes do polinômio P(x) = a0 + a1*x + a2*x^2 + ...
    """
    n = len(x)
    A = np.vander(x, n, increasing=True)
    try:
        coeffs = np.linalg.solve(A, y)
    except np.linalg.LinAlgError:
        return "Não foi possível resolver. A matriz é singular."
    yi = sum(coeffs[i] * (xi ** i) for i in range(n))
    return yi

# -------------------------------------------------------------------
# MÉTODO 3: NEWTON (DIFERENÇAS DIVIDIDAS - GERAL)
# -------------------------------------------------------------------
def interpolacao_newton(x, y, xi):
    """
    Calcula a interpolação usando o método de Newton com diferenças divididas.
    Esta é a forma GERAL, que funciona para pontos com espaçamento IGUAL ou DESIGUAL.
    """
    n = len(x)
    coef = np.copy(y).astype(float)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (x[i] - x[i-j])
    yi = coef[n-1]
    for i in range(n - 2, -1, -1):
        yi = yi * (xi - x[i]) + coef[i]
    return yi

# -------------------------------------------------------------------
# MÉTODO 4: GREGORY-NEWTON (DIFERENÇAS FINITAS - PONTOS IGUALMENTE ESPAÇADOS)
# -------------------------------------------------------------------
def gregory_newton_finitas(x, y, xi):
    """
    Calcula a interpolação usando a fórmula de Gregory-Newton para diferenças finitas.
    Este é o caso ESPECIAL, que funciona APENAS para pontos x IGUALMENTE espaçados.
    """
    n = len(x)
    if n < 2:
        return y[0] if n == 1 else "Erro: precisa de pelo menos 2 pontos."
    h = x[1] - x[0]
    for i in range(1, n - 1):
        if not np.isclose(x[i+1] - x[i], h):
            return (f"Erro: Os pontos x não são igualmente espaçados. "
                    f"Use o método de Newton (Diferenças Divididas).")
    delta_y = np.zeros((n, n))
    delta_y[:, 0] = y
    for j in range(1, n):
        for i in range(n - j):
            delta_y[i, j] = delta_y[i+1, j-1] - delta_y[i, j-1]
    diferencas_topo = delta_y[0]
    s = (xi - x[0]) / h
    yi = diferencas_topo[0]
    termo_s = 1.0
    for i in range(1, n):
        termo_s *= (s - (i - 1))
        termo_adicional = (termo_s * diferencas_topo[i]) / math.factorial(i)
        yi += termo_adicional
    return yi

# -------------------------------------------------------------------
# FUNÇÕES AUXILIARES
# -------------------------------------------------------------------
def obter_dados():
    try:
        x_str = input("Digite os valores de x separados por espaço: ")
        x = [float(val) for val in x_str.split()]
        y_str = input("Digite os valores de y separados por espaço: ")
        y = [float(val) for val in y_str.split()]
        if len(x) != len(y):
            print("\nErro: As listas de x e y devem ter o mesmo número de pontos.")
            return None, None, None
        xi = float(input("Digite o valor de x (xi) a ser interpolado/analisado: "))
        return x, y, xi
    except ValueError:
        print("\nErro: Entrada inválida. Por favor, digite apenas números.")
        return None, None, None

# -------------------------------------------------------------------
# FUNÇÃO DE ERRO (MODIFICADA COM CÁLCULO AUTOMÁTICO DE M)
# -------------------------------------------------------------------
def calcular_limite_erro_truncamento(x, xi):
    """
    Calcula o limite teórico do erro de truncamento, calculando M
    automaticamente a partir da função f(x) fornecida.
    """
    print("\n--- Cálculo do Limite do Erro de Truncamento ---")
    
    # n é o grau do polinômio, que é o número de pontos - 1
    n = len(x) - 1
    
    try:
        # 1. Obter a função do usuário
        f_str = input("Digite a função f(x) (ex: '2*x**4 + 3*x**2 + 1'): ")
        
        # 2. Configurar o SymPy
        x_sym = sympy.symbols('x')
        f_sym = sympy.sympify(f_str)
        
        # 3. Calcular a derivada (n+1)-ésima
        n_plus_1 = n + 1
        derivada_n_plus_1 = sympy.diff(f_sym, x_sym, n_plus_1)
        
        # 4. Converter a derivada simbólica em uma função numérica
        #    Isso é muito mais rápido para a avaliação
        f_deriv_num = sympy.lambdify(x_sym, derivada_n_plus_1, 'numpy')
        
        # 5. Encontrar o intervalo de busca para M
        #    O intervalo deve conter todos os pontos x e também xi
        todos_os_pontos_x = np.append(x, xi)
        intervalo_min = np.min(todos_os_pontos_x)
        intervalo_max = np.max(todos_os_pontos_x)
        
        # 6. Encontrar M (valor máximo) numericamente
        #    Amostramos a derivada em alta resolução (2000 pontos)
        x_amostra = np.linspace(intervalo_min, intervalo_max, 2000)
        valores_derivada = f_deriv_num(x_amostra)
        M = np.max(np.abs(valores_derivada))
        
        # 7. Calcular os outros termos da fórmula do erro
        produtorio = np.prod([(xi - val_x) for val_x in x])
        fatorial_n_mais_1 = math.factorial(n_plus_1)
        
        # 8. Calcular o limite do erro
        limite_erro = (M / fatorial_n_mais_1) * abs(produtorio)
        
        print("\n--- Resultado do Limite do Erro ---")
        print(f"Função f(x): {f_sym}")
        print(f"Derivada f^({n_plus_1})(x): {derivada_n_plus_1}")
        print(f"Intervalo de busca para M: [{intervalo_min}, {intervalo_max}]")
        print(f"Limite M (calculado): {M:.6e}")
        print(f"Grau do Polinômio (n): {n}")
        print(f"Termo do Produtório |Π(xi-xj)|: {abs(produtorio):.6e}")
        print(f"Termo do Fatorial (n+1)!: {fatorial_n_mais_1}")
        print(f"O erro de truncamento |E(xi)| é NO MÁXIMO: {limite_erro:.6e}")
        
    except sympy.SympifyError:
        print("Erro: A função digitada não é válida. Use a sintaxe do Python (ex: 'x**2' para x²).")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        print("Verifique se a função digitada está correta e se o número de pontos é adequado.")


# -------------------------------------------------------------------
# MENU PRINCIPAL (Sem mudanças aqui)
# -------------------------------------------------------------------
def menu():
    while True:
        print("\n--- Calculadora de Interpolação Polinomial ---")
        print("1. Método de Lagrange")
        print("2. Método Prático (Sistema Linear)")
        print("3. Método de Newton (Diferenças Divididas - Espaçamento qualquer)")
        print("4. Método de Gregory-Newton (Diferenças Finitas - Apenas espaçamento igual)")
        print("0. Sair")
        
        escolha = input("Escolha uma opção (ou 0 para sair): ")

        if escolha == '0':
            print("Saindo do programa. Até mais!")
            break
        
        if escolha not in ['1', '2', '3', '4']:
            print("Opção inválida. Tente novamente.")
            continue
            
        x, y, xi = obter_dados()
        
        if x is None:
            continue

        resultado = None
        metodo_nome = ""
        
        if escolha == '1':
            resultado = interpolacao_lagrange(x, y, xi)
            metodo_nome = "Lagrange"
        elif escolha == '2':
            resultado = metodo_pratico(x, y, xi)
            metodo_nome = "Prático (Sistema Linear)"
        elif escolha == '3':
            resultado = interpolacao_newton(x, y, xi)
            metodo_nome = "Newton (Diferenças Divididas)"
        elif escolha == '4':
            resultado = gregory_newton_finitas(x, y, xi)
            metodo_nome = "Gregory-Newton (Diferenças Finitas)"
            
        print("\n--- Resultado ---")
        print(f"Método Utilizado: {metodo_nome}")
        print(f"Pontos x: {x}")
        print(f"Pontos y: {y}")
        
        if isinstance(resultado, str): # Verifica se a função retornou uma string de erro
            print(f"Resultado: {resultado}")
        else:
            print(f"O valor interpolado em x = {xi} é y = {resultado:.6f}")
            
            # --- Bloco que chama a função de erro ---
            print("-------------------") 
            deseja_erro = input("\nDeseja calcular o limite do erro de truncamento (com cálculo de M)? (s/n): ").strip().lower()
            if deseja_erro == 's':
                # Chama a nova função de limite de erro
                calcular_limite_erro_truncamento(x, xi)
        
        print("-------------------")
        input("\nPressione Enter para continuar...")

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    menu()