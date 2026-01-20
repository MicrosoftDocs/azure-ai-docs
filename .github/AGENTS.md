# Doc-Kit: AI-Assisted Documentation System for Azure AI Foundry

**Version 2.0** | Updated 2026-01-08 | AI-first documentation authoring toolkit

This file provides shared instructions for all AI agents working on Azure AI Foundry documentation.

## Architecture Overview

Doc-Kit is a layered AI customization system for creating Diataxis-compliant Azure documentation. The architecture separates concerns across VS Code extension points:

1. **Custom Agents** (`.github/agents/*.agent.md`) - 6 specialized AI agents for different documentation phases
2. **Prompt Files** (`.github/prompts/*.prompt.md`) - Reusable validation and generation workflows
3. **Agent Skills** (`.github/skills/*/SKILL.md`) - Portable capabilities for SDK code retrieval, validation, etc.
4. **Instruction Files** (`.github/instructions/*.instructions.md`) - Conditional guidelines based on file types
5. **GitHub Tools** - Query Azure SDK repositories and documentation via GitHub Copilot's built-in tools

## The Seven Constitutional Principles

All documentation MUST adhere to these principles. These are non-negotiable quality gates.

### Principle I: Diataxis-First Documentation

**CRITICAL**: Never mix Diataxis types in a single article. Each document must be exclusively ONE type:

| Type | User Intent | Content Focus | Analogy |
|------|-------------|---------------|---------|
| **Tutorial** | Learn by doing | Step-by-step learning journey with verification | Cooking class |
| **How-to** | Accomplish a task | Goal-oriented with multiple approaches | Recipe |
| **Reference** | Look up facts | Complete specifications, scannable tables | Ingredient list |
| **Explanation** | Understand concepts | Why/how things work, trade-offs | Food science |

### Principle II: Content Quality Standards

- **Clarity**: Language is clear and concise
- **Accuracy**: Technical details are correct
- **Accessibility**: WCAG 2.1 Level AA compliant
- **SEO**: Optimized for discoverability

### Principle III: Template-Driven Authoring

Every document follows its Diataxis-type-specific template with required sections.

### Principle IV: Context Engineering Integration

AI-generated content requires human verification. Code samples must be sourced from actual SDK repositories.

### Principle V: Pattern Library Compliance

Use Microsoft Learn conventions: alerts (NOTE, TIP, WARNING), tabbed code blocks, includes, proper metadata.

### Principle VI: Information Architecture Excellence

Documents must fit logically in the TOC and include proper cross-references (no orphaned pages).

### Principle VII: Maintainability & Freshness

Include `ms.date` field, version tagging, and plan for content updates.

## SDK Code Retrieval (Preventing Hallucinations)

**CRITICAL**: Always search GitHub repositories before generating code samples.

### Primary Azure SDK Repositories

| Language | Repository | Key Packages |
|----------|------------|--------------|
| Python | `Azure/azure-sdk-for-python` | azure-ai-projects, azure-ai-inference, azure-ai-evaluation, azure-search-documents, azure-openai |
| .NET | `Azure/azure-sdk-for-net` | Azure.AI.Projects, Azure.AI.Inference, Azure.Search.Documents, Azure.AI.OpenAI |
| JavaScript | `Azure/azure-sdk-for-js` | @azure/ai-projects, @azure/ai-inference-rest, @azure/search-documents, @azure/openai |
| Java | `Azure/azure-sdk-for-java` | com.azure.ai.projects, com.azure.ai.inference, com.azure.search.documents, com.azure.ai.openai |
| Go | `Azure/azure-sdk-for-go` | azopenai (limited to OpenAI) |

### OpenAI SDK Repositories

| Language | Repository | Purpose |
|----------|------------|---------|
| Python | `openai/openai-python` | OpenAI official SDK |
| Go | `openai/openai-go` | OpenAI Go SDK |

### Documentation Repositories

- `MicrosoftDocs/azure-ai-docs` - Published Azure AI Foundry documentation (public)
- `MicrosoftDocs/azure-ai-docs-pr` - Private working repository with active feature branches

