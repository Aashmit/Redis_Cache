# Redis Semantic Cache

A semantic caching system using Redis and Ollama embeddings to efficiently store and retrieve LLM responses based on semantic similarity.

## Description

This project implements a semantic cache using Redis Vector Database to store and retrieve LLM-generated responses. It uses Ollama embeddings to vectorize text, allowing for similarity-based retrieval of cached responses.

## Installation

1. Clone the repository
2. Create a Python virtual environment (recommended):
   ```
   # Option 1: Using venv (built into Python)
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   
   # Option 2: Using conda
   conda create -n redis-semantic-cache python=3.9
   conda activate redis-semantic-cache
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up Redis:
   - Make sure Docker is installed and running on your system
   - Pull the Redis Stack Docker image:
     ```
     docker pull redis/redis-stack
     ```
   - Run the Redis Stack container:
     ```
     docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
     ```
   - Verify Redis is running:
     ```
     docker ps | grep redis-stack
     ```
5. Set up Ollama:
   - Install Ollama by following the instructions at [Ollama's official website](https://ollama.ai/download)
   - Start the Ollama service:
     ```
     ollama serve
     ```
   - Pull the required models:
     ```
     # Pull the LLM model
     ollama pull llama3.2
     
     # Pull the embedding model
     ollama pull nomic-embed-text
     ```
   - Verify Ollama is running:
     ```
     curl http://localhost:11434/api/version
     ```
6. Set up environment variables:
   - Copy the example environment file to create your .env file:
     ```
     cp .env.example .env
     ```
   - The default configuration should work if you're running Redis locally with the Docker setup above

## Configuration

The `.env` file in the project root contains the following variables:

```
OLLAMA_BASE_URL=http://localhost:11434
REDIS_URL=redis://localhost:6379
```

You can modify these values if your setup differs from the default configuration.

## Usage

Run the test script to interact with the semantic cache:

```
python test.py
```

The system will:
- Prompt you for a question
- Check if a semantically similar response exists in the cache
- Return the cached response if found
- Otherwise, generate a new response using Ollama LLM and store it in the cache

## Components

- `cache_vectorizer.py`: Handles text vectorization using Ollama embeddings
- `test.py`: Demo script showing cache functionality