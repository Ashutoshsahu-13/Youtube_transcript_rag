# youtube Trnascript RAG

## overview
This project implements a Retrieval-Augmented-Generation(RAG) system that allows users to ask questions about any youtube video.
The system automatically fetches the video transcript,processes it, stores embeddings in a vector database, and uses an llm to generate accurate,context-grounded answes based on the video content.

## why this project
LLMs are powerful but often hallucinate and lack context about specific videos.

This YouTube Transcript RAG solves that by:
- Extracting transcripts directly from YouTube
- Splitting them into meaningful chunks
- Storing them as embeddings in a vector database
- Retrieving only relevant chunks for each question
- Letting the LLM answer based on actual video content

## Howv it works
        User Question
              ↓
      Video Transcript Retriever
              ↓
        Chunking & Embeddings
              ↓
        Vector Database (FAISS)
              ↓
          Retriever
              ↓
      LLM + Transcript Context
              ↓
         Final Answer

## Steps

1. Input YouTube URL
The system retrieves the transcript using the YouTube API or libraries like youtube-transcript-api.

2. Preprocessing
- Clean text
- Remove timestamps
- Chunk into manageable segments
- Generate embeddings
3. Store in Vector DB
Using FAISS.
4. Ask Questions
User query is embedded → similar transcript chunks are retrieved.
5. LLM Generation
The model uses the retrieved transcript chunks to produce a grounded answer.

## Features
- Fetch transcript from any public YouTube video.
- RAG-powered Q/A grounded in real transcript content.
- Fast semantic search through transcript.
- Works with long videos (over 1 hour).
- Plug-and-play architecture for embeddings + vector DB.
- Supports multiple LLMs (OpenAI, Llama3, Mistral, etc.).

## Tech Stack

- Python

- youtube-transcript-api

- LangChain 

- Vector DB: FAISS

- LLM: GROQ

- Embeddings: Cohere api

## Use Cases

- Video summarization

- Educational content Q/A

- Podcast analysis

- Research & learning

- Turning YouTube lectures into chatbots

- Customer support training from video tutorials
