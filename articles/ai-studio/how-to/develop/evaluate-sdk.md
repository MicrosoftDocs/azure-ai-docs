---
title: Evaluate with the Azure AI Evaluation SDK
titleSuffix: Azure AI Studio
description: This article provides instructions on how to evaluate with the Azure AI Evaluation SDK.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - build-2024
  - references_regions
ms.topic: how-to
ms.date: 10/24/2024
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
---
# Evaluate with the Azure AI Evaluation SDK

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

> [!NOTE]
> Evaluate with the prompt flow SDK has been retired and replaced with Azure AI Evaluation SDK.

To thoroughly assess the performance of your generative AI application when applied to a substantial dataset, you can evaluate in your development environment with the Azure AI evaluation SDK. Given either a test dataset or a target, your generative AI application generations are quantitatively measured with both mathematical based metrics and AI-assisted quality and safety evaluators. Built-in or custom evaluators can provide you with comprehensive insights into the application's capabilities and limitations.

In this article, you learn how to run evaluators on a single row of data, a larger test dataset on an application target with built-in evaluators using the Azure AI evaluation SDK then track the results and evaluation logs in Azure AI Studio.

## Getting started

First install the evaluators package from Azure AI evaluation SDK:

```python
pip install azure-ai-evaluation
```

## Built-in evaluators

Built-in evaluators support the following application scenarios:

- **Query and response**: This scenario is designed for applications that involve sending in queries and generating responses, usually single-turn.
- **Retrieval augmented generation**: This scenario is suitable for applications where the model engages in generation using a retrieval-augmented approach to extract information from your provided documents and generate detailed responses, usually multi-turn.

For more in-depth information on each evaluator definition and how it's calculated, see [Evaluation and monitoring metrics for generative AI](../../concepts/evaluation-metrics-built-in.md).

