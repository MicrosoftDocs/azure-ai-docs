---
title: Include file
description: Include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/20/2026
ms.custom: include, classic-and-new
---

Use the Azure OpenAI Responses API to generate stateful, multi-turn responses. It brings together capabilities from chat completions and the Assistants API in one unified experience. The Responses API also supports the `computer-use-preview` model that powers [Computer use](../../../foundry-classic/openai/how-to/computer-use.md).

## Prerequisites

- A deployed Azure OpenAI model.
- An authentication method:
  - API key (for example, `AZURE_OPENAI_API_KEY`), or
  - Microsoft Entra ID (recommended).
- Install the client library for your language:
  - **Python**: `pip install openai azure-identity`
  - **.NET**: `dotnet add package OpenAI` and `dotnet add package Azure.Identity`
  - **JavaScript/TypeScript**: `npm install openai @azure/identity`
  - **Java**: Add `com.openai:openai-java` and `com.azure:azure-identity` to your project.
- For REST examples, set `AZURE_OPENAI_API_KEY` (API key flow) or `AZURE_OPENAI_AUTH_TOKEN` (Microsoft Entra ID flow).

## Generate a text response

Generate a simple text response using the Responses API. Replace `YOUR-RESOURCE-NAME` and `MODEL_NAME` with your deployment values.

# [Python](#tab/python)
```python
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# API key authentication
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)
response = client.responses.create(
    model="MODEL_NAME",
    input="This is a test."
)
print(response.model_dump_json(indent=2))

# Microsoft Entra ID authentication (recommended)

    DefaultAzureCredential(), "https://ai.azure.com/.default"
)
client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider,
)
response = client.responses.create(
    model="MODEL_NAME",
    input="This is a test."
)
print(response.model_dump_json(indent=2))
```

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using Azure.Identity;
using OpenAI.Responses;
using System.ClientModel.Primitives;

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

// API key authentication
ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

// Microsoft Entra ID authentication (recommended)
BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");
ResponsesClient openAIClientEntra = new(
    authenticationPolicy: tokenPolicy,
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    Input = { ResponseItem.CreateUserMessageItem("This is a test.") }
};
ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)
```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";

// API key authentication
const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});
const response = await openai.responses.create({
  model: "MODEL_NAME",
  input: "This is a test."
});
console.log(response.output_text);

// Microsoft Entra ID authentication (recommended)
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);
const openaiEntra = new OpenAI({
  baseURL: endpoint,
  apiKey: await tokenProvider(),
});
const responseEntra = await openaiEntra.responses.create({
  model: "MODEL_NAME",
  input: "This is a test."
});
console.log(responseEntra.output_text);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

// API key authentication
OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

// Microsoft Entra ID authentication (recommended)
OpenAIClient openAIClientEntra = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
            new DefaultAzureCredentialBuilder().build(),
            "https://ai.azure.com/.default")))
    .build();

ResponseCreateParams params = ResponseCreateParams.builder()
    .model("MODEL_NAME")
    .input("This is a test.")
    .build();
Response response = openAIClient.responses().create(params);
System.out.println(response.outputText());
```

# [REST](#tab/rest)
### Microsoft Entra ID
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "MODEL_NAME",
     "input": "This is a test."
    }'
```
### API Key
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "MODEL_NAME",
     "input": "This is a test."
    }'
```

# [Output](#tab/output)
```json
{
  "id": "resp_67cb32528d6881909eb2859a55e18a85",
  "created_at": 1741369938.0,
  "output_text": "Great! How can I help you today?",
  ...
}
```
---

## Retrieve a response

Retrieve a response by its ID from a previous Responses API call.

# [Python](#tab/python)
```python
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# API key authentication
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)
response = client.responses.retrieve("<response_id>")
print(response.model_dump_json(indent=2))

# Microsoft Entra ID authentication
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)
client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider,
)
response = client.responses.retrieve("<response_id>")
print(response.model_dump_json(indent=2))
```

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using Azure.Identity;
using OpenAI.Responses;

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

// API key authentication
ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

// Microsoft Entra ID authentication
BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");
ResponsesClient openAIClientEntra = new(
    authenticationPolicy: tokenPolicy,
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

string responseId = "<response_id>";
ResponseResult response = await openAIClient.GetResponseAsync(responseId);
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)
```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";

// API key authentication
const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});
const response = await openai.responses.retrieve("<response_id>");
console.log(response.output_text);

// Microsoft Entra ID authentication
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);
const openaiEntra = new OpenAI({
  baseURL: endpoint,
  apiKey: await tokenProvider(),
});
const responseEntra = await openaiEntra.responses.retrieve("<response_id>");
console.log(responseEntra.output_text);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

// API key authentication
OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

// Microsoft Entra ID authentication
OpenAIClient openAIClientEntra = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
            new DefaultAzureCredentialBuilder().build(),
            "https://ai.azure.com/.default")))
    .build();

Response response = openAIClient.responses().retrieve("<response_id>");
System.out.println(response.outputText());
```

