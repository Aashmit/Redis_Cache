import time
from langchain_ollama import ChatOllama
from redisvl.extensions.llmcache import SemanticCache
from cache_vectorizer import vectorizer
import os
from dotenv import load_dotenv

load_dotenv()
redis_url = os.getenv('REDIS_URL')
# Initialize Semantic Cache

try:
    llmcache = SemanticCache(
        name="OllamaLLMCache",
        redis_url="redis://localhost:6379",
        distance_threshold=0.1,
        vectorizer=vectorizer,
        connection_kwargs={
            'decode_responses': True,
            'socket_timeout': 5,
            'retry_on_timeout': True
        },
        dimension=768
    )
except Exception as e:
    print(f"Error initializing SemanticCache: {e}")
    exit(1)

question = input("Enter your question:")

client = ChatOllama(model="llama3.2",verbose=True)

def ask_ollama(question: str) -> str:
    response = client.invoke(input=question)
    return response.content

# Measure time for cache check
start_time = time.time()
cached_response = llmcache.check(prompt=question)
cache_time = time.time() - start_time

if cached_response:
    print("Returned from cache")
    print("Prompt:", cached_response[0]['prompt'])
    print("Response:", cached_response[0]['response'])
    print(f"Time taken for cache retrieval: {cache_time:.4f} seconds")
else:
    try:
        start_time = time.time()
        response = ask_ollama(question)
        llm_time = time.time() - start_time
        print("No response in cache. LLM generated response.")
        print("Prompt:", question)
        print("Response:", response)
        print(f"Time taken for LLM response: {llm_time:.4f} seconds")
        
        # Store the response in cache
        llmcache.store(prompt=question, response=response)
        print("Stored in cache successfully.")
    except Exception as e:
        print(f"Error during LLM operations: {e}")
