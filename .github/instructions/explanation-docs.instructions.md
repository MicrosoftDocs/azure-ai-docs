---
applyTo: "**/concepts/**/*.md,**/overview/**/*.md"
---

# Explanation Documentation Guidelines

Apply these conventions when creating or editing conceptual/explanation documentation.

## Explanation Definition

Explanation documentation is **understanding-oriented** content that helps readers grasp concepts and make informed decisions. Think of it as food science.

## Required Structure

### 1. Title
Format: "Understanding [concept]" or "[Concept] overview"

Examples:
- "Understanding model deployments"
- "Azure AI Foundry architecture overview"
- "How AI agents work"

### 2. Introduction
- What this concept is
- Why it matters
- When you'd use it

### 3. Conceptual Content

Use these elements:

**Analogies**: Relate to familiar concepts
```markdown
Think of a deployment like a restaurant kitchen. The model is the recipe, 
the deployment is the kitchen where it's prepared, and the endpoint is 
the window where customers order.
```

**Diagrams**: Visual representations of architecture/flow

**Comparisons**: When to use one approach vs another

| Approach | Best for | Trade-offs |
|----------|----------|------------|
| Real-time | Low latency | Higher cost |
| Batch | Large volumes | Higher latency |

**Trade-offs**: Honest discussion of pros/cons

### 4. Mental Models
Help readers build intuition:
- Core principles
- Rules of thumb
- Common patterns

### 5. Related Content
- Tutorials to try the concept
- How-to guides for specific tasks
- Reference documentation

## Writing Rules

- **Answer "why"** - Focus on understanding, not procedure
- **Use analogies** - Connect to familiar concepts
- **Discuss trade-offs** - Be honest about limitations
- **Build mental models** - Help readers develop intuition

## Do Not Include

- Step-by-step procedures (→ tutorial, how-to)
- Complete API specifications (→ reference)
- "Do this, then that" instructions (→ tutorial, how-to)
- Code that needs to be run (→ tutorial, how-to)
