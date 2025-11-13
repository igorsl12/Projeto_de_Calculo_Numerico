def multiplicar_matriz_vetor(matriz, vetor):
    """Multiplica uma matriz por um vetor"""
    n = len(matriz)
    m = len(vetor)
    if len(matriz[0]) != m:
        raise ValueError("Número de colunas da matriz deve ser igual ao número de linhas do vetor.")

    resultado = [0.0] * n
    for i in range(n):
        soma = 0.0
        for j in range(m):
            soma += matriz[i][j] * vetor[j]
        resultado[i] = soma
    return resultado

def multiplicar_matrizes(matriz1, matriz2):
    """Multiplica duas matrizes"""
    n1 = len(matriz1)
    m1 = len(matriz1[0])
    n2 = len(matriz2)
    m2 = len(matriz2[0])

    if m1 != n2:
        raise ValueError("Número de colunas da primeira matriz deve ser igual ao número de linhas da segunda.")

    resultado = [[0.0] * m2 for _ in range(n1)]
    for i in range(n1):
        for j in range(m2):
            soma = 0.0
            for k in range(m1):
                soma += matriz1[i][k] * matriz2[k][j]
            resultado[i][j] = soma
    return resultado

def gauss_sem_pivotacao(A, b):
    n = len(A)
    # Cria uma cópia da matriz aumentada para não modificar a original
    Ab = [row + [b[i]] for i, row in enumerate(A)]

    for i in range(n):
        if Ab[i][i] == 0:
            raise ValueError("Pivô nulo encontrado. Use a versão com pivotação.")

        pivot = Ab[i][i]
        for j in range(i, n + 1):
            Ab[i][j] /= pivot

        for k in range(i + 1, n):
            fator = Ab[k][i]
            for j in range(i, n + 1):
                Ab[k][j] -= fator * Ab[i][j]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        soma = 0.0
        for j in range(i + 1, n):
            soma += Ab[i][j] * x[j]
        x[i] = Ab[i][n] - soma
    return x

def gauss_com_pivotacao(A, b):
    n = len(A)
    Ab = [row + [b[i]] for i, row in enumerate(A)]

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(Ab[r][i]))
        if Ab[max_row][i] == 0:
            raise ValueError("Sistema impossível ou indeterminado (pivô nulo após pivotação).")
        if max_row != i:
            Ab[i], Ab[max_row] = Ab[max_row], Ab[i]

        pivot = Ab[i][i]
        for j in range(i, n + 1):
            Ab[i][j] /= pivot

        for k in range(i + 1, n):
            fator = Ab[k][i]
            for j in range(i, n + 1):
                Ab[k][j] -= fator * Ab[i][j]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        soma = 0.0
        for j in range(i + 1, n):
            soma += Ab[i][j] * x[j]
        x[i] = Ab[i][n] - soma
    return x

def decomposicao_LU(A):
    """Decomposição LU sem pivotação"""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for k in range(i, n):
            soma = 0.0
            for j in range(i):
                soma += L[i][j] * U[j][k]
            U[i][k] = A[i][k] - soma

        for k in range(i, n):
            if i == k:
                L[i][i] = 1.0
            else:
                soma = 0.0
                for j in range(i):
                    soma += L[k][j] * U[j][i]
                if U[i][i] == 0:
                    raise ValueError("Pivô nulo encontrado na decomposição LU.")
                L[k][i] = (A[k][i] - soma) / U[i][i]
    return L, U

def decomposicao_LU_pivotacao(A):
    """Decomposição LU com pivotação parcial (retorna P, L, U)"""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [row[:] for row in A]
    P = [[float(i == j) for j in range(n)] for i in range(n)]

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(U[r][i]))
        if U[max_row][i] == 0:
            raise ValueError("Matriz singular: não é possível decompor em LU.")

        U[i], U[max_row] = U[max_row], U[i]
        P[i], P[max_row] = P[max_row], P[i]
        if i > 0:
            for j in range(i):
                L[i][j], L[max_row][j] = L[max_row][j], L[i][j]

        for j in range(i + 1, n):
            L[j][i] = U[j][i] / U[i][i]
            for k in range(i, n):
                U[j][k] -= L[j][i] * U[i][k]

        L[i][i] = 1.0

    return P, L, U

