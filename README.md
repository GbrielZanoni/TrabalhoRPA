[![Build](https://github.com/GbrielZanoni/TrabalhoRPA/actions/workflows/streamlit-check.yml/badge.svg)](https://github.com/GbrielZanoni/TrabalhoRPA/actions/workflows/streamlit-check.yml)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Dependencies](https://img.shields.io/badge/dependencies-poetry-blue)
![License](https://img.shields.io/github/license/GbrielZanoni/TrabalhoRPA)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)
[![Wiki](https://img.shields.io/badge/docs-wiki-blue)](https://github.com/GbrielZanoni/TrabalhoRPA/wiki)
![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)

# 🤖 Atividade de Automação

Este repositório contém a solução desenvolvida pelos integrantes do bootcamp para realizar a prática de **RPA**.

---

## 📌 Sobre o Projeto

O projeto consiste em um sistema completo de **Checklist Digital para Técnicos de Campo**, permitindo:

- Preenchimento digital de inspeções em subestações elétricas
- Geração automática de relatórios em PDF e Excel
- Visualização gerencial via painel analítico com **Streamlit**
- Análise de métricas operacionais, alertas e chamados

O objetivo é **automatizar e centralizar o fluxo de inspeções**, reduzindo papel, aumentando a confiabilidade dos registros e permitindo **tomada de decisão com base em dados**.

---

## 🧠 Tecnologias Utilizadas

- `GitHub`
- `Python 3.11+`
- `Tkinter` (interface desktop)
- `Pandas`, `OpenPyXL`, `FPDF`
- `Streamlit` + `Plotly`
- `PyPDF2` (leitura de PDFs gerados)
- Organização com `.gitignore` e `requirements.txt`

---

## 👨‍💻 Integrantes

| Nome                      | GitHub                                     |
|---------------------------|--------------------------------------------|
| Ana Julia         | [@4nanotfound](https://github.com/4nanotfound)     |
| Gabriel Zanoni  | [@GbrielZanoni](https://github.com/GbrielZanoni)   |
| Mateus Euzébio            | [@mateuseuz](https://github.com/mateuseuz)         |
| Gabriel Moura             | [@gmoura0](https://github.com/gmoura0 )            |
| João Gabriel              | [@JoaoGabFB](https://github.com/JoaoGabFB)         |
| Maria Delmonaco           | [@mariadelmonaco](https://github.com/mariadelmonaco)|

---

## 📁 Estrutura do Repositório

```text
documentos/              → Documentos do Projeto (PDD, ODI, PDI, To-Be, As-Is)
projeto/
├── checklist/           → Aplicação de geração de checklists (.exe)
├── streamlit/           → Painel gerencial e visualizações
│   ├── csv/             → Base de dados (.csv)
│   └── streamlit.py     → App principal
├── requirements.txt     → Dependências do projeto
├── .gitignore           → Itens ignorados no Git
└── README.md            → Este documento
```
---

## 🚀 Como Executar

```bash
# 1. Clone este repositório
git clone https://github.com/GbrielZanoni/TrabalhoRPA.git
cd TrabalhoRPA

# 2. Instale o Poetry (caso ainda não tenha)
# https://python-poetry.org/docs/#installation

# 3. Instale as dependências e crie o ambiente virtual automaticamente
poetry install

# 4. Ative o ambiente virtual gerenciado pelo Poetry
poetry shell

# 5. Execute o painel Streamlit
cd projeto/streamlit
streamlit run streamlit.py
```