# [REST](#tab/rest)
### Microsoft Entra ID
```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
```
### API Key
```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id> \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```

# [Output](#tab/output)
```json
{
  "id": "resp_67cb61fa3a448190bcf2c42d96f0d1a8",
  "output_text": "Hello! How can I assist you today?",
  ...
}
```
---

## Delete a response

By default, response data is retained for 30 days. Delete a stored response by ID.

# [Python](#tab/python)
```python
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# API key authentication
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)
response = client.responses.delete("<response_id>")
print(response)

# Microsoft Entra ID authentication
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)
client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider,
)
response = client.responses.delete("<response_id>")
print(response)
```

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using Azure.Identity;
using OpenAI.Responses;

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

// API key authentication
ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

// Microsoft Entra ID authentication
BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");
ResponsesClient openAIClientEntra = new(
    authenticationPolicy: tokenPolicy,
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

string responseId = "<response_id>";
var result = await openAIClient.DeleteResponseAsync(responseId);
Console.WriteLine(result); // result.Deleted == true if successful
```

# [JavaScript](#tab/javascript)
```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";

// API key authentication
const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});
const result = await openai.responses.delete("<response_id>");
console.log(result);

// Microsoft Entra ID authentication
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);
const openaiEntra = new OpenAI({
  baseURL: endpoint,
  apiKey: await tokenProvider(),
});
const resultEntra = await openaiEntra.responses.delete("<response_id>");
console.log(resultEntra);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

// API key authentication
OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

// Microsoft Entra ID authentication
OpenAIClient openAIClientEntra = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
            new DefaultAzureCredentialBuilder().build(),
            "https://ai.azure.com/.default")))
    .build();

Response result = openAIClient.responses().delete("<response_id>");
System.out.println(result);
```

# [REST](#tab/rest)
### Microsoft Entra ID
```bash
curl -X DELETE https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
```
### API Key
```bash
curl -X DELETE https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id> \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```
---

## Chaining responses together

Chain turns by passing the previous response ID to `previous_response_id`.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

first_response = client.responses.create(
    model="MODEL_NAME",
    input="Define catastrophic forgetting."
)

second_response = client.responses.create(
    model="MODEL_NAME",
    previous_response_id=first_response.id,
    input="Explain it for a college freshman."
)

print(second_response.output_text)
```

# [JavaScript](#tab/javascript)
```javascript
import { OpenAI } from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const firstResponse = await client.responses.create({
  model: "MODEL_NAME",
  input: "Define catastrophic forgetting."
});

const secondResponse = await client.responses.create({
  model: "MODEL_NAME",
  previous_response_id: firstResponse.id,
  input: "Explain it for a college freshman."
});

console.log(secondResponse.output_text);
```

# [REST](#tab/rest)
```bash
# First turn
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": "Define catastrophic forgetting."
  }'

# Follow-up turn using previous_response_id from the first call
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "previous_response_id": "<response_id>",
    "input": "Explain it for a college freshman."
  }'
```
---

### Chaining responses manually

Alternatively, you can manually carry forward output items in the next request.

```python
import os
from openai import OpenAI

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)

inputs = [{"type": "message", "role": "user", "content": "Define and explain the concept of catastrophic forgetting?"}] 
  
response = client.responses.create(  
    model="gpt-4o",  # replace with your model deployment name  
    input=inputs  
)  
  
inputs += response.output

inputs.append({"role": "user", "type": "message", "content": "Explain this at a level that could be understood by a college freshman"}) 
               

second_response = client.responses.create(
  model="MODEL_NAME",
    input=inputs
)

print(second_response.model_dump_json(indent=2))
```

## Compact a Response

Compaction reduces the input context while preserving essential state for later turns.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

compacted = client.responses.compact(
  model="MODEL_NAME",
  input=[
    {"role": "user", "content": "Create a simple landing page for a dog cafe."},
    {
      "id": "msg_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [{"type": "output_text", "text": "..."}],
    },
  ]
)

follow_up = client.responses.create(
  model="MODEL_NAME",
  input=[*compacted.output, {"role": "user", "content": "Add a booking form."}]
)
print(follow_up.output_text)
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/compact \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": [
      {"role": "user", "content": "Create a simple landing page for a dog cafe."},
      {
      "id": "msg_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [{"type": "output_text", "text": "..."}]
      }
    ]
    }'
