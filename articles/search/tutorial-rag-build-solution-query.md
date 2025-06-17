---
title: 'RAG tutorial: Search using an LLM'
titleSuffix: Azure AI Search
description: Learn how to build queries and engineer prompts for LLM-enabled search on Azure AI Search. Queries used in generative search provide the inputs to an LLM chat engine.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: tutorial
ms.date: 06/17/2025
---

# Tutorial: Search your data using a chat model (RAG in Azure AI Search)

The defining characteristic of a RAG solution on Azure AI Search is sending queries to a Large Language Model (LLM) for a conversational search experience over your indexed content. It can be surprisingly easy if you implement just the basics.

In this tutorial, you:

> [!div class="checklist"]
> - Set up clients
> - Write instructions for the LLM
> - Provide a query designed for LLM inputs
> - Review results and explore next steps

This tutorial builds on the previous tutorials. It assumes you have a search index created by the [indexing pipeline](tutorial-rag-build-solution-pipeline.md).

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/). For more information, see [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

- [Azure AI Search](search-create-service-portal.md), in a region shared with Azure OpenAI.

- [Azure OpenAI](/azure/ai-services/openai/how-to/create-resource), with a deployment of gpt-4o. For more information, see [Choose models for RAG in Azure AI Search](tutorial-rag-build-solution-models.md)

## Download the sample

You use the same notebook from the previous indexing pipeline tutorial. Scripts for querying the LLM follow the pipeline creation steps. If you don't already have the notebook, [download it](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Tutorial-RAG/Tutorial-rag.ipynb) from GitHub.

## Configure clients for sending queries

The RAG pattern in Azure AI Search is a synchronized series of connections to a search index to obtain the grounding data, followed by a connection to an LLM to formulate a response to the user's question. The same query string is used by both clients.

You're setting up two clients, so you need endpoints and permissions on both resources. This tutorial assumes you set up role assignments for authorized connections, but you should provide the endpoints in your sample notebook:

```python
# Set endpoints and API keys for Azure services
AZURE_SEARCH_SERVICE: str = "PUT YOUR SEARCH SERVICE ENDPOINT HERE"
# AZURE_SEARCH_KEY: str = "DELETE IF USING ROLES, OTHERWISE PUT YOUR SEARCH SERVICE ADMIN KEY HERE"
AZURE_OPENAI_ACCOUNT: str = "PUT YOUR AZURE OPENAI ENDPOINT HERE"
# AZURE_OPENAI_KEY: str = "DELETE IF USING ROLES, OTHERWISE PUT YOUR AZURE OPENAI KEY HERE"
```

## Example script for prompt and query

Here's the Python script that instantiates the clients, defines the prompt, and sets up the query. You can run this script in the notebook to generate a response from your chat model deployment.

For the Azure Government cloud, modify the API endpoint on the token provider to `"https://cognitiveservices.azure.us/.default"`.

```python
# Import libraries
from azure.search.documents import SearchClient
from openai import AzureOpenAI

token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
openai_client = AzureOpenAI(
     api_version="2024-06-01",
     azure_endpoint=AZURE_OPENAI_ACCOUNT,
     azure_ad_token_provider=token_provider
 )

deployment_name = "gpt-4o"

search_client = SearchClient(
     endpoint=AZURE_SEARCH_SERVICE,
     index_name=index_name,
     credential=credential
 )

# Provide instructions to the model
GROUNDED_PROMPT="""
You are an AI assistant that helps users learn from the information found in the source material.
Answer the query using only the sources provided below.
Use bullets if the answer has multiple points.
If the answer is longer than 3 sentences, provide a summary.
Answer ONLY with the facts listed in the list of sources below. Cite your source when you answer the question
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
Sources:\n{sources}
"""

# Provide the search query. 
# It's hybrid: a keyword search on "query", with text-to-vector conversion for "vector_query".
# The vector query finds 50 nearest neighbor matches in the search index
query="What's the NASA earth book about?"
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="text_vector")

# Set up the search results and the chat thread.
# Retrieve the selected fields from the search index related to the question.
# Search results are limited to the top 5 matches. Limiting top can help you stay under LLM quotas.
search_results = search_client.search(
    search_text=query,
    vector_queries= [vector_query],
    select=["title", "chunk", "locations"],
    top=5,
)

# Newlines could be in the OCR'd content or in PDFs, as is the case for the sample PDFs used for this tutorial.
# Use a unique separator to make the sources distinct. 
# We chose repeated equal signs (=) followed by a newline because it's unlikely the source documents contain this sequence.
sources_formatted = "=================\n".join([f'TITLE: {document["title"]}, CONTENT: {document["chunk"]}, LOCATIONS: {document["locations"]}' for document in search_results])

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

In this response, the answer is based on five inputs (`top=5`) consisting of chunks determined by the search engine to be the most relevant. Instructions in the prompt tell the LLM to use only the information in the `sources`, or formatted search results. 

Results from the first query `"What's the NASA earth book about?"` should look similar to the following example.

```
The NASA Earth book is about the intricate and captivating science of our planet, studied 
through NASA's unique perspective and tools. It presents Earth as a dynamic and complex 
system, observed through various cycles and processes such as the water cycle and ocean 
circulation. The book combines stunning satellite images with detailed scientific insights, 
portraying Earth’s beauty and the continuous interaction of land, wind, water, ice, and 
air seen from above. It aims to inspire and demonstrate that the truth of our planet is 
as compelling as any fiction.

Source: page-8.pdf
```

It's expected for LLMs to return different answers, even if the prompt and queries are unchanged. Your result might look very different from the example. For more information, see [Learn how to use reproducible output](/azure/ai-services/openai/how-to/reproducible-output).

> [!NOTE]
> In testing this tutorial, we saw a variety of responses, some more relevant than others. A few times, repeating the same request caused a deterioration in the response, most likely due to confusion in the chat history, possibly with the model registering the repeated requests as dissatisfaction with the generated answer. Managing chat history is out of scope for this tutorial, but including it in your application code should mitigate or even eliminate this behavior.

## Add a filter

Recall that you created a `locations` field using applied AI, populated with places recognized by the Entity Recognition skill. The field definition for locations includes the `filterable` attribute. Let's repeat the previous request, but this time adding a filter that selects on the term *ice* in the locations field. 

A filter introduces inclusion or exclusion criteria. The search engine is still doing a vector search on `"What's the NASA earth book about?"`, but it's now excluding matches that don't include *ice*. For more information about filtering on string collections and on vector queries, see [text filter fundamentals](search-filters.md#text-filter-fundamentals), [Understand collection filters](search-query-understand-collection-filters.md), and [Add filters to a vector query](vector-search-filters.md).

Replace the search_results definition with the following example that includes a filter:

```python
query="what is the NASA earth book about?"
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="text_vector")

