import asyncio
from src.data_ingestion import fetch_transcript
from src.text_spliter import text_split
from src.embeedding import embedding_store
from src.retriver import retriver
from src.prompt_template import QA_PROMPT
from src.config import EMBEDDING_MODEL,LLM
from src.logger import setup_logger
logger=setup_logger()

class pipeline:
    def __init__(self, video_id: str):
        self.video_id = video_id
        self.vector_store = None
        self.model = None
    async def prepare(self):
        """Fetch transcript, split, and prepare retriever."""
        
    
        transcript=await fetch_transcript(self.video_id)
    
        chunks=text_split(transcript)
    
        self.vector_store=embedding_store(chunks,EMBEDDING_MODEL,video_id=self.video_id)
    
        self.model=retriver(self.vector_store,QA_PROMPT,LLM)
        logger.info("Pipeline initialized successfully ")
        
    async def ask(self, question: str):
        """Ask a question using the prepared retriever."""
        if not self.model:
            raise RuntimeError("Pipeline not initialized. Call prepare() first.")
        
        logger.info(f"Asking question: {question}")
        answer = await self.model.ainvoke(question)
        return answer
    