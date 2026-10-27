import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sistema_bancario (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        saldo REAL NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        cpf TEXT NOT NULL,
        operacao TEXT NOT NULL,
        valor REAL NOT NULL,
        data_hora TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
""")

conexao.commit()


def consultar_saldo(cpf):
    cursor.execute(
        "SELECT nome, saldo FROM sistema_bancario WHERE cpf = ?",
        (cpf,),
    )
    return cursor.fetchone()


def consultar_historico(cpf):
    cursor.execute("""
        SELECT operacao, valor, data_hora
        FROM historico
        WHERE cpf = ?
        ORDER BY id
    """, (cpf,))
    return cursor.fetchall()


def criar_conta(cpf, nome, idade, saldo):
    if saldo < 0:
        raise ValueError("O saldo inicial não pode ser negativo.")

    try:
        cursor.execute("""
            INSERT INTO sistema_bancario (cpf, nome, idade, saldo)
            VALUES (?, ?, ?, ?)
        """, (cpf, nome, idade, saldo))

        if saldo > 0:
            cursor.execute("""
                INSERT INTO historico (cpf, operacao, valor)
                VALUES (?, ?, ?)
            """, (cpf, "Saldo inicial", saldo))

        conexao.commit()
    except Exception:
        conexao.rollback()
        raise


def buscar_conta(cpf):
    cursor.execute(
        "SELECT nome, idade, cpf, saldo FROM sistema_bancario WHERE cpf = ?",
        (cpf,),
    )
    return cursor.fetchone()


def depositar(cpf, valor):
    if valor <= 0:
        return 0

    try:
        cursor.execute("""
            UPDATE sistema_bancario
            SET saldo = saldo + ?
            WHERE cpf = ?
        """, (valor, cpf))

        linhas_atualizadas = cursor.rowcount
        if linhas_atualizadas == 0:
            conexao.rollback()
            return 0

        cursor.execute("""
            INSERT INTO historico (cpf, operacao, valor)
            VALUES (?, ?, ?)
        """, (cpf, "Depósito", valor))

        conexao.commit()
        return linhas_atualizadas
    except Exception:
        conexao.rollback()
        raise


def sacar(cpf, valor):
    if valor <= 0:
        return 0

    try:
        cursor.execute("""
            UPDATE sistema_bancario
            SET saldo = saldo - ?
            WHERE cpf = ? AND saldo >= ?
        """, (valor, cpf, valor))

        linhas_atualizadas = cursor.rowcount
        if linhas_atualizadas == 0:
            conexao.rollback()
            return 0

        cursor.execute("""
            INSERT INTO historico (cpf, operacao, valor)
            VALUES (?, ?, ?)
        """, (cpf, "Saque", valor))

        conexao.commit()
        return linhas_atualizadas
    except Exception:
        conexao.rollback()
        raise
