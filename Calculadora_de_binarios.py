def decimal_para_binario():
    print("\n--- Decimal para Binário ---")
    entrada = input("Digite um número decimal (ou 'v' para voltar): ")
    
    if entrada.lower() == 'v':
        return

    try:
        numero_decimal = int(entrada)
        # O 'b' dentro da f-string formata para binário
        numero_binario = f"{numero_decimal:b}" 
        print(f"Resultado: Decimal {numero_decimal} = Binário {numero_binario}")
        input("\nPressione Enter para continuar...")
    except ValueError:
        print(f"Erro: '{entrada}' não é um número decimal válido.")
        input("\nPressione Enter para continuar...")

def binario_para_decimal():
    print("\n--- Binário para Decimal ---")
    entrada = input("Digite um número binário (apenas 0s e 1s) (ou 'v' para voltar): ")

    if entrada.lower() == 'v':
        return

    try:
        # O '2' indica que a entrada está na base 2 (binário)
        numero_decimal = int(entrada, 2)
        print(f"Resultado: Binário {entrada} = Decimal {numero_decimal}")
        input("\nPressione Enter para continuar...")
    except ValueError:
        print(f"Erro: '{entrada}' não é um binário válido (use apenas 0 e 1).")
        input("\nPressione Enter para continuar...")

def main():
    while True:
        # Limpa a tela (opcional, printando linhas vazias para simplicidade)
        print("\n" * 2)
        print("=====================================")
        print("      CONVERSOR DE BASES NUMÉRICAS   ")
        print("=====================================")
        print("1. Decimal para Binário")
        print("2. Binário para Decimal")
        print("S. Sair")
        print("=====================================")
        
        opcao = input("Escolha uma opção: ").lower()

        if opcao == '1':
            decimal_para_binario()
        elif opcao == '2':
            binario_para_decimal()
        elif opcao == 's' or opcao == 'sair':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()