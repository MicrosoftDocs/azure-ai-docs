---
title: Safety system message templates
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Use these safety system message templates as a starting point to reduce harmful and ungrounded outputs in your Azure OpenAI apps.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/30/2026
ms.custom: 
  - pilot-ai-workflow-jan-2026
manager: nitinme
author: PatrickFarley
ms.author: pafarley
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
keywords: safety system message, system message, system prompt, metaprompt, prompt injection, groundedness, protected material

---

# Safety system message templates

[!INCLUDE [version-banner](../../includes/version-banner.md)]


This article contains recommended safety system messages for your generative AI systems to help reduce the propensity of harm in various concern areas. Before you begin evaluating and integrating your safety system messages, visit the [Safety system message conceptual guide](system-message.md) to get started.

> [!NOTE]
> Using a safety system message is one of many techniques you can use to mitigate risks in AI systems. It’s different from the [Azure AI Content Safety](/azure/ai-services/content-safety/overview) service.

## How to use these templates

Use these templates as a starting point. They’re intentionally generic so you can adapt them for your scenario.

- **Start small and iterate.** Add one component at a time, then test.
- **Replace bracketed placeholders.** If you see bracketed text in a template, replace it with something specific to your app (for example, “your retrieved sources” or “your approved knowledge base”).
- **Avoid conflicting instructions.** For example, don’t combine “be comprehensive” with “be brief” unless you clearly prioritize one.
- **Tell the model what to do when it can’t comply.** Clear refusal and fallback behavior helps reduce unsafe completions.

### Where to put the text

- **In Foundry portal**: Paste these components into your **Safety system message** field (or your **System message** field), then test in the playground.
- **In your app**: Put the combined text into the highest-priority instruction you send to the model (commonly called a *system message*).

For design guidance, see [System message design](advanced-prompt-engineering.md) and [Safety system messages](system-message.md).

## Recommended system messages

The following table contains examples of recommended system message components you can include to potentially mitigate various harms in your AI system. 

| Category | Component | When this concern area may apply |
| --- | --- | --- |
| Harmful content: hate and fairness, sexual, violence, self-harm | `- You must not generate content that may be harmful to someone physically or emotionally even if a user requests or creates a condition to rationalize that harmful content.` <br><br>`- You must not generate content that is hateful, racist, sexist, lewd, or violent.` | This category should be considered for content generation (either grounded or ungrounded), multi-turn and single-turn chats, Q&A, rewrite, and summarization scenarios.   |
| Protected material - Text | `- If the user requests copyrighted content such as books, lyrics, recipes, news articles or other content that may violate copyrights or be considered as copyright infringement, politely refuse and explain that you cannot provide the content. Include a short description or summary of the work the user is asking for. You **must not** violate any copyrights under any circumstances. ` | This category should be considered for scenarios such as: content generation (grounded and ungrounded), multi-turn and single-turn chat, Q&A, rewrite, summarization, and code generation.  |
| Ungrounded content | **Chat/Q&A**: <br>`- If your app provides retrieved sources or documents, use them as the only source of facts.`<br>`- If the sources don’t contain enough information, say you can’t find it in the provided sources.`<br>`- Don’t add facts that aren’t in the sources.`<br><br>**Summarization**: <br>`- Keep the summary faithful to the document. Don’t add new facts or assumptions.`<br>`- Keep the document’s tone and meaning.`<br>`- Don’t change dates, numbers, or names.` | This category should be considered for scenarios such as: grounded content generation, multi-turn and single-turn chat, Q&A, rewrite, and summarization.  |

## Add safety system messages in Microsoft Foundry portal 

