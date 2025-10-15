---
title: Custom Evaluators
titleSuffix: Azure AI Foundry
description: Learn how to create custom evaluators for your AI applications using code-based or prompt-based approaches.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: mithigpe
ms.date: 10/16/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# Custom evaluators

To start evaluating your application's generations, built-in evaluators are great out of the box. To cater to your evaluation needs, you can build your own code-based or prompt-based evaluator.

## Code-based evaluators

You don't need a large language model for certain evaluation metrics. Code-based evaluators can give you the flexibility to define metrics based on functions or callable classes. You can build your own code-based evaluator, for example, by creating a simple Python class that calculates the length of an answer in `answer_length.py` under directory `answer_len/`, as in the following example.

### Code-based evaluator example: Answer length

```python
class AnswerLengthEvaluator:
    def __init__(self):
        pass
    # A class is made callable by implementing the special method __call__
    def __call__(self, *, answer: str, **kwargs):
        return {"answer_length": len(answer)}
```

Run the evaluator on a row of data by importing a callable class:

```python
from answer_len.answer_length import AnswerLengthEvaluator

answer_length_evaluator = AnswerLengthEvaluator()
answer_length = answer_length_evaluator(answer="What is the speed of light?")
```

### Code-based evaluator output: Answer length

```python
{"answer_length":27}
```

## Prompt-based evaluators

To build your own prompt-based large language model evaluator or AI-assisted annotator, you can create a custom evaluator based on a *Prompty* file.

Prompty is a file with the `.prompty` extension for developing prompt template. The Prompty asset is a markdown file with a modified front matter. The front matter is in YAML format. It contains metadata fields that define model configuration and expected inputs of the Prompty.

To measure friendliness of a response, you can create a custom evaluator `FriendlinessEvaluator`:

### Prompt-based evaluator example: Friendliness evaluator

First, create a `friendliness.prompty` file that defines the friendliness metric and its grading rubric:

```md
---
name: Friendliness Evaluator
description: Friendliness Evaluator to measure warmth and approachability of answers.
model:
  api: chat
  configuration:
    type: azure_openai
    azure_endpoint: ${env:AZURE_OPENAI_ENDPOINT}
    azure_deployment: gpt-4o-mini
  parameters:
    model:
    temperature: 0.1
inputs:
  response:
    type: string
outputs:
  score:
    type: int
  explanation:
    type: string
---

system:
Friendliness assesses the warmth and approachability of the answer. Rate the friendliness of the response between one to five stars using the following scale:

One star: the answer is unfriendly or hostile

Two stars: the answer is mostly unfriendly

Three stars: the answer is neutral

Four stars: the answer is mostly friendly

Five stars: the answer is very friendly

Please assign a rating between 1 and 5 based on the tone and demeanor of the response.

**Example 1**
generated_query: I just don't feel like helping you! Your questions are getting very annoying.
output:
{"score": 1, "reason": "The response is not warm and is resisting to be providing helpful information."}
**Example 2**
generated_query: I'm sorry this watch is not working for you. Very happy to assist you with a replacement.
output:
{"score": 5, "reason": "The response is warm and empathetic, offering a resolution with care."}


**Here the actual conversation to be scored:**
generated_query: {{response}}
output:
```

Then create a class `FriendlinessEvaluator` to load the Prompty file and process the outputs with JSON format:

```python
import os
import json
import sys
from promptflow.client import load_flow


class FriendlinessEvaluator:
    def __init__(self, model_config):
        current_dir = os.path.dirname(__file__)
        prompty_path = os.path.join(current_dir, "friendliness.prompty")
        self._flow = load_flow(source=prompty_path, model={"configuration": model_config})

    def __call__(self, *, response: str, **kwargs):
        llm_response = self._flow(response=response)
        try:
            response = json.loads(llm_response)
        except Exception as ex:
            response = llm_response
        return response
```

Now, create your own Prompty-based evaluator and run it on a row of data:

```python
from friendliness.friend import FriendlinessEvaluator

friendliness_eval = FriendlinessEvaluator(model_config)

friendliness_score = friendliness_eval(response="I will not apologize for my behavior!")
```

### Prompt-based evaluator output: Friendliness evaluator

```python
{
    'score': 1, 
    'reason': 'The response is hostile and unapologetic, lacking warmth or approachability.'
}
```

## Related content

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)
