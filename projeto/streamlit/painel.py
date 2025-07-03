import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime, date
from fpdf import FPDF
from io import BytesIO
from api import obter_chamados, validar_chamado_api
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Dashboard Energral", page_icon="⚡", layout="centered")

st.title("Dashboard Energral")

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
    for _, row in df.iterrows():
        texto = " | ".join(f"{col}: {row[col]}" for col in df.columns[:4])
        pdf.multi_cell(0, 6, texto, 0, 1)
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return BytesIO(pdf_bytes)

dados = carregar_dados()

with st.sidebar:
    st.markdown(
        """
        <div style="padding-bottom: 1rem;">
            <h2 style='margin-bottom:0; font-size: 1.6rem;'>Energral</h2>
            <p style='margin-top:0; color: #888;'>Painel de Gestão Operacional</p>
        </div>
        """, unsafe_allow_html=True
    )

    st.radio(
        "Navegação",
        ["Geral", "Técnicos", "Equipamentos", "Inspeções", "Alertas", "Checklists"],
        label_visibility="collapsed",
        key="navegacao"
    )

    st.markdown(
        f"""
        <hr style="margin-top:2rem; margin-bottom:0.8rem;">
        <p style='font-size: 0.9rem; color: #666;'>Hoje é: <strong>{date.today().strftime('%d/%m/%Y')}</strong></p>
        """, unsafe_allow_html=True
    )

    st.caption("© 2025 Energral | RPA Team")

aba = st.session_state["navegacao"]

