---
title: Design system messages with Azure OpenAI
titleSuffix: Azure OpenAI Service
description: Learn about system message design with GPT-3, GPT-35-Turbo, and GPT-4 models.
author: mrbullwinkle
ms.author: mbullwin 
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 09/05/2024
manager: nitinme
keywords: ChatGPT, GPT-4, meta prompts, chain of thought
zone_pivot_groups: openai-prompt
---

# System messages

This guide will walk you through some techniques in system message design. 

While the principles of prompt engineering can be generalized across many different model types, certain models expect a specialized prompt structure. For Azure OpenAI GPT models, there are currently two distinct APIs where prompt engineering comes into play:

- Chat Completion API.
- Completion API.

Each API requires input data to be formatted differently, which in turn impacts overall prompt design. The **Chat Completion API** supports the GPT-35-Turbo and GPT-4 models. These models are designed to take input formatted in a [specific chat-like transcript](../how-to/chatgpt.md) stored inside an array of dictionaries.

The **Completion API** supports the older GPT-3 models and has much more flexible input requirements in that it takes a string of text with no specific format rules.

The techniques in this guide will teach you strategies for increasing the accuracy and grounding of responses you generate with a Large Language Model (LLM). It is, however, important to remember that even when using prompt engineering effectively you still need to validate the responses the models generate. Just because a carefully crafted prompt worked well for a particular scenario doesn't necessarily mean it will generalize more broadly to certain use cases. Understanding the [limitations of LLMs](/legal/cognitive-services/openai/transparency-note?context=/azure/ai-services/openai/context/context#limitations), is just as important as understanding how to leverage their strengths.


## System message examples

The system message is included at the beginning of the prompt and is used to prime the model with context, instructions, or other information relevant to your use case. You can use the system message to describe the assistant’s personality, define what the model should and shouldn’t answer, and define the format of model responses.

The example below, shows a sample system message and the resulting model response:

| System message |User     | Assistant  |
|----------------|---------|------------|
| You're an AI assistant that helps people find information and responds in rhyme. If the user asks you a question you don't know the answer to, say so. | What can you tell about me, John Doe? | Dear John, I'm sorry to say,<br>But I don't have info on you today.<br>I'm just an AI with knowledge in my brain,<br>But without your input, I can't explain.<br>So please tell me more about what you seek,<br>And I'll do my best to give you an answer unique.|

Some other examples of system messages are:
-	“Assistant is a large language model trained by OpenAI.”
-	“Assistant is an intelligent chatbot designed to help users answer technical questions about Azure OpenAI Service. Only answer questions using the context below and if you're not sure of an answer, you can say "I don't know".
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


