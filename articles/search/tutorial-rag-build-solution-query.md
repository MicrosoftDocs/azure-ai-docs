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



## Generate an answer

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
You are an AI assistant that helps users find the information their looking for.
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

In this example, the answer is based on a single input (`top=1`) consisting of the one chunk determined by the search engine to be the most relevant. Results from the query should look similar to the following example.

```
About 72% of the Earth's surface is covered in water, according to page-79.pdf. The provided sources do not give further information on this topic.
```

Run the same query again after setting `top=3`. When you increase the inputs, the model returns different results each time, even if the query doesn't change. Here's one example of what the model returns after increasing the inputs to 3.

```
About 71% of the earth is covered by water, while the remaining 29% is land. Canada has numerous water bodies like lakes, ponds, and streams, giving it a unique landscape. The Nunavut territory is unsuitable for agriculture due to being snow-covered most of the year and frozen during the summer thaw. Don Juan Pond in the McMurdo Dry Valleys of Antarctica is the saltiest body of water on earth with a salinity level over 40%, much higher than the Dead Sea and Great Salt Lake. It rarely snows in the valley and Don Juan's calcium chloride–rich waters rarely freeze. NASA studies our planet's physical processes, including the water cycle, carbon cycle, ocean circulation, heat movement, and light interaction. NASA has a unique vantage point of observing the earth and making sense of it from space.
```


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

## Next step

> [!div class="nextstepaction"]
> [Maximize relevance](tutorial-rag-build-solution-maximize-relevance.md)
