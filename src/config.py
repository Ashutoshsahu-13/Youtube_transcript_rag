from langchain_groq import ChatGroq
from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv
import os


#load the env variable
load_dotenv()

API_KEY=os.getenv('GROQ_API_KEY')

LLM=ChatGroq(model="llama-3.1-8b-instant",api_key=API_KEY)

EMBEDDING_MODEL = CohereEmbeddings(model="embed-english-v3.0")