```
---

### Compact using items returned

You can compact all items returned from previous requests like reasoning, message, function call, etc.

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/compact \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
        "model": "MODEL_NAME",
        "input": [
          {
            "role"   : "user",
            "content": "Create a simple landing page for a dog petting café."
          },
          {
            "id": "msg_001",
            "type": "message",
            "status": "completed",
            "content": [
              {
                "type": "output_text",
                "annotations": [],
                "logprobs": [],
                "text": "Below is a single file, ready-to-use landing page for a dog petting café:..."
              }
            ],
            "role": "assistant"
          }
        ]
    }'
```

```python
# Use the compacted output as input for the next turn.
next_response = client.responses.create(
  model="MODEL_NAME",
  input=[*compacted.output, {"role": "user", "content": "Add opening hours."}],
)
print(next_response.output_text)
```

### Compact using previous response ID

You can also compact using a previous response ID.

```python
initial_response = client.responses.create(
  model="MODEL_NAME",
  input="What is the size of France?"
)

compacted_response = client.responses.compact(
  model="MODEL_NAME",
  previous_response_id=initial_response.id
)

follow_up_response = client.responses.create(
  model="MODEL_NAME",
  input=[
    *compacted_response.output,
    {"role": "user", "content": "What is the capital?"}
  ]
)
print(follow_up_response.output_text)
```

### Server-side compaction

You can also use server-side compaction directly in Responses (`POST /responses` or `client.responses.create`) by setting `context_management` with a `compact_threshold`.

* When the output token count crosses the configured threshold, the Responses API automatically runs compaction.
* In this mode, you do not need to call `/responses/compact` separately.
* The response includes an encrypted compaction item.
* Server-side compaction will work when you set store=false on your Responses create requests.

The compaction item carries forward the essential prior state and reasoning into the next turn using fewer tokens. It is opaque and not intended to be human-readable.

If you are using stateless input-array chaining, append output items as usual. If you are using `previous_response_id`, pass only the new user message on each turn. In both patterns, the compaction item carries the context needed for the next window.

> [!TIP]
> After appending output items to the previous input items, you can drop items that came before the most recent compaction item to keep requests smaller and reduce long-tail latency. The latest compaction item carries the necessary context to continue the conversation. If you use `previous_response_id` chaining, do not manually prune.

#### Flow

1. Call `responses` as usual. Add `context_management` with `compact_threshold` to enable server-side compaction.
2. If the output crosses the threshold, the service triggers compaction, emits a compaction item in the output stream, and prunes the context before continuing inference.
3. Continue the conversation using one of these patterns:
   1. Stateless input-array chaining: append output items, including compaction items, to the next input array.
   2. `previous_response_id` chaining: pass only the new user message on each turn and carry the latest response ID forward.

#### Example

```python
conversation = [
  {
    "type": "message",
    "role": "user",
    "content": "Let's begin a long coding task.",
  }
]

while keep_going:
  response = client.responses.create(
    model="MODEL_NAME",
    input=conversation,
    store=False,
    context_management=[{"type": "compaction", "compact_threshold": 200000}],
  )

  conversation.append(
    {
      "type": "message",
       "role": "user",
      "content": get_next_user_input(),
    }
  )
```

## Streaming

> [!NOTE]
> During streaming, the Responses API might return an error event ( `500`, `429`, and similar errors) if the service encounters an error, such as token limits or parsing problems. Applications should detect this event and gracefully stop or restart streaming. You aren't charged for tokens generated during failed streaming responses.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

stream = client.responses.create(
    model="MODEL_NAME",
    input="Summarize Azure OpenAI Responses API in one sentence.",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
```

# [JavaScript](#tab/javascript)
```javascript
import { OpenAI } from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const stream = await client.responses.create({
  model: "MODEL_NAME",
  input: "Summarize Azure OpenAI Responses API in one sentence.",
  stream: true,
});

for await (const event of stream) {
  if (event.type === "response.output_text.delta") {
    process.stdout.write(event.delta);
  }
}
```

# [REST](#tab/rest)
```bash
curl -N -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": "Summarize Azure OpenAI Responses API in one sentence.",
    "stream": true
  }'
```
---

## Function calling

The Responses API supports function calling.

# [Python](#tab/python)
```python
import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.responses.create(
    model="MODEL_NAME",
    tools=[
        {
            "type": "function",
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
            },
        }
    ],
    input="What is the weather in San Francisco?",
)

tool_outputs = []
for item in response.output:
    if item.type == "function_call" and item.name == "get_weather":
        args = json.loads(item.arguments)
        weather = {"location": args["location"], "temperature": "70 F"}
        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(weather),
            }
        )

final_response = client.responses.create(
    model="MODEL_NAME",
    previous_response_id=response.id,
    input=tool_outputs,
)

