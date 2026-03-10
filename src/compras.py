from src.database import get_conexao

def registrar_compra(id_cliente, id_skins, valor):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Compras (id_cliente, id_skins, valor) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id_cliente, id_skins, valor))
            conn.commit()
            print("Compra registrada com sucesso!")
        except Exception as e:
            print(f"Erro ao registrar compra: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()