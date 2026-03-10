from src import clientes
from src import skins
from src import compras

def menu():
    while True:
        print("\n=== MERCADO CS2 ===")
        print("1. Cadastrar Cliente")
        print("2. Listar Skins")
        print("3. Registrar Compra")
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
        elif opcao == '4': # Assumindo que a opção 2 é para Inserir Skin
            print("\n--- CADASTRAR NOVA SKIN ---")
            nome = input("Nome da Skin (Ex: AK-47 Redline): ")
            estado = input("Estado (Ex: Field-Tested): ")
            raridade = input("Raridade (Ex: Classified): ")
            pattern = int(input("Pattern (Número inteiro): "))
            wear = float(input("Wear Rating (Ex: 0.15): "))
           
            
            # Chama a função que acabámos de criar
            skins.inserir_skin(nome, estado, raridade, pattern, wear)    
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()