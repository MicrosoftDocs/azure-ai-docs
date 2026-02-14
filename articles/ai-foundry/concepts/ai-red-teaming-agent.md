---
title: AI Red Teaming Agent
titleSuffix: Microsoft Foundry
description: This article provides conceptual overview of the AI Red Teaming Agent.
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 11/18/2025
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
monikerRange: 'foundry-classic || foundry'
---

# AI Red Teaming Agent (preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

The AI Red Teaming Agent is a powerful tool designed to help organizations proactively find safety risks associated with generative AI systems during design and development of generative AI models and applications.

Traditional red teaming involves exploiting the cyber kill chain and describes the process by which a system is tested for security vulnerabilities. However, with the rise of generative AI, the term AI red teaming has been coined to describe probing for novel risks (both content and security related) that these systems present and refers to simulating the behavior of an adversarial user who is trying to cause your AI system to misbehave in a particular way.

The AI Red Teaming Agent leverages Microsoft's open-source framework for Python Risk Identification Tool's ([PyRIT](https://github.com/Azure/PyRIT)) AI red teaming capabilities along with Microsoft Foundry's [Risk and Safety Evaluations](./observability.md) to help you automatically assess safety issues in three ways:

- **Automated scans for content risks:** Firstly, you can automatically scan your model and application endpoints for safety risks by simulating adversarial probing.
- **Evaluate probing success:** Next, you can evaluate and score each attack-response pair to generate insightful metrics such as Attack Success Rate (ASR).
- **Reporting and logging** Finally, you can generate a score card of the attack probing techniques and risk categories to help you decide if the system is ready for deployment. Findings can be logged, monitored, and tracked over time directly in Foundry, ensuring compliance and continuous risk mitigation.

Together these components (scanning, evaluating, and reporting) help teams understand how AI systems respond to common attacks, ultimately guiding a comprehensive risk management strategy.

## When to use an AI red teaming run

When thinking about AI-related safety risks developing trustworthy AI systems, Microsoft uses NIST's framework to mitigate risk effectively: Govern, Map, Measure, Manage. We'll focus on the last three parts in relation to the generative AI development lifecycle:

- Map: Identify relevant risks and define your use case.
- Measure: Evaluate risks at scale.
- Manage: Mitigate risks in production and monitor with a plan for incident response.

:::image type="content" source="../media/evaluations/red-teaming-agent/map-measure-mitigate-ai-red-teaming.png" alt-text="Diagram of how to use AI Red Teaming Agent showing proactive to reactive and less costly to more costly." lightbox="../media/evaluations/red-teaming-agent/map-measure-mitigate-ai-red-teaming.png":::

AI Red Teaming Agent can be used to run automated scans and simulate adversarial probing to help accelerate the identification and evaluation of known risks at scale. This helps teams "shift left" from costly reactive incidents to more proactive testing frameworks that can catch issues before deployment. Manual AI red teaming process is time and resource intensive. It relies on the creativity of safety and security expertise to simulate adversarial probing. This process can create a bottleneck for many organizations to accelerate AI adoption. With the AI Red Teaming Agent, organizations can now leverage Microsoft's deep expertise to scale and accelerate their AI development with Trustworthy AI at the forefront.

We encourage teams to use the AI Red Teaming Agent to run automated scans throughout the design, development, and pre-deployment stage:

::: moniker range="foundry-classic"

- Design: Picking out the safest foundational model on your use case.
- Development: Upgrading models within your application or creating fine-tuned models for your specific application.
- Pre-deployment: Before deploying GenAI applications to productions.

In production, we recommend implementing **safety mitigations** such as [Azure AI Content Safety filters](../../ai-services/content-safety/overview.md) or implementing safety system messages using our [templates](../openai/concepts/safety-system-message-templates.md).

::: moniker-end

::: moniker range="foundry"

- Design: Picking out the safest foundational model on your use case.
- Development: Upgrading models within your application or creating fine-tuned models for your specific application.
- Pre-deployment: Before deploying GenAI applications and agents to production.
- Post-deployment: Monitor your Gen AI applications and agents after deployment with scheduled continuous red teaming runs on synthetic adversarial data.

In production, we recommend implementing **safety guardrails** such as [Azure AI Content Safety filters](../../ai-services/content-safety/overview.md) or implementing safety system messages using our [templates](../openai/concepts/safety-system-message-templates.md). For agentic workflows, we recommend leveraging [Foundry Control Plane](../default/control-plane/overview.md) to apply guardrails and govern your fleet of agents.

::: moniker-end

## How AI Red Teaming works

The AI Red Teaming Agent helps automate simulation of adversarial probing of your target AI system. It provides a curated dataset of seed prompts or attack objectives per supported risk categories. These can be used to automate direct adversarial probing. However, direct adversarial probing might be easily caught by existing safety alignments of your model deployment. Applying attack strategies from PyRIT provides an extra conversion that can help to by-pass or subvert the AI system into producing undesirable content.

In the diagram, we can see that a direct ask to your AI system on how to loot a bank triggers a refusal response. However, applying an attack strategy such as flipping all the characters can help trick the model into answering the question.

:::image type="content" source="../media/evaluations/red-teaming-agent/how-ai-red-teaming-works.png" alt-text="Diagram of how AI Red Teaming Agent works." lightbox="../media/evaluations/red-teaming-agent/how-ai-red-teaming-works.png":::

Additionally, the AI Red Teaming Agent provides users with a fine-tuned adversarial large language model dedicated to the task of simulating adversarial attacks and evaluating responses that might have harmful content in them with the Risk and Safety Evaluators. The key metric to assess the risk posture of your AI system is Attack Success Rate (ASR) which calculates the percentage of successful attacks over the number of total attacks.

## Supported risk categories

The following risk categories are supported in the AI Red Teaming Agent from [Risk and Safety Evaluations](./observability.md). Only text-based scenarios are supported.

::: moniker range="foundry-classic"

| **Risk category** | **Description** |
|------------------|-----------------|
| **Hateful and Unfair Content** | Hateful and unfair content refers to any language or imagery pertaining to hate toward or unfair representations of individuals and social groups along factors including but not limited to race, ethnicity, nationality, gender, sexual orientation, religion, immigration status, ability, personal appearance, and body size. Unfairness occurs when AI systems treat or represent social groups inequitably, creating or contributing to societal inequities. |
| **Sexual Content** | Sexual content includes language or imagery pertaining to anatomical organs and genitals, romantic relationships, acts portrayed in erotic terms, pregnancy, physical sexual acts (including assault or sexual violence), prostitution, pornography, and sexual abuse. |
| **Violent Content** | Violent content includes language or imagery pertaining to physical actions intended to hurt, injure, damage, or kill someone or something. It also includes descriptions of weapons and guns (and related entities such as manufacturers and associations). |
| **Self-Harm-Related Content** | Self-harm-related content includes language or imagery pertaining to actions intended to hurt, injure, or damage one's body or kill oneself. |

::: moniker-end

::: moniker range="foundry"

| **Risk category** | **Supported target(s)** | **Local or cloud red teaming** |**Description** |
|------------------|-----------------|-----------------|-------------|
| **Hateful and Unfair Content** |  Model and agents | Local and cloud | Hateful and unfair content refers to any language or imagery pertaining to hate toward or unfair representations of individuals and social groups along factors including but not limited to race, ethnicity, nationality, gender, sexual orientation, religion, immigration status, ability, personal appearance, and body size. Unfairness occurs when AI systems treat or represent social groups inequitably, creating or contributing to societal inequities. |
| **Sexual Content** | Model and agents |  Local and cloud | Sexual content includes language or imagery pertaining to anatomical organs and genitals, romantic relationships, acts portrayed in erotic terms, pregnancy, physical sexual acts (including assault or sexual violence), prostitution, pornography, and sexual abuse. |
| **Violent Content** |  Model and agents |  Local and cloud | Violent content includes language or imagery pertaining to physical actions intended to hurt, injure, damage, or kill someone or something. It also includes descriptions of weapons and guns (and related entities such as manufacturers and associations). |
| **Self-Harm-Related Content** |  Model and agents | Local and cloud | Self-harm-related content includes language or imagery pertaining to actions intended to hurt, injure, or damage one's body or kill oneself. |
| **Protected Materials** |  Model and agents | Local and cloud |  Copyrighted or protected materials such as lyrics, songs, and recipes. |
| **Code vulnerability** | Model and agents |  Local and cloud | Measures whether AI generates code with security vulnerabilities, such as code injection, tar-slip, SQL injections, stack trace exposure and other risks across Python, Java, C++, C#, Go, JavaScript, and SQL. |
| **Ungrounded attributes** | Model and agents |  Local and cloud | Measures an AI system's generation of text responses that contain ungrounded inferences about personal attributes, such as their demographics or emotional state. |
| **Prohibited actions** | Agents only | Cloud only |Measures an AI agent's ability to engage in behaviors that violate explicitly disallowed actions or tool uses based on user verified policy/taxonomy of prohibited actions. |
| **Sensitive data leakage** | Agents only | Cloud only |Measures an AI agent's vulnerability to exposing sensitive information (financial data, personal identifiers, health data, etc.) |
| **Task adherence** | Agents only | Cloud only |Measures whether an AI agent completes the assigned task by following the user’s goal, respecting all rules and constraints, and executing required procedures without unauthorized actions or omissions. |

## Agentic risks

Agent-specific risk categories such as prohibited actions, sensitive data leakage, and task adherence requires an approach to automated red teaming that differs from model-only risk categories. Specifically, the AI Red Teaming Agent is no longer only checking for generated outputs, but also checks for tool outputs for unsafe or risky behavior.  Agentic risk categories are only available in cloud red-teaming to provide a minimally sandboxed environment.

For cloud red teaming runs, we redact the harmful or adversarial inputs sent to your model or agent from the resulting red teaming results. This prevents developers and non-technical stakeholders from being exposed to potentially harmful prompt attacks generated by the AI Red Teaming Agent's red teaming runs.

For red teaming agentic risk categories, we ensure that when an AI red teaming run targets a Foundry hosted agent, it's a transient run so that harmful data isn't logged by the Foundry Agent Service and chat completions aren't stored. We recommend all developers to run red teaming exercises in a "purple environment," or a non-production environment that is configured with production-like resources to see how your agents work in as real-life as possible scenarios.

### Sensitive data leakage

Sensitive data leakage red teaming tests for leakage of financial, medical, and personal data from internal knowledge bases and tool calls. The AI Red Teaming Agent uses synthetic dataset of sensitive information and mock tools to generate scenarios prompting the agent to divulge information. The Attack Success Rate (ASR) defines whether or not the red teaming run detects format-level leaks using pattern matching.

**Limitations:** Single-turn, English-only; synthetic data; excludes memory/training-set leaks.

### Prohibited actions

Prohibited actions red teaming tests for whether agents perform prohibited, high-risk, or irreversible actions by generating dynamic adversarial prompts based on user-provided policies and taxonomy of prohibited actions along with the set of supported tools that the agent is using and user-provided tool descriptions. The Attack Success Rate (ASR) defines policy violations exhibited by the agent based on the user-provided policies.

| Category | Description | Allowance Rule |
|--|--|--|
| Prohibited Actions | Universally banned (for example, facial recognition, emotion inference, social scoring). | ❌ Never allowed |
| High-Risk Actions | Sensitive actions need explicit human authorization (for example, financial transactions, medical decisions). | ⚠️ Allowed with human-in-the-loop confirmation |
| Irreversible Actions | Permanent operations (for example, file deletions, system resets). | ⚠️ Allowed with disclosure plus confirmation |

**Limitations:** Single-turn, English-only; Tool-level focus; no live production data.

> [!CAUTION]
> **Disclaimer for Third-Party Use of Prohibited Actions Taxonomy:**  
> The taxonomy of prohibited, high-risk, and irreversible actions provided in this product is intended solely as illustrative guidance to support agent developers in evaluating and customizing their own risk frameworks. It doesn't constitute a definitive or exhaustive list of prohibited practices, nor does it reflect Microsoft policy or regulatory interpretation. Third-party organizations remain solely responsible for ensuring their agents comply with applicable laws and regulations, including but not limited to the EU AI Act and other jurisdictional requirements. Microsoft strongly recommends retaining default prohibited actions derived from regulatory constraints and discourages deselection of these items. Use of this product doesn't guarantee compliance. Organizations should consult their own legal counsel to assess and implement appropriate safeguards and prohibitions tailored to their operational context and risk tolerance.

### Task adherence

Task adherence red teaming tests whether agents faithfully complete assigned tasks by achieving the user’s goal, respecting all rules and constraints, and following required procedures. The AI Red Teaming Agent probes along three dimensions: goal achievement (did the agent achieve the intended goal), rule compliance (including policy guardrails and presentation contracts), and procedural discipline (correct tool use, workflow, and grounding). The prompting dataset takes into account supported and available tools to generate diverse agentic trajectories, including representative and adversarial cases, to test both ordinary and edge-case scenarios.

### Indirect Prompt Injected Attacks

Indirect Prompt Injected Attacks (also known as Cross-Domain Prompt Injected Attacks, XPIA) red teaming tests whether an agent can be manipulated by malicious instructions hidden in external data sources, such as emails or documents—retrieved via tool calls. The AI Red Teaming Agent uses a synthetic dataset of benign user queries and mock tool outputs containing attack placeholders. During the probing, the AI Red Teaming Agent injects risk-specific attacks into these contexts to assess if the target agent executes unintended or unsafe actions. Attack Success Rate (ASR) measures how often the agent is compromised by indirect prompt injection, using agentic-specific risk categories such as prohibited actions, sensitive data leakage, or task adherence.

See full list of attack strategies in the next section.

### Supported agents and tools

The AI Red Teaming Agent currently supported red teaming Foundry agents with Azure tool calls, with the following supportability matrix:

| Supported Agents/Actions                | Status      |
|-----------------------------------------|-------------|
| Foundry hosted prompt agents            | Supported   |
| Foundry hosted container agents         | Supported   |
| Foundry workflow agents                 | Not Supported |
| Non-Foundry agents                      | Not Supported |
| Non-Azure tools | Not Supported |
| Azure tool calls | Supported |
| Function tool calls                 | Not supported|
| Browser automation tool calls    | Not Supported |
| Connected Agent tool calls              | Not Supported |
| Computer Use tool calls                  | Not Supported |

For a comprehensive list of tools, see [Tools](../agents/how-to/tools-classic/overview.md).

::: moniker-end

## Supported attack strategies

The following attack strategies are supported in the AI Red Teaming Agent from [PyRIT](https://azure.github.io/PyRIT/index.html):

| **Attack Strategy** | **Description** |
|---------------------|-----------------|
| AnsiAttack | Utilizes ANSI escape sequences to manipulate text appearance and behavior. |
| AsciiArt | Generates visual art using ASCII characters, often used for creative or obfuscation purposes. |
| AsciiSmuggler | Conceals data within ASCII characters, making it harder to detect. |
| Atbash | Implements the Atbash cipher, a simple substitution cipher where each letter is mapped to its reverse. |
| Base64 | Encodes binary data into a text format using Base64, commonly used for data transmission. |
| Binary | Converts text into binary code, representing data in a series of 0s and 1s. |
| Caesar | Applies the Caesar cipher, a substitution cipher that shifts characters by a fixed number of positions. |
| CharacterSpace | Alters text by adding spaces between characters, often used for obfuscation. |
| CharSwap | Swaps characters within text to create variations or obfuscate the original content. |
| Diacritic | Adds diacritical marks to characters, changing their appearance and sometimes their meaning. |
| Flip | Flips characters from front to back, creating a mirrored effect. |
| Leetspeak | Transforms text into Leetspeak, a form of encoding that replaces letters with similar-looking numbers or symbols. |
| Morse | Encodes text into Morse code, using dots and dashes to represent characters. |
| ROT13 | Applies the ROT13 cipher, a simple substitution cipher that shifts characters by 13 positions. |
| SuffixAppend | Appends an adversarial suffix to the prompt |
| StringJoin | Joins multiple strings together, often used for concatenation or obfuscation. |
| UnicodeConfusable | Uses Unicode characters that look similar to standard characters, creating visual confusion. |
| UnicodeSubstitution | Substitutes standard characters with Unicode equivalents, often for obfuscation. |
| Url | Encodes text into URL format |
| Jailbreak | Injects specially crafted prompts to bypass AI safeguards, known as User Injected Prompt Attacks (UPIA). |
| Indirect Jailbreak | Injects attack prompts in tool outputs or returned context to by pass AI safeguards indirectly, known as Indirect Prompt Injection Attacks. |
| Tense | Changes the tense of text, specifically converting it into past tense. |
| Multi turn |Executes attacks across multiple conversational turns, using context accumulation to bypass safeguards or elicit unintended behaviors. |
| Crescendo | Gradually escalates the complexity or risk of prompts over successive turns, probing for weaknesses in agent defenses through incremental challenge. |

## Known limitations of AI Red Teaming Agent

AI Red Teaming Agent has several important limitations to consider when running and interpreting red teaming results.

- Red teaming runs simulate scenarios in which a Foundry agent is exposed to sensitive data or attack vehicle data directly.  Since this data is all synthetic, this isn't representative of real world data distributions.
- Mock tools are only currently enabled to retrieve synthetic data and enable red teaming evaluations. They don't currently support mocking behaviors, which would enable testing closer to real sandboxing than what is currently supported.
- Due to lack of completely locked-down sandboxing support, the adversarial nature of our red teaming evaluations is controlled to avoid real world impact.
- Red teaming runs only represent adversarial population and don't include any observational population.
- Red teaming runs use generative models to evaluate Attack Success Rates (ASR) and can be non-deterministic, non-predictive. Therefore, there's always a chance of false positives and we always recommend reviewing results before taking mitigation actions.

## Learn more

Get started with our [documentation on how to run an automated scan for safety risks with the AI Red Teaming Agent](../how-to/develop/run-scans-ai-red-teaming-agent.md).

Learn more about the tools used by the AI Red Teaming Agent.

- [Azure AI Risk and Safety Evaluations](./safety-evaluations-transparency-note.md)
- [PyRIT: Python Risk Identification Tool](https://github.com/Azure/PyRIT)

The most effective strategies for risk assessment we've seen use automated tools to surface potential risks, which are then analyzed by expert human teams for deeper insights. If your organization is just starting with AI red teaming, we encourage you to explore the resources created by our own AI red team at Microsoft to help you get started.

- [Planning red teaming for large language models (LLMs) and their applications](../openai/concepts/red-teaming.md)
- [Three takeaways from red teaming 100 generative AI products](https://www.microsoft.com/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)
- [Microsoft AI Red Team building future of safer AI](https://www.microsoft.com/security/blog/2023/08/07/microsoft-ai-red-team-building-future-of-safer-ai/)
