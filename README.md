# 🤖 Trabalho RPA — Bootcamp Energral

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
| Ana Julia Martins         | [@4nanotfound](https://github.com/4nanotfound)     |
| Gabriel Zanoni Herculano  | [@GbrielZanoni](https://github.com/GbrielZanoni)   |
| Mateus Euzébio            | [@mateuseuz](https://github.com/mateuseuz)         |
| Gabriel Moura             | [@gmoura0](https://github.com/gmoura0 )            |
| João Gabriel              | [@JoaoGabFB](https://github.com/JoaoGabFB)         |
| Maria Delmonaco           | [@mariadelmonaco](https://github.com/mariadelmonaco)|

---

## 📁 Estrutura do Repositório

documentos/ → Documentos do Projeto (PDD, ODI, PDI, To-Be, As-Is)
projeto/
├── checklist/ → Aplicação de geração de checklists (.exe)
├── streamlit/ → Painel gerencial e visualizações
│ ├── csv/ → Base de dados (.csv)
│ └── streamlit.py → App principal
├── requirements.txt → Dependências do projeto
├── .gitignore → Itens ignorados no Git
└── README.md → Este documento

---

## 🚀 Como Executar

```bash
# 1. Clone este repositório
git clone https://github.com/GbrielZanoni/TrabalhoRPA.git
cd TrabalhoRPA

# 2. Crie e ative um ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou no Linux/macOS:
# source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o painel Streamlit
cd projeto/streamlit
streamlit run streamlit.py
```
