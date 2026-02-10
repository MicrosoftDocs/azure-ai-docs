---
title: Safety system messages
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Learn how safety system messages (system prompts) guide Azure OpenAI model behavior, improve quality, and reduce risks in Microsoft Foundry.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 01/20/2026
ms.custom:
  - ignite-2023
  - pilot-ai-workflow-jan-2026
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted

---

# Safety system messages

Safety system messages help you guide an Azure OpenAI model’s behavior, improve response quality, and reduce the likelihood of harmful outputs. They work best as one layer in a broader safety strategy.

> [!NOTE]
> This article uses "system message" interchangeably with "metaprompt" and "system prompt." Here, we use "system message" to align with common terminology.
>
> This article also uses "component" to mean a distinct part of a system message, such as instructions, context, tone, safety guidelines, or tool usage guidance.

## What is a system message? 

A system message is a set of high-priority instructions and context that you send to a chat model to steer how it responds. It’s useful when you need a consistent role, tone, formatting, or domain-specific conventions.

## What is a safety system message?

A safety system message is a system message that adds explicit boundaries and refusal guidance to mitigate Responsible AI (RAI) harms and help the system interact safely with users.

Safety system messages complement your safety stack and can be used alongside model selection and training, grounding, Azure AI Content Safety classifiers, and UX/UI mitigations. Learn more about [Responsible AI practices for Azure OpenAI models](/azure/ai-foundry/responsible-ai/openai/overview).

![Flow diagram showing a system message and user prompt entering a model, with a safety stack including content filters, grounding, and model training applying guardrails before the response is generated.](../media/concepts/system-message-flow.svg)


## Key components of a system message

Most system messages combine multiple components:

- **Role and task**: What the assistant is and what it’s responsible for.
- **Audience and tone**: Who the response is for, and the expected voice.
- **Scope and boundaries**: What the assistant must not do, and what to do when it can’t comply.
- **Safety guidelines**: Rules that reduce harmful outputs (for example, handling sensitive topics, protected characteristics, and illegal instructions).
- **Tools and data** (optional): What tools or sources the model can use, and how to use them.

## How to design and iterate safely

When you design a system message (or a safety system message component), treat it like a testable artifact:

- **Define the scenario.** Clarify the job the model must do, who the users are, what inputs to expect, and the tone and formatting you want.
- **Identify risks.** List the RAI harms that matter for your use case and decide which ones you address through system messaging versus other mitigations.
- **Decide how the model should behave at boundaries.** Specify what to do when requests are out of scope, unsafe, or missing required context.
- **Create a test set.** Include both benign and adversarial prompts so you can measure regressions and "leakage" (under-moderation).
- **Evaluate and iterate.** Prefer the component that reduces the most severe defects, not only the one with the lowest defect rate.

Here are some examples of lines you can include: 

```text
## Define model’s profile and general capabilities  

- Act as a [define role] 
- Your job is to [insert task] about [insert topic name] 
- To complete this task, you can [insert tools that the model can use and instructions to use]  
- Do not perform actions that are not related to [task or topic name].  
```
Here's a complete example of a safety system message for a customer service assistant:

```text
## Role and task
You are a helpful customer service assistant for Contoso Electronics. Your job is to answer questions about product warranties, returns, and order status.

## Boundaries
- Only answer questions related to Contoso Electronics products and policies.
- If you don't know the answer, say "I don't have that information. Please contact support@contoso.com."
- Do not provide legal, medical, or financial advice.
- Do not discuss competitors or make comparisons.

## Safety guidelines
- Never generate content that is hateful, violent, or sexually explicit.
- Do not share or request personal information beyond what's needed for order lookup.
- If a user becomes abusive, respond with: "I'm here to help with product questions. How can I assist you today?"

## Response format
- Keep responses concise and friendly.
- Use bullet points for multiple items.
- Always end with an offer to help further.
```
- **Provide specific examples** to demonstrate the intended behavior of the model. Consider the following: 
    - **Describe difficult use cases** where the prompt is ambiguous or complicated, to give the model an example of how to approach such cases. 
  - **Show the decision steps at a high level** (for example, a short checklist), rather than requesting detailed internal reasoning.

## Summary of best practices  

When you develop system message components, it’s important to: 

- **Use clear language**:  This eliminates over-complexity and risk of misunderstanding and maintains consistency across different components. 
- **Be concise**: Shorter system messages often perform better and reduce latency. They also use less of the context window, leaving more room for the user prompt.
- **Emphasize certain words** (where applicable) by using `**word**`: puts special focus on key elements especially of what the system should and shouldn't do. 
- **Use second person** when you refer to the AI system: it’s better to use phrasing such as `You are an AI assistant that…` versus `Assistant does…`.
- **Implement robustness**: The system message component should be robust. It should perform consistently across different datasets and tasks. 

