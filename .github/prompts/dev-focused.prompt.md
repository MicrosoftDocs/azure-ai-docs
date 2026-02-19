---
tools: ['editFiles', 'search', 'problems', 'changes', 'think','todos', 'fetch','openSimpleBrowser', 'microsoft.docs.mcp']
description: 'Evaluate Markdown documentation for developer audiences and produce a prioritized edit plan (no direct edits).'
---

Evaluate a Markdown article and produce a prioritized edit plan. Do not apply changes. Follow behavioral rules defined in the paired chatmode; this prompt adds task-specific evaluation criteria and output expectations.

## Referenced Instruction Files

Reference the instruction files below for detailed guidance. Make sure your recommendations incorporate this information.

- .github/copilot-instructions.md
- .github/instructions/dev-focused.instructions.md
- .github/instructions/foundry-branding.instructions.md

## Goals

### Core goals

- Front-load code as much as possible. We want developers to see working code as soon as possible.
- Include  a minimal runnable example (hello world) when feasible.
- Minimize lengthy descriptions and overviews.
Ensure the first H2 is a prerequisites section; if missing or misplaced, recommend adding/moving one.
- Keep only essential code inline; link to full samples in GitHub.
- Defer deep dives, edge configuration, and troubleshooting to later sections or separate reference/concept content.
- Include all required imports/usings in each snippet (or explicitly note if intentionally truncated).
- Immediately explain each snippet: what it does, required inputs, expected output (success or intentional error).
- After each snippet, add a references line linking to each class/method/schema on Microsoft Learn.
- List any required Azure role-based access control (RBAC) roles (e.g., Reader, Owner) in prerequisites.

### Enable tracking & telemetry
 - When prompted to make changes to an article, ensure that the two values below are added to the article metadata.
    - `ms.custom:`Leave existing custom tags intact and add `dev-focus` to the list.
    - `ai-usage`: if not already present, add `ai-usage: ai-assisted` to the article metadata.

### Plan, don't change

Output only a prioritized plan (move > modify > add) unless explicit user approval to execute is given. Never modify code samples without approval.

### Execution philosophy

- 20% changes for 80% value**: Focus on high-impact improvements using the Pareto principle
- **Preserve, don't replace**: Work within the existing article structure and messaging  as much as possible
- **Targeted fixes**: Address specific issues rather than rewriting entire sections
- **Author collaboration**: Present plans for user approval before implementation
- Change is expensive and prone to risk. Focus on the least amount of change to make the most impact.
- Use the move > modify > add approach. 
  - Move: Focus first on what we can move or remove to better suit developer needs. 
  - Modify: If code samples need to be modified, suggest the minimum modifications that suit developer needs
Add: If we need to add code or text, suggest the minimum additions that suit developer needs
- **CRITICAL**: All code changes require explicit user approval before implementation.
- **Preserve functionality**: Ensure any suggested changes maintain the intended developer workflow

### Input assumptions

- Input is a single Markdown article (or excerpt) intended for developers.
- If metadata (`ms.topic`, language tags) is missing, recommend adding it.
- If the content is empty or purely placeholder, output a scaffold plan only.

## Output expectations

Produce the following sections (in this exact order) in the response:
1. Summary (one–two sentences of overall state).
2. Numbered list of planned changes grouped by impact and effort. Focus on high-impact, low-effort changes first. For each impact category (High, Medium, Low) use these categories:
   - Move: items to reorder, relocate, or remove (issue, recommendation, rationale, risk).
   - Modify: minimal edits to existing text/code.
   - Add: essential additions only. Mark optional enhancements with `[SUGGESTION]`.
3. Gaps & risks: list unverified claims, missing prerequisites, outdated APIs.
4. Scoring snapshot (0–5): density, structure, code readiness, pattern compliance, completeness.
5. Next questions (only if blocked; otherwise omit).
6. Make sure each actionable item is numbered for reference in chat. 

Each item should justify its recommendation with rationale. **In your chat explanations**, you SHOULD cite instruction files, style guides, or patterns (e.g., "per dev-focused.instructions.md", "Microsoft Writing Style Guide"). **In any suggested article text**, provide clean documentation without ANY citations or meta-commentary. Include `[TO VERIFY]` if uncertain. Keep recommendations actionable and minimal; avoid broad rewrites.

## Flags reference

- `[SUGGESTION]`: Optional or nice-to-have improvement; not required for correctness or pattern compliance.
- `[TO VERIFY]`: Uncertain claim lacking a confirmed source; user or editor must validate.

### Clarification rule

Ask  focused clarifying questions only if blocked by: unclear context or intent, ambiguous target pattern, or conflicting instructions. Otherwise proceed with assumptions (state them briefly in Summary).

### Scoring rubric (0–5)

Provide numeric 0–5 scores (0 = absent, 5 = excellent) for: density, structure, code readiness, pattern compliance, completeness. Highlight any score ≤2 in Gaps & risks.

### Non-fabrication & citation

Do not invent APIs, parameters, or file paths. Cite sources or mark `[TO VERIFY]`.

### Internal reference protection

**CRITICAL**: Distinguish between chat explanations and article content:

**In your chat responses** (explaining your reasoning to the user):
- ✅ SHOULD cite instruction files for transparency (e.g., "per foundry-branding.instructions.md", "based on dev-focused.instructions.md")
- ✅ SHOULD reference pattern files and guidelines when justifying recommendations
- ✅ SHOULD cite style guides ("Microsoft Writing Style Guide") when explaining why you recommend changes
- This helps users understand the basis for your suggestions

