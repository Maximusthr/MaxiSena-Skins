from src.database import get_conexao

def inserir_skin(tipo ,nome, valor, estado, raridade, pattern, wear_rating):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO Skins (tipo ,nome, valor, estado, raridade, pattern, wear_rating) 
                VALUES (%s ,%s, %s, %s, %s, %s , %s)
            """
            valores = (tipo , nome, valor, estado, raridade, pattern, wear_rating)
            
            cursor.execute(sql, valores)
            conn.commit()
            
            print(f"\nSucesso! A skin '{nome}' foi inserida no banco.")
            
        except Exception as e:
            print(f"\nErro ao inserir a skin: {e}")
            conn.rollback()
             
        finally:
            cursor.close()
            conn.close()

def atualizar_skin_completa(id, tipo, nome, valor, estado, raridade, pattern, wear_rating):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()

            sql = """
                UPDATE Skins
                SET tipo = %s, nome = %s, valor = %s, estado = %s,
                    raridade = %s, pattern = %s, wear_rating = %s
                WHERE id_skins = %s
            """

            valores = (tipo, nome, valor, estado, raridade, pattern, wear_rating, id)

            cursor.execute(sql, valores)

            if cursor.rowcount > 0:
                print(f"\nSkin ID {id} atualizada!")

            else:
                print(f"\nNenhuma skin encontrada com ID {id}")

            conn.commit()

        except Exception as e:
            print("Erro ao atualizar skin.")
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

def atualizar_um_atributo(id, atributo, novo_valor):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()

            sql = f"UPDATE Skins SET {atributo} = %s WHERE id_skins = %s"

            cursor.execute(sql, (novo_valor, id))

            if cursor.rowcount > 0:
                print(f"\nAtributo {atributo} atualizado!")

            else:
                print("Skin não encontrada.")

            conn.commit()

        except Exception as e:
            print("Erro ao atualizar atributo.")
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

def listar_skins(tipo_ordem):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()

            if tipo_ordem == "crescente":
                query = "SELECT id_skins, tipo, nome, valor, estado FROM Skins ORDER BY valor ASC"


            elif tipo_ordem == "decrescente":
                query = "SELECT id_skins, tipo, nome, valor, estado FROM Skins ORDER BY valor DESC"

            else:  
                query = "SELECT id_skins, tipo, nome, valor, estado FROM Skins ORDER BY id_skins ASC"

                

            cursor.execute(query)
            skins = cursor.fetchall()

            if len(skins) == 0:
                print("\nNenhuma skin cadastrada.")

            else:
                print("\n===== LISTA DE SKINS =====")

                for skin in skins:
                    print(f"ID: {skin[0]} | Tipo: {skin[1]} | Nome: {skin[2]} | Preço: {skin[3]} | Estado: {skin[4]}")

                gerar_relatorio(cursor)
            return len(skins)

        except Exception as e:
            print(f"Erro ao listar skins: {e}")
            return 0

        finally:
            cursor.close()
            conn.close()

def deletar_skin(id_skins):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            
            sql = "DELETE FROM Skins WHERE id_skins = %s"
            
            cursor.execute(sql, (id_skins,))
            
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"\n Sucesso! A skin com ID {id_skins} foi removida do sistema.")
            else:
                print(f"\n Aviso: Nenhuma skin encontrada com o ID {id_skins}.")
                
        except Exception as e:
            print(f"\n Erro ao eliminar skin: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            
def pesquisar_skin_por_nome(nome_pesquisa):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            
            sql = "SELECT id_skins, tipo , nome, estado, valor FROM Skins WHERE nome ILIKE %s"
            cursor.execute(sql, (f"%{nome_pesquisa}%",))
            
            skins = cursor.fetchall()
            
            if skins:
                print(f"\nResultados para '{nome_pesquisa}':")
                for s in skins:
                    print(f"ID: {s[0]} | Tipo: {s[1]} | Nome: {s[2]} | Estado: {s[3]} | Valor: R$ {s[4]}")
            else:
                print(f"\n Nenhuma skin encontrada com o nome '{nome_pesquisa}'.")
        except Exception as e:
            print(f"Erro na pesquisa: {e}")
        finally:
            cursor.close()
            conn.close()

def exibir_uma_skin(id_skin):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Skins WHERE id_skins = %s", (id_skin,))
            skin = cursor.fetchone()
            
            if skin:
                print("\n--- DETALHES DA SKIN ---")
                print(f"ID: {skin[0]}")
                print(f"TIPO: {skin[1]}")
                print(f"Nome: {skin[2]}")
                print(f"Valor: R$ {skin[3]}")
                print(f"Estado: {skin[4]}")
                print(f"Raridade: {skin[5]}")
                print(f"Pattern: {skin[6]}")
                print(f"Wear Rating: {skin[7]}")
            else:
                print(f"\n Skin com ID {id_skin} não encontrada.")
        except Exception as e:
            print(f"Erro ao exibir skin: {e}")
        finally:
            cursor.close()
            conn.close()

def gerar_relatorio(cursor):

    cursor.execute("SELECT SUM(valor) FROM Skins")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT tipo, nome, valor
        FROM Skins
        ORDER BY valor DESC
        LIMIT 1
    """)
    mais_cara = cursor.fetchone()

    cursor.execute("""
        SELECT tipo, nome, valor
        FROM Skins
        ORDER BY valor ASC
        LIMIT 1
    """)
    mais_barata = cursor.fetchone()

    cursor.execute("SELECT * FROM Skins")
    quantidade = len(cursor.fetchall())
    print(f"\n-----RELATÓRIO-----")
    print(f"Total de skins cadastradas: {quantidade}")
    print(f"Valor total das skins: R$ {total}")
    print(f"Skin mais cara: {mais_cara[0]} | {mais_cara[1]} (R$ {mais_cara[2]})")
    print(f"Skin mais barata: {mais_barata[0]} | {mais_barata[1]} (R$ {mais_barata[2]})")