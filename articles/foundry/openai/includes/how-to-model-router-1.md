---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/10/2026
ms.custom: include, update-code4, dev-focus
ai-usage: ai-assisted
---

## Test model router with Foundry Responses and Chat Completions

Call model router the same way you call any OpenAI chat model. Set the `model` parameter to the name of your model router deployment. You can use the Microsoft Foundry SDK with the Responses API or the OpenAI SDK with the Chat Completions API, in either Python or JavaScript/TypeScript.

> [!NOTE]
> Install the required packages before you run the samples:
> - **Foundry Responses (Python)**: `pip install azure-ai-projects>=2.0.0 azure-identity`
> - **Foundry Responses (JavaScript/TypeScript)**: `npm install @azure/ai-projects @azure/identity`
> - **Chat Completions (Python)**: `pip install openai>=1.75.0`
> - **Chat Completions (JavaScript/TypeScript)**: `npm install openai @azure/identity`

# [Foundry Responses](#tab/foundry-responses)

**Python**

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-foundry-responses.py" id="foundry_responses":::

**JavaScript/TypeScript**

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

const project = new AIProjectClient(
  process.env["FOUNDRY_PROJECT_ENDPOINT"]!,
  new DefaultAzureCredential(),
);

// Get an OpenAI-compatible client that works with all Foundry models
const client = project.getOpenAIClient();

const response = await client.responses.create({
  model: process.env["MODEL_ROUTER_DEPLOYMENT_NAME"] || "model-router",
  input: "Explain retrieval-augmented generation in one sentence.",
});

// The "model" field reveals which underlying model was selected
console.log(`Responded model: ${response.model}`);
console.log(response.output_text);
```

# [Chat Completions](#tab/chat-completions)
**Python**

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions.py" id="chat_completion":::

**JavaScript/TypeScript**

```typescript
import { AzureOpenAI } from "openai";
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";

const endpoint = process.env["AZURE_OPENAI_ENDPOINT"]!;
const deploymentName =
  process.env["MODEL_ROUTER_DEPLOYMENT_NAME"] || "model-router";
const apiVersion = "2025-11-18";

const credential = new DefaultAzureCredential();
const azureADTokenProvider = getBearerTokenProvider(
  credential,
  "https://cognitiveservices.azure.com/.default",
);

const client = new AzureOpenAI({
  endpoint,
  azureADTokenProvider,
  apiVersion,
  deployment: deploymentName,
});

const completion = await client.chat.completions.create({
  model: deploymentName,
  messages: [
    {
      role: "user",
      content: "Explain retrieval-augmented generation in one sentence.",
    },
  ],
});

// The "model" field reveals which underlying model was selected
console.log(`Responded model: ${completion.model}`);
console.log(completion.choices[0].message.content);
```

---

> [!TIP]
> For the full runnable samples, see [Model Router samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/foundry-models/model-router) in the foundry-samples repository.

- Reference: [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses) (`responses.create`, both languages)
- Reference: [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat) (`chat.completions.create`, both languages)
- Reference: [`AIProjectClient`](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient) (Python)
- Reference: [`AIProjectClient`](/javascript/api/@azure/ai-projects/aiprojectclient) (JavaScript/TypeScript)
- Reference: [`AzureOpenAI` (OpenAI Python SDK)](https://pypi.org/project/openai/)
- Reference: [`AzureOpenAI` (OpenAI JavaScript/TypeScript SDK)](https://www.npmjs.com/package/openai)
