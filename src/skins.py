from src.database import get_conexao

def inserir_skin(nome, estado, raridade, pattern, wear_rating):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO Skins (nome, estado, raridade, pattern, wear_rating) 
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nome, estado, raridade, pattern, wear_rating)
            
            cursor.execute(sql, valores)
            conn.commit()
            
            print(f"\nSucesso! A skin '{nome}' foi inserida no stock.")
            
        except Exception as e:
            print(f"\nErro ao inserir a skin: {e}")
            conn.rollback()
            
        finally:
            cursor.close()
            conn.close()

def atualizar_skin(nome, estado, raridade, pattern, wear_rating):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                UPDATE INTO Skins(nome, estado, raridade, pattern, wear_rating)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nome, estado, raridade, pattern, wear_rating)

            cursor.execute(sql, valores)
            conn.commit()

            print(f"\n Valores atualizados!")
        
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