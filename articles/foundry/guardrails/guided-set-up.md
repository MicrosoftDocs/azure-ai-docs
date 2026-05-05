---
title: Guided guardrail setup
titleSuffix: Azure AI services
description: This is a guide to set up guided guarrails.
author: ssalgadodev
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 05/05/2026
ms.author: ssalgado

---

# Guided guardrail setup

Guided guardrail setup helps you configure appropriate safety and security controls for your agent based on how it is designed and used.

Instead of manually selecting controls, you answer a set of questions. Microsoft Foundry uses your responses to recommend guardrails and apply them at the correct intervention points (user input, tool calls, tool responses, and output). [Guardrails...soft Learn | Learn.Microsoft.com]

---

### Why use guided guardrail setup?

Each agent is purpose-built for a specific scenario and may differ in:

- Who can access it  
- What data it handles  
- What tools it uses  
- Whether it can take actions  

Because these factors affect risk, guardrails should be tailored to each agent, not applied as a single default.

Guided guardrail setup ensures:

- Relevant protections are applied based on agent design  
- Controls are scoped to where they are needed  
- The agent remains both safe and usable  

---

## How it works

You answer questions about your agent in three areas:

#### Who the agent is for

- Who will use this agent? (for example, public users or internal teams)

**Why it matters:**  
Broader access increases exposure to unexpected or adversarial inputs.

---

#### What inputs and data the agent handles

- Where does the agent receive inputs from?  
- Will it access or return sensitive data?  

**Why it matters:**  
External inputs increase risk of prompt injection. Sensitive data increases risk of data exposure.

---

#### What tools and actions the agent uses

- Does the agent call external tools?  
- Can it take real-world or consequential actions?  
- Does it handle personal data or generate code?  

**Why it matters:**  
Tool usage and actions introduce additional risks that require targeted controls.

---

### From answers to guardrails

Based on your responses, Microsoft Foundry:

- Identifies relevant risk categories  
- Recommends appropriate controls  
- Applies those controls across the correct intervention points:  
  - User input  
  - Tool calls  
  - Tool responses  
  - Output  

---

### Guided guardrail setup questions and outcomes

The following table shows how responses during guided setup map to potential risks and recommended guardrails.

| Area | Question | Why it matters | Example risks | Recommended controls |
|------|----------|----------------|---------------|---------------------|
| Who is this agent designed for? | Determines exposure to untrusted or adversarial input | Content safety issues, jailbreak attempts | Content safety filtering, jailbreak protections |
| Where does the agent receive inputs from? | External or untrusted inputs may contain malicious or hidden instructions | Prompt injection (XPIA) | Prompt injection defenses, input grounding/spotlighting |
| Can the agent surface content from external or user-provided sources? | Tool outputs may introduce untrusted content into the system | Prompt injection (XPIA) via tool responses | Tool response validation, spotlighting |
| Will the agent access, process, or return sensitive data? | Sensitive data flowing across tools and outputs may be exposed unintentionally | Sensitive data leakage | Data protection controls, suspicious tool chain detection |
| Does the agent handle personal data about individuals? | Personal data requires additional safeguards to prevent misuse or exposure | Personally identifiable information (PII) leakage | PII detection and protection |
| Can the agent take real-world or consequential actions? | Incorrect or manipulated actions can have real-world impact | Misaligned or unintended actions | Task adherence controls, action validation |
| Does the agent generate, modify, or execute code? | Generated code may introduce security or IP risks | IP infringement, unsafe code generation | Protected material detection, code safety controls |

---

### Key principle

Guardrails should match the agent’s purpose and context.

Agents built on the same model can require different guardrails depending on their scenario. Guided guardrail setup ensures configurations are scenario-specific and aligned with intended use.

---

### Summary

Guided guardrail setup helps you:

- Capture agent intent (users, data, tools)  
- Identify where risk can occur  
- Apply tailored guardrails instead of generic defaults  
- Protect your agent across its full execution flow  
