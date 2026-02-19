---
title: "Prompt Shields in Azure AI Content Safety"
titleSuffix: Azure AI services
description: Learn about User Prompt injection attacks and document attacks and how to prevent them with the Prompt Shields feature.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: build-2023, dev-focus
ms.topic: concept-article
ai-usage: ai-assisted
ms.date: 11/21/2025
ms.author: pafarley
---

# Prompt Shields

Prompt Shields is a unified API in Azure AI Content Safety that detects and blocks adversarial user input attacks on large language models (LLMs). It helps prevent harmful, unsafe, or policy-violating AI outputs by analyzing prompts and documents before content is generated.

Generative AI models can pose risks of exploitation by malicious actors. To mitigate these risks, we integrate safety mechanisms to restrict the behavior of large language models (LLMs) within a safe operational scope. However, despite these safeguards, LLMs can still be vulnerable to adversarial inputs that bypass the integrated safety protocols. In these cases, specialized filters like Prompt Shields are effective.

## User scenarios

### AI content creation platforms: Detecting harmful prompts

- Scenario: An AI content creation platform uses generative AI models to produce marketing copy, social media posts, and articles based on user-provided prompts. To prevent the generation of harmful or inappropriate content, the platform integrates Prompt Shields.
- User: Content creators, platform administrators, and compliance officers.
- Action: The platform uses Azure AI Content Safety's Prompt Shields to analyze user prompts before generating content. If a prompt is detected as potentially harmful or likely to lead to policy-violating outputs (for example, prompts asking for defamatory content or hate speech), the shield blocks the prompt and alerts the user to modify their input.
- Outcome: The platform ensures all AI-generated content is safe, ethical, and compliant with community guidelines, enhancing user trust and protecting the platform's reputation.

### AI-powered chatbots: Mitigating risk from user prompt attacks

- Scenario: A customer service provider uses AI-powered chatbots for automated support. To safeguard against user prompts that could lead the AI to generate inappropriate or unsafe responses, the provider uses Prompt Shields.
- User: Customer service agents, chatbot developers, and compliance teams.
- Action: The chatbot system integrates Prompt Shields to monitor and evaluate user inputs in real-time. If a user prompt is identified as potentially harmful or designed to exploit the AI (for example, attempting to provoke inappropriate responses or extract sensitive information), the system intervenes by blocking the response or redirecting the query to a human agent.
- Outcome: The customer service provider maintains high standards of interaction safety and compliance, preventing the chatbot from generating responses that could harm users or breach policies.

### E-learning platforms: Preventing inappropriate AI-generated educational content
- Scenario: An e-learning platform employs GenAI to generate personalized educational content based on student inputs and reference documents. To avoid generating inappropriate or misleading educational content, the platform utilizes Prompt Shields.
- User: Educators, content developers, and compliance officers.
- Action: The platform uses Prompt Shields to analyze both user prompts and uploaded documents for content that could lead to unsafe or policy-violating AI outputs. If a prompt or document is detected as likely to generate inappropriate educational content, the shield blocks it and suggests alternative, safe inputs.
- Outcome: The platform ensures that all AI-generated educational materials are appropriate and compliant with academic standards, fostering a safe and effective learning environment.

### Healthcare AI assistants: Blocking unsafe prompts and document inputs
- Scenario: A healthcare provider uses AI assistants to offer preliminary medical advice based on user inputs and uploaded medical documents. To ensure the AI doesn't generate unsafe or misleading medical advice, the provider implements Prompt Shields.
- User: Healthcare providers, AI developers, and compliance teams.
- Action: The AI assistant employs Prompt Shields to analyze patient prompts and uploaded medical documents for harmful or misleading content. If a prompt or document is identified as potentially leading to unsafe medical advice, the shield prevents the AI from generating a response and redirects the patient to a human healthcare professional.
- Outcome: The healthcare provider ensures that AI-generated medical advice remains safe and accurate, protecting patient safety and maintaining compliance with healthcare regulations.

### Generative AI for creative writing: Protecting against prompt manipulation
- Scenario: A creative writing platform uses GenAI to assist writers in generating stories, poetry, and scripts based on user inputs. To prevent the generation of inappropriate or offensive content, the platform incorporates Prompt Shields.
- User: Writers, platform moderators, and content reviewers.
- Action: The platform integrates Prompt Shields to evaluate user prompts for creative writing. If a prompt is detected as likely to produce offensive, defamatory, or otherwise inappropriate content, the shield blocks the AI from generating such content and suggests revisions to the user.

[!INCLUDE [prompt shields attack info](../includes/prompt-shield-attack-info.md)]

## Limitations

- **Language availability**: Models are trained and tested on Chinese, English, French, German, Spanish, Italian, Japanese, Portuguese. Other languages might work but with varying quality.
- **Text length**: See [Input requirements](../overview.md#input-requirements) for maximum text length limitations.
- **Region availability**: You must create your Azure AI Content Safety resource in one of the [supported regions](../overview.md#region-availability).
- **Rate limits**: See [Query rates](../overview.md#query-rates). [Contact us](mailto:contentsafetysupport@microsoft.com) for higher rate requests.

## Troubleshooting

Common issues and solutions:

- **401 Unauthorized**: Verify your API key is correct and the resource is active. Check that your key environment variable is properly set.
- **429 Too Many Requests**: You've exceeded rate limits. Implement exponential backoff or request higher limits.
- **400 Bad Request**: Check that your text input doesn't exceed length limits and required parameters are included.
- **403 Forbidden**: Verify your RBAC role assignment. You need at least Cognitive Services User permissions.
- **False positives/negatives**: Prompt Shields may not catch all attack vectors or may flag legitimate prompts. Always implement additional validation layers.

## Next steps

Explore these resources to implement Prompt Shields in your application:

> [!div class="nextstepaction"]
> [Prompt Shields quickstart](../quickstart-jailbreak.md)

**Additional resources**:
- [Content Safety REST API reference](/rest/api/contentsafety/text-operations)
- [Python SDK documentation](/python/api/azure-ai-contentsafety/)
- [.NET SDK documentation](/dotnet/api/azure.ai.contentsafety)
- [GitHub samples repository](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentsafety/azure-ai-contentsafety/samples)
- [Content Safety overview](../overview.md)
