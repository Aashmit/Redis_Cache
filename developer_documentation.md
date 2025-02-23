
# Developer Documentation for MyProject

## Introduction
This document provides a comprehensive overview and detailed documentation for the code files in the MyProject project, focusing on functionality related to caching, vectorization, and language model interactions with GitHub repositories.

## Table of Contents
- [cache_vectorizer.py](#cache_vectorizer-py)
- [test.py](#test-py)

## File Documentation

### cache_vectorizer.py
#### Overview
#### Overview:

The `cache_vectorizer.py` file contains a class-like module named `create_vectorizer()` that serves as a custom vectorizer for text data, utilizing the capabilities of `OllamaEmbeddings` and `redisvl.utils.vectorize.CustomTextVectorizer`. This module is designed to provide asynchronous and synchronous text embedding functions, enabling efficient vectorization of large datasets.

#### Details
#### Details:

##### 1. Importing Required Libraries
- The file imports necessary libraries such as `OllamaEmbeddings` from the `langchain_ollama` package, `CustomTextVectorizer` from `redisvl.utils.vectorize`, and `asyncio`.
- It also includes type hints for function parameters and return types using `typing`.

##### 2. Function: create_vectorizer()
The central function in this module is `create_vectorizer()`. This function initializes the primary components required for text vectorization:

- **OllamaEmbeddings**: An instance of `OllamaEmbeddings` model is created with the specified model name 'nomic-embed-text'. The Ollama embeddings are a type of dense representation used to encode text data into high-dimensional vectors.

##### 3. Synchronous Embedding Functions
- **sync_embed(text: str) -> List[float]**: This function accepts a single string (text) as input and returns the corresponding vectorized embedding using `OllamaEmbeddings`.

- **sync_embed_many(texts: List[str]) -> List[List[float]]**: This function takes a list of strings (texts) as input and returns an array of lists, where each inner list contains the vectorized embeddings for the corresponding text in the input list.

##### 4. Asynchronous Embedding Wrappers
- **async_embed(text: str) -> List[float]**: This async wrapper function converts a synchronous call to `sync_embed` into an asynchronous one, leveraging Python's `asyncio`. It runs the synchronous method in a separate thread using `asyncio.to_thread()` and returns the vectorized embedding as a list of floats.

- **async_embed_many(texts: List[str]) -> List[List[float]]**: Similar to the above, but it accepts multiple strings (texts) instead of just one. It converts the synchronous call to `sync_embed_many` into an asynchronous operation and returns the resulting array of lists containing vectorized embeddings.

##### 5. CustomTextVectorizer Configuration
- Upon defining the required embedding functions, `create_vectorizer()` constructs a `CustomTextVectorizer` object with customizable embedders:
  - The synchronous embedding is set to `sync_embed`.
  - The asynchronous single-text embedding is set to `async_embed`.
  - Batch asynchronous text embedding is configured for multiple texts using `sync_embed_many`.
  - The asynchronous many-to-one embedding, which accepts a list of texts and returns a list of individual embeddings, utilizes `async_embed_many` as the underlying function.

##### 6. Singleton Instance Creation
Finally, this singleton instance of `CustomTextVectorizer` is returned from `create_vectorizer()` to ensure only one vectorizer is in use across an application, facilitating consistent and efficient text embedding processes throughout the code base.



### test.py
#### Overview
#### Overview of test.py

The `test.py` file is a Python script that serves as an interactive unit test for integrating the Ollama chat model with a cache system using Redis and vectorization. The primary objective of this code is to demonstrate how to leverage caching to improve response times when interacting with the Ollama LLM (Language Learning Model).

#### Details
#### Details

##### Import Statements
The script begins by importing necessary packages: `time`, `ChatOllama` from `langchain_ollama`, `SemanticCache` from `redisvl.extensions.llmcache`, `vectorizer` from `cache_vectorizer`, and environment variables handling using the `dotenv` package.

##### Loading Environment Variables
The script loads environment variables for Redis connection details using `load_dotenv()` and `os.getenv()`.

##### Cache Initialization
The code attempts to initialize a `SemanticCache` instance, which acts as an in-memory cache for storing responses alongside their corresponding prompts. If successful, the prompt vectorization is registered with this cache. Otherwise, it prints an error message and exits the program due to an unsuccessful initialization of the cache.

##### Question Input
The script prompts the user to enter a question via `input()`.

##### ChatOllama Client
An instance of `ChatOllama` from `langchain_ollama` is created, using the "llama3.2" model and verbose output.

##### ask_ollama Function
This function calls the client's `invoke()` method to generate a response for a given question:
    - It takes the user-provided question as an argument (`str`, named `question`).
    - The function returns the content of the response generated by Ollama, i.e., `client.invoke(input=question).content`.

##### Caching Mechanism
The script then measures time taken for a cache check and retrieval using the `SemanticCache` instance:
   - It records the start time (`start_time = time.time()`) before calling the cache's `check()` method with the prompt derived from the user-input question.
   - After caching, it prints the retrieved cached response details (prompt, response) alongside the elapsed time for retrieval.

##### LLM Operations If No Cache Hit
If no matching cached response is found, the script proceeds to generate an Ollama-based response and stores it in the cache:
    - It measures the time taken (`start_time = time.time()`) before calling `ask_ollama(question)` to fetch a response from the chat model.
    - The script then prints the user question, generated response, and elapsed time for LLM operations.
    - Finally, it stores both the prompt and response in the cache using `llmcache.store()`.

##### Error Handling
If any exceptions occur during either the LLM operations or while storing the response in the cache, the script prints an error message corresponding to those issues.

In summary, this code illustrates a practical use-case of integrating caching with Ollama for optimizing responses by leveraging Redis and vectorization for faster data retrieval and storage.

