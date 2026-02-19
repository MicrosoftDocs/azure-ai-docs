---
description: 'Instructions file for dev-focused edits using the related prompt and chat mode.'
applyTo: '*/articles/**/*.md'
---

Instructions for Foundry Dev-Focused Chat Mode

**CRITICAL - Internal Reference Protection**: When explaining your reasoning in chat, you SHOULD cite this file and other instruction files for transparency. However, NEVER include ANY source citations (internal or public) in the actual article content you suggest for publication. Published content should be clean documentation without meta-commentary about style guides or patterns.

You have access to MCP tools called `microsoft_docs_search` and `microsoft_docs_fetch` - these tools allow you to search through and fetch Microsoft's latest official documentation, and that information might be more detailed or newer than what's in your training data set.

If a question includes a Microsoft product, service, or technology, you should leverage these tools to search for an answer and to fetch content for deep research.

# Accelerate time to first success
*    Front-load the code so that developers can begin reading/using it as soon as possible. 
*    Remember that the prerequisite section must be the first h2
*    If possible, start with a basic "hello world" sample to fail or succeed early
*    Save information on edge configurations, troubleshooting, deep dives, etc. for the end of the article or move to concept or reference article
*    Show only the most important code for the concept; link to GitHub for complete examples
*    Show complete imports: Always include all import/using statements at the top of code snippets
*    Clearly describe what each example does and expected results
*    For each code snippet, add a section under it with links to the referenced classes, methods, schemas, etc. Search Microsoft Docs for the relevant links. Use the "Reference: [<class/method/schema name>](url)" format.
*    List any special RBAC requirements that might need to be setup by a subscription owner (such as reader roles) in the prereqs

# Code Best Practices
*    If possible, the article should pull code snippets from a full example that lives in GitHub and is maintained by Engineering.
*    Always show import/using statements at the top of a snippet.
*    After each snippet, list links to referenced classes, methods, schemas, etc.
*    Enforce an 80-character line wrap to eliminate horizontal scrolling for code imported into docs as a snippet.
*    Avoid monolithic scripts and encapsulate logic into clearly named functions and classes.
*    Specify programming language: Use correct devlang tags (JSON, .NET, Python) for all code snippets
*    Show complete context: Include all necessary setup code and dependencies.
*    Always include prerequisites: Add bullet lists with dependencies and assumptions for each code section
*    Clearly explain the input and output of an example; in some cases, the input is "bad" data or the expected output is an error. Call these out so the user understands what the example does and the output to expect. Also to reduce change requests to "fix" bad data.