print(final_response.output_text)
```

# [JavaScript](#tab/javascript)
```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const response = await client.responses.create({
  model: "MODEL_NAME",
  tools: [
    {
      type: "function",
      name: "get_weather",
      description: "Get weather for a location",
      parameters: {
        type: "object",
        properties: { location: { type: "string" } },
        required: ["location"],
      },
    },
  ],
  input: "What is the weather in San Francisco?",
});

const toolOutputs = [];
for (const item of response.output ?? []) {
  if (item.type === "function_call" && item.name === "get_weather") {
    const args = JSON.parse(item.arguments);
    toolOutputs.push({
      type: "function_call_output",
      call_id: item.call_id,
      output: JSON.stringify({ location: args.location, temperature: "70 F" }),
    });
  }
}

const finalResponse = await client.responses.create({
  model: "MODEL_NAME",
  previous_response_id: response.id,
  input: toolOutputs,
});

console.log(finalResponse.output_text);
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "tools": [
      {
        "type": "function",
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
          "type": "object",
          "properties": {"location": {"type": "string"}},
          "required": ["location"]
        }
      }
    ],
    "input": "What is the weather in San Francisco?"
  }'
```
---

## Code Interpreter

The Code Interpreter tool enables models to write and execute Python code in a secure, sandboxed environment. It supports a range of advanced tasks, including:

* Processing files with varied data formats and structures
* Generating files that include data and visualizations (for example, graphs)
* Iteratively writing and running code to solve problems—models can debug and retry code until successful
* Enhancing visual reasoning in supported models (for example, o3, o4-mini) by enabling image transformations such as cropping, zooming, and rotation
* This tool is especially useful for scenarios involving data analysis, mathematical computation, and code generation.

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
        "model": "MODEL_NAME",
        "tools": [
            { "type": "code_interpreter", "container": {"type": "auto"} }
        ],
        "instructions": "You are a personal math tutor. When asked a math question, write and run code using the python tool to answer the question.",
        "input": "I need to solve the equation 3x + 11 = 14. Can you help me?"
    }'
```

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.responses.create(
    model="MODEL_NAME",
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
    instructions="You are a math tutor. Write and run Python code to solve math problems.",
    input="Solve 3x + 11 = 14."
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)
```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const response = await client.responses.create({
  model: "MODEL_NAME",
  tools: [{ type: "code_interpreter", container: { type: "auto" } }],
  instructions: "You are a math tutor. Write and run Python code to solve math problems.",
  input: "Solve 3x + 11 = 14.",
});

console.log(response.output_text);
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "tools": [{"type": "code_interpreter", "container": {"type": "auto"}}],
    "instructions": "You are a math tutor. Write and run Python code to solve math problems.",
    "input": "Solve 3x + 11 = 14."
  }'
```
---

### Containers

> [!IMPORTANT]
> Code Interpreter has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token based fees for Azure OpenAI usage. If your Responses API calls Code Interpreter simultaneously in two different threads, two code interpreter sessions are created. Each session is active by default for 1 hour with an idle timeout of 20 minutes.

The Code Interpreter tool requires a container—a fully sandboxed virtual machine where the model can execute Python code. Containers can include uploaded files or files generated during execution.

To create a container, specify `"container": { "type": "auto", "file_ids": ["file-1", "file-2"] }` in the tool configuration when creating a new Response object. This automatically creates a new container or reuses an active one from a previous code_interpreter_call in the model’s context. The `code_interpreter_call` in the output of the APIwill contain the `container_id` that was generated. This container expires if it is not used for 20 minutes.

### File inputs and outputs

When running Code Interpreter, the model can create its own files. For example, if you ask it to construct a plot, or create a CSV, it creates these images directly on your container. It will cite these files in the annotations of its next message.

Any files in the model input get automatically uploaded to the container. You do not have to explicitly upload it to the container.

### Supported Files

|File format|MIME type|
|---|---|
|`.c`|text/x-c|
|`.cs`|text/x-csharp|
|`.cpp`|text/x-c++|
|`.csv`|text/csv|
|`.doc`|application/msword|
|`.docx`|application/vnd.openxmlformats-officedocument.wordprocessingml.document|
|`.html`|text/html|
|`.java`|text/x-java|
|`.json`|application/json|
|`.md`|text/markdown|
|`.pdf`|application/pdf|
|`.php`|text/x-php|
|`.pptx`|application/vnd.openxmlformats-officedocument.presentationml.presentation|
|`.py`|text/x-python|
|`.py`|text/x-script.python|
|`.rb`|text/x-ruby|
|`.tex`|text/x-tex|
|`.txt`|text/plain|
|`.css`|text/css|
|`.js`|text/JavaScript|
|`.sh`|application/x-sh|
|`.ts`|application/TypeScript|
|`.csv`|application/csv|
|`.jpeg`|image/jpeg|
|`.jpg`|image/jpeg|
|`.gif`|image/gif|
|`.pkl`|application/octet-stream|
|`.png`|image/png|
|`.tar`|application/x-tar|
|`.xlsx`|application/vnd.openxmlformats-officedocument.spreadsheetml.sheet|
|`.xml`|application/xml or "text/xml"|
|`.zip`|application/zip|

