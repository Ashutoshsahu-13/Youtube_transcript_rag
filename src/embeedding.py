import time
import os
from langchain_community.vectorstores import FAISS
from src.logger import setup_logger

logger=setup_logger()

def embedding_store(chunks, embeddings,batch_size=10,save_path="faiss_indexes", video_id=None):
    """
    Creates and updates a FAISS vector store from text chunks using the given embedding model.
    
    Args:
        chunks (List[Document]): List of LangChain Document chunks to embed.
        embeddings: Embedding model (e.g., GoogleGenerativeAIEmbeddings).
        batch_size (int): Number of chunks to process per batch.
        retry_delay (int): Delay in seconds before retrying after a failed batch.

    Returns:
        FAISS: The populated FAISS vector store, or None if embedding failed.
    """
    if not chunks:
        logger.warning(" No chunks provided for embedding. Skipping FAISS creation.")
        return None
    
    os.makedirs(save_path, exist_ok=True)
    # Check if already saved
    if video_id and os.path.exists(os.path.join(save_path, video_id + ".faiss")):
        logger.info(f"Loading existing FAISS index for video {video_id}")
        return FAISS.load_local(
        folder_path=save_path,
        embeddings=embeddings,
        index_name=video_id,
        allow_dangerous_deserialization=True  # ✅ opt-in for trusted local files
        )
    logger.info(f"Starting embedding process for {len(chunks)} chunks (batch_size={batch_size})")
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
    if vector_store and video_id:
        vector_store.save_local(save_path, video_id)
        logger.info(f"Saved FAISS index for video {video_id} to disk")
    return vector_store

