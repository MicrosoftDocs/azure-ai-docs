---
title: 'RAG Tutorial: Search using an LLM'
titleSuffix: Azure AI Search
description: Learn how to build queries and engineer prompts for LLM-enabled search on Azure AI Search. Queries used in generative search provide the inputs to an LLM chat engine.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: tutorial
ms.date: 09/12/2024

---

# Tutorial: Search your data using a chat model (RAG in Azure AI Search)

The defining characteristic of a RAG solution on Azure AI Search is sending queries to a Large Language Model (LLM) and providing a conversational search experience over your indexed content. It can be surprisingly easy if you implement just the basics.

In this tutorial, you:

> [!div class="checklist"]
> - Set up clients
> - Write instructions for the LLM
> - Provide a query designed for LLM inputs
> - Review results and explore next steps

This tutorial builds on the previous tutorials. It assumes you have a search index created by the [indexing pipeline](tutorial-rag-build-solution-pipeline.md).

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/). For more information, see [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

- Azure AI Search, in a region shared with Azure OpenAI.

- Azure OpenAI, with a deployment of gpt-35-turbo. For more information, see [Choose models for RAG in Azure AI Search](tutorial-rag-build-solution-models.md)

## Download the sample

You use the same notebook from the previous indexing pipeline tutorial. Scripts for querying the LLM follow the pipeline steps. If you don't already have the notebook, [download it](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Tutorial-RAG/Tutorial-rag.ipynb) from GitHub.

## Configure clients for sending queries

The RAG pattern in Azure AI Search is a synchronized connection to a search index to obtain the grounding data, followed by a connection to an LLM to formulate a response to the user's question. The same query string is used by both clients.

You're setting up two clients, so you need permissions on both resources. We use API keys for this exercise. The following endpoints and keys are used for queries:

```python
# Set endpoints and API keys for Azure services
AZURE_SEARCH_SERVICE: str = "PUT YOUR SEARCH SERVICE URL HERE"
AZURE_SEARCH_KEY: str = "PUT YOUR SEARCH SERVICE ADMIN KEY HERE"
AZURE_OPENAI_ACCOUNT: str = "PUT YOUR AZURE OPENAI ACCOUNT URL HERE"
AZURE_OPENAI_KEY: str = "PUT YOUR AZURE OPENAI KEY HERE"
```

## Example script for prompt and query

```python
# Import libraries
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

# Set up clients and specify the chat model
openai_client = AzureOpenAI(
     api_version="2024-06-01",
     azure_endpoint=AZURE_OPENAI_ACCOUNT,
     api_key=AZURE_OPENAI_KEY
 )

deployment_name = "gpt-35-turbo"

search_client = SearchClient(
     endpoint=AZURE_SEARCH_SERVICE,
     index_name=index_name,
     credential=AZURE_SEARCH_CREDENTIAL
 )

# Provide instructions to the model
GROUNDED_PROMPT="""
You are an AI assistant that helps users learn from the information found in the source material.
Answer the query using only the sources provided below.
Use bullets if the answer has multiple points.
If the answer is longer than 3 sentences, provide a summary.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
Sources:\n{sources}
"""

# Provide the query. Notice it's sent to both the search engine and the LLM.
query="how much of earth is covered by water"

# Set up the search results and the chat thread.
# Retrieve the selected fields from the search index related to the question.
search_results = search_client.search(
    search_text=query,
    top=1,
    select="title, chunk, locations"
)
sources_formatted = "\n".join([f'{document["title"]}:{document["chunk"]}:{document["locations"]}' for document in search_results])

response = openai_client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": GROUNDED_PROMPT.format(query=query, sources=sources_formatted)
        }
    ],
    model=deployment_name
)

print(response.choices[0].message.content)
```

## Review results

In this example, the answer is based on a single input (`top=1`) consisting of the one chunk determined by the search engine to be the most relevant. Instructions in the prompt tell the LLM to use only the information in the `sources`, or formatted search results. Results from the first query`"how much of earth is covered by water"` should look similar to the following example.

:::image type="content" source="media/tutorial-rag-solution/chat-results-1.png" alt-text="Screenshot of an LLM response to a simple question using a single match from search results.":::

### Changing the inputs

Increasing or decreasing the number of inputs to the LLM can have a large effect on the response. Try running the same query again after setting `top=3`. When you increase the inputs, the model returns different results each time, even if the query doesn't change. Here's one example of what the model returns after increasing the inputs to 3.

:::image type="content" source="media/tutorial-rag-solution/chat-results-2.png" alt-text="Screenshot of an LLM response to a simple question using a larger result set.":::

Because the model is bound to just the grounding data, the answer is larger also more vague. You can use relevance tuning to potentially generate more focused answers.

### Changing the prompt

You can also change the prompt to control the format of the output, tone, and whether you want the model to supplement the answer with its own training data by changing the prompt. Here's another example of LLM output if we refocus the prompt.

```python
# Provide instructions to the model
GROUNDED_PROMPT="""
You are an AI assistant that helps users pull facts from the source material.
Answer the query cocisely, using bulleted points.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Do not exceed 5 bullets.
Query: {query}
Sources:\n{sources}
"""
```

Output from changing just the prompt, retaining `top=3` from the previous query, might look like this example. 

:::image type="content" source="media/tutorial-rag-solution/chat-results-3.png" alt-text="Screenshot of an LLM response to a change in prompt composition.":::

In this tutorial, assessing the quality of the answer is subjective, but since the model is working with the same results as the previous query, the answer feels incomplete given the body of content available. Let's try the request one last time, increasing `top=10`.

:::image type="content" source="media/tutorial-rag-solution/chat-results-4.png" alt-text="Screenshot of an LLM response to a simple question using top set to 10.":::

There are several observations to note:

- Raising the `top` value can exhaust available quota on the model. If there's no quota, an error message is returned.

- Improving the relevance of the search results from Azure AI Search is the most effective approach for maximizing the utility of your LLM.

In the next series of tutorials, the focus shifts to maximizing relevance and optimizing query performance for speed and concision. We revisit the schema definition and query logic to implement relevance features, but the rest of the pipeline and models remain intact.

<!-- In this tutorial, learn how to send queries and prompts to a chat model for generative search.

Objective:

- Set up clients for chat model and search engine, set up a prompt, point the model to search results.

Key points:

- You can swap out models to see which one works best for your query. No reindexing or upstream modifications required.
- Basic query (takeaway is prompt, scoping to grounding data, calling two clients)
- Basic query is hybrid for the purposes of this tutorial
- Query parent-child, one index
- Query parent-child, two indexes
- Filters

Tasks:

- H2 Set up clients and configure access (to the chat model)
- H2 Query using text, with a filter
- H2 Query using vectors and text-to-vector conversion at query time (not sure what the code looks like for this)
- H2 Query parent-child two indexes (unclear how to do this, Carey said query on child, do a lookup query on parent) -->

<!-- 
## Old introduction

The queries that you create for a conversational search are built for prompts and the orchestration layer. The query response is fed into message prompts sent to an LLM like GPT.

In a RAG app, the query request needs to:

- Target searchable text (vector or nonvector) in the index
- Return the most relevant results
- Return any metadata necessary for citations or other client-side requirements

A query request also specifies relevance options, which can include:

- Scoring profile
- L2 semantic reranking
- Minimum thresholds

A query request can spin off multiple query executions that execute in parallel. A hybrid query can:

- do one or more vector searches
- do keyword search
- apply filters (including geospatial)

Multiple query results are merged and ranked and returned to the client as a single result set.

## Basic query for RAG

TBD

## Add relevance features

TBD

## Hybrid query with relevance features

TBD

## Customize results

Search results are passed in messages to the LLM. This section explains refining results.

### Increase or decrease quantity

Depending on the quota of your LLM, you might want to increase or decrease the amount of information passed in messages.

TBD

### Trim results based on minimum threshold

In preview APIs, you can set a "threshhold" query parameter to exlude results having low search scores. For more information about seeting this vector query parameter, see [Create a vector query](vector-search-how-to-query.md).

### Add or remove fields

Only fields marked as "retrievable" in the search index can appear in results. If a field you want isn't already retrievable, you must drop and rebuild the index to create the physical data structures for storing retrievable data. -->

<!-- ## Next step

> [!div class="nextstepaction"]
> [Maximize relevance](tutorial-rag-build-solution-maximize-relevance.md) -->
