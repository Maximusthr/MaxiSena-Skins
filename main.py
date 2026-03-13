from src import clientes
from src import skins
from src import compras

def menu():
    while True:
        print("\n=== MERCADO CS2 ===")
        print("1. Cadastrar Cliente")
        print("2. Listar Skins")
        print("3. Registrar Compra")
        print("4. Cadastrar nova skin")
        print("5. Atualizar skin")
        print("6. Deletar skin")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '0':
            break
        elif opcao == '1':
            nome = input("Nome: ")
            cpf = input("CPF: ")
            email = input("Email: ")
            cidade = input("Cidade: ")
            telefone = input("Telefone: ")
            clientes.cadastrar_cliente(nome, cpf, email, cidade, telefone)
        elif opcao == '2':
            skins.listar_skins()
        elif opcao == '3':
            id_cli = int(input("ID do Cliente: "))
            id_skn = int(input("ID da Skin: "))
            valor = float(input("Valor da transação (R$): "))
            compras.registrar_compra(id_cli, id_skn, valor)
        elif opcao == '4': 
            print("\n--- CADASTRAR NOVA SKIN ---")
            nome = input("Nome da Skin (Ex: AK-47 Redline): ")
            estado = input("Estado (Ex: Field-Tested): ")
            raridade = input("Raridade (Ex: Classified): ")
            pattern = int(input("Pattern (Número inteiro): "))
            wear = float(input("Wear Rating (Ex: 0.15): "))
           
            
            skins.inserir_skin(nome, estado, raridade, pattern, wear)
        elif opcao == '5':
            print("\n--- ATUALIZAR SKIN ---")
            nome = input("Nome da Skin (Ex: AK-47 Redline): ")
            estado = input("Estado (Ex: Field-Tested): ")
            raridade = input("Raridade (Ex: Classified): ")
            pattern = int(input("Pattern (Número inteiro): "))
            wear = float(input("Wear Rating (Ex: 0.15): "))

            skins.atualizar_skin(nome, estado, raridade, pattern, wear)

        elif opcao == '6':
            print("\n" + "="*30)
            print("   DELETAR SKIN DO STOCK")
            print("="*30)
            
            print("Skins disponíveis no sistema:")
            skins.listar_skins() 
            
            print("-" * 30)
            
            try:
                id_remover = int(input("\nIntroduza o ID da skin que deseja apagar: "))
                
                confirmar = input(f"Tem a certeza que deseja remover o ID {id_remover}? (S/N): ").upper()
                
                if confirmar == 'S':
                    skins.deletar_skin(id_remover)
                else:
                    print(" Operação cancelada pelo utilizador.")
                    
            except ValueError:
                print(" Erro: Por favor, insira um número de ID válido (ex: 1, 2, 5).")    
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()