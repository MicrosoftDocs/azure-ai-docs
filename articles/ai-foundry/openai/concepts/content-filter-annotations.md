---
title: Guardrail annotations 
description: Learn about annotations for content filtering in Azure OpenAI, including severity levels and optional models.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 01/15/2025
author: ssalgadodev
ms.author: ssalgado
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Guardrail annotations

Microsoft Foundry Models provide annotations to help you understand the Guardrail (previously content filtering) results for your requests. Annotations can be enabled even for filters and severity levels that have been disabled from blocking content. 

## Standard guardrail annotations 

When annotations are enabled as shown in the code snippets below, the following information is returned via the API for the categories hate and fairness, sexual, violence, and self-harm: 
- risk category (hate, sexual, violence, self_harm) 
- the severity level (safe, low, medium, or high) within each content category 
- filtering status (true or false).

Azure OpenAI in Foundry Models provides content filtering annotations to help you understand the content filtering results for your requests. Annotations can be enabled even for filters and severity levels that have been disabled from blocking content.

## Optional model annotations

Optional models can be set to annotate mode (returns information when content is flagged, but not filtered) or filter mode (returns information when content is flagged and filtered).  

When annotations are enabled as shown in the code snippets below, the following information is returned by the API for each optional model:

|Model| Output|
|--|--|
|User prompt attack|detected (true or false), </br>filtered (true or false)|
|indirect attacks|detected (true or false), </br>filtered (true or false)|
|protected material text|detected (true or false), </br>filtered (true or false)|
|protected material code|detected (true or false), </br>filtered (true or false), </br>Example citation of public GitHub repository where code snippet was found, </br>The license of the repository|
|Personally identifiable information (PII)|detected (true or false)</br>filtered (true or false) </br>redacted (true or false) |
|Groundedness | detected (true or false)</br>filtered (true or false, with details) </br>(Annotate mode only) details:(`completion_end_offset`, `completion_start_offset`) |

When displaying code in your application, we strongly recommend that the application also displays the example citation from the annotations. Compliance with the cited license may also be required for Customer Copyright Commitment coverage.

See the following table for the annotation mode availability in each API version:

|Filter category |2024-10-01-preview|2024-02-01 GA| 2024-04-01-preview | 2023-10-01-preview | 2023-06-01-preview| 2025-01-01-preview |
|--|--|--|--|--|
| Hate | ✅|✅ |✅ |✅ |✅ |✅ |
| Violence | ✅|✅ |✅ |✅ |✅ |✅ |
| Sexual |✅ |✅|✅ |✅ |✅ |✅ |
| Self-harm |✅|✅|✅ |✅ |✅ |✅ |
| Prompt Shield for user prompt attacks|✅|✅|✅ |✅ |✅ |✅ |
|Prompt Shield for indirect attacks|   | | ✅ | | |✅ |
|Protected material text|✅|✅ |✅ |✅ |✅ |✅ |
|Protected material code|✅|✅ |✅ |✅ |✅ |✅ |
|Personally identifiable information (PII)| |  |  |  |  |✅ |
|Profanity blocklist|✅|✅ |✅ |✅ |✅ |✅ |
|Custom blocklist|✅| | ✅ |✅ |✅ |✅ |
|Groundedness<sup>1</sup>|✅| |  | |  |✅ |

<sup>1</sup> Not available in non-streaming scenarios; only available for streaming scenarios. The following regions support Groundedness Detection: Central US, East US, France Central, and Canada East 

## Code examples

The following code snippets show how to view content filter annotations in different programming languages.

# [OpenAI Python 1.x](#tab/python-new)

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

## Output

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
            "URL": " https://github.com/username/repository-name/path/to/file-example.txt", 
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
        "content": "Example model response will be returned ", 
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

# [OpenAI Python 0.28.1](#tab/python)

[!INCLUDE [Deprecation](../includes/deprecation.md)]

```python
# os.getenv() for the endpoint and key assumes that you are using environment variables.

import os
import openai
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai.api_version = "2024-03-01-preview" # API version required to use Annotations
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

response = openai.Completion.create(
    engine="gpt-35-turbo-instruct", # engine = "deployment_name".
    messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Example prompt that leads to a protected code completion that was detected, but not filtered"}]     # Content that is detected at severity level medium or high is filtered, 
    # while content detected at severity level low isn't filtered by the content filters.
)

print(response)

```

## Output

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
            "URL": " https://github.com/username/repository-name/path/to/file-example.txt", 
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
        "content": "Example model response will be returned ", 
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

The following code snippet shows how to retrieve annotations when content was filtered:

```python
# os.getenv() for the endpoint and key assumes that you are using environment variables.

import os
import openai
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai.api_version = "2024-03-01-preview" # API version required to use  Annotations
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

try:
    response = openai.Completion.create(
        prompt="<PROMPT>",
        engine="<MODEL_DEPLOYMENT_NAME>",
    )
    print(response)

except openai.error.InvalidRequestError as e:
    if e.error.code == "content_filter" and e.error.innererror:
        content_filter_results = e.error.innererror.content_filter_results
        # print the formatted JSON
        print(content_filter_results)

        # or access the individual categories and details
        for category, details in content_filter_results.items():
            print(f"{category}:\n filtered={details['filtered']}\n severity={details['severity']}")

```

