---
title: Include file
description: Include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 07/15/2026
ms.custom: include, doc-kit-assisted
ai-usage: ai-assisted
---

Tool search lets the model dynamically search for and load tool definitions into its context as needed, so you don't have to load every tool definition up front. This approach can reduce token usage and cost. Tool search also preserves the model's cache by injecting newly discovered tools at the end of the context window. Access tool search through the `tool_search` tool in the Azure OpenAI Responses API.

> [!NOTE]
> Tool search is supported on `gpt-5.4` and later models. In the examples that follow, replace `gpt-5.5` with the name of your model deployment.

Tool search in the Responses API is different from [tool search in a Foundry Agent Service toolbox](../../agents/how-to/tools/tool-search.md). Responses API tool search defers tool definitions that you declare in a request. Toolbox tool search discovers tools configured in a versioned Foundry toolbox.

## Prerequisites

- An Azure OpenAI model deployment that supports tool search.
- An authentication method:
  - API key, or
  - Microsoft Entra ID (recommended).
- Install the client libraries for your language:
  - **Python**:

    ```bash
    pip install openai azure-identity
    ```

  - **JavaScript**:

    ```bash
    npm install openai @azure/identity
    ```

- For REST requests, set `AZURE_OPENAI_API_KEY` for API key authentication or `AZURE_OPENAI_AUTH_TOKEN` for Microsoft Entra ID authentication.

## Understand how tool search works

To activate tool search:

1. Add `tool_search` to the `tools` array.
1. Mark the tools that you want to defer with `defer_loading: true`.

You can defer individual functions, functions inside a namespace, and MCP servers. When you defer a tool, the model doesn't load its full definition into the context until it decides that it needs the tool. The model then uses tool search to load the relevant tools before it calls them.

## Use namespaces where possible

You can use tool search with deferred functions, namespaces, or MCP servers. Use namespaces or MCP servers when possible. Models are primarily trained to search these surfaces, and they usually provide greater token savings.

For namespaces, `defer_loading` applies to the functions inside the namespace, not to the namespace object itself.

At the start of a request, the model still sees the name and description of each searchable surface. For a namespace or MCP server, the model sees only the namespace or server name and description. It doesn't see the individual function definitions until tool search loads them. For an individually deferred function, the model still sees the function name and description, so tool search primarily defers the parameter schema.

For the greatest token savings, group deferred functions into namespaces or MCP servers. Give each surface a clear, high-level description that summarizes its contents. The model can then search and load only the relevant functions.

> [!TIP]
> Keep each namespace to fewer than 10 functions for better token efficiency and model performance.

The following tool configuration defines a namespace with one deferred function:

```json
{
  "tools": [
    {
      "type": "namespace",
      "name": "crm",
      "description": "CRM tools for customer lookup and order management.",
      "tools": [
        {
          "type": "function",
          "name": "list_open_orders",
          "description": "List open orders for a customer ID.",
          "defer_loading": true,
          "parameters": {
            "type": "object",
            "properties": {
              "customer_id": { "type": "string" }
            },
            "required": ["customer_id"],
            "additionalProperties": false
          }
        }
      ]
    },
    {
      "type": "tool_search"
    }
  ]
}
```

A namespace can mix deferred and nondeferred tools. Tools without `defer_loading: true` are callable immediately. Deferred tools in the same namespace are loaded through tool search.

## Choose a tool search type

Tool search supports two execution types:

- **Hosted tool search**: Azure OpenAI searches the deferred tools that you declare in the request and returns the loaded subset in the same response.
- **Client-executed tool search**: The model emits a `tool_search_call`. Your application performs the lookup and returns a matching `tool_search_output`.

Start with hosted tool search when you know the candidate tools when you create the request. Use client-executed tool search when tool discovery depends on project state, tenant state, or another system that your application controls.

## Use hosted tool search

Hosted tool search is the simplest option when you know the full inventory of functions, namespaces, or MCP servers that the model can search. Declare the inventory, add `{"type": "tool_search"}`, and let Azure OpenAI decide which tools to load.

### Authenticate with Microsoft Entra ID

The following example defines a namespace that contains an immediately available function and a deferred function. The prompt requires the deferred function, so the model searches the namespace before it creates a function call.

# [Python](#tab/python)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

openai = OpenAI(base_url=endpoint, api_key=token_provider)

