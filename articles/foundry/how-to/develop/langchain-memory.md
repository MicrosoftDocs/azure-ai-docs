---
title: Use Foundry Memory with LangChain and LangGraph
description: Learn how to use langchain-azure-ai with Foundry Memory to build AI apps that remember user preferences across sessions.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/05/2026
ms.author: fasantia
author: santiagxf
ms.reviewer: sgilley
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to use langchain-azure-ai with Foundry Memory so that my application can retrieve long-term user context across sessions.
---

# Use Foundry Memory with LangChain and LangGraph

Use `langchain-azure-ai` and Foundry Memory to add long-term memory to your
applications. In this article, you create a memory-backed chain,
store user preferences, recall them in a new session, and run direct memory
queries.

This pattern works for both LangChain and LangGraph applications. The core idea
is to keep short-term chat history in your runtime and use Foundry Memory as the
long-term store for user-level context.

Foundry Memory focuses on long-term memory. Keep short-term turn-by-turn state
in LangChain or LangGraph runtime state.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A [Foundry project](../../how-to/create-projects.md).
- A deployed Microsoft Foundry chat model for memory retrieval.
	- This tutorial uses "gpt-4.1".
- A deployed chat model and embedding model for the memory store.
	- This tutorial uses `text-embedding-3-large`.
- Python 3.10 or later.
- Azure CLI signed in (`az login`) so `DefaultAzureCredential` can authenticate with role **Azure AI Developer**.

### Configure your environment

Install the required packages for this tutorial. Use `langchain-azure-ai` for
LangChain and LangGraph integration, `azure-ai-projects` for memory store
management, and `azure-identity` for authentication.

```bash
pip install -U "langchain-azure-ai" azure-ai-projects azure-identity
```

Set your environment variables that we use in this tutorial:

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
```

## Understand the memory model

Foundry Memory stores and retrieves two long-term memory types:

- User profile memory: stable user facts and preferences, such as preferred
	name or dietary constraints.
- Chat summary memory: distilled summaries of prior discussion topics.

Memory uses the idea of "scope" to partition information so it can be stored and retrieved consistently. Scopes
are like identifiers or keys to organize information.

- You can use *user IDs* as the stable identity for long-term memory. Keep it the same across
	sessions for the same user.
- You can use *session IDs* as the short-term conversation identity. Change it per chat
	session.
- You can use *resource IDs* as the stable identifier for long-term memory across multiple users.

This separation lets your app remember user preferences across sessions without
mixing unrelated conversations.

## Create the memory store

Before getting started, you need to create a memory store. For this operation, use
the Microsoft Foundry projects SDK `azure-ai-projects`.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
	MemoryStoreDefaultDefinition,
	MemoryStoreDefaultOptions,
)
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
credential = DefaultAzureCredential()
client = AIProjectClient(endpoint=endpoint, credential=credential)

store_name = "lc-integration-test-store"
try:
    store = client.beta.memory_stores.get(store_name)
    print(f"✓ Memory store '{store_name}' already exists")
except ResourceNotFoundError:
    print(f"Creating memory store '{store_name}'...")
    definition = MemoryStoreDefaultDefinition(
        chat_model="gpt-4.1", 						# Change for your LLM model
        embedding_model="text-embedding-3-large",	# Change for your emebddings model
        options=MemoryStoreDefaultOptions(
            user_profile_enabled=True,
            chat_summary_enabled=True,
        ),
    )
    store = client.beta.memory_stores.create(
        name=store_name,
        description="Long-term memory store",
        definition=definition,
    )
    print(f"✓ Memory store '{store_name}' created successfully")
```

```output
✓ Memory store 'lc-integration-test-store' created successfully
```

**What this snippet does:** Connects to your Foundry project, gets or creates
the memory store, and enables user profile plus chat summary extraction.


## Using memory in LangGraph and LangChain

Foundry Memory integrates in LangGraph and LangChain by introducing two objects:

* The class `langchain_azure_ai.chat_message_history.AzureAIMemoryChatMessageHistory`
creates a memory-backed chat history.
* The class `langchain_azure_ai.retrievers.AzureAIMemoryRetriever` allows retrieval of
memories from the chat message history.

In general, you can use the following practical retrieval strategies with them:

- Retrieve user profile memory early in a conversation to personalize responses.
- Retrieve chat summary memory based on the current turn to recover relevant
	prior context.

## Example: Add a session-aware memory layer

In this example, we build a single runnable in LangChain that retrieves relevant long-term memory,
injects it into the prompt, and executes the model with short-term chat history
and long-term memory together.

Let's see how to implement it:

### Create the chat message history

This example uses a stable `user_id` as the memory scope. Use `session_id` for per-session
conversation context.

