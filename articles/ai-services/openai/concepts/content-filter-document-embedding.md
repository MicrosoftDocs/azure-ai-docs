---
title: Document Embedding in Prompts
description: Learn how to embed documents in prompts for Azure OpenAI, including JSON escaping and indirect attack detection.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-services
ms.topic: conceptual
ms.date: 05/07/2025
ms.author: pafarley
---

# Document embedding in prompts

A key aspect of Azure OpenAI's Responsible AI measures is the content safety system. This system runs alongside the core GPT model to monitor any irregularities in the model input and output. Its performance is improved when it can differentiate between various elements of your prompt like system input, user input, and AI assistant's output. 
 
For enhanced detection capabilities, prompts should be formatted according to the following recommended methods.

## Chat Completions API

The Chat Completion API is structured by definition. It consists of a list of messages, each with an assigned role. 

The safety system parses this structured format and applies the following behavior: 
- On the latest “user” content, the following categories of RAI Risks will be detected: 
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

In addition to detection on last user content, Azure OpenAI also supports the detection of specific risks inside context documents via Prompt Shields – Indirect Prompt Attack Detection. You should identify parts of the input that are a document (for example, retrieved website, email, etc.) with the following document delimiter.  

```
\"\"\" <documents> *insert your document content here* </documents> \"\"\" 
```

When you do so, the following options are available for detection on tagged documents: 
- On each tagged “document” content, detect the following categories: 
    - Indirect attacks (optional) 

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