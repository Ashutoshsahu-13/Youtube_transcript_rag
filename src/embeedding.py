import time
from langchain_community.vectorstores import FAISS
from logger import setup_logger
logger=setup_logger()

def embedding_store(chunks, embeddings,batch_size=10):
    vector_store = None
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        try:
            if vector_store is None:
                vector_store = FAISS.from_documents(batch, embeddings)
            else:
                vector_store.add_documents(batch)
        except Exception as e:
            logger.error(f"Error embedding batch {i}-{i+batch_size}: {e}")
            time.sleep(5)  # wait a bit and retry
    return vector_store

