---
title: Azure OpenAI JavaScript support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI JavaScript support
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 09/15/2025
ai-usage: ai-assisted
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Reference](../../reference.md) |

## Azure OpenAI API version support

- v1 Generally Available (GA) API now allows access to both GA and Preview operations. To learn more, see the [API version lifecycle guide](../../api-version-lifecycle.md).

## Installation

```cmd
npm install openai
```

## Authentication

# [Microsoft Entra ID](#tab/secure)

```cmd
npm install @azure/identity
```

In order to authenticate the `OpenAI` client, however, we need to use the `getBearerTokenProvider` function from the `@azure/identity` package. This function creates a token provider that `OpenAI` uses internally to obtain tokens for each request. The token provider is created as follows:

```typescript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');
const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});
```

For more information about Azure OpenAI keyless authentication, see the "[Get started with the Azure OpenAI security building block](/azure/developer/ai/get-started-securing-your-ai-app?tabs=github-codespaces&pivots=typescript)" QuickStart article. 

# [API Key](#tab/api-key)

API keys aren't recommended for production use because they're less secure than other authentication methods.

```typescript
import { OpenAI } from "openai";

const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: process.env['OPENAI_API_KEY'] //Your Azure OpenAI API key
});
```

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]
---

## Responses

`responses.create`

```typescript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');
const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const response = await client.responses.create({
  model: 'gpt-4.1-nano', //model deployment name
  instructions: 'You are a helpful AI agent',
  input: 'Tell me about the bitter lesson?',
});

console.log(response.output_text);
```

### Streaming

```typescript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');
const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const stream = await client.responses.create({
  model: 'gpt-4.1-nano', // model deployment name
  input: 'Provide a brief history of the attention is all you need paper.',
  stream: true,
});

for await (const event of stream) {
  if (event.type === 'response.output_text.delta' && event.delta) {
    process.stdout.write(event.delta);
  }
}
```

### MCP Server

```javascript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');
const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const resp = await client.responses.create({
  model: "gpt-5",
  tools: [
    {
      type: "mcp",
      server_label: "microsoft_learn",
      server_description: "Microsoft Learn MCP server for searching and fetching Microsoft documentation.",
      server_url: "https://learn.microsoft.com/api/mcp",
      require_approval: "never",
    },
  ],
  input: "Search for information about Azure Functions",
});

console.log(resp.output_text);
```

## Chat

`chat.completions.create`

```typescript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');
const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const messages = [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Tell me about the attention is all you need paper' }
];

// Make the API request with top-level await
const result = await client.chat.completions.create({ 
    messages, 
    model: 'gpt-4.1-nano', // model deployment name
    max_tokens: 100 
});

// Print the full response
console.log('Full response:', result);

// Print just the message content from the response
console.log('Response content:', result.choices[0].message.content);
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
The following errors are automatically retried twice by default with a brief exponential backoff:

- Connection Errors
- 408 Request Timeout
- 429 Rate Limit
- `>=`500 Internal Errors

Use `maxRetries` to set/disable the retry behavior:

```typescript
// Configure the default for all requests:
const client = new OpenAI({
  maxRetries: 0, // default is 2
});

// Or, configure per-request:
await client.chat.completions.create({ messages: [{ role: 'user', content: 'How can I get the name of the current day in Node.js?' }], model: '' }, {
  maxRetries: 5,
});
```