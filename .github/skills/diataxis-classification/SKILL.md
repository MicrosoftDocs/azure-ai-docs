---
name: diataxis-classification
description: Classify documentation content into the correct Diataxis type (Tutorial, How-to, Reference, Explanation). Use this skill when planning documentation to ensure type purity and proper structure.
---

# Diataxis Classification Skill

This skill helps classify documentation content into the correct Diataxis documentation type.

## When to Use

- When planning new documentation
- When reviewing existing content for type purity
- When content seems to mix multiple types
- When deciding how to split mixed content

## The Four Diataxis Types

### Tutorial

**User Intent**: Learn by doing (hands-on practice to acquire competence)

**Characteristics**:
- Learning-oriented
- Step-by-step journey
- One canonical path
- Minimal explanations
- Beginner audience
- Includes verification steps
- Has cleanup section

**Analogy**: Cooking class

**Title Pattern**: "Tutorial: [Action verb] [noun]" or "Build your first..."

### How-to Guide

**User Intent**: Accomplish a specific task (solve a problem or achieve a goal)

**Characteristics**:
- Task-oriented
- Assumes knowledge
- Multiple approaches (portal/CLI/SDK)
- Troubleshooting section
- Experienced audience
- Gets to the point quickly

**Analogy**: Recipe

**Title Pattern**: "How to [verb] [noun]" or "[Verb] [noun]"

### Reference

**User Intent**: Look up technical details (specifications, parameters, return values)

**Characteristics**:
- Information-oriented
- Complete specifications
- Tables for scanability
- All parameters documented
- All errors documented
- Dry, neutral tone

**Analogy**: Ingredient list

**Title Pattern**: "[API/Class/Command] reference"

### Explanation

**User Intent**: Understand concepts (grasp why/how something works)

**Characteristics**:
- Understanding-oriented
- Answers "why" questions
- Discusses trade-offs
- Uses analogies
- Includes conceptual diagrams
- No step-by-step instructions

**Analogy**: Food science

**Title Pattern**: "Understanding [concept]" or "[Concept] overview"

## Classification Matrix

Use these questions to classify content:

| Question | Tutorial | How-to | Reference | Explanation |
|----------|----------|--------|-----------|-------------|
| User wants to... | Learn by doing | Solve problem | Look up facts | Understand |
| Content focuses on... | Education | Tasks | Information | Knowledge |
| Form | Lesson | Steps | Dry description | Discussion |
| Tone | Encouraging | Direct | Neutral | Thoughtful |

## Classification Workflow

### Step 1: Identify Primary User Intent

Ask: "What is the user trying to accomplish?"

- **Learn by doing** → Tutorial
- **Accomplish a specific task** → How-to
- **Look up technical details** → Reference
- **Understand concepts** → Explanation

### Step 2: Check Content Characteristics

Does the content:
- Have numbered steps? → Tutorial or How-to
- List all parameters/options? → Reference
- Explain "why" without "how"? → Explanation

### Step 3: Verify Type Purity

**CRITICAL**: Content must be ONE type only.

Mixed content indicators:
- Tutorial that lists all API parameters → Split to Tutorial + Reference
- How-to that teaches fundamentals → Split to Tutorial + How-to
- Reference that explains design decisions → Split to Reference + Explanation

## Output Format

When classifying content, provide:

```markdown
## Classification Result

**Recommended Type**: [Tutorial | How-to | Reference | Explanation]

**Confidence Level**: [High 90%+ | Medium 70-89% | Low <70%]

**Justification**:
- **User need**: [What the user is trying to accomplish]
- **Content characteristics**: [Why this type is the best fit]
- **Key indicator**: [The primary signal for this classification]

**Alternative Consideration** (if confidence < 90%):
[Alternative type and why it was ruled out]

**Split Recommendation** (if content mixes types):
- **[Type 1]**: [What content goes here]
- **[Type 2]**: [What content goes here]

**Suggested Structure**:
[Key sections for the classified type]
```

## Common Classification Mistakes

### Mistake 1: Tutorial + Reference Mix

**Symptom**: Tutorial includes exhaustive parameter lists

**Fix**: Link to reference from tutorial, don't duplicate

### Mistake 2: How-to Teaching Fundamentals

**Symptom**: How-to explains basic concepts before the task

**Fix**: Create separate tutorial for beginners, link from how-to prerequisites

### Mistake 3: Reference with "Why" Content

**Symptom**: Reference explains design decisions

**Fix**: Move conceptual content to explanation article

### Mistake 4: Explanation with Steps

**Symptom**: Explanation includes "do this, then that" instructions

**Fix**: Move procedural content to how-to or tutorial
