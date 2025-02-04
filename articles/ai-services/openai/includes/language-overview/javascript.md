---
title: Azure OpenAI JavaScript support
titleSuffix: Azure OpenAI Service
description: Azure OpenAI JavaScript support
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 11/18/2024
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Reference](../../reference.md) |


## Azure OpenAI API version support

Feature availability in Azure OpenAI is dependent on what version of the REST API you target. For the newest features, target the latest preview API.

| Latest GA API | Latest Preview API|
|:-----|:------|
|`2024-10-21` |`2025-01-01-preview`|

## Installation

```cmd
npm install openai
```

## Authentication

# [Microsoft Entra ID](#tab/secure)

There are several ways to authenticate with the Azure OpenAI service using Microsoft Entra ID tokens. The default way is to use the `DefaultAzureCredential` class from the `@azure/identity` package.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
const credential = new DefaultAzureCredential();
```

This object is then passed to the second argument of the `OpenAIClient` and `AssistantsClient` client constructors.

In order to authenticate the `AzureOpenAI` client, however, we need to use the `getBearerTokenProvider` function from the `@azure/identity` package. This function creates a token provider that `AzureOpenAI` uses internally to obtain tokens for each request. The token provider is created as follows:

```typescript
import { AzureOpenAI } from 'openai';
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
const credential = new DefaultAzureCredential();
const endpoint = "https://your-azure-openai-resource.com";
const apiVersion = "2024-10-21"
const scope = "https://cognitiveservices.azure.com/.default";
const azureADTokenProvider = getBearerTokenProvider(credential, scope);


const client = new AzureOpenAI({ 
    endpoint, 
    apiVersions,
    azureADTokenProvider
     });
```

# [API Key](#tab/api-key)

API Key

API keys are not recommended for production use because they are less secure than other authentication methods. 

```typescript
import { AzureKeyCredential } from "@azure/openai";
const apiKey = new AzureKeyCredential("your API key");
const endpoint = "https://your-azure-openai-resource.com";0
const apiVersion = "2024-10-21"

const client = new AzureOpenAI({ apiKey, endpoint, apiVersion });
```

`AzureOpenAI` can be authenticated with an API key by setting the `AZURE_OPENAI_API_KEY` environment variable or by setting the `apiKey` string property in the options object when creating the `AzureOpenAI` client.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

---

## Audio

### Transcription

```typescript
import { createReadStream } from "fs";

const result = await client.audio.transcriptions.create({
  model: '',
  file: createReadStream(audioFilePath),
});
```

## Chat

`chat.completions.create`

```typescript
const result = await client.chat.completions.create({ messages, model: '', max_tokens: 100 });
```

### Streaming

```typescript
const stream = await client.chat.completions.create({ model: '', messages, max_tokens: 100, stream: true });
```

## Embeddings

```typescript
const embeddings = await client.embeddings.create({ input, model: '' });
```

## Image generation

```typescript
  const results = await client.images.generate({ prompt, model: '', n, size });
```

## Error handling

### Error codes

| Status Code | Error Type |
|----|---|
| 400         | `Bad Request Error`          |
| 401         | `Authentication Error`       |
| 403         | `Permission Denied Error`    |
| 404         | `Not Found Error`            |
| 422         | `Unprocessable Entity Error` |
| 429         | `Rate Limit Error`           |
| 500         | `Internal Server Error`      |
| 503         | `Service Unavailable`       |
| 504         | `Gateway Timeout` |

### Retries

The following errors are automatically retired twice by default with a brief exponential backoff:

- Connection Errors
- 408 Request Timeout
- 429 Rate Limit
- `>=`500 Internal Errors

Use `maxRetries` to set/disable the retry behavior:

```typescript
// Configure the default for all requests:
const client = new AzureOpenAI({
  maxRetries: 0, // default is 2
});

// Or, configure per-request:
await client.chat.completions.create({ messages: [{ role: 'user', content: 'How can I get the name of the current day in Node.js?' }], model: '' }, {
  maxRetries: 5,
});
```