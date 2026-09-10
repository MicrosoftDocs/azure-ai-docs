---
title: Work with the Chat Completions API
titleSuffix: Azure OpenAI
description: Learn how to work with the Chat Completions API by using TypeScript.
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 08/24/2026
manager: mcleans
keywords: ChatGPT
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

## Set up

1. Install [Node.js 22](https://nodejs.org/download) or later.

1. Create a TypeScript project and install the required packages.

    ```shell
    npm init --yes
    npm install openai @azure/identity
    npm install --save-dev typescript tsx @types/node
    ```

1. Save each complete example as `chat.ts`, and then run it.

    ```shell
    npx tsx chat.ts
    ```

## Work with chat completion models

The following examples show the basic way to interact with models that use the Chat Completions API.

> [!NOTE]
> The [Responses API](../how-to/responses.md) uses the same chat style of interaction, but supports the latest features that aren't available with the older Chat Completions API.

# [Microsoft Entra ID](#tab/javascript-secure)

```typescript
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";
import OpenAI from "openai";

const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default",
);
const openai = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: tokenProvider,
});

const completion = await openai.chat.completions.create({
  model: "YOUR-DEPLOYMENT-NAME",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Who were the founders of Microsoft?" },
  ],
});

console.log(completion.choices[0]?.message.content);
console.log(`Finish reason: ${completion.choices[0]?.finish_reason}`);
```

# [API Key](#tab/javascript-key)

```typescript
import OpenAI from "openai";

const apiKey = process.env["AZURE_OPENAI_API_KEY"];
if (!apiKey) throw new Error("AZURE_OPENAI_API_KEY is required.");

const openai = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey,
});

const completion = await openai.chat.completions.create({
  model: "YOUR-DEPLOYMENT-NAME",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Who were the founders of Microsoft?" },
  ],
});

console.log(completion.choices[0]?.message.content);
console.log(`Finish reason: ${completion.choices[0]?.finish_reason}`);
```

---

The following output is representative. The exact wording might vary:

```output
Microsoft was founded by Bill Gates and Paul Allen.
Finish reason: stop
```

For the complete Azure OpenAI v1 client pattern, see the OpenAI Node [Azure Chat Completions example](https://github.com/openai/openai-node/blob/main/examples/azure/chat.ts).

Every response includes `finish_reason`. The possible values are:

* **stop**: The API returned complete model output.
* **length**: The model stopped because of `max_completion_tokens` or the token limit.
* **content_filter**: A content filter omitted content.
* **tool_calls**: The model called a tool.
* **function_call**: The model called a function. This value is deprecated.

For streaming responses, `finish_reason` is `null` until the final chunk completes the response.

Set `max_completion_tokens` high enough for the expected response. A higher value helps prevent the model from stopping before it reaches the end of the message.

## Work with the Chat Completions API

Chat completion models accept input formatted as a conversation. The `messages` parameter takes an array of message objects with a conversation organized by role. Type the array as `OpenAI.Chat.ChatCompletionMessageParam[]` when you define it outside the request.

The format of a basic chat completion is:

```typescript
const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  { role: "system", content: "Provide context or instructions to the model." },
  { role: "user", content: "The user's message goes here." },
];
```

A conversation with one example answer followed by a question looks like this:

```typescript
const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  { role: "system", content: "Provide context or instructions to the model." },
  { role: "user", content: "Example question goes here." },
  { role: "assistant", content: "Example answer goes here." },
  { role: "user", content: "First question for the model to answer." },
];
```

### System role

Include the system role, also known as the system message, at the beginning of the array. This message provides the initial instructions to the model. It can define the assistant's purpose, behavior, rules, or grounding data.

The system message is optional, but include at least a basic one to get the best results.

### Messages

After the system role, include a series of messages between the `user` and the `assistant`:

```typescript
const message: OpenAI.Chat.ChatCompletionUserMessageParam = {
  role: "user",
  content: "What is thermodynamics?",
};
```

End with a user message to indicate that it's the assistant's turn to respond. You can also include example messages between the user and the assistant for few-shot learning.

### Message prompt examples

Use these examples as starting points for prompts that you can adapt to your application.

#### Basic example

```typescript
const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  { role: "system", content: "You are a helpful assistant." },
  { role: "user", content: "Who were the founders of Microsoft?" },
];
```

#### Example with instructions

Use the system message to define boundaries for the model's responses:

```typescript
const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  {
    role: "system",
    content: `You help users answer tax-related questions.
Only answer questions about taxes.
If you don't know an answer, recommend the IRS website.`,
  },
  { role: "user", content: "When are my taxes due?" },
];
```

#### Use data for grounding

Include a small amount of relevant data in the system message to ground the model's answer:

```typescript
const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  {
    role: "system",
    content: `Answer only from this context. If the answer isn't present,
say "I don't know."

Context: Azure OpenAI provides REST API access to OpenAI models.`,
  },
  { role: "user", content: "What does Azure OpenAI provide?" },
];
```

For larger grounding datasets, use [embeddings](../tutorials/embeddings.md?tabs=command-line) or Azure AI Search to retrieve relevant information at request time.

#### Use few-shot learning

Include example user and assistant messages before the final question:

```typescript
const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  { role: "system", content: "You help users answer tax questions." },
  { role: "user", content: "When do I need to file my taxes?" },
  { role: "assistant", content: "Check the current deadline at irs.gov." },
  { role: "user", content: "How can I check my refund status?" },
];
```

#### Use chat completion for nonchat scenarios

The Chat Completions API also supports nonchat tasks, such as entity extraction:

```typescript
const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  {
    role: "system",
    content: "Extract names and companies. Return a JSON object.",
  },
  {
    role: "user",
    content: "Robert Smith is calling from Contoso Insurance.",
  },
];
```

## Create a basic conversation loop

The following example reads questions from the console, sends the complete conversation to the model, and adds each answer to the conversation history. Because the model has no memory, send the updated history with every request.

```typescript
import { stdin, stdout } from "node:process";
import { createInterface } from "node:readline/promises";
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";
import OpenAI from "openai";

