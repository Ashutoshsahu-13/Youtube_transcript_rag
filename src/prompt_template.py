from langchain_core.prompts import PromptTemplate
from src.logger import setup_logger
logger=setup_logger()

QA_PROMPT = PromptTemplate(
    template="""
   You are a helpful assistant. Answer the question **STRICTLY using the context** below.

### CONTEXT
{context}

### RULES
- Use ONLY the information from the context.
- If the context does not include the answer, respond with:
  "I don't know based on the provided context."
- Do NOT use outside knowledge.
- Be clear and concise.

### QUESTION
{question}

### ANSWER
""",
    input_variables=["context", "question"]
)
logger.info("prompt template initialized successfully.")