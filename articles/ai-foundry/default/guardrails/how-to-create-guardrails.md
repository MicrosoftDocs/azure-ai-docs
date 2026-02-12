---
title: 'How-to configure guardrails and controls in Microsoft Foundry'
titleSuffix: Microsoft Foundry
description: How-to guide for creating, configuring, and managing guardrails and controls in Microsoft Foundry, including UI instructions and API configuration.
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 10/31/2025
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.custom: azure-ai-guardrails
# customer intent: As a developer, I want a comprehensive guide to guardrails and controls in Microsoft Foundry so that I can implement complete safety measures for my models and agents.
---

# How to configure guardrails and controls in Microsoft Foundry

This comprehensive guide walks you through every aspect of creating, configuring, and managing guardrails and controls in Microsoft Foundry. From basic setup to advanced features, this article covers both UI instructions and API configuration methods.

## Prerequisites 

- An Azure account. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An [Azure AI resource](https://ms.portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/AIServices). 


## Create a guardrail in Foundry

1. Go to [Foundry](https://ai.azure.com) and navigate to your project.
2. Select **Build** in the top right menu.
3. Select the **Guardrails** page from the left navigation.
4. Select **Create Guardrail** in the top right.

## Add controls to a guardrail

Default controls are displayed in the right pane when you create a new guardrail.

1. **Select a risk** from the dropdown menu.
2. **Choose intervention points and actions**: Recommended intervention points and actions for that risk is shown. Select one or many intervention points and one action to configure your control.

   > [!NOTE]
   > Some intervention points will not be available for a risk if that is inapplicable at that intervention point. For example, by definition, user input attacks are malicious content added to the user input. So, that risk can be scanned only at that intervention point. 

3. Select **Add control**. The control is added to the table on the right.

## Delete controls from a guardrail

To delete a control:

1. Select the control you want to remove.
2. Select **Delete**.

> [!NOTE]
> Some controls can only be deleted by Managed Customers who are approved for modified content filtering. Learn more about [modified content filtering](../../foundry-models/concepts/content-filter.md).

## Edit controls in a guardrail

There are two ways to edit a control: deleting it and adding a new one, or overriding an existing control. The latter is the only way to edit a control that cannot be deleted, such as Violence, Hate, Sexual, and Self-harm controls on user inputs and outputs.

To edit a control by overriding it:

1. Select the same risk of the control that needs to be edited.
2. Change the configuration of the control or the intervention points and action as desired.
3. Select **Add control**.
4. A pop-up asks for confirmation to override the existing control. Select **Confirm**.

## Assign a guardrail to agents and models

After adding, editing, and/or deleting controls as desired:

1. Select **Next** to proceed to Step 2: assigning a guardrail to agents and/or models.
2. Select **Add agents** and/or **Add models** to view a list of agents and models in this project.
3. Select models or agents. Previously assigned agents and models can also be deselected to remove this guardrail and re-assign the Microsoft Default.
4. Select **Save** to confirm.

## Review and name guardrail

1. Select **Next** to proceed to Step 3: Review.
2. Review the controls added to this guardrail and the models and/or agent it's assigned to.
3. Name the guardrail, or leave the automatically assigned name.
4. Select **Create** to create this new custom guardrail and assign it to the selected models and agents.

## Edit an existing guardrail

1. Select **Build** in the top right menu.
2. Select the **Guardrails** page from the left navigation.
3. Find the guardrail in the list of guardrails. Select its name directly or click on its row and select **Edit** in the right pane that pops up.

   > [!NOTE]
   > Microsoft Default guardrails, such as Default.V2, cannot be edited.

4. Follow the same instructions as in [Create a guardrail](#create-a-guardrail-in-foundry) to edit, add, or remove controls; assign or re-assign agents and/or models; and rename the guardrail, as needed.

## Assign a guardrail

There are two paths to assigning a guardrail to a model or agent:

### Option 1: Edit the guardrail

1. Select **Build** in the top right menu.
2. Select the **Guardrails** page from the left navigation.
3. Find the guardrail in the list of guardrails. Click on its name directly or click on its row and select **Edit** in the right pane that pops up.
4. Select **Next** on Step 1: Add Controls to skip forward to the assignment step.
5. Select **Add agents** or **Add models** and select and deselect models and/or agents as needed to update the guardrail's assignment.

### Option 2: Edit the model or agent

1. Select **Build** in the top right menu.
2. Select **Agents** or **Models** in the left navigation.
3. Select the individual agent or model that needs to update.
4. A section for **Guardrails** appears in the left panel of the Agent Playground or Chat Playground.
5. Select **Manage** at the bottom of the Guardrails section.
6. Select **Assign a new guardrail**.
7. Browse guardrails available in this project.
8. Select the desired guardrail from the list on the left of the pop-up.
9. Select **Assign** to update the agent or model's guardrail assignment. The new guardrail takes effect immediately.

## Delete a guardrail

### To delete a guardrail with no models or agents assigned

1. Select **Build** in the top right menu.
2. Select the **Guardrails** page from the left navigation.
3. Find the guardrail in the list of guardrails and select on its row.
4. A panel appears on the right. Select **Delete** at the top of the panel.

### To delete a guardrail with assigned models or agents

1. Reassign the models and/or agents to a different guardrail, or remove them from this guardrail to reassign them to the Microsoft Default Guardrails.
2. Follow the instructions to [delete a guardrail with no models or agents assigned](#to-delete-a-guardrail-with-no-models-or-agents-assigned).

## Test guardrails

To test the behavior of a particular guardrail:

1. Select **Build** in the top right menu.
2. Select the **Guardrails** page from the left navigation.
3. Find the guardrail in the list of guardrails and select on its row.
4. A panel appears on the right. Select **Try in Playground** at the top of the panel.

   > [!NOTE]
   > If that button does not appear, assign this guardrail to a model or agent first. This will immediately change the safety & security behavior of the model or agent, so make sure to use one not in production that can be experimented with.

5. In the playground, send queries to the model or agent.
6. When a control that has "Annotate and block" as its action is triggered, a message appears in the chat with details on which risk was detected and at which intervention point.

## API instructions

### Creating a Guardrail in Foundry 
A guardrail is represented as a RaiPolicy in the Resource Manager. Use the [RAI Policies page](/rest/api/aiservices/accountmanagement/rai-policies/create-or-update) to create or update a new guardrail through code. 


### Assigning a Guardrail to a Model 

Assign an existing guardrail to a model via the [model deployment properties](/rest/api/aiservices/accountmanagement/deployments/create-or-update).


## Work with annotations

Foundry provides annotations to help you understand the guardrail results for your requests. Annotations can be enabled even for filters and severity levels that have been disabled from blocking content.

### Standard guardrail annotations

When annotations are enabled, the following information is returned via the API for the categories hate, sexual, violence, and self-harm:

- **Risk category** (hate, sexual, violence, self_harm)
- **Severity level** (safe, low, medium, or high) within each content category
- **Filtering status** (true or false)

### Optional model annotations

Optional models can be set to annotate mode (returns information when content is flagged, but not filtered) or filter mode (returns information when content is flagged and filtered).

| Model | Output |
|-------|--------|
| User prompt attack | - detected (true or false)<br>- filtered (true or false) |
| Indirect attacks | - detected (true or false)<br>- filtered (true or false) |
| Protected material text | - detected (true or false)<br>- filtered (true or false) |
| Protected material code | - detected (true or false)<br>- filtered (true or false)<br>- Example citation of public GitHub repository where code snippet was found<br>- The license of the repository |
| Personally identifiable information (PII) | - detected (true or false)<br>- filtered (true or false)<br>- redacted (true or false) |
| Groundedness | - detected (true or false)<br>- filtered (true or false, with details)<br>- (Annotate mode only) details:(completion_end_offset, completion_start_offset) |


> [!IMPORTANT]
> When displaying code in your application, we strongly recommend that the application also displays the example citation from the annotations. Compliance with the cited license may also be required for Customer Copyright Commitment coverage.

### API version compatibility

The following table shows annotation mode availability in each API version:

| Filter category | 2024-10-01-preview | 2024-02-01 GA | 2024-04-01-preview | 2023-10-01-preview | 2023-06-01-preview | 2025-01-01-preview |
|----------------|-------------------|---------------|-------------------|-------------------|-------------------|-------------------|
| Hate | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Violence | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sexual | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Self-harm | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt Shield for user prompt attacks | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt Shield for indirect attacks | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Protected material text | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Protected material code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Personally identifiable information (PII) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Profanity blocklist | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Custom blocklist | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Groundedness¹ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |


¹ Not available in non-streaming scenarios; only available for streaming scenarios. 

## Code examples

The following code snippets show how to view guardrail annotations in different programming languages.

# [Python](#tab/python)

```python
# os.getenv() for the endpoint and key assumes that you are using environment variables.

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-03-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
)

response = client.completions.create(
    model="gpt-35-turbo-instruct", # model = "deployment_name".
    prompt="{Example prompt where a severity level of low is detected}" 
    # Content that is detected at severity level medium or high is filtered, 
    # while content detected at severity level low isn't filtered by the content filters.
)

print(response.model_dump_json(indent=2))
```

# [JavaScript](#tab/javascript)

```javascript
const { OpenAI } = require('openai');

const client = new OpenAI({
  apiKey: process.env.AZURE_OPENAI_API_KEY,
  baseURL: `${process.env.AZURE_OPENAI_ENDPOINT}/openai/deployments/gpt-35-turbo-instruct`,
  defaultQuery: { 'api-version': '2024-03-01-preview' },
  defaultHeaders: {
    'api-key': process.env.AZURE_OPENAI_API_KEY,
  },
});

async function main() {
  const completion = await client.completions.create({
    model: '',
    prompt: 'Example prompt where a severity level of low is detected',
  });

  console.log(JSON.stringify(completion, null, 2));
}

main();
```

---

### Example output

```json
{
  "choices": [
    {
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "protected_material_code": {
          "citation": {
            "URL": "https://github.com/username/repository-name/path/to/file-example.txt",
            "license": "EXAMPLE-LICENSE"
          },
          "detected": true,
          "filtered": false
        },
        "protected_material_text": {
          "detected": false,
          "filtered": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      },
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "Example model response will be returned",
        "role": "assistant"
      }
    }
  ],
  "created": 1699386280,
  "id": "chatcmpl-8IMI4HzcmcK6I77vpOJCPt0Vcf8zJ",
  "model": "gpt-35-turbo-instruct",
  "object": "text.completion",
  "usage": {
    "completion_tokens": 40,
    "prompt_tokens": 11,
    "total_tokens": 417
  },
  "prompt_filter_results": [
    {
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "detected": false,
          "filtered": false
        },
        "profanity": {
          "detected": false,
          "filtered": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      },
      "prompt_index": 0
    }
  ]
}
```

For details on the inference REST API endpoints for Azure OpenAI and how to create Chat and Completions, follow [Azure OpenAI REST API reference guidance](../../openai/reference.md). Annotations are returned for all scenarios when using any preview API version starting from 2023-06-01-preview, as well as the GA API version 2024-02-01.

## Document embedding in prompts

Guardrails perform better when they can differentiate between the various elements of your prompt, like system input, user input, and the AI assistant's output. For enhanced detection capabilities, prompts should be formatted according to the following recommended methods.

### Default behavior in Chat Completions API

The Chat Completions API is structured by definition. Inputs consist of a list of messages, each with an assigned role.

The safety system parses this structured format and applies the following behavior:

On the latest "user" content, the following categories of risks are detected:
- Hate
- Sexual
- Violence
- Self-Harm
- Prompt shields (optional)

**Example message array:**

```json
[
  {"role": "system", "content": "Provide some context and/or instructions to the model."},
  {"role": "user", "content": "Example question goes here."},
  {"role": "assistant", "content": "Example answer goes here."},
  {"role": "user", "content": "First question/message for the model to actually respond to."}
]
```

### Embedding documents in your prompt

In addition to detection on last user content, guardrails also support the detection of specific risks inside context documents via Prompt Shields – Indirect Prompt Attack Detection and Groundedness detection. You should identify the parts of the input that are a document (for example, retrieved website, email, etc.) with the following document delimiter:

```
""" <documents> *insert your document content here* </documents> """
```

When you do this, the following options are available for detection on tagged documents:
- Indirect attacks (optional)
- Groundedness detection

**Example chat completion messages array:**

```json
[
  {"role": "system", "content": "Provide some context and/or instructions to the model."},
  {"role": "user", "content": "First question/message for the model to actually respond to, including document context. \"\"\" <documents>\n*insert your document content here*\n</documents> \"\"\""}
]
```

### JSON escaping

When you tag unvetted documents for detection, the document content should be JSON-escaped to ensure successful parsing by the Azure AI safety system.

For example, see the following email body:

```
Hello José,

I hope this email finds you well today.
```

With JSON escaping, it would read:

```
Hello Jos\u00E9,\nI hope this email finds you well today.
```

The escaped text in a chat completion context would read:

```json
[
  {"role": "system", "content": "Provide some context and/or instructions to the model, including document context. \"\"\" <documents>\n Hello Jos\\u00E9,\\nI hope this email finds you well today. \n</documents> \"\"\""},
  {"role": "user", "content": "First question/message for the model to respond to"}
]
```

## Specify guardrail configuration at request time

In addition to the model deployment-level guardrail, you can specify your custom guardrail at request time for each API call using a request header.

```bash
curl --request POST \
    --url 'URL' \
    --header 'Content-Type: application/json' \
    --header 'api-key: API_KEY' \
    --header 'x-policy-id: CUSTOM_CONTENT_FILTER_NAME' \
    --data '{
        "messages": [
            {
                "role": "system",
                "content": "You are a creative assistant."
            },
            {
                "role": "user",
                "content": "Write a poem about the beauty of nature."
            }
        ]
    }'
```

The request-level guardrails configuration will override the deployment-level configuration for the specific API call.

> [!IMPORTANT]
> Guardrails specification at request time is not available for image input (chat with images) scenarios. In those cases the default guardrail is used.

If a configuration is specified that does not exist, the following error message is returned:

```json
{
    "error": {
        "code": "InvalidContentFilterPolicy",
        "message": "Your request contains invalid content filter policy. Please provide a valid policy."
    }
}
```

## Best practices

We recommend informing your guardrails configuration decisions through an iterative identification process (for example, red team testing, stress-testing, and analysis) and measurement process to address the potential harms that are relevant for a specific model, application, and deployment scenario. After you implement mitigations such as guardrails, repeat measurement to test effectiveness.

For recommendations and best practices for Responsible AI, grounded in the Microsoft Responsible AI Standard, see the [Responsible AI Overview](../../responsible-ai/openai/overview.md).


## Next steps

- [Understand content filtering in Azure OpenAI](../../openai/concepts/content-filter.md)
- [Learn about intervention points and controls](intervention-points.md)
- [Configure content filters for Azure OpenAI](../../openai/how-to/content-filters.md)