if aba == "Geral":
    
    st.markdown("---")
    st.subheader("Visão Geral")
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)

        estilo_box = """
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 0.5rem 0;
        """
        estilo_titulo = "font-size: 16px; color: #888; margin-bottom: 0.2rem;"
        estilo_valor = "font-size: 32px; font-weight: 600; margin-top: 0;"

        with col1:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Inspeções</div>
                    <div style="{estilo_valor}">{len(dados['inspeções'])}</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Equipamentos</div>
                    <div style="{estilo_valor}">{len(dados['equipamentos'])}</div>
                </div>
                """, unsafe_allow_html=True)

        with col3:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Técnicos</div>
                    <div style="{estilo_valor}">{len(dados['tecnicos'])}</div>
                </div>
                """, unsafe_allow_html=True)

        with col4:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Alertas</div>
                    <div style="{estilo_valor}">{len(dados['alertas'])}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ## Sobre o Projeto
    O **Painel Gerencial - Energral** é uma aplicação interativa desenvolvida para apoiar a tomada de decisão e a gestão operacional de uma empresa fictícia do setor de energia elétrica.
    A **Energral** é especializada na manutenção e operação de subestações, linhas de transmissão e sistemas de distribuição de energia. O projeto simula o monitoramento de suas operações, com base em dados simulados de inspeções, equipes técnicas, equipamentos instalados e alertas operacionais.
    Este painel foi desenvolvido como parte de uma atividade prática de RPA.
    
    ---

    ### Funcionalidades
    - Visão Geral com totais de inspeções, equipamentos, técnicos e alertas.
    - Análise de Técnicos com distribuição por experiência e áreas de atuação.
    - Inventário de Equipamentos com classificação por tipo.
    - Histórico de Inspeções com critérios de aprovação.
    - Alertas Operacionais com evolução temporal.
    - Leitura Automática de Checklists.
    ---
    ### Equipe
    - Ana Julia – [@4nanotfound](https://github.com/4nanotfound)  
    - Gabriel Zanoni – [@GbrielZanoni](https://github.com/GbrielZanoni)  
    - Mateus Euzébio – [@mateuseuz](https://github.com/mateuseuz)  
    - Gabriel Moura – [@gmoura0](https://github.com/gmoura0)  
    - João Gabriel – [@JoaoGabFB](https://github.com/JoaoGabFB)  
    - Maria Delmonaco – [@mariadelmonaco](https://github.com/mariadelmonaco)
    """)

elif aba == "Técnicos":
    
    st.markdown("---")
    st.subheader("Equipes Técnicas")

    df_tec = dados["tecnicos"]
    niveis = df_tec["nivel_de_experiencia"].value_counts()

    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)

        estilo_box = """
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 0.5rem 0;
        """
        estilo_titulo = "font-size: 16px; color: #888; margin-bottom: 0.2rem;"
        estilo_valor = "font-size: 32px; font-weight: 600; margin-top: 0;"

        with col1:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Funcionários</div>
                    <div style="{estilo_valor}">{len(df_tec)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Júnior</div>
                    <div style="{estilo_valor}">{niveis.get("Júnior", 0)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Pleno</div>
                    <div style="{estilo_valor}">{niveis.get("Pleno", 0)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Sênior</div>
                    <div style="{estilo_valor}">{niveis.get("Sênior", 0)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


    if "area_de_atuacao" in df_tec.columns:
        areas = df_tec["area_de_atuacao"].value_counts()
        option = {
            "tooltip": {"trigger": "item"},
            "legend": {
                "top": "bottom",
                "textStyle": {
                    "color": "#fff"
                }
            },
            "series": [
                {
                    "name": "Área de Atuação",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "avoidLabelOverlap": False,
                    "itemStyle": {
                        "borderRadius": 10,
                        "borderColor": "#fff",
                        "borderWidth": 2
                    },
                    "label": {
                        "show": False,
                        "position": "center",
                        "color": "#fff"
                    },
                    "emphasis": {
                        "label": {
                            "show": True,
                            "fontSize": 16,
                            "fontWeight": "bold",
                            "color": "#fff"
                        }
                    },
                    "labelLine": {"show": False},
                    "data": [{"value": int(qtd), "name": area} for area, qtd in areas.items()],
                }
            ],
        }

        from streamlit_echarts import st_echarts
        st_echarts(option, height="400px")

        with st.expander("Dados Detalhados"):
            st.data_editor(df_tec, use_container_width=True, num_rows="dynamic", disabled=True)
            
            extras = [
                f"Total de funcionários: {len(df_tec)}",
                f"Distribuição de níveis: {niveis.to_dict()}",
                f"Áreas de atuação: {areas.to_dict() if 'areas' in locals() else 'N/A'}",
            ]
            buffer = gerar_pdf("Relatório de Técnicos", df_tec, extras)
            
            st.download_button(
                label="Gerar Relatório de Técnicos",
                data=buffer,
                file_name="relatorio_tecnicos.pdf",
                mime="application/pdf",
                use_container_width=True
            )

elif aba == "Equipamentos":
    
    st.markdown("---")
    st.subheader("Equipamentos")
    df_eq = dados["equipamentos"]

    with st.container(border=True):
        top5 = df_eq["tipo"].value_counts().head(5)
        col1, col2, col3, col4, col5 = st.columns(5)

        estilo_box = """
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            min-height: 100px;
            text-align: center;
        """
        estilo_titulo = "font-size: 14px; color: #888; margin-bottom: 0.2rem;"

        for i, (tipo, qtd) in enumerate(top5.items()):
            cor = "#00cc66" if qtd >= 21 else "#ff4d4d"
            seta = "↑" if qtd >= 21 else "↓"
            estilo_valor = f"font-size: 24px; font-weight: 600; margin-top: 0; color: {cor};"

            with [col1, col2, col3, col4, col5][i]:
                st.markdown(
                    f"""
                    <div style="{estilo_box}">
                        <div style="{estilo_titulo}">{tipo}</div>
                        <div style="{estilo_valor}">{qtd} {seta}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if "tipo" in df_eq.columns:
        tipo_counts = df_eq["tipo"].value_counts()
        pie_data = [{"value": int(qtd), "name": tipo} for tipo, qtd in tipo_counts.items()]

        pie_option = {
            "tooltip": {"trigger": "item"},
            "legend": {"top": "bottom", "textStyle": {"color": "#fff"}},
            "series": [
                {
                    "name": "Tipo de Equipamento",
                    "type": "pie",
                    "radius": "60%",
                    "data": pie_data,
                    "label": {
                        "color": "#fff"
                    },
                    "emphasis": {
                        "itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"}
                    },
                }
            ],
        }

        st_echarts(options=pie_option, height="400px")
    
    if "status_atual" in df_eq.columns:
        status_counts = df_eq["status_atual"].value_counts().reset_index()
        status_counts.columns = ["status", "quantidade"]

        cor_status = {
            "Operacional": "#10B981",       
            "Com falha": "#EF4444",         
            "Inativo": "#FACC15",          
            "Em manutenção": "#F97316",     
        }

        series_data = []
        for _, row in status_counts.iterrows():
            status = row["status"]
            quantidade = row["quantidade"]
            cor = cor_status.get(status, "#999") 
            series_data.append({
                "value": quantidade,
                "name": status,
                "itemStyle": {"color": cor}
            })

        status_option = {
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {"type": "value"},
            "yAxis": {
                "type": "category",
                "data": status_counts["status"].tolist(),
                "axisLabel": {"color": "#fff"},
            },
            "series": [
                {
                    "name": "Equipamentos",
                    "type": "bar",
                    "data": series_data,
                }
            ],
        }

        st_echarts(options=status_option, height="350px")

    with st.expander("Dados Detalhados", expanded=False):
        st.data_editor(df_eq, use_container_width=True, num_rows="dynamic", disabled=True)

        extras = [
            f"Total de equipamentos: {len(df_eq)}",
            f"Tipos: {df_eq['tipo'].value_counts().to_dict()}",
            f"Pontos de instalação: {df_eq['localizacao'].nunique()} locais",
        ]
        buffer = gerar_pdf("Relatório de Equipamentos", df_eq, extras)

        st.download_button(
            "Gerar Relatório de Equipamentos",
            buffer,
            file_name="relatorio_equipamentos.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

elif aba == "Inspeções":
    st.markdown("---")
    st.subheader("Inspeções Realizadas")
    df_insp = dados["inspeções"]
 
 
    criterio = df_insp["criterio_de_aprovacao"].value_counts().reset_index()
    criterio.columns = ["Critério", "Quantidade"]

    cor_criterio = {
        "Sem danos visíveis": "#10B981",  
        "Funcionamento normal": "#059669",  
        "Sinal estável": "#FACC15",         
        "Dentro dos parâmetros": "#EF4444", 
    }

    criterio_data = []
    for _, row in criterio.iterrows():
        nome = row["Critério"]
        qtd = row["Quantidade"]
        cor = cor_criterio.get(nome, "#999")  
        criterio_data.append({
            "value": qtd,
            "name": nome,
            "itemStyle": {"color": cor}
        })

    criterio_option = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {
            "type": "category",
            "data": criterio["Critério"].tolist(),
            "axisLabel": {"color": "#fff"},
        },
        "series": [
            {
                "name": "Inspeções",
                "type": "bar",
                "data": criterio_data,
            }
        ],
    }

    st_echarts(options=criterio_option, height="350px")
    with st.expander("Dados Detalhados", expanded=False):
        st.data_editor(df_insp, use_container_width=True, num_rows="dynamic", disabled=True)

        extras = [
            f"Total de inspeções: {len(df_insp)}",
            f"Critérios de aprovação: {criterio.set_index('Critério')['Quantidade'].to_dict() if 'criterio' in locals() else 'N/A'}",
        ]
        buffer = gerar_pdf("Relatório de Inspeções", df_insp, extras)

        st.download_button(
            "Gerar Relatório de Inspeções",
            buffer,
            file_name="relatorio_inspecoes.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

elif aba == "Alertas":
    st.subheader("🚨 Alertas e Notificações")
    df_alertas = dados["alertas"].copy()
    if "data/hora" in df_alertas.columns:
        df_alertas["data/hora"] = pd.to_datetime(df_alertas["data/hora"], errors="coerce")
        df_alertas = df_alertas.dropna(subset=["data/hora"])
        df_alertas["data"] = df_alertas["data/hora"].dt.date
    st.dataframe(df_alertas, hide_index=True)
    if "status" in df_alertas.columns and not df_alertas.empty:
        status_count = df_alertas["status"].value_counts().reset_index()
        status_count.columns = ["status", "quantidade"]
        st.plotly_chart(px.bar(status_count, x="status", y="quantidade", color="status", color_discrete_map={"Lido": "orange", "Pendente": "red", "Resolvido": "blue"}), use_container_width=True)
    if "data/hora" in df_alertas.columns and not df_alertas.empty:
        st.plotly_chart(px.histogram(df_alertas, x="data/hora", nbins=30), use_container_width=True)
    if st.button("Gerar Relatório de Alertas"):
        extras = [
            f"Total de alertas: {len(df_alertas)}",
            f"Distribuição de status: {df_alertas['status'].value_counts().to_dict()}",
        ]
        buffer = gerar_pdf("Relatório de Alertas", df_alertas, extras)
        st.download_button("Baixar PDF", buffer, file_name="relatorio_alertas.pdf", mime="application/pdf")

elif aba == "Checklists":
    st.subheader("📂 Checklists")
    with st.spinner("🔄 Buscando chamados ..."):
        chamados = obter_chamados()
    if not chamados:
        st.info("⚠️ Nenhum chamado encontrado.")
        st.stop()
    df_chamados = pd.DataFrame(chamados)
    if "validez" in df_chamados.columns:
        df_chamados["validez"] = df_chamados["validez"].astype(bool)
        outras = [c for c in df_chamados.columns if c != "validez"]
        df_chamados = df_chamados[outras + ["validez"]]
    st.dataframe(df_chamados, hide_index=True, height=420)
    st.markdown("### ✅ Validar chamado")
    csel, cbtn = st.columns([3, 1])
    with csel:
        id_opcao = st.selectbox("Selecione o ID", df_chamados["id"] if "id" in df_chamados.columns else df_chamados.index)
    with cbtn:
        if st.button("Validar"):
            with st.spinner("Enviando validação ..."):
                resultado = validar_chamado_api(int(id_opcao), True)
            if not resultado.get("erro"):
                st.success("Chamado validado com sucesso!")
                st.rerun()
            else:
                st.error(f"Erro ao validar: {resultado['erro']}")
    st.markdown("---\n### Análise dos Chamados")
    if "Tipo de Inspeção" in df_chamados.columns:
        tipo = df_chamados["Tipo de Inspeção"].value_counts().reset_index()
        tipo.columns = ["Tipo", "Quantidade"]
        st.plotly_chart(px.pie(tipo, names="Tipo", values="Quantidade"), use_container_width=True)
    if "Gravidade" in df_chamados.columns:
        grav = df_chamados["Gravidade"].value_counts().reset_index()
        grav.columns = ["Gravidade", "Quantidade"]
        st.plotly_chart(px.bar(grav, x="Gravidade", y="Quantidade"), use_container_width=True)
    if "Técnico" in df_chamados.columns:
        tecnico = df_chamados["Técnico"].value_counts().reset_index()
        tecnico.columns = ["Técnico", "Total"]
        st.plotly_chart(px.bar(tecnico, x="Técnico", y="Total"), use_container_width=True)
    if "Ação Tomada" in df_chamados.columns:
        acao = df_chamados["Ação Tomada"].value_counts().reset_index()
        acao.columns = ["Ação", "Qtd"]
        st.plotly_chart(px.pie(acao, names="Ação", values="Qtd"), use_container_width=True)
    if st.button("Gerar Relatório de Chamados"):
        extras = [
            f"Total de chamados: {len(df_chamados)}",
            f"Distribuição de gravidade: {df_chamados['Gravidade'].value_counts().to_dict()}",
            f"Tipos de inspeção: {df_chamados['Tipo de Inspeção'].value_counts().to_dict()}",
        ]
        buffer = gerar_pdf("Relatório de Chamados", df_chamados, extras)
        st.download_button("Baixar Relatório PDF", buffer, file_name="relatorio_chamados.pdf", mime="application/pdf")
