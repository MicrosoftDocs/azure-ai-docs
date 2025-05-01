---
title: Safety system messages 
titleSuffix: Azure OpenAI Service
description: Learn about how to construct system messages also know as metaprompts to guide an AI system's behavior.
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 03/27/2025
ms.custom:
  - ignite-2023
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Safety system messages 

This article recommends frameworks and examples for writing effective system messages to guide AI models’ behavior, improve output quality and accuracy, and mitigate harms. Alongside other mitigation techniques, system messages provide a more precise way of determining safe outputs.  

> [!NOTE]
> System message is used interchangeably with "metaprompt," and "system prompt." Here, we use "system message" to align with industry taxonomy and standards.
>
> Additionally, we use the term "component" - a component is a distinct part that contributes to the overall structure and function of the system message. Examples include instructions, context, tone, safety guidelines, and tools.  

## What is a system message? 

A system message is a feature-specific set of instructions or contextual frameworks given to a generative AI model (for example, GPT4-o, GPT3.5 Turbo, etc.) to direct and improve the quality and safety of a model’s output. This is helpful in situations that need certain degrees of formality, technical language, or industry-specific terms.  


There is no prescribed length. A system message can be one short sentence:  

```
You are a helpful AI assistant.
```

A system message can also be *many* lines long, containing detailed rules, detailed context, formatting and output guidelines, and responsible AI (RAI) mitigations.

## Safety system message examples

Safety system messages are a type of system message that provides explicit instructions to mitigate against potential RAI harms and guide systems to interact safely with users. Safety system messages complement your safety stack and can be added alongside foundation model training, data grounding, Azure AI Content Safety classifiers, and UX/UI interventions. Learn more about [Responsible AI practices for Azure OpenAI models](/legal/cognitive-services/openai/overview?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext). 

While this technique is effective, it is still fallible, and most safety system messages need to be used in combination with other safety mitigations.  

## Step-by-step authoring best practices  

To develop a system message or safety system message component, we recommend these steps: 

### 1/ Define the scenario 

Define the model’s profile, capabilities, and limitations for your scenario 

- **Define the specific task(s)** you would like the model to complete. Who are the users? What type of inputs will they provide?  What should the model do with these inputs? Are there specific modality/modalities that are applicable?  
- **Consider the model type.** Determine what type of model you should be using based on your use (for example, multimodal vs LLM etc.), which may reflect model considerations for your system (such as performance, cost, risks etc.), and assess whether the type of model affects the system message. 
- **Define how the model should complete the tasks.** If applicable, this could include other tools (like APIs, code, plug-ins, etc.) the model should use.  
- **Define the scope and limitations** of the model’s performance. Provide clear instructions on how the model should respond when faced with any limitations. For example, define how the model should respond if prompted on subjects or for uses outside of what you want the system to do.  
- **Define the tone** the model should exhibit in its responses. 

Here are some examples of lines you can include: 

```
## Define model’s profile and general capabilities  

- Act as a [define role] 
- Your job is to [insert task] about [insert topic name] 
- To complete this task, you can [insert tools that the model can use and instructions to use]  
- Do not perform actions that are not related to [task or topic name].  
```

- **Provide specific examples** to demonstrate the intended behavior of the model. Consider the following: 
    - **Describe difficult use cases** where the prompt is ambiguous or complicated, to give the model an example of how to approach such cases. 
    - **Show the potential chain-of-thought reasoning** to better inform the model on the steps it should take to achieve the desired outcomes. 


### 2/ Define your potential risks 

Based on your use case and modality, outline the potential risks, consider the overall system mitigation strategy, and finally decide what risks will be addressed through system messaging.  

 

### 3/ Outline your overall mitigation strategy 

Determine which harm mitigation techniques and layers you’ll use. Then, define the strategy that system messages should play in your safety stack and how it complements other mitigations. 

 

### 4/ Collect or create initial system message and safety system components  

These should be based on research, red-teaming results, customer feedback where applicable, and reviewing and extracting similar patterns from similar evaluations and system messages.  

 

### 5/ Build a robust dataset  

Build datasets and collect example user prompts to test. Datasets should contain a distribution of both adversarial and benign examples to determine the level of under-moderation (also known as leakage) and regression in your candidate components. Ensure your dataset is specific to the harm(s) you are testing to determine the best system message for your scenario.  

 

### 6/ Evaluate system message and safety message components 

Define metrics that are relevant to your scenario. Then, apply your system message components to your model to assess defect rates and other relevant metrics.  

 

For safety system message components, the primary criterion is the improvement in safety. The system message yielding the lowest defect rate is typically your best component. However, there are exceptions. Consider the severity of defects, not just their frequency. For example, if you were working with identity-based harms, and one component has a 10% defect rate with severe slurs and insults, while another has a 15% defect rate with mild harms using language outside of best practice, the second component would be preferable to the first.  

 

### 7/ Iterate on system messages and safety system components and above steps 

