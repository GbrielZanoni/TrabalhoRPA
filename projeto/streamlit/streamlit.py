import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Energral | Gestão Operacional", layout="wide")
st.title("🔧 Painel Gerencial - Energral")

@st.cache_data
def carregar_dados():
    base = os.path.join(os.path.dirname(__file__), "csv")
    dados = {
        "inspeções": pd.read_csv(os.path.join(base, "checklist_inspecoes.csv")),
        "equipamentos": pd.read_csv(os.path.join(base, "equipamentos_subestacoes.csv")),
        "tecnicos": pd.read_csv(os.path.join(base, "tecnicos_equipes.csv")),
        "alertas": pd.read_csv(os.path.join(base, "alertas_notificacoes.csv")),
    }
    for nome in dados:
        dados[nome].columns = (
            dados[nome]
            .columns.str.lower()
            .str.strip()
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
            .str.replace(" ", "_")
        )
    if "data_hora" in dados["alertas"].columns:
        dados["alertas"]["data_hora"] = pd.to_datetime(dados["alertas"]["data_hora"], errors="coerce")
    return dados

dados = carregar_dados()

aba = st.sidebar.radio("Visão", ["Geral", "Técnicos", "Equipamentos", "Inspeções", "Alertas", "Checklists PDF"])

if aba == "Geral":
    st.subheader("📌 Visão Geral")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Inspeções", len(dados["inspeções"]))
    col2.metric("Equipamentos", len(dados["equipamentos"]))
    col3.metric("Técnicos", len(dados["tecnicos"]))
    col4.metric("Alertas", len(dados["alertas"]))

elif aba == "Técnicos":
    st.subheader("👷 Equipes Técnicas")
    st.dataframe(dados["tecnicos"])
    if "nivel_de_experiencia" in dados["tecnicos"].columns:
        fig = px.histogram(dados["tecnicos"], x="nivel_de_experiencia", title="Distribuição por Nível de Experiência")
        st.plotly_chart(fig, use_container_width=True)

elif aba == "Equipamentos":
    st.subheader("🔌 Equipamentos")
    st.dataframe(dados["equipamentos"])
    if "tipo" in dados["equipamentos"].columns:
        tipo_counts = dados["equipamentos"]["tipo"].value_counts().reset_index()
        tipo_counts.columns = ["tipo", "quantidade"]
        fig = px.pie(tipo_counts, names="tipo", values="quantidade", title="Tipos de Equipamento")
        st.plotly_chart(fig, use_container_width=True)

elif aba == "Inspeções":
    st.subheader("📄 Inspeções Realizadas")
    st.dataframe(dados["inspeções"])
    if "criterio_de_aprovacao" in dados["inspeções"].columns:
        criterio = dados["inspeções"]["criterio_de_aprovacao"].value_counts().reset_index()
        criterio.columns = ["criterio", "quantidade"]
        fig = px.bar(criterio, x="criterio", y="quantidade", title="Critérios de Aprovação")
        st.plotly_chart(fig, use_container_width=True)

elif aba == "Alertas":
    st.subheader("🚨 Alertas e Notificações")
    st.dataframe(dados["alertas"])
    if "status" in dados["alertas"].columns:
        status_count = dados["alertas"]["status"].value_counts().reset_index()
        status_count.columns = ["status", "quantidade"]
        fig = px.bar(status_count, x="status", y="quantidade", title="Alertas por Status")
        st.plotly_chart(fig, use_container_width=True)
    if "data_hora" in dados["alertas"].columns:
        dados["alertas"] = dados["alertas"].sort_values("data_hora")
        fig2 = px.histogram(dados["alertas"], x="data_hora", nbins=20, title="Distribuição Temporal dos Alertas")
        st.plotly_chart(fig2, use_container_width=True)
elif aba == "Checklists PDF":
    st.subheader("📂 Checklists em PDF")

    import PyPDF2

    pasta = os.path.join(os.path.dirname(__file__), "..", "checklist", "dist")
    arquivos = [f for f in os.listdir(pasta) if f.endswith(".pdf")]

    registros = []

    for nome in arquivos:
        caminho = os.path.join(pasta, nome)
        with open(caminho, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            texto = ""
            for pagina in reader.pages:
                texto += pagina.extract_text() + "\n"

        def pega(campo):
            try:
                return texto.split(f"{campo}:")[1].split("\n")[0].strip()
            except:
                return "-"

        registros.append({
            "Arquivo": nome,
            "Data": pega("Data e Hora"),
            "Local": pega("Local da Subestação"),
            "Técnico": pega("Nome do Técnico"),
            "Tipo de Inspeção": pega("Tipo de Inspeção"),
            "Gravidade": pega("Gravidade"),
            "Ação Tomada": pega("Ação Tomada")
        })

    df = pd.DataFrame(registros)

    st.dataframe(df)

    if not df.empty:
        tipo = df["Tipo de Inspeção"].value_counts().reset_index()
        tipo.columns = ["Tipo", "Quantidade"]
        st.plotly_chart(px.pie(tipo, names="Tipo", values="Quantidade", title="Distribuição por Tipo de Inspeção"), use_container_width=True)

        grav = df["Gravidade"].value_counts().reset_index()
        grav.columns = ["Gravidade", "Quantidade"]
        st.plotly_chart(px.bar(grav, x="Gravidade", y="Quantidade", title="Distribuição por Gravidade"), use_container_width=True)

        tecnico = df["Técnico"].value_counts().reset_index()
        tecnico.columns = ["Técnico", "Total"]
        st.plotly_chart(px.bar(tecnico, x="Técnico", y="Total", title="Atuação por Técnico"), use_container_width=True)

        acao = df["Ação Tomada"].value_counts().reset_index()
        acao.columns = ["Ação", "Qtd"]
        st.plotly_chart(px.pie(acao, names="Ação", values="Qtd", title="Ações Tomadas"), use_container_width=True)
