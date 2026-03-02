import streamlit as st
from datetime import datetime
import sqlite3
import base64
import pytz

st.set_page_config(page_title="Ponto Digital", layout="centered")

fuso = pytz.timezone("America/Sao_Paulo")

conn = sqlite3.connect('ponto.db', check_same_thread=False)
c = conn.cursor()

# ===== TABELAS =====
c.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    senha TEXT,
    tipo TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    data TEXT,
    hora TEXT,
    foto TEXT
)
''')
conn.commit()

# ===== GARANTIR ADMIN PADRÃO =====
c.execute("SELECT * FROM usuarios WHERE nome = ?", ("adm",))
if not c.fetchone():
    c.execute(
        "INSERT INTO usuarios (nome, senha, tipo) VALUES (?, ?, ?)",
        ("adm", "1324", "admin")
    )
    conn.commit()

# ===== LOGIN =====
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    st.title("🔐 Login")

    nome = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        user = c.execute(
            "SELECT * FROM usuarios WHERE nome=? AND senha=?",
            (nome, senha)
        ).fetchone()

        if user:
            st.session_state.logado = True
            st.session_state.usuario = user[1]
            st.session_state.tipo = user[3]
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

# ===== SISTEMA LOGADO =====
if st.session_state.logado:

    st.sidebar.write(f"👤 {st.session_state.usuario}")

    # ===== ADMIN =====
    if st.session_state.tipo == "admin":

        menu = st.sidebar.selectbox(
            "Menu",
            ["Bater Ponto", "Criar Funcionário", "Ver Registros"]
        )

        # BATER PONTO
        if menu == "Bater Ponto":

            st.title("📸 Bater Ponto")
            foto = st.camera_input("Tire uma selfie")

            if st.button("Registrar"):

                if foto:
                    agora = datetime.now(fuso)
                    data = agora.strftime("%d/%m/%Y")
                    hora = agora.strftime("%H:%M:%S")

                    imagem_base64 = base64.b64encode(
                        foto.getvalue()
                    ).decode("utf-8")

                    c.execute(
                        "INSERT INTO registros (nome, data, hora, foto) VALUES (?, ?, ?, ?)",
                        (st.session_state.usuario, data, hora, imagem_base64)
                    )
                    conn.commit()

                    st.success(f"Ponto registrado às {hora}")
                else:
                    st.error("Tire a selfie")

        # CRIAR FUNCIONÁRIO
        if menu == "Criar Funcionário":

            st.title("➕ Novo Funcionário")

            novo_nome = st.text_input("Nome do funcionário")
            nova_senha = st.text_input("Senha", type="password")

            if st.button("Criar"):

                try:
                    c.execute(
                        "INSERT INTO usuarios (nome, senha, tipo) VALUES (?, ?, ?)",
                        (novo_nome, nova_senha, "funcionario")
                    )
                    conn.commit()
                    st.success("Funcionário criado com sucesso")
                except:
                    st.error("Usuário já existe")

        # VER TODOS REGISTROS
        if menu == "Ver Registros":

            st.title("📋 Todos os Pontos")

            dados = c.execute(
                "SELECT nome, data, hora, foto FROM registros ORDER BY id DESC"
            ).fetchall()

            for nome, data, hora, foto in dados:

                st.write(f"👤 {nome}")
                st.write(f"📅 {data}")
                st.write(f"🕒 {hora}")

                st.image(base64.b64decode(foto), width=200)
                st.markdown("---")

    # ===== FUNCIONÁRIO =====
    else:

        menu = st.sidebar.selectbox(
            "Menu",
            ["Bater Ponto", "Meu Histórico"]
        )

        if menu == "Bater Ponto":

            st.title("📸 Bater Ponto")
            foto = st.camera_input("Tire uma selfie")

            if st.button("Registrar"):

                if foto:
                    agora = datetime.now(fuso)
                    data = agora.strftime("%d/%m/%Y")
                    hora = agora.strftime("%H:%M:%S")

                    imagem_base64 = base64.b64encode(
                        foto.getvalue()
                    ).decode("utf-8")

                    c.execute(
                        "INSERT INTO registros (nome, data, hora, foto) VALUES (?, ?, ?, ?)",
                        (st.session_state.usuario, data, hora, imagem_base64)
                    )
                    conn.commit()

                    st.success(f"Ponto registrado às {hora}")
                else:
                    st.error("Tire a selfie")

        if menu == "Meu Histórico":

            st.title("📋 Meu Histórico")

            dados = c.execute(
                "SELECT data, hora, foto FROM registros WHERE nome=? ORDER BY id DESC",
                (st.session_state.usuario,)
            ).fetchall()

            for data, hora, foto in dados:

                st.write(f"📅 {data}")
                st.write(f"🕒 {hora}")
                st.image(base64.b64decode(foto), width=200)
                st.markdown("---")
