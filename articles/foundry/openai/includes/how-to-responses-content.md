---
title: Include file
description: Include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/20/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
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

## Supported regions

Before you run the examples in this article, confirm that your resource region supports the Responses API. The v1 API is required to access the latest features — for details, see the [API version lifecycle](../api-version-lifecycle.md). The Responses API is currently available in the following regions:

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

## Supported models

The Responses API supports the following models:

- `gpt-chat-latest` (Versions: `2026-05-28`, `2026-05-05`)
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

Not every model is available in every supported region. Check the [models page](../../foundry-models/concepts/models-sold-directly-by-azure.md) for model region availability. For the full set of request and response parameters, see the [Responses API reference documentation](../reference-preview-latest.md).

> [!NOTE]
> Not currently supported:
> - Image generation using multi-turn editing and streaming.
> - Images can't be uploaded as a file and then referenced as input.
>
> There's a known issue with the following:
> - PDF as an input file [is now supported](#file-input), but setting file upload purpose to `user_data` is not currently supported.
> - Performance issues when background mode is used with streaming. Microsoft is working to resolve this issue.

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
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)
client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider(),
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
    InputItems = { ResponseItem.CreateUserMessageItem("This is a test.") }
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

---

### Example response

```json
{
  "id": "resp_67cb32528d6881909eb2859a55e18a85",
  "created_at": 1741369938.0,
  "output_text": "Great! How can I help you today?",
  ...
}
```

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

---

### Example response

```json
{
  "id": "resp_67cb61fa3a448190bcf2c42d96f0d1a8",
  "output_text": "Hello! How can I assist you today?",
  ...
}
```

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

CreateResponseOptions firstOptions = new()
{
    Model = "MODEL_NAME",
    InputItems = { ResponseItem.CreateUserMessageItem("Define and explain the concept of catastrophic forgetting?") }
};
ResponseResult firstResponse = await openAIClient.CreateResponseAsync(firstOptions);
Console.WriteLine(firstResponse.GetOutputText());

CreateResponseOptions secondOptions = new()
{
    Model = "MODEL_NAME",
    PreviousResponseId = firstResponse.Id,
    InputItems = { ResponseItem.CreateUserMessageItem("Explain this at a level that could be understood by a college freshman") }
};
ResponseResult secondResponse = await openAIClient.CreateResponseAsync(secondOptions);
Console.WriteLine(secondResponse.GetOutputText());
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

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Response first = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("Define and explain the concept of catastrophic forgetting?")
        .build());

Response second = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .previousResponseId(first.id())
        .input("Explain this at a level that could be understood by a college freshman.")
        .build());

second.output().stream()
    .flatMap(item -> item.message().stream())
    .flatMap(m -> m.content().stream())
    .flatMap(c -> c.outputText().stream())
    .forEach(t -> System.out.println(t.text()));
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

# [C#](#tab/csharp)
> [!NOTE]
> The .NET SDK doesn't yet provide a strongly typed surface for Response compaction. See the **REST** tab for the call shape, or invoke the protocol method directly with `BinaryContent` JSON.

