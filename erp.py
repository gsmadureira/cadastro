#Tentando importar Banco de Dados e biblioteca para registrar datas
import sqlite3
from datetime import datetime
#Importando bibliotecas para fazer gráficos
import pandas as pd
import matplotlib.pyplot as plt

def iniciar(conn, cursor):
    #Aqui vou inciar/verificar as tabelas que usarei no sistema
    cursor.execute("""CREATE TABLE IF NOT EXISTS estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    valor_unit REAL NOT NULL,
    quantidade INTEGER NOT NULL
)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS movimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    datahora TEXT NOT NULL,
    quantidade_movimentada INTEGER NOT NULL,
    quantidade_final INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES estoque(id) ON DELETE CASCADE
)""")
    return conn, cursor

def cadastrar_item(conn, cursor, nome, categoria, valor_unit, quantidade):
    insert_estoque = ("""INSERT INTO estoque (nome, categoria, valor_unit, quantidade) VALUES (?, ?, ?, ?)""")
    cursor.execute(insert_estoque, (nome, categoria, valor_unit, quantidade))
    cursor.execute("SELECT id FROM estoque WHERE nome = ?", (nome, ))
    id_compact = cursor.fetchone()
    id = id_compact[0]
    insert_movimentos = ("INSERT INTO movimentos (item_id, tipo, datahora, quantidade_movimentada, quantidade_final) VALUES(?, ?, ?, ?, ?)")
    tipo = "Cadastro"
    data_n = datetime.now()
    datahora = data_n.strftime("%d/%m/%Y, %H:%M:%S")
    cursor.execute(insert_movimentos, (id, tipo, datahora, quantidade, quantidade))
    print(f"Produto {nome} adicionado com sucesso!")
    conn.commit()
    return

def verificar_estoque(conn, cursor): #def para verificar se há linhas no estoque
    cursor.execute("SELECT COUNT(*) FROM estoque")
    linhas_compact = cursor.fetchone()
    verificador = linhas_compact[0]
    if verificador == 0:
        return verificador
    return 1

def alerta_estoque(conn, cursor): #def para criar um alerta para o usuário caso o estoque esteja baixo
    verify_estoque = verificar_estoque(conn, cursor)
    if verify_estoque != 0:
        quantidade_alerta = 5
        cursor.execute("SELECT * FROM estoque WHERE quantidade <= ?", (quantidade_alerta, ))
        produtos_estoque_baixo = cursor.fetchall()
        for produto in produtos_estoque_baixo:
            print(f"ALERTA - Produto ID {produto['id']} - Nome: {produto['nome']} - ESTOQUE BAIXO {produto['quantidade']}")
            print("="*100)
        conn.commit()
        return

def visualizar_estoque(conn, cursor): #def para visualizar itens cadastrados no estoque
    verify_estoque = verificar_estoque(conn, cursor)
    if verify_estoque != 0:
        cursor.execute("""SELECT * FROM estoque WHERE quantidade > 5""")
        for produto in cursor:
            print(f"ID {produto['id']} - Nome: {produto['nome']} - Categoria: {produto['categoria']} - Valor: {produto['valor_unit']} - Quantidade: {produto['quantidade']}")
            print("="*100)
        cursor.execute("""SELECT COUNT(*) FROM estoque WHERE quantidade <= 5""")
        linhas_compact = cursor.fetchone()
        resultado = linhas_compact[0]
        if resultado != 0:
            cursor.execute("""SELECT * FROM estoque WHERE quantidade <= 5""")
            for produto in cursor:
                print(f"**ESTOQUE BAIXO**: ID {produto['id']} - Nome: {produto['nome']} - Categoria: {produto['categoria']} - Valor: {produto['valor_unit']} - Quantidade: {produto['quantidade']}")
                print("="*100)
            print("\n")
        return
    else:
        print("O estoque está vazio!")
        return

#def para buscar itens especificos pelo nome ou pelo id
def buscar_item(conn, cursor, buscar):
    cursor.execute("""SELECT * FROM estoque WHERE nome = ? OR id = ?""", (buscar, buscar))
    item_encontrado = cursor.fetchone()
    if item_encontrado is None:
        print("Nenhum produto encontrado!")
        conn.commit()
        return None
    else:
        print("Produto encontrado!")
        print(f"ID {item_encontrado['id']} - Nome: {item_encontrado['nome']} - Categoria: {item_encontrado['categoria']} - Valor: {item_encontrado['valor_unit']} - Quantidade: {item_encontrado['quantidade']} ")
        print("="*100)
        conn.commit()
        return item_encontrado

