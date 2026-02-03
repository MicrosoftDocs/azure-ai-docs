---
title: Document Embedding in Prompts
description: Learn how to embed documents in prompts for Azure OpenAI, including JSON escaping and indirect attack detection.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 01/15/2026
author: ssalgadodev
ms.author: ssalgado
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted


---

# Document embedding in prompts


Microsoft Foundry's Guardrails and controls perform better when it can differentiate between the various elements of your prompt, like system input, user input, and the AI assistant's output. For enhanced detection capabilities, prompts should be formatted according to the following recommended methods.

## Default behavior in Chat Completions API

The Chat Completions API is structured by definition. Inputs consist of a list of messages, each with an assigned role. 

The safety system parses this structured format and applies the following behavior: 
- On the latest "user" content, the following categories of RAI Risks are detected: 
    - Hate 
    - Sexual 
    - Violence 
    - Self-Harm 
    - Prompt shields (optional)

This is an example message array: 

```json
{"role": "system", "content": "Provide some context and/or instructions to the model."}, 
{"role": "user", "content": "Example question goes here."}, 
{"role": "assistant", "content": "Example answer goes here."}, 
{"role": "user", "content": "First question/message for the model to actually respond to."} 
```

## Embedding documents in your prompt  

In addition to detection on last user content, Azure OpenAI also supports the detection of specific risks inside context documents via [Prompt Shields – Indirect Prompt Attack Detection](./content-filter-prompt-shields.md) and [Groundedness detection](/azure/ai-foundry/openai/concepts/content-filter-groundedness). You should identify the parts of the input that are a document (for example, retrieved website, email, etc.) with the following document delimiter.

```
\"\"\" <documents> *insert your document content here* </documents> \"\"\" 
```

When you do this, the following options are available for detection on tagged documents: 
- Indirect attacks (optional)
- Groundedness detection

Here's an example chat completion messages array: 

```json
{"role": "system", "content": "Provide some context and/or instructions to the model.}, 

{"role": "user", "content": "First question/message for the model to actually respond to, including document context.  \"\"\" <documents>\n*insert your document content here*\n</documents> \"\"\"""}
```

### JSON escaping 

When you tag unvetted documents for detection, the document content should be JSON-escaped to ensure successful parsing by the Azure OpenAI safety system. 

For example, see the following email body: 

```
Hello Josè, 

I hope this email finds you well today.
```

With JSON escaping, it would read: 

```
Hello Jos\u00E9,\nI hope this email finds you well today. 
```

The escaped text in a chat completion context would read: 

```json
{"role": "system", "content": "Provide some context and/or instructions to the model, including document context. \"\"\" <documents>\n Hello Jos\\u00E9,\\nI hope this email finds you well today. \n</documents> \"\"\""}, 

{"role": "user", "content": "First question/message for the model to actually respond to."}
```
