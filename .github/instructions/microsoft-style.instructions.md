---
applyTo: "**/*.md"
---

# Microsoft Writing Style Guidelines

Apply these writing conventions when creating or editing markdown documentation.

## Voice and Tone

- Use **second person** ("you") to address the reader directly
- Use **active voice** over passive voice
- Be **friendly but professional** - conversational, not casual
- Be **concise** - shorter sentences are clearer

**Good**: "You create a deployment by selecting a model."  
**Bad**: "A deployment is created by the user when a model has been selected."

## Word Choices

### Verb Forms

| Use | Avoid |
|-----|-------|
| select | click on, hit, press |
| enter | type, input |
| go to | navigate to |
| open | launch |
| sign in | log in, log on |

### Contractions

Use common contractions for friendlier tone:
- it's, you're, you'll, we're, don't, can't, won't, isn't

### Avoid

- **Jargon**: Explain technical terms on first use
- **Latinisms**: Use "for example" not "e.g.", use "that is" not "i.e."
- **Marketing speak**: Avoid "leverage", "utilize", "cutting-edge"
- **Future promises**: Avoid "will soon", "coming soon", "in a future release"

## Capitalization

- **Sentence case** for headings: "Deploy a model" not "Deploy A Model"
- **Product names**: Match official capitalization (Azure AI Foundry, not Azure AI foundry)
- **UI elements**: Match the interface exactly
- **Buttons**: Use bold - "Select **Create**"

## Lists

- Use **numbered lists** for sequential steps
- Use **bulleted lists** for non-sequential items
- Start each item with a capital letter
- End with periods only if items are complete sentences
- Maintain parallel structure (all start with verbs, or all start with nouns)

## Procedures

- Number steps sequentially (1, 2, 3)
- Start each step with an imperative verb
- One action per step when possible
- Include expected results after significant actions

**Example**:
```markdown
1. Open the Azure portal.
2. Search for **AI Foundry** in the search bar.
3. Select **Azure AI Foundry** from the results.
   
   The Azure AI Foundry overview page appears.
```