def movimentar_item(conn, cursor, buscar, opcao):#def para movimentar itens pelo estoque
    item_encontrado = buscar_item(conn, cursor, buscar)
    if item_encontrado is None:
        print("Nenhum item encontrado!")
        return
    else:
        nome = item_encontrado['nome']
        id = item_encontrado['id']
        quantidade_inicial = int(item_encontrado['quantidade'])
        quantidade_movimentada = 0
        tipo_movimento = ""
        data_now = datetime.now()
        datahora = data_now.strftime("%d/%m/%Y, %H:%M:%S")
        if opcao == 1:
            while True:
                try:
                    quantidade_movimentada = int(input(f"Digite quantas unidades serão adicionadas à '{nome}': "))
                    break
                except TypeError:
                    print("Entrada inválida! Tente novamente.")
                    continue
            cursor.execute("""UPDATE estoque SET quantidade = quantidade + ? WHERE nome = ?""", (quantidade_movimentada, nome))
            conn.commit()
            tipo_movimento = "Entrada"
        elif opcao == 2:
            while True:
                try:
                    quantidade_movimentada = int(input(f"Digite quantas unidades serão retiradas de '{nome}': "))
                    break
                except TypeError:
                    print("Entrada inválida! Tente novamente.")
                    continue
                
            if quantidade_movimentada > quantidade_inicial:
                print("Não é possível realizar essa operação!")
                print(f"Quantidade no estoque: {quantidade_inicial}\nRetirada Requisitada: {quantidade_movimentada}")
                return
            else:
                cursor.execute("""UPDATE estoque SET quantidade = quantidade - ? WHERE nome = ?""", (quantidade_movimentada, nome))
                tipo_movimento = "Saída"
                conn.commit()
        cursor.execute("SELECT quantidade FROM estoque WHERE nome = ?", (nome, ))
        quantidade_atualizada_list = cursor.fetchone()
        quantidade_atualizada = quantidade_atualizada_list[0]
        insert = ("""INSERT INTO movimentos (item_id, tipo, datahora, quantidade_movimentada, quantidade_final) 
        VALUES (?, ?, ?, ?, ?)""")
        cursor.execute(insert, (id, tipo_movimento, datahora, quantidade_movimentada, quantidade_atualizada))
        conn.commit()
        print(f"Movimentação de {quantidade_movimentada} unidades realizada com sucesso. Novo estoque: {quantidade_atualizada}")
        return

def excluir_item(conn, cursor, buscar):
    item_encontrado = buscar_item(conn, cursor, buscar)
    nome = item_encontrado['nome']
    print(f"Atenção!!! caso o item {nome} for excluido todos os registros envolvendo o item serão perdidos!")
    while True:
        try:
            editor = int(input("Continuar exclusão:\n1 - SIM\n2 - NÃO\n"))
            break
        except ValueError:
            print("Você deve digitar uma das opções!")
            continue
        except editor != 1 and editor != 2:
            print("Opção inválida! Tente novamente.")
            continue
    if editor == 1:
        cursor.execute("DELETE FROM estoque WHERE nome = ?", (nome, ))
        print(f"Produto '{nome}' excluido com sucesso!")
        conn.commit()
        return
    elif editor == 2:
        print(f"Exclusão de {nome} cancelada")
        return
    
def buscar_registros(conn, cursor, buscar):
    item_encontrado = buscar_item(conn, cursor, buscar)
    if item_encontrado is None:
        return
    else:
        cursor.execute("SELECT id FROM estoque WHERE nome = ?", (item_encontrado['nome'], ))
        id_mov = cursor.fetchone()
        id_mov_d = id_mov[0]
        cursor.execute("SELECT * FROM movimentos WHERE item_id = ?", (id_mov_d, ))
        print("\n")
        print("=== Movimentações ===")
        print("\n")
        for transacao in cursor:
            print(f"Tipo: {transacao['tipo']} - Data: {transacao['datahora']} - Quantidade Movimentada: {transacao['quantidade_movimentada']} - Quantidade Final: {transacao['quantidade_final']}")
            print("="*100)
        conn.commit()
        return

