import sqlite3
from pathlib import Path
import sys

BASE_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
DB_PATH = BASE_DIR / "clipping.db"

def _abrir_conexao():
    return sqlite3.connect(DB_PATH)


def _inicializar_banco():
    with _abrir_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS noticias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                link TEXT UNIQUE,
                resumo TEXT,
                palavra TEXT,
                data DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        _garantir_coluna(cursor, "fonte", "TEXT")
        _garantir_coluna(cursor, "data_publicacao", "TEXT")
        conn.commit()


def _garantir_coluna(cursor, nome_coluna, definicao_coluna):
    cursor.execute("PRAGMA table_info(noticias)")
    colunas = {linha[1] for linha in cursor.fetchall()}
    if nome_coluna not in colunas:
        cursor.execute(
            f"ALTER TABLE noticias ADD COLUMN {nome_coluna} {definicao_coluna}"
        )


_inicializar_banco()


def salvar_noticia(titulo, link, resumo, palavra, fonte=None, data_publicacao=None):
    data_publicacao_str = (
        data_publicacao.isoformat() if getattr(data_publicacao, "isoformat", None) else None
    )
    try:
        with _abrir_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO noticias (titulo, link, resumo, palavra, fonte, data_publicacao)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (titulo, link, resumo, palavra, fonte, data_publicacao_str)
            )
            conn.commit()

    except sqlite3.IntegrityError:
        pass


def listar_noticias():
    with _abrir_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT titulo, link, resumo, palavra, fonte, data_publicacao, data
            FROM noticias
            ORDER BY data DESC
            """
        )
        return cursor.fetchall()