## List input items

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

items = client.responses.input_items.list("<response_id>")
print(items.model_dump_json(indent=2))
```

# [REST](#tab/rest)
```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id>/input_items \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```

# [Output](#tab/output)
```json
{
  "object": "list",
  "data": [
    {
      "id": "msg_...",
      "type": "message",
      "role": "user",
      "content": [{"type": "input_text", "text": "This is a test."}]
    }
  ]
}
```
---

## Image input

For vision-enabled models, supported image formats are PNG, JPEG, and WebP.

### Image URL

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.responses.create(
    model="MODEL_NAME",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What is in this image?"},
                {"type": "input_image", "image_url": "<image_url>"}
            ]
        }
    ]
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)
```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const response = await client.responses.create({
  model: "MODEL_NAME",
  input: [
    {
      role: "user",
      content: [
        { type: "input_text", text: "What is in this image?" },
        { type: "input_image", image_url: "<image_url>" }
      ],
    },
  ],
});

console.log(response.output_text);
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": [
      {
        "role": "user",
        "content": [
          {"type": "input_text", "text": "What is in this image?"},
          {"type": "input_image", "image_url": "<image_url>"}
        ]
      }
    ]
  }'
```
---

### Base64-encoded image

# [Python](#tab/python)
```python
import base64
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

with open("path_to_your_image.jpg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

response = client.responses.create(
    model="MODEL_NAME",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What is in this image?"},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"}
            ]
        }
    ]
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)
```javascript
import { readFileSync } from "node:fs";
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const base64Image = readFileSync("path_to_your_image.jpg").toString("base64");

const response = await client.responses.create({
  model: "MODEL_NAME",
  input: [
    {
      role: "user",
      content: [
        { type: "input_text", text: "What is in this image?" },
        { type: "input_image", image_url: `data:image/jpeg;base64,${base64Image}` }
      ],
    },
  ],
});

console.log(response.output_text);
```
---

## File input

Models with vision capabilities support PDF input. PDF files can be provided either as Base64-encoded data or as file IDs. To help models interpret PDF content, both the extracted text and an image of each page are included in the model’s context. This is useful when key information is conveyed through diagrams or non-textual content.

> [!NOTE]
> - All extracted text and images are put into the model's context. Make sure you understand the pricing and token usage implications of using PDFs as input.
> - In a single API request, the size of content uploaded across multiple inputs (files) should be within the model's context length.
> - Only models that support both text and image inputs can accept PDF files as input.
> - A `purpose` of `user_data` is currently not supported. As a temporary workaround you will need to set purpose to `assistants`.

### Convert PDF to Base64 and analyze

# [Python](#tab/python)
```python
import base64
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

with open("PDF-FILE-NAME.pdf", "rb") as f:
    base64_string = base64.b64encode(f.read()).decode("utf-8")

response = client.responses.create(
    model="MODEL_NAME",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "filename": "PDF-FILE-NAME.pdf",
                    "file_data": f"data:application/pdf;base64,{base64_string}",
                },
                {"type": "input_text", "text": "Summarize this PDF."},
            ],
        },
    ]
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)
```javascript
import { readFileSync } from "node:fs";
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const base64Pdf = readFileSync("PDF-FILE-NAME.pdf").toString("base64");

const response = await client.responses.create({
  model: "MODEL_NAME",
  input: [
    {
      role: "user",
      content: [
        {
          type: "input_file",
          filename: "PDF-FILE-NAME.pdf",
          file_data: `data:application/pdf;base64,${base64Pdf}`,
        },
        { type: "input_text", text: "Summarize this PDF." },
      ],
    },
  ],
});

console.log(response.output_text);
```
---

### Upload PDF and analyze

Upload the PDF file with `purpose="assistants"`. A `purpose` of `user_data` isn't currently supported.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

file = client.files.create(
    file=open("nucleus_sampling.pdf", "rb"),
    purpose="assistants"
)

response = client.responses.create(
    model="MODEL_NAME",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_file", "file_id": file.id},
                {"type": "input_text", "text": "Summarize this PDF."},
            ],
        },
    ]
)

print(response.output_text)
```

# [REST](#tab/rest)
```bash
# Upload the PDF
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/files \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F purpose="assistants" \
  -F file="@your_file.pdf"

# Use the returned file ID with Responses
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": [
      {
        "role": "user",
        "content": [
          {"type": "input_file", "file_id": "<file_id>"},
          {"type": "input_text", "text": "Summarize this PDF."}
        ]
      }
    ]
  }'
```
---

