from data_ingestion import fetch_transcript
from text_spliter import text_split
from embeedding import embedding_store
from retriver import retriver
from prompt_template import QA_PROMPT
from config import EMBEDDING_MODEL,LLM
from logger import setup_logger
logger=setup_logger()
def main():
    video_id="BMym71Dwox0"
    
    transcript=fetch_transcript(video_id)
    
    chunks=text_split(transcript)
    
    vector_store=embedding_store(chunks,EMBEDDING_MODEL)
    
    model=retriver(vector_store,QA_PROMPT,LLM)
    
    question="Check if the video discusses 'Serializers' and explain."
    ans=model.invoke(question)
    print(ans)

if __name__ =="__main__":
    main()
    
    
    