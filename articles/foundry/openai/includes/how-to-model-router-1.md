---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/09/2026
ms.custom: include, update-code1, dev-focus
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

## Keep Chat Completions requests on the same model (preview)

The Chat Completions API is stateless, so your application sends the conversation history with each request. By default, model router evaluates each request independently and might select a different underlying model for a later turn. Session affinity lets your application identify related requests and asks model router to try the same eligible model first.

Session affinity can improve the opportunity for prompt-cache reuse when consecutive requests have overlapping prompt prefixes. It doesn't inspect cache state or guarantee a cache hit.

### Configure session affinity

After your application reads the endpoint, API key, and deployment name, create the client with the preview feature header. Then create an opaque, application-owned session ID that doesn't contain secrets or personal information:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-session-affinity.py" id="session_affinity_enable":::

Use the same session ID for every turn in one conversation. Use a different session ID for an unrelated conversation.

You can alternatively provide the application-owned identifier in the `x-ms-session-id` request header. When a request contains valid identifiers in both locations, `routing_config.session_affinity.session_id` takes precedence. A session ID must contain 1 through 256 Unicode code points, including at least one non-whitespace character. Model router ignores an invalid body identifier and tries a valid header identifier. If neither identifier is valid, Chat Completions uses normal routing.

### Send related conversation turns

Send the first request, append its response and the next user message to the conversation history, and send the next request with the same session affinity configuration:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-session-affinity.py" id="session_affinity_turns":::

Model router creates or updates a model association only after a successful request. The association expires after 30 minutes without a successful create or update.

### Verify the affinity decision

Inspect `model_selection_details.model_router_details.session_affinity` to determine how model router applied affinity:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-session-affinity.py" id="session_affinity_extract":::

A typical run produces output similar to the following example:

```output
--- First turn ---
Serving model: <model-name>
Affinity mode: sticky
Affinity source: session_id_payload
Affinity decision: initialize
Response:
<first-response>

--- Second turn ---
Serving model: <model-name>
Affinity mode: sticky
Affinity source: session_id_payload
Affinity decision: retain
Response:
<second-response>
```

The first successful request typically returns `initialize`. A later request returns `retain` when the associated model serves the response. It returns `switch` when eligibility or fallback causes another model to serve the response. Policy, safety, capability, quota, availability, and fallback requirements take precedence over affinity.

To disable affinity for one request, set `routing_config.session_affinity.mode` to `none`. Model router uses normal routing for that request and doesn't read or update the model association. The response reports `mode` as `none` and omits `source` and `decision`.

Session affinity is best-effort. An affinity lookup or persistence failure doesn't fail inference. In that case, model router uses normal routing and omits the complete `session_affinity` response object. Session affinity doesn't store conversation content, prevent fallback, or provide adaptive cache-aware switching.

For the response fields and fallback diagnostics, see [Monitor model router](../how-to/monitor-model-router.md#interpret-session-affinity-metadata).