## Using remote MCP servers

You can extend the capabilities of your model by connecting it to tools hosted on remote Model Context Protocol (MCP) servers. These servers are maintained by developers and organizations and expose tools that can be accessed by MCP-compatible clients, such as the Responses API.

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is an open standard that defines how applications provide tools and contextual data to large language models (LLMs). It enables consistent, scalable integration of external tools into model workflows.

The following example shows how to use a remote MCP server to query information about an Azure REST API repository. The model retrieves and reasons over repository content in real time.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.responses.create(
    model="MODEL_NAME",
    tools=[
        {
            "type": "mcp",
            "server_label": "github",
            "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
            "require_approval": "never"
        }
    ],
    input="What transport protocols are supported in the 2025-03-26 version of the MCP spec?"
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)
```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const response = await client.responses.create({
  model: "MODEL_NAME",
  tools: [
    {
      type: "mcp",
      server_label: "github",
      server_url: "https://contoso.com/Azure/azure-rest-api-specs",
      require_approval: "never",
    },
  ],
  input: "What is this repo in 100 words?",
});

console.log(response.output_text);
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "tools": [
      {
        "type": "mcp",
        "server_label": "github",
        "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
        "require_approval": "never"
      }
    ],
    "input": "What is this repo in 100 words?"
  }'
```
---

The MCP tool works only in the Responses API, and is available across all newer models (gpt-4o, gpt-4.1, and our reasoning models). When you're using the MCP tool, you only pay for tokens used when importing tool definitions or making tool calls—there are no additional fees involved.

### Approvals

By default, the Responses API requires explicit approval before any data is shared with a remote MCP server. This approval step helps ensure transparency and gives you control over what information is sent externally.

We recommend reviewing all data being shared with remote MCP servers and optionally logging it for auditing purposes.

When an approval is required, the model returns a `mcp_approval_request` item in the response output. This object contains the details of the pending request and allows you to inspect or modify the data before proceeding.

```json
{
  "id": "mcpr_682bd9cd428c8198b170dc6b549d66fc016e86a03f4cc828",
  "type": "mcp_approval_request",
  "arguments": {},
  "name": "fetch_azure_rest_api_docs",
  "server_label": "github"
}
```

To proceed with the remote MCP call, you must respond to the approval request by creating a new response object that includes an mcp_approval_response item. This object confirms your intent to allow the model to send the specified data to the remote MCP server.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.responses.create(
    model="MODEL_NAME",
    tools=[
        {
            "type": "mcp",
            "server_label": "github",
            "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
            "require_approval": "never"
        }
    ],
    previous_response_id="<previous_response_id>",
    input=[
        {
            "type": "mcp_approval_response",
            "approve": True,
            "approval_request_id": "<approval_request_id>"
        }
    ]
)

print(response.output_text)
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "tools": [
      {
        "type": "mcp",
        "server_label": "github",
        "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
        "require_approval": "never"
      }
    ],
    "previous_response_id": "<previous_response_id>",
    "input": [
      {
        "type": "mcp_approval_response",
        "approve": true,
        "approval_request_id": "<approval_request_id>"
      }
    ]
  }'
```
---

### Authentication

> [!IMPORTANT]
> - The MCP client within the Responses API requires TLS 1.2 or greater.
> - mutual TLS (mTLS) is currently not supported.
> - [Azure service tags](/azure/virtual-network/service-tags-overview) are currently not supported for MCP client traffic.

Unlike the GitHub MCP server, most remote MCP servers require authentication. The MCP tool in the Responses API supports custom headers, allowing you to securely connect to these servers using the authentication scheme they require.

You can specify headers such as API keys, OAuth access tokens, or other credentials directly in your request. The most commonly used header is the `Authorization` header.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.responses.create(
    model="MODEL_NAME",
    input="What is this repo in 100 words?",
    tools=[
        {
            "type": "mcp",
            "server_label": "github",
            "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
            "headers": {"Authorization": "Bearer $YOUR_MCP_TOKEN"}
        }
    ]
)

print(response.output_text)
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": "What is this repo in 100 words?",
    "tools": [
      {
        "type": "mcp",
        "server_label": "github",
        "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
        "headers": {"Authorization": "Bearer $YOUR_MCP_TOKEN"}
      }
    ]
  }'
```
---

## Background tasks

Background mode lets you run long-running tasks asynchronously with reasoning models such as `o3` and `o1-pro`. It's useful for complex tasks that can take several minutes to complete (for example, Codex- or Deep Research-style agents). When a request is sent with `"background": true`, the task is processed asynchronously, and you poll for its status.

### Start a background task

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.responses.create(
    model="MODEL_NAME",
    input="Write me a very long story.",
    background=True
)

