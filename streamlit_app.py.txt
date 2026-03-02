import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Ponto Digital", layout="centered")

st.title("📱 Sistema de Ponto")

nome = st.text_input("Digite seu nome")

if st.button("Bater Ponto"):
    hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.success(f"Ponto registrado para {nome} às {hora}")