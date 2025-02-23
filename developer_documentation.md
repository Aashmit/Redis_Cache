
# Developer Documentation 

## Introduction
This document provides a comprehensive overview and detailed documentation for the code files in this project.

## Table of Contents
- [cache_vectorizer.py](#cache_vectorizer-py)
- [test.py](#test-py)

## File Documentation

### cache_vectorizer.py
#### Overview
#### Overview

This Python file, `cache_vectorizer.py`, implements a custom text vectorization class named `CustomTextVectorizer`. The purpose of this class is to provide asynchronous (async) and synchronous (sync) methods for embedding text data using the OllamaEmbeddings model from the langchain\_ollama library. This is achieved through the use of asyncio for asynchronous operations and threading for synchronous operations, ensuring that the vectorization process remains efficient even when dealing with large datasets or high concurrency.

#### Details
#### Details

1. **Imports**
   - The file imports necessary modules:
     - `OllamaEmbeddings` from `langchain_ollama`: This module contains an Ollama model (presumably 'nomic-embed-text') for text embedding tasks.
     - `CustomTextVectorizer` from `redisvl.utils.vectorize`: This is a custom vectorization class that will be adapted to support asynchronous and synchronous operations.
     - `asyncio`: Python's built-in library for writing single-threaded concurrent code using coroutines, multiplexing I/O access over sockets and other resources.
     - `typing.List` from the Python standard library: Used for type annotations indicating that the functions return lists of floats.

2. **Function: `create_vectorizer()`**
   - This function initializes OllamaEmbeddings with a specified model ('nomic-embed-text').
   - It then defines three embedding methods, one each for synchronous operations on single text inputs (`sync_embed`), multiple text inputs (`sync_embed_many`), and asynchronous operations on single texts (`async_embed`) and batches of texts (`async_embed_many`).
     - `sync_embed` and `sync_embed_many` use the underlying OllamaEmbeddings methods to directly generate embedded vectors for input strings.
     - The asynchronous wrappers, `async_embed` and `async_embed_many`, employ asyncio's `to_thread` function to wrap their respective synchronous methods in separate threads, thereby enabling them to run concurrently with other tasks.
   - Finally, the function returns a `CustomTextVectorizer` instance configured with these embedding functions for both synchronous and asynchronous use cases.

3. **Singleton Instance**
   - The `create_vectorizer()` function is called once when the module is imported or executed, creating a single instance of the `CustomTextVectorizer`. This ensures that only one vectorization object exists within the application context, avoiding potential memory leaks and simplifying management.

The class `CustomTextVectorizer` created by this method provides flexibility in using text embedding either synchronously (single-threaded) or asynchronously (multiple-core utilization), which is valuable for optimizing performance when dealing with large amounts of text data or high concurrency requirements.



### test.py
#### Overview
#### Overview

The `test.py` file is a Python script designed for testing and demonstrating the functionality of a conversational AI model, specifically using ChatOllama (an API client for OpenAI's ChatGLM) and Semantic Cache for optimizing subsequent interactions. This script is intended to serve as a user interface where users can input questions, receive responses from the model, measure time taken for both cache hits and miss scenarios, and observe caching behavior.

#### Details
#### Details

**1. Import Statements:**
   - `time`: For measuring execution times of operations.
   - `langchain_ollama` (imported as `ChatOllama`): A client facilitating interaction with the ChatGLM API.
   - `redisvl.extensions.llmcache` (imported as `SemanticCache`): A cache implementation using Redis to store model responses, thereby reducing redundant computations and speeding up subsequent interactions by returning cached results if available.
   - `cache_vectorizer`: Not explicitly documented in this file but presumably a vectorization component for transforming text into numerical vectors before caching or processing with the LLM.
   - `os` and `dotenv`: For environment variable handling, particularly to obtain the Redis URL from an `.env` file.

**2. Environment Setup:**
   - `.load_dotenv()` initializes Dotenv library, which reads environment variables from a .env file.
   - `redis_url = os.getenv('REDIS_URL')`: Retrieves the Redis connection string from the `.env` file using `os.getenv`.

**3. Semantic Cache Initialization:**
   - The cache is initialized with key details including its name, base Redis URL, distance threshold (0.1 in this case), and a vectorizer object for transforming text inputs into vectors. Connection parameters such as encoding, timeout settings, and retry behavior are also configured.

**4. Main Functionality:**
   - The script prompts the user to enter their question via `input("Enter your question:")`.
   - It creates an instance of `ChatOllama` client with the model "llama3.2" set to verbose mode for detailed responses.

**5. `ask_ollama(question: str) -> str` Function:**
   - This is a simple wrapper that invokes ChatOllama's API, passing the user input as a parameter and returns its response content.

**6. Cache Check & Execution:**
   - The script measures time taken for the cache check by calling `time.time()` before and after `llmcache.check(prompt=question)`. If the result is not None (indicating the query was found in the cache), it prints the prompt, response from the cache along with the time taken to retrieve this data.
   - For a non-cached case (LLM generated response), the script first measures time for invoking `ask_ollama` and stores the returned result in the SemanticCache with the same key as the user's query. It then prints the prompt, original response from ChatOllama, new LLM-generated response, and the total time taken to generate this response.

**7. Error Handling:**
   - Any exceptions during the execution of `ask_ollama` or cache storage are caught and printed as error messages. This ensures robustness against potential issues in interacting with the ChatGLM API or managing Redis connections.

In summary, `test.py` is a script that tests caching mechanisms using Semantic Cache in conjunction with ChatOllama for faster access to conversational responses. It captures user input, compares it against cached results or prompts LLM if necessary, and records the performance metrics of both cache hits and misses.

