---
description: 'Branding instructions for Microsoft and related services and components.'
applyTo: '*/articles/ai-foundry/**/*.md'
---

# Branding instructions for Foundry documentation

Your role is to ensure that all references to Microsoft  Foundry, its components, and related services are accurate and consistent with official branding guidelines.

## First-mention vs. subsequent-mention patterns

In our documentation, we use different terminology on first mention versus subsequent mentions within an article. This helps establish full context initially while maintaining readability throughout the document.

### Core product and services

| Original Term | New term - First Mention | New term - Subsequent Mentions |
|---------------|---------------|---------------------|
| Azure AI Foundry | Microsoft Foundry | Foundry |
| Azure AI Foundry Agent Service | Foundry Agent Service | Agent Service |
| Azure AI Foundry IQ | Foundry IQ in Foundry Tools | Foundry IQ |
| Azure AI Foundry SDK | Microsoft Foundry SDK | Microsoft Foundry SDK |

### AI services in Foundry Tools

When referencing individual AI services, use the pattern "Azure [Service] in Foundry Tools" on first mention, then just the service name subsequently:

| Original Term | New term - First Mention | New term - Subsequent Mentions |
|---------------|---------------|---------------------|
| Azure AI Speech | Azure Speech in Foundry Tools | Speech |
| Azure AI Language | Azure Language in Foundry Tools | Language |
| Azure AI Vision | Azure Vision in Foundry Tools | Vision |
| Azure AI Document Intelligence | Azure Document Intelligence in Foundry Tools | Document Intelligence |
| Azure AI Form Recognizer | Azure Document Intelligence in Foundry Tools | Document Intelligence |
| Azure AI Translator | Azure Translator in Foundry Tools | Translator |
| Azure AI Content Understanding | Azure Content Understanding in Foundry Tools | Content Understanding |

**Note**: Azure AI Form Recognizer is now referred to as Azure Document Intelligence.

### Model catalog

| Original Term |New term - First Mention | New term - Subsequent Mentions |
|---------------|---------------|---------------------|
| Azure AI model catalog | Foundry model catalog | model catalog |
| Azure AI Foundry model catalog | Foundry model catalog | model catalog |

## Protected terms (never replace)

The following terms must **NEVER** be changed, regardless of context:

- **Azure OpenAI** — Retains "Azure" branding as a distinct service
- **Azure AI Projects client library** — SDK/library names remain unchanged (all case variations)
- **Azure Project client library** — SDK/library names remain unchanged (all case variations)
- **Azure AI services subscription** — Subscription terminology remains unchanged (all case variations)
- **"Azure AI Foundry is now Microsoft Foundry"** — The announcement phrase itself must not be altered

**Rationale**: These terms represent specific technical artifacts (SDKs, subscription types) or the rebrand announcement that require exact terminology for accuracy.

## Special handling rules

### Historical context preservation

When terms appear in historical or explanatory contexts (using "formerly," "previously," or "originally"), preserve the original terminology. This maintains historical accuracy.

**Examples**:
- ✅ Correct: "Document Intelligence (formerly Azure AI Form Recognizer)"
- ✅ Correct: "This feature was previously called Azure AI Studio"
- ❌ Incorrect: "Document Intelligence (formerly Document Intelligence)" — the old name should remain

### Metadata and titles

In YAML frontmatter (metadata) and the article's main title (first `#` heading):
- Always use the **first-mention** form, even if the term appears multiple times
- This ensures consistency in titles, descriptions, and metadata fields

### YAML files vs. Markdown files

- **YAML files** (TOC, configuration): Use **first-mention** form uniformly throughout (no differentiation between first and subsequent uses)
- **Markdown files** (articles): Apply first-mention/subsequent-mention logic within the body content

### Grammar corrections

After shortening service names, ensure proper article usage:

- Use "a" (not "an") before: Foundry, Microsoft, Language, Speech, Translator, Vision
- **Examples**:
  - ✅ "a Foundry resource"
  - ✅ "a Speech service"
  - ❌ "an Foundry resource"

### Portal capitalization

Use lowercase "portal" in compound terms:
- ✅ "Azure portal"
- ✅ "Foundry portal"
- ❌ "Azure Portal"
- ❌ "Foundry Portal"

### Bookmark and anchor standardization

When referencing document sections or creating anchors, use simplified forms:
- Remove redundant "azure-ai" and "ai-foundry" prefixes
- Use shortest clear form
- **Examples**:
  - ✅ `#create-a-guardrail-in-foundry`
  - ✅ `#view-quotas-in-foundry-portal`
  - ❌ `#create-a-guardrail-in-azure-ai-foundry`

## Excluded content

### Deprecated service folders

Do **not** apply rebranding rules to the following deprecated service directories (retain original terminology):
- `anomaly-detector`
- `content-moderator`
- `immersive-reader`
- `luis`
- `metrics-advisor`
- `personalizer`
- `qnamaker`


## Application guidelines

### Processing sequence

When applying branding rules, follow this order:

1. **Protect** never-replace terms (temporarily preserve them)
2. **Apply first-mention logic** to body content (first occurrence vs. subsequent)
3. **Apply uniform replacements** to metadata and titles (always first-mention form)
4. **Apply cleanup** (grammar, capitalization, bookmarks)
5. **Restore** protected terms

### Content sections

Different parts of a document receive different treatment:

- **Metadata (YAML frontmatter)**: All occurrences use first-mention form
- **Title (first `#` heading)**: All occurrences use first-mention form
- **Body content**: First occurrence uses first-mention, subsequent use short form

### Compound phrases

Some phrases receive special uniform treatment regardless of position:

- References to "Azure AI Foundry portal" should become "Foundry portal"
- Service-specific compound phrases should be simplified consistently
- Links and headings containing these phrases should be updated accordingly

## Examples

### First mention within body content

**Before**:
```markdown
Azure AI Foundry provides powerful capabilities. You can use Azure AI Foundry to build applications.
```

**After**:
```markdown
Microsoft Foundry provides powerful capabilities. You can use Foundry to build applications.
```

### AI service with context

**Before**:
```markdown
# Use Azure AI Speech

Azure AI Speech provides voice capabilities. Configure Azure AI Speech in your application.
```

**After**:
```markdown
# Use Azure Speech in Foundry Tools

Azure Speech in Foundry Tools provides voice capabilities. Configure Speech in your application.
```

### Historical context (preserved)

**Before**:
```markdown
Document Intelligence (formerly Azure AI Form Recognizer) processes documents.
```

**After** (unchanged):
```markdown
Document Intelligence (formerly Azure AI Form Recognizer) processes documents.
```

### Protected terms

**Before**:
```markdown
Use Azure OpenAI models through Azure AI Foundry. Install the Azure AI Projects client library.
```

**After**:
```markdown
Use Azure OpenAI models through Microsoft Foundry. Install the Azure AI Projects client library.
```

## Summary

Apply first-mention/subsequent-mention patterns consistently, respect protected terms, preserve historical context, and follow special handling rules for metadata, titles, grammar, and deprecated services. When in doubt, consult the source CSV files in `.github/rebrand-main/patterns/` for definitive rules.
