---
title: Use structured outputs with JavaScript and TypeScript
description: Learn how to use structured outputs with the OpenAI JavaScript and TypeScript library for Azure OpenAI.
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 08/24/2026
zone_pivot_groups: structured-outputs
ms.custom: classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

## Prerequisites

- An Azure subscription.
- An Azure OpenAI resource with a `gpt-5-mini` model deployment. To create a resource and deploy a model, see [Create a resource and deploy a model with Azure OpenAI](/azure/ai-foundry/openai/how-to/create-resource).
- Your Azure OpenAI v1 endpoint, such as `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/`.
- For Microsoft Entra ID authentication, an identity with the `Cognitive Services OpenAI User` role assigned to the Azure OpenAI resource. Install the [Azure CLI](/cli/azure/install-azure-cli), and then run `az login`.
- For API key authentication, an Azure OpenAI resource key stored in the `AZURE_OPENAI_API_KEY` environment variable.

## Set up

The examples require Node.js 22 or later. Create a project, configure ECMAScript modules, and install the OpenAI, Zod, and Azure Identity packages:

```shell
npm init --yes
npm pkg set type=module
npm install openai zod @azure/identity
npm install --save-dev typescript tsx @types/node
```

For TypeScript, save each example as `structured-outputs.ts`, and then run it:

```shell
npx tsx structured-outputs.ts
```

For JavaScript, save each example as `structured-outputs.mjs`, and then run it:

```shell
node structured-outputs.mjs
```

## Use structured outputs with Chat Completions

Define the output structure with Zod. The `zodResponseFormat` helper converts the Zod object to a strict JSON Schema and validates the model response. All properties in the Zod object are required unless you define a nullable union.

# [Microsoft Entra ID](#tab/javascript-secure)

```typescript
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";
import OpenAI from "openai";
import { zodResponseFormat } from "openai/helpers/zod";
import { z } from "zod/v4";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default",
);
const openai = new OpenAI({ baseURL: endpoint, apiKey: tokenProvider });
const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const completion = await openai.chat.completions.parse({
  model: "gpt-5-mini",
  messages: [
    { role: "system", content: "Extract the event information." },
    {
      role: "user",
      content: "Alice and Bob are going to a science fair on Friday.",
    },
  ],
  response_format: zodResponseFormat(CalendarEvent, "calendar_event"),
});
const message = completion.choices[0]?.message;
if (message?.refusal) throw new Error(`Request refused: ${message.refusal}`);
if (!message?.parsed) throw new Error("The response wasn't parsed.");
console.log(message.parsed);
```

# [API Key](#tab/javascript-key)

```typescript
import OpenAI from "openai";
import { zodResponseFormat } from "openai/helpers/zod";
import { z } from "zod/v4";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
if (!apiKey) throw new Error("AZURE_OPENAI_API_KEY is required.");
const openai = new OpenAI({ baseURL: endpoint, apiKey });
const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const completion = await openai.chat.completions.parse({
  model: "gpt-5-mini",
  messages: [
    { role: "system", content: "Extract the event information." },
    {
      role: "user",
      content: "Alice and Bob are going to a science fair on Friday.",
    },
  ],
  response_format: zodResponseFormat(CalendarEvent, "calendar_event"),
});
const message = completion.choices[0]?.message;
if (message?.refusal) throw new Error(`Request refused: ${message.refusal}`);
if (!message?.parsed) throw new Error("The response wasn't parsed.");
console.log(message.parsed);
```

---

The output is similar to:

```output
{
  name: 'Science Fair',
  date: 'Friday',
  participants: [ 'Alice', 'Bob' ]
}
```

## Use structured outputs with the Responses API

For the Responses API, pass the result of `zodTextFormat` under `text.format`. The parsed value is available through `output_parsed` after the response completes.

```typescript
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod/v4";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default",
);
const openai = new OpenAI({ baseURL: endpoint, apiKey: tokenProvider });
const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const response = await openai.responses.parse({
  model: "gpt-5-mini",
  input:
    "Extract the event information: Alice and Bob are going to a science " +
    "fair on Friday.",
  text: { format: zodTextFormat(CalendarEvent, "calendar_event") },
});
if (response.status !== "completed") {
  const details = response.error ?? response.incomplete_details;
  throw new Error(JSON.stringify(details));
}
const refusal = response.output
  .flatMap((item) => item.type === "message" ? item.content : [])
  .find((content) => content.type === "refusal");
if (refusal) throw new Error(`Request refused: ${refusal.refusal}`);
if (!response.output_parsed) throw new Error("The response wasn't parsed.");
console.log(response.output_parsed);
```

The output is similar to:

```output
{
  name: 'Science Fair',
  date: 'Friday',
  participants: [ 'Alice', 'Bob' ]
}
```

## Use structured outputs for function calling

Use `zodFunction` to create a strict function tool and parse its arguments. Azure OpenAI doesn't support parallel function calls with structured outputs, so set `parallel_tool_calls` to `false`.

```typescript
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";
import OpenAI from "openai";
import { zodFunction } from "openai/helpers/zod";
import { z } from "zod/v4";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default",
);
const openai = new OpenAI({ baseURL: endpoint, apiKey: tokenProvider });
const DeliveryRequest = z.object({ order_id: z.string() });

const completion = await openai.chat.completions.parse({
  model: "gpt-5-mini",
  messages: [
    { role: "system", content: "Use the supplied tool to help the user." },
    { role: "user", content: "When will order 12345 be delivered?" },
  ],
  tools: [zodFunction({
    name: "get_delivery_date",
    description: "Get the delivery date for an order.",
    parameters: DeliveryRequest,
  })],
  parallel_tool_calls: false,
});
const toolCall = completion.choices[0]?.message.tool_calls?.[0];
if (toolCall?.type !== "function") {
  throw new Error("No function call returned.");
}
console.log(toolCall.function.parsed_arguments);
```

The output is similar to:

```output
{ order_id: '12345' }
```

For the underlying request shapes without Zod, use the JSON Schema examples in the REST language option.