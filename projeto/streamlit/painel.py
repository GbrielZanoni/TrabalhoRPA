import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime, date
from fpdf import FPDF
from io import BytesIO
from api import obter_chamados, validar_chamado_api
from streamlit_echarts import st_echarts
import random

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
        estilo_titulo = "font-size: 16px; color: #ffffff; margin-bottom: 0.2rem;"
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
        estilo_titulo = "font-size: 16px; color: #ffffff; margin-bottom: 0.2rem;"
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
            "legend": {"top": "bottom", "textStyle": {"color": "#fff"}},
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
                    "label": {"show": False, "position": "center", "color": "#fff"},
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
    st.markdown("### Funcionários")

    def cor_por_area(area):
        cores = {
            "Manutenção": "#1e3a8a",
            "Inspeção": "#065f46",
            "Segurança": "#7c2d12",
            "Operações": "#4b5563"
        }
        return cores.get(area, "#3b82f6")

    def icone_senioridade(nivel):
        icones = {
            "Júnior": "👶",
            "Pleno": "🧑‍💼",
            "Sênior": "🧓"
        }
        return icones.get(nivel, "🔧")

    for i in range(0, len(df_tec), 4):
        row = df_tec.iloc[i:i+4]
        cols = st.columns(len(row))

        for j, (_, item) in enumerate(row.iterrows()):
            nome = item.get("nome", "Técnico")
            nivel = item.get("nivel_de_experiencia", "—")
            area = item.get("area_de_atuacao", "—")
            iniciais = "".join([parte[0] for parte in nome.split()[:2]]).upper()

            id_ = item.get("id", "—")
            email = item.get("email", "—")
            telefone = item.get("telefone", "—")
            cor = cor_por_area(area)
            icone = icone_senioridade(nivel)

            tooltip = f"ID: {id_}\nEmail: {email}\nTelefone: {telefone}"

            cols[j].markdown(f"""
                <div style="padding: 8px;">
                    <div title="{tooltip}" style="
                        border-radius: 16px;
                        background: linear-gradient(135deg, {cor} 0%, #111827 100%);
                        padding: 16px;
                        text-align: center;
                        height: 250px;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.25);
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        transition: all 0.3s ease;
                        cursor: default;
                    ">
                        <div>
                            <div style="
                                width:90px;
                                height:90px;
                                border-radius:50%;
                                background:#fff3;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                margin:auto;
                            ">
                                <span style="font-size:36px;color:#fff;font-weight:700;">{iniciais}</span>
                            </div>
                            <div style="font-size:18px; font-weight:600; color:#fff; margin-top:0.8rem;">{nome}</div>
                            <div style="font-size:14px; color:#d1d5db;">{nivel} {icone}</div>
                        </div>
                        <div style="font-size:13px; color:#9ca3af;">{area}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

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
        estilo_titulo = "font-size: 14px; color: #ffffff; margin-bottom: 0.2rem;"

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

    with st.container(border=True):
            total_insp = len(df_insp)
            criterio_counts = df_insp["criterio_de_aprovacao"].value_counts().head(4)
            col1, col2, col3, col4, col5 = st.columns(5)

            estilo_box = """
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                min-height: 100px;
                padding: 5px;
                box-sizing: border-box;
                text-align: center;
            """
            estilo_titulo = "font-size: 14px; color: #ffffff; margin-bottom: 0.5rem;"
            estilo_valor_total = "font-size: 28px; font-weight: 700; margin: 0; color: #2DD4BF;"
            estilo_valor = "font-size: 24px; font-weight: 600; margin: 0;"

            with col1:
                st.markdown(
                    f"""
                    <div style="{estilo_box}">
                        <div style="{estilo_titulo}">Total de Inspeções</div>
                        <div style="{estilo_valor_total}">{total_insp}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            for i, (criterio, qtd) in enumerate(criterio_counts.items()):
                cor = "#00cc66" if qtd >= 15 else "#ff4d4d"
                seta = "↑" if qtd >= 15 else "↓"
                estilo_valor_criterio = f"{estilo_valor} color: {cor};"

                with [col2, col3, col4, col5][i]:
                    st.markdown(
                        f"""
                        <div style="{estilo_box}">
                            <div style="{estilo_titulo}">{criterio}</div>
                            <div style="{estilo_valor_criterio}">{qtd} {seta}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
    if "criterio_de_aprovacao" in df_insp.columns:
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
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "textStyle": {"color": "#888"}
            },
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
    st.markdown("---")
    st.subheader("Alertas e Notificações")
    df_alertas = dados["alertas"].copy()

    if "data/hora" in df_alertas.columns:
        df_alertas["data/hora"] = pd.to_datetime(df_alertas["data/hora"], errors="coerce")
        df_alertas = df_alertas.dropna(subset=["data/hora"])
        df_alertas["data"] = df_alertas["data/hora"].dt.date

    with st.container(border=True):
        total_alertas = len(df_alertas)
        status_counts = df_alertas["status"].value_counts()

        col1, col2, col3, col4 = st.columns(4)

        estilo_box = """
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            min-height: 120px;
            padding: 12px;
            box-sizing: border-box;
            text-align: center;
        """
        estilo_titulo = "font-size: 14px; color: #ffffff; margin-bottom: 0.5rem;"
        estilo_valor_total = "font-size: 28px; font-weight: 700; margin: 0; color: #2DD4BF;"
        estilo_valor = "font-size: 24px; font-weight: 600; margin: 0;"

        with col1:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Total de Alertas</div>
                    <div style="{estilo_valor_total}">{total_alertas}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        for i, status in enumerate(["Lido", "Pendente", "Resolvido"]):
            cor = {"Lido": "#f97316", "Pendente": "#ef4444", "Resolvido": "#3b82f6"}.get(status, "#999")
            qtd = status_counts.get(status, 0)
            estilo_valor_status = f"{estilo_valor} color: {cor};"

            with [col2, col3, col4][i]:
                st.markdown(
                    f"""
                    <div style="{estilo_box}">
                        <div style="{estilo_titulo}">{status}</div>
                        <div style="{estilo_valor_status}">{qtd}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if "tipo_de_alerta" in df_alertas.columns:
        tipo_counts = df_alertas["tipo_de_alerta"].value_counts()
        pie_data = [{"value": int(qtd), "name": tipo} for tipo, qtd in tipo_counts.items()]

        pie_option = {
            "tooltip": {
                "trigger": "item",
                "formatter": "{b}: {c} ({d}%)", 
                "textStyle": {"color": "#888"},  
                "backgroundColor": "#fff"       
            },
            "legend": {"top": "bottom", "textStyle": {"color": "#fff"}},
            "series": [
                {
                    "name": "Tipo de Alerta",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "label": {"show": True, "color": "#fff"},
                    "labelLine": {"lineStyle": {"color": "#fff"}},
                    "data": pie_data
                }
            ]
        }

        st_echarts(options=pie_option, height="350px")

    if "status" in df_alertas.columns and not df_alertas.empty:
        status_counts = df_alertas["status"].value_counts().reset_index()
        status_counts.columns = ["status", "quantidade"]

        cor_status = {
            "Lido": "#f97316",
            "Pendente": "#ef4444",
            "Resolvido": "#3b82f6"
        }

        series_data = []
        for _, row in status_counts.iterrows():
            nome = row["status"]
            qtd = row["quantidade"]
            cor = cor_status.get(nome, "#999")
            series_data.append({
                "value": qtd,
                "name": nome,
                "itemStyle": {"color": cor}
            })
    
        bar_option = {
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}, "textStyle": {"color": "#888"}},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {"type": "value", "axisLabel": {"color": "#fff"}},
            "yAxis": {
                "type": "category",
                "data": status_counts["status"].tolist(),
                "axisLabel": {"color": "#fff"}
            },
            "series": [
                {
                    "name": "Status",
                    "type": "bar",
                    "data": series_data,
                    "label": {"show": True, "color": "#fff"}
                }
            ]
        }

        st_echarts(options=bar_option, height="350px")

    if not df_alertas.empty and "data" in df_alertas.columns:
        calendar_data = df_alertas.groupby("data").size().reset_index(name="count")
        calendar_data["data"] = calendar_data["data"].astype(str)

        calendar_option = {
            "tooltip": {"position": "top", "textStyle": {"color": "#888"}},
            "visualMap": {
                "min": 0,
                "max": int(calendar_data["count"].max()),
                "type": "piecewise",
                "orient": "horizontal",
                "left": "center",
                "top": 0,
                "textStyle": {"color": "#fff"}
            },
            "calendar": {
                "top": 50,
                "left": 30,
                "right": 30,
                "cellSize": ["auto", 20],
                "range": str(pd.to_datetime(calendar_data["data"]).min().year),
                "itemStyle": {"borderWidth": 0.5},
                "dayLabel": {"color": "#fff"},
                "monthLabel": {"color": "#fff"},
                "yearLabel": {"color": "#fff"},
            },
            "series": [{
                "type": "heatmap",
                "coordinateSystem": "calendar",
                "data": calendar_data.values.tolist()
            }]
        }

        st_echarts(options=calendar_option, height="250px")

    with st.expander("Dados Detalhados", expanded=False):
        st.data_editor(df_alertas, use_container_width=True, num_rows="dynamic", disabled=True)

        extras = [
            f"Total de alertas: {len(df_alertas)}",
            f"Distribuição de status: {df_alertas['status'].value_counts().to_dict()}",
        ]
        buffer = gerar_pdf("Relatório de Alertas", df_alertas, extras)

       
        st.download_button(
                    "Gerar Relatório de Inspeções",
                    buffer,
                    file_name="relatorio_inspecoes.pdf",
                    mime="relatorio_alertas/pdf",
                    use_container_width=True,
                )