crm_namespace = {
    "type": "namespace",
    "name": "crm",
    "description": "CRM tools for customer lookup and order management.",
    "tools": [
        {
            "type": "function",
            "name": "get_customer_profile",
            "description": "Fetch a customer profile by customer ID.",
            "parameters": {
                "type": "object",
                "properties": {"customer_id": {"type": "string"}},
                "required": ["customer_id"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "list_open_orders",
            "description": "List open orders for a customer ID.",
            "defer_loading": True,
            "parameters": {
                "type": "object",
                "properties": {"customer_id": {"type": "string"}},
                "required": ["customer_id"],
                "additionalProperties": False,
            },
        },
    ],
}

response = openai.responses.create(
    model="gpt-5.5",
    input="List open orders for customer CUST-12345.",
    tools=[crm_namespace, {"type": "tool_search"}],
    parallel_tool_calls=False,
)

print(response.output)
```

# [JavaScript](#tab/javascript)

```javascript
import OpenAI from "openai";
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: await tokenProvider(),
});

const crmNamespace = {
  type: "namespace",
  name: "crm",
  description: "CRM tools for customer lookup and order management.",
  tools: [
    {
      type: "function",
      name: "get_customer_profile",
      description: "Fetch a customer profile by customer ID.",
      parameters: {
        type: "object",
        properties: { customer_id: { type: "string" } },
        required: ["customer_id"],
        additionalProperties: false,
      },
    },
    {
      type: "function",
      name: "list_open_orders",
      description: "List open orders for a customer ID.",
      defer_loading: true,
      parameters: {
        type: "object",
        properties: { customer_id: { type: "string" } },
        required: ["customer_id"],
        additionalProperties: false,
      },
    },
  ],
};

const response = await openai.responses.create({
  model: "gpt-5.5",
  input: "List open orders for customer CUST-12345.",
  tools: [crmNamespace, { type: "tool_search" }],
  parallel_tool_calls: false,
});