# [JavaScript](#tab/javascript)
```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const compacted = await client.responses.compact({
  model: "MODEL_NAME",
  input: [
    { role: "user", content: "Create a simple landing page for a dog cafe." },
    {
      id: "msg_001",
      type: "message",
      status: "completed",
      role: "assistant",
      content: [{ type: "output_text", text: "..." }],
    },
  ],
});

const followUp = await client.responses.create({
  model: "MODEL_NAME",
  input: [...compacted.output, { role: "user", content: "Add a booking form." }],
});
console.log(followUp.output_text);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.CompactedResponse;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCompactParams;
import com.openai.models.responses.ResponseCreateParams;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Response initial = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("Create a simple landing page for a dog cafe.")
        .build());

CompactedResponse compacted = openAIClient.responses().compact(
    ResponseCompactParams.builder()
        .model("MODEL_NAME")
        .previousResponseId(initial.id())
        .build());

Response followUp = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .previousResponseId(compacted.id())
        .input("Add a booking form.")
        .build());

System.out.println(followUp.outputText());
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

- When the output token count crosses the configured threshold, the Responses API automatically runs compaction.
- In this mode, you do not need to call `/responses/compact` separately.
- The response includes an encrypted compaction item.
- Server-side compaction will work when you set store=false on your Responses create requests.

The compaction item carries forward the essential prior state and reasoning into the next turn using fewer tokens. It is opaque and not intended to be human-readable.

If you are using stateless input-array chaining, append output items as usual. If you are using `previous_response_id`, pass only the new user message on each turn. In both patterns, the compaction item carries the context needed for the next window.

> [!TIP]
> After appending output items to the previous input items, you can drop items that came before the most recent compaction item to keep requests smaller and reduce long-tail latency. The latest compaction item carries the necessary context to continue the conversation. If you use `previous_response_id` chaining, do not manually prune.

#### Flow

1. Call `responses` as usual. Add `context_management` with `compact_threshold` to enable server-side compaction.
1. If the output crosses the threshold, the service triggers compaction, emits a compaction item in the output stream, and prunes the context before continuing inference.
1. Continue the conversation using one of these patterns:
   1. Stateless input-array chaining: append output items, including compaction items, to the next input array.
   1. `previous_response_id` chaining: pass only the new user message on each turn and carry the latest response ID forward.

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

Stream the response as it's generated by setting `stream=true`. The service emits incremental events you can consume to render output token-by-token.

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
    InputItems = { ResponseItem.CreateUserMessageItem("Summarize Azure OpenAI Responses API in one sentence.") },
    StreamingEnabled = true
};

await foreach (StreamingResponseUpdate update in openAIClient.CreateResponseStreamingAsync(options))
{
    if (update is StreamingResponseOutputTextDeltaUpdate textDelta)
    {
        Console.Write(textDelta.Delta);
    }
    else if (update is StreamingResponseCompletedUpdate completed)
    {
        Console.WriteLine();
        Console.WriteLine($"[done] response id: {completed.Response.Id}");
    }
}
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

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.http.StreamResponse;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseStreamEvent;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

ResponseCreateParams params = ResponseCreateParams.builder()
    .model("MODEL_NAME")
    .input("This is a test")
    .build();

try (StreamResponse<ResponseStreamEvent> stream = openAIClient.responses().createStreaming(params)) {
    stream.stream()
        .flatMap(event -> event.outputTextDelta().stream())
        .forEach(delta -> System.out.print(delta.delta()));
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

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using System.Text.Json;
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

FunctionTool getWeatherTool = ResponseTool.CreateFunctionTool(
    functionName: "get_weather",
    functionParameters: BinaryData.FromBytes("""
        {
          "type": "object",
          "properties": {
            "location": { "type": "string", "description": "The city, e.g. Boston, MA" }
          },
          "required": ["location"]
        }
        """u8.ToArray()),
    strictModeEnabled: false,
    functionDescription: "Get the current weather for a location.");

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems = { ResponseItem.CreateUserMessageItem("What is the weather in San Francisco?") },
    Tools = { getWeatherTool }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);

foreach (ResponseItem item in response.OutputItems)
{
    if (item is FunctionCallResponseItem call && call.FunctionName == "get_weather")
    {
        using JsonDocument args = JsonDocument.Parse(call.FunctionArguments);
        string location = args.RootElement.GetProperty("location").GetString();
        string toolOutput = $"{{ \"location\": \"{location}\", \"temperature\": \"70 F\" }}";

        CreateResponseOptions followUp = new()
        {
            Model = "MODEL_NAME",
            PreviousResponseId = response.Id,
            InputItems = { ResponseItem.CreateFunctionCallOutputItem(call.CallId, toolOutput) },
            Tools = { getWeatherTool }
        };

        ResponseResult finalResponse = await openAIClient.CreateResponseAsync(followUp);
        Console.WriteLine(finalResponse.GetOutputText());
    }
}
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

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseFunctionToolCall;
import com.openai.models.responses.ResponseInputItem;
import java.util.ArrayList;
import java.util.List;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

// Strongly-typed function parameter class.
class GetWeather {
    @JsonPropertyDescription("City and country, for example, Paris, France")
    public String location;
}

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("What is the weather like in Paris today?")
        .addTool(GetWeather.class)
        .build());

List<ResponseInputItem> followUp = new ArrayList<>();
response.output().forEach(item -> {
    if (item.isFunctionCall()) {
        ResponseFunctionToolCall call = item.asFunctionCall();
        // Execute the tool with call.arguments() and capture the result.
        String result = "{\"temperature\":\"22 C\",\"conditions\":\"Sunny\"}";
        followUp.add(ResponseInputItem.ofFunctionCallOutput(
            ResponseInputItem.FunctionCallOutput.builder()
                .callId(call.callId())
                .output(result)
                .build()));
    }
});

Response finalResponse = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .previousResponseId(response.id())
        .inputOfResponse(followUp)
        .addTool(GetWeather.class)
        .build());

System.out.println(finalResponse.outputText());
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

## Handle guardrails and content filtering

Guardrails (content filters) are applied at the deployment level and run automatically on every Responses API call, so they protect both the input you send and the output the model generates. You configure guardrails separately. For more information, see [Configure guardrails and controls](../../guardrails/how-to-create-guardrails.md). This section shows how to detect and handle guardrail results when you call the Responses API.

The Responses API surfaces guardrail results differently from chat completions. Instead of the `prompt_filter_results` and `content_filter_results` fields that chat completions return, the response object includes a top-level `content_filters` array. Each entry describes one filter result.

| Field | Description |
| --- | --- |
| `blocked` | Whether the content was blocked. |
| `source_type` | Whether the result applies to the `prompt` (input) or the `completion` (output). |
| `content_filter_results` | The category results, such as `hate`, `sexual`, `violence`, and `self_harm` with severity levels, plus optional categories such as `jailbreak`, `indirect_attack`, `protected_material_text`, and `protected_material_code`. |
| `content_filter_offsets` | The character offsets that the result applies to. |

> [!NOTE]
> The `content_filters` array is a Microsoft Foundry extension that isn't part of the base OpenAI response schema, so the SDKs don't expose a typed property for it. Read it as a raw or extra field, as shown in the following examples.

### Detect blocked input

When guardrails block your input, the API returns an HTTP 400 error with the code `content_filter`. Catch this error to handle blocked prompts gracefully.

# [Python](#tab/python)
```python
import os
from openai import OpenAI, BadRequestError

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

# A blocked prompt raises BadRequestError with the code "content_filter"
try:
    response = client.responses.create(
        model="MODEL_NAME",
        input="This is a test."
    )
    print(response.output_text)
except BadRequestError as error:
    if error.code == "content_filter":
        print("The prompt was blocked by a guardrail.")
    else:
        raise
