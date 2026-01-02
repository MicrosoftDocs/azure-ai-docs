---
title: Design system messages with Azure OpenAI
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Learn about system message design
author: mrbullwinkle
ms.author: mbullwin 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: conceptual 
ms.date: 12/6/2025
manager: nitinme
keywords: ChatGPT, GPT-4, meta prompts, chain of thought
monikerRange: 'foundry-classic || foundry'

---

# System message design

This guide describes concrete techniques for writing system messages, including when to use short constraints versus multi-line rule sets.  
<!-- Edited to replace low-signal introductory boilerplate with concise, concrete guidance per agent feedback. -->



## What is a system message?

A system message is a feature-specific set of instructions given to a generative AI model (for example, GPT‑4o or GPT‑3.5‑Turbo) that constrains output style, scope, and safety (for example, formality level, required terminology, or allowed topics).  
<!-- Edited to remove generic benefit language and focus on specific, actionable purpose. -->


There is no prescribed length; use one sentence for a single behavioral constraint, or multiple lines when defining rules, formatting requirements, or refusal behavior:  
<!-- Edited to emphasize actionable guidance on when to use short versus multi-line system messages. -->

```
You are a helpful AI assistant.
```

A system message can also be *many* lines long, containing detailed rules, detailed context, formatting and output guidelines, and responsible AI (RAI) mitigations.

## System message examples

The system message is included at the beginning of the prompt and is used to prime the model with context, instructions, or other information relevant to your use case. You can use the system message to describe the assistant’s personality, define what the model should and shouldn’t answer, and define the format of model responses.

The following example shows a sample system message and the resulting model response:

| System message |User     | Assistant  |
|----------------|---------|------------|
| You're an AI assistant that helps people find information and responds in rhyme. If the user asks you a question you don't know the answer to, say so. | What can you tell about me, John Doe? | Dear John, I'm sorry to say,<br>But I don't have info on you today.<br>I'm just an AI with knowledge in my brain,<br>But without your input, I can't explain.<br>So please tell me more about what you seek,<br>And I'll do my best to give you an answer unique.|

Some other examples of system messages are:
-	“Assistant is a large language model trained by OpenAI.”
-	“Assistant is an intelligent chatbot designed to help users answer technical questions about Azure OpenAI in Microsoft Foundry Models. Only answer questions using the context below and if you're not sure of an answer, you can say "I don't know".
-	“Assistant is an intelligent chatbot designed to help users answer their tax related questions.”
-	“You're an assistant designed to extract entities from text. Users will paste in a string of text and you'll respond with entities you've extracted from the text as a JSON object. Here's an example of your output format:

```json
{  
   "name": "",
   "company": "",
   "phone_number": ""
}
```

Even with explicit instructions (for example, “respond with *I don’t know* when uncertain”), compliance is probabilistic. System messages increase likelihood, not guarantees, and should be validated with testing and monitoring.  
<!-- Edited to reduce repetition and clearly state limitations with a concrete outcome. -->