---
title: Vector store integrations
titleSuffix: Microsoft Agent Framework
description: Learn how Agent Framework uses vector store abstractions and implementations in .NET and Python.
zone_pivot_groups: programming-languages
author: westey-m
ms.topic: overview
ms.author: westey
ms.date: 09/09/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

<!--
  Language parity table - keep in sync when adding or removing sections.

  | Section                    | C# | Python | Go | Notes                    |
  |----------------------------|:--:|:------:|:--:|--------------------------|
  | Overview and workflow      | Yes | Yes   | Yes | Shared                  |
  | Abstractions and implementations | Yes | Yes | No | Language-specific APIs |
  | Get started                | Yes | Yes   | No  | Language-specific setup |
  | Availability status        | No  | No    | Yes | Go status only          |
-->

# Vector store integrations

Vector stores keep data and its vector embeddings together so applications can
find records by semantic similarity. In Agent Framework applications, you can
use vector stores to retrieve grounding data for Retrieval Augmented Generation
(RAG) or to store information that an agent can recall later.

Vector store abstractions provide common operations for collections and
records, keeping your application logic separated from the specific vector
store implementation. You can, for example, start with a local implementation
and switch to a managed service with minimal changes.

## How vector store integrations work

A typical vector store workflow includes these steps:

1. Define a data model that identifies the record key, data fields, and vector
   fields.
1. Configure an embedding generator if the vector store doesn't generate
   embeddings.
1. Connect to a vector store and select or create a collection.
1. Generate embeddings and upsert records into the collection.
1. Search the collection with text or a vector, depending on the
   implementation's capabilities.
1. Pass relevant search results to an agent as context or expose search as an
   agent tool.

:::zone pivot="programming-language-csharp"

## .NET vector store support

Agent Framework uses the .NET AI ecosystem's standalone abstractions:

- [`Microsoft.Extensions.VectorData`](/dotnet/ai/conceptual/mevd-library)
  provides common vector store, collection, record, and search APIs.
- [`Microsoft.Extensions.AI`](/dotnet/ai/microsoft-extensions-ai) provides
  abstractions such as `IEmbeddingGenerator` for generating embeddings
  independently of a specific model provider.

Where an Agent Framework component accepts a vector store, you can supply a
compatible `Microsoft.Extensions.VectorData` implementation. Each database
implementation is distributed separately from the abstractions package.

### Core abstractions

| Abstraction | Purpose |
|---|---|
| `VectorStore` | Provides operations across collections and creates typed collection instances. |
| `VectorStoreCollection<TKey, TRecord>` | Creates or deletes a collection and upserts, retrieves, or deletes its records. |
| `IVectorSearchable<TRecord>` | Searches records by vector or by text when an embedding generator or database-side embedding capability is available. |

### Available vector store implementations

The following implementations use the common .NET vector store abstractions.
Review each implementation's documentation for package versions, supported
data types, and service-specific limitations.

