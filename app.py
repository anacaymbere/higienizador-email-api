import streamlit as st
import requests
import pandas as pd

# Configuração da página no Streamlit
st.set_page_config(
    page_title="Higienizador de E-mails",
    page_icon="📧",
    layout="centered"
)

# URL da sua API hospedada no Render
API_URL = "https://higienizador-email-api.onrender.com/v1/higienizar-lote"

st.title("📧 Higienizador de E-mails")
st.write(
    "Valide, desduplique e corrija domínios de e-mails automaticamente "
    "usando nossa ferramenta gratuita."
)

st.markdown("---")

# Caixa de texto para entrada de dados
entrada_texto = st.text_area(
    "Cole sua lista de e-mails abaixo (um por linha):",
    height=200,
    placeholder="exemplo1@gmal.com\nCONTATO@UOL.COM\nexemplo1@gmal.com\nteste@outlok.com"
)

# Botão de Ação
if st.button("🚀 Higienizar E-mails", type="primary"):
    # Converte o texto em uma lista de linhas não vazias
    lista_emails = [linha.strip() for linha in entrada_texto.split("\n") if linha.strip()]

    if not lista_emails:
        st.warning("Por favor, insira pelo menos um e-mail antes de continuar.")
    else:
        with st.spinner("Processando e higienizando sua lista..."):
            try:
                # Dispara a requisição POST para a sua API no Render
                response = requests.post(API_URL, json={"emails": lista_emails})
                
                if response.status_code == 200:
                    dados = response.json()
                    
                    st.success("Processamento concluído com sucesso!")
                    
                    # Exibe métricas e estatísticas em cartões
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Recebidos", dados["total_recebidos"])
                    col2.metric("Únicos Filtrados", dados["total_unicos"])
                    col3.metric("E-mails Corrigidos", dados["total_alterados"])

                    st.markdown("---")
                    st.subheader("📋 Lista Tratada")

                    # Converte o resultado em uma Tabela Pandas para exibição amigável
                    df = pd.DataFrame(dados["itens"])
                    df.columns = ["E-mail Original", "E-mail Higienizado", "Foi Alterado?", "Formato Válido?"]
                    
                    st.dataframe(df, use_container_width=True)

                    # Botão para baixar em CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Baixar Resultado em CSV",
                        data=csv,
                        file_name="emails_higienizados.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("Ocorreu um erro ao processar no servidor. Tente novamente.")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")