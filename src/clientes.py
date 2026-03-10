from src.database import get_conexao

def cadastrar_cliente(nome, cpf, email, cidade, telefone):
    conn = get_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Clientes (nome, cpf, email, cidade, telefone) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, cpf, email, cidade, telefone))
            conn.commit()
            print(f"Cliente {nome} cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao cadastrar cliente: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()