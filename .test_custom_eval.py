"""Test all code samples from custom-evaluators.md"""
import os
import time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import EvaluatorCategory, EvaluatorDefinitionType
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam, SourceFileContent, SourceFileContentContent,
)

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]
project_client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
client = project_client.get_openai_client()
print("Client setup OK")


def wait_for_run(eval_id, run_id):
    while True:
        run = client.evals.runs.retrieve(run_id=run_id, eval_id=eval_id)
        if run.status in ("completed", "failed"):
            return run
        time.sleep(5)


# Step 1: Create code-based evaluator
print("\n=== Creating code-based evaluator ===")
code_evaluator = project_client.evaluators.create_version(
    name="response_length_scorer",
    evaluator_version={
        "name": "response_length_scorer",
        "categories": [EvaluatorCategory.QUALITY],
        "display_name": "Response Length Scorer",
        "description": "Scores responses based on length, preferring 50-500 characters",
        "definition": {
            "type": EvaluatorDefinitionType.CODE,
            "code_text": (
                'def grade(sample: dict, item: dict) -> float:\n'
                '    """Score based on response length (prefer 50-500 chars)."""\n'
                '    response = item.get("response", "")\n'
                '    if not response:\n'
                '        return 0.0\n'
                '    length = len(response)\n'
                '    if length < 50:\n'
                '        return 0.2\n'
                '    elif length > 500:\n'
                '        return 0.5\n'
                '    return 1.0\n'
            ),
            "init_parameters": {
                "type": "object",
                "properties": {
                    "deployment_name": {"type": "string"},
                    "pass_threshold": {"type": "number"},
                },
                "required": ["deployment_name", "pass_threshold"],
            },
            "metrics": {
                "result": {
                    "type": "continuous",
                    "desirable_direction": "increase",
                    "min_value": 0.0,
                    "max_value": 1.0,
                }
            },
            "data_schema": {
                "type": "object",
                "required": ["item"],
                "properties": {
                    "item": {
                        "type": "object",
                        "properties": {
                            "response": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
)
print(f"Code evaluator created: {code_evaluator.name} v{code_evaluator.version}")

# Step 2: Create prompt-based evaluator
print("\n=== Creating prompt-based evaluator ===")
prompt_evaluator = project_client.evaluators.create_version(
    name="friendliness_evaluator",
    evaluator_version={
        "name": "friendliness_evaluator",
        "categories": [EvaluatorCategory.QUALITY],
        "display_name": "Friendliness Evaluator",
        "description": "Evaluates the warmth and approachability of a response",
        "definition": {
            "type": EvaluatorDefinitionType.PROMPT,
            "prompt_text": (
                "Friendliness assesses the warmth and approachability of the response.\n"
                "Rate the friendliness of the response between one and five "
                "using the following scale:\n\n"
                "1 - Unfriendly or hostile\n"
                "2 - Mostly unfriendly\n"
                "3 - Neutral\n"
                "4 - Mostly friendly\n"
                "5 - Very friendly\n\n"
                "Assign a rating based on the tone and demeanor of the response.\n\n"
                "Response:\n{{response}}\n\n"
                "Output Format (JSON):\n"
                '{\n  "result": <integer from 1 to 5>,\n'
                '  "reason": "<brief explanation for the score>"\n}\n'
            ),
            "init_parameters": {
                "type": "object",
                "properties": {
                    "deployment_name": {"type": "string"},
                    "threshold": {"type": "number"},
                },
                "required": ["deployment_name", "threshold"],
            },
            "data_schema": {
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
                "required": ["response"],
            },
            "metrics": {
                "custom_prompt": {
                    "type": "ordinal",
                    "desirable_direction": "increase",
                    "min_value": 1,
                    "max_value": 5,
                }
            },
        },
    },
)
print(f"Prompt evaluator created: {prompt_evaluator.name} v{prompt_evaluator.version}")

# Test 1: Dataset evaluation with both evaluators
print("\n=== Test 1: Dataset evaluation (code + prompt) ===")
ds_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {"response": {"type": "string"}},
        "required": ["response"],
    },
)

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "response_length_scorer",
        "evaluator_name": "response_length_scorer",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
            "pass_threshold": 0.5,
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "friendliness_evaluator",
        "evaluator_name": "friendliness_evaluator",
        "data_mapping": {
            "response": "{{item.response}}",
        },
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
            "threshold": 3,
        },
    },
]

eval_obj = client.evals.create(
    name="test-dataset-both",
    data_source_config=ds_config,
    testing_criteria=testing_criteria,
)
print(f"Eval created: {eval_obj.id}")

eval_run = client.evals.runs.create(
    eval_id=eval_obj.id,
    name="dataset-run",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl",
        source=SourceFileContent(
            type="file_content",
            content=[
                SourceFileContentContent(
                    item={
                        "response": "I'm sorry this watch isn't working for you. I'd be happy to help you with a replacement!",
                    }
                ),
                SourceFileContentContent(
                    item={
                        "response": "I will not apologize for my behavior!",
                    }
                ),
            ],
        ),
    ),
)
print(f"Run started: {eval_run.id}")