def substituicao_direta(L, b):
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        soma = 0.0
        for j in range(i):
            soma += L[i][j] * y[j]
        y[i] = b[i] - soma
    return y

def substituicao_retroativa(U, y):
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = 0.0
        for j in range(i + 1, n):
            soma += U[i][j] * x[j]
        if U[i][i] == 0:
            raise ValueError("Pivô nulo encontrado na substituição retroativa.")
        x[i] = (y[i] - soma) / U[i][i]
    return x

def calcular_residuo(A, b, x):
    """Calcula o resíduo do sistema linear r = b - Ax"""
    Ax = multiplicar_matriz_vetor(A, x)
    residuo = [b[i] - Ax[i] for i in range(len(b))]
    return residuo

def resolver_por_LU(A, b):
    L, U = decomposicao_LU(A)
    y = substituicao_direta(L, b)
    x = substituicao_retroativa(U, y)
    print("\nMatriz L:")
    for linha in L:
        print(linha)
    print("\nMatriz U:")
    for linha in U:
        print(linha)
    print("\nVetor Y:", y)
    return x

def resolver_por_LU_pivotacao(A, b):
    P, L, U = decomposicao_LU_pivotacao(A)
    Pb = multiplicar_matriz_vetor(P, b)
    y = substituicao_direta(L, Pb)
    x = substituicao_retroativa(U, y)
    print("\nMatriz P:")
    for linha in P:
        print(linha)
    print("\nMatriz L:")
    for linha in L:
        print(linha)
    print("\nMatriz U:")
    for linha in U:
        print(linha)
    print("\nVetor Y:", y)
    return x

def ler_sistema():
    n = int(input("Digite a ordem da matriz (n): "))
    A = []
    print("\nDigite os coeficientes da matriz A (linha por linha):")
    for i in range(n):
        linha = list(map(float, input(f"Linha {i+1}: ").split()))
        if len(linha) != n:
            raise ValueError("Cada linha deve ter exatamente n elementos.")
        A.append(linha)

    print("\nDigite os termos independentes do vetor b:")
    b = list(map(float, input().split()))
    if len(b) != n:
        raise ValueError("O vetor b deve ter exatamente n elementos.")
    
    return A, b

def main():
    A, b = None, None

    while True:
        print("\n=== Resolução de Sistemas Lineares ===")
        print("1 - Digitar um novo sistema")
        print("2 - Resolver com método de Gauss (sem pivotação)")
        print("3 - Resolver com método de Gauss (com pivotação parcial)")
        print("4 - Resolver com decomposição LU (sem pivotação)")
        print("5 - Resolver com decomposição LU (com pivotação parcial)")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Encerrando o programa...")
            break

        elif escolha == "1":
            try:
                A, b = ler_sistema()
                print("Sistema salvo com sucesso!")
            except ValueError as e:
                print("Erro:", e)
                A, b = None, None

        elif escolha in ["2", "3", "4", "5"]:
            if A is None or b is None:
                print("Nenhum sistema foi digitado ainda. Escolha a opção 1 para inserir um sistema.")
                continue
            
            # Cria cópias de A e b para evitar modificação do sistema original
            A_copy = [row[:] for row in A]
            b_copy = b[:]

            try:
                if escolha == "2":
                    solucao = gauss_sem_pivotacao(A_copy, b_copy)
                    print("\nSolução (Gauss sem pivotação):", solucao)
                elif escolha == "3":
                    solucao = gauss_com_pivotacao(A_copy, b_copy)
                    print("\nSolução (Gauss com pivotação):", solucao)
                elif escolha == "4":
                    solucao = resolver_por_LU(A_copy, b_copy)
                    print("\nSolução (LU sem pivotação):", solucao)
                elif escolha == "5":
                    solucao = resolver_por_LU_pivotacao(A_copy, b_copy)
                    print("\nSolução (LU com pivotação parcial):", solucao)
                
                # Calcula e exibe o resíduo para as opções 2, 3, 4 e 5
                residuo = calcular_residuo(A, b, solucao)
                print("Resíduo do sistema (b - Ax):", residuo)

            except ValueError as e:
                print("Erro:", e)

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()