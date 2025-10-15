from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from src.logger import setup_logger

logger=setup_logger()
parser = StrOutputParser()

def format_docs(retrieved_docs):
  """Combine retrieved document texts into a single context string."""
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

def retriver(vector_store,prompt,llm):
    """
    Create a retriever and chain that combines retrieval, prompt templating, and LLM querying.
    
    Args:
        vector_store (FAISS): The vector store used for similarity search.
        prompt (PromptTemplate): LangChain prompt template for Q&A.
        llm: The language model to generate the answer.

    Returns:
        RunnableSequence: The complete retrieval → prompt → LLM → parse pipeline.
    """
    if vector_store is None:
        logger.error(" Vector store is None — cannot initialize retriever.")
        return None
    try:
      logger.info("🔍 Initializing retriever with FAISS vector store...")
      retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
      logger.debug(" Retriever initialized successfully.")
      parallel_chain = RunnableParallel({
      'context': retriever | RunnableLambda(format_docs),
      'question': RunnablePassthrough()
      })
      chain= parallel_chain | prompt | llm | parser 
      logger.info(" Retrieval + LLM chain successfully constructed.")
      return chain
    except Exception as e:
      logger.exception(f"Failed to create retriever chain: {e}")