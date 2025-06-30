import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime, date
from fpdf import FPDF
from io import BytesIO

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

def gerar_pdf(titulo, df, extras):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, titulo, 0, 1, "C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1)
    pdf.ln(2)
    for linha in extras:
        pdf.cell(0, 6, linha, 0, 1)
    pdf.ln(4)
    for i, row in df.iterrows():
        texto = " | ".join(f"{col}: {row[col]}" for col in df.columns[:4])
        pdf.multi_cell(0, 6, texto, 0, 1)

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    buffer = BytesIO(pdf_bytes)
    return buffer

dados = carregar_dados()

from datetime import date

with st.sidebar:
    st.markdown("## ⚡ Energral")
    st.markdown("### 📊 Painel de Gestão Operacional")
    st.markdown("---")

    aba = st.radio(
        "📁 Navegação",
        ["Geral", "Técnicos", "Equipamentos", "Inspeções", "Alertas", "Checklists PDF"]
    )

    st.markdown("---")
    st.markdown("📅 Hoje é: **{}**".format(date.today().strftime("%d/%m/%Y")))
    st.caption("Desenvolvido pela equipe de RPA")

if aba == "Geral":
    st.subheader("📌 Visão Geral")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Inspeções", len(dados["inspeções"]))
    col2.metric("Equipamentos", len(dados["equipamentos"]))
    col3.metric("Técnicos", len(dados["tecnicos"]))
    col4.metric("Alertas", len(dados["alertas"]))
    st.markdown("---")

    st.markdown("""
    ## 🏢 Sobre o Projeto

    O **Painel Gerencial - Energral** é uma aplicação interativa desenvolvida para apoiar a tomada de decisão e a gestão operacional de uma empresa fictícia do setor de energia elétrica.

    A **Energral** é uma companhia especializada na manutenção e operação de subestações, linhas de transmissão e sistemas de distribuição de energia. O projeto simula o monitoramento de suas operações técnicas e administrativas, com base em dados reais ou simulados, incluindo inspeções, equipes técnicas, equipamentos instalados e alertas operacionais.

    Este painel foi desenvolvido como parte de uma atividade prática de RPA, com foco na coleta, análise e visualização de dados para fins operacionais e estratégicos.

    ---
    ### 🔍 Funcionalidades do Painel

    - **Visão Geral** com totais de inspeções, equipamentos, técnicos e alertas.
    - **Análise de Técnicos** com distribuição por experiência e áreas de atuação.
    - **Inventário de Equipamentos** com classificação por tipo.
    - **Histórico de Inspeções** com critérios de aprovação e análise de PDF de checklists.
    - **Alertas Operacionais** com evolução temporal e status.
    - **Leitura Automática de Checklists PDF**, com gráficos e heatmaps de correlação.

    ---
    ### 📊 Sobre os Dados Apresentados

    - Os arquivos `.csv` utilizados simulam bases reais de operação da Energral.
    - Os arquivos `.pdf` representam relatórios de inspeção técnica preenchidos por engenheiros e eletricistas em campo.
    - As colunas foram padronizadas para facilitar a análise e visualização.

    ---
    ### 👨‍💻 Equipe de Desenvolvimento

    - Ana Julia – [@4nanotfound](https://github.com/4nanotfound)  
    - Gabriel Zanoni – [@GbrielZanoni](https://github.com/GbrielZanoni)  
    - Mateus Euzébio – [@mateuseuz](https://github.com/mateuseuz)  
    - Gabriel Moura – [@gmoura0](https://github.com/gmoura0)  
    - João Gabriel – [@JoaoGabFB](https://github.com/JoaoGabFB)  
    - Maria Delmonaco – [@mariadelmonaco](https://github.com/mariadelmonaco)  

    """)

