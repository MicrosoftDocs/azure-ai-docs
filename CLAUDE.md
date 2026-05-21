# Claude Instructions — azure-ai-docs-pr

This documentation repository contains Microsoft's technical documentation for application development using Microsoft Foundry (and other products) that publishes to Microsoft Learn.

## Doc-Kit System

This repo uses Doc-Kit v4.3.0. See `.github/AGENTS.md` for the full agent system specification including:
- Custom agents: dockit.plan, dockit.author, dockit.evaluate, dockit.researcher, dockit.review
- Skills catalog (evaluation, validation, research, authoring, vision)
- Multi-language code reference pipeline
- Quality gates checklist
- Constitutional principles

Setup:
```bash
cd .dockit && python -m venv .venv && source .venv/bin/activate
pip install -r evaluate/requirements.txt
pipx install "git+ssh://git@github.com/coreai-microsoft/doc-review-agent.git"
gh auth login && az login && azd auth login
```

## Referenced Instruction Files

- .github/instructions/foundry-branding.instructions.md
- .github/instructions/dev-focused.instructions.md

## Disclosure

For any Markdown files modified by AI, add the following frontmatter key/value pair:

```
ai-usage: ai-assisted
```

## Content Verification Rules

- DO NOT invent or fabricate technical details, API parameters, or service capabilities.
- DO NOT create fictional code examples or imaginary features.
- ALWAYS check specification documents and official references before making suggestions.
- When a recommendation is based on another instruction file or linked source, cite it inline.
- If the required information is missing or unclear, insert a placeholder with `[TO VERIFY]` — do not guess.

### Internal Reference Protection

**In chat discussions**: cite instruction files for transparency.

**In suggested article edits** (actual text for publication):
- DO NOT cite instruction files from `.github/instructions/`
- DO NOT reference prompt files, chatmode files, or internal `.github/` directory structure
- DO NOT include ANY source citations in article text
- DO provide clean, direct documentation text without meta-commentary

## Writing Style

Follow [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/):

### Voice and Tone
- Active voice, second person.
- Conversational tone with contractions.
- Present tense for instructions/descriptions.
- Imperative mood for instructions.
- Use "might" instead of "may" for possibility; "can" instead of "may" for permission.
- Avoid "we"/"our" referring to documentation authors or product teams.

### Structure and Format
- Sentence case titles and headings; avoid gerunds in titles.
- Paragraphs: 1-3 sentences.
- Break up sentences >25 words.
- Oxford comma in lists.
- Number ordered list items using `1.`.
- Use "for example" instead of "e.g."; "that is" instead of "i.e.".
- Don't stack headings without intervening text.

### Formatting Conventions
- Bold: UI labels and visible button/menu text.
- Code style (backticks): file names, folders, inline code, commands, class and method names.
- Relative links for repo-local files.
- Truncate `https://learn.microsoft.com/en-us/` from MS Learn links.
- Update bookmark links when changing H2 headers.
- Present tense only.

## File Naming

- New Markdown files: lowercase, hyphen-separated.
- Omit filler words unless needed for clarity.
- Keep names task- or concept-focused.

## Change Boundaries

- Don't alter original meaning unless the task explicitly requests it.
- Safe edits: clarity, consistency, formatting, style compliance, verified corrections.

## General Guidance

- Always re-check `.github/instructions/` before large edits.
- Keep diffs focused; avoid opportunistic large-scale refactors unless requested.
- Align with current product branding from `foundry-branding.instructions.md`.
