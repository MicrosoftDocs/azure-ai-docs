---
title: "Tutorial: Build a RAG application"
titleSuffix: Foundry Local
description: Build a retrieval-augmented generation (RAG) application that answers questions about a document collection using on-device embedding and chat models with the Foundry Local SDK.
ms.service: microsoft-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: tutorial
ms.author: nakersha
ms.reviewer: samkemp
ms.date: 04/24/2026
author: natke
reviewer: samuel100
ai-usage: ai-assisted
# CustomerIntent: As a developer, I want to build a RAG application so that I can answer questions about my documents locally without sending data to the cloud.
---

# Tutorial: Build a RAG application

Build a retrieval-augmented generation (RAG) application that answers questions about a collection of documents entirely on your device. RAG combines embedding-based search with a chat model so that answers are grounded in your own data rather than relying solely on the model's training knowledge.

In this tutorial, you learn how to:

> [!div class="checklist"]
> * Set up a project and install the Foundry Local SDK
> * Create a knowledge base of text documents
> * Generate embeddings for the documents
> * Search for relevant documents by similarity
> * Generate answers grounded in retrieved context
> * Clean up resources

## Prerequisites

- A Windows, macOS, or Linux computer with at least 8 GB of RAM.
- [Python 3.11](https://www.python.org/downloads/) or later installed.

## Install packages

[!INCLUDE [Python project setup](../includes/python-project-setup.md)]

## Create a knowledge base

A RAG application needs a collection of documents to search. Define a list of text strings that serve as the knowledge base. In a production application, the list could be paragraphs from files, database records, or any other text source.

Create a file called `main.py` and add the following code:

```python
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

# Knowledge base — each string represents a document
documents = [
    "Foundry Local runs AI models directly on your device without cloud connectivity.",
    "The Foundry Local SDK supports Python, C#, JavaScript, and Rust.",
    "Embedding models convert text into numerical vectors for similarity search.",
    "Foundry Local uses ONNX Runtime for efficient model inference on CPUs and GPUs.",
    "The model catalog provides pre-optimized models that you can download and run locally.",
    "Retrieval-augmented generation grounds model responses in your own data.",
    "Vector similarity search finds documents that are semantically close to a query.",
    "Chat completions generate natural language responses from a prompt and context.",
]
```

## Generate document embeddings

Initialize the SDK, load an embedding model, and convert each document into a numerical vector. These vectors represent the semantic meaning of each document and enable similarity search.

Add the following code to `main.py`:

```python
def main():
    # Initialize the SDK
    config = Configuration(app_name="foundry_local_rag")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Load the embedding model
    embedding_model = manager.catalog.get_model("qwen3-embedding-0.6b")
    embedding_model.download(
        lambda p: print(f"\rDownloading embedding model: {p:.1f}%", end="", flush=True)
    )
    print()
    embedding_model.load()
    embedding_client = embedding_model.get_embedding_client()

    # Embed all documents in a single batch call
    response = embedding_client.generate_embeddings(documents)
    doc_embeddings = [item.embedding for item in response.data]
    print(f"Indexed {len(doc_embeddings)} documents.")
```

The `generate_embeddings` method accepts a list of strings and returns one vector per input. Each vector captures the semantic meaning of the text, so similar documents produce vectors that are close together in the embedding space.

## Search for relevant documents

To find documents that relate to a query, compare the query's embedding against every document embedding using cosine similarity. Cosine similarity measures how close two vectors are in direction, regardless of magnitude. Values near 1.0 indicate high similarity.

Add the following helper functions above `main()` in `main.py`:

```python
def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def find_relevant(query_embedding, doc_embeddings, top_k=2):
    """Return the indices and scores of the top-k most similar documents."""
    scores = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scores.append((i, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
```

The `find_relevant` function ranks all documents by similarity and returns the top matches. This approach works well for small collections. For larger datasets, consider a dedicated vector database.

## Generate grounded answers

Load a chat model and combine the retrieved documents with the user's question in a system prompt. The chat model uses the provided context to generate an answer that is grounded in your documents.

Add the following code to the `main()` function, after the embedding section:

```python
    # Load the chat model
    chat_model = manager.catalog.get_model("qwen2.5-0.5b")
    chat_model.download(
        lambda p: print(f"\rDownloading chat model: {p:.1f}%", end="", flush=True)
    )
    print()
    chat_model.load()
    chat_client = chat_model.get_chat_client()

    print("\nModels loaded. Ready for questions.")
    print("\nThe knowledge base contains information about:")
    print("  - Foundry Local features and architecture")
    print("  - Supported programming languages")
    print("  - Embedding models and vector search")
    print("  - ONNX Runtime inference")
    print("  - The model catalog")
    print("  - RAG and chat completions")
    print("\nExample questions:")
    print('  "What programming languages does the SDK support?"')
    print('  "How does Foundry Local run models?"')
    print('  "What is retrieval-augmented generation?"')
    print('\nType "quit" to exit.\n')

    # Interactive query loop
    while True:
        query = input("Question: ").strip()
        if not query or query.lower() == "quit":
            break

        # Embed the query
        query_response = embedding_client.generate_embedding(query)
        query_embedding = query_response.data[0].embedding

        # Retrieve the most relevant documents
        results = find_relevant(query_embedding, doc_embeddings, top_k=2)
        context = "\n".join(f"- {documents[i]}" for i, _ in results)

        # Build the prompt with retrieved context
        messages = [
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the provided context. "
                    "If the context doesn't contain enough information, say so.\n\n"
                    f"Context:\n{context}"
                ),
            },
            {"role": "user", "content": query},
        ]

        # Stream the response
        print("Answer: ", end="", flush=True)
        for chunk in chat_client.complete_streaming_chat(messages):
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
        print("\n")

    # Clean up
    embedding_model.unload()
    chat_model.unload()
    print("Models unloaded. Done!")


if __name__ == "__main__":
    main()
```

The system prompt instructs the model to answer using only the retrieved context. The system prompt keeps responses grounded in your documents and reduces incorrect answers. The streaming output prints each token as it is generated, making the response feel interactive.

## Complete code

Here is the full application that combines all the steps:

```python
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

# Knowledge base
documents = [
    "Foundry Local runs AI models directly on your device without cloud connectivity.",
    "The Foundry Local SDK supports Python, C#, JavaScript, and Rust.",
    "Embedding models convert text into numerical vectors for similarity search.",
    "Foundry Local uses ONNX Runtime for efficient model inference on CPUs and GPUs.",
    "The model catalog provides pre-optimized models that you can download and run locally.",
    "Retrieval-augmented generation grounds model responses in your own data.",
    "Vector similarity search finds documents that are semantically close to a query.",
    "Chat completions generate natural language responses from a prompt and context.",
]


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def find_relevant(query_embedding, doc_embeddings, top_k=2):
    """Return the indices and scores of the top-k most similar documents."""
    scores = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scores.append((i, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


def main():
    # Initialize the SDK
    config = Configuration(app_name="foundry_local_rag")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Load the embedding model
    embedding_model = manager.catalog.get_model("qwen3-embedding-0.6b")
    embedding_model.download(
        lambda p: print(f"\rDownloading embedding model: {p:.1f}%", end="", flush=True)
    )
    print()
    embedding_model.load()
    embedding_client = embedding_model.get_embedding_client()

    # Embed all documents
    response = embedding_client.generate_embeddings(documents)
    doc_embeddings = [item.embedding for item in response.data]
    print(f"Indexed {len(doc_embeddings)} documents.")

    # Load the chat model
    chat_model = manager.catalog.get_model("qwen2.5-0.5b")
    chat_model.download(
        lambda p: print(f"\rDownloading chat model: {p:.1f}%", end="", flush=True)
    )
    print()
    chat_model.load()
    chat_client = chat_model.get_chat_client()

    print("\nModels loaded. Ready for questions.")
    print("\nThe knowledge base contains information about:")
    print("  - Foundry Local features and architecture")
    print("  - Supported programming languages")
    print("  - Embedding models and vector search")
    print("  - ONNX Runtime inference")
    print("  - The model catalog")
    print("  - RAG and chat completions")
    print("\nExample questions:")
    print('  "What programming languages does the SDK support?"')
    print('  "How does Foundry Local run models?"')
    print('  "What is retrieval-augmented generation?"')
    print('\nType "quit" to exit.\n')

    # Interactive query loop
    while True:
        query = input("Question: ").strip()
        if not query or query.lower() == "quit":
            break

        # Embed the query
        query_response = embedding_client.generate_embedding(query)
        query_embedding = query_response.data[0].embedding

        # Retrieve the most relevant documents
        results = find_relevant(query_embedding, doc_embeddings, top_k=2)
        context = "\n".join(f"- {documents[i]}" for i, _ in results)

        # Build the prompt with retrieved context
        messages = [
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the provided context. "
                    "If the context doesn't contain enough information, say so.\n\n"
                    f"Context:\n{context}"
                ),
            },
            {"role": "user", "content": query},
        ]

        # Stream the response
        print("Answer: ", end="", flush=True)
        for chunk in chat_client.complete_streaming_chat(messages):
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
        print("\n")

    # Clean up
    embedding_model.unload()
    chat_model.unload()
    print("Models unloaded. Done!")


if __name__ == "__main__":
    main()
```

Run the application:

```bash
python main.py
```

You see output similar to:

```
Downloading embedding model: 100.0%
Indexed 8 documents.
Downloading chat model: 100.0%

Models loaded. Ready for questions.

The knowledge base contains information about:
  - Foundry Local features and architecture
  - Supported programming languages
  - Embedding models and vector search
  - ONNX Runtime inference
  - The model catalog
  - RAG and chat completions

Example questions:
  "What programming languages does the SDK support?"
  "How does Foundry Local run models?"
  "What is retrieval-augmented generation?"

Type "quit" to exit.

Question: What programming languages does the SDK support?
Answer: The Foundry Local SDK supports Python, C#, JavaScript, and Rust.

Question: quit
Models unloaded. Done!
```

## Clean up resources

The model weights remain in your local cache after you unload a model. The next time you run the application, the download step is skipped and the models load faster. No extra cleanup is needed unless you want to reclaim disk space.

## Related content

- [Generate text embeddings with Foundry Local](../how-to/how-to-generate-embeddings.md)
- [Tutorial: Build a multi-turn chat assistant](tutorial-build-chat-assistant.md)
- [Use native chat completions API with Foundry Local](../how-to/how-to-use-native-chat-completions.md)
- [Foundry Local SDK reference](../reference/reference-sdk-current.md)
