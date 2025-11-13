import sys
def calcular():
    print("--- Conversor Decimal para Binário ---")
    print("Digite um número decimal para converter.")
    print("Digite 's' ou 'sair' a qualquer momento para fechar o programa.")

    while True:
        # 1. Pedir o número ao usuário
        entrada = input("\nDigite um número decimal: ")

        # 2. Verificar se o usuário quer sair
        if entrada.lower() == 's' or entrada.lower() == 'sair':
            print("Saindo do programa. Até mais!")
            break # Encerra o loop while

        # 3. Tentar converter e imprimir o resultado
        try:
            # Tenta converter a entrada (string) para um número inteiro
            numero_decimal = int(entrada)
            
            # Formata o número para binário (sem o prefixo '0b')
            numero_binario = f"{numero_decimal:b}"
            
            print(f"Decimal {numero_decimal} = Binário {numero_binario}")

        # 4. Lidar com erros se o usuário não digitar um número
        except ValueError:
            print(f"Erro: '{entrada}' não é um número inteiro válido. Tente novamente.")
if __name__ == "__calcular__":
    calcular()