# Add a filter that selects documents based on whether locations includes the term "ice".
search_results = search_client.search(
    search_text=query,
    vector_queries= [vector_query],
    filter="search.ismatch('ice*', 'locations', 'full', 'any')",
    select=["title", "chunk", "locations"],
    top=5
)

sources_formatted = "=================\n".join([f'TITLE: {document["title"]}, CONTENT: {document["chunk"]}, LOCATIONS: {document["locations"]}' for document in search_results])
```

Results from the filtered query should now look similar to the following response. Notice the emphasis on ice cover.

```
The NASA Earth book showcases various geographic and environmental features of Earth through 
satellite imagery, highlighting remarkable landscapes and natural phenomena. 

- It features extraordinary views like the Holuhraun Lava Field in Iceland, captured by 
Landsat 8 during an eruption in 2014, with false-color images illustrating different elements 
such as ice, steam, sulfur dioxide, and fresh lava ([source](page-43.pdf)).
- Other examples include the North Patagonian Icefield in South America, depicted through 
clear satellite images showing glaciers and their changes over time ([source](page-147.pdf)).
- It documents melt ponds in the Arctic, exploring their effects on ice melting and 
- heat absorption ([source](page-153.pdf)).
  
Overall, the book uses satellite imagery to give insights into Earth's dynamic systems 
and natural changes.
```

## Change the inputs

Increasing or decreasing the number of inputs to the LLM can have a large effect on the response. Try running the same query again after setting `top=8`. When you increase the inputs, the model returns different results each time, even if the query doesn't change. 

Here's one example of what the model returns after increasing the inputs to 8.

```
The NASA Earth book features a range of satellite images capturing various natural phenomena 
across the globe. These include:

- The Holuhraun Lava Field in Iceland documented by Landsat 8 during a 2014 volcanic 
eruption (Source: page-43.pdf).
- The North Patagonian Icefield in South America, highlighting glacial landscapes 
captured in a rare cloud-free view in 2017 (Source: page-147.pdf).
- The impact of melt ponds on ice sheets and sea ice in the Arctic, with images from 
an airborne research campaign in Alaska during July 2014 (Source: page-153.pdf).
- Sea ice formations at Shikotan, Japan, and other notable geographic features in various 
locations recorded by different Landsat missions (Source: page-168.pdf).

Summary: The book showcases satellite images of diverse Earth phenomena, such as volcanic 
eruptions, icefields, and sea ice, to provide insights into natural processes and landscapes.
```

Because the model is bound to the grounding data, the answer becomes more expansive as you increase size of the input. You can use relevance tuning to potentially generate more focused answers.

## Change the prompt

You can also change the prompt to control the format of the output, tone, and whether you want the model to supplement the answer with its own training data by changing the prompt. 

Here's another example of LLM output if we refocus the prompt on identifying locations for scientific study.

```python
# Provide instructions to the model
GROUNDED_PROMPT="""
You are an AI assistant that helps scientists identify locations for future study.
Answer the query cocisely, using bulleted points.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Do not exceed 5 bullets.
Query: {query}
Sources:\n{sources}
"""
```

Output from changing just the prompt, otherwise retaining all aspects of the previous query, might look like this example. 

```
The NASA Earth book appears to showcase various locations on Earth captured through satellite imagery, 
highlighting natural phenomena and geographic features. For instance, the book includes:

- The Holuhraun Lava Field in Iceland, detailing volcanic activity and its observation via Landsat 8.
- The North Patagonian Icefield in South America, covering its glaciers and changes over time as seen by Landsat 8.
- Melt ponds in the Arctic and their impacts on the heat balance and ice melting.
- Iceberg A-56 in the South Atlantic Ocean and its interaction with cloud formations.

(Source: page-43.pdf, page-147.pdf, page-153.pdf, page-39.pdf)
```

> [!TIP]
> If you're continuing on with the tutorial, remember to restore the prompt to its previous value (`You are an AI assistant that helps users learn from the information found in the source material`).

Changing parameters and prompts affects the response from the LLM. As you explore on your own, keep the following tips in mind:

- Raising the `top` value can exhaust available quota on the model. If there's no quota, an error message is returned or the model might return "I don't know".

- Raising the `top` value doesn't necessarily improve the outcome. In testing with top, we sometimes notice that the answers aren't dramatically better.

- So what might help? Typically, the answer is relevance tuning. Improving the relevance of the search results from Azure AI Search is usually the most effective approach for maximizing the utility of your LLM.

In the next series of tutorials, the focus shifts to maximizing relevance and optimizing query performance for speed and concision. We revisit the schema definition and query logic to implement relevance features, but the rest of the pipeline and models remain intact.

<!-- In this tutorial, learn how to send queries and prompts to a chat model for generative search. The queries that you create for a conversational search are built for prompts and the orchestration layer. The query response is fed into message prompts sent to an LLM like gpt-4o.

Objective:

- Set up clients for chat model and search engine, set up a prompt, point the model to search results.

Key points:

In a RAG app, the query request needs to:

- Target searchable text (vector or nonvector) in the index
- Return the most relevant results
- Return any metadata necessary for citations or other client-side requirements

A query request also specifies relevance options, which can include:

- Scoring profile
- L2 semantic reranking
- Minimum thresholds

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

## Next step

> [!div class="nextstepaction"]
> [Maximize relevance](tutorial-rag-build-solution-maximize-relevance.md)
