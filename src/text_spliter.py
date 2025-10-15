from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.logger import setup_logger
from typing import List
logger=setup_logger()

def text_split(transcript:str,chunk_size=1000,chunk_overlap=200)->List[Document]:
    """
    Splits a transcript string into smaller text chunks for embedding or processing.
    
    Args:
        transcript (str): The full transcript text.
        chunk_size (int): Maximum size of each text chunk.
        chunk_overlap (int): Number of overlapping characters between chunks.

    Returns:
        List[Document]: A list of LangChain Document objects representing text chunks.
    """
    logger.info("split the text into chunks ")
    # Validate input
    if not transcript or not transcript.strip():
        logger.warning(" Empty or invalid transcript provided. No chunks created.")
        return []
    
    
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
            )
        chunks = splitter.create_documents([transcript])
        logger.info(f"Successfully split transcript into {len(chunks)} chunks ")
        return chunks
    except Exception as e:
        logger.exception(f"Error splitting transcript into chunks: {e}")
        return []