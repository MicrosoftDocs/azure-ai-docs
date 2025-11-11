---
title: 'How to use Azure OpenAI in Microsoft Foundry Models evaluation - REST
titleSuffix: Azure OpenAI
description:  Learn how to use evaluations with Azure OpenAI - REST
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 07/28/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
---

## Create evaluation

You can create an evaluation by specifying a data source config and the evaluation testing criteria. Below is one of many ways you can define a data source config. You can also specify one or many testing criteria.

```curl
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/evals" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "aoai-evals: preview" \
  -d '{
    "name": "Math Quiz",
    "data_source_config": {
      "type": "custom",
      "include_sample_schema": true,
      "item_schema": {
        "type": "object",
        "properties": {
          "question": { "type": "string" },
          "A": { "type": "string" },
          "B": { "type": "string" },
          "C": { "type": "string" },
          "D": { "type": "string" },
          "answer": { "type": "string" }
        }
      }
    },
    "testing_criteria": [
      {
        "type": "string_check",
        "reference": "{{item.answer}}",
        "input": "{{sample.output_text}}",
        "operation": "eq",
        "name": "string check"
      }
    ]
  }'
```

### Create a Single Run

Azure OpenAI Evaluation allows creating multiple runs under an evaluation job. 
You can add new evaluation runs to the evaluation job you had created in the previous step, by specifying `eval-id`.

```curl
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/evals/{eval-id}/runs" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
  -H "aoai-evals: preview" \
```

### Update Existing Evaluation

```curl
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/evals/{eval-id} \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
  -H "aoai-evals: preview" \
```

## Evaluation Results

Once evaluation is complete, you can fetch the evaluation results for the evaluation job by specifying the `eval_id`.

```curl
curl -X GET "$AZURE_OPENAI_ENDPOINT/openai/v1/evals/{eval-id}" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
  -H "aoai-evals: preview" \
```

### Single Evaluation Run Result

Just like how you can create a single evaluation run under an existing evaluation job, you can also retrieve the result for a single run:

```curl
curl -X GET "$AZURE_OPENAI_ENDPOINT/openai/v1/evals/{eval-id}/runs/{run-id}" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
  -H "aoai-evals: preview" \
```

In addition to the parameters in the examples above, you can optionally add these parameters for more specific drill-downs into the evaluation results: 

| Name      | In    | Required | Type    | Description |
|-----------|-------|----------|---------|-------------|
| endpoint  | path  | Yes      | string  | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id   | path  | Yes      | string  | The ID of the evaluation to retrieve runs for. |
| run-id    | path  | Yes      | string  | The ID of the run to retrieve output items for. |
| after     | query | No       | string  | Identifier for the last output item from the previous pagination request. |
| limit     | query | No       | integer | Number of output items to retrieve. |
| status    | query | No       | string  | Possible values: fail, pass. Filter output items by status. Use fail to filter by failed output items or pass to filter by passed output items. |
| order     | query | No       | string  | Possible values: asc, desc. Sort order for output items by timestamp. Use asc for ascending order or desc for descending order. Defaults to asc. |
| api-version | query | Yes    | string  | The requested API version. |

### Evaluation List

To see the list of all evaluation jobs that were created:

```curl
curl -X GET "$AZURE_OPENAI_ENDPOINT/openai/v1/evals/{eval-id}/runs" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
  -H "aoai-evals: preview" \
```

### Output Details for a Run

You can view the individual outputs generated from the graders for a single evaluation run: 

```curl
curl -X GET "$AZURE_OPENAI_ENDPOINT/openai/v1/evals/{eval-id}/runs/{run-id}/output_items" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
  -H "aoai-evals: preview" \
```

If you have a particular output result you would like to see, you can specify the output item ID: 

```curl
curl -X GET "$AZURE_OPENAI_ENDPOINT/openai/v1/evals/{eval-id}/runs/{run-id}/output_items/{output-item-id}" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
  -H "aoai-evals: preview" \
```