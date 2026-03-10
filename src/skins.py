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
            
            print(f"\n✅ Sucesso! A skin '{nome}' foi inserida no stock.")
            
        except Exception as e:
            print(f"\n❌ Erro ao inserir a skin: {e}")
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