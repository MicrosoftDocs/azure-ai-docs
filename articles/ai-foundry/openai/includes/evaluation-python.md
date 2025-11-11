---
title: 'How to use Azure OpenAI in Microsoft Foundry Models evaluation - Python
titleSuffix: Azure OpenAI
description:  Learn how to use evaluations with Azure OpenAI -Python
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

```python
import asyncio
import json
import requests

async def create_eval():
    response = await asyncio.to_thread(
        requests.post,
        f'{API_ENDPOINT}/openai/v1/evals',
        headers={
            'api-key': API_KEY,
            'aoai-evals': 'preview'
        },
        json={
            'name': 'My Evaluation',
            'data_source_config': {
                'type': 'custom',
                'item_schema': {
                'type': 'object',
                'properties': {
                    'question': {
                    'type': 'string'
                    },
                    'subject': {
                    'type': 'string'
                    },
                    'A': {
                    'type': 'string'
                    },
                    'B': {
                    'type': 'string'
                    },
                    'C': {
                    'type': 'string'
                    },
                    'D': {
                    'type': 'string'
                    },
                    'answer': {
                    'type': 'string'
                    },
                    'completion': {
                    'type': 'string'
                    }
                }
                }
            },
            'testing_criteria': [
                {
                'type': 'string_check',
                'reference': '{{item.completion}}',
                'input': '{{item.answer}}',
                'operation': 'eq',
                'name': 'string check'
                }
            ]
        })

    print(response.status_code)
    print(json.dumps(response.json(), indent=2))

```

### Create a Single Run

Azure OpenAI Evaluation allows creating multiple runs under an evaluation job. If you would like to add a single evaluation run to an existing evaluation, you can specify the `eval_id` of the existing evaluation: 

```python
import asyncio
import requests
import json


response = await asyncio.to_thread(
    requests.post,
    f'{API_ENDPOINT}/openai/v1/evals/{eval_id}/runs',
    headers={
        'api-key': API_KEY,
        'aoai-evals': 'preview'
    },
    json={
        "name": "No sample",
        "metadata": {
            "sample_generation": "off",
            "file_format": "jsonl"
        },
        "data_source": {
            "type": "jsonl",
            "source": {
            "type": "file_id",
            "id": "file-75099d8d4b5b4abca7cc91e9eca7bba1"
            }
        }
    })

print(response.status_code)
print(json.dumps(response.json(), indent=2))
```

### Update Existing Evaluation

```python
import asyncio
import requests
import json

async def update_eval():
    response = await asyncio.to_thread(
        requests.post,
        f'{API_ENDPOINT}/openai/v1/evals/{eval_id}',
        headers={
            'api-key': API_KEY,
            'aoai-evals': 'preview'
        },
        json={
            "name": "Updated Eval Name",
            "metadata": {
                "sample_generation": "off",
                "file_format": "jsonl",
                "updated": "metadata"
            }
        })

    print(response.status_code)
    print(json.dumps(response.json(), indent=2))
```

## Evaluation Results

Once evaluation is complete, you can fetch the evaluation results for the evaluation job by specifying the `eval_id`.

```python
import asyncio
import requests

async def get_eval():
    response = await asyncio.to_thread(
        requests.get,
        f'{API_ENDPOINT}/openai/v1/evals/{eval_id}',
        headers={
            'api-key': API_KEY,
            'aoai-evals': 'preview'
        })

    print(response.status_code)
    print(response.json())
```

### Single Evaluation Run Result

Just like how you can create a single evaluation run under an existing evaluation job, you can also retrieve the result for a single run:

```python
import asyncio
import requests
import json

async def get_eval_run():
    response = await asyncio.to_thread(
        requests.get,
        f'{API_ENDPOINT}/openai/v1/evals/eval_67fd95c864f08190817f0dff5f42f49e/runs/evalrun_67fe987a6c548190ba6f33f7cd89343d',
        headers={
            'api-key': API_KEY,
            'aoai-evals': 'preview'
        })

    print(response.status_code)
    print(json.dumps(response.json(), indent=2))
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

```python
import asyncio
import requests
import json

async def get_eval_list():
    response = await asyncio.to_thread(
        requests.get,
        f'{API_ENDPOINT}/openai/v1/evals',
        headers={
            'api-key': API_KEY,
            'aoai-evals': 'preview'
        })

    print(response.status_code)
    print(json.dumps(response.json(), indent=2))
```

### Output Details for a Run

You can view the individual outputs generated from the graders for a single evaluation run: 

```python
import asyncio
import requests
import json

async def get_eval_output_item_list():
    response = await asyncio.to_thread(
        requests.get,
        f'{API_ENDPOINT}/openai/v1/evals/eval_67fd95c864f08190817f0dff5f42f49e/runs/evalrun_67fe987a6c548190ba6f33f7cd89343d/output_items',
        headers={
            'api-key': API_KEY,
            'aoai-evals': 'preview'
        })

    print(response.status_code)
    print(json.dumps(response.json(), indent=2))

```

If you have a particular output result you would like to see, you can specify the output item ID: 

```python
import asyncio
import requests
import json

async def get_eval_output_item():
    response = await asyncio.to_thread(
        requests.get,
        f'{API_ENDPOINT}/openai/v1/evals/eval_67fd95c864f08190817f0dff5f42f49e/runs/evalrun_67fe987a6c548190ba6f33f7cd89343d/output_items/outputitem_67fe988369308190b50d805120945deb',
        headers={'api-key': API_KEY})

    print(response.status_code)
    print(json.dumps(response.json(), indent=2))

```