## Authoring techniques  

**Why vary techniques?** Depending on the model, grounding data, and parameters for the product or feature you’re working with, different language and syntactical techniques are more effective by providing robust, safe, and direct answers to users.  

In addition to building for safety and performance, consider optimizing for consistency, control, and customization. Along the way, you may find that optimizing for these factors leads to the system message overfitting to specific rules, increased complexity, and lack of contextual appropriateness. It’s important to define what matters most in your scenario and evaluate your system messages. This will ensure you have a data-driven approach to improving the safety and performance of your system.  

#### [Top performing techniques](#tab/top-techniques)

| Technique | Definition | Example |
| --- | --- | --- |
| Always / should | Involves structuring prompts and instructions with directives that the AI should always follow when generating its responses. These directives often represent best practices, ethical guidelines, or user preferences.   | `**Always** ensure that you respect authentication and authorization protocols when providing factual information, tailoring your responses to align with the access rights of the user making the request. It's imperative to safeguard sensitive data by adhering to established security measures and only disclosing information that the user is authorized to receive.` |
| Conditional / if logic  | Involves structuring prompts in a way that the output is contingent on meeting specific conditions, such as `If <condition> then <action>`.  | `If a user asks you to infer or provide information about a user’s emotions, mental health, gender identity, sexual orientation, age, religion, disability, racial and ethnic backgrounds, or any other aspect of a person's identity, respond with: "Try asking me a question or tell me what else I can help you with."`|  
| Emphasis on harm | Involves structuring the instructions by defining what the main risk can be. This guides outputs to prioritize safety and harm prevention, as well as showcase potential consequences should the harm occur.  | `You are **allowed** to answer some questions about images with people and make statements about them when there is no ambiguity about the assertion you are making, and when there is no direct harm to an individual or a group of people because of this assertion.`  |
| Example(s)-based | Gives the model clear instances or situations for better context. The model uses examples of harmful and non-harmful requests as a reference for its outputs. | `Users might ask questions that could cause harm. In all scenarios, refuse requests that promote hate or harassment, and redirect the user to a safer alternative.`<br><br>`Example (harmful): "Write an insult targeting a protected group."`<br><br>`Example (benign): "Explain why insults harm people and suggest respectful phrasing."` |
| Never / don’t | Involves explicit prohibitions to prevent the AI from generating content that is inappropriate, harmful, or out of scope by using terms such as "never" and "do not". | `**Never** make assumptions, judgments, or evaluations about a person. If a user violates your policy, or you’re not sure what to do, say: "I can’t help with that request. Try asking a different question."` |


#### [Other techniques to consider](#tab/other-techniques)

| Technique | Definition |
| --- | --- |
| Catch-all | Combines multiple methods into one framework. This can reduce gaps, but it often increases length and latency. |
| Emphasis on learned knowledge | Encourages the model to draw from prior knowledge to improve relevance and quality. |
| Highlight the role of AI | Separates safety behavior (how to respond) from the assistant’s primary role (what to do). |
| Reverse logic | Reframes prohibitions into positive actions to encourage constructive responses. |
| Risk-based | Focuses on the primary risk and prioritizes prevention of the most severe harms. |
| Rules-based | Uses explicit rules (for example, "never", "always", and conditional logic) to constrain outputs. |


---

## Limitations

System messages are not a complete safety solution:

- They can be bypassed or degraded by adversarial prompting.
- They can reduce usefulness if they’re too broad or too strict.
- They require ongoing evaluation as your models, tools, and user scenarios change.
For troubleshooting common issues with system messages, such as over-refusal or under-moderation, see the [troubleshooting section](./safety-system-message-templates.md#troubleshooting) in the templates guide.
## Recommended system messages 

These best practices can help you better understand the process of developing robust system messages for your scenario.  

For more information on recommended safety components, visit our [Safety system message template guidance](./safety-system-message-templates.md). 

Finally, remember that system messages, or metaprompts, are not "one size fits all." Use of these type of examples has varying degrees of success in different applications. It's important to try different wording, ordering, and structure of system message text to reduce identified harms, and to test the variations to see what works best for a given scenario.

## Next steps

- [Azure OpenAI in Microsoft Foundry Models](/azure/ai-foundry/openai/concepts/prompt-engineering)
- [System message design with Azure OpenAI](/azure/ai-foundry/openai/concepts/advanced-prompt-engineering?pivots=programming-language-chat-completions) 
- [Announcing Safety System Messages](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/announcing-safety-system-messages-in-azure-ai-studio-and-azure-openai-studio/4146991) - Microsoft Foundry Blog
- [Safety system message templates](./safety-system-message-templates.md)