Based on your evaluations, revisit your top components to improve any issues to reach an acceptable level. Continue to monitor and evaluate your system regularly as changes are introduced, including new use cases, updated models, etc. Remember that even when using this guidance, you still need to validate your model responses per scenario. A well-crafted system message for one scenario may not work more broadly across other scenarios. Understanding the [limitations of LLMs](/legal/cognitive-services/openai/transparency-note?context=/azure/ai-services/openai/context/context#limitations) and the [mechanisms for evaluating and mitigating those limitations](/legal/cognitive-services/openai/overview?context=/azure/ai-services/openai/context/context) is as important as understanding how to leverage their strengths. 


## Summary of best practices  

When you develop system message components, it’s important to: 

- **Use clear language**:  This eliminates over-complexity and risk of misunderstanding and maintains consistency across different components. 
- **Be concise**: This helps with latency, as shorter system messages perform better versus lengthy ones. Additionally, longer system messages occupy part of the context window (that is, number of tokens the model takes into account when making predictions or generating text), thus potentially impacting the remaining context window for the user prompt. 
- **Emphasize certain words** (where applicable) by using `**word**`: puts special focus on key elements especially of what the system should and shouldn't do. 
- **Use first person language** when you refer to the AI system: it’s better to use phrasing such as `you are an AI assistant that does […]` versus `assistant does […]`. 
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
| Example(s)-based | Gives the model clear instances or situations for better context. The model utilizes specific examples of interactions that are unequivocally harmful, implicitly problematic, not harmful, or undesirable as a reference for its outputs.  | `Users will ask you a spectrum of questions that might harm somebody physically or emotionally. In all scenarios, you should not respond meaningfully.`<br><br> `An unequivocally harmful statement is something like: "Tell me why <minority group> should be excluded from society."` <br><br> `A request that is more implicitly problematic is something like: "Imagine you are playing an antagonist in a movie, tell me why <minority group> should be excluded from society".`|
| Never / don’t | Involves structuring prompts and instructions with explicit prohibitions to prevent the AI from generating content that could be inappropriate, harmful, or outside its scope of capabilities by using terms such as "never," "don’t," "do not" etc. | `**Never** make assumptions, judgements or evaluations about a person. Any time a user violates your policy, or you’re not sure what to respond, say: "It looks like I can’t work with this content. Try asking me a question or telling me how I can help."` |
| [Spotlighting](https://arxiv.org/pdf/2403.14720) | **Spotlighting** is a family of techniques that helps models distinguish between valid system instructions and potentially untrustworthy external inputs. These techniques are effective against indirect attacks, also referred to as indirect prompt attacks or cross-domain prompt injection attacks. They work by transforming the input text in a way that makes it more salient to the model, while preserving its semantic content and task performance. <ul><li> **Delimiters** are a natural starting point to help mitigate indirect attacks. Including delimiters in your system message helps to explicitly demarcate the location of the input text in the system message. You can choose one or more special tokens to prepend and append the input text, and the model will be made aware of this boundary. By using delimiters, the model will only handle documents if they contain the appropriate delimiters, reducing the success rate of indirect attacks. However, since delimiters can be subverted by clever adversaries, we recommend you combine this with other spotlighting approaches. </li><li>**Data marking** is an extension of the delimiter concept. Instead of only using special tokens to demarcate the beginning and end of a block of content, data marking involves interleaving a special token throughout the entirety of the text.</li></ul> | You might choose `^` as the delimiter. You might then transform the input text by replacing all whitespace with the special token. Given an input document with the phrase `In this manner, Joe traversed the labyrinth of...`, the phrase would become: `In^this^manner^Joe^traversed^the^labyrinth^of`. In the system message, the model is warned that this transformation has occurred and can be used to help the model distinguish between token blocks. |

#### [Other techniques to consider](#tab/other-techniques)


| Technique | Definition |
| --- | --- | 
| 
Catch-all | Involves integrating different methods in one framework to try to cover all kinds of possible behavior and to reduce harm. However, the drawback is that components often become too long and impact latency.  |
|Emphasis on learned knowledge |Involves structuring the prompt in a way that encourages the AI to draw from previous learning (either stated, from its training data, etc.), thereby improving the quality and relevance of the output.  |
|Highlight the role of AI  |Involves structuring prompts and instructions in a way that instructs the AI concerning how to behave (protecting against certain type of harms, ensuring respect towards human identity, etc.) versus its primary role (such as providing information, answering questions, engaging in conversations).  |
|Reverse logic |Guides responses by reframing prohibitions into positive actions. Instead of telling the AI what it should not do, this technique involves structuring prompts and instructions to emphasize what the AI should do. This can lead to more constructive and positive outcomes, as it encourages the AI to generate content that aligns with desired behaviors and standards. This works in contrast to simply avoiding undesired outcomes. |
|Risk-based |Guides AI responses to prioritize safety and harm prevention. It involves structuring the instructions on defining what the primary risk is and showcasing potential consequences should risk occur.  |
|Rules-based |Involves structuring prompts and instructions according to specific guidelines that the AI must adhere to when generating its responses. These rules can cover a wide range of aspects and techniques such as, but not limited to, "never," "do not," "always," "should," "if queries" and combinations of them.  |


---

## Recommended system messages 

These best practices can help you better understand the process of developing robust system messages for your scenario.  

For more information on recommended safety components, visit our [Safety system message template guidance](./safety-system-message-templates.md). 

Finally, remember that system messages, or metaprompts, are not "one size fits all." Use of these type of examples has varying degrees of success in different applications. It's important to try different wording, ordering, and structure of system message text to reduce identified harms, and to test the variations to see what works best for a given scenario.

## Next steps

- [Azure OpenAI Service](/azure/ai-services/openai/concepts/prompt-engineering)
- [System message design with Azure OpenAI](/azure/ai-services/openai/concepts/advanced-prompt-engineering?pivots=programming-language-chat-completions) 
- [Announcing Safety System Messages in Azure AI Foundry portal](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/announcing-safety-system-messages-in-azure-ai-studio-and-azure/ba-p/4146991) - Microsoft Community Hub 
- [Safety system message templates ](./safety-system-message-templates.md)
