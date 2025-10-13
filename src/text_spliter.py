from langchain.text_splitter import RecursiveCharacterTextSplitter
from logger import setup_logger
logger=setup_logger()

def text_split(transcript:str,chunk_size=1000,chunk_overlap=200):
    logger.info("split the text into chunks ")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.create_documents([transcript])
    return chunks