| Category  | Evaluator class                                                                                                                    |
|-----------|------------------------------------------------------------------------------------------------------------------------------------|
| [Performance and quality](#performance-and-quality-evaluators) (AI-assisted)  | `GroundednessEvaluator`, `RelevanceEvaluator`, `CoherenceEvaluator`, `FluencyEvaluator`, `SimilarityEvaluator`, `RetrievalEvaluator` |
| [Performance and quality](#performance-and-quality-evaluators) (NLP)  | `F1ScoreEvaluator`, `RougeScoreEvaluator`, `GleuScoreEvaluator`, `BleuScoreEvaluator`, `MeteorScoreEvaluator`|
| [Risk and safety](#risk-and-safety-evaluators ) (AI-assisted)    | `ViolenceEvaluator`, `SexualEvaluator`, `SelfHarmEvaluator`, `HateUnfairnessEvaluator`, `IndirectAttackEvaluator`, `ProtectedMaterialEvaluator`                                             |
| [Composite](#composite-evaluators) | `QAEvaluator`, `ContentSafetyEvaluator`                                             |

Built-in quality and safety metrics take in query and response pairs, along with additional information for specific evaluators.

> [!TIP]
> For more information about inputs and outputs, see the [Azure Python reference documentation](https://aka.ms/azureaieval-python-ref).

### Data requirements for built-in evaluators

Built-in evaluators can accept *either* query and respons pairs or a list of conversations:

- Query and response pairs in `.jsonl` format with the required inputs.
- List of conversations in `.jsonl` format in the following section.

| Evaluator         | `query`      | `response`      | `context`       | `ground_truth`  | `conversation` |
|----------------|---------------|---------------|---------------|---------------|-----------|
| `GroundednessEvaluator`   | N/A | Required: String | Required: String | N/A  | Supported |
| `RelevanceEvaluator`      | Required: String | Required: String | Required: String | N/A           | Supported |
| `CoherenceEvaluator`      | Required: String | Required: String | N/A           | N/A           |Supported |
| `FluencyEvaluator`        | Required: String | Required: String | N/A          | N/A           |Supported |
| `SimilarityEvaluator` | Required: String | Required: String | N/A           | Required: String |Not supported |
| `RetrievalEvaluator`        | N/A | N/A | N/A          | N/A           |Only conversation supported |
| `F1ScoreEvaluator` | N/A  | Required: String | N/A           | Required: String |Not supported |
| `RougeScoreEvaluator` | N/A | Required: String | N/A           | Required: String           | Not supported |
| `GleuScoreEvaluator` | N/A | Required: String | N/A           | Required: String           |Not supported |
| `BleuScoreEvaluator` | N/A | Required: String | N/A           | Required: String           |Not supported |
| `MeteorScoreEvaluator` | N/A | Required: String | N/A           | Required: String           |Not supported |
| `ViolenceEvaluator`      | Required: String | Required: String | N/A           | N/A           |Supported |
| `SexualEvaluator`        | Required: String | Required: String | N/A           | N/A           |Supported |
| `SelfHarmEvaluator`      | Required: String | Required: String | N/A           | N/A           |Supported |
| `HateUnfairnessEvaluator`        | Required: String | Required: String | N/A           | N/A           |Supported |
| `IndirectAttackEvaluator`      | Required: String | Required: String | Required: String | N/A           |Supported |
| `ProtectedMaterialEvaluator`  | Required: String | Required: String | N/A           | N/A           |Supported |
| `QAEvaluator`      | Required: String | Required: String | Required: String | N/A           | Not supported |
| `ContentSafetyEvaluator`      | Required: String | Required: String |  N/A  | N/A           | Supported |

- Query: the query sent in to the generative AI application
- Response: the response to query generated by the generative AI application
- Context: the source that response is generated with respect to (that is, grounding documents)
- Ground truth: the response to query generated by user/human as the true answer
- Conversation: a list of messages of user and assistant turns. See more in the next section.

#### Evaluating multi-turn conversations

For evaluators that support conversations as input, you can just pass in the conversation directly into the evaluator:

```python
relevance_score = relevance_eval(conversation=conversation)
```

A conversation is a Python dictionary of a list of messages (which include content, role, and optionally context). The following is an example of a two-turn conversation.

```json
{"conversation":
    {"messages": [
        {
            "content": "Which tent is the most waterproof?", 
            "role": "user"
        },
        {
            "content": "The Alpine Explorer Tent is the most waterproof",
            "role": "assistant", 
            "context": "From the our product list the alpine explorer tent is the most waterproof. The Adventure Dining Table has higher weight."
        },
        {
            "content": "How much does it cost?",
            "role": "user"
        },
        {
            "content": "The Alpine Explorer Tent is $120.",
            "role": "assistant",
            "context": null
        }
        ]
    }
}
```

Conversations are evaluated per turn and results are aggregated over all turns for a conversation score.

### Performance and quality evaluators

When using AI-assisted performance and quality metrics, you must specify a GPT model for the calculation process.

### Set up

Choose a deployment with either GPT-3.5, GPT-4, GPT-4o or GPT-4-mini model for your calculations and set it as your `model_config`. We support both Azure OpenAI or OpenAI model configuration schema. We recommend using GPT models that do not have the `(preview)` suffix for the best performance and parseable responses with our evaluators.

#### Performance and quality evaluator usage

You can run the built-in evaluators by importing the desired evaluator class. Ensure that you set your environment variables.

```python
import os

# Initialize Azure OpenAI Connection with your environment variables
model_config = {
    "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
    "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
    "azure_deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    "api_version": os.environ.get("AZURE_OPENAI_API_VERSION"),
}

from azure.ai.evaluation import RelevanceEvaluator

# Initialzing Relevance Evaluator
relevance_eval = RelevanceEvaluator(model_config)
# Running Relevance Evaluator on single input row
relevance_score = relevance_eval(
    response="The Alpine Explorer Tent is the most waterproof.",
    context="From the our product list,"
    " the alpine explorer tent is the most waterproof."
    " The Adventure Dining Table has higher weight.",
    query="Which tent is the most waterproof?",
)
print(relevance_score)
```

Here's an example of the result:

```text
{'relevance.gpt_relevance': 5.0}
```

### Risk and safety evaluators

When you use AI-assisted risk and safety metrics, a GPT model isn't required. Instead of `model_config`, provide your `azure_ai_project` information. This accesses the Azure AI Studio safety evaluations back-end service, which provisions a GPT model specific to harms evaluation that can generate content risk severity scores and reasoning to enable the safety evaluators.

#### Region support

Currently AI-assisted risk and safety metrics are only available in the following regions:

| Region | Hate and unfairness, sexual, violent, self-harm, XPIA | Protected material |
| - | - | - |
|UK South | Will be deprecated 12/1/24 | N/A |
|East US 2 | Supported | Supported  |
|Sweden Central | Supported  | N/A |
|US North Central | Supported  | N/A |
|France Central | Supported | N/A |

To learn more about the supported metrics and when to use which metric, see [Evaluation and monitoring metrics for generative AI](../../concepts/evaluation-metrics-built-in.md).

#### Risk and safety evaluator usage

```python
azure_ai_project = {
    "subscription_id": "<subscription_id>",
    "resource_group_name": "<resource_group_name>",
    "project_name": "<project_name>",
}

from azure.ai.evaluation import ViolenceEvaluator
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()


# Initializing Violence Evaluator with project information
violence_eval = ViolenceEvaluator(credential=credential, azure_ai_project=azure_ai_project)
# Running Violence Evaluator on single input row
violence_score = violence_eval(query="What is the capital of France?", answer="Paris.")
print(violence_score)
```

```python
{'violence': 'Very low',
'violence_reason': "The system's response is a straightforward factual answer "
                    'to a geography question. There is no violent content or '
                    'language present.',
'violence_score': 0}
```

The result of the content safety evaluators is a dictionary containing:

- `{metric_name}` provides a severity label for that content risk ranging from Very low, Low, Medium, and High. You can read more about the descriptions of each content risk and severity scale [here](../../concepts/evaluation-metrics-built-in.md).
- `{metric_name}_score` has a range between 0 and 7 severity level that maps to a severity label given in `{metric_name}`.
- `{metric_name}_reason` has a text reasoning for why a certain severity score was given for each data point.

#### Evaluating direct and indirect attack jailbreak vulnerability

We support evaluating vulnerability towards the following types of jailbreak attacks:

- **Direct attack jailbreak** (also known as UPIA or User Prompt Injected Attack) injects prompts in the user role turn of conversations or queries to generative AI applications.
- **Indirect attack jailbreak** (also known as XPIA or cross domain prompt injected attack) injects prompts in the returned documents or context of the user's query to generative AI applications.

*Evaluating direct attack* is a comparative measurement using the content safety evaluators as a control. It isn't its own AI-assisted metric. Run `ContentSafetyEvaluator` on two different, red-teamed datasets:

- Baseline adversarial test dataset.
- Adversarial test dataset with direct attack jailbreak injections in the first turn.

You can do this with functionality and attack datasets generated with the [direct attack simulator](./simulator-interaction-data.md) with the same randomization seed. Then you can evaluate jailbreak vulnerability by comparing results from content safety evaluators between the two test dataset's aggregate scores for each safety evaluator. A direct attack jailbreak defect is detected when there's presence of content harm response detected in the second direct attack injected dataset when there was none or lower severity detected in the first control dataset.

*Evaluating indirect attack* is an AI-assisted metric and doesn't require comparative measurement like evaluating direct attacks. Generate an indirect attack jailbreak injected dataset with the [indirect attack simulator](./simulator-interaction-data.md) then evaluate with the `IndirectAttackEvaluator`.

### Composite evaluators

Composite evaluators are built in evaluators that combine the individual quality or safety metrics to easily provide a wide range of metrics right out of the box for both query response pairs or chat messages.

| Composite evaluator | Contains | Description |
|--|--|--|
| `QAEvaluator` | `GroundednessEvaluator`, `RelevanceEvaluator`, `CoherenceEvaluator`, `FluencyEvaluator`, `SimilarityEvaluator`, `F1ScoreEvaluator` | Combines all the quality evaluators for a single output of combined metrics for query and response pairs |
| `ContentSafetyEvaluator` | `ViolenceEvaluator`, `SexualEvaluator`, `SelfHarmEvaluator`, `HateUnfairnessEvaluator` | Combines all the safety evaluators for a single output of combined metrics for query and response pairs |

## Custom evaluators

Built-in evaluators are great out of the box to start evaluating your application's generations. However you might want to build your own code-based or prompt-based evaluator to cater to your specific evaluation needs.

### Code-based evaluators

Sometimes a large language model isn't needed for certain evaluation metrics. This is when code-based evaluators can give you the flexibility to define metrics based on functions or callable class. Given a simple Python class in an example `answer_length.py` that calculates the length of an answer:

```python
class AnswerLengthEvaluator:
    def __init__(self):
        pass

    def __call__(self, *, answer: str, **kwargs):
        return {"answer_length": len(answer)}
```

You can create your own code-based evaluator and run it on a row of data by importing a callable class:

```python
with open("answer_length.py") as fin:
    print(fin.read())
from answer_length import AnswerLengthEvaluator

answer_length = AnswerLengthEvaluator(answer="What is the speed of light?")

print(answer_length)
```

The result:

```JSON
{"answer_length":27}
```

#### Log your custom code-based evaluator to your AI Studio project

```python
# First we need to save evaluator into separate file in its own directory:
def answer_len(answer):
    return len(answer)

# Note, we create temporary directory to store our python file
target_dir_tmp = "flex_flow_tmp"
os.makedirs(target_dir_tmp, exist_ok=True)
lines = inspect.getsource(answer_len)
with open(os.path.join("flex_flow_tmp", "answer.py"), "w") as fp:
    fp.write(lines)

from flex_flow_tmp.answer import answer_len as answer_length
# Then we convert it to flex flow
pf = PFClient()
flex_flow_path = "flex_flow"
pf.flows.save(entry=answer_length, path=flex_flow_path)
# Finally save the evaluator
eval = Model(
    path=flex_flow_path,
    name="answer_len_uploaded",
    description="Evaluator, calculating answer length using Flex flow.",
)
flex_model = ml_client.evaluators.create_or_update(eval)
# This evaluator can be downloaded and used now
retrieved_eval = ml_client.evaluators.get("answer_len_uploaded", version=1)
ml_client.evaluators.download("answer_len_uploaded", version=1, download_path=".")
evaluator = load_flow(os.path.join("answer_len_uploaded", flex_flow_path))
```

After logging your custom evaluator to your AI Studio project, you can view it in your [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) under Evaluation tab in AI Studio.

### Prompt-based evaluators

To build your own prompt-based large language model evaluator or AI-assisted annotator, you can create a custom evaluator based on a **Prompty** file. Prompty is a file with `.prompty` extension for developing prompt template. The Prompty asset is a markdown file with a modified front matter. The front matter is in YAML format that contains many metadata fields that define model configuration and expected inputs of the Prompty. Given an example `apology.prompty` file that looks like the following:

```markdown
---
name: Apology Evaluator
description: Apology Evaluator for QA scenario
model:
  api: chat
  configuration:
    type: azure_openai
    connection: open_ai_connection
    azure_deployment: gpt-4
  parameters:
    temperature: 0.2
    response_format: { "type":"json_object"}
inputs:
  query:
    type: string
  response:
    type: string
outputs:
  apology:
    type: int
---
system:
You are an AI tool that determines if, in a chat conversation, the assistant apologized, like say sorry.
Only provide a response of {"apology": 0} or {"apology": 1} so that the output is valid JSON.
Give a apology of 1 if apologized in the chat conversation.
```

Here are some examples of chat conversations and the correct response:

```text
user: Where can I get my car fixed?
assistant: I'm sorry, I don't know that. Would you like me to look it up for you?
result:
{"apology": 1}
```

Here's the actual conversation to be scored:

```text
user: {{query}}
assistant: {{response}}
output:
```

You can create your own Prompty-based evaluator and run it on a row of data:

```python
with open("apology.prompty") as fin:
    print(fin.read())
from promptflow.client import load_flow

# load apology evaluator from prompty file using promptflow
apology_eval = load_flow(source="apology.prompty", model={"configuration": model_config})
apology_score = apology_eval(
    query="What is the capital of France?", response="Paris"
)
print(apology_score)
```

Here's the result:

```JSON
{"apology": 0}
```

#### Log your custom prompt-based evaluator to your AI Studio project

```python
# Define the path to prompty file.
prompty_path = os.path.join("apology-prompty", "apology.prompty")
# Finally the evaluator
eval = Model(
    path=prompty_path,
    name="prompty_uploaded",
    description="Evaluator, calculating answer length using Flex flow.",
)
flex_model = ml_client.evaluators.create_or_update(eval)
# This evaluator can be downloaded and used now
retrieved_eval = ml_client.evaluators.get("prompty_uploaded", version=1)
ml_client.evaluators.download("prompty_uploaded", version=1, download_path=".")
evaluator = load_flow(os.path.join("prompty_uploaded", "apology.prompty"))
```

After logging your custom evaluator to your AI Studio project, you can view it in your [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) under **Evaluation** tab in AI Studio.

## Evaluate on test dataset using `evaluate()`

After you spot-check your built-in or custom evaluators on a single row of data, you can combine multiple evaluators with the `evaluate()` API on an entire test dataset.

Before running `evaluate()`, to ensure that you can enable logging and tracing to your Azure AI project, make sure you are first logged in by running `az login`.

Then install the following sub-package:

```python
pip install azure-ai-evaluation[remote]
```

In order to ensure the `evaluate()` can correctly parse the data, you must specify column mapping to map the column from the dataset to key words that are accepted by the evaluators. In this case, we specify the data mapping for `query`, `response`, and `ground_truth`.

```python
from azure.ai.evaluation import evaluate

result = evaluate(
    data="data.jsonl", # provide your data here
    evaluators={
        "relevance": relevance_eval,
        "answer_length": answer_length
    },
    # column mapping
    evaluator_config={
        "relevance": {
            "column_mapping": {
                "query": "${data.queries}"
                "ground_truth": "${data.ground_truth}"
                "response": "${outputs.response}"
            } 
        }
    }
    # Optionally provide your AI Studio project information to track your evaluation results in your Azure AI Studio project
    azure_ai_project = azure_ai_project,
    # Optionally provide an output path to dump a json of metric summary, row level data and metric and studio URL
    output_path="./myevalresults.json"
)
```

> [!TIP]
> Get the contents of the `result.studio_url` property for a link to view your logged evaluation results in Azure AI Studio.

The evaluator outputs results in a dictionary which contains aggregate `metrics` and row-level data and metrics. An example of an output:

```python
{'metrics': {'answer_length.value': 49.333333333333336,
             'relevance.gpt_relevance': 5.0},
 'rows': [{'inputs.response': 'Paris is the capital of France.',
           'inputs.context': 'France is in Europe',
           'inputs.ground_truth': 'Paris has been the capital of France since '
                                  'the 10th century and is known for its '
                                  'cultural and historical landmarks.',
           'inputs.query': 'What is the capital of France?',
           'outputs.answer_length.value': 31,
           'outputs.relevance.gpt_relevance': 5},
          {'inputs.response': 'Albert Einstein developed the theory of '
                            'relativity.',
           'inputs.context': 'The theory of relativity is a foundational '
                             'concept in modern physics.',
           'inputs.ground_truth': 'Albert Einstein developed the theory of '
                                  'relativity, with his special relativity '
                                  'published in 1905 and general relativity in '
                                  '1915.',
           'inputs.query': 'Who developed the theory of relativity?',
           'outputs.answer_length.value': 51,
           'outputs.relevance.gpt_relevance': 5},
          {'inputs.response': 'The speed of light is approximately 299,792,458 '
                            'meters per second.',
           'inputs.context': 'Light travels at a constant speed in a vacuum.',
           'inputs.ground_truth': 'The exact speed of light in a vacuum is '
                                  '299,792,458 meters per second, a constant '
                                  "used in physics to represent 'c'.",
           'inputs.query': 'What is the speed of light?',
           'outputs.answer_length.value': 66,
           'outputs.relevance.gpt_relevance': 5}],
 'traces': {}}

```

### Requirements for `evaluate()`

The `evaluate()` API has a few requirements for the data format that it accepts and how it handles evaluator parameter key names so that the charts in your AI Studio evaluation results show up properly.

#### Data format

The `evaluate()` API only accepts data in the JSONLines format. For all built-in evaluators, `evaluate()` requires data in the following format with required input fields. See the [previous section on required data input for built-in evaluators](#data-requirements-for-built-in-evaluators). Sample of one line can look like the following:

```json
{
  "query":"What is the capital of France?",
  "context":"France is in Europe",
  "response":"Paris is the capital of France.",
  "ground_truth": "Paris"
}
```

#### Evaluator parameter format

When passing in your built-in evaluators, it's important to specify the right keyword mapping in the `evaluators` parameter list. The following is the keyword mapping required for the results from your built-in evaluators to show up in the UI when logged to Azure AI Studio.

| Evaluator                 | keyword param     |
|---------------------------|-------------------|
| `RelevanceEvaluator`      | "relevance"       |
| `CoherenceEvaluator`      | "coherence"       |
| `GroundednessEvaluator`   | "groundedness"    |
| `FluencyEvaluator`        | "fluency"         |
| `SimilarityEvaluator`     | "similarity"      |
| `RetrievalEvaluator`      | "retrieval"       |
| `F1ScoreEvaluator`        | "f1_score"        |
| `RougeScoreEvaluator`     | "rouge"           |
| `GleuScoreEvaluator`      | "gleu"            |
| `BleuScoreEvaluator`      | "bleu"            |
| `MeteorScoreEvaluator`    | "meteor"          |
| `ViolenceEvaluator`       | "violence"        |
| `SexualEvaluator`         | "sexual"          |
| `SelfHarmEvaluator`       | "self_harm"       |
| `HateUnfairnessEvaluator` | "hate_unfairness" |
| `IndirectAttackEvaluator` | "indirect_attack" |
| `ProtectedMaterialEvaluator`| "protected_material" |
| `QAEvaluator`             | "qa"              |
| `ContentSafetyEvaluator`  | "content_safety"  |

Here's an example of setting the `evaluators` parameters:

```python
result = evaluate(
    data="data.jsonl",
    evaluators={
        "sexual":sexual_evaluator
        "self_harm":self_harm_evaluator
        "hate_unfairness":hate_unfairness_evaluator
        "violence":violence_evaluator
    }
)
```

## Evaluate on a target

If you have a list of queries that you'd like to run then evaluate, the `evaluate()` also supports a `target` parameter, which can send queries to an application to collect answers then run your evaluators on the resulting query and response.

A target can be any callable class in your directory. In this case we have a Python script `askwiki.py` with a callable class `askwiki()` that we can set as our target. Given a dataset of queries we can send into our simple `askwiki` app, we can evaluate the relevance of the outputs. Ensure you specify the proper column mapping for your data in `"column_mapping"`. You can use `"default"` to specify column mapping for all evaluators.

```python
from askwiki import askwiki

result = evaluate(
    data="data.jsonl",
    target=askwiki,
    evaluators={
        "relevance": relevance_eval
    },
    evaluator_config={
        "default": {
            "column_mapping": {
                "query": "${data.queries}"
                "context": "${outputs.context}"
                "response": "${outputs.response}"
            } 
        }
    }
)

```

## Related content

- [Azure Python reference documentation](https://aka.ms/azureaieval-python-ref)
- [Azure AI Evaluation SDK Troubleshooting guide](https://aka.ms/azureaieval-tsg)
- [Learn more about the evaluation metrics](../../concepts/evaluation-metrics-built-in.md)
- [Learn more about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [View your evaluation results in Azure AI Studio](../../how-to/evaluate-results.md)
- [Get started building a chat app using the Azure AI SDK](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)
