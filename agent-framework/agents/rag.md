---
title: RAG
description: Learn how to use Retrieval Augmented Generation (RAG) with Agent Framework
zone_pivot_groups: programming-languages
author: westey-m
ms.topic: reference
ms.author: westey
ms.date: 09/09/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

<!--
  Language parity table - keep in sync when adding/removing sections.

  | Section                  | C# | Python | Go | Notes                          |
  |--------------------------|:--:|:------:|:--:|--------------------------------|
  | RAG overview             | ✅ |   ✅   | ✅ | Shared                         |
  | TextSearchProvider       | ✅ |   ❌   | ❌ | .NET-specific                  |
  | Vector store search tools | ❌ |   ✅   | ❌ | Python native Agent Framework APIs |
  | Go availability          | ✅ |   ✅   | ✅ | Go zone is status only         |
  | Service integrations     | ✅ |   ✅   | ✅ | Shared links                   |
-->

# RAG

Microsoft Agent Framework supports Retrieval Augmented Generation (RAG)
through context providers that add retrieved content before model invocation
and search tools that let the model retrieve grounding data on demand.

For conversation/session patterns alongside retrieval, see [Conversations & Memory overview](../concepts/agents/conversations/index.md).
For service-specific setup, see [Azure AI Search](../integrations/by-component/context-providers/azure-ai-search.md), [Microsoft Foundry](../integrations/by-component/context-providers/microsoft-foundry.md#use-file-search-rag), and [Neo4j](../integrations/by-component/context-providers/neo4j.md#graphrag-from-an-existing-knowledge-graph).

::: zone pivot="programming-language-csharp"

## Using TextSearchProvider

The `TextSearchProvider` class is an out-of-the-box implementation of a RAG context provider.
It supports different modes of operation, e.g. doing a search for each agent run with chat history, or advertising function tools for doing searches.

It can easily be attached to a `ChatClientAgent` using the `AIContextProviders` option.

```csharp
// Configure the options for the TextSearchProvider.
TextSearchProviderOptions textSearchOptions = new()
{
    SearchTime = TextSearchProviderOptions.TextSearchBehavior.BeforeAIInvoke,
};

// Create the AI agent with the TextSearchProvider.
AIAgent agent = azureOpenAIClient
    .GetChatClient(deploymentName)
    .AsAIAgent(new ChatClientAgentOptions
    {
        ChatOptions = new() { Instructions = "You are a helpful support specialist. Answer questions using the provided context and cite the source document when available." },
        AIContextProviders = [new TextSearchProvider(SearchAdapter, textSearchOptions)]
    });
```

The `TextSearchProvider` requires a function that provides the search results given a query. This can be implemented using any search technology, e.g. Azure AI Search, or a web search engine.

> [!TIP]
> See [Vector store integrations](../integrations/by-component/vector-stores/index.md)
> for more information on how to use a vector store for search results.

Here is an example of a mock search function that returns pre-defined results based on the query.
`SourceName` and `SourceLink` are optional, but if provided will be used by the agent to cite the source of the information when answering the user's question.

```csharp
static Task<IEnumerable<TextSearchProvider.TextSearchResult>> SearchAdapter(string query, CancellationToken cancellationToken)
{
    // The mock search inspects the user's question and returns pre-defined snippets
    // that resemble documents stored in an external knowledge source.
    List<TextSearchProvider.TextSearchResult> results = new();

    if (query.Contains("return", StringComparison.OrdinalIgnoreCase) || query.Contains("refund", StringComparison.OrdinalIgnoreCase))
    {
        results.Add(new()
        {
            SourceName = "Contoso Outdoors Return Policy",
            SourceLink = "https://contoso.com/policies/returns",
            Text = "Customers may return any item within 30 days of delivery. Items should be unused and include original packaging. Refunds are issued to the original payment method within 5 business days of inspection."
        });
    }

    return Task.FromResult<IEnumerable<TextSearchProvider.TextSearchResult>>(results);
}
```

### TextSearchProvider Options

The `TextSearchProvider` can be customized via the `TextSearchProviderOptions` class. Here is an example of creating options to run the search prior to every model invocation and keep a short rolling window of chat history for searches.

```csharp
TextSearchProviderOptions textSearchOptions = new()
{
    // Run the search prior to every model invocation and keep a short rolling window of chat history for searches.
    SearchTime = TextSearchProviderOptions.TextSearchBehavior.BeforeAIInvoke,
    RecentMessageMemoryLimit = 6,
};
```

The `TextSearchProvider` class supports the following options via the `TextSearchProviderOptions` class.

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| SearchTime | `TextSearchProviderOptions.TextSearchBehavior` | Indicates when the search should be executed. There are two options, each time the agent is run, or on-demand via function calling. | `TextSearchProviderOptions.TextSearchBehavior.BeforeAIInvoke` |
| FunctionToolName | `string` | The name of the exposed search tool when operating in on-demand mode. | "Search" |
| FunctionToolDescription | `string` | The description of the exposed search tool when operating in on-demand mode. | "Allows searching for additional information to help answer the user question." |
| ContextPrompt | `string` | The context prompt prefixed to results. | "## Additional Context\nConsider the following information from source documents when responding to the user:" |
| CitationsPrompt | `string` | The instruction appended after results to request citations. | "Include citations to the source document with document name and link if document name and link is available." |
| ContextFormatter | `Func<IList<TextSearchProvider.TextSearchResult>, string>` | Optional delegate to fully customize formatting of the result list. If provided, `ContextPrompt` and `CitationsPrompt` are ignored. | `null` |
| RecentMessageMemoryLimit | `int` | The number of recent conversation messages (both user and assistant) to keep in memory and include when constructing the search input for `BeforeAIInvoke` searches. | `0` (disabled) |
| RecentMessageRolesIncluded | `List<ChatRole>` | The list of `ChatRole` types to filter recent messages to when deciding which recent messages to include when constructing the search input. | `ChatRole.User` |

> [!TIP]
> See the [.NET samples](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/02-agents/AgentWithRAG) for complete runnable examples.

::: zone-end
::: zone pivot="programming-language-python"

Agent Framework provides native vector-store contracts and
`create_vector_search_tool()`. The helper turns any
`SupportsVectorSearch` implementation into a function tool, so the model can
retrieve grounding data before it answers.

### Create a native vector search tool

First, define your vector-store model, create a collection, and load its
records. The following sample uses `InMemoryCollection` with
`OpenAIEmbeddingClient`, but you can supply any native Agent Framework
collection that implements `SupportsVectorSearch`. It then exposes optional
category and rating filters to the model, maps each result to grounding text,
and instructs the agent to search before it answers:

:::code language="python" source="~/../agent-framework-code/python/samples/02-agents/vector_stores/in_memory_search_tool.py" range="3-20,116-179":::

The full sample defines the `Hotel` model and loads the source records before
the shown collection setup. Set `OPENAI_API_KEY` before you run it.

### Customize search behavior

Configure `create_vector_search_tool()` with the following options:

| Option | Purpose |
|---|---|
| `name` | Sets the function name exposed to the model. Use a unique name when you add multiple search tools. |
| `description` | Explains when and why the model should use the tool. |
| `approval_mode` | Sets tool approval to `always_require` or `never_require`. |
| `search_type` | Selects `vector` or `keyword_hybrid` search. The collection must support the selected mode. |
| `top` and `skip` | Set fixed paging values or use typed `Param` values that the model supplies. |
| `filter` | Applies a portable `Filter` or `FilterGroup`. A filter can contain typed `Param` values exposed in the tool schema. |
| `result_mapper` | Converts each `SearchResponse` into text or multimodal `Content` for the model. |

The generated tool always includes a `query` string. Any `Param` values in the
filter, `top`, or `skip` settings become additional validated tool arguments.
Use `Literal` and numeric constraints to keep model-supplied values within the
range your application accepts.

You can create multiple tools for different collections or search modes. Give
each tool a distinct `name` and `description` so the model can select the
appropriate knowledge source.

### Choose a native vector store

Native Python implementations are available for in-memory search, Azure AI
Search, PostgreSQL with pgvector, Qdrant, and Redis. Their search modes,
package lifecycle, installation commands, and limitations differ. See
[Vector store integrations](../integrations/by-component/vector-stores/index.md)
to select and configure an implementation. That page also identifies databases
that currently have only a separate Semantic Kernel connector.

::: zone-end

::: zone pivot="programming-language-go"

> [!NOTE]
> Go support for this feature is coming soon. See the [Agent Framework Go repository](https://github.com/microsoft/agent-framework-go) for the latest status.

::: zone-end
## Graph RAG

For GraphRAG using graph traversal enriched search with Cypher queries, see the [Neo4j GraphRAG Provider](../integrations/by-component/context-providers/neo4j.md#graphrag-from-an-existing-knowledge-graph).

## Next steps

> [!div class="nextstepaction"]
> [Declarative Agents](./declarative.md)
