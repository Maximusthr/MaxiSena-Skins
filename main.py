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

    tipo_skin = {1: "AK-47", 2: "AWP", 3: "DESERT EAGLE",
                 4: "FACA", 5: "GLOCK", 6: "LUVA", 7: "M4A4",
                 8: "M4A1-S", 9: "USP"}

    while True:
        print("\n=== MENU SKINS ===")
        print("1. Listar + Relatorio Skins")
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
            print("\nComo deseja ordenar as skins?")
            print("1 - Crescente (mais barata → mais cara)")
            print("2 - Decrescente (mais cara → mais barata)")
            print("3 - Ordem de inserção")

            op = input("Escolha: ")

            if op == '1':
                skins.listar_skins("crescente", op)

            elif op == '2':
                skins.listar_skins("decrescente", op)

            elif op == '3':
                skins.listar_skins("insercao", op)

            else:
                print("Opção inválida.")

        elif opcao == '2':
            print("\n--- CADASTRAR NOVA SKIN ---")

            print(f"Digite o tipo da skin: \n")
            for index, nome_skin in tipo_skin.items():
                print(f"{index} - {nome_skin}")
            
            tipo = 0
            while True:
                try:
                    tipo = int(input("\nDigite o número do tipo da skin: "))
                    
                    if tipo in tipo_skin:
                        break 
                    else:
                        print("Opção inválida. Escolha um número que esteja na lista.")
                        
                except ValueError:
                    print("Entrada inválida. Por favor, digite apenas números inteiros.")


            nome = input("Nome da Skin: ")
            valor = float(input("Valor (R$): "))
            estado = input("Estado: ")
            raridade = input("Raridade: ")
            pattern = int(input("Pattern: "))
            wear = float(input("Wear Rating: "))

            skins.inserir_skin(tipo_skin[tipo], nome, valor, estado, raridade, pattern, wear)

        elif opcao == '3':

            quantidade = skins.listar_skins("id", '6')

            if (quantidade == 0):
                print("\nVoltando pro menu.")
                continue

            print("\nComo deseja atualizar?")
            print("1 - Atualizar todos os atributos")
            print("2 - Atualizar apenas um atributo")

            op = input("Escolha: ")

            if op == '1':
                id = int(input("ID da skin: "))

                print(f"TIPOS: \n")
                for index, nome_skin in tipo_skin.items():
                    print(f"{index} - {nome_skin}")

                tipo = 0
                while True:
                    try:
                        tipo = int(input("\nDigite o número do tipo da skin: "))
                        
                        if tipo in tipo_skin:
                            break 
                        else:
                            print("Opção inválida. Escolha um número que esteja na lista.")
                            
                    except ValueError:
                        print("Entrada inválida. Por favor, digite apenas números inteiros.")

                nome = input("Nome: ")
                valor = float(input("Valor: "))
                estado = input("Estado: ")
                raridade = input("Raridade: ")
                pattern = int(input("Pattern: "))
                wear = float(input("Wear rating: "))

                skins.atualizar_skin_completa(id, tipo_skin[tipo], nome, valor, estado, raridade, pattern, wear)
                 
            elif op == '2':
                id = int(input("ID da skin: "))

                print("\nQual atributo deseja alterar?")
                print("1 Tipo")
                print("2 Nome")
                print("3 Valor")
                print("4 Estado")
                print("5 Raridade")
                print("6 Pattern")
                print("7 Wear rating")

                escolha = input("Escolha: ")

                atributos = {
                    '1': ('tipo', str),
                    '2': ('nome', str),
                    '3': ('valor', float),
                    '4': ('estado', str),
                    '5': ('raridade', str),
                    '6': ('pattern', int),
                    '7': ('wear_rating', float)
                }

                selecao = atributos.get(escolha)

                if selecao:
                    nome_atributo = selecao[0]
                    tipo_valor = selecao[1]

                    valor = input(f"Novo valor para {nome_atributo}: ")

                    try:
                        novo_valor_convertido = tipo_valor(valor)
                        
                        skins.atualizar_um_atributo(id, nome_atributo, novo_valor_convertido)
                        
                    except ValueError:
                        print(f"\nErro: O valor '{valor}' não é válido para {nome_atributo}.")
                        print(f"Por favor, insira um dado do tipo {tipo_valor.__name__}.")
                else:
                    print("Opção inválida.")   
                 
                                
        elif opcao == '4':
            
            print("\n--- DELETAR SKIN ---")

            quantidade = skins.listar_skins("crescente", opcao)
            
            if (quantidade == 0):
                print("\nVoltando pro menu")
                continue

            try:
                id_remover = int(input("ID da skin que deseja apagar: "))

                confirmar = input("Tem certeza? (S/N): ").upper()

                if confirmar == 'S':
                    skins.deletar_skin(id_remover)
                else:
                    print("Operação cancelada.")

            except ValueError:
                print("Erro: ID inválido.")
        elif opcao == '5': 
            nome_busca = input("\nDigite o nome (ou parte do nome) da skin: ")
            skins.pesquisar_skin_por_nome(nome_busca)

        elif opcao == '6': 
            try:
                quantidade = skins.listar_skins("id", opcao)
                if (quantidade == 0):
                    print("Voltando pro menu")
                    continue

                id_busca = int(input("\nDigite o ID exato da skin para ver detalhes: "))
                skins.exibir_uma_skin(id_busca)
            except ValueError:
                print(" Erro: Insira um número de ID válido.")
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