```

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using OpenAI.Responses;
using System.ClientModel;
using System.ClientModel.Primitives;

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems = { ResponseItem.CreateUserMessageItem("This is a test.") }
};

// A blocked prompt throws ClientResultException with HTTP 400
try
{
    ResponseResult response = await openAIClient.CreateResponseAsync(options);
    Console.WriteLine(response.GetOutputText());
}
catch (ClientResultException error) when (error.Status == 400)
{
    Console.WriteLine("The prompt was blocked by a guardrail.");
}
```

# [JavaScript](#tab/javascript)
```javascript
import { OpenAI, APIError } from "openai";

const openai = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

// A blocked prompt throws APIError with the code "content_filter"
try {
  const response = await openai.responses.create({
    model: "MODEL_NAME",
    input: "This is a test."
  });
  console.log(response.output_text);
} catch (error) {
  if (error instanceof APIError && error.code === "content_filter") {
    console.log("The prompt was blocked by a guardrail.");
  } else {
    throw error;
  }
}
```

# [Java](#tab/java)
```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.AzureApiKeyCredential;
import com.openai.errors.BadRequestException;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

ResponseCreateParams params = ResponseCreateParams.builder()
    .model("MODEL_NAME")
    .input("This is a test.")
    .build();

// A blocked prompt throws BadRequestException (HTTP 400)
try {
    Response response = openAIClient.responses().create(params);
    System.out.println(response.outputText());
} catch (BadRequestException error) {
    System.out.println("The prompt was blocked by a guardrail.");
}
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": "This is a test."
  }'
```

When guardrails block the input, the API returns HTTP 400 with the code `content_filter`:

```json
{
  "error": {
    "code": "content_filter",
    "message": "The response was filtered due to the prompt triggering content management policy."
  }
}
```

---

### Read guardrail annotations

When a request succeeds, read the `content_filters` array from the response to inspect the guardrail results for the input and output.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)
response = client.responses.create(
    model="MODEL_NAME",
    input="This is a test."
)

# content_filters is an Azure extension, so read it from model_extra
content_filters = response.model_extra.get("content_filters", [])
for result in content_filters:
    print(f"Source: {result['source_type']}, Blocked: {result['blocked']}")
```

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using OpenAI.Responses;
using System.ClientModel;
using System.ClientModel.Primitives;
using System.Text.Json;

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems = { ResponseItem.CreateUserMessageItem("This is a test.") }
};

// content_filters has no typed property, so parse it from the raw response
ClientResult<ResponseResult> result = await openAIClient.CreateResponseAsync(options);
using JsonDocument doc = JsonDocument.Parse(result.GetRawResponse().Content);
if (doc.RootElement.TryGetProperty("content_filters", out JsonElement filters))
{
    foreach (JsonElement filter in filters.EnumerateArray())
    {
        string source = filter.GetProperty("source_type").GetString()!;
        bool blocked = filter.GetProperty("blocked").GetBoolean();
        Console.WriteLine($"Source: {source}, Blocked: {blocked}");
    }
}
```

# [JavaScript](#tab/javascript)
```javascript
import { OpenAI } from "openai";

const openai = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});
const response = await openai.responses.create({
  model: "MODEL_NAME",
  input: "This is a test."
});

// content_filters is an Azure extension not in the typed response
const contentFilters = response.content_filters ?? [];
for (const result of contentFilters) {
  console.log(`Source: ${result.source_type}, Blocked: ${result.blocked}`);
}
```

# [Java](#tab/java)
```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.AzureApiKeyCredential;
import com.openai.core.JsonValue;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

ResponseCreateParams params = ResponseCreateParams.builder()
    .model("MODEL_NAME")
    .input("This is a test.")
    .build();
Response response = openAIClient.responses().create(params);

// content_filters has no typed accessor, so read it from additional properties
JsonValue contentFilters = response._additionalProperties().get("content_filters");
System.out.println(contentFilters);
```

# [REST](#tab/rest)
```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "MODEL_NAME",
    "input": "This is a test."
  }'
```

The `content_filters` array appears on the response object:

```json
{
  "id": "resp_<id>",
  "content_filters": [
    {
      "source_type": "prompt",
      "blocked": false,
      "content_filter_results": {
        "hate": { "filtered": false, "severity": "safe" },
        "self_harm": { "filtered": false, "severity": "safe" },
        "sexual": { "filtered": false, "severity": "safe" },
        "violence": { "filtered": false, "severity": "safe" }
      }
    }
  ]
}
```

---

To learn more about guardrail categories and severity levels, see [Guardrails overview](../../guardrails/guardrails-overview.md) and [Work with annotations](../../guardrails/how-to-create-guardrails.md#work-with-annotations).

## Code Interpreter

The Code Interpreter tool enables models to write and execute Python code in a secure, sandboxed environment. It supports a range of advanced tasks, including:

- Processing files with varied data formats and structures
- Generating files that include data and visualizations (for example, graphs)
- Iteratively writing and running code to solve problems—models can debug and retry code until successful
- Enhancing visual reasoning in supported models (for example, o3, o4-mini) by enabling image transformations such as cropping, zooming, and rotation
- This tool is especially useful for scenarios involving data analysis, mathematical computation, and code generation.

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

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using Azure.Identity;
using OpenAI.Containers;
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

CodeInterpreterToolContainer container = new(
    CodeInterpreterToolContainerConfiguration.CreateAutomaticContainerConfiguration());
CodeInterpreterTool codeInterpreterTool = new(container);

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem("Solve 3x + 11 = 14.")
    },
    Tools = { codeInterpreterTool }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
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

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.Tool;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Tool codeInterpreter = Tool.ofCodeInterpreter(
    Tool.CodeInterpreter.builder()
        .container(Tool.CodeInterpreter.Container.ofCodeInterpreterToolAuto(
            Tool.CodeInterpreter.Container.CodeInterpreterToolAuto.builder().build()))
        .build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("Solve 3x + 11 = 14.")
        .addTool(codeInterpreter)
        .build());