console.log(response.output);
```

---

Reference: [Responses API reference](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1-preview&preserve-view=true)

### Authenticate with an API key

The API key example uses the same namespace and prompt:

# [Python](#tab/python)

```python
import os
from openai import OpenAI

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
openai = OpenAI(
    base_url=endpoint,
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

crm_namespace = {
    "type": "namespace",
    "name": "crm",
    "description": "CRM tools for customer lookup and order management.",
    "tools": [
        {
            "type": "function",
            "name": "get_customer_profile",
            "description": "Fetch a customer profile by customer ID.",
            "parameters": {
                "type": "object",
                "properties": {"customer_id": {"type": "string"}},
                "required": ["customer_id"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "list_open_orders",
            "description": "List open orders for a customer ID.",
            "defer_loading": True,
            "parameters": {
                "type": "object",
                "properties": {"customer_id": {"type": "string"}},
                "required": ["customer_id"],
                "additionalProperties": False,
            },
        },
    ],
}

response = openai.responses.create(
    model="gpt-5.5",
    input="List open orders for customer CUST-12345.",
    tools=[crm_namespace, {"type": "tool_search"}],
    parallel_tool_calls=False,
)

print(response.output)
```

# [JavaScript](#tab/javascript)

```javascript
import OpenAI from "openai";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const crmNamespace = {
  type: "namespace",
  name: "crm",
  description: "CRM tools for customer lookup and order management.",
  tools: [
    {
      type: "function",
      name: "get_customer_profile",
      description: "Fetch a customer profile by customer ID.",
      parameters: {
        type: "object",
        properties: { customer_id: { type: "string" } },
        required: ["customer_id"],
        additionalProperties: false,
      },
    },
    {
      type: "function",
      name: "list_open_orders",
      description: "List open orders for a customer ID.",
      defer_loading: true,
      parameters: {
        type: "object",
        properties: { customer_id: { type: "string" } },
        required: ["customer_id"],
        additionalProperties: false,
      },
    },
  ],
};

const response = await openai.responses.create({
  model: "gpt-5.5",
  input: "List open orders for customer CUST-12345.",
  tools: [crmNamespace, { type: "tool_search" }],
  parallel_tool_calls: false,
});

console.log(response.output);
```

---

Reference: [Responses API reference](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1-preview&preserve-view=true)

When the model needs a deferred tool, the response includes two output items before the function call:

- `tool_search_call` records the hosted search step.
- `tool_search_output` contains the loaded subset that becomes callable.

The following example shows a hosted tool search response:

```json
[
  {
    "type": "tool_search_call",
    "execution": "server",
    "call_id": null,
    "status": "completed",
    "arguments": {
      "paths": ["crm"]
    }
  },
  {
    "type": "tool_search_output",
    "execution": "server",
    "call_id": null,
    "status": "completed",
    "tools": [
      {
        "type": "namespace",
        "name": "crm",
        "description": "CRM tools for customer lookup and order management.",
        "tools": [
          {
            "type": "function",
            "name": "list_open_orders",
            "description": "List open orders for a customer ID.",
            "defer_loading": true,
            "parameters": {
              "type": "object",
              "properties": {
                "customer_id": { "type": "string" }
              },
              "required": ["customer_id"],
              "additionalProperties": false
            }
          }
        ]
      }
    ]
  },
  {
    "type": "function_call",
    "name": "list_open_orders",
    "namespace": "crm",
    "call_id": "call_abc123",
    "arguments": "{\"customer_id\":\"CUST-12345\"}"
  }
]
```

In hosted mode, `execution` is `server` and `call_id` is `null`.

For complex tasks, the model can load multiple namespaces or MCP servers in one `tool_search_call`. For example, if a task requires functions from different namespaces, the model can search and load those surfaces together before it creates the function calls.

## Use client-executed tool search

Client-executed tool search gives your application full control over tool discovery. Use it when available tools depend on information that isn't practical to declare in the initial `tools` list.

Configure the `tool_search` tool with `execution: "client"` and a schema for the search arguments that your application expects:

# [Python](#tab/python)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)
openai = OpenAI(base_url=endpoint, api_key=token_provider)

first_response = openai.responses.create(
    model="gpt-5.5",
    input="Find the shipping ETA tool first, then use it for order_42.",
    tools=[
        {
            "type": "tool_search",
            "execution": "client",
            "description": "Find project tools needed to continue the task.",
            "parameters": {
                "type": "object",
                "properties": {"goal": {"type": "string"}},
                "required": ["goal"],
                "additionalProperties": False,
            },
        }
    ],
    parallel_tool_calls=False,
)

search_call = next(
    item for item in first_response.output
    if item.type == "tool_search_call"
)

loaded_tools = [
    {
        "type": "function",
        "name": "get_shipping_eta",
        "description": "Look up shipping ETA details for an order.",
        "defer_loading": True,
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
            "additionalProperties": False,
        },
    }
]

second_response = openai.responses.create(
    model="gpt-5.5",
    input=[
        *first_response.output,
        {
            "type": "tool_search_output",
            "execution": "client",
            "call_id": search_call.call_id,
            "status": "completed",
            "tools": loaded_tools,
        },
    ],
)

print(second_response.output)
```

# [JavaScript](#tab/javascript)

```javascript
import OpenAI from "openai";
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);
const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: await tokenProvider(),
});

const firstResponse = await openai.responses.create({
  model: "gpt-5.5",
  input: "Find the shipping ETA tool first, then use it for order_42.",
  tools: [
    {
      type: "tool_search",
      execution: "client",
      description: "Find project tools needed to continue the task.",
      parameters: {
        type: "object",
        properties: { goal: { type: "string" } },
        required: ["goal"],
        additionalProperties: false,
      },
    },
  ],
  parallel_tool_calls: false,
});

const searchCall = firstResponse.output.find(
  (item) => item.type === "tool_search_call"
);
if (!searchCall) {
  throw new Error("The response didn't include a tool_search_call item.");
}

const loadedTools = [
  {
    type: "function",
    name: "get_shipping_eta",
    description: "Look up shipping ETA details for an order.",
    defer_loading: true,
    parameters: {
      type: "object",
      properties: { order_id: { type: "string" } },
      required: ["order_id"],
      additionalProperties: false,
    },
  },
];

const secondResponse = await openai.responses.create({
  model: "gpt-5.5",
  input: [
    ...firstResponse.output,
    {
      type: "tool_search_output",
      execution: "client",
      call_id: searchCall.call_id,
      status: "completed",
      tools: loadedTools,
    },
  ],
});

console.log(secondResponse.output);
```

---

Reference: [Responses API reference](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1-preview&preserve-view=true)

To use API key authentication, replace the Microsoft Entra credential with your API key, as shown in the hosted tool search API key example.

On the first turn, the model emits a `tool_search_call` and stops:

```json
[
  {
    "type": "tool_search_call",
    "execution": "client",
    "call_id": "call_abc123",
    "status": "completed",
    "arguments": {
      "goal": "Find the shipping ETA tool for order_42."
    }
  }
]
```

Your application performs the search and returns a `tool_search_output` that contains the tools to load:

```json
[
  {
    "type": "tool_search_output",
    "execution": "client",
    "call_id": "call_abc123",
    "status": "completed",
    "tools": [
      {
        "type": "function",
        "name": "get_shipping_eta",
        "description": "Look up shipping ETA details for an order.",
        "defer_loading": true,
        "parameters": {
          "type": "object",
          "properties": {
            "order_id": { "type": "string" }
          },
          "required": ["order_id"],
          "additionalProperties": false
        }
      }
    ]
  }
]
```

On the next turn, the loaded tool is callable like a normal function:

```json
[
  {
    "type": "function_call",
    "name": "get_shipping_eta",
    "namespace": "get_shipping_eta",
    "call_id": "call_xyz456",
    "arguments": "{\"order_id\":\"order_42\"}"
  }
]
```

In client mode, `execution` is `client` and `call_id` is defined. Echo the same `call_id` from `tool_search_call` in the corresponding `tool_search_output`.

## Apply advanced usage patterns

Use the following patterns to improve discovery quality and control how tools are added to the context.

### Keep namespace descriptions clear

Write concise namespace descriptions that describe the use case. The model uses this description to decide when to load functions from the namespace. Put richer detail in the deferred function descriptions, which load only when needed.

### Understand what gets loaded

The `tool_search_output.tools` array contains the tools that the model dynamically loads. The model can call these tools in later turns, so client mode doesn't need to load the same tool again across turns. Tools that aren't in this array aren't available to the model.

To disable a loaded tool, remove it from the `tool_search_output` item where you define the loaded tool set. Changing the loaded tool set breaks the model's cache from that point forward.

### Use advanced injection patterns

Most integrations declare tools in the request's `tools` parameter. Client-executed tool search also supports advanced patterns where your application returns tools that weren't present in the original request. Validate returned schemas carefully, and expose only trusted tool definitions.

### Preserve caching

Both hosted and client-executed tool search load tools at the end of the model's context window. This placement preserves the model's cache between requests, which can lower costs and improve speed.

### Add tools at a specific point in the input

Use an `additional_tools` input item to make tools available at a specific point in a conversation. This pattern is useful when your application loads tools outside the normal tool search flow or needs to preserve the ordering of tools added during a previous response.

Set `role` to `developer` and include the tools in the item's `tools` array:

```json
{
  "type": "additional_tools",
  "role": "developer",
  "tools": [
    {
      "type": "function",
      "name": "get_customer",
      "description": "Look up a customer by ID.",
      "parameters": {
        "type": "object",
        "properties": {
          "customer_id": { "type": "string" }
        },
        "required": ["customer_id"],
        "additionalProperties": false
      }
    }
  ]
}
```

Tools in an `additional_tools` item become available only after that item appears in the input. When you manually send conversation items in later requests, preserve the item's position so the model sees the same tools at the same point in the conversation.

## Troubleshoot tool search

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| The model doesn't search for a deferred tool. | The namespace, MCP server, or function description doesn't match the task. | Rewrite the description to state the surface's purpose and the tasks it supports. |
| Hosted search doesn't load an expected function. | The function isn't marked with `defer_loading: true`, or its parent surface is unclear. | Add `defer_loading: true` and improve the namespace or MCP server description. |
| Client-executed search can't continue. | The `tool_search_output.call_id` doesn't match the preceding `tool_search_call.call_id`. | Echo the same `call_id` in the output item. |
| A dynamically loaded tool isn't callable. | The tool wasn't included in `tool_search_output.tools`. | Return the complete, trusted tool definition in the output array. |
| Prompt caching stops at a tool update. | The loaded tool set or an earlier item in the context changed. | Keep prior items stable and append newly loaded tools at the end of the context. |

## Related content

- [Use the Azure OpenAI Responses API](../how-to/responses.md)
- [Use function calling with Azure OpenAI](../how-to/function-calling.md)
- [Web search with the Responses API](../how-to/web-search.md)
