
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------------------
# STREAMLIT
# ----------------------------

def streamlit_app():
    """App Streamlit simples com filtros e gráfico de série temporal (Plotly)."""
    import streamlit as st
    import plotly.express as px

    st.set_page_config(page_title="Mini Dashboard (Streamlit)", layout="wide")
    st.title("📊 Mini Dashboard – Streamlit")
    st.write("Carregue um CSV ou use dados de exemplo.")

    uploaded = st.file_uploader("CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        rng = pd.date_range("2024-01-01", periods=180, freq="D")
        df = pd.DataFrame({
            "date": rng,
            "categoria": np.random.choice(["A","B","C"], size=len(rng)),
            "valor": np.random.randn(len(rng)).cumsum() + 100
        })

    st.sidebar.header("Filtros")
    cats = sorted(df["categoria"].unique()) if "categoria" in df.columns else []
    if cats:
        pick = st.sidebar.multiselect("Categorias", cats, default=cats)
        df_f = df[df["categoria"].isin(pick)]
    else:
        df_f = df

    col1, col2, col3 = st.columns(3)
    col1.metric("Linhas", len(df_f))
    if "categoria" in df_f.columns:
        col2.metric("Categorias", df_f["categoria"].nunique())
    else:
        col2.metric("Categorias", "—")
    if "valor" in df_f.columns:
        col3.metric("Valor médio", f"{df_f['valor'].mean():.2f}")
    else:
        col3.metric("Valor médio", "—")

    if {"date", "valor"}.issubset(df_f.columns):
        fig = px.line(
            df_f,
            x="date",
            y="valor",
            color="categoria" if "categoria" in df_f.columns else None,
            title="Série Temporal"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df_f.head(50))

if __name__ == "__main__":
    streamlit_app()