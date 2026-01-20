---
applyTo: "**/how-to/**/*.md,**/howto/**/*.md"
---

# How-to Guide Documentation Guidelines

Apply these conventions when creating or editing how-to documentation.

## How-to Definition

A how-to guide is a **task-oriented** document that helps experienced users accomplish a specific goal. Think of it as a recipe.

## Required Structure

### 1. Title
Format: "How to [verb] [noun]" or "[Verb] [noun]"

Examples:
- "How to deploy a model"
- "Configure model endpoints"
- "Manage API keys"

### 2. Introduction
- 1 paragraph maximum
- State the goal clearly
- Mention prerequisites briefly

### 3. Prerequisites
Brief list:
- Required resources
- Required permissions
- Links to setup guides

### 4. Multiple Approaches (when applicable)

Use tabbed format for Portal/CLI/SDK:

```markdown
# [Portal](#tab/portal)

Portal instructions...

# [Azure CLI](#tab/cli)

CLI instructions...

# [Python SDK](#tab/python)

SDK instructions...

---
```

### 5. Troubleshooting
Common issues and solutions:
- Error messages with fixes
- Known limitations
- Edge cases

### 6. Related Content
- Other how-to guides
- Reference documentation
- Conceptual explanations

## Writing Rules

- **Get to the point** - Users know what they want
- **Assume knowledge** - Don't explain basic concepts
- **Offer choices** - Show multiple ways to accomplish the task
- **Be practical** - Include real-world considerations

## Do Not Include

- Learning exercises (→ tutorial)
- Complete API documentation (→ reference)
- Theoretical background (→ explanation)
- "Build your first" language (→ tutorial)