| Implementation | Availability | Uses an officially supported database SDK | Maintainer or vendor |
|---|:---:|:---:|---|
| [Azure AI Search](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-ai-search-connector) | Available | Yes | Microsoft |
| [Azure Cosmos DB for MongoDB vCore](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector) | Available | Yes | Microsoft |
| [Azure Cosmos DB for NoSQL](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-nosql-connector) | Available | Yes | Microsoft |
| [Couchbase](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/couchbase-connector) | Available | Yes | Couchbase |
| [Elasticsearch](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/elasticsearch-connector) | Available | Yes | Elastic |
| Chroma | Planned | Not applicable | Not applicable |
| [In-memory](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/inmemory-connector) | Available | Not applicable | Microsoft |
| Milvus | Planned | Not applicable | Not applicable |
| [MongoDB](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/mongodb-connector) | Available | Yes | Microsoft |
| [Neon Serverless Postgres](https://neon.com/) | Use the [Postgres implementation](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector) | Yes | Microsoft |
| [Oracle](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/oracle-connector) | Available | Yes | Oracle |
| [Pinecone](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/pinecone-connector) | Available | No | Microsoft |
| [Postgres](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector) | Available | Yes | Microsoft |
| [Qdrant](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/qdrant-connector) | Available | Yes | Microsoft |
| [Redis](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/redis-connector) | Available | Yes | Microsoft |
| [SQL Server](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/sql-connector) | Available | Yes | Microsoft |
| [SQLite](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/sqlite-connector) | Available | Yes | Microsoft |
| [Volatile in-memory](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/volatile-connector) | Deprecated; use the in-memory implementation | Not applicable | Microsoft |
| [Weaviate](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/weaviate-connector) | Available | Yes | Microsoft |

> [!IMPORTANT]
> Vector store implementations come from multiple maintainers. Evaluate each
> implementation's quality, licensing, support policy, and version
> compatibility before you use it. Some implementations use database SDKs that
> the database provider doesn't officially support.

### Get started

1. Add the
   [`Microsoft.Extensions.VectorData.Abstractions`](https://www.nuget.org/packages/Microsoft.Extensions.VectorData.Abstractions)
   package and the package for your chosen vector store implementation.
1. Define a record type and identify its key, data, and vector properties.
1. Configure an `IEmbeddingGenerator` if your implementation requires
   application-generated embeddings.
1. Create the implementation's `VectorStore`, and then get a typed
   `VectorStoreCollection<TKey, TRecord>`.
1. Ensure that the collection exists, upsert records, and call `SearchAsync`
   with text or a vector.

For a complete introduction to data models, ingestion, embeddings, and search,
see [Vector databases for .NET AI apps](/dotnet/ai/vector-stores/overview).

:::zone-end

:::zone pivot="programming-language-python"

## Python vector store support

Agent Framework provides experimental, native Python contracts for vector store
models, collection operations, store factories, vector and keyword-hybrid
search, and agent search tools. The contracts are part of
`agent-framework-core` and don't require Pydantic, NumPy, pandas, or Semantic
Kernel.

> [!WARNING]
> The native Python vector store APIs are experimental. Limited breaking changes
> might occur before they become stable.

### Core abstractions

| Abstraction | Purpose |
|---|---|
| `VectorStoreField` and `VectorStoreCollectionDefinition` | Describe key, data, and vector fields, including storage names, indexes, dimensions, and distance functions. |
| `@vectorstoremodel` and `register_vectorstoremodel()` | Register dataclasses, Pydantic models, msgspec structs, plain classes, or externally owned model types. |
| `BaseVectorCollection` and `SupportsVectorUpsert` | Define batch upsert, get, delete, collection lifecycle, record conversion, and optional embedding generation. |
| `BaseVectorStore` | Defines a store that lists collections and creates typed collection clients. |
| `BaseVectorSearch` and `SupportsVectorSearch` | Define vector and keyword-hybrid search, paging, filters, score thresholds, and search results. |
| `Filter`, `FilterGroup`, and `Param` | Define portable, data-only filters, including model-supplied filter parameters for search tools. |
| `InMemoryStore` and `InMemoryCollection` | Provide process-local CRUD and linear-scan search for development and tests. |
| `GenerateVectors` | Controls whether upserts generate all, none, or selected vector fields. |
| `create_vector_search_tool()` | Exposes any `SupportsVectorSearch` implementation as an Agent Framework function tool. |

The following sample defines vector store records by annotating their key, data,
and vector fields:

:::code language="python" source="~/../agent-framework-code/python/samples/02-agents/vector_stores/vector_store_models.py" range="126-143":::

Use `VectorStoreCollectionDefinition` directly for dictionaries. For model types
owned by another package, use `register_vectorstoremodel()` with an explicit
definition and optional encoder and decoder. Array-like vector values serialize
through `tolist()` without adding a NumPy dependency.

Agent Framework includes an in-memory implementation for development and tests.
It stores records in the current process and uses a linear scan, so use a
database connector for production workloads.

The following sample stores precomputed vectors and searches them with a
portable filter tree:

:::code language="python" source="~/../agent-framework-code/python/samples/02-agents/vector_stores/in_memory_filters.py" range="3-7,17-64":::

Use `Param` when the model should supply a filter value. Its Python type,
description, and constraints become part of the search tool's JSON schema:

:::code language="python" source="~/../agent-framework-code/python/samples/02-agents/vector_stores/in_memory_search_tool.py" range="132-162":::

### Native Agent Framework implementations

The following implementations use the native Agent Framework contracts. Each
one is also available as a separate Semantic Kernel connector, but the two
connector families aren't interchangeable.

| Implementation | Agent Framework package and lifecycle | Separate Semantic Kernel connector | Search modes | Key limitations |
|---|---|---|---|---|
| In-memory | `agent-framework-core`; released package with experimental vector APIs | [Available](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/inmemory-connector) | Dense vector with portable filters | Process-local linear scan for development and tests, not a production database. |
| Azure AI Search | `agent-framework-azure-ai-search`; beta package with experimental vector APIs | [Available](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-ai-search-connector) | Dense vector and keyword-hybrid | One top-level dense vector field per query. Some thresholds, hybrid text-recall controls, strict post-filtering, and permissions require a supporting preview SDK/API and `allow_preview=True`. |
| PostgreSQL with pgvector | `agent-framework-postgres`; alpha package | [Available](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector) | Exact dense vector, HNSW, and IVFFlat | Requires PostgreSQL 13+, pgvector 0.8.0+, an existing schema, and the enabled extension. Keyword and hybrid search aren't supported. |
| Qdrant | `agent-framework-qdrant`; alpha package | [Available](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/qdrant-connector) | Dense vector with server-side portable filters | Server mode requires Qdrant 1.16.2+. Keys must be unsigned 64-bit integers or UUIDs. Keyword and hybrid search aren't supported, and filters aren't available in local SDK mode. |
| Redis | `agent-framework-redis`; beta package with experimental vector APIs | [Available](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/redis-connector) | Dense vector over HASH or JSON records | Requires Redis 8.0.3+ with Search; JSON records also require RedisJSON. Redis Cluster, keyword search, and hybrid search aren't supported. |

Install a prerelease connector package for the database you use:

```bash
pip install agent-framework-azure-ai-search --pre
pip install agent-framework-postgres --pre
pip install agent-framework-qdrant --pre
pip install agent-framework-redis --pre
```

Each connector implements the common model, collection, CRUD, filter, and
search contracts. Database-specific capabilities and restrictions still apply.
For complete examples, see the
[Azure AI Search](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/vector_stores/azure_ai_search.py),
[Postgres](https://github.com/microsoft/agent-framework/blob/main/python/packages/postgres/samples/postgres_vectors.py),
[Qdrant](https://github.com/microsoft/agent-framework/blob/main/python/packages/qdrant/samples/qdrant_vectors.py),
and
[Redis](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/vector_stores/redis_store.py)
samples.

### Semantic Kernel-only implementations

Applications can continue to use Semantic Kernel's Python vector stores
directly. These implementations use the separate Semantic Kernel vector store
contracts rather than the native Agent Framework contracts. The following
implementations don't currently have a native Agent Framework connector:

| Implementation | Availability | Uses an officially supported database SDK | Maintainer or vendor |
|---|:---:|:---:|---|
| [Azure Cosmos DB for MongoDB vCore](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-mongodb-connector) | Available | Yes | Microsoft Semantic Kernel project |
| [Azure Cosmos DB for NoSQL](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/azure-cosmosdb-nosql-connector) | Available | Yes | Microsoft Semantic Kernel project |
| [Chroma](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/chroma-connector) | Available | Yes | Microsoft Semantic Kernel project |
| Elasticsearch | Planned | Not applicable | Not applicable |
| [Faiss](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/faiss-connector) | Available | Yes | Microsoft Semantic Kernel project |
| [MongoDB](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/mongodb-connector) | Available | Yes | Microsoft Semantic Kernel project |
| [Neon Serverless Postgres](https://neon.com/) | Use the [Postgres implementation](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/postgres-connector) | Yes | Microsoft Semantic Kernel project |
| [Oracle](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/oracle-connector) | Available | Yes | Oracle |
| [Pinecone](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/pinecone-connector) | Available | Yes | Microsoft Semantic Kernel project |
| [SQL Server](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/sql-connector) | Available | `pyodbc` | Microsoft Semantic Kernel project |
| SQLite | Planned | Not applicable | Microsoft Semantic Kernel project |
| [Weaviate](/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/weaviate-connector) | Available | Yes | Microsoft Semantic Kernel project |

> [!IMPORTANT]
> Vector store implementations come from multiple maintainers. Evaluate each
> implementation's quality, licensing, support policy, and version compatibility
> before you use it.

### Use a Semantic Kernel-only implementation

1. Install `semantic-kernel` and the dependencies required by your chosen
   implementation.
1. Define a model with the `@vectorstoremodel` decorator and identify its key,
   data, and vector fields.
1. Create an implementation-specific collection for that model.
1. Ensure that the collection exists, and then upsert records.
1. Use the collection's search APIs to retrieve records for your application.

For implementation setup and complete examples, see
[Semantic Kernel Vector Stores](/semantic-kernel/concepts/vector-store-connectors/).

:::zone-end

:::zone pivot="programming-language-go"

## Go vector store support

Vector store integration isn't yet available in Agent Framework for Go. See the
[Agent Framework Go repository](https://github.com/microsoft/agent-framework-go)
for the latest status.

:::zone-end

## Related Agent Framework scenarios

- [Add RAG to an agent](../../../agents/rag.md).
- [Add semantic chat history memory](../../../concepts/agents/conversations/chat-history-memory-provider.md).
- [Choose a context provider integration](../context-providers/index.md).

## Next steps

> [!div class="nextstepaction"]
> [Add RAG to an agent](../../../agents/rag.md)