**In suggested article edits** (the actual text you propose for publication):
- ❌ Do NOT include ANY source citations (internal OR public)
- ❌ Do NOT include phrases like "(Source: foundry-branding.instructions.md)" or "per how-to article pattern" or "following Microsoft Writing Style Guide"
- ❌ Do NOT add meta-commentary about documentation standards
- ❌ Do NOT reference `.github/` files, prompt files, or chatmode files
- ✅ DO provide clean, direct documentation text without citations
- Article content should be written for the end developer/user, not documentation authors

## Evaluation criteria & best practices

### Quality dimensions

Assess along these dimensions:
1. Information density: Trim redundancy; expand underspecified critical steps.
2. Code completeness: Are snippets runnable and contextual (imports, setup, expected output)?
3. Practical implementation: Can a developer act end-to-end? Note missing steps, RBAC, environment setup, SDK install.
4. Structural clarity: Logical heading hierarchy; prerequisites first; outcomes explicit.
5. Pattern alignment: Matches selected template constraints (time to complete, single objective, verification steps).
6. Accuracy & currency: No deprecated APIs; flag uncertainties `[TO VERIFY]`.
7. Accessibility: Alt text, descriptive links, no heading skips.
8. References: Each snippet followed by a references line to official docs only.
9. Visual aids: Suggest a diagram when multi-service architecture or >3 conceptual steps.
10. Language & style: Active voice, second person, sentence case headings.
11. Version-specific content: Identify moniker ranges (`:::moniker range="<version>"` ... `:::moniker-end`) and ensure all edits preserve moniker boundaries and respect version applicability. See `.github/instructions/dev-focused.instructions.md` for details.

### Content & code best practices

Follow these best practices when editing:
- Reduce lengthy descriptions and overview content.
- Front load code to get developers to the "how" quickly. Move conceptual or reference information to later sections or link to reference documentation.
- Front-load key information—start with summaries and code examples.
- After each code snippet, link to the documentation for the classes, methods, or functions used in the code.
- Clear Structure: Organize content with a logical hierarchy and clear purpose. Use descriptive headings according to pattern guidance.
- Explain code snippets and their relevance to the task, ensuring developers understand how to use them in their projects.
- Scannable Layout: Use bullet points, numbered steps, tables, and bold text to highlight key points. Avoid long paragraphs—break content into digestible chunks.
- Preserve Code: Do not modify any code samples without explicit instructions to do so.

#### Code best practices

- Prefer snippet extraction from a maintained GitHub example.
- Include imports/usings at top of each snippet.
- Wrap lines (~80 chars) to avoid horizontal scroll (do not reflow without approval).
- Avoid monolithic scripts—recommend function/class decomposition when clarity gains justify.
- Declare language for every fenced block.
- Provide concise input/output explanation; call out intentionally bad data.
- Include environment setup and dependency installation in prerequisites, not scattered.

### Pattern selection & links

Link to template files instead of duplicating full instructions:
- How-to (`ms.topic: how-to`): `.github/patterns/How-to-template.md` – task-focused, verifiable end state, includes validation steps & troubleshooting.
- Quickstart (`ms.topic: quickstart`): `.github/patterns/Quickstart-template.md` – ≤10 minutes, single outcome, fastest path.
- Tutorial (`ms.topic: tutorial`): `.github/patterns/Tutorial-template.md` – ≤30 minutes, progressive build, single learning objective.

#### Pattern-specific checks

- All: prerequisites first; clear goal statement; complete sequential steps.
- How-to: explicit validation + troubleshooting section.
- Quickstart: minimal narrative; one runnable success checkpoint.
- Tutorial: staged progression; each stage builds on prior with rationale.

### Risk & verification triggers

Flag: missing RBAC, deprecated parameters, absent references after snippets, placeholder metadata, broken heading hierarchy, or scores ≤2.

## Appendix A: Example output

Summary: Strong conceptual depth; runnable code delayed and RBAC missing; structure improvable with early verification snippet.

Planned changes (grouped by impact; each recommendation numbered):

High impact (low effort)
1. Move: Long architecture overview (lines 40–85) to a separate concept article. Issue: blocks first runnable code until ~60% scroll. Rationale: accelerate time to first success. Risk: loss of inline context (mitigate with one-sentence pointer early). 
2. Modify: Split combined prerequisites paragraph into a bulleted list (accounts, required Azure role, SDK install, environment variables). Rationale: scan-ability and completeness. Risk: none.
3. Add: Minimal Python hello world snippet instantiating the client and performing a lightweight list operation to verify auth (includes imports, expected JSON key in output). Rationale: early verification path. Risk: snippet must stay in sync with SDK version. 

Medium impact
4. Move: Troubleshooting subsection (currently mid-body) to end under a dedicated Troubleshooting heading. Issue: interrupts task flow. Rationale: keeps primary path concise. Risk: discoverability (mitigate with anchor link in validation step). 
5. Modify: Add explicit RBAC role names (e.g., Cognitive Services Contributor, Reader) to prerequisites with link to RBAC doc. Issue: missing role clarity. Risk: potential regional variance `[TO VERIFY]`.

Low impact
6. Add: Diagram reference (one-line pointer) for multi-service architecture when >3 Azure resources referenced. Rationale: aids mental model. Risk: optional asset maintenance. [SUGGESTION]
7. Modify: Normalize headings to sentence case (two are Title Case). Rationale: style compliance. Risk: minimal.
8. Add: References line after each code snippet linking to class/method docs (currently absent). Rationale: rapid API discovery. Risk: link rot if APIs move.

Gaps & risks: Missing RBAC roles (item 5); two parameter names appear deprecated (`fooVersion` vs `apiVersion`) `[TO VERIFY]`; no references after snippets (item 8); architecture section front-load slows success (item 1); no early auth validation (item 3).

Scoring snapshot: density 3, structure 2, code readiness 2, pattern compliance 3, completeness 2.



