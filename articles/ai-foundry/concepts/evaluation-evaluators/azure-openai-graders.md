---
title: Azure OpenAI Graders for generative AI
titleSuffix: Microsoft Foundry
description: Learn about Azure OpenAI Graders for evaluating AI model outputs, including label grading, string checking, text similarity, and custom grading.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: mithigpe
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# Azure OpenAI graders

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Azure OpenAI graders are a new set of evaluation tools in the Microsoft Foundry SDK that evaluate the performance of AI models and their outputs. These graders include:

::: moniker range="foundry-classic"

- [Label grader](#label-grader)
- [String checker](#string-checker)
- [Text similarity](#text-similarity)
- [Python grader](#python-grader)

::: moniker-end

::: moniker range="foundry"

| Name                  | Type             | What it does                                                                 |
|-----------------------|------------------|------------------------------------------------------------------------------|
| `label_grader`        | `label_model`   | Classifies sentiment as **positive**, **neutral**, or **negative** using an LLM. |
| `text_check_grader`   | `text_similarity`| Compares ground truth and response using BLEU score for similarity.          |
| `string_check_grader` | `string_check`  | Performs a string equality check between two values.                         |
| `score`               | `score_model`   | Assigns a similarity score (1–5) based on semantic and structural comparison. |

::: moniker-end

You can run graders locally or remotely. Each grader assesses specific aspects of AI models and their outputs.

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

::: moniker range="foundry-classic"

## Model configuration for AI-assisted grader

The following code snippet shows the model configuration used by the AI-assisted grader:

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from dotenv import load_dotenv
load_dotenv()

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    api_key=os.environ.get("AZURE_API_KEY"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION")
)
```

## Label grader

`AzureOpenAILabelGrader` uses your custom prompt to instruct a model to classify outputs based on labels you define. It returns structured results with explanations for why each label was chosen.

> [!NOTE]
> We recommend using Azure OpenAI o3-mini for the best results.

Here's an example of `data.jsonl` used in the following code snippets:

```json
[
    {
        "query": "What is the importance of choosing the right provider in getting the most value out of your health insurance plan?",
        "ground_truth": "Choosing an in-network provider helps you save money and ensures better, more personalized care. [Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "Choosing the right provider is key to maximizing your health insurance benefits. In-network providers reduce costs, offer better coverage, and support continuity of care, leading to more effective and personalized treatment. [Northwind_Health_Plus_Benefits_Details.pdf][Northwind_Standard_Benefits_Details.pdf]"
    },
    {
        "query": "What should you do when choosing an in-network provider for your health care needs?",
        "ground_truth": "Check with Northwind Health Plus to confirm the provider is in-network, as this helps reduce costs.\n[Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "To choose an in-network provider, confirm they are part of your plan using the Northwind website or by calling their office. Also consider location, availability, and office hours. [Northwind_Standard_Benefits_Details.pdf]"
    },
    {
        "query": "What range of in-network providers does Northwind Health Plus offer?",
        "ground_truth": "Northwind Health Plus offers a wide range of in-network providers, including doctors, specialists, hospitals, and pharmacies.\n[Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "Northwind Health Plus offers a wide range of in-network providers, including primary care physicians, specialists, hospitals, and pharmacies [Northwind_Health_Plus_Benefits_Details.pdf]. The exact range of in-network providers may vary depending on the area, but the Northwind Health Plus website provides a searchable directory of all in-network providers in your area [Northwind_Health_Plus_Benefits_Details.pdf]. It is important to check with Northwind Health Plus to ensure that the provider you are considering is in-network [Northwind_Health_Plus_Benefits_Details.pdf]."
    },
    {
        "query": "What is the limitation of in-network providers?",
        "ground_truth": "The limitation of in-network providers is that they may not always be available in every area.\n[Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "The limitation of in-network providers is that they may not accept the amount of payment offered by Northwind Health, which means you may be responsible for a greater portion of the cost [Northwind_Standard_Benefits_Details.pdf]. Additionally, out-of-network providers may not offer additional services or discounts that are available to in-network providers [Northwind_Standard_Benefits_Details.pdf]. It is recommended to choose an in-network provider whenever possible to ensure the best value for your health care expenses [Northwind_Standard_Benefits_Details.pdf].\n\nSources:\n- Northwind_Standard_Benefits_Details.pdf"
    },
    {
        "query": "What resource does Northwind Health Plus provide to find in-network providers in your area?",
        "ground_truth": "The Northwind Health Plus website offers a searchable directory of all in-network providers in your area. This directory is regularly updated, so you can be sure that you are choosing from in-network providers that are available.\n[Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "Northwind Health Plus provides a variety of in-network providers, including primary care physicians, specialists, hospitals, and pharmacies [Northwind_Health_Plus_Benefits_Details.pdf]."
    }
]
```

### Label grader example

```python
from azure.ai.evaluation import AzureOpenAILabelGrader, evaluate

data_file_name="data.jsonl"

#  Evaluation criteria: Determine if the response column contains text that is "too short," "just right," or "too long," and pass if it is "just right."
label_grader = AzureOpenAILabelGrader(
    model_config=model_config,
    input=[{"content": "{{item.response}}", "role": "user"},
           {"content": "Any text including space that's more than 600 characters is too long, less than 500 characters is too short; 500 to 600 characters is just right.", "role": "user", "type": "message"}],
    labels=["too short", "just right", "too long"],
    passing_labels=["just right"],
    model="gpt-4o",
    name="label",
)

label_grader_evaluation = evaluate(
    data=data_file_name,
    evaluators={
        "label": label_grader
    },
)
```

### Label grader output

For each set of sample data in the data file, an evaluation result of `True` or `False` is returned, signifying if the output matches the defined passing label. The `score` is `1.0` for `True` cases, and `0.0` for `False` cases. The reason the model provided the label for the data is in `content` under `outputs.label.sample`.

```python
'outputs.label.sample':
...
...
    'output': [{'role': 'assistant',
      'content': '{"steps":[{"description":"Calculate the number of characters in the user\'s input including spaces.","conclusion":"The provided text contains 575 characters."},{"description":"Evaluate if the character count falls within the given ranges (greater than 600 too long, less than 500 too short, 500 to 600 just right).","conclusion":"The character count falls between 500 and 600, categorized as \'just right.\'"}],"result":"just right"}'}],
...
...
'outputs.label.passed': True,
'outputs.label.score': 1.0
```

In addition to individual data evaluation results, the grader returns a metric indicating the overall dataset pass rate.

```python
'metrics': {'label.pass_rate': 0.2}, #1/5 in this case
```

## String checker

Compares input text to a reference value, checking for exact or partial matches with optional case insensitivity. Useful for flexible text validations and pattern matching.

### String checker example

```python
from azure.ai.evaluation import AzureOpenAIStringCheckGrader

# Evaluation criteria: Pass if the query column contains "What is"
string_grader = AzureOpenAIStringCheckGrader(
    model_config=model_config,
    input="{{item.query}}",
    name="starts with what is",
    operation="like", # "eq" for equal, "ne" for not equal, "like" for contains, "ilike" for case-insensitive contains
    reference="What is",
)

string_grader_evaluation = evaluate(
    data=data_file_name,
    evaluators={
        "string": string_grader
    },
)
```

### String checker output

For each set of sample data in the data file, an evaluation result of `True` or `False` is returned, indicating whether the input text matches the defined pattern-matching rules. The `score` is `1.0` for `True` cases while `score` is `0.0` for `False` cases.

```python
'outputs.string.passed': True,
'outputs.string.score': 1.0
```

The grader also returns a metric indicating the overall dataset pass rate.

```python
'metrics': {'string.pass_rate': 0.4}, # 2/5 in this case
```

## Text similarity

Evaluates how closely input text matches a reference value using similarity metrics like `fuzzy_match`, `BLEU`, `ROUGE`, or `METEOR`. This is useful for assessing text quality or semantic closeness.

### Text similarity example

```python
from azure.ai.evaluation import AzureOpenAITextSimilarityGrader

# Evaluation criteria: Pass if response column and ground_truth column similarity score >= 0.5 using "fuzzy_match"
sim_grader = AzureOpenAITextSimilarityGrader(
    model_config=model_config,
    evaluation_metric="fuzzy_match", # support evaluation metrics including: "fuzzy_match", "bleu", "gleu", "meteor", "rouge_1", "rouge_2", "rouge_3", "rouge_4", "rouge_5", "rouge_l", "cosine",
    input="{{item.response}}",
    name="similarity",
    pass_threshold=0.5,
    reference="{{item.ground_truth}}",
)

sim_grader_evaluation = evaluate(
    data=data_file_name,
    evaluators={
        "similarity": sim_grader
    },
)
sim_grader_evaluation
```

### Text similarity output

For each set of sample data in the data file, a numerical similarity score is generated. This score ranges from 0 to 1 and indicates the degree of similarity, with higher scores representing greater similarity. An evaluation result of `True` or `False` is also returned, signifying whether the similarity score meets or exceeds the specified threshold based on the evaluation metric defined in the grader.

```python
'outputs.similarity.passed': True,
'outputs.similarity.score': 0.6117136659436009
```

The grader also returns a metric indicating the overall dataset pass rate.

```python
'metrics': {'similarity.pass_rate': 0.4}, # 2 out of 5 in this case
```

## Python grader

Advanced users can create or import custom Python grader functions and integrate them into the Azure OpenAI Python grader. This enables evaluations tailored to specific areas of interest beyond the capabilities of the existing Azure OpenAI graders. The following example demonstrates how to import a custom similarity grader function and configure it to run as an Azure OpenAI Python grader using the Microsoft Foundry SDK.

### Python grader example

```python
from azure.ai.evaluation import AzureOpenAIPythonGrader
 
python_similarity_grader = AzureOpenAIPythonGrader(
    model_config=model_config_aoai,
    name="custom_similarity",
    image_tag="2025-05-08",
    pass_threshold=0.3,
    source="""
    def grade(sample, item) -> float:
     \"\"\"
     Custom similarity grader using word overlap.
     Note: All data is in the 'item' parameter.
     \"\"\"
     # Extract from item, not sample!
     response = item.get("response", "") if isinstance(item, dict) else ""
     ground_truth = item.get("ground_truth", "") if isinstance(item, dict) else ""
    
     # Simple word overlap similarity
     response_words = set(response.lower().split())
     truth_words = set(ground_truth.lower().split())
    
     if not truth_words:
     return 0.0
    
     overlap = response_words.intersection(truth_words)
     similarity = len(overlap) / len(truth_words)
    
     return min(1.0, similarity)
""",
)

file_name = "eval_this.jsonl"
evaluation = evaluate(
    data=data_file_name,
    evaluators={
        "custom_similarity": python_similarity_grader,
    },
    #azure_ai_project=azure_ai_project,
)
evaluation
```

### Output

For each set of sample data in the data file, the Python grader returns a numerical score based on the defined function. Given a numerical threshold defined as part of the custom grader, we also output `True` if the score >= threshold, or `False` otherwise.

For example:

```python
"outputs.custom_similarity.passed": false,
"outputs.custom_similarity.score": 0.0
```

Aside from individual data evaluation results, the grader also returns a metric indicating the overall dataset pass rate.

```python
'metrics': {'custom_similarity.pass_rate': 0.0}, #0/5 in this case
```

::: moniker-end

::: moniker range="foundry"

## Example

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    DatasetVersion,
)
import json
import time
import os
from pprint import pprint
from openai.types.evals.create_eval_jsonl_run_data_source_param import CreateEvalJSONLRunDataSourceParam, SourceFileID
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

endpoint = os.environ[
    "AZURE_AI_PROJECT_ENDPOINT"
]  # Sample : https://<account_name>.services.ai.azure.com/api/projects/<project_name>

connection_name = os.environ.get("CONNECTION_NAME", "")
model_endpoint = os.environ.get("MODEL_ENDPOINT", "")  # Sample: https://<account_name>.openai.azure.com.
model_api_key = os.environ.get("MODEL_API_KEY", "")
model_deployment_name = os.environ.get("MODEL_DEPLOYMENT_NAME", "")  # Sample : gpt-4o-mini
dataset_name = os.environ.get("DATASET_NAME", "")
dataset_version = os.environ.get("DATASET_VERSION", "1")

# Construct the paths to the data folder and data file used in this sample
script_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.environ.get("DATA_FOLDER", os.path.join(script_dir, "data_folder"))
data_file = os.path.join(data_folder, "sample_data_evaluation.jsonl")

with DefaultAzureCredential() as credential:

    with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:

        print("Upload a single file and create a new Dataset to reference the file.")
        dataset: DatasetVersion = project_client.datasets.upload_file(
            name=dataset_name or f"eval-data-{datetime.utcnow().strftime('%Y-%m-%d_%H%M%S_UTC')}",
            version=dataset_version,
            file_path=data_file,
        )
        pprint(dataset)

        print("Creating an OpenAI client from the AI Project client")

        client = project_client.get_openai_client()

        data_source_config = {
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "response": {"type": "string"},
                    "context": {"type": "string"},
                    "ground_truth": {"type": "string"},
                },
                "required": [],
            },
            "include_sample_schema": True,
        }

        testing_criteria = [
            {
                "type": "label_model",
                "model": "{{aoai_deployment_and_model}}",
                "input": [
                    {
                        "role": "developer",
                        "content": "Classify the sentiment of the following statement as one of 'positive', 'neutral', or 'negative'",
                    },
                    {"role": "user", "content": "Statement: {{item.query}}"},
                ],
                "passing_labels": ["positive", "neutral"],
                "labels": ["positive", "neutral", "negative"],
                "name": "label_grader",
            },
            {
                "type": "text_similarity",
                "input": "{{item.ground_truth}}",
                "evaluation_metric": "bleu",
                "reference": "{{item.response}}",
                "pass_threshold": 1,
                "name": "text_check_grader",
            },
            {
                "type": "string_check",
                "input": "{{item.ground_truth}}",
                "reference": "{{item.ground_truth}}",
                "operation": "eq",
                "name": "string_check_grader",
            },
            {
                "type": "score_model",
                "name": "score",
                "model": "{{aoai_deployment_and_model}}",
                "input": [
                    {
                        "role": "system",
                        "content": 'Evaluate the degree of similarity between the given output and the ground truth on a scale from 1 to 5, using a chain of thought to ensure step-by-step reasoning before reaching the conclusion.\n\nConsider the following criteria:\n\n- 5: Highly similar - The output and ground truth are nearly identical, with only minor, insignificant differences.\n- 4: Somewhat similar - The output is largely similar to the ground truth but has few noticeable differences.\n- 3: Moderately similar - There are some evident differences, but the core essence is captured in the output.\n- 2: Slightly similar - The output only captures a few elements of the ground truth and contains several differences.\n- 1: Not similar - The output is significantly different from the ground truth, with few or no matching elements.\n\n# Steps\n\n1. Identify and list the key elements present in both the output and the ground truth.\n2. Compare these key elements to evaluate their similarities and differences, considering both content and structure.\n3. Analyze the semantic meaning conveyed by both the output and the ground truth, noting any significant deviations.\n4. Based on these comparisons, categorize the level of similarity according to the defined criteria above.\n5. Write out the reasoning for why a particular score is chosen, to ensure transparency and correctness.\n6. Assign a similarity score based on the defined criteria above.\n\n# Output Format\n\nProvide the final similarity score as an integer (1, 2, 3, 4, or 5).\n\n# Examples\n\n**Example 1:**\n\n- Output: "The cat sat on the mat."\n- Ground Truth: "The feline is sitting on the rug."\n- Reasoning: Both sentences describe a cat sitting on a surface, but they use different wording. The structure is slightly different, but the core meaning is preserved. There are noticeable differences, but the overall meaning is conveyed well.\n- Similarity Score: 3\n\n**Example 2:**\n\n- Output: "The quick brown fox jumps over the lazy dog."\n- Ground Truth: "A fast brown animal leaps over a sleeping canine."\n- Reasoning: The meaning of both sentences is very similar, with only minor differences in wording. The structure and intent are well preserved.\n- Similarity Score: 4\n\n# Notes\n\n- Always aim to provide a fair and balanced assessment.\n- Consider both syntactic and semantic differences in your evaluation.\n- Consistency in scoring similar pairs is crucial for accurate measurement.',
                    },
                    {"role": "user", "content": "Output: {{item.response}}\nGround Truth: {{item.ground_truth}}"},
                ],
                "image_tag": "2025-05-08",
                "pass_threshold": 0.5,
            },
        ]

        print("Creating Eval Group")
        eval_object = client.evals.create(
            name="aoai graders test",
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
        )
        print(f"Eval Group created")

        print("Get Eval Group by Id")
        eval_object_response = client.evals.retrieve(eval_object.id)
        print("Eval Run Response:")
        pprint(eval_object_response)

        print("Creating Eval Run")
        eval_run_object = client.evals.runs.create(
            eval_id=eval_object.id,
            name="dataset",
            metadata={"team": "eval-exp", "scenario": "notifications-v1"},
            data_source=CreateEvalJSONLRunDataSourceParam(
                source=SourceFileID(id=dataset.id or "", type="file_id"), type="jsonl"
            ),
        )
        print(f"Eval Run created")
        pprint(eval_run_object)

        print("Get Eval Run by Id")
        eval_run_response = client.evals.runs.retrieve(run_id=eval_run_object.id, eval_id=eval_object.id)
        print("Eval Run Response:")
        pprint(eval_run_response)

        while True:
            run = client.evals.runs.retrieve(run_id=eval_run_response.id, eval_id=eval_object.id)
            if run.status == "completed" or run.status == "failed":
                output_items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_object.id))
                pprint(output_items)
                print(f"Eval Run Report URL: {run.report_url}")
                
                break
            time.sleep(5)
            print("Waiting for eval run to complete...")
```

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)
- [How to run agent evaluation](../../how-to/develop/agent-evaluate-sdk.md)

::: moniker-end

::: moniker range="foundry"

- [Complete working sample.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_graders.py#L9)
- [How to run agent evaluation](../../default/observability/how-to/evaluate-agent.md)
- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)

::: moniker-end
