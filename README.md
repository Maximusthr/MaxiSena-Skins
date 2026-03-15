# MaxiSena-Skins 🎮✨

## 🎯 Sobre o trabalho

Este projeto foi desenvolvido para a disciplina de **Banco de Dados** 📚.
A proposta é simular um mini marketplace de **skins de CS2** 🔫🎮, aplicando na prática conceitos como:

- modelagem relacional;
- criação de tabelas e chaves;
- operações de cadastro, consulta, atualização e remoção (CRUD).

Praticando SQL e integração com Python.

---

Projeto em Python para gerenciamento de clientes, skins e compras (PostgreSQL) 🐍🐘, com:

- aplicação principal em terminal (`main.py`) 💻;
- módulo de conexão direta com `psycopg2` 🔌;
- app Flask auxiliar com SQLAlchemy/Migrate em `src/app.py` 🌐. (TO DO)

> **Observação:** a parte em Flask será desenvolvida na **Parte 2** do projeto 🚧. Nesta etapa, o foco principal é a aplicação via terminal com `main.py` ✅.

---

## 👥 Autores

- Arthur — [@Maximusthr](https://github.com/Maximusthr) 🚀
- Yvesena — [@Yvesena](https://github.com/Yvesena) ✨

---

## 1) Pré-requisitos 🧰

Instale na sua máquina:

- Python 3.10+ (recomendado 3.11+)
- PostgreSQL 14+
- Cliente `psql` disponível no terminal

> Dica 💡: no Windows, normalmente o `psql` vem junto com o instalador do PostgreSQL (Stack Builder). Se o comando não for encontrado, adicione o diretório `bin` do PostgreSQL ao `PATH`.

---

## 2) Clonar/abrir o projeto 📂

Abra o projeto na raiz (onde está o `main.py`).

---

## 3) Criar e ativar ambiente virtual (Linux/Windows/macOS) 🧪

### Linux/macOS (bash/zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

---

## 4) Instalar dependências 📦

Com o ambiente virtual ativo:

```bash
pip install -r requirements.txt
```

---

## 5) Configurar variáveis de ambiente ⚙️

Crie o arquivo `.env` a partir de `.env.example`.

### Linux/macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Windows CMD

```cmd
copy .env.example .env
```

Depois, edite o `.env` com seus dados locais do PostgreSQL.

Exemplo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=maxisena
DB_USER=postgres
DB_PASSWORD=sua_senha

DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/maxisena
```

### Por que existem os dois formatos? 🤔

- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: usados em [src/database.py](src/database.py)
- `DATABASE_URL`: usado em [src/app.py](src/app.py)

---

## 6) Criar o banco de dados e tabelas 🗄️

### 6.1 Criar database vazio

```bash
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE maxisena;"
```

### 6.2 Executar script SQL

Na raiz do projeto:

```bash
psql -U postgres -h localhost -p 5432 -d maxisena -f tabelas/Maxisena.sql
```

### 6.3 Conferir tabelas criadas

```bash
psql -U postgres -h localhost -p 5432 -d maxisena -c "\dt"
```

---

## 7) Rodar o projeto ▶️

### Aplicação principal (terminal) 🖥️

```bash
python main.py
```

### App Flask (Parte 2 do projeto) 🌍

```bash
python src/app.py
```

Depois acesse:

- `GET /usuarios`
- `GET /adicionar/<nome>/<email>`

Exemplo local: `http://127.0.0.1:5000/usuarios`

---

## 8) Organização dos arquivos 🧭

- [main.py](main.py): menu principal da aplicação
- [src/database.py](src/database.py): conexão com PostgreSQL (`psycopg2`)
- [src/clientes.py](src/clientes.py): operações de clientes
- [src/skins.py](src/skins.py): operações de skins
- [src/compras.py](src/compras.py): operações de compras
- [tabelas/Maxisena.sql](tabelas/Maxisena.sql): criação das tabelas
- [src/app.py](src/app.py): app Flask com SQLAlchemy + Migrate

---

## 9) Fluxo para “mexer nos arquivos” com segurança 🔒

1. Ative o ambiente virtual.
2. Ajuste o `.env`.
3. Faça alterações em módulos de [src/](src).
4. Rode `python main.py` para validar o fluxo principal.
5. Se alterou estrutura do banco, atualize [tabelas/Maxisena.sql](tabelas/Maxisena.sql) para manter consistência.

---

## 10) Troubleshooting rápido 🛠️

- Erro de conexão com banco ❌:
	- verifique `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` no `.env`;
	- confira se o PostgreSQL está ativo.
- `psql` não reconhecido ⚠️:
	- adicione o diretório `bin` do PostgreSQL ao `PATH`.
- Dependências faltando 📌:
	- execute novamente `pip install -r requirements.txt` com o ambiente virtual ativo.

---

## Licença 📄

Este projeto está sob a licença definida em [LICENSE](LICENSE).