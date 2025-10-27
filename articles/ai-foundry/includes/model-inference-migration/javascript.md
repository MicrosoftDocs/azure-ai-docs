## Benefits of migrating

Migrating to the OpenAI v1 SDK provides several advantages:

- **Unified API**: Use the same SDK for both OpenAI and Azure OpenAI endpoints
- **Latest features**: Access to the newest OpenAI features without waiting for Azure-specific updates
- **Simplified authentication**: Built-in support for both API key and Microsoft Entra ID authentication
- **No API versioning**: The v1 API eliminates the need to frequently update `api-version` parameters
- **Broader model support**: Works with Azure OpenAI in Foundry Models and other Foundry Models from providers like DeepSeek and Grok

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

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const client = ModelClient(
    "https://<resource>.services.ai.azure.com/models", 
    new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL)
);
```

# [OpenAI v1 SDK](#tab/openai)

```javascript
import { OpenAI } from "openai";

const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: process.env.AZURE_OPENAI_API_KEY
});
```

---

With Microsoft Entra ID:

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

# [OpenAI v1 SDK](#tab/openai)

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

---

## Responses API

For Azure OpenAI models, use the Responses API for chat completions:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support the Responses API. Use chat completions instead.

# [OpenAI v1 SDK](#tab/openai)

```javascript
const result = await client.responses.stream({
    model: 'gpt-4o-mini', // Your deployment name
    input: 'This is a test.',
}).finalResponse();

console.log('Response content:', result.choices[0].message.content);
```

---

## Chat completions

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
const response = await client.path("/chat/completions").post({
    body: {
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "What is Azure AI?" }
        ],
        model: "gpt-4o-mini" // Optional for single-model endpoints
    }
});

console.log(response.body.choices[0].message.content);
```

# [OpenAI v1 SDK](#tab/openai)

```javascript
const completion = await client.chat.completions.create({
    model: "gpt-4o-mini", // Required: your deployment name
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "What is Azure AI?" }
    ]
});

console.log(completion.choices[0].message.content);
```

---

### Streaming

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
const response = await client.path("/chat/completions").post({
    body: {
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "Write a poem about Azure." }
        ],
        model: "gpt-4o-mini",
        stream: true
    }
}).asNodeStream();

for await (const chunk of response) {
    if (chunk.choices && chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

# [OpenAI v1 SDK](#tab/openai)

```javascript
const stream = await client.chat.completions.create({
    model: "gpt-4o-mini",
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

---

## Embeddings

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

# [OpenAI v1 SDK](#tab/openai)

```javascript
const response = await client.embeddings.create({
    input: "Your text string goes here",
    model: "text-embedding-3-small" // Your deployment name
});

const embedding = response.data[0].embedding;
```

---

## Image generation

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support image generation. Use OpenAI SDK instead.

# [OpenAI v1 SDK](#tab/openai)

```javascript
const response = await client.images.generate({
    model: "dall-e-3", // Your deployment name
    prompt: "a happy monkey eating a banana, in watercolor",
    n: 1,
    size: "1024x1024",
    quality: "standard"
});

const imageUrl = response.data[0].url;
console.log(`Generated image available at: ${imageUrl}`);
```

---

## Error handling

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```javascript
try {
    const response = await client.path("/chat/completions").post({
        body: {
            messages: [{ role: "user", content: "Hello" }],
            model: "gpt-4o-mini"
        }
    });
} catch (error) {
    console.error(`Request failed: ${error.statusCode}`);
    console.error(`Error message: ${error.message}`);
}
```

# [OpenAI v1 SDK](#tab/openai)

```javascript
import { OpenAI } from "openai";

try {
    const completion = await client.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: "Hello" }]
    });
} catch (error) {
    if (error instanceof OpenAI.APIError) {
        console.error(`API error: ${error.status} - ${error.message}`);
    } else {
        console.error(`Unexpected error: ${error}`);
    }
}
```

---
