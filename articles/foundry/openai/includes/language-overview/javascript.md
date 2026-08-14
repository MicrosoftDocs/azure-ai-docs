---
title: Azure OpenAI JavaScript support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI JavaScript and TypeScript support.
author: alvinashcraft
manager: mcleans
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 07/20/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

[Source code](https://github.com/openai/openai-node) | [Package](https://www.npmjs.com/package/openai) | [REST API reference](https://ai.azure.com/api-reference/) | [Azure OpenAI v1 guidance](../../api-version-lifecycle.md)

The examples require Node.js 20 or later. They were tested with `openai` 6.46.0 and `@azure/identity` 4.13.1. Use `openai` 5.18.0 or later when you pass a Microsoft Entra token provider as `apiKey`.

## Install the packages

Install the OpenAI and Azure Identity packages:

```bash
npm install openai @azure/identity
```

The command adds both packages to your project.

## Create a response with Microsoft Entra ID

Use `DefaultAzureCredential` and `getBearerTokenProvider` to authenticate without storing an API key. The token provider refreshes the access token when needed.

```typescript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import OpenAI from "openai";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default",
);
const openai = new OpenAI({ baseURL: endpoint, apiKey: tokenProvider });

async function main() {
  const response = await openai.responses.create({
    model: "gpt-5-mini",
    input: "Explain the purpose of an API in one sentence.",
  });
  console.log(response.output_text);
}

main().catch(console.error);
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`OpenAI` client and Azure OpenAI v1 authentication](https://github.com/openai/openai-node/blob/main/azure.md)

## Create a response with an API key

API keys aren't recommended for production use. Store the key in the `AZURE_OPENAI_API_KEY` environment variable instead of placing it in source code.

```bash
export AZURE_OPENAI_API_KEY="<your-api-key>"
```

Then create the client and request:

```typescript
import OpenAI from "openai";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
if (!apiKey) throw new Error("AZURE_OPENAI_API_KEY is required.");

const openai = new OpenAI({ baseURL: endpoint, apiKey });

async function main() {
  const response = await openai.responses.create({
    model: "gpt-5-mini",
    input: "Explain the purpose of an API in one sentence.",
  });
  console.log(response.output_text);
}

main().catch(console.error);
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`responses.create`](https://github.com/openai/openai-node/blob/main/examples/azure/responses.ts)

## Use Chat Completions

For new applications, use the Responses API. Use Chat Completions when you need its message-based interface or are maintaining an existing application.

```typescript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import OpenAI from "openai";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default",
);
const openai = new OpenAI({ baseURL: endpoint, apiKey: tokenProvider });

async function main() {
  const completion = await openai.chat.completions.create({
    model: "gpt-5-mini",
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: "Explain the purpose of an API." },
    ],
  });
  console.log(completion.choices[0]?.message.content ?? "No response returned.");
}

main().catch(console.error);
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Keeping `messages` inside the request provides the contextual typing required for the `role` values. If you define the array separately, declare it as `OpenAI.Chat.ChatCompletionMessageParam[]`.

Reference: [`chat.completions.create`](https://github.com/openai/openai-node/blob/main/examples/azure/chat.ts)

## Stream a response

Set `stream` to `true`, and process text delta events as the model generates them:

```typescript
import OpenAI from "openai";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
if (!apiKey) throw new Error("AZURE_OPENAI_API_KEY is required.");
const openai = new OpenAI({ baseURL: endpoint, apiKey });

async function main() {
  // Stream text as the model generates it.
  const stream = await openai.responses.create({
    model: "gpt-5-mini",
    input: "Explain the purpose of an API in one sentence.",
    stream: true,
  });
  for await (const event of stream) {
    if (event.type === "response.output_text.delta") {
      process.stdout.write(event.delta);
    }
  }
}

main().catch(console.error);
```

The following streamed output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`responses.create` streaming](https://github.com/openai/openai-node#streaming-responses)

## Handle errors and retries

The SDK automatically retries connection errors, timeouts, HTTP 408, 409, 429, and 5xx responses twice with exponential backoff. Set `maxRetries` on the `OpenAI` client to change this behavior. Catch `APIError` to inspect the HTTP status, request ID, and error details for a failed request.

The following example sets four retries and records the request ID for successful and failed requests:

```typescript
import OpenAI from "openai";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
if (!apiKey) throw new Error("AZURE_OPENAI_API_KEY is required.");
const openai = new OpenAI({ baseURL: endpoint, apiKey, maxRetries: 4 });

async function main() {
  try {
    // Send the request and record its request ID.
    const response = await openai.responses.create({
      model: "gpt-5-mini",
      input: "Explain the purpose of an API in one sentence.",
    });
    console.log(response.output_text);
    console.log(`Request ID: ${response._request_id}`);
  } catch (error) {
    if (error instanceof OpenAI.APIError) {
      console.error(`Status: ${error.status}; Request ID: ${error.requestID}`);
    }
    throw error;
  }
}

main().catch(console.error);
```

For a successful request, the following output is representative. The response text and request ID vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
Request ID: <request-id>
```

Reference: [Request IDs, errors, and retries](https://github.com/openai/openai-node#request-ids)

## More SDK examples

- [Use the Responses API](../../how-to/responses.md)
- [Generate embeddings](../../how-to/embeddings.md)
- [Analyze images](../../how-to/gpt-with-vision.md)
- [Fine-tune a model](../../how-to/fine-tuning.md)
