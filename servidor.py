import argparse
import mysql.connector
from mysql.connector import errorcode
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Demo HBr - CIIA")

def init_db(user='root', password='pass123', host='127.0.0.3', database='hbr_demo_db'):
    # Tenta a conexão
    try:
        connection = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('ACESSO NEGADO: user ou senha incorreto(a).')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('A base de dados não existe.')
        else:
            print(err)
    else:
        # Caso dê certo, criamos o cursor e realizamos a query
        
        cursor = connection.cursor()

        query = cursor.execute("""
                               CREATE TABLE IF NOT EXISTS tomografo (
                                idExame INT PRIMARY KEY AUTO_INCREMENT,
                                nomePaciente VARCHAR(100),
                                idade INT,
                                resultados VARCHAR(100)
                                )
                               """
                                )
        connection.commit()

        return connection, cursor

@mcp.tool()
def add_data(query: str) -> bool:
    """Adiciona novos dados à tabela do tomógrafo usando uma consulta SQL INSERT.

    Argumentos:
        query (str): query SQL INSERT seguindo o seguinte formato:
            INSERT INTO tomografo (nomePaciente, idade, resultados)
            VALUES ('João Silva', 45, 'Glaucoma')
        
    Esquema:
        - nomePaciente: campo de texto (exigido)
        - idade: campo de inteiro (exigido)
        - resultados: campo de texto (exigido)
        Observação: O campo 'idExame' é gerado automaticamente.
    
    Retorno:
        bool: True se os dados foram inseridos corretamente, False caso contrário
    
    Exemplo:
        >>> query = '''
        ... INSERT INTO tomografo (nomePaciente, idade, resultados)
        ... VALUES ('Alice Guerra', 25, 'Retinopatia diabética')
        ... '''
        >>> add_data(query)
        True
    """

    conn, cursor = init_db()
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Erro ao inserir dados: {e}")
        return False
    finally:
        conn.close()

@mcp.tool()
def read_data(query: str = "SELECT * FROM tomografo") -> list:
    """Lê dados da tabela tomografo usando uma query SQL SELECT.

    Argumentos:
        query (str, optional): SQL SELECT query. O comportamento default é: "SELECT * FROM tomografo;".
            Exemplos:
            - "SELECT * FROM tomografo"
            - "SELECT nomePaciente, idade FROM tomografo WHERE idade > 25"
            - "SELECT * FROM tomografo ORDER BY idade DESC"
    
    Retorna:
        list: Uma lista de tuplas contento os resultados da query.
              Para uma query default, o formato da tupla é (idExame, nomePaciente, idade, resultados)
              
    
    Exemplo:
        >>> # Leia todos os registros
        >>> read_data()
        [(1, 'João Silva', 45, 'Glaucoma'), (2, 'Alice Guerra', 25, 'Retinopatia diabética')]
        
        >>> # Leia com uma query específica
        >>> read_data("SELECT nomePaciente, resultados FROM tomografo WHERE idade < 30")
        [('João Silva', 'Glaucoma')]
    """
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Erro ao inserir dados: {e}")
        return False
    finally:
        conn.close()

@mcp.tool()
def erase_data(query: str) -> bool:
    """Remove registros da tabela tomografo usando uma query SQL SELECT.

    Argumentos:
        query (str, opcional): SQL DELETE query. 
            Exemplos:
            - "DELETE FROM tomografo WHERE nomePaciente=\"Alice Guerra\""
            - "DELETE FROM tomografo WHERE idade > 25"
    
    Retorna:
        bool: True se os dados foram inseridos corretamente, False caso contrário
              
    
    Exemplo:
        >>> # Apague o registro do paciente João Silva, de 45 anos.
        >>> query = '''
        ... DELETE FROM tomografo
        ... WHERE nomePaciente="João Silva" AND idade=45;
        ... '''
        >>> erase_data(query)
        True
    """
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Erro ao remover dados: {e}")
        return False
    finally:
        conn.close()


if __name__=="__main__":
    print("Iniciando servidor...")

    # Modo Debug
    # uv run mcp dev server.py

    # Modo Produção
    # uv run server.py --server_type=sse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )

    args = parser.parse_args()
    mcp.run(args.server_type)