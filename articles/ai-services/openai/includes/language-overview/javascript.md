---
title: Azure OpenAI JavaScript support
titleSuffix: Azure OpenAI Service
description: Azure OpenAI JavaScript support
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/27/2025
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Reference](../../reference.md) |


## Azure OpenAI API version support

Feature availability in Azure OpenAI is dependent on what version of the REST API you target. For the newest features, target the latest preview API.

| Latest GA API | Latest Preview API|
|:-----|:------|
|`2024-10-21` |`2025-03-01-preview`|

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

This object is then passed as part of the [`AzureClientOptions`](#configuration) object to the `AzureOpenAI` and `AssistantsClient` client constructors.

In order to authenticate the `AzureOpenAI` client, however, we need to use the `getBearerTokenProvider` function from the `@azure/identity` package. This function creates a token provider that `AzureOpenAI` uses internally to obtain tokens for each request. The token provider is created as follows:

```typescript
import { AzureOpenAI } from 'openai';
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
const credential = new DefaultAzureCredential();
const endpoint = "https://your-azure-openai-resource.com";
const apiVersion = "2024-10-21"
const scope = "https://cognitiveservices.azure.com/.default";
const azureADTokenProvider = getBearerTokenProvider(credential, scope);
const deployment = "gpt-35-turbo";

const client = new AzureOpenAI({ 
    endpoint, 
    apiVersion,
    deployment,
    azureADTokenProvider
});
```

For more information about Azure OpenAI keyless authentication, see the "[Get started with the Azure OpenAI security building block](/azure/developer/ai/get-started-securing-your-ai-app?tabs=github-codespaces&pivots=typescript)" QuickStart article. 


### Configuration

The `AzureClientOptions` object extends the OpenAI `ClientOptions` object. This Azure-specific client object is used to configure the connection and behavior of the Azure OpenAI client. It includes properties for specifying the properties unique to Azure.

| Property | Details |
|--|--|
| apiVersion: `string` | Specifies the API version to use. |
| azureADTokenProvider: `(() => Promise<string>)` | A function that returns an access token for Microsoft Entra (formerly known as Azure Active Directory), invoked on every request.|
| deployment: `string` | A model deployment. If provided, sets the base client URL to include `/deployments/{deployment}`. Non-deployment endpoints can't be used (not supported with Assistants APIs).|
| endpoint: `string` | Your Azure OpenAI endpoint with the following format: `https://RESOURCE-NAME.azure.openai.com/`.|

# [API Key](#tab/api-key)

API keys aren't recommended for production use because they're less secure than other authentication methods. 

```typescript
import { AzureKeyCredential } from "@azure/openai";
const apiKey = new AzureKeyCredential("your API key");
const endpoint = "https://your-azure-openai-resource.com";
const apiVersion = "2024-10-21"
const deployment = "gpt-35-turbo";

const client = new AzureOpenAI({ 
    apiKey, 
    endpoint, 
    apiVersion, 
    deployment 
});
```

### Configuration

The `AzureClientOptions` object extends the OpenAI `ClientOptions` object. This Azure-specific client object is used to configure the connection and behavior of the Azure OpenAI client. It includes properties for specifying the properties unique to Azure.

| Property | Details |
|--|--|
| apiKey: `string` | Your API key for authenticating requests. |
| apiVersion: `string` | Specifies the API version to use. |
| deployment: `string` | A model deployment. If provided, sets the base client URL to include `/deployments/{deployment}`. Non-deployment endpoints can't be used (not supported with Assistants APIs).|
| endpoint: `string` | Your Azure OpenAI endpoint with the following format: `https://RESOURCE-NAME.azure.openai.com/`.|

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