System.out.println(response.outputText());
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

Retrieve the input items that were sent to a response. This is useful for inspecting the full conversation context, including any items added by the model (for example, function calls or compaction items).

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

# [C#](#tab/csharp)
> [!NOTE]
> The .NET SDK exposes this endpoint only as a protocol method. See the **REST** tab for the call shape, or invoke the protocol method directly.

# [JavaScript](#tab/javascript)
```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const items = await client.responses.inputItems.list("<response_id>");
console.log(JSON.stringify(items, null, 2));
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.inputitems.ResponseInputItemListPage;
import com.openai.models.responses.inputitems.ResponseInputItemListParams;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

ResponseInputItemListPage page = openAIClient.responses().inputItems().list(
    ResponseInputItemListParams.builder()
        .responseId("<response_id>")
        .build());

page.autoPager().stream().forEach(item -> System.out.println(item));
```

# [REST](#tab/rest)
```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id>/input_items \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```

---

### Example response

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

## Image input

Vision-enabled models can interpret images alongside text. They can recognize objects, shapes, colors, and textures, and read text contained within an image, subject to the limitations listed later in this article.

You can provide an image as input to a request in any of the following ways:

- A fully qualified URL to an image file
- A Base64-encoded data URI
- A file ID created with the [Files API](../reference-preview-latest.md)

### Image URL

Reference an image hosted at a public URL. The model fetches the image and includes it as part of the input content.

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
    InputItems =
    {
        ResponseItem.CreateUserMessageItem(
        [
            ResponseContentPart.CreateInputTextPart("What is in this image?"),
            ResponseContentPart.CreateInputImagePart(new Uri("<image_url>"))
        ])
    }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
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

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseInputImage;
import com.openai.models.responses.ResponseInputItem;
import java.util.List;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

ResponseInputImage image = ResponseInputImage.builder()
    .detail(ResponseInputImage.Detail.AUTO)
    .imageUrl("<image_url>")
    .build();

ResponseInputItem userMsg = ResponseInputItem.ofMessage(
    ResponseInputItem.Message.builder()
        .role(ResponseInputItem.Message.Role.USER)
        .addInputTextContent("What is in this image?")
        .addContent(image)
        .build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .inputOfResponse(List.of(userMsg))
        .build());

System.out.println(response.outputText());
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

Send an image inline by encoding its bytes as a base64 data URI. Use this pattern when the image isn't hosted at a public URL or when you want to avoid an extra network fetch.

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

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using System.IO;
using System.Threading.Tasks;
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

byte[] imageBytes = await File.ReadAllBytesAsync("path_to_your_image.jpg");
BinaryData imageData = BinaryData.FromBytes(imageBytes);

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem(
        [
            ResponseContentPart.CreateInputTextPart("What is in this image?"),
            ResponseContentPart.CreateInputImagePart(imageData, "image/jpeg")
        ])
    }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
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
# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseInputImage;
import com.openai.models.responses.ResponseInputItem;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.List;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

byte[] bytes = Files.readAllBytes(Paths.get("cat.jpg"));
String dataUrl = "data:image/jpeg;base64," + Base64.getEncoder().encodeToString(bytes);

ResponseInputImage image = ResponseInputImage.builder()
    .detail(ResponseInputImage.Detail.AUTO)
    .imageUrl(dataUrl)
    .build();

ResponseInputItem userMsg = ResponseInputItem.ofMessage(
    ResponseInputItem.Message.builder()
        .role(ResponseInputItem.Message.Role.USER)
        .addInputTextContent("What is in this image?")
        .addContent(image)
        .build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .inputOfResponse(List.of(userMsg))
        .build());

System.out.println(response.outputText());
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
          {"type": "input_image", "image_url": "data:image/jpeg;base64,<BASE64_IMAGE>"}
        ]
      }
    ]
  }'
```

---

### File ID

Upload an image with the Files API by using `purpose="vision"`, then reference the returned file ID in your request. This approach is useful when you want to reuse the same image across multiple requests without resending its bytes.

# [Python](#tab/python)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

def create_file(file_path):
    with open(file_path, "rb") as file_content:
        result = client.files.create(
            file=file_content,
            purpose="vision",
        )
        return result.id

file_id = create_file("path_to_your_image.jpg")

response = client.responses.create(
    model="MODEL_NAME",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What is in this image?"},
                {"type": "input_image", "file_id": file_id},
            ],
        }
    ],
)

print(response.output_text)
```

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using System.IO;
using System.Threading.Tasks;
using Azure.Identity;
using OpenAI;
using OpenAI.Files;
using OpenAI.Responses;
using System.ClientModel.Primitives;

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

// API key authentication
ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

OpenAIFileClient fileClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new OpenAIClientOptions { Endpoint = new Uri(endpoint) });

// Microsoft Entra ID authentication (recommended)
BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");
ResponsesClient openAIClientEntra = new(
    authenticationPolicy: tokenPolicy,
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

byte[] imageBytes = await File.ReadAllBytesAsync("path_to_your_image.jpg");
OpenAIFile uploadedFile = await fileClient.UploadFileAsync(
    BinaryData.FromBytes(imageBytes),
    "path_to_your_image.jpg",
    FileUploadPurpose.Vision);

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem(
        [
            ResponseContentPart.CreateInputTextPart("What is in this image?"),
            ResponseContentPart.CreateInputImagePart(uploadedFile.Id)
        ])
    }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)
