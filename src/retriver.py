from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever
from src.logger import setup_logger

logger=setup_logger()
parser = StrOutputParser()
compressor=FlashrankRerank()

def format_docs(retrieved_docs):
  """Combine retrieved document texts into a single context string."""
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

def pre_retrieval(llm):
  
   rewrite_prompt = PromptTemplate.from_template("""
        You are an assistant that rewrites user queries to be more clear, concise,
        and optimized for document retrieval.

        Original query: {query}
        Rewritten query:
        """)
   rewrite_chain = rewrite_prompt | llm | StrOutputParser()
   return rewrite_chain


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
      logger.info(" Initializing retriever with FAISS vector store...")
      retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 20})
      logger.debug(" Retriever initialized successfully.")
      rewrite_query=pre_retrieval(llm)
      compressor_retrieval=ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
      parallel_chain = RunnableParallel({
      'context': compressor_retrieval | RunnableLambda(format_docs),
      'question': RunnablePassthrough()
      })
      chain= rewrite_query | parallel_chain | prompt | llm | parser 
      logger.info(" Retrieval + LLM chain successfully constructed.")
      return chain
    except Exception as e:
      logger.exception(f"Failed to create retriever chain: {e}")