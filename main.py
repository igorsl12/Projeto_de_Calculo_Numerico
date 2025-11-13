# 1. Importa os outros arquivos como módulos
import Interpolacao
import Decomposicao
import Ajustes_de_curvas  # <-- Note o nome corrigido, sem .py

def exibir_menu_principal():
    """
    Exibe o menu principal do projeto de Cálculo Numérico.
    """
    while True:
        print("\n=========================================")
        print("--- PROJETO DE CÁLCULO NUMÉRICO ---")
        print("=========================================")
        print("1. Módulo de Interpolação")
        print("2. Módulo de Decomposição (Sistemas Lineares)")
        print("3. Módulo de Ajuste de Curvas")
        print("0. Sair do Programa")

        escolha = input("\nEscolha o módulo que deseja usar: ").strip()

        if escolha == '1':
            print("\n...Iniciando Módulo de Interpolação...")
            # 2. Chama a função 'menu' do arquivo Interpolacao.py
            Interpolacao.menu() 
            print("\n...Módulo de Interpolação finalizado. Retornando ao menu principal...")

        elif escolha == '2':
            print("\n...Iniciando Módulo de Decomposição...")
            # 2. Chama a função 'main' do arquivo Decomposicao.py
            Decomposicao.main() 
            print("\n...Módulo de Decomposição finalizado. Retornando ao menu principal...")

        elif escolha == '3':
            print("\n...Iniciando Módulo de Ajuste de Curvas...")
            # 2. Chama a função 'menu' do arquivo Ajustes_de_curvas.py
            Ajustes_de_curvas.menu() 
            print("\n...Módulo de Ajuste de Curvas finalizado. Retornando ao menu principal...")

        elif escolha == '0':
            print("Encerrando o programa principal. Até mais!")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")

# 3. Ponto de entrada do programa principal
if __name__ == "__main__":
    exibir_menu_principal()