```javascript
import fs from "node:fs";
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const file = await client.files.create({
  file: fs.createReadStream("path_to_your_image.jpg"),
  purpose: "vision",
});

const response = await client.responses.create({
  model: "MODEL_NAME",
  input: [
    {
      role: "user",
      content: [
        { type: "input_text", text: "What is in this image?" },
        { type: "input_image", file_id: file.id },
      ],
    },
  ],
});

console.log(response.output_text);
```

# [Java](#tab/java)
```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.AzureApiKeyCredential;
import com.openai.models.FileCreateParams;
import com.openai.models.FileObject;
import com.openai.models.FilePurpose;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseInputImage;
import com.openai.models.responses.ResponseInputItem;
import java.nio.file.Paths;
import java.util.List;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

FileObject uploaded = openAIClient.files().create(
    FileCreateParams.builder()
        .file(Paths.get("path_to_your_image.jpg"))
        .purpose(FilePurpose.VISION)
        .build());

ResponseInputImage image = ResponseInputImage.builder()
    .detail(ResponseInputImage.Detail.AUTO)
    .fileId(uploaded.id())
    .build();

ResponseInputItem userMsg = ResponseInputItem.ofMessage(
    ResponseInputItem.Message.builder()
        .role(ResponseInputItem.Message.Role.USER)
        .addInputTextContent("What is in this image?")
        .addContent(image)
        .build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .inputOfResponse(List.of(userMsg))
        .build());

System.out.println(response.outputText());
```

# [REST](#tab/rest)
```bash
# Upload the image
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/files \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F purpose="vision" \
  -F file="@path_to_your_image.jpg"

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
          {"type": "input_text", "text": "What is in this image?"},
          {"type": "input_image", "file_id": "<file_id>"}
        ]
      }
    ]
  }'
```

---

### Image input requirements

The following table lists the supported file types for image inputs.

| File type   | MIME type         |
|-------------|-------------------|
| PNG         | `image/png`       |
| JPEG        | `image/jpeg`      |
| WebP        | `image/webp`      |
| Non-animated GIF | `image/gif`  |

In a single request, you can include up to 100 images. Each individual image file must be under 50 MB, and the combined size of all images in the request must also be under 50 MB.

Images must meet these additional requirements:

- The image must be relevant to the prompt; the model isn't designed for unrelated visual content.
- Images shouldn't contain harmful or sensitive content that violates content policies.
- Image files can't be corrupted or unreadable. If the model can't process an image, the request fails.

### Choose an image detail level

Use the `detail` property on an `input_image` content part to control how the model processes the image. Lower detail uses fewer tokens and is faster, while higher detail uses more tokens but lets the model capture finer features.

```json
{
  "type": "input_image",
  "image_url": "<image_url>",
  "detail": "high"
}
```

The following table describes each detail level.

| Detail level | Description |
|--------------|-------------|
| `low`        | The model uses a lower-resolution version of the image. This option uses the fewest tokens and produces the fastest response, but the model might miss fine details. |
| `high`       | The model uses a higher-resolution version of the image. This option captures finer details but uses more tokens and takes longer to respond. |
| `auto`       | The default. The model selects the appropriate detail level based on the image and the prompt. |

### Image input limitations

Vision-enabled models have the following limitations:

- **Medical images**: The model isn't suitable for interpreting specialized medical images such as CT scans and shouldn't be used for medical advice.
- **Non-English text**: The model might not perform optimally when handling images that contain text in non-Latin alphabets, such as Japanese or Korean.
- **Small text**: Enlarge text within an image to improve readability, but avoid cropping out important details.
- **Rotation**: The model might misinterpret rotated or upside-down text and images.
- **Visual elements**: The model might struggle with graphs or text where colors or styles—such as solid, dashed, or dotted lines—vary.
- **Spatial reasoning**: The model has difficulty with tasks that require precise spatial localization, such as identifying chess positions.
- **Accuracy**: The model might generate incorrect descriptions or captions in some cases.
- **Image shape**: The model has difficulty with panoramic and fisheye images.
- **Metadata and resizing**: The model doesn't process original file names or metadata, and images are resized before analysis, which affects their original dimensions.
- **Counting**: The model might give approximate counts for objects in images.
- **CAPTCHAs**: For safety reasons, a system is in place to block the submission of CAPTCHAs.

## File input

Models with vision capabilities support PDF input. PDF files can be provided either as Base64-encoded data or as file IDs. To help models interpret PDF content, both the extracted text and an image of each page are included in the model’s context. This is useful when key information is conveyed through diagrams or non-textual content.

> [!NOTE]
> - All extracted text and images are put into the model's context. Make sure you understand the pricing and token usage implications of using PDFs as input.
> - In a single API request, you can include more than one file, but each file must be under 50 MB. The combined limit across all files in the request is 50 MB.
> - Only models that support both text and image inputs can accept PDF files as input.
> - A `purpose` of `user_data` is currently not supported. As a temporary workaround you will need to set purpose to `assistants`.

### Convert PDF to Base64 and analyze

Send a PDF inline by encoding its bytes as a base64 data URI. The model receives both the extracted text and a rendered image of each page.

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

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using System.IO;
using System.Threading.Tasks;
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

