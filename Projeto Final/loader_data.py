
import json
from pathlib import Path
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import *


arquivos = [
    "documentos/chunk-manual-4.json"   #trocar para arquivo.json
]

def update_vectorstore(list_arquivos):
    """Recebe um ou vários documentos e atualiza a base de dados"""
    documentos = []

    for caminho in list_arquivos:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))

        for item in dados:
            texto = item.get("texto", "")
            metadados = {k: v for k, v in item.items() if k != "texto"}
            documentos.append(Document(page_content=texto, metadata=metadados))

    # Dividir documentos
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_divididos = splitter.split_documents(documentos)

    vectorstore = Chroma(
        embedding_function=embedding,
        persist_directory=INDEX_PATH
    )
    vectorstore.add_documents(docs_divididos)
    vectorstore.persist()
    print(f"Total de documentos na base: {len(vectorstore._collection.get()['documents'])}")


def carregar_vectorstore():
    """Cria uma base vetorial e povoa com chunks de vários documentos"""
    documentos = []

    for caminho in arquivos:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))

        # Converter para objetos Document
        for item in dados:
            texto = item.get("texto", "")
            metadados = {k: v for k, v in item.items() if k != "texto"}
            documentos.append(Document(page_content=texto, metadata=metadados))

    # Dividir documentos
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_divididos = splitter.split_documents(documentos)

    # Criar BD e salvar
    vectorstore = Chroma.from_documents(
        docs_divididos,
        embedding=embedding,
        persist_directory=INDEX_PATH
    )
    vectorstore.persist()
    print(f"Total de documentos na base: {len(vectorstore._collection.get()['documents'])}")

    return vectorstore

def main():
    carregar_vectorstore()
    #update_vectorstore(["documentos/arquivo.json"]) tirar o comentário caso queira testar update de documentos


if __name__ == "__main__":
    main()