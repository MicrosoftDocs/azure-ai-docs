---
applyTo: "**/tutorials/**/*.md"
---

# Tutorial Documentation Guidelines

Apply these conventions when creating or editing tutorial documentation.

## Tutorial Definition

A tutorial is a **learning-oriented** document that takes the reader through a hands-on exercise to acquire new skills. Think of it as a cooking class.

## Required Structure

Every tutorial must include these sections:

### 1. Title
Format: "Tutorial: [Action verb] [your first | a] [noun]"

Examples:
- "Tutorial: Build your first AI agent"
- "Tutorial: Deploy a model to Azure AI Foundry"

### 2. Introduction
- 1-2 paragraphs maximum
- State what the reader will learn
- State what they'll build
- Include estimated time to complete

### 3. Prerequisites
List everything needed:
- Azure subscription
- Required tools/software
- Previous knowledge (link to resources)
- Required permissions

### 4. Numbered Steps
- One action per step
- Start with imperative verb
- Include verification after significant steps
- Add screenshots for UI-based actions

### 5. Verification Step
Help the reader confirm success:
- Expected output
- What to check
- Common success indicators

### 6. Clean Up
Always include cleanup:
- How to delete resources
- Cost implications if not deleted

### 7. Next Steps
- Related tutorials (progressive)
- How-to guides for specific tasks
- Reference documentation

## Writing Rules

- **One path only** - Don't offer alternatives (that's for how-to guides)
- **Minimal explanation** - Teach by doing, not by reading
- **Small successes** - Let readers verify progress frequently
- **Forgive mistakes** - Include troubleshooting tips at error-prone steps

## Do Not Include

- Exhaustive option lists (→ reference)
- "Why" explanations (→ explanation)
- Alternative approaches (→ how-to)
- Production considerations (→ how-to)
