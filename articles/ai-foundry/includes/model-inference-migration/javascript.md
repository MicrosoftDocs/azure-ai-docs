---
title: JavaScript file for model inference SDK to OpenAI SDK migration
description: Include file
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 11/05/2025
ms.custom: include
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
    'https://cognitiveservices.azure.com/.default'
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
        { role: "user", content: "What is Azure AI?" }
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
            { role: "user", content: "What is Azure AI?" }
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

## Embeddings

# [OpenAI SDK](#tab/openai)

```javascript
import OpenAI from "openai";
import { getBearerTokenProvider, DefaultAzureCredential } from "@azure/identity";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');
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