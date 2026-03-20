---
title: Include file
description: Include file
author: lgayhardt
ms.reviewer: minthigpen
ms.author: lagayhar
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

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

- [Azure AI Risk and Safety Evaluations](../concepts/safety-evaluations-transparency-note.md)
- [PyRIT: Python Risk Identification Tool](https://github.com/Azure/PyRIT)

The most effective strategies for risk assessment we've seen use automated tools to surface potential risks, which are then analyzed by expert human teams for deeper insights. If your organization is just starting with AI red teaming, we encourage you to explore the resources created by our own AI red team at Microsoft to help you get started.

- [Planning red teaming for large language models (LLMs) and their applications](../openai/concepts/red-teaming.md)
- [Three takeaways from red teaming 100 generative AI products](https://www.microsoft.com/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)
- [Microsoft AI Red Team building future of safer AI](https://www.microsoft.com/security/blog/2023/08/07/microsoft-ai-red-team-building-future-of-safer-ai/)