elif aba == "Checklists":
    st.subheader("Checklists")
    with st.spinner("Buscando chamados ..."):
        chamados = obter_chamados()

    if not chamados:
        st.info("Nenhum chamado encontrado.")
        st.stop()

    df_chamados = pd.DataFrame(chamados)

    if "data/hora" in df_chamados.columns:
        df_chamados["data/hora"] = pd.to_datetime(df_chamados["data/hora"], errors="coerce")
        df_chamados = df_chamados.dropna(subset=["data/hora"])
        df_chamados["data"] = df_chamados["data/hora"].dt.date

    with st.container(border=True):
        total_chamados = len(df_chamados)
        status_counts = df_chamados["situacao_subestacao"].value_counts() if "situacao_subestacao" in df_chamados.columns else {}

        col1, col2, col3, col4 = st.columns(4)
        estilo_box = """
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            min-height: 120px;
            padding: 12px;
            box-sizing: border-box;
            text-align: center;
        """
        estilo_titulo = "font-size: 14px; color: #ffffff; margin-bottom: 0.5rem;"
        estilo_valor_total = "font-size: 28px; font-weight: 700; margin: 0; color: #2DD4BF;"
        estilo_valor = "font-size: 24px; font-weight: 600; margin: 0;"

        with col1:
            st.markdown(
                f"""
                <div style="{estilo_box}">
                    <div style="{estilo_titulo}">Total de Chamados</div>
                    <div style="{estilo_valor_total}">{total_chamados}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        for i, status in enumerate(["Crítica", "Normal", "Quebrada"]):
            cor = {"Crítica": "#f97316", "Normal": "#10B981", "Quebrada": "#ef4444"}.get(status, "#999")
            qtd = status_counts.get(status, 0)
            estilo_valor_status = f"{estilo_valor} color: {cor};"

            if i + 1 < 5:
                with [col2, col3, col4][i]:
                    st.markdown(
                        f"""
                        <div style="{estilo_box}">
                            <div style="{estilo_titulo}">{status}</div>
                            <div style="{estilo_valor_status}">{qtd}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    if "situacao_subestacao" in df_chamados.columns:
        pie_data = df_chamados["situacao_subestacao"].value_counts().reset_index()
        pie_data.columns = ["Situação", "Quantidade"]
        pie_data = [{"value": int(row["Quantidade"]), "name": row["Situação"]} for _, row in pie_data.iterrows()]

        situacao_option = {
            "tooltip": {
                "trigger": "item",
                "formatter": "{b}: {c} ({d}%)",
                "textStyle": {"color": "#000"},
                "backgroundColor": "#fff"
            },
            "legend": {"top": "bottom", "textStyle": {"color": "#fff"}},
            "series": [
                {
                    "name": "Situação",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "label": {"show": True, "color": "#fff"},
                    "labelLine": {"lineStyle": {"color": "#fff"}},
                    "data": pie_data
                }
            ]
        }

        st_echarts(options=situacao_option, height="350px")

    if not df_chamados.empty and "data_hora" in df_chamados.columns:
        df_chamados["data_hora"] = pd.to_datetime(df_chamados["data_hora"], errors="coerce")
        df_chamados = df_chamados.dropna(subset=["data_hora"])
        df_chamados["data"] = df_chamados["data_hora"].dt.date

        calendar_data = df_chamados.groupby("data").size().reset_index(name="count")
        calendar_data["data"] = calendar_data["data"].astype(str)

        calendar_option = {
            "tooltip": {"position": "top", "textStyle": {"color": "#888"}},
            "visualMap": {
                "min": 0,
                "max": int(calendar_data["count"].max()),
                "type": "piecewise",
                "orient": "horizontal",
                "left": "center",
                "top": 0,
                "textStyle": {"color": "#fff"}
            },
            "calendar": {
                "top": 50,
                "left": 30,
                "right": 30,
                "cellSize": ["auto", 20],
                "range": str(pd.to_datetime(calendar_data["data"]).min().year),
                "itemStyle": {"borderWidth": 0.5},
                "dayLabel": {"color": "#fff"},
                "monthLabel": {"color": "#fff"},
                "yearLabel": {"color": "#fff"},
            },
            "series": [{
                "type": "heatmap",
                "coordinateSystem": "calendar",
                "data": calendar_data.values.tolist()
            }]
        }

        st_echarts(options=calendar_option, height="250px")

    if "local_subestacao" in df_chamados.columns and not df_chamados.empty:
        local_counts = df_chamados["local_subestacao"].value_counts().reset_index()
        local_counts.columns = ["local_subestacao", "quantidade"]

        cores_unicas = {}
        for sub in local_counts["local_subestacao"]:
            if sub not in cores_unicas:
                cores_unicas[sub] = f"#{random.randint(0, 0xFFFFFF):06x}"

        series_data = [
            {
                "value": row["quantidade"],
                "name": row["local_subestacao"],
                "itemStyle": {"color": cores_unicas.get(row["local_subestacao"], "#888")}
            }
            for _, row in local_counts.iterrows()
        ]

        bar_local_option = {
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "textStyle": {"color": "#888"}
            },
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {"type": "value", "axisLabel": {"color": "#fff"}},
            "yAxis": {
                "type": "category",
                "data": local_counts["local_subestacao"].tolist(),
                "axisLabel": {"color": "#fff"}
            },
            "series": [
                {
                    "name": "Local da Subestação",
                    "type": "bar",
                    "data": series_data,
                    "label": {"show": True, "color": "#fff"}
                }
            ]
        }

        st_echarts(options=bar_local_option, height="350px")

    with st.expander("Dados Detalhados", expanded=False):
        st.data_editor(df_chamados, use_container_width=True, num_rows="dynamic", disabled=True)

        extras = [
            f"Total de chamados: {len(df_chamados)}",
            f"Gravidades: {df_chamados['gravidade'].value_counts().to_dict() if 'gravidade' in df_chamados else {}}",
            f"Tipos de inspeção: {df_chamados['Tipo de Inspeção'].value_counts().to_dict() if 'Tipo de Inspeção' in df_chamados else {}}",
        ]
        buffer = gerar_pdf("Relatório de Checklists", df_chamados, extras)

        st.markdown("Validar Chamado")

        with st.form("form_validacao_detalhado"):
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                id_opcao = st.selectbox(
                    "Selecione o ID",
                    df_chamados["id"] if "id" in df_chamados.columns else df_chamados.index,
                    format_func=lambda x: f"Chamado #{x}"
                )
            with col2:
                submit = st.form_submit_button("Validar", use_container_width=True)

            if submit:
                with st.spinner("Enviando validação..."):
                    resultado = validar_chamado_api(int(id_opcao), True)

                if not resultado.get("erro"):
                    st.success(f"Chamado #{id_opcao} validado com sucesso!")
                    st.rerun()
                else:
                    st.error(f"Erro ao validar: {resultado['erro']}")
    
        st.download_button(
            "Gerar Relatório de Checklists",
            buffer,
            file_name="relatorio_checklists.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

