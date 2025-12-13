from langchain_core.prompts import PromptTemplate
from src.logger import setup_logger
logger=setup_logger()

QA_PROMPT = PromptTemplate(
    template="""
   You are an expert AI assistant answering questions about YouTube video content.

### CONTEXT
{context}

### INSTRUCTIONS
- Use the transcript as the primary source of truth.
- Convert spoken language into clear, well-written explanations.
- Silently correct transcription errors, grammar issues, and misheard terms.
- If the speaker’s explanation is unclear, clarify it in simple terms **without changing the meaning**.
- Do NOT introduce topics or facts that are unrelated to the transcript.
- If the answer is not present or cannot be inferred from the transcript, respond with:
  "I don't know based on the provided context."

### QUESTION
{question}

### ANSWER
""",
    input_variables=["context", "question"]
)
logger.info("prompt template initialized successfully.")