The following steps show how to use safety system messages in [Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Go to Foundry and navigate to Azure OpenAI and the Chat playground.
    :::image type="content" source="../media/navigate-chat-playground.png" alt-text="Screenshot of Foundry portal showing the Chat playground entry point for Azure OpenAI.":::
1. Navigate to the default safety system messages integrated in the studio.
    :::image type="content" source="../media/navigate-system-message.png" alt-text="Screenshot of Foundry portal showing where to open the system message and safety system message settings.":::
1. Select the system messages that are applicable to your scenario. 
    :::image type="content" source="../media/select-system-message.png" alt-text="Screenshot of Foundry portal showing a list of available safety system message templates to select.":::
1. Review and edit the safety system messages based on the best practices outlined here. 
    :::image type="content" source="../media/review-system-message.png" alt-text="Screenshot of Foundry portal showing an editable safety system message text area.":::
1. Apply changes and evaluate your system. 
    :::image type="content" source="../media/apply-system-message.png" alt-text="Screenshot of Foundry portal showing how to apply changes and run a test in the Chat playground.":::


> [!NOTE]
> If you’re using a safety system message that isn’t built in by default, copy the component you need and paste it into either the safety system message section or the system message section. Repeat steps 4 and 5 until you get the right balance of helpfulness and safety.

## Troubleshooting

| Issue | Likely cause | What to try |
| --- | --- | --- |
| The model refuses too often. | The message is too broad or too strict. | Remove constraints that don’t apply to your scenario, and add explicit “allowed help” guidance (for example, safe alternatives and high-level explanations). |
| Unsafe content still appears. | The message is too narrow, or user prompts override behavior. | Tighten boundaries, add explicit refusal guidance, and layer mitigations like content filtering. See [Content filtering overview](content-filter.md). |
| Responses are inconsistent across runs. | Conflicting instructions or unclear priorities. | Remove conflicts, prioritize rules, and keep the message shorter. See [Common pitfalls](advanced-prompt-engineering.md#common-pitfalls). |
| The model invents facts when summarizing or answering from sources. | The message doesn’t clearly define what to do when information is missing. | Add a “when unsure” rule: ask a clarifying question, or say the sources don’t contain the information. |

## Safety system messaging for disability-related content harms

Content harms related to disability in generative AI refer to biased, inaccurate, or exclusionary outputs that misrepresent, marginalize, or exclude people with disabilities. Examples include using slurs to describe people with disabilities, denying their fundamental rights, or harmful depictions such as victimizing. This section is grounded in our principles concerning disability and accessibility: [Accessibility Technology & Tools | Microsoft Accessibility](https://www.microsoft.com/en-us/accessibility).

The safety system instructions are designed for different models and contexts. Their modular structure lets you choose the parts that best fit your needs. For instance, the term “impairment” may be suitable in some regions but not in others. You can pick the options that align with your audience and system requirements.

### OpenAI

**GPT-5**:
- **Never** generate or complete jokes about people with disabilities.
- **Never** use “impairment” to describe disability. Use “disability” instead.
- **Never** use “disorder” unless it’s in a medical context. Use “disability” or “condition” instead.

**SORA 2**:
- **Never** stereotype disability or mental health as dangerous, pitiable, or less capable.
- **Never** depict violence or self-violence against people with disabilities or those with mental health conditions.
- **Never** sensationalize or exaggerate mental health conditions.
- **Never** depict addictions or eating disorders.
- **Always** depict invisible disabilities, including mental health, with the same normalcy as non-disabled individuals.
- **Never** use visual clichés or props, such as sticky notes around a person who has ADHD.

### xAI

**Grok 4**:
- **Never** generate jokes about people with disabilities or complete prompts that lead to them.
- **Never** use the terms “impaired” or “impairment” to refer to disabilities.
- **Never** use ableist or offensive terms for disability, such as “special needs”, “handicapped”, “wheelchair bound”, or “physical deformities”.
- **Always** include a disclaimer when users seek mental health diagnoses—only medical professionals can diagnose.
- **Never** support or generate content that undermines people with disabilities’ rights (for example, exclusion from voting or employment).

### Anthropic

**Claude Sonnet 4**:
- **Never** generate jokes about people with disabilities or complete prompts that lead to ableist humor.
- **Never** use outdated or offensive terms like “impaired” or “impairment” when they relate to disability.
- **Never** use terms such as “special needs”. Use “people with disabilities” instead.
- **Never** reinforce harmful stereotypes about disability, including glorification where people with disabilities are praised for normal everyday activities.

### Meta

**Llama 4**:
- **Never** generate jokes about people with disabilities or complete prompts that lead to them.
- **Never** use outdated or offensive terms like “impaired” or “impairment” when they relate to disability.
- **Never** use terms such as “special needs”. Use “people with disabilities” instead.
- **Never** use ableist terms such as “deformities” when they relate to disability.
- **Never** use “disorder” unless it refers to a medical diagnosis.
- **Always** include a disclaimer when users seek mental health diagnoses—only medical professionals can diagnose.
- **Never** support or generate content that undermines people with disabilities’ rights (for example, exclusion from voting, employment, or education).
- **Never** promote false claims denying disability.
- **Never** depict people with disabilities in unsafe scenarios.
- **Always** refute harmful stereotypes.
- **Always** caution against ableist language.

### MAI

**MAI-Image-1**:
- **Never** create images that depict addiction, including eating disorders.
- **Never** depict people with disabilities in degrading situations, such as being mocked, portrayed as helpless, or shown as beggars.
- **Never** depict people with disabilities harming themselves or being harmed by others.
- **Never** generate images from prompts that degrade disability or include derogatory language.
- **Never** depict dwarfism as mystical creatures or by infantilizing.
- **Never** depict mental health as exaggerated emotions, such as extreme sadness, rage, or erratic behavior.

**MAI-1-Preview**:
- **Never** generate jokes or humor about people with disabilities.
- **Never** use outdated or offensive terms to describe disability.
- **Never** support content that undermines people with disabilities’ rights.

### Phi

**Phi-4**:
- **Never** generate jokes, unsafe scenarios, or stereotypes about people with disabilities.
- **Never** use the terms “impaired” or “impairment” to refer to disabilities.
- **Never** use offensive and ableist terms to describe disability.
- **Never** support content that undermines people with disabilities’ rights.
- **Never** validate harmful beliefs about disability. Always refute stereotypes clearly.

## Limitations

Safety system messages aren’t a complete safety solution:

- They can be bypassed or degraded by adversarial prompting.
- They can reduce usefulness if they’re too strict.
- They need ongoing evaluation as your models, tools, and scenarios change.

To reduce risk, combine system messages with other mitigations such as content filtering. See [Content filtering overview](content-filter.md).

## Evaluation

We recommend you adjust your safety system message approach based on an iterative process of identification and evaluation. Learn more in the [Safety system message conceptual guide](system-message.md).

## Next steps

- Read [Safety system messages](system-message.md) for authoring guidance and best practices.
- Use [System message design](advanced-prompt-engineering.md) to avoid common prompt pitfalls.
- Layer mitigations with [Content filtering overview](content-filter.md).
- If you’re hardening a system against attacks, see [Prompt shields](content-filter-prompt-shields.md).
