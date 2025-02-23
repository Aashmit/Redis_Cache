
# Developer Documentation 

## Introduction
This document provides a comprehensive overview and detailed documentation for the code files in this project.

## Table of Contents
- [cache_vectorizer.py](#cache_vectorizer-py)
- [test.py](#test-py)

## File Documentation

### cache_vectorizer.py
#### Overview
#### Overview:
This Python file, `cache_vectorizer.py`, defines a custom vectorization utility for efficient text embedding using the OllamaEmbeddings model from the `langchain_ollama` library and Redis's vectorization capabilities through `redisvl.utils.vectorize`. The primary purpose of this code is to provide synchronous and asynchronous methods for single-text and batch text embeddings, enabling high-performance text representation in a cacheable manner.

#### Details
#### Details:

**1. Importing Necessary Libraries:**
   - `OllamaEmbeddings`: A model from the `langchain_ollama` library, specifically designed for text embeddings using the 'nomic-embed-text' pre-trained model.
   - `CustomTextVectorizer` and `asyncio`: From `redisvl.utils.vectorize`, which facilitates vectorization with Redis's capabilities.

**2. Function: `create_vectorizer()`**
    - Initializes OllamaEmbeddings with the 'nomic-embed-text' model, ensuring that text embeddings are produced efficiently and accurately.
    - Defines three synchronous embedding functions (`sync_embed`, `sync_embed_many`):
        * `sync_embed`: Takes a single string of text as input and returns its corresponding vectorized representation (List[float]).
        * `sync_embed_many`: Accepts a list of strings, each representing a piece of text, and outputs the combined vectors for all inputs in List[List[float]].
    - Creates asynchronous wrappers (`async_embed`, `async_embed_many`) to achieve vectorization in an event-driven manner. These wrappers leverage `asyncio.to_thread` to execute their respective synchronous methods on a separate thread, ensuring non-blocking behavior and scalability.
    - Configures and returns a custom `CustomTextVectorizer` object with the following properties:
        * `embed`: Points to the `sync_embed` function for single-text embeddings.
        * `aembed`: Points to the `async_embed` asynchronous wrapper for single-text embedding.
        * `embed_many`: Points to the `sync_embed_many` function for batch text embeddings.
        * `aembed_many`: Points to the `async_embed_many` asynchronous wrapper for batch text embedding.

**3. Singleton Instance:**
   - By calling `create_vectorizer()` and assigning its returned value to `vectorizer`, a singleton instance of this custom vectorization utility is created, ensuring a single global object with these methods.

This code is intended to be part of a larger system that employs efficient text representation for tasks like semantic search or clustering within a caching environment, leveraging Redis's capabilities for high-speed vector operations.



### test.py
#### Overview
#### Overview

**test.py** is a Python script that demonstrates the use of several libraries to interact with a language model, specifically ChatOllama, and a cache system based on SemanticCache for optimizing subsequent queries. The primary goal is to compare the time taken between retrieving responses directly from the LLM (Language Learning Model) and using cached data.

#### Details
#### Details

##### Libraries Imported

- `time`: Used to measure elapsed time in both the cache check and LLM operations.
  
- `langchain_ollama` (imported as `ChatOllama`): This library provides an interface for interacting with ChatOllama, a large language model. It allows users to invoke the model with specific prompts and retrieves the generated responses as text.

- `redisvl.extensions.llmcache` (imported as `SemanticCache`): The Semantic Cache is a caching solution that leverages Redis as its backend for storing and retrieving key-value pairs. In this script, it stores and manages cached responses to questions, reducing redundant computations with similar inputs by leveraging previously generated outputs.

- `vectorizer`: This class from the `cache_vectorizer` package is utilized in initializing the SemanticCache, as it provides a method for converting textual input into vector representations that can be used for similarity or retrieval purposes within Redis.

- `os`, `dotenv`: For environment handling and accessing the REDIS_URL from environment variables (which contains the connection string to the Redis database).

##### Key Functions/Methods

1. **`load_dotenv()`**: This function loads the `.env` file's environment variables into the process-wide variable namespace, enabling access to sensitive data such as the REDIS_URL without hardcoding it in the source code.
   
2. **Initialization of `SemanticCache`**

   - The code attempts to instantiate a cache object using `SemanticCache`. If successful, it sets up a connection string pointing to Redis running locally at port 6379 and employs specified vectorization parameters from the `vectorizer` class for generating vectors.
  
3. **Prompt Handling**: It prompts the user with "Enter your question:" to gather input as a string, which will be used as both an LLM prompt and cache key.
   
4. **`ask_ollama(question: str)`**

   - This function invokes ChatOllama's `invoke()` method using the provided question as its input. The model generates a response in text format, which is then returned.

5. **Cache Check (Time Measurement)**

   - The script initiates time measurement to gauge how long it takes for the `SemanticCache` system to find an entry for the given prompt. If cached data exists, it prints out the retrieved prompt and corresponding vector representation along with the elapsed time taken for retrieval from cache.

6. **LLM Operations (Direct Retrieval)**

   - In case the prompt is not found in the cache, the script calls `ask_ollama` as before to obtain a response from ChatOllama via the LLM directly.
  
7. **Caching Responses**
   
   - Once an LLM response has been fetched, it gets stored back into the `SemanticCache`, ensuring future queries with identical prompts will quickly return cached results instead of re-executing LLM operations.
  
8. **Error Handling**: If any exceptions occur during either cache retrieval or storing, they are caught and printed to indicate operational issues for debugging purposes.

