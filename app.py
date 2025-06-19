import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Lotofácil App", layout="wide")
st.title("📊 Análise e Geração de Jogos - Lotofácil")

# Função para carregar dados reais do site da Caixa
@st.cache_data
def carregar_dados():
    url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados"
    payload = {"modalidade": "LOTOFACIL"}
    r = requests.post(url, json=payload)
    if r.status_code != 200:
        st.error("Erro ao buscar os resultados da Caixa.")
        return None
    df = pd.DataFrame(r.json()["listaResultado"])
    df["dataApuracao"] = pd.to_datetime(df["dataApuracao"], dayfirst=True)
    df["numeros"] = df["listaDezenas"].apply(lambda x: list(map(int, x.split(","))))
    return df

dados = carregar_dados()
if dados is not None:
    st.success("Dados carregados com sucesso!")
    st.markdown(f"Último concurso: **{dados.iloc[0]['numero']:,}** — Data: {dados.iloc[0]['dataApuracao'].date()}")

    # Frequência dos números
    todas_dezenas = sum(dados["numeros"].tolist(), [])
    freq = pd.Series(todas_dezenas).value_counts().sort_index()
    freq_df = pd.DataFrame({"Dezena": freq.index, "Frequência": freq.values})

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Frequência das Dezenas")
        fig = px.bar(freq_df, x="Dezena", y="Frequência", text="Frequência")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Gerador de Jogos")
        qtd_jogos = st.slider("Quantidade de jogos:", 1, 20, 5)
        mais_frequentes = freq.sort_values(ascending=False).index.tolist()[:20]
        jogos = [sorted(pd.Series(mais_frequentes).sample(15).tolist()) for _ in range(qtd_jogos)]
        for i, jogo in enumerate(jogos, 1):
            st.write(f"**Jogo {i}:**", ", ".join(f"{n:02d}" for n in sorted(jogo)))

else:
    st.warning("Sem dados disponíveis no momento.")