run = wait_for_run(eval_obj.id, eval_run.id)
print(f"Status: {run.status}")
if run.error:
    print(f"Error: {run.error}")
else:
    items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_obj.id))
    print(f"Items: {len(items)}")
    for it in items:
        print(f"  {it.results}")
print(f"Report: {run.report_url}")

# Test 2: Agent/model target evaluation (code-based only, using sample access pattern)
print("\n=== Test 2: Model target evaluation (code-based with sample access) ===")
# Create a code evaluator that accesses item.sample
code_eval_sample = project_client.evaluators.create_version(
    name="response_length_scorer_sample",
    evaluator_version={
        "name": "response_length_scorer_sample",
        "categories": [EvaluatorCategory.QUALITY],
        "display_name": "Response Length Scorer (Sample)",
        "description": "Scores generated responses via item.sample access pattern",
        "definition": {
            "type": EvaluatorDefinitionType.CODE,
            "code_text": (
                'def grade(sample: dict, item: dict) -> float:\n'
                '    """Score based on response length using sample access pattern."""\n'
                '    # Model/agent target: access generated response via item.sample\n'
                '    response = item.get("sample", {}).get("output_text", "")\n'
                '    if not response:\n'
                '        # Fallback to direct item access for dataset evaluation\n'
                '        response = item.get("response", "")\n'
                '    if not response:\n'
                '        return 0.0\n'
                '    length = len(response)\n'
                '    if length < 50:\n'
                '        return 0.2\n'
                '    elif length > 500:\n'
                '        return 0.5\n'
                '    return 1.0\n'
            ),
            "init_parameters": {
                "type": "object",
                "properties": {
                    "deployment_name": {"type": "string"},
                    "pass_threshold": {"type": "number"},
                },
                "required": ["deployment_name", "pass_threshold"],
            },
            "metrics": {
                "result": {
                    "type": "continuous",
                    "desirable_direction": "increase",
                    "min_value": 0.0,
                    "max_value": 1.0,
                }
            },
            "data_schema": {
                "type": "object",
                "required": ["item"],
                "properties": {
                    "item": {
                        "type": "object",
                        "properties": {
                            "response": {"type": "string"},
                            "sample": {
                                "type": "object",
                                "properties": {
                                    "output_text": {"type": "string"},
                                },
                            },
                        },
                    },
                },
            },
        },
    },
)
print(f"Sample evaluator created: {code_eval_sample.name} v{code_eval_sample.version}")

# Test with data that simulates sample field
ds_config2 = DataSourceConfigCustom({
    "type": "custom",
    "item_schema": {
        "type": "object",
        "properties": {
            "response": {"type": "string"},
            "sample": {
                "type": "object",
                "properties": {"output_text": {"type": "string"}},
            },
        },
        "required": ["response"],
    },
    "include_sample_schema": True,
})

testing_criteria2 = [
    {
        "type": "azure_ai_evaluator",
        "name": "response_length_scorer_sample",
        "evaluator_name": "response_length_scorer_sample",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
            "pass_threshold": 0.5,
        },
    },
]

eval_obj2 = client.evals.create(
    name="test-sample-access",
    data_source_config=ds_config2,
    testing_criteria=testing_criteria2,
)

eval_run2 = client.evals.runs.create(
    eval_id=eval_obj2.id,
    name="sample-access-run",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl",
        source=SourceFileContent(
            type="file_content",
            content=[
                SourceFileContentContent(
                    item={"response": "A medium-length helpful response for testing purposes."}
                ),
            ],
        ),
    ),
)

run2 = wait_for_run(eval_obj2.id, eval_run2.id)
print(f"Status: {run2.status}")
if run2.error:
    print(f"Error: {run2.error}")
else:
    items2 = list(client.evals.runs.output_items.list(run_id=run2.id, eval_id=eval_obj2.id))
    print(f"Items: {len(items2)}")
    for it in items2:
        print(f"  {it.results}")

print("\n=== All tests complete ===")
