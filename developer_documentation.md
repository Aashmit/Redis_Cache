
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

The `cache_vectorizer.py` file contains a utility class named `CustomTextVectorizer`, which is designed to efficiently handle both synchronous and asynchronous text embedding tasks using the OllamaEmbeddings model from the `langchain_ollama` library and RedisVL's vectorization functionality from `redisvl.utils.vectorize`. This class serves as an intermediary between applications and the underlying text embedding models, providing a consistent interface for vectorizing text data regardless of whether the operations are synchronous or asynchronous.

#### Details
#### Details:

1. **Imports**:
   - The file imports necessary libraries including `OllamaEmbeddings` from `langchain_ollama`, `CustomTextVectorizer` from `redisvl.utils.vectorize`, `asyncio` for handling asynchronous tasks, and types for type hinting.

2. **Function: `create_vectorizer()`**

   - Initializes an instance of `OllamaEmbeddings` using the 'nomic-embed-text' model.
   - Defines three functions:
     - `sync_embed(text: str) -> List[float]`: Embeds a single text string asynchronously and returns its embedded representation as a list of floats, leveraging OllamaEmbeddings' synchronous method `embed_query`.
     - `sync_embed_many(texts: List[str]) -> List[List[float]]`: Batch embeds multiple texts concurrently using OllamaEmbedings' synchronous method `embed_documents`, returning a list of lists where each inner list corresponds to an embedded document.
   - Creates asynchronous wrappers for the synchronous methods using `asyncio.to_thread`. The functions `async_embed(text: str) -> List[float]` and `async_embed_many(texts: List[str]) -> List[List[float]]` execute their respective synchronous counterparts on separate threads, ensuring that these tasks do not block the caller's execution.
   - Configures a `CustomTextVectorizer` object with the following embedded methods:
     - `embed=sync_embed`: Binds the synchronous single-text embedding function to the vectorizer.
     - `aembed=async_embed`: Associates the asynchronous single-text embedding function.
     - `embed_many=sync_embed_many`: Links the batch text embedding function using a synchronous thread pool executor.
     - `aembed_many=async_embed_many`: Pairs the asynchronous batch text embedding function with an asynchronous task queue.

3. **Singleton Instance**:
   - The `create_vectorizer()` function is called once and returns the `CustomTextVectorizer` instance, ensuring that only one vectorizer object exists in memory, facilitating easy reuse across different parts of a project.

By using this class, applications can efficiently perform text embedding tasks both synchronously and asynchronously while leveraging the powerful OllamaEmbeddings model for quality vector representations.



### test.py
#### Overview
#### Overview

The `test.py` file is a Python script designed for testing the integration of three external libraries: `langchain_ollama`, `redisvl.extensions.llmcache`, and `cache_vectorizer`. The primary goal of this script is to demonstrate how these components can work together to optimize the retrieval and caching of responses from a language model, specifically Llama3.2, using Redis as a backend.

#### Details
#### Details

1. **Imports**
   - `time`: To measure elapsed time.
   - `ChatOllama` from `langchain_ollama`: This is a client for the LangChain Ollama language model, which provides an API to interact with the Llama3.2 model.
   - `SemanticCache` from `redisvl.extensions.llmcache`: This is a cache class that utilizes Redis as its backend and leverages vectorization through `vectorizer`. The goal of this class is to store computed responses alongside their prompts for later retrieval, thereby reducing the need for repeated model execution when similar queries appear.
   - `vectorizer` from `cache_vectorizer`: This component is responsible for converting textual inputs into numerical representations (vectors) that can be efficiently stored and retrieved by Redis.

2. **Environment Variables**
   - The script loads environment variables via the `dotenv` package, specifically the `REDIS_URL`, which points to a local Redis instance running on port 6379. This is essential for connecting to a real-time Redis server during testing.

3. **Semantic Cache Initialization**
   - In an exceptional handling block, the script attempts to initialize the `SemanticCache` object with specific parameters:
     - Cache name: "OllamaLLMCache"
     - Redis connection URL: localhost:6379
     - Distance threshold for cache check: 0.1
     - Vectorizer instance
     - Connection settings (decode_responses, socket_timeout, retry_on_timeout) to adapt to the local Redis environment
   - If initialization fails, an error message is printed and execution ends with a non-zero exit status.

4. **User Input**
   - The script prompts the user for their question via the `input` function.

5. **ChatOllama Client Initialization**
   - A `ChatOllama` client is instantiated, utilizing Llama3.2 with verbosity enabled to provide detailed model responses.

6. **Ask Olla Function**
   - This function takes a question as input and sends it to the ChatOllama client through its `invoke` method, which in turn returns a response. The content of this response is then returned by the function.

7. **Cache Check and Response Retrieval**:
   - The script measures the time taken for a cache check using the `time` module's `time()` function before and after calling the `check()` method on an instance of `SemanticCache`. If cached data exists, it prints out the prompt and response from the cache along with the elapsed time.

8. **LLM Operations**:
   - When no cached response is found, the script executes the user's question through the ChatOllama client, capturing its output in a variable named `response`. The time taken for this operation is measured using `time.time()`.
   - In parallel with measuring LLM execution time, the script attempts to store the generated response alongside the original prompt within the `SemanticCache` instance, utilizing the `store()` method.

9. **Exception Handling**:
   - Any exceptions occurring during either LLM operations or cache insertions are caught and printed as error messages. This ensures that failures in these components do not disrupt the overall testing process.