byte[] pdfBytes = await File.ReadAllBytesAsync("PDF-FILE-NAME.pdf");
BinaryData pdfData = BinaryData.FromBytes(pdfBytes);

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem(
        [
            ResponseContentPart.CreateInputFilePart(pdfData, "application/pdf", "PDF-FILE-NAME.pdf"),
            ResponseContentPart.CreateInputTextPart("Summarize this PDF.")
        ])
    }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
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
# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseInputFile;
import com.openai.models.responses.ResponseInputItem;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.List;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

byte[] pdfBytes = Files.readAllBytes(Paths.get("document.pdf"));
String dataUrl = "data:application/pdf;base64," + Base64.getEncoder().encodeToString(pdfBytes);

ResponseInputFile file = ResponseInputFile.builder()
    .filename("document.pdf")
    .fileData(dataUrl)
    .build();

ResponseInputItem userMsg = ResponseInputItem.ofMessage(
    ResponseInputItem.Message.builder()
        .role(ResponseInputItem.Message.Role.USER)
        .addInputTextContent("Summarize this PDF.")
        .addContent(file)
        .build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .inputOfResponse(List.of(userMsg))
        .build());

System.out.println(response.outputText());
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
          {"type": "input_file", "filename": "PDF-FILE-NAME.pdf", "file_data": "data:application/pdf;base64,<BASE64_PDF>"},
          {"type": "input_text", "text": "Summarize this PDF."}
        ]
      }
    ]
  }'
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

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using System.IO;
using System.Threading.Tasks;
using Azure.Identity;
using OpenAI;
using OpenAI.Files;
using OpenAI.Responses;
using System.ClientModel.Primitives;

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

// API key authentication
ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

OpenAIFileClient fileClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new OpenAIClientOptions { Endpoint = new Uri(endpoint) });

// Microsoft Entra ID authentication (recommended)
BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");
ResponsesClient openAIClientEntra = new(
    authenticationPolicy: tokenPolicy,
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

byte[] pdfBytes = await File.ReadAllBytesAsync("nucleus_sampling.pdf");
OpenAIFile uploadedFile = await fileClient.UploadFileAsync(
    BinaryData.FromBytes(pdfBytes),
    "nucleus_sampling.pdf",
    FileUploadPurpose.UserData);

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem(
        [
            ResponseContentPart.CreateInputFilePart(uploadedFile.Id),
            ResponseContentPart.CreateInputTextPart("Summarize this PDF.")
        ])
    }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)
```javascript
import fs from "node:fs";
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const file = await client.files.create({
  file: fs.createReadStream("nucleus_sampling.pdf"),
  purpose: "assistants",
});

const response = await client.responses.create({
  model: "MODEL_NAME",
  input: [
    {
      role: "user",
      content: [
        { type: "input_file", file_id: file.id },
        { type: "input_text", text: "Summarize this PDF." },
      ],
    },
  ],
});

console.log(response.output_text);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.FileCreateParams;
import com.openai.models.FileObject;
import com.openai.models.FilePurpose;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseInputFile;
import com.openai.models.responses.ResponseInputItem;
import java.nio.file.Paths;
import java.util.List;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

FileObject uploaded = openAIClient.files().create(
    FileCreateParams.builder()
        .file(Paths.get("document.pdf"))
        .purpose(FilePurpose.USER_DATA)
        .build());

ResponseInputFile file = ResponseInputFile.builder()
    .fileId(uploaded.id())
    .build();

ResponseInputItem userMsg = ResponseInputItem.ofMessage(
    ResponseInputItem.Message.builder()
        .role(ResponseInputItem.Message.Role.USER)
        .addInputTextContent("Summarize this PDF.")
        .addContent(file)
        .build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .inputOfResponse(List.of(userMsg))
        .build());

System.out.println(response.outputText());
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
    InputItems = { ResponseItem.CreateUserMessageItem("What transport protocols are supported in the 2025-03-26 version of the MCP spec?") },
    Tools =
    {
        new McpTool(serverLabel: "github", serverUri: new Uri("https://contoso.com/Azure/azure-rest-api-specs"))
        {
            ToolCallApprovalPolicy = GlobalMcpToolCallApprovalPolicy.NeverRequireApproval
        }
    }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
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

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.Tool;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Tool mcpTool = Tool.ofMcp(
    Tool.Mcp.builder()
        .serverLabel("github")
        .serverUrl("https://contoso.com/Azure/azure-rest-api-specs")
        .requireApproval(Tool.Mcp.RequireApproval.ofMcpToolApprovalSetting(
            Tool.Mcp.RequireApproval.McpToolApprovalSetting.NEVER))
        .build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("What is this repo in 100 words?")
        .addTool(mcpTool)
        .build());

System.out.println(response.outputText());
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

McpTool mcpTool = new(serverLabel: "github", serverUri: new Uri("https://contoso.com/Azure/azure-rest-api-specs"));

ResponseResult priorResponse = await openAIClient.GetResponseAsync("<previous_response_id>");

foreach (ResponseItem item in priorResponse.OutputItems)
{
    if (item is McpToolCallApprovalRequestItem approvalRequest)
    {
        CreateResponseOptions followUp = new()
        {
            Model = "MODEL_NAME",
            PreviousResponseId = priorResponse.Id,
            InputItems = { new McpToolCallApprovalResponseItem(approvalRequest.Id, approved: true) },
            Tools = { mcpTool }
        };

        ResponseResult finalResponse = await openAIClient.CreateResponseAsync(followUp);
        Console.WriteLine(finalResponse.GetOutputText());
    }
}
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
  previous_response_id: "<previous_response_id>",
  input: [
    {
      type: "mcp_approval_response",
      approve: true,
      approval_request_id: "<approval_request_id>",
    },
  ],
});

console.log(response.output_text);
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
import com.openai.models.responses.ResponseInputItem;
import java.util.List;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .previousResponseId("<previous_response_id>")
        .inputOfResponse(List.of(
            ResponseInputItem.ofMcpApprovalResponse(
                ResponseInputItem.McpApprovalResponse.builder()
                    .approvalRequestId("<approval_request_id>")
                    .approve(true)
                    .build())))
        .build());

System.out.println(response.outputText());
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
> - Mutual TLS (mTLS) is currently not supported.
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
    InputItems = { ResponseItem.CreateUserMessageItem("What is this repo in 100 words?") },
    Tools =
    {
        new McpTool(serverLabel: "github", serverUri: new Uri("https://contoso.com/Azure/azure-rest-api-specs"))
        {
            AuthorizationToken = Environment.GetEnvironmentVariable("YOUR_MCP_TOKEN"),
            ToolCallApprovalPolicy = GlobalMcpToolCallApprovalPolicy.NeverRequireApproval
        }
    }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
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
  input: "What is this repo in 100 words?",
  tools: [
    {
      type: "mcp",
      server_label: "github",
      server_url: "https://contoso.com/Azure/azure-rest-api-specs",
      headers: { Authorization: "Bearer $YOUR_MCP_TOKEN" },
    },
  ],
});

console.log(response.output_text);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.JsonValue;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.Tool;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Tool mcpTool = Tool.ofMcp(
    Tool.Mcp.builder()
        .serverLabel("github")
        .serverUrl("https://contoso.com/Azure/azure-rest-api-specs")
        .headers(Tool.Mcp.Headers.builder()
            .putAdditionalProperty("Authorization", JsonValue.from("Bearer $YOUR_MCP_TOKEN"))
            .build())
        .requireApproval(Tool.Mcp.RequireApproval.ofMcpToolApprovalSetting(
            Tool.Mcp.RequireApproval.McpToolApprovalSetting.NEVER))
        .build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("What is this repo in 100 words?")
        .addTool(mcpTool)
        .build());

System.out.println(response.outputText());
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

Set `background=true` on the request to queue the task. The service returns immediately with a response ID and a `queued` status — use that ID to poll, stream, or cancel the task.

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
    InputItems = { ResponseItem.CreateUserMessageItem("Write me a very long story.") },
    BackgroundModeEnabled = true
};

ResponseResult queued = await openAIClient.CreateResponseAsync(options);
Console.WriteLine($"Response id: {queued.Id}");
Console.WriteLine($"Status: {queued.Status}");
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

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("Write a 1000-word essay on the history of computing.")
        .background(true)
        .build());

System.out.println(response.status());
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

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using System.Threading.Tasks;
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

ResponseResult current = await openAIClient.GetResponseAsync("<response_id>");

while (current.Status == ResponseStatus.Queued || current.Status == ResponseStatus.InProgress)
{
    Console.WriteLine($"Current status: {current.Status}");
    await Task.Delay(TimeSpan.FromSeconds(2));
    current = await openAIClient.GetResponseAsync(current.Id);
}

Console.WriteLine($"Final status: {current.Status}");
if (current.Status == ResponseStatus.Completed)
{
    Console.WriteLine(current.GetOutputText());
}
```

