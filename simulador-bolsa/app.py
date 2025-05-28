import streamlit as st
from bolsa import *

sistema_bolsa: SistemaBolsa = st.session_state.sistema_bolsa if 'sistema_bolsa' in st.session_state.keys() else SistemaBolsa()

    
def pregao_page():
    pass


def lista_ativos_page():
    pass


@st.dialog('Cadastrar Pessoa Juridica')
def cadastrar_pessoa_juridica_dialog():
    with st.form(clear_on_submit=True, border=False, key='cadastrar_pessoa_juridica_form'):
        nome = st.text_input('Razão Social:')
        cnpj = st.text_input('CNPJ:')
        saldo = st.number_input('Saldo (R$):', min_value=0, value=1000000)
        if st.form_submit_button('Submeter'):
            sistema_bolsa.cadastrar_pessoa_juridica(nome, cnpj, saldo)
            st.rerun()


def lista_pessoas_juridicas_page():
    with st.sidebar:
        st.button('Cadastrar Pessoa Jurídica', use_container_width=True, on_click=cadastrar_pessoa_juridica_dialog)

    for pj in sistema_bolsa.pessoas_juridicas:
        with st.container(border=True):
            st.write('**Nome Completo:** ', pj.nome)
            st.write('**CNPJ**: ', pj.cnpj)
            st.write('**Saldo**: R$', pj.saldo)


@st.dialog('Cadastrar Pessoa Física')
def cadastrar_pessoa_fisica_dialog():
    with st.form(clear_on_submit=True, border=False, key='cadastrar_pessoa_fisica_form'):
        nome = st.text_input('Nome Completo:')
        cpf = st.text_input('CPF:')
        saldo = st.number_input('Saldo (R$):', min_value=0, value=1000)
        if st.form_submit_button('Submeter'):
            sistema_bolsa.cadastrar_pessoa_fisica(nome, cpf, saldo)
            st.rerun()


def lista_pessoas_fisicas_page():
    with st.sidebar:
        st.button('Cadastrar Pessoa Física', use_container_width=True, on_click=cadastrar_pessoa_fisica_dialog)

    for pf in sistema_bolsa.pessoas_fisicas:
        with st.container(border=True):
            st.write('**Nome Completo:** ', pf.nome)
            st.write('**CPF**: ', pf.cpf)
            st.write('**Saldo**: R$', pf.saldo)


def home_page():
    st.title('**Bolsa de Valores da Cyber (BOVAC)**')


def main():
    if 'sistema_bolsa' not in st.session_state.keys():
        st.session_state.sistema_bolsa = sistema_bolsa

    st.logo('logo.png')

    nav = st.navigation([
        st.Page(home_page, title='Início'),
        st.Page(lista_pessoas_fisicas_page, title='Pessoas Físicas'),
        st.Page(lista_pessoas_juridicas_page, title='Pessoas Jurídicas'),
        st.Page(lista_ativos_page, title='Ativos'),
        st.Page(pregao_page, title='Pregao')
    ])
    nav.run()


main()