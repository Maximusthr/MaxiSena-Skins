from src import clientes
from src import skins
from src import compras


# ================= MENU CLIENTES =================
def menu_clientes():
    while True:
        print("\n=== MENU CLIENTES ===")
        print("1. Cadastrar Cliente")
        print("2. Registrar Compra")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

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
            id_cli = int(input("ID do Cliente: "))
            id_skn = int(input("ID da Skin: "))
            valor = float(input("Valor da transação (R$): "))

            compras.registrar_compra(id_cli, id_skn, valor)

        else:
            print("Opção inválida.")


# ================= MENU SKINS =================
def menu_skins():
    while True:
        print("\n=== MENU SKINS ===")
        print("1. Listar Skins")
        print("2. Cadastrar Skin")
        print("3. Atualizar Skin")
        print("4. Deletar Skin")
        print("5. Buscar Skin por nome")
        print("6. Buscar uma Skin")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '0':
            break

        elif opcao == '1':
            skins.listar_skins()

        elif opcao == '2':
            print("\n--- CADASTRAR NOVA SKIN ---")

            nome = input("Nome da Skin: ")
            estado = input("Estado: ")
            raridade = input("Raridade: ")
            pattern = int(input("Pattern: "))
            wear = float(input("Wear Rating: "))

            skins.inserir_skin(nome, estado, raridade, pattern, wear)

        elif opcao == '3':
            print("\n--- ATUALIZAR SKIN ---")

            skins.listar_skins()

            try:
                id_atualizar = int(input("Qual ID deseja atualizar? "))

                nome = input("Nome da Skin: ")
                estado = input("Estado: ")
                raridade = input("Raridade: ")
                pattern = int(input("Pattern: "))
                wear = float(input("Wear Rating: "))

                skins.atualizar_skin(id_atualizar, nome, estado, raridade, pattern, wear)

            except ValueError:
                print("Erro: ID inválido.")

        elif opcao == '4':
            print("\n--- DELETAR SKIN ---")

            skins.listar_skins()

            try:
                id_remover = int(input("ID da skin que deseja apagar: "))

                confirmar = input("Tem certeza? (S/N): ").upper()

                if confirmar == 'S':
                    skins.deletar_skin(id_remover)
                else:
                    print("Operação cancelada.")

            except ValueError:
                print("Erro: ID inválido.")

        else:
            print("Opção inválida.")


# ================= MENU PRINCIPAL =================
def menu():
    while True:
        print("\n===== MERCADO CS2 =====")
        print("1. Clientes")
        print("2. Skins")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '0':
            print("Encerrando sistema...")
            break

        elif opcao == '1':
            menu_clientes()

        elif opcao == '2':
            menu_skins()

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()