# [JavaScript](#tab/javascript)
```javascript
let current = response;
while (current.status === "queued" || current.status === "in_progress") {
  console.log(`Current status: ${current.status}`);
  await new Promise((r) => setTimeout(r, 2000));
  current = await client.responses.retrieve(current.id);
}
console.log(`Final status: ${current.status}\nOutput:\n${current.output_text}`);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Response current = openAIClient.responses().retrieve("<response_id>");
while (current.status().filter(s ->
        s.equals(Response.Status.QUEUED) || s.equals(Response.Status.IN_PROGRESS)).isPresent()) {
    System.out.println("Current status: " + current.status());
    Thread.sleep(2000);
    current = openAIClient.responses().retrieve(current.id());
}
System.out.println("Final status: " + current.status());
System.out.println("Output:\n" + current.outputText());
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

ResponseResult cancelled = await openAIClient.CancelResponseAsync("<response_id>");
Console.WriteLine($"Status: {cancelled.Status}");
```

# [JavaScript](#tab/javascript)
```javascript
const cancelled = await client.responses.cancel("<response_id>");
console.log(cancelled.status);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Response cancelled = openAIClient.responses().cancel("<response_id>");
System.out.println(cancelled.status());
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

CreateResponseOptions createOptions = new()
{
    Model = "MODEL_NAME",
    InputItems = { ResponseItem.CreateUserMessageItem("Write me a very long story.") },
    BackgroundModeEnabled = true,
    StreamingEnabled = true
};

string queuedResponseId = null;
int lastSequenceNumber = 0;

await foreach (StreamingResponseUpdate update in openAIClient.CreateResponseStreamingAsync(createOptions))
{
    if (update is StreamingResponseQueuedUpdate queuedUpdate)
    {
        queuedResponseId = queuedUpdate.Response.Id;
        lastSequenceNumber = queuedUpdate.SequenceNumber;
        Console.WriteLine($"Queued response: {queuedResponseId}, sequence {lastSequenceNumber}");
        break;
    }
}

// Resume streaming from where we disconnected.
GetResponseOptions resumeOptions = new(queuedResponseId)
{
    StartingAfter = lastSequenceNumber,
    StreamingEnabled = true
};

await foreach (StreamingResponseUpdate update in openAIClient.GetResponseStreamingAsync(resumeOptions))
{
    Console.WriteLine(update.GetType().Name);
    if (update is StreamingResponseCompletedUpdate completed)
    {
        Console.WriteLine($"[done] final id: {completed.Response.Id}");
    }
}
```