```python
from langchain_azure_ai.chat_message_histories import AzureAIMemoryChatMessageHistory
from langchain_azure_ai.retrievers import AzureAIMemoryRetriever
from langchain_core.chat_history import InMemoryChatMessageHistory

_session_histories: dict[tuple[str, str], AzureAIMemoryChatMessageHistory] = {}

def get_session_history(user_id: str, session_id: str) -> AzureAIMemoryChatMessageHistory:
    """Get or create a session history for a user and session.
    
    Args:
        user_id: Stable user identifier (used as scope in Foundry Memory)
        session_id: Ephemeral session identifier
        
    Returns:
        AzureAIMemoryChatMessageHistory instance
    """
    cache_key = (user_id, session_id)
    if cache_key not in _session_histories:
        _session_histories[cache_key] = AzureAIMemoryChatMessageHistory(
            project_endpoint=endpoint,
            credential=credential,
            store_name=store_name,
            scope=user_id,
            base_history=InMemoryChatMessageHistory(),
            update_delay=0,  # TEST MODE: process updates immediately (default ~300s)
        )
    return _session_histories[cache_key]


def get_foundry_retriever(user_id: str, session_id: str) -> AzureAIMemoryRetriever:
    """Get a retriever tied to the cached session history.
    
    This preserves incremental search state across turns.
    
    Args:
        user_id: Stable user identifier
        session_id: Ephemeral session identifier
        
    Returns:
        AzureAIMemoryRetriever instance
    """
    return get_session_history(user_id, session_id).get_retriever(k=5)
```

**What this snippet does:** Creates a memory-backed history and retriever per
`(user_id, session_id)` pair and caches them so retrieval state survives across
turns in the same session. For this walkthrough, `update_delay=0` makes memory updates immediately visible.
In production, use the default delay unless you specifically need instant
extraction. `session_histories` is used to avoid having to recreate the objects constantly.

### Compose the runnable with memory retrieval

Let's create a runnable to implement the loop:

```python
from typing import Any
import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

llm = init_chat_model("azure_ai:gpt4.1" temperature=0.7)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are helpful and concise. Use prior memories when relevant."),
        MessagesPlaceholder("history"),
        ("system", "Memories:\n{memories}"),
        ("human", "{question}"),
    ]
)


def chain_for_session(user_id: str, session_id: str) -> RunnableWithMessageHistory:
    """Create a chain with message history for a specific user and session.
    
    Args:
        user_id: Stable user identifier
        session_id: Ephemeral session identifier
        
    Returns:
        Runnable chain with message history
    """
    retriever = get_foundry_retriever(user_id, session_id)

    def format_memories(x: dict[str, Any]) -> str:
        """Retrieve and format memories as text."""
        docs = retriever.invoke(x["question"])
        return (
            "\n".join([doc.page_content for doc in docs])
            if docs
            else "No relevant memories found."
        )

    # Use RunnablePassthrough.assign to add memories to the input dict
    # RunnableWithMessageHistory will inject history automatically
    chain = RunnablePassthrough.assign(memories=format_memories) | prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history=get_session_history,
        input_messages_key="question",
        history_messages_key="history",
        history_factory_config=[
            ConfigurableFieldSpec(
                id="user_id",
                annotation=str,
                name="User ID",
                description="Unique identifier for the user.",
                default="",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id="session_id",
                annotation=str,
                name="Session ID",
                description="Unique identifier for the session.",
                default="",
                is_shared=True,
            ),
        ],
    )
    return chain_with_history
```

**What this snippet does:** Builds a runnable that injects retrieved memories
into the prompt, then wraps it with `RunnableWithMessageHistory` so chat history
and long-term memory work together.

This pattern keeps your prompt deterministic: every turn explicitly includes
retrieved memory in the `Memories` section.

### Run a practical cross-session scenario

This scenario shows the full value of long-term memory:

1. In session A, the user shares preferences.
1. In session B, the app recalls those preferences automatically.

```python
import time

user_id = "user_001"
session_id = "session_2026_02_10_001"
chain = chain_for_session(user_id, session_id)

# 4) Session A: seed preferences (long-term memory extraction happens async)
print(
	"\n=== Turn 1 (Session A): Introduce a preference "
	"(will be extracted into long-term memory) ==="
)
r1 = chain.invoke(
	{"question": "Hi! Call me JT. I prefer dark roast coffee and budget trips."},
	config={"configurable": {"user_id": user_id, "session_id": session_id}},
)
print("ASSISTANT:", r1.content)

print("\n=== Turn 2 (Session A): Add another preference ===")
r2 = chain.invoke(
	{
		"question": "Also, I usually drink green tea in the afternoon "
		"and I like staying in hostels."
	},
	config={"configurable": {"user_id": user_id, "session_id": session_id}},
)
print("ASSISTANT:", r2.content)

# Because we set update_delay=0, extraction should happen immediately for demo.
# If you use the default delay, you may need to wait before querying from new session.
time.sleep(60)

# 5) Cross-session test: same user_id, new session_id
session_id_b = "session_2026_02_10_002"
chain_b = chain_for_session(user_id, session_id_b)

print("\n=== Turn 3 (Session B): New session should recall coffee preference ===")
r4 = chain_b.invoke(
	{"question": "Remind me of my coffee preference and travel style."},
	config={"configurable": {"user_id": user_id, "session_id": session_id_b}},
)
print("ASSISTANT:", r4.content)

print("\n=== Turn 4 (Session B): Retrieve another preference ===")
r5 = chain_b.invoke(
	{
		"question": "What do I usually drink in the afternoon, "
		"and where do I like to stay?"
	},
	config={"configurable": {"user_id": user_id, "session_id": session_id_b}},
)
print("ASSISTANT:", r5.content)
```