print(response.status)
```

# [JavaScript](#tab/javascript)
```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const response = await client.responses.create({
  model: "MODEL_NAME",
  input: "Write me a very long story.",
  background: true,
});

console.log(response.status);
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": "Write me a very long story.",
    "background": true
  }'
```
---

### Poll for completion

Continue polling while the status is `queued` or `in_progress`. Once the response reaches a terminal state, it's available for retrieval.

# [Python](#tab/python)
```python
from time import sleep

while response.status in {"queued", "in_progress"}:
    print(f"Current status: {response.status}")
    sleep(2)
    response = client.responses.retrieve(response.id)

print(f"Final status: {response.status}\nOutput:\n{response.output_text}")
```

# [REST](#tab/rest)
```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id> \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```
---

### Cancel a background task

Cancel an in-progress background task with the `cancel` endpoint. Canceling is idempotent—subsequent calls return the final response object.

# [Python](#tab/python)
```python
response = client.responses.cancel("<response_id>")
print(response.status)
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id>/cancel \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```
---

To stream a background response, set both `background` and `stream` to `true`. This pattern lets you resume streaming if the connection drops. Track your position with the `sequence_number` from each event.

# [Python](#tab/python)
```python
stream = client.responses.create(
    model="MODEL_NAME",
    input="Write me a very long story.",
    background=True,
    stream=True,
)

cursor = None
for event in stream:
    print(event)
    cursor = event["sequence_number"]
```

# [REST](#tab/rest)
```bash
curl -N -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": "Write me a very long story.",
    "background": true,
    "stream": true
  }'
```
---

> Background responses currently have a higher time-to-first-token latency than synchronous responses. Improvements are underway to reduce this gap.

### Limitations

* Background mode requires `store=true`. Stateless requests are not supported.
* You can only resume streaming if the original request included `stream=true`.
* To cancel a synchronous response, terminate the connection directly.

### Resume streaming from a specific point

```bash
curl -N -X GET "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id>?stream=true&starting_after=42" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```

## Encrypted Reasoning Items

When you use the Responses API in stateless mode (`store=false`), you must still preserve reasoning context across conversation turns. To do this, include encrypted reasoning items in your requests.

To retain reasoning items across turns, add `reasoning.encrypted_content` to the `include` parameter. The response then contains an encrypted version of the reasoning trace, which you can pass to future requests.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.responses.create(
    model="MODEL_NAME",
    reasoning={"effort": "medium"},
    input="What is the weather like today?",
    tools=[
        # Replace with your function or tool definitions.
    ],
    include=["reasoning.encrypted_content"],
    store=False,
)

print(response.output_text)
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "reasoning": {"effort": "medium"},
    "input": "What is the weather like today?",
    "tools": [],
    "include": ["reasoning.encrypted_content"],
    "store": false
  }'
```
---

The Responses API enables image generation as part of conversations and multi-step workflows. It supports image inputs and outputs within context, and it includes built-in tools for generating and editing images.

Compared to the standalone Image API, the Responses API offers two advantages:

* **Streaming**: Display partial image outputs during generation to improve perceived latency.
* **Flexible inputs**: Accept image file IDs as inputs in addition to raw image bytes.

