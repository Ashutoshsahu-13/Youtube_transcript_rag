from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()

def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

def retriver(vector_store,prompt,llm):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
    })
    return  parallel_chain | prompt | llm | parser 