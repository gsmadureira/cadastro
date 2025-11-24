# 🏭 Sistema de Gerenciamento de Estoque em Python

Este projeto é um sistema completo de **controle de estoque**,
desenvolvido em Python com **SQLite**, permitindo cadastrar produtos,
registrar movimentações, consultar itens, emitir alertas de baixo
estoque e gerar gráficos informativos sobre os produtos.

O sistema roda diretamente no terminal e utiliza banco de dados local
(`estoque.db`) para armazenar todas as informações.

Este sistema tem o objetivo de desenvolver habilidades práticas em
programação, banco de dados e lógica de sistemas, aplicando conceitos
aprendidos em aula na construção de uma solução funcional para
gerenciamento de estoque.

## 🚀 Funcionalidades

### 📦 Gerenciamento de Itens

- Cadastrar novos produtos com nome, categoria, valor unitário e
  quantidade.
- Visualizar todo o estoque com identificação de itens em baixa.
- Buscar produtos por **nome** ou **ID**.
- Excluir itens, removendo também todo o histórico relacionado.

### 🔄 Movimentações

- Registrar **entrada** e **saída** de produtos.
- Histórico completo de movimentações com:
  - Tipo (Entrada/Saída/Cadastro)
  - Data e hora
  - Quantidade movimentada
  - Estoque final após a operação

### ⚠️ Alertas Automáticos

O sistema emite alertas sempre que algum produto está com **quantidade ≤
5**.

### 📊 Gráficos e Relatórios

Utiliza **Pandas** e **Matplotlib** para gerar gráficos como: - Valor
total em estoque organizado por categoria (pizza) - Quantidade de cada
produto (barras) - Relação entre quantidade e valor total por produto
(dispersão)

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **SQLite3**
- **Pandas**
- **Matplotlib**
- **Datetime**

## 📁 Estrutura do Banco de Dados

### Tabela: `estoque`

Campo Tipo Descrição

---

id INTEGER Identificador único
nome TEXT Nome do produto
categoria TEXT Categoria do item
valor_unit REAL Preço unitário
quantidade INTEGER Quantidade atual em estoque

### Tabela: `movimentos`

---

Campo Tipo Descrição

---

id INTEGER Identificador do registro

item_id INTEGER ID do produto relacionado

tipo TEXT Entrada, Saída ou Cadastro

datahora TEXT Data e hora da movimentação

quantidade_movimentada INTEGER Quantidade movimentada

quantidade_final INTEGER Estoque final após a movimentação

---

## ▶️ Como Executar o Sistema

### 1. Instale as dependências:

```bash
pip install pandas matplotlib
```

### 2. Execute o arquivo principal:

```bash
python erp.py
```

### 3. O menu principal será exibido:

    1 - Cadastrar Produto
    2 - Visualizar Estoque
    3 - Buscar Item
    4 - Movimentar Estoque
    5 - Excluir item
    6 - Movimentações de um Produto
    7 - Gráficos e Relatórios
    8 - Sair do sistema

## 📌 Observações Importantes

- O sistema gera automaticamente o arquivo **estoque.db**.
- A estrutura do banco é criada na primeira execução.
- Todos os dados são salvos automaticamente após cada ação.
- Os gráficos são exibidos em janelas separadas.

## 🧩 Possíveis Melhorias Futuras

- Interface gráfica com Tkinter ou Flask.
- Exportar relatórios em PDF.
- Implementar autenticação de usuários.
- Adicionar filtros avançados nas consultas.
