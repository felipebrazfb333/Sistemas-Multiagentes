import streamlit as st
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever

from config import *

#Informações de metadados
metadata_info = [
    AttributeInfo(
        name="id_doc",
        description="O identificador do documento",
        type="string"),
    AttributeInfo(
        name="tipo",
        description="O tipo da seção",
        type="string"),
    AttributeInfo(
        name="id_secao",
        description="ID da seção que a informação está localizada",
        type="string"),
    AttributeInfo(
        name="titulo_secao",
        description="O título da seção",
        type="string"),
    AttributeInfo(
        name="numero_item",
        description="Corresponde a seção do documento seção",
        type="string"),
    AttributeInfo(
        name="numero_tabela",
        description="Número da tabela no documento",
        type="string"),
    AttributeInfo(
        name="titulo_tabela",
        description="Título da tabela",
        type="string"),
    AttributeInfo(
        name="hora",
        description="Campo que pode ou não ter horário",
        type="string"),

]


def init_streamlit():
    st.set_page_config(layout="wide")
    st.title("SmartLux AI 💡 - Consultor de documentação V1.0")

def carregar_vectorstore():
    if os.path.exists(INDEX_PATH):
        vectorstore = Chroma(persist_directory=INDEX_PATH, embedding_function=embedding)
        return vectorstore
    else:
        print("Base vetorial não localizada")


@st.cache_resource
def carregar_llm():
    llm = ChatGoogleGenerativeAI(
        google_api_key= api_key,
        model="gemini-2.0-flash"
    )
    return llm

def main():
    init_streamlit()

    try:
        langfuse = Langfuse(
            public_key=api_public_langfuse,
            secret_key=api_secret_lanfuse,
            host="https://us.cloud.langfuse.com"
        )
        langfuse_handler = CallbackHandler()
    except Exception:
        st.error("Erro ao conectar com o Langfuse")

    try:
        llm = carregar_llm()
    except:
        st.error("Erro de conexão com o modelo de linguagem.")


    try:
        vectorstore = carregar_vectorstore()
    except:
        st.error("Erro ao carregar base vetorial")

    # Retriever
    retriever = SelfQueryRetriever.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        document_contents="Trechos dos documentos da Chesf",
        metadata_field_info=metadata_info,
        search_type="mmr"  # ou "similarity"
    )
    retriever.verbose = True

    # Prompt
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
    Você é um consultor especialista na documentação da Chesf.
    Utilize somente os documentos abaixo para responder a pergunta de forma clara e objetiva.
    Retorne o fragmento na íntegra com o conteúdo.
    Obs: ao encontrar "\n"" pular linha na resposta.
    Se a saída se referir a uma tabela, observar o conteúdo e montar uma tabela minimamente estruturada.
    Mesmo que a informação se refira a apenas um item da tabela deve-se sempre retornar a tabela inteira.

    DOCUMENTOS:
    {context}

    PERGUNTA:
    {question}

    RESPOSTA:"""
    )


    #RAG
    rag = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )


    # Interface de consulta
    st.subheader("Pergunte algo relacionado à documentação da Chesf:")
    query = st.text_input("Digite sua pergunta aqui:")

    if query:
        with st.spinner("Consultando..."):
            try:
                resultado = rag.invoke({"query": query},config={"callbacks": [langfuse_handler]})
                print(resultado)
                st.subheader("Resposta:")
                st.write(resultado["result"])

                st.markdown("---")
                st.subheader("Fontes:")
                for doc in resultado["source_documents"]:
                    st.markdown(doc.page_content[:300] + "...")
            except:
                print("Erro ao consultar o RAG")




if __name__ == "__main__":
    main()