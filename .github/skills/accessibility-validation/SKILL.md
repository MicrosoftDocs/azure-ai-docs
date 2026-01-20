---
name: accessibility-validation
description: Validate documentation for WCAG 2.1 Level AA accessibility compliance. Use this skill to check images, headings, links, and tables meet accessibility standards before publication.
---

# Accessibility Validation Skill

This skill validates documentation against WCAG 2.1 Level AA accessibility requirements.

## When to Use

- Before publishing any documentation
- When reviewing documentation with images
- When checking heading structure
- When validating link text and tables

## Accessibility Requirements

### 1. Images (Alt Text)

**Standard**: All images must have descriptive alt text.

| Requirement | Value |
|-------------|-------|
| Length | 40-150 characters |
| Format | Start with graphic type: "Screenshot of...", "Diagram that shows..." |
| Ending | Must end with a period |
| Content | Describe what the image shows, not just its subject |

**Good Example**:
```markdown
![Screenshot of the Azure AI Foundry portal showing the Deployments page with three GPT-4 models listed.](media/deployments-list.png)
```

**Bad Examples**:
```markdown
![deployments](media/deployments-list.png)  <!-- Too short, not descriptive -->
![Click here to see the deployments](media/deployments-list.png)  <!-- Action-oriented -->
```

### 2. Headings

**Standard**: Headings must follow proper hierarchical structure.

| Requirement | Rule |
|-------------|------|
| Single H1 | Only one H1 per article (the title) |
| No skipping | H1 → H2 → H3 → H4 (never H1 → H3) |
| Max depth | 4 levels maximum (H1 through H4) |
| Logical nesting | Subheadings must relate to parent |

**Good Example**:
```markdown
# Tutorial: Deploy a Model

## Prerequisites

## Step 1: Create deployment

### Configure settings

### Verify status

## Step 2: Test deployment
```

**Bad Example**:
```markdown
# Tutorial: Deploy a Model

#### Configure settings  <!-- Skipped H2, H3 -->

# Another section  <!-- Multiple H1s -->
```

### 3. Links

**Standard**: Link text must be descriptive and readable out of context.

| Requirement | Rule |
|-------------|------|
| Descriptive | Clearly indicates destination |
| No generic phrases | Avoid "click here", "read more", "here" |
| Context-independent | Screen reader users understand without surrounding text |

**Good Examples**:
```markdown
For more information, see [Azure AI Foundry pricing](link).
Learn more about [model deployment strategies](link).
```

**Bad Examples**:
```markdown
For more information, click [here](link).
See [this page](link) for details.
```

### 4. Tables

**Standard**: Tables must have proper headers and structure.

| Requirement | Rule |
|-------------|------|
| Header row | First row must define column headers |
| Bold first column | For data matrix tables |
| No merged cells | Markdown doesn't support cell merging |

**Good Example**:
```markdown
| **Feature** | **Basic** | **Standard** |
|-------------|-----------|--------------|
| **Models** | 5 | 20 |
| **Storage** | 10 GB | 100 GB |
```

## Validation Output Format

Report violations using this structure:

```markdown
### Accessibility Violation {number}

**Severity**: [BLOCKER | HIGH | MEDIUM | LOW]
**Category**: [Images | Headings | Links | Tables]
**Location**: Line {number} or Section "{name}"

**Issue**: {Description}

**Current**:
{problematic markdown}

**Recommended Fix**:
{corrected markdown}

**Explanation**: {Why this matters}
```

## Severity Classifications

| Severity | Examples | Action |
|----------|----------|--------|
| BLOCKER | Missing alt text, multiple H1s, "click here" links | Must fix before publish |
| HIGH | Alt text missing graphic type, generic link text | Should fix before publish |
| MEDIUM | Alt text >150 chars, data tables without bold first column | Nice to fix |
| LOW | Alt text could be more descriptive | Optional improvement |

## Quality Checklist

After validation, verify:

- [ ] All images have alt text 40-150 characters
- [ ] All alt text has graphic type prefix
- [ ] All alt text ends with a period
- [ ] Exactly one H1 per article
- [ ] No skipped heading levels
- [ ] Maximum heading depth is H4
- [ ] No "click here" link text
- [ ] All links have descriptive text
- [ ] All tables have header rows