const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default",
);
const openai = new OpenAI({
  baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  apiKey: tokenProvider,
});
const conversation: OpenAI.Chat.ChatCompletionMessageParam[] = [
  { role: "system", content: "You are a helpful assistant." },
];
const consoleInput = createInterface({ input: stdin, output: stdout });

while (true) {
  const question = await consoleInput.question("Q: ");
  if (!question.trim()) break;
  conversation.push({ role: "user", content: question });
  const response = await openai.chat.completions.create({
    model: "YOUR-DEPLOYMENT-NAME",
    messages: conversation,
  });
  const answer =
    response.choices[0]?.message.content ?? "No response returned.";
  conversation.push({ role: "assistant", content: answer });
  console.log(`\n${answer}\n`);
}
consoleInput.close();
```

When you run the code, enter a question at the `Q:` prompt. Enter a blank line to close the application.

## Manage conversations

The conversation loop runs until the conversation reaches the model's context window. The combined token count of `messages` and the requested output must stay within the model's limit. For current token limits, see the [models page](../../foundry-models/concepts/models-sold-directly-by-azure.md).
The OpenAI Node SDK reports token usage after each request through `response.usage`, but it doesn't include a tokenizer for estimating the next request. To estimate token usage before a request, choose a tokenizer that supports your model and encoding, and evaluate it before adoption.

For longer conversations, use one of these approaches:

* Remove the oldest complete user and assistant turns while preserving the system message. Keep a conservative safety margin because character or turn counts aren't exact token counts.
* Start a new conversation after a fixed number of turns.
* Use the [Responses API](../how-to/responses.md), which supports server-managed conversation state and truncation.

## Troubleshooting

### Failed to create completion as the model generated invalid Unicode output

- **Error code:** 500
- **Error message:** `Failed to create completion as the model generated invalid Unicode output`
- **Workaround:** For models that support it, set `temperature` to less than 1. The OpenAI Node SDK retries connection errors and selected HTTP errors twice by default. Set `maxRetries` on the `OpenAI` client to change this behavior.

### Common errors

- **401/403 (authentication)**: Verify the API key, or confirm that the signed-in identity can access the Azure OpenAI resource.
- **400/404 (deployment not found)**: Confirm that `model` matches the deployment name.
- **Invalid URL**: Confirm that `baseURL` ends with `/openai/v1/`.