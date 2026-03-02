import streamlit as st
from datetime import datetime
import sqlite3
import base64
import pytz

st.set_page_config(page_title="Ponto Digital", layout="centered")

st.title("📸 Ponto com Selfie")

# Fuso horário Brasil
fuso = pytz.timezone("America/Sao_Paulo")

# Banco
conn = sqlite3.connect('ponto.db', check_same_thread=False)
c = conn.cursor()

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

menu = st.sidebar.selectbox("Menu", ["Bater Ponto", "Histórico"])

# ===== BATER PONTO =====
if menu == "Bater Ponto":

    nome = st.text_input("Digite seu nome")
    foto = st.camera_input("Tire uma selfie")

    if st.button("📍 Bater Ponto"):

        if nome and foto:

            agora = datetime.now(fuso)
            data = agora.strftime("%d/%m/%Y")
            hora = agora.strftime("%H:%M:%S")

            imagem_bytes = foto.getvalue()
            imagem_base64 = base64.b64encode(imagem_bytes).decode("utf-8")

            c.execute("INSERT INTO registros (nome, data, hora, foto) VALUES (?, ?, ?, ?)",
                      (nome, data, hora, imagem_base64))
            conn.commit()

            st.success(f"Ponto registrado às {hora}")

        else:
            st.error("Preencha o nome e tire a selfie")

# ===== HISTÓRICO =====
if menu == "Histórico":

    st.subheader("📋 Histórico de Pontos")

    dados = c.execute("SELECT nome, data, hora, foto FROM registros ORDER BY id DESC").fetchall()

    for nome, data, hora, foto in dados:

        st.write(f"👤 {nome}")
        st.write(f"📅 {data}")
        st.write(f"🕒 {hora}")

        img = base64.b64decode(foto)
        st.image(img, width=200)

        st.markdown("---")