## Multi-Language Code Syntax

Use Microsoft Learn tabbed format for language selection:

```markdown
# [Python](#tab/python)

\`\`\`python
from azure.ai.projects import AIProjectsClient
from azure.identity import DefaultAzureCredential

client = AIProjectsClient(
    endpoint="https://your-project.azure.com",
    credential=DefaultAzureCredential()
)
\`\`\`

# [.NET](#tab/dotnet)

\`\`\`csharp
using Azure.AI.Projects;
using Azure.Identity;

var client = new AIProjectsClient(
    new Uri("https://your-project.azure.com"),
    new DefaultAzureCredential()
);
\`\`\`

# [JavaScript](#tab/javascript)

\`\`\`javascript
import { AIProjectsClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

const client = new AIProjectsClient(
  "https://your-project.azure.com",
  new DefaultAzureCredential()
);
\`\`\`

---
```

## Accessibility Requirements (WCAG 2.1 AA)

All documentation must meet these accessibility standards:

### Images
- Alt text: 40-150 characters
- Start with graphic type: "Screenshot of...", "Diagram that shows..."
- End with period

### Headings
- Single H1 per article
- Sequential hierarchy: H1 → H2 → H3 → H4 (no skipping)
- Maximum depth: H4

### Links
- Descriptive text (never "click here" or "here")
- Screen-reader friendly

### Tables
- Proper header rows
- Bold first column for data tables

## Metadata Standards (Microsoft Learn)

Required frontmatter fields:

```yaml
---
title: "30-65 chars, primary keyword first"
description: "120-165 chars, primary keyword, action-oriented"
author: github-alias
ms.author: microsoft-alias
ms.date: MM/DD/YYYY
ms.topic: tutorial|how-to|concept|reference
ms.service: azure-ai-services
---
```

## Agent Workflow

The recommended documentation workflow using Doc-Kit agents:

```
1. PLAN (dockit.plan)
   ├── Classify Diataxis type
   ├── Create outline
   ├── Identify resources needed
   └── HANDOFF → appropriate authoring agent

2. AUTHOR (dockit.tutorial | dockit.howto | dockit.reference | dockit.explanation)
   ├── Write content following template
   ├── Retrieve SDK code samples
   ├── Add accessibility-compliant media
   └── HANDOFF → dockit.review

3. REVIEW (dockit.review)
   ├── Validate all 7 constitutional principles
   ├── Check accessibility
   ├── Verify code security
   ├── Generate publication decision
   └── HANDOFF → back to authoring agent if revisions needed

4. PUBLISH
   └── Content passes all quality gates
```

## Quality Gates Checklist

Before any documentation can be published, verify:

| Gate | Validation | Blocker? |
|------|------------|----------|
| Diataxis Purity | Single type, no mixing | ✅ YES |
| Accessibility | WCAG 2.1 AA compliant | ✅ YES |
| Technical Accuracy | Code samples tested | ✅ YES |
| Style Conformance | Microsoft Writing Style Guide | HIGH |
| Link Validity | No broken internal links | HIGH |
| Metadata | All frontmatter fields present | MEDIUM |
| SEO | BLUF + keyword density | MEDIUM |

## Terminology Consistency

**Product Names** (MUST be consistent):
- ✅ "Azure AI Foundry" (not "Foundry", "AI Foundry", "Azure Foundry")
- ✅ "Azure OpenAI Service" (not "Azure OpenAI", "OpenAI Service")
- ✅ "GPT-4" with hyphen (not "GPT4", "gpt-4")

**SDK/API Terms**:
- ✅ Exact class names: `AIProjectsClient` not "AI Project Client"
- ✅ Package names lowercase: `azure-ai-projects` not "Azure-AI-Projects"

## Related Resources

- [Diataxis Framework](https://diataxis.fr) - Documentation architecture
- [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/)
- [WCAG 2.1 Accessibility](https://www.w3.org/WAI/WCAG21/quickref/)
- [VS Code Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Agent Skills Standard](https://agentskills.io/)
