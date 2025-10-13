from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY=os.getenv('GROQ_API_KEY')
LLM=ChatGroq(model="llama-3.1-8b-instant")
ans=LLM.invoke("hello")
print(ans.content)