elif aba == "Técnicos":
    st.subheader("👷 Equipes Técnicas")
    df_tec = dados["tecnicos"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Funcionários", len(df_tec))

    niveis = df_tec["nivel_de_experiencia"].value_counts()
    col2.metric("Júnior", niveis.get("Júnior", 0))
    col3.metric("Pleno", niveis.get("Pleno", 0))
    col4.metric("Sênior", niveis.get("Sênior", 0))

    if "area_de_atuacao" in df_tec.columns:
        areas = df_tec["area_de_atuacao"].value_counts()
        colunas_areas = st.columns(len(areas))
        for col, (area, qtd) in zip(colunas_areas, areas.items()):
            col.metric(area, f"{qtd}")

        import plotly.express as px
        import pandas as pd

        radar_df = pd.DataFrame({
            "Área": areas.index,
            "Quantidade": areas.values
        })

        fig_radar = px.line_polar(
            radar_df,
            r="Quantidade",
            theta="Área",
            line_close=True,
            title="",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.subheader("📋 Dados Detalhados")
    st.dataframe(df_tec)
    if st.button("Gerar Relatório de Técnicos"):
        extras = [
            f"Total de funcionários: {len(df_tec)}",
            f"Distribuição de níveis: {niveis.to_dict()}",
            f"Áreas de atuação: {areas.to_dict() if 'areas' in locals() else 'N/A'}",
        ]
        buffer = gerar_pdf("Relatório de Técnicos", df_tec, extras)
        st.download_button("Baixar PDF", buffer, file_name="relatorio_tecnicos.pdf", mime="application/pdf")

elif aba == "Equipamentos":
    st.subheader("🔌 Equipamentos")
    df_eq = dados["equipamentos"]
    st.dataframe(df_eq)

    if "tipo" in df_eq.columns:
        tipo_counts = df_eq["tipo"].value_counts().reset_index()
        tipo_counts.columns = ["tipo", "quantidade"]
        fig = px.pie(tipo_counts, names="tipo", values="quantidade", title="Tipos de Equipamento")
        st.plotly_chart(fig, use_container_width=True)

    if {"localizacao", "tipo"}.issubset(df_eq.columns):
        st.subheader("🏭 Concentração por Localização e Tipo de Equipamento")
        agrupado = df_eq.groupby(["localizacao", "tipo"]).size().reset_index(name="quantidade")
        fig_bar = px.bar(
            agrupado,
            x="localizacao",
            y="quantidade",
            color="tipo",
            title="Distribuição de Equipamentos por Localização",
            barmode="group"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    if st.button("Gerar Relatório de Equipamentos"):
        extras = [
            f"Total de equipamentos: {len(df_eq)}",
            f"Tipos: {df_eq['tipo'].value_counts().to_dict()}",
            f"Pontos de instalação: {df_eq['localizacao'].nunique()} locais",
        ]
        buffer = gerar_pdf("Relatório de Equipamentos", df_eq, extras)
        st.download_button("Baixar PDF", buffer, file_name="relatorio_equipamentos.pdf", mime="application/pdf")

elif aba == "Inspeções":
    st.subheader("📄 Inspeções Realizadas")
    df_insp = dados["inspeções"]
    st.dataframe(df_insp)

    if "criterio_de_aprovacao" in df_insp.columns:
        criterio = df_insp["criterio_de_aprovacao"].value_counts().reset_index()
        criterio.columns = ["Critério", "Quantidade"]
        fig = px.bar(criterio, x="Critério", y="Quantidade", title="Distribuição por Critério de Aprovação")
        st.plotly_chart(fig, use_container_width=True)

    if {"item", "criterio_de_aprovacao"}.issubset(df_insp.columns):
        st.subheader("")
        heat_df = (
            df_insp.groupby(["item", "criterio_de_aprovacao"])
            .size()
            .reset_index(name="quantidade")
        )

        fig_heat = px.density_heatmap(
            heat_df,
            x="criterio_de_aprovacao",
            y="item",
            z="quantidade",
            color_continuous_scale="Reds",
            title="Frequência de Critérios por Item Inspecionado"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    if st.button("Gerar Relatório de Inspeções"):
        extras = [
            f"Total de inspeções: {len(df_insp)}",
            f"Critérios de aprovação: {criterio.set_index('Critério')['Quantidade'].to_dict() if 'criterio' in locals() else 'N/A'}",
        ]
        buffer = gerar_pdf("Relatório de Inspeções", df_insp, extras)
        st.download_button("Baixar PDF", buffer, file_name="relatorio_inspecoes.pdf", mime="application/pdf")

elif aba == "Alertas":
    st.subheader("🚨 Alertas e Notificações")

    df_alertas = dados["alertas"].copy()

    if "data/hora" in df_alertas.columns:
        df_alertas["data/hora"] = pd.to_datetime(df_alertas["data/hora"], errors="coerce")
        df_alertas = df_alertas.dropna(subset=["data/hora"])
        df_alertas["data"] = df_alertas["data/hora"].dt.date

    st.dataframe(df_alertas)

    if "status" in df_alertas.columns and not df_alertas.empty:
        status_count = df_alertas["status"].value_counts().reset_index()
        status_count.columns = ["status", "quantidade"]

        mapa_cores_alerta = {
            "Lido": "orange",
            "Pendente": "red",
            "Resolvido": "blue"
        }

        fig = px.bar(
            status_count,
            x="status",
            y="quantidade",
            color="status",
            color_discrete_map=mapa_cores_alerta,
            title="Alertas por Status"
        )
        st.plotly_chart(fig, use_container_width=True)

    if "data/hora" in df_alertas.columns and not df_alertas.empty:
        fig2 = px.histogram(
            df_alertas,
            x="data/hora",
            nbins=30,
            title="Distribuição Temporal dos Alertas"
        )
        st.plotly_chart(fig2, use_container_width=True)

    if "data" in df_alertas.columns and not df_alertas.empty:
        from streamlit_calendar import calendar

        eventos = [
            {
                "title": row.get("status", "Alerta"),
                "start": row["data"].isoformat()
            }
            for _, row in df_alertas.iterrows()
        ]

        opcoes = {
            "initialView": "dayGridMonth",
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": ""
            },
            "locale": "pt-br"
        }

        st.subheader("📅 Calendário de Alertas")
        calendar(eventos, options=opcoes, key="cal_alertas")
  
    if st.button("Gerar Relatório de Alertas"):
        extras = [
            f"Total de alertas: {len(df_alertas)}",
            f"Distribuição de status: {df_alertas['status'].value_counts().to_dict()}",
        ]
        buffer = gerar_pdf("Relatório de Alertas", df_alertas, extras)
        st.download_button("Baixar PDF", buffer, file_name="relatorio_alertas.pdf", mime="application/pdf")

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
    if not df.empty and st.button("Gerar Relatório de Checklists"):
        extras = [
            f"Total de checklists: {len(df)}",
            f"Tipos de inspeção: {df['Tipo'].value_counts().to_dict()}",
            f"Gravidades: {df['Gravidade'].value_counts().to_dict()}",
        ]
        buffer = gerar_pdf("Relatório de Checklists", df, extras)
        st.download_button("Baixar PDF", buffer, file_name="relatorio_checklists.pdf", mime="application/pdf")
