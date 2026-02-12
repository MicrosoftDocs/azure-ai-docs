"""
Validate evaluator configurations from documentation.
Tests coherence, fluency, groundedness, relevance configs.
"""

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
)
import time
import sys

endpoint = 'https://aprilk-swedencentral-resource.services.ai.azure.com/api/projects/aprilk-swedencentral'
model_deployment = 'gpt-4o-mini'

credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=endpoint, credential=credential)
client = project_client.get_openai_client()


def run_eval(name, testing_criteria, data_source_config, test_data):
    print(f"\n=== Testing {name} ===")
    eval_obj = client.evals.create(
        name=name,
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )
    print(f"Evaluation: {eval_obj.id}")

    run = client.evals.runs.create(
        eval_id=eval_obj.id,
        name="test_run",
        data_source=CreateEvalJSONLRunDataSourceParam(
            type="jsonl",
            source=SourceFileContent(
                type="file_content",
                content=[SourceFileContentContent(item=d) for d in test_data],
            ),
        ),
    )

    while True:
        r = client.evals.runs.retrieve(run_id=run.id, eval_id=eval_obj.id)
        if r.status in ["completed", "failed"]:
            print(f"Status: {r.status}")
            if r.status == "completed":
                for item in client.evals.runs.output_items.list(run_id=r.id, eval_id=eval_obj.id):
                    for res in item.results:
                        score = getattr(res, "score", "N/A")
                        passed = getattr(res, "passed", "N/A")
                        print(f"  {res.name}: score={score}, passed={passed}")
            break
        time.sleep(5)

    client.evals.delete(eval_id=eval_obj.id)
    return r.status == "completed"


# Test 1: Textual Similarity
if "similarity" in sys.argv or len(sys.argv) == 1:
    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "Similarity",
            "evaluator_name": "builtin.similarity",
            "initialization_parameters": {"deployment_name": model_deployment},
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
                "ground_truth": "{{item.ground_truth}}",
            },
        },
        {
            "type": "azure_ai_evaluator",
            "name": "BLEUScore",
            "evaluator_name": "builtin.bleu_score",
            "data_mapping": {
                "ground_truth": "{{item.ground_truth}}",
                "response": "{{item.response}}",
            },
        },
        {
            "type": "azure_ai_evaluator",
            "name": "ROUGEScore",
            "evaluator_name": "builtin.rouge_score",
            "initialization_parameters": {"rouge_type": "rouge1"},
            "data_mapping": {
                "ground_truth": "{{item.ground_truth}}",
                "response": "{{item.response}}",
            },
        },
    ]

    data_source_config = DataSourceConfigCustom({
        "type": "custom",
        "item_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "response": {"type": "string"},
                "ground_truth": {"type": "string"},
            },
            "required": ["query", "response", "ground_truth"],
        },
        "include_sample_schema": False,
    })

    test_data = [{
        "query": "What is the capital of France?",
        "response": "Paris is the capital of France.",
        "ground_truth": "The capital of France is Paris.",
    }]

    run_eval("Textual Similarity", testing_criteria, data_source_config, test_data)


# Test 2: Risk/Safety
if "safety" in sys.argv or len(sys.argv) == 1:
    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "Violence",
            "evaluator_name": "builtin.violence",
            "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "Self Harm",
            "evaluator_name": "builtin.self_harm",
            "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "Hate Unfairness",
            "evaluator_name": "builtin.hate_unfairness",
            "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
        },
    ]

    data_source_config = DataSourceConfigCustom({
        "type": "custom",
        "item_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "response": {"type": "string"},
            },
            "required": ["query", "response"],
        },
        "include_sample_schema": False,
    })

    test_data = [{
        "query": "How do I handle a difficult coworker?",
        "response": "Try having an open conversation to understand their perspective and find common ground.",
    }]

    run_eval("Risk Safety", testing_criteria, data_source_config, test_data)


# Test 3: Agent evaluators (task_adherence)
if "agent" in sys.argv or len(sys.argv) == 1:
    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "task_adherence",
            "evaluator_name": "builtin.task_adherence",
            "initialization_parameters": {"deployment_name": model_deployment},
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
    ]

    data_source_config = DataSourceConfigCustom({
        "type": "custom",
        "item_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "response": {"type": "string"},
            },
            "required": ["query", "response"],
        },
        "include_sample_schema": False,
    })

    test_data = [{
        "query": "What's the weather in Seattle?",
        "response": "The weather in Seattle is rainy, 14C.",
    }]

    run_eval("Agent Evaluators", testing_criteria, data_source_config, test_data)


print("\n=== All tests complete! ===")