## Conceptual tabs for Code language
*    Use language tabs for multiple languages (Python, .NET, REST, etc.) when the article is not specific to a single language.
*    Ensure that each language tab has equivalent content. If a language does not support a feature, add a note in that tab.
*    Tabs should be listed in the same order, and use consistent titles. The correct order is Python, C#, JavaScript/TypeScript, and Java. Additional languages are allowed, but when any ofthese four are present, they should be listed in the order below.
    *    [Python](#tab/python)
    *    [C#](#tab/csharp)
    *    [JavaScript/TypeScript](#tab/javascript)
    *    [Java](#tab/java)

* If the content for the above language is not available, flag it in your recommendations.

# Version-Specific Content (Monikers)

Some articles contain version-specific content using moniker ranges. Monikers allow a single article to serve multiple product versions by tagging sections that apply only to specific versions.

## Understanding Monikers

### Moniker Metadata
Articles that support multiple versions declare this in the YAML frontmatter:
```yaml
monikerRange: '<version 1> || <version 2>'
```

### Moniker Range Blocks
Version-specific content is wrapped in moniker range tags:
```markdown
:::moniker range="<version 1>"
[Content that applies ONLY to version 1]
:::moniker-end
```

### Untagged Content
Any content NOT wrapped in moniker tags applies to ALL versions listed in the document's `monikerRange` metadata.

## Critical Moniker Editing Rules

When reviewing or editing articles with monikers, you MUST:

1. **Identify all moniker ranges** before suggesting any edits. Scan the article for `:::moniker range="<version>"` and `:::moniker-end` pairs.

2. **Preserve moniker syntax exactly**. Never:
   - Delete or malform `:::moniker range="<version>"` opening tags
   - Delete or malform `:::moniker-end` closing tags
   - Break the pairing between opening and closing tags
   - Introduce typos in the version identifiers

3. **Respect version boundaries**. When editing content:
   - Content inside a moniker block applies ONLY to that version
   - Do NOT move content out of a moniker block unless explicitly instructed
   - Do NOT add content inside a moniker block if it should apply to all versions
   - Do NOT duplicate content across multiple moniker blocks unless intentional

4. **Treat each moniker range as a discrete unit**:
   - Edits to version 1-specific content must stay within the `:::moniker range="<version 1>"` block
   - Edits to version 2-specific content must stay within the `:::moniker range="<version 2>"` block
   - Edits to shared content must remain OUTSIDE any moniker blocks

5. **Flag version-specific concerns** in your recommendations:
   - Note when suggested changes affect only one version
   - Identify when similar changes might be needed across multiple version blocks
   - Warn if moving content would change its version applicability

## Common Moniker Patterns

- **Next steps sections**: Often version-specific with different links for each API version
- **Code examples**: May differ significantly between versions, requiring separate moniker blocks
- **Deprecated features**: Typically wrapped in the older version's moniker range with deprecation notices
- **New features**: Often in newer version moniker blocks only

## Example: Safe Edit Within Monikers

**Before:**
```markdown
:::moniker range="<version 1>"
To deploy the model, use the `AciWebservice.deploy_configuration()` method.
:::moniker-end
```

**Safe Edit (preserves moniker boundary):**
```markdown
:::moniker range="<version 1>"
To deploy the model, use the `AciWebservice.deploy_configuration()` method. For more information, see [Deploy models](./v1/how-to-deploy-and-where.md).
:::moniker-end
```

**Unsafe Edit (breaks moniker):**
```markdown
To deploy the model, use the `AciWebservice.deploy_configuration()` method. For more information, see [Deploy models](./v1/how-to-deploy-and-where.md).
:::moniker-end
```
*(The opening tag was deleted - content now incorrectly applies to all versions)*

# Pattern and schema compliance

Ensure that the article complies with the relevant patterns, as listed below. Instructions for the pattern are contained in comments in the referenced file.

## How to articles
For articles with the `ms.topic: how-to` tag, ensure the article follows the How-To Article Pattern. See `.github/patterns/How-to-template.md` for details. 

## Quickstarts
For articles with the `ms.topic: quickstart` tag, ensure the article follows the Quickstart Article Pattern. See `.github/patterns/Quickstart-template.md` for details.

## Tutorials
For articles with the `ms.topic: tutorial` tag, ensure the article follows the Tutorial Article Pattern. See `.github/patterns/Tutorial-template.md` for details.

# Branding compliance

For all articles, verify terminology follows the branding guidelines detailed in `.github/instructions/foundry-branding.instructions.md`. While these guidelines primarily apply to Foundry content, the patterns ensure consistent terminology across all documentation.

## Key Areas to Check

When reviewing content for branding compliance, focus on:

- **First-mention vs. subsequent-mention patterns**: Verify correct terminology on first vs. subsequent uses (e.g., "Microsoft Foundry" → "Foundry")
- **Protected terms**: Ensure terms like "Azure OpenAI" and SDK/library names remain unchanged
- **Historical context**: Preserve original terminology in "formerly/previously/originally" contexts
- **Grammar corrections**: Verify proper article usage (a/an) after service name changes
- **Metadata and titles**: Confirm YAML frontmatter and main titles use first-mention forms consistently
- **Bookmark references**: Check that section anchors are simplified without redundant prefixes

## Priority Guidance

- **High Impact**: Incorrect product names in titles/first mentions, protected terms changed incorrectly, historical context altered
- **Medium Impact**: Missing "in Foundry Tools" qualifiers, inconsistent first-mention/subsequent-mention usage, grammar errors
- **Low Impact**: Portal capitalization, bookmark simplification, minor consistency improvements

## Implementation Notes

- Apply branding checks to all articles, with primary focus on Foundry content
- Skip deprecated service folders (anomaly-detector, content-moderator, immersive-reader, luis, metrics-advisor, personalizer, qnamaker)
- When explaining recommendations in chat, cite foundry-branding.instructions.md for transparency
- Never include source citations in the actual article content suggestions

For complete branding rules, examples, and detailed guidance, refer to `.github/instructions/foundry-branding.instructions.md`.






