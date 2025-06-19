import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Lotofácil App", layout="wide")
st.title("📊 Análise e Geração de Jogos — Lotofácil")

@st.cache_data
def carregar_dados():
    return pd.read_csv("lotofacil_resultados_ate_2025.csv")

df = carregar_dados()

# Mostrar resumo dos concursos
st.subheader("📅 Resultados Carregados")
st.write(f"Total de concursos: {df.shape[0]}")
st.dataframe(df.tail(5))

# 📊 Frequência de dezenas
st.subheader("📈 Frequência das Dezenas")
dezenas_cols = [col for col in df.columns if "Dezena" in col]
todas_dezenas = df[dezenas_cols].values.flatten()
frequencia = pd.Series(todas_dezenas).value_counts().sort_index()

fig = px.bar(frequencia, labels={"index": "Dezena", "value": "Frequência"}, title="Frequência das Dezenas")
st.plotly_chart(fig)

# 🎯 Geração de jogos
st.subheader("🎰 Gerador de Jogos")
qtd_jogos = st.slider("Quantidade de jogos", 1, 20, 5)
gerar = st.button("Gerar Jogos")

if gerar:
    jogos = []
    for _ in range(qtd_jogos):
        jogo = sorted(random.sample(range(1, 26), 15))
        jogos.append(jogo)
    
    st.write("Jogos gerados (em ordem crescente):")
    for i, jogo in enumerate(jogos, 1):
        st.text(f"Jogo {i:02}: {jogo}")
    
    # Exportar para CSV
    df_export = pd.DataFrame(jogos)
    csv = df_export.to_csv(index=False, header=False)
    st.download_button("⬇️ Baixar jogos em CSV", csv, "jogos_gerados.csv", "text/csv")
    