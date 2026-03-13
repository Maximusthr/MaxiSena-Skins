from src.database import get_conexao

def inserir_skin(nome, valor, estado, raridade, pattern, wear_rating):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO Skins (nome, valor, estado, raridade, pattern, wear_rating) 
                VALUES (%s, %s, %s, %s, %s , %s)
            """
            valores = (nome, valor, estado, raridade, pattern, wear_rating)
            
            cursor.execute(sql, valores)
            conn.commit()
            
            print(f"\nSucesso! A skin '{nome}' foi inserida no stock.")
            
        except Exception as e:
            print(f"\nErro ao inserir a skin: {e}")
            conn.rollback()
             
        finally:
            cursor.close()
            conn.close()

def atualizar_skin(id, nome, valor, estado, raridade, pattern, wear_rating):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                UPDATE Skins SET nome = %s, valor = %s, estado = %s, raridade = %s, pattern = %s, wear_rating = %s  
                WHERE id_skins = %s
            """
            valores = (nome, valor, estado, raridade, pattern, wear_rating, id)

            cursor.execute(sql, valores)

            if cursor.rowcount > 0:
                print(f"\n ID {id} atualizado!")
            else:
                print(f"\n Nenhuma skin encontrada com ID: {id}")

            conn.commit()
        
        except Exception as e:
                print("\nErro ao atualizar os valores.")
                conn.rollback()
        
        finally:
            cursor.close()
            conn.close()

def listar_skins():
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_skins, nome, estado FROM Skins;")
            skins = cursor.fetchall()

            if len(skins) == 0:
                print(f"Nenhuma Skin listada")
            
            else:
                for skin in skins:
                    print(f"ID: {skin[0]} | Nome: {skin[1]} | Estado: {skin[2]}")

        except Exception as e:
            print(f"Erro ao listar skins: {e}")
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
            
            sql = "SELECT id_skins, nome, estado, valor FROM Skins WHERE nome ILIKE %s"
            cursor.execute(sql, (f"%{nome_pesquisa}%",))
            
            skins = cursor.fetchall()
            
            if skins:
                print(f"\nResultados para '{nome_pesquisa}':")
                for s in skins:
                    print(f"ID: {s[0]} | Nome: {s[1]} | Estado: {s[2]} | Valor: R$ {s[3]}")
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
                print(f"Nome: {skin[1]}")
                print(f"Valor: R$ {skin[2]}")
                print(f"Estado: {skin[3]}")
                print(f"Raridade: {skin[4]}")
                print(f"Pattern: {skin[5]}")
                print(f"Wear Rating: {skin[6]}")
            else:
                print(f"\n Skin com ID {id_skin} não encontrada.")
        except Exception as e:
            print(f"Erro ao exibir skin: {e}")
        finally:
            cursor.close()
            conn.close()