```output
=== Turn 1 (Session A) ===
ASSISTANT: Nice to meet you, JT. I noted that you prefer dark roast coffee and budget trips.

=== Turn 2 (Session A) ===
ASSISTANT: Got it. I also noted that you usually drink green tea in the afternoon and prefer hostels.

=== Turn 3 (Session B) ===
ASSISTANT: Your coffee preference is dark roast, and your travel style is budget trips.

=== Turn 4 (Session B) ===
ASSISTANT: You usually drink green tea in the afternoon, and you like staying in hostels.
```

**What this snippet does:** Seeds user preferences in session A, starts session
B for the same user, and shows that the app can recall prior preferences across
sessions.

## Example: Query memory directly for non-chat use cases

Use an ad-hoc retriever when you want direct memory reads outside the
conversation pipeline, for example in personalization middleware or profile
inspection tools.

```python
adhoc = AzureAIMemoryRetriever(
	project_endpoint=endpoint,
	credential=credential,
	store_name=store_name,
	scope=user_id,
	k=5,
)
print("\n=== Turn 5 (Ad-hoc): Direct retriever query without session history ===")
adhoc_docs = adhoc.invoke("What are my drinking preferences?")
for i, doc in enumerate(adhoc_docs, start=1):
	print(f"MEMORY {i}:", doc.page_content)
```

```output
MEMORY 1: Prefers dark roast coffee.
MEMORY 2: Prefers budget trips.
MEMORY 3: Usually drinks green tea in the afternoon.
MEMORY 4: Likes staying in hostels.
```

**What this snippet does:** Runs a direct memory search for the current scope. All memories
are retrieved (capped by `k`) but sorted by relevance.

Use this pattern when you need direct memory reads for features such as profile
cards, personalization middleware, or workflow routing.

## Example: Use memory in graphs

LangGraph uses the same conceptual pattern:

- Keep `user_id` stable for long-term memory.
- Use `thread_id` (or equivalent) for short-term thread context.
- Retrieve memory before calling the model node.

If you already have a `StateGraph`, inject retrieval in your model node and
append memory text to your model input. Another typical strategy is to use
a pre-model hook.

```python
from langgraph.graph import MessagesState


def call_model_with_foundry_memory(state: MessagesState, config: dict):
	user_id = config["configurable"]["user_id"]
	session_id = config["configurable"]["thread_id"]
	query = state["messages"][-1].content

	retriever = get_foundry_retriever(user_id, session_id)
	docs = retriever.invoke(query)
	memory_text = "\n".join(d.page_content for d in docs) if docs else ""

	response = llm.invoke(
		[
			{"role": "system", "content": "Use prior memories when relevant."},
			{"role": "system", "content": f"Memories:\n{memory_text}"},
			*state["messages"],
		]
	)
	return {"messages": [response]}
```

**What this snippet does:** Shows a LangGraph node pattern that retrieves
Foundry memory for the current turn and injects it into model input.

For broader LangGraph memory concepts, see:

- [Add memory in LangGraph](https://docs.langchain.com/oss/python/langgraph/add-memory)

## Understand preview limits and operational guidance

Before moving to production, validate these constraints:

- Memory is in preview and behavior can change.
- Memory requires compatible chat and embedding deployments.
- Quotas apply per store and per scope, including search and update request
	rates.

Also plan defensive controls for memory poisoning or prompt-injection attempts.
Validate untrusted inputs before they influence stored memory.

## Clean up resources

After running samples, delete the scope to avoid test data leaking into future
runs.

```python
result = client.memory_stores.delete_scope(name=store_name, scope=user_id)
print(
	f"Deleted {getattr(result, 'deleted_count', 'all')} memories "
	f"for scope '{user_id}'."
)
```

```output
Deleted 4 memories for scope 'user_001'.
```

> [!div class="nextstepaction"]
> [Trace LangChain and LangGraph apps](langchain-traces.md)

## Related content

- [Use Foundry Agent Service with LangGraph](langchain-agents.md)
- [Get started with Microsoft Foundry SDKs and Endpoints](sdk-overview.md)
- [Use memory with Foundry Agent Service](../../agents/how-to/memory-usage.md)
- [What is memory in Foundry Agent Service](../../agents/concepts/what-is-memory.md)
