---
title: "Prompt Shields in Azure AI Content Safety"
titleSuffix: Azure AI services
description: Learn about User Prompt injection attacks and document attacks and how to prevent them with the Prompt Shields feature.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: build-2023
ms.topic: conceptual
ms.date: 10/16/2024
ms.author: pafarley
---

# Prompt Shields

Generative AI models can pose risks of being exploited by malicious actors. To mitigate these risks, we integrate safety mechanisms to restrict the behavior of large language models (LLMs) within a safe operational scope. However, despite these safeguards, LLMs can still be vulnerable to adversarial inputs that bypass the integrated safety protocols.

Prompt Shields is a unified API that analyzes LLM inputs and detects adversarial user input attacks.


## User scenarios
### AI content creation platforms: Detecting harmful prompts
- Scenario: An AI content creation platform uses generative AI models to produce marketing copy, social media posts, and articles based on user-provided prompts. To prevent the generation of harmful or inappropriate content, the platform integrates "Prompt Shields."
- User: Content creators, platform administrators, and compliance officers.
- Action: The platform uses Azure AI Content Safety's "Prompt Shields" to analyze user prompts before generating content. If a prompt is detected as potentially harmful or likely to lead to policy-violating outputs (e.g., prompts asking for defamatory content or hate speech), the shield blocks the prompt and alerts the user to modify their input.
- Outcome: The platform ensures all AI-generated content is safe, ethical, and compliant with community guidelines, enhancing user trust and protecting the platform's reputation.
### AI-powered chatbots: Mitigating risk from user prompt attacks
- Scenario: A customer service provider uses AI-powered chatbots for automated support. To safeguard against user prompts that could lead the AI to generate inappropriate or unsafe responses, the provider uses "Prompt Shields."
- User: Customer service agents, chatbot developers, and compliance teams.
- Action: The chatbot system integrates "Prompt Shields" to monitor and evaluate user inputs in real-time. If a user prompt is identified as potentially harmful or designed to exploit the AI (e.g., attempting to provoke inappropriate responses or extract sensitive information), the shield intervenes by blocking the response or redirecting the query to a human agent.
- Outcome: The customer service provider maintains high standards of interaction safety and compliance, preventing the chatbot from generating responses that could harm users or breach policies.
### E-learning platforms: Preventing inappropriate AI-generated educational content
- Scenario: An e-learning platform employs GenAI to generate personalized educational content based on student inputs and reference documents. To avoid generating inappropriate or misleading educational content, the platform utilizes "Prompt Shields."
- User: Educators, content developers, and compliance officers.
- Action: The platform uses "Prompt Shields" to analyze both user prompts and uploaded documents for content that could lead to unsafe or policy-violating AI outputs. If a prompt or document is detected as likely to generate inappropriate educational content, the shield blocks it and suggests alternative, safe inputs.
- Outcome: The platform ensures that all AI-generated educational materials are appropriate and compliant with academic standards, fostering a safe and effective learning environment.
### Healthcare AI assistants: Blocking unsafe prompts and document inputs
- Scenario: A healthcare provider uses AI assistants to offer preliminary medical advice based on user inputs and uploaded medical documents. To ensure the AI does not generate unsafe or misleading medical advice, the provider implements "Prompt Shields."
- User: Healthcare providers, AI developers, and compliance teams.
- Action: The AI assistant employs "Prompt Shields" to analyze patient prompts and uploaded medical documents for harmful or misleading content. If a prompt or document is identified as potentially leading to unsafe medical advice, the shield prevents the AI from generating a response and redirects the patient to a human healthcare professional.
- Outcome: The healthcare provider ensures that AI-generated medical advice remains safe and accurate, protecting patient safety and maintaining compliance with healthcare regulations.
### Generative AI for creative writing: Protecting against prompt manipulation
- Scenario: A creative writing platform uses GenAI to assist writers in generating stories, poetry, and scripts based on user inputs. To prevent the generation of inappropriate or offensive content, the platform incorporates "Prompt Shields."
- User: Writers, platform moderators, and content reviewers.
- Action: The platform integrates "Prompt Shields" to evaluate user prompts for creative writing. If a prompt is detected as likely to produce offensive, defamatory, or otherwise inappropriate content, the shield blocks the AI from generating such content and suggests revisions to the user.

[!INCLUDE [prompt shields attack info](../includes/prompt-shield-attack-info.md)]

## Limitations

### Language availability

Prompt Shields have been specifically trained and tested on the following languages: Chinese, English, French, German, Spanish, Italian, Japanese, Portuguese. However, the feature can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.

### Text length limitations

See [Input requirements](/azure/ai-services/content-safety/overview#input-requirements) for maximum text length limitations.

### Region availability

To use this API, you must create your Azure AI Content Safety resource in the supported regions. See [Region availability](/azure/ai-services/content-safety/overview#region-availability).

### Rate limitations

See [Query rates](/azure/ai-services/content-safety/overview#query-rates).

If you need a higher rate, please [contact us](mailto:contentsafetysupport@microsoft.com) to request it.

## Next steps

Follow the quickstart to get started using Azure AI Content Safety to detect user input risks.

> [!div class="nextstepaction"]
> [Prompt Shields quickstart](../quickstart-jailbreak.md)