> [!NOTE]
> The image generation tool in the Responses API is supported by `gpt-image-1`-series models, and you can call it from a set of compatible chat and reasoning models. For the current list of supported orchestration models, see the [Model support](#model-support) section later in this article.
>
> The image generation tool doesn't currently support streaming mode. To stream partial images, call the [image generation API](../how-to/dall-e.md) directly outside of the Responses API.

Use the Responses API to build conversational image experiences with GPT Image models.

# [Python](#tab/python)
```python
import base64
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider,
    default_headers={
        "x-ms-oai-image-generation-deployment": os.getenv("IMAGE_MODEL_NAME"),
        "api_version": "preview",
    },
)

response = client.responses.create(
    model="MODEL_NAME",
    input="Generate an image of a gray tabby cat hugging an otter with an orange scarf.",
    tools=[{"type": "image_generation"}],
)

image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    with open("otter.png", "wb") as f:
        f.write(base64.b64decode(image_data[0]))
```

# [JavaScript](#tab/javascript)
```javascript
import fs from "fs";
import OpenAI from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: await tokenProvider(),
  defaultHeaders: {
    "x-ms-oai-image-generation-deployment": process.env.IMAGE_MODEL_NAME,
    api_version: "preview",
  },
});

const response = await client.responses.create({
  model: "MODEL_NAME",
  input: "Generate an image of a gray tabby cat hugging an otter with an orange scarf.",
  tools: [{ type: "image_generation" }],
});

const imageBase64 = response.output
  .filter((o) => o.type === "image_generation_call")
  .map((o) => o.result)[0];

if (imageBase64) {
  fs.writeFileSync("otter.png", Buffer.from(imageBase64, "base64"));
}
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "x-ms-oai-image-generation-deployment: $IMAGE_MODEL_NAME" \
  -d '{
    "model": "MODEL_NAME",
    "input": "Generate an image of a gray tabby cat hugging an otter with an orange scarf.",
    "tools": [{ "type": "image_generation" }]
  }'
```
---

## Reasoning models

For examples of how to use reasoning models with the responses API see the [reasoning models guide](../how-to/reasoning.md#reasoning-summary).

## Computer use

Computer use with Playwright has moved to the [dedicated computer use model guide](../../../foundry-classic/openai/how-to/computer-use.md#playwright-integration)

## Responses API

### API support

- The v1 API is required for access to the latest features. For details, see the [API version lifecycle](../api-version-lifecycle.md).

### Region Availability

The responses API is currently available in the following regions:

- australiaeast
- brazilsouth
- canadacentral
- canadaeast  
- eastus
- eastus2
- francecentral
- germanywestcentral
- italynorth
- japaneast
- koreacentral
- northcentralus
- norwayeast
- polandcentral
- southafricanorth
- southcentralus
- southeastasia
- southindia
- spaincentral
- swedencentral
- switzerlandnorth
- uaenorth
- uksouth
- westus
- westus3

### Model support

- `gpt-chat-latest` (Version: `2026-05-05`)
- `gpt-5.5` (Version: `2026-04-24`)
- `gpt-5.4-nano` (Version: `2026-03-17`)
- `gpt-5.4-mini` (Version: `2026-03-17`)
- `gpt-5.4-pro` (Version:`2026-03-05`)
- `gpt-5.4` (Version:`2026-03-05`)
- `gpt-5.3-chat` (Version: `2026-03-03`)
- `gpt-5.3-codex` (Version: `2026-02-24`)
- `gpt-5.2-codex` (Version: `2026-01-14`)
- `gpt-5.2` (Version: `2025-12-11`)
- `gpt-5.2-chat` (Version: `2025-12-11`)
- `gpt-5.2-chat` (Version: `2026-02-10`)
- `gpt-5.1-codex-max` (Version: `2025-12-04`)
- `gpt-5.1` (Version: `2025-11-13`)
- `gpt-5.1-chat` (Version: `2025-11-13`)
- `gpt-5.1-codex` (Version: `2025-11-13`)
- `gpt-5.1-codex-mini` (Version: `2025-11-13`)
- `gpt-5-pro` (Version: `2025-10-06`)
- `gpt-5-codex`  (Version: `2025-09-11`)
- `gpt-5` (Version: `2025-08-07`)
- `gpt-5-mini` (Version: `2025-08-07`)
- `gpt-5-nano` (Version: `2025-08-07`)
- `gpt-5-chat` (Version: `2025-08-07`)
- `gpt-5-chat` (Version: `2025-10-03`)
- `gpt-5-codex` (Version: `2025-09-15`)
- `gpt-4o` (Versions: `2024-11-20`, `2024-08-06`, `2024-05-13`)
- `gpt-4o-mini` (Version: `2024-07-18`)
- `computer-use-preview`
- `gpt-4.1` (Version: `2025-04-14`)
- `gpt-4.1-nano` (Version: `2025-04-14`)
- `gpt-4.1-mini` (Version: `2025-04-14`)
- `gpt-image-1` (Version: `2025-04-15`)
- `gpt-image-1-mini` (Version: `2025-10-06`)
- `gpt-image-1.5` (Version: `2025-12-16`)
- `o1` (Version: `2024-12-17`)
- `o3-mini` (Version: `2025-01-31`)
- `o3` (Version: `2025-04-16`)
- `o4-mini` (Version: `2025-04-16`)

Not every model is available in the regions supported by the responses API. Check the [models page](../../foundry-models/concepts/models-sold-directly-by-azure.md) for model region availability.

> [!NOTE]
> Not currently supported:
> - Image generation using multi-turn editing and streaming.
> - Images can't be uploaded as a file and then referenced as input.
>
> There's a known issue with the following:
> - PDF as an input file [is now supported](#file-input), but setting file upload purpose to `user_data` is not currently supported.
> - Performance issues when background mode is used with streaming. The issue is expected to be resolved soon.

### Reference documentation

- [Responses API reference documentation](../reference-preview-latest.md)

## Troubleshooting

- **401/403**: If you use Microsoft Entra ID, verify your token is scoped for `https://ai.azure.com/.default`. If you use an API key, confirm you're using the correct key for the resource.
- **404**: Confirm `model` matches your deployment name.

## Related content

- [API version lifecycle](../api-version-lifecycle.md)
- [Azure OpenAI REST API reference](../latest.md)
- [Computer use](../../../foundry-classic/openai/how-to/computer-use.md)
