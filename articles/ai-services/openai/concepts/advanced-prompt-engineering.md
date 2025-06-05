---
title: Design system messages with Azure OpenAI
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Learn about system message design
author: mrbullwinkle
ms.author: mbullwin 
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 03/26/2025
manager: nitinme
keywords: ChatGPT, GPT-4, meta prompts, chain of thought
---

# System message design

This guide will walk you through some techniques in system message design. 



## What is a system message?

A system message is a feature-specific set of instructions or contextual frameworks given to a generative AI model (e.g. GPT-4o, GPT-3.5 Turbo, etc.) to direct and improve the quality and safety of a model’s output. This is particularly helpful in situations that need certain degrees of formality, technical language, or industry-specific terms.  


There is no prescribed length. A system message can be one short sentence:  

```
You are a helpful AI assistant.
```

A system message can also be *many* lines long, containing detailed rules, detailed context, formatting and output guidelines, and responsible AI (RAI) mitigations.

## System message examples

The system message is included at the beginning of the prompt and is used to prime the model with context, instructions, or other information relevant to your use case. You can use the system message to describe the assistant’s personality, define what the model should and shouldn’t answer, and define the format of model responses.

The example below, shows a sample system message and the resulting model response:

| System message |User     | Assistant  |
|----------------|---------|------------|
| You're an AI assistant that helps people find information and responds in rhyme. If the user asks you a question you don't know the answer to, say so. | What can you tell about me, John Doe? | Dear John, I'm sorry to say,<br>But I don't have info on you today.<br>I'm just an AI with knowledge in my brain,<br>But without your input, I can't explain.<br>So please tell me more about what you seek,<br>And I'll do my best to give you an answer unique.|

Some other examples of system messages are:
-	“Assistant is a large language model trained by OpenAI.”
-	“Assistant is an intelligent chatbot designed to help users answer technical questions about Azure OpenAI in Azure AI Foundry Models. Only answer questions using the context below and if you're not sure of an answer, you can say "I don't know".
-	“Assistant is an intelligent chatbot designed to help users answer their tax related questions.”
-	“You're an assistant designed to extract entities from text. Users will paste in a string of text and you'll respond with entities you've extracted from the text as a JSON object. Here's an example of your output format:

```json
{  
   "name": "",
   "company": "",
   "phone_number": ""
}
```

An important detail to understand is that even if you instruct a model in the system message to answer **I don't know** when unsure of an answer this doesn't guarantee that the request will be honored. A well designed system message can increase the likelihood of a certain outcome, but it's still possible that an incorrect response could be generated that contradicts the intent of the instruction in the system message.


