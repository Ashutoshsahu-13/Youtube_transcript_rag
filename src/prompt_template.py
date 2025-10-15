from langchain_core.prompts import PromptTemplate
from src.logger import setup_logger
logger=setup_logger()
QA_PROMPT = PromptTemplate(
    template="""
    You are a helpful assistant.
    Answer ONLY from the provided transcript context.
    If the context is insufficient, just say you don't know.

    {context}
    Question: {question}
    """,
    input_variables=['context', 'question']
)
logger.info("prompt template initialized successfully.")