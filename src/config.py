from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from dotenv import load_dotenv
import os

# # Suppress gRPC warnings (optional)
# os.environ["GRPC_VERBOSITY"] = "NONE"
# os.environ["GRPC_CPP_VERBOSITY"] = "NONE"

#load the env variable
load_dotenv()

API_KEY=os.getenv('GROQ_API_KEY')
#API_KEY1=os.getenv('GOOGLE_GEMINI')
LLM=ChatGroq(model="llama-3.1-8b-instant",api_key=API_KEY)
#EMBEDDING_MODEL= GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=API_KEY1)
EMBEDDING_MODEL = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")