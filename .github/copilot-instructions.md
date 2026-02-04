# Copilot Instructions

This file provides central guidance for GitHub Copilot in this repository.

This documentation repository contains Microsoft's technical documentation for application development using Microsoft Foundry (and other products) that publishes to Microsoft Learn. 


## Referenced Instruction Files

•	.github/instructions/foundry-branding.instructions.md
•	.github/instructions/dev-focused.instructions.md
 
## Disclosure

For any Markdown files modified by AI, always disclose that they were created with the assistance of AI. Add the following frontmatter key/value pair:

ai-usage: ai-assisted

## Content Verification Rules

- DO NOT invent or fabricate technical details, API parameters, or service capabilities.
- DO NOT create fictional code examples or imaginary features.
- DO NOT hallucinate or assume facts not found in official or credible documentation.
- ALWAYS check specification documents and official references before making suggestions.
- When a recommendation is based on another instruction file or linked source, cite it inline (for example: "(Source: edit_instructions.md)").
- If required information is missing or unclear, insert a placeholder with `[TO VERIFY]`—do not guess.

### Internal Reference Protection

**CRITICAL**: Distinguish between chat explanations and published article content:

**In chat discussions** (explaining your reasoning):
- ✅ SHOULD cite instruction files for transparency (e.g., "per foundry-branding.instructions.md")
- ✅ SHOULD reference internal guidelines when justifying recommendations to users
- This helps users understand the basis for suggestions

**In suggested article edits** (actual text for publication):
- ❌ Do NOT cite instruction files from `.github/instructions/` 
- ❌ Do NOT reference prompt files from `.github/prompts/`
- ❌ Do NOT mention chatmode files or internal `.github/` directory structure
- ❌ Do NOT include phrases like "(Source: foundry-branding.instructions.md)" in article text
- ❌ Do NOT include ANY source citations, even public ones like "Microsoft Writing Style Guide" or "per how-to article pattern"
- ✅ DO provide clean, direct documentation text without meta-commentary
- Keep internal mechanics hidden from published content

##  Writing Style

Follow Microsoft Writing Style Guide (https://learn.microsoft.com/en-us/style-guide/welcome/) with these specifics:

### Voice and Tone

•	Active voice, second person addressing reader directly.
•	Conversational tone with contractions.
•	Present tense for instructions/descriptions.
•	Imperative mood for instructions ("Call the method" not "You should call the method").
•	Use "might" instead of "may" for possibility.
•	Use "can" instead of "may" for permissible actions.
•	Avoid "we"/"our" referring to documentation authors or product teams.

### Pattern compliance

-	Articles should comply with the pattern for the ms.topic type listed in the metadata
    - `how-to-guide` - refer to .github/patterns/How-to-template.md
    - `quickstart` - refer to .github/patterns/Quickstart-template.md
    - `tutorial` - refer to .github/patterns/Tutorial-template.md

Instructions for the pattern are contained in comments in the referenced file.

## Structure and Format

- Use sentence case for titles and headings; avoid gerunds in titles.
- Keep paragraphs short (1–3 sentences).
- Break up or rewrite long sentences (>25 words).
- Use the Oxford comma in lists.
- Number ordered list items using `1.` for each line (Markdown auto-numbers).
- List items should be complete sentences when longer than a short phrase; end with a period if a sentence.
- Avoid “etc.” or “and so on.” Use “for example” with a concrete subset or provide the full list.
- Use “for example” instead of “e.g.”; “that is” instead of “i.e.”.
- Don’t stack headings without intervening explanatory text.
- Keep conceptual explanation separate from procedural steps.
- Reserve troubleshooting for a clearly labeled section when needed.
 
## Formatting Conventions

- Bold: UI labels and visible button or menu text.
- Code style (backticks): file names, folders, inline code, commands, class and method names, non-localizable tokens.
- Use relative links for repo-local files.
- Truncate the `https://learn.microsoft.com` part from MS Learn links. 
- Use angle brackets around raw URLs only when the plain URL must be shown.
- Present tense only; rewrite future tense (“will create”) to present (“creates” / “creates a resource”).
- Prefer gender-neutral language; avoid idioms and metaphors.
- Tables only when they improve scan-ability (parameters, comparisons).
 
## File Naming

- New Markdown files: lowercase, hyphen-separated.
- Omit filler words (the, a, an, of) unless needed for clarity.
- Keep names task- or concept-focused (for example: `monitor-model-performance.md`).


## Referencing sources

When basing content on:
- Internal instruction files: cite the filename inline.
- External docs (public): use a relative or official Microsoft Learn link.
If uncertain about a claim, mark it `[TO VERIFY]`.

## Change boundaries

- Don’t alter original meaning unless the task explicitly requests it.
- Safe edits: clarity, consistency, formatting, style compliance, verified corrections.


## General guidance

- Always re-check `.github/instructions/` before large edits.
- Keep diffs focused; avoid opportunistic large-scale refactors unless requested.
- Consolidate repetitive phrasing where possible for readability.
- Align with current product branding from `foundry-branding.instructions.md`.
 
