import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma

# carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
api_secret_lanfuse = os.getenv("secret_key_langfuse")
api_public_langfuse = os.getenv("public_key_langfuse")

# embedding
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key
)

#caminho base vetorial
INDEX_PATH = "chroma_chunk_manual"