# [JavaScript](#tab/javascript)
```javascript
const stream = await client.responses.create({
  model: "MODEL_NAME",
  input: "Write me a very long story.",
  background: true,
  stream: true,
});

let cursor = null;
for await (const event of stream) {
  console.log(event);
  cursor = event.sequence_number;
}
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.http.StreamResponse;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.ResponseRetrieveParams;
import com.openai.models.responses.ResponseStreamEvent;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

long cursor = 0L;
try (StreamResponse<ResponseStreamEvent> stream = openAIClient.responses().retrieveStreaming(
        "<response_id>",
        ResponseRetrieveParams.builder().startingAfter(cursor).build())) {
    stream.stream().forEach(event -> System.out.println(event));
}
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

Background responses currently have a higher time-to-first-token latency than synchronous responses. Improvements are underway to reduce this gap.

### Limitations

- Background mode requires `store=true`. Stateless requests are not supported.
- You can only resume streaming if the original request included `stream=true`.
- To cancel a synchronous response, terminate the connection directly.

### Resume streaming from a specific point

If a streaming connection drops, you can resume from a known event by passing `stream=true` along with `starting_after=<sequence_number>` on a `GET` to the response. The service replays events emitted after that sequence number.

```bash
curl -N -X GET "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/<response_id>?stream=true&starting_after=42" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```

## Encrypted reasoning items

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

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using System.Collections.Generic;
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

List<ResponseItem> inputItems =
[
    ResponseItem.CreateUserMessageItem("<your_prompt>")
];

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    StoredOutputEnabled = false,
    IncludedProperties = { IncludedResponseProperty.ReasoningEncryptedContent }
};
foreach (ResponseItem item in inputItems)
{
    options.InputItems.Add(item);
}

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());

// To carry encrypted reasoning into a follow-up turn, append response.OutputItems to inputItems
// and resend with StoredOutputEnabled = false. Don't use PreviousResponseId when not stored.
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
  reasoning: { effort: "medium" },
  input: "What is the weather like today?",
  tools: [
    // Replace with your function or tool definitions.
  ],
  include: ["reasoning.encrypted_content"],
  store: false,
});

console.log(response.output_text);
```

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Reasoning;
import com.openai.models.responses.ReasoningEffort;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseIncludable;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("Explain quantum entanglement.")
        .reasoning(Reasoning.builder().effort(ReasoningEffort.MEDIUM).build())
        .addInclude(ResponseIncludable.REASONING_ENCRYPTED_CONTENT)
        .store(false)
        .build());

System.out.println(response.outputText());
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

- **Streaming**: Display partial image outputs during generation to improve perceived latency.
- **Flexible inputs**: Accept image file IDs as inputs in addition to raw image bytes.

> [!NOTE]
> The image generation tool in the Responses API is supported by `gpt-image-1`-series models, and you can call it from a set of compatible chat and reasoning models. For the current list of supported orchestration models, see the [Supported models](#supported-models) section later in this article.
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

# [C#](#tab/csharp)
```csharp
#pragma warning disable OPENAI001
using System.IO;
using System.Threading.Tasks;
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

ImageGenerationTool imageTool = ResponseTool.CreateImageGenerationTool(model: "gpt-image-1");

CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem("Generate an image of an otter swimming in a pond.")
    },
    Tools = { imageTool }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);

foreach (ResponseItem item in response.OutputItems)
{
    if (item is ImageGenerationCallResponseItem imageCall && imageCall.ImageResultBytes is not null)
    {
        await File.WriteAllBytesAsync("otter.png", imageCall.ImageResultBytes.ToArray());
        Console.WriteLine($"Saved image. Revised prompt: {imageCall.RevisedPrompt}");
    }
}
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

# [Java](#tab/java)
```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.identity.AuthenticationUtil;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseOutputItem;
import com.openai.models.responses.Tool;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;

String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
    .baseUrl(endpoint)
    .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
    .build();

Tool imageGen = Tool.ofImageGeneration(Tool.ImageGeneration.builder().build());

Response response = openAIClient.responses().create(
    ResponseCreateParams.builder()
        .model("MODEL_NAME")
        .input("Generate an image of a gray tabby cat hugging an otter with an orange scarf.")
        .addTool(imageGen)
        .build());

response.output().stream()
    .filter(ResponseOutputItem::isImageGenerationCall)
    .map(ResponseOutputItem::asImageGenerationCall)
    .findFirst()
    .flatMap(call -> call.result())
    .ifPresent(b64 -> {
        try {
            Files.write(Paths.get("otter.png"), Base64.getDecoder().decode(b64));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    });
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

Computer use with Playwright has moved to the [dedicated computer use model guide](../../../foundry-classic/openai/how-to/computer-use.md#playwright-integration).

## Troubleshooting

- **401/403**: If you use Microsoft Entra ID, verify your token is scoped for `https://ai.azure.com/.default`. If you use an API key, confirm you're using the correct key for the resource.
- **404**: Confirm `model` matches your deployment name.

## Related content

- [The Azure OpenAI Starter Kit](https://aka.ms/openai/start)
- [Azure OpenAI To Responses](https://aka.ms/azure-openai-to-responses)
- [API version lifecycle](../api-version-lifecycle.md)
- [Azure OpenAI REST API reference](../latest.md)
- [Computer use](../../../foundry-classic/openai/how-to/computer-use.md)