def graficos(conn):
    #Para fazer os gráficos que vou usar, irei usar a biblioteca pandas para acessar os dados no estoque e transformar em dataframes e após isso usar matplotlib para fazer os gráficos
    while True:
        while True:
            try:
                option_graficos = int(input("Qual gráfico deseja visualizar:\n1 - Visualizar valor em estoque por categoria\n2 - Visualizar produtos e quantidades no estoque\n3 - Visualizar distribuição de valores unitários dos produtos em estoque\n"))
                break
            except ValueError:
                print("Digite uma opção válida!")
                continue
        if option_graficos == 1:
            print("\nGerando gráfico de valor por categoria...")
            query = "SELECT categoria, SUM(valor_unit * quantidade) as valor_total FROM estoque GROUP BY categoria"
            dataframe = pd.read_sql_query(query, conn)
            valor_geral_total = dataframe['valor_total'].sum()
            texto_total = f"Total:\nR$ {valor_geral_total:,.2f}"
            dataframe.plot.pie(y='valor_total', labels=dataframe['categoria'])
            plt.title("Gráfico de Valor por Categoria")
            plt.text(0, 0, texto_total, ha='center', va='center')
            plt.ylabel('')
            plt.show()
            print("\n")
            break
        elif option_graficos == 2:
            print("\nGerando gráfico de produtos e quantidades no estoque...")
            query = "SELECT nome, quantidade FROM estoque GROUP BY nome"
            dataframe = pd.read_sql_query(query, conn)
            dataframe.plot.bar(x='nome', y='quantidade', figsize=(10, 6), legend=False)
            plt.title("Gráfico de Produtos e Quantidades")
            plt.xlabel("Produto", fontsize=12)
            plt.ylabel("Quantidade em Estoque", fontsize=12)
            plt.xticks(rotation=0, ha='right')
            plt.tight_layout()
            plt.show()
            print("\n")
            break
        elif option_graficos == 3:
            print("\nGerando gráfico de dispersão para correlação entre quantidade e valor total por produto...")
            query = "SELECT nome, SUM(quantidade) as total_quantidade, SUM(valor_unit * quantidade) as valor_total FROM estoque GROUP BY nome"
            dataframe = pd.read_sql_query(query, conn)
            dataframe.plot.scatter(x='total_quantidade', y='valor_total', figsize=(10, 6), s=100, alpha=0.7)
            plt.title("Correlação entre Quantidade e Valor Total por Produto", fontsize=16)
            plt.xlabel("Quantidade Total em Estoque", fontsize=12)
            plt.ylabel("Valor Total Acumulado (R$)", fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.show()
            print("\n")
            break
        else:
            print("Opção inválida. Escolha uma das opções válidas (1 a 3).")
            continue

#Menu Principal do Sistema
print("--          Gerenciamento de Estoques          --")
print("="*50)
#Conexão com o banco de dados e cursor para executar os comandos SQL
conn = sqlite3.connect('estoque.db')
#Comando para formatar as saídas do banco de dados para um dicionário facilitando o manejo dos dados
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

iniciar(conn, cursor)
while True:
    alerta_estoque(conn, cursor)
    while True:
        try:
            verify = int(input("Digite qual operação você deseja fazer:\n1 - Cadastrar Produto\n2 - Visualizar Estoque\n3 - Buscar Item\n4 - Movimentar Estoque\n5 - Excluir item\n6 - Movimentações de um Produto\n7 - Gráficos e Relatórios\n8 - Sair do sistema\n"))
            break
        except ValueError:
            print("Digite uma opção válida!")
            continue
    if verify == 1:
        nome = input("Digite o nome do produto: ")
        while True:
            while True:
                try:
                    escolher_categoria = int(input("Digite a categoria do produto:\n1 - Alimentos/Bebidas\n2 - Higiene/Limpeza\n3 - Vestuário/Têxteis\n4 - Material de Escritório/Escolar\n5 - Ferramentas/Construção\n"))
                    break
                except ValueError:
                    print("Digite uma opção válida!")
                    continue
            if escolher_categoria == 1:
                categoria = "Alimentos/Bebidas"
                break
            elif escolher_categoria == 2:
                categoria = "Higiene/Limpeza"
                break
            elif escolher_categoria == 3:
                categoria = "Vestuário/Têxteis"
                break
            elif escolher_categoria == 4:
                categoria = "Material de Escritório/Escolar"
                break
            elif escolher_categoria == 5:
                categoria = "Ferramentos/Construção"
                break
            else:
                print("Opção inválida. Escolha uma das opções válidas (1 a 5).")
                continue
        while True:
            try:
                valor_unit = float(input("Digite o valor unitário dos produtos: "))
                quantidade = int(input("Digite a quantidade: "))
                break
            except ValueError:
                print("Entrada inválida! Tente novamente.")
                continue
            except Exception as e:
                print(f"Ocorreu um erro inesperado {e}")
                print("Tente Novamente.")
                continue
        cadastrar_item(conn, cursor, nome, categoria, valor_unit, quantidade)
        print("\n")
    
    elif verify == 2:
        visualizar_estoque(conn, cursor)

    elif verify == 3:
        verify_estoque = verificar_estoque(conn, cursor)
        if verify_estoque != 0:
            option = int(input("Deseja buscar o produto por\n1 - Nome\n2 - ID\n"))
            if option == 1:
                buscar = input("Digite o nome do produto que deseja buscar: ")
                buscar_item(conn, cursor, buscar)
                print("\n")
            elif option == 2:
                buscar = int(input("Digite o ID do produto que deseja buscar: "))
                buscar_item(conn, cursor, buscar)
                print("\n")
            else:
                print("Opção inválida!")
        else:
            print("O banco de dados está vazio, adicione algum item para fazer operações.\n")

    elif verify == 4:
        verify_estoque = verificar_estoque(conn, cursor)
        if verify_estoque != 0:        
            option = int(input("Deseja buscar o produto por\n1 - Nome\n2 - ID\n"))
            if option == 1:
                buscar = input("Digite o nome do produto que deseja buscar: ")
                opcao = int(input("Digite qual operação deseja fazer:\n1 - Entrada\n2 - Saída\n"))
                movimentar_item(conn, cursor, buscar, opcao)
                print("\n")
            elif option == 2:
                buscar= int(input("Digite o ID do produto que deseja buscar: "))
                opcao = int(input("Digite qual operação deseja fazer:\n1 - Entrada\n2 - Saída\n"))
                movimentar_item(conn, cursor, buscar, opcao)
                print("\n")
        else:
            print("O banco de dados está vazio, adicione algum item para fazer operações.\n")

    elif verify == 5:
        verify_estoque = verificar_estoque(conn, cursor)
        if verify_estoque != 0:        
            option = int(input("Deseja buscar o produto por\n1 - Nome\n2 - ID\n"))
            if option == 1:
                buscar = input("Digite o nome do produto que deseja buscar: ")
                excluir_item(conn, cursor, buscar)
                print("\n")
            elif option == 2:
                buscar= int(input("Digite o ID do produto que deseja buscar: "))
                excluir_item(conn, cursor, buscar)
                print("\n")
        else:
            print("O banco de dados está vazio, adicione algum item para fazer operações.\n")

    elif verify == 6:
        verify_estoque = verificar_estoque(conn, cursor)
        if verify_estoque != 0:        
            option = int(input("Deseja buscar o produto por\n1 - Nome\n2 - ID\n"))
            if option == 1:
                buscar = input("Digite o nome do produto que deseja buscar: ")
                buscar_registros(conn, cursor, buscar)
                print("\n")
            elif option == 2:
                buscar= int(input("Digite o ID do produto que deseja buscar: "))
                buscar_registros(conn, cursor, buscar)
                print("\n")
        else:
            print("O banco de dados está vazio, adicione algum item para fazer operações.\n")

    elif verify == 7:
        verify_estoque = verificar_estoque(conn, cursor)
        if verify_estoque != 0:        
            graficos(conn)
        else:
            print("O banco de dados está vazio, adicione algum item para fazer operações.\n")

    elif verify == 8:
        print("Encerrando Operação...\nObrigado por usar nossos serviços.")
        conn.close()
        break

    else:
        print("Opção inválida. Escolha uma das opções válidas (1 a 8).")
        continue