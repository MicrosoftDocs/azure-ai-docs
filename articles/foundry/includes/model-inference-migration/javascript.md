---
title: JavaScript file for model inference SDK to OpenAI SDK migration
description: Include file
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 06/04/2026
ms.custom: include
ai-usage: ai-assisted
---

## Setup

Install the OpenAI SDK:

```bash
npm install openai
```

For Microsoft Entra ID authentication, also install:

```bash
npm install @azure/identity
```

## Client configuration

With API key authentication:

# [OpenAI SDK](#tab/openai)

```javascript
import { OpenAI } from "openai";

const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: process.env.AZURE_OPENAI_API_KEY
});
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const client = ModelClient(
    "https://<resource>.services.ai.azure.com/models", 
    new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL)
);
```

---

With Microsoft Entra ID authentication:

# [OpenAI SDK](#tab/openai)

```javascript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://ai.azure.com/.default'
);

const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { DefaultAzureCredential } from "@azure/identity";

const clientOptions = { 
    credentials: { 
        scopes: ["https://cognitiveservices.azure.com/.default"] 
    } 
};

const client = ModelClient(
    "https://<resource>.services.ai.azure.com/models", 
    new DefaultAzureCredential(),
    clientOptions
);
```

---

## Chat completions

# [OpenAI SDK](#tab/openai)

```javascript
const completion = await client.chat.completions.create({
    model: "DeepSeek-V3.1", // Required: your deployment name
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "How many languages are in the world?" }
    ]
});

console.log(completion.choices[0].message.content);
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
const response = await client.path("/chat/completions").post({
    body: {
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "How many languages are in the world?" }
        ],
        model: "DeepSeek-V3.1" // Optional for single-model endpoints
    }
});

console.log(response.body.choices[0].message.content);
```

---


### Streaming

# [OpenAI SDK](#tab/openai)

```javascript
const stream = await client.chat.completions.create({
    model: "DeepSeek-V3.1",
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "Write a poem about Azure." }
    ],
    stream: true
});

for await (const chunk of stream) {
    if (chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
const response = await client.path("/chat/completions").post({
    body: {
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "Write a poem about Azure." }
        ],
        model: "DeepSeek-V3.1",
        stream: true
    }
}).asNodeStream();

for await (const chunk of response) {
    if (chunk.choices && chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

---

## Responses

The Responses API is OpenAI's stateful interface that returns a structured `output` array containing message, tool call, and reasoning items.

# [OpenAI SDK](#tab/openai)

```javascript
const response = await client.responses.create({
    model: "DeepSeek-V3.1", // Required: your deployment name
    input: "How many languages are in the world?",
    max_output_tokens: 2000,
});

console.log(response.output_text);
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To call it, use the OpenAI SDK.

---

### Reasoning

> [!NOTE]
> This information on reasoning content doesn't apply to Azure OpenAI models. Azure OpenAI reasoning models use the [reasoning summaries feature](../../openai/how-to/reasoning.md#reasoning-summary).

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind them. The Responses API surfaces this as a structured `reasoning` output item whose `summary[].text` contains the model's thinking, alongside the final answer.

# [OpenAI SDK](#tab/openai)

```javascript
const response = await client.responses.create({
    model: "DeepSeek-R1-0528", // Required: your deployment name
    input: "How many languages are in the world?",
    max_output_tokens: 2000,
});

// Walk response.output for items of type "reasoning" and join summary[].text.
const parts = [];
for (const item of response?.output ?? []) {
    if (item?.type !== "reasoning") continue;
    for (const s of item?.summary ?? []) {
        if (s?.text) parts.push(s.text);
    }
}
const reasoningSummary = parts.join("\n").trim();

console.log("Thinking:", reasoningSummary);
console.log("Answer:  ", response.output_text);
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
Answer:   There are approximately 7,000 languages spoken around the world today.
```

[!INCLUDE [reasoning-tokens-known-issue](reasoning-tokens-known-issue.md)]

# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To get reasoning content, call the chat completions API instead. The reasoning is included in the message content wrapped in `<think>` and `</think>` tags, which you can extract with a regex match.

```javascript
const response = await client.path("/chat/completions").post({
    body: {
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "How many languages are in the world?" }
        ],
        model: "DeepSeek-R1-0528" // Optional for single-model endpoints
    }
});

const content = response.body.choices[0].message.content;
const match = content.match(/<think>(.*?)<\/think>(.*)/s);

if (match) {
    console.log("Thinking:", match[1].trim());
    console.log("Answer:  ", match[2].trim());
} else {
    console.log("Response:", content);
}
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
Answer:   There are approximately 7,000 languages spoken around the world today.
```

---

When you make multi-turn conversations, avoid sending the reasoning content in the chat history because reasoning tends to generate long explanations.

## Embeddings

# [OpenAI SDK](#tab/openai)

```javascript
import OpenAI from "openai";
import { getBearerTokenProvider, DefaultAzureCredential } from "@azure/identity";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://ai.azure.com/.default');
const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const embedding = await client.embeddings.create({
  model: "text-embedding-3-large", // Required: your deployment name
  input: "The quick brown fox jumped over the lazy dog",
  encoding_format: "float",
});

console.log(embedding);
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const client = ModelClient(
    "https://<resource>.services.ai.azure.com/models",
    new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL)
);

const response = await client.path("/embeddings").post({
    body: {
        input: ["Your text string goes here"],
        model: "text-embedding-3-small"
    }
});

const embedding = response.body.data[0].embedding;
```



---