# [JavaScript](#tab/javascrit)

[Azure OpenAI JavaScript SDK source code & samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai)

```javascript

import { OpenAIClient, AzureKeyCredential } from "@azure/openai";

// Load the .env file if it exists
import * as dotenv from "dotenv";
dotenv.config();

// You will need to set these environment variables or edit the following values
const endpoint = process.env["ENDPOINT"] || "Your endpoint";
const azureApiKey = process.env["AZURE_API_KEY"] || "Your API key";

const messages = [
  { role: "system", content: "You are a helpful assistant. You will talk like a pirate." },
  { role: "user", content: "Can you help me?" },
  { role: "assistant", content: "Arrrr! Of course, me hearty! What can I do for ye?" },
  { role: "user", content: "What's the best way to train a parrot?" },
];

export async function main() {
  console.log("== Get completions Sample ==");

  const client = new OpenAIClient(endpoint, new AzureKeyCredential(azureApiKey));
  const deploymentId = "gpt-35-turbo"; //This needs to correspond to the name you chose when you deployed the model. 
  const events = await client.listChatCompletions(deploymentId, messages, { maxTokens: 128 });

  for await (const event of events) {
    for (const choice of event.choices) {
      console.log(choice.message);
      if (!choice.contentFilterResults) {
        console.log("No content filter is found");
        return;
      }
      if (choice.contentFilterResults.error) {
        console.log(
          `Content filter ran into the error ${choice.contentFilterResults.error.code}: ${choice.contentFilterResults.error.message}`
        );
      } else {
        const { hate, sexual, selfHarm, violence } = choice.contentFilterResults;
        console.log(
          `Hate category is filtered: ${hate?.filtered} with ${hate?.severity} severity`
        );
        console.log(
          `Sexual category is filtered: ${sexual?.filtered} with ${sexual?.severity} severity`
        );
        console.log(
          `Self-harm category is filtered: ${selfHarm?.filtered} with ${selfHarm?.severity} severity`
        );
        console.log(
          `Violence category is filtered: ${violence?.filtered} with ${violence?.severity} severity`
        );
      }
    }
  }
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

# [PowerShell](#tab/powershell)

```powershell-interactive
# Env: for the endpoint and key assumes that you are using environment variables.
$openai = @{
    api_key     = $Env:AZURE_OPENAI_API_KEY
    api_base    = $Env:AZURE_OPENAI_ENDPOINT # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_version = '2024-03-01-preview' # this may change in the future
    name        = 'YOUR-DEPLOYMENT-NAME-HERE' #This will correspond to the custom name you chose for your deployment when you deployed a model.
}

$prompt = 'Example prompt where a severity level of low is detected'
    # Content that is detected at severity level medium or high is filtered, 
    # while content detected at severity level low isn't filtered by the content filters.

$headers = [ordered]@{
    'api-key' = $openai.api_key
}

$body = [ordered]@{
    prompt    = $prompt
    model      = $openai.name
} | ConvertTo-Json

# Send a completion call to generate an answer
$url = "$($openai.api_base)/openai/deployments/$($openai.name)/completions?api-version=$($openai.api_version)"

$response = Invoke-RestMethod -Uri $url -Headers $headers -Body $body -Method Post -ContentType 'application/json'
return $response.prompt_filter_results.content_filter_results | format-list
```

The `$response` object contains a property named `prompt_filter_results` that contains annotations
about the filter results. If you prefer JSON to a .NET object, pipe the output to `ConvertTo-JSON`
instead of `Format-List`.

```output
hate      : @{filtered=False; severity=safe}
self_harm : @{filtered=False; severity=safe}
sexual    : @{filtered=False; severity=safe}
violence  : @{filtered=False; severity=safe}
```

---

For details on the inference REST API endpoints for Azure OpenAI and how to create Chat and Completions, follow [Azure OpenAI REST API reference guidance](../reference.md). Annotations are returned for all scenarios when using any preview API version starting from `2023-06-01-preview`, as well as the GA API version `2024-02-01`.


<!--
### Example scenario: An input prompt containing content that is classified at a filtered category and severity level is sent to the completions API

```json
{
    "error": {
        "message": "The response was filtered due to the prompt triggering Azure Content management policy. 
                   Please modify your prompt and retry. To learn more about our content filtering policies
                   please read our documentation: https://go.microsoft.com/fwlink/?linkid=21298766",
        "type": null,
        "param": "prompt",
        "code": "content_filter",
        "status": 400,
        "innererror": {
            "code": "ResponsibleAIPolicyViolation",
            "content_filter_results": {
                "hate": {
                    "filtered": true,
                    "severity": "high"
                },
                "self-harm": {
                    "filtered": true,
                    "severity": "high"
                },
                "sexual": {
                    "filtered": false,
                    "severity": "safe"
                },
                "violence": {
                    "filtered":true,
                    "severity": "medium"
                }
            }
        }
    }
}
```
-->
