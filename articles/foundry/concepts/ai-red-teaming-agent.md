---
title: "AI Red Teaming Agent"
description: "This article provides conceptual overview of the AI Red Teaming Agent."
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 02/25/2026
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
---

# AI Red Teaming Agent (preview)

[!INCLUDE [ai-red-teaming-agent 1](../includes/concepts-ai-red-teaming-agent-1.md)]

## When to use an AI red teaming run

When thinking about AI-related safety risks developing trustworthy AI systems, Microsoft uses NIST's framework to mitigate risk effectively: Govern, Map, Measure, Manage. We'll focus on the last three parts in relation to the generative AI development lifecycle:

- Map: Identify relevant risks and define your use case.
- Measure: Evaluate risks at scale.
- Manage: Mitigate risks in production and monitor with a plan for incident response.

:::image type="content" source="../media/evaluations/red-teaming-agent/map-measure-mitigate-ai-red-teaming.png" alt-text="Diagram of how to use AI Red Teaming Agent showing proactive to reactive and less costly to more costly." lightbox="../media/evaluations/red-teaming-agent/map-measure-mitigate-ai-red-teaming.png":::

AI Red Teaming Agent can be used to run automated scans and simulate adversarial probing to help accelerate the identification and evaluation of known risks at scale. This helps teams "shift left" from costly reactive incidents to more proactive testing frameworks that can catch issues before deployment. Manual AI red teaming process is time and resource intensive. It relies on the creativity of safety and security expertise to simulate adversarial probing. This process can create a bottleneck for many organizations to accelerate AI adoption. With the AI Red Teaming Agent, organizations can now leverage Microsoft's deep expertise to scale and accelerate their AI development with Trustworthy AI at the forefront.

We encourage teams to use the AI Red Teaming Agent to run automated scans throughout the design, development, and pre-deployment stage:

- Design: Picking out the safest foundational model on your use case.
- Development: Upgrading models within your application or creating fine-tuned models for your specific application.
- Pre-deployment: Before deploying GenAI applications and agents to production.
- Post-deployment: Monitor your Gen AI applications and agents after deployment with scheduled continuous red teaming runs on synthetic adversarial data.

In production, we recommend implementing **safety guardrails** such as [Azure AI Content Safety filters](../../ai-services/content-safety/overview.md) or implementing safety system messages using our [templates](../openai/concepts/safety-system-message-templates.md). For agentic workflows, we recommend leveraging [Foundry Control Plane](../control-plane/overview.md) to apply guardrails and govern your fleet of agents.

[!INCLUDE [ai-red-teaming-agent 2](../includes/concepts-ai-red-teaming-agent-2.md)]

## Supported risk categories

The following risk categories are supported in the AI Red Teaming Agent from [Risk and Safety Evaluations](./evaluation-evaluators/risk-safety-evaluators.md). Only text-based scenarios are supported.

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

For a comprehensive list of tools, see [Tools](../agents/concepts/tool-catalog.md).

[!INCLUDE [ai-red-teaming-agent 3](../includes/concepts-ai-red-teaming-agent-3.md)]
