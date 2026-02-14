"""
Verbatim doc test: Run all 4 cloud evaluation types.
Code copied directly from cloud-evaluation.md (foundry moniker).
Only substitutions: endpoint, model name, agent name.
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GET STARTED (doc section verbatim)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
from azure.identity import DefaultAzureCredential 
from azure.ai.projects import AIProjectClient 
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
    SourceFileID,
)

# Azure AI Project endpoint
endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT",
    "https://aprilk-swedencentral-resource.services.ai.azure.com/api/projects/aprilk-swedencentral")

# Model deployment name (for AI-assisted evaluators)
model_deployment_name = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

# Dataset details (optional, for reusing existing datasets)
dataset_name = os.environ.get("DATASET_NAME", "eval-verbatim-test")
dataset_version = os.environ.get("DATASET_VERSION", "1")

# Create the project client
project_client = AIProjectClient( 
    endpoint=endpoint, 
    credential=DefaultAzureCredential(), 
)

# Get the OpenAI client for evaluation API
client = project_client.get_openai_client()

print("✓ Get started — client created")
print(f"  Base URL: {client.base_url}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PREPARE INPUT DATA (doc section verbatim)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Upload a local JSONL file. Skip this step if you already have a dataset registered.
try:
    data_id = project_client.datasets.upload_file(
        name=dataset_name,
        version=dataset_version,
        file_path="./evaluate_test_data.jsonl",
    ).id
except Exception as e:
    if "already exists" in str(e):
        ds = project_client.datasets.get(name=dataset_name, version=dataset_version)
        data_id = ds.id
    else:
        raise

print(f"✓ Data uploaded — {data_id}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# POLLING HELPER (from doc "Get results" section)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import time
from pprint import pprint

def poll(eval_id, run_id, label):
    while True:
        run = client.evals.runs.retrieve(run_id=run_id, eval_id=eval_id)
        if run.status in ("completed", "failed"):
            break
        time.sleep(5)
        print(f"  Waiting for eval run to complete... ({run.status})")
    output_items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_id))
    print(f"  Status: {run.status} | Items: {len(output_items)} | Report: {run.report_url}")
    if run.status == "failed":
        print(f"  ERROR: {getattr(run, 'error', 'unknown')}")
    return run


# ╔═══════════════════════════════════════════════════════════════════╗
# ║ 1. DATASET EVALUATION (doc section verbatim)                    ║
# ╚═══════════════════════════════════════════════════════════════════╝
print("\n" + "=" * 60)
print("1. DATASET EVALUATION")
print("=" * 60)

data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "response": {"type": "string"},
            "ground_truth": {"type": "string"},
        },
        "required": [],
    },
)

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "f1",
        "evaluator_name": "builtin.f1_score",
        "data_mapping": {
            "response": "{{item.response}}",
            "ground_truth": "{{item.ground_truth}}",
        },
    },
]

# Create the evaluation
eval_object = client.evals.create(
    name="dataset-evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Create a run using the uploaded dataset
eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="dataset-run",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl",
        source=SourceFileID(
            type="file_id",
            id=data_id,
        ),
    ),
)

print(f"  Eval: {eval_object.id} | Run: {eval_run.id}")
poll(eval_object.id, eval_run.id, "Dataset")


# ╔═══════════════════════════════════════════════════════════════════╗
# ║ 2. MODEL TARGET EVALUATION (doc section verbatim)               ║
# ╚═══════════════════════════════════════════════════════════════════╝
print("\n" + "=" * 60)
print("2. MODEL TARGET EVALUATION")
print("=" * 60)

input_messages = {
    "type": "template",
    "template": [
        {
            "type": "message",
            "role": "user",
            "content": {
                "type": "input_text",
                "text": "{{item.query}}"
            }
        }
    ]
}

target = {
    "type": "azure_ai_model",
    "model": model_deployment_name,  # doc uses "gpt-5-mini"
    "sampling_params": {
        "top_p": 1.0,
        "max_completion_tokens": 2048,
    },
}

data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
        "required": ["query"],
    },
    include_sample_schema=True,
)

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
]

eval_object = client.evals.create(
    name="Model Target Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_target_completions",
    "source": {
        "type": "file_id",
        "id": data_id,
    },
    "input_messages": input_messages,
    "target": target,
}

eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="model-target-evaluation",
    data_source=data_source,
)

print(f"  Eval: {eval_object.id} | Run: {eval_run.id}")
poll(eval_object.id, eval_run.id, "Model Target")


# ╔═══════════════════════════════════════════════════════════════════╗
# ║ 3. AGENT TARGET EVALUATION (doc section verbatim)               ║
# ╚═══════════════════════════════════════════════════════════════════╝
print("\n" + "=" * 60)
print("3. AGENT TARGET EVALUATION")
print("=" * 60)

input_messages = {
    "type": "template",
    "template": [
        {
            "type": "message",
            "role": "developer",
            "content": {
                "type": "input_text",
                "text": "You are a helpful assistant. Answer clearly and safely."
            }
        },
        {
            "type": "message",
            "role": "user",
            "content": {
                "type": "input_text",
                "text": "{{item.query}}"
            }
        }
    ]
}

target = {
    "type": "azure_ai_agent",
    "name": "code-agent",  # doc uses "my-agent"
}

data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
        "required": ["query"],
    },
    include_sample_schema=True,
)

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "task_adherence",
        "evaluator_name": "builtin.task_adherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
    },
]

eval_object = client.evals.create(
    name="Agent Target Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_target_completions",
    "source": {
        "type": "file_id",
        "id": data_id,
    },
    "input_messages": input_messages,
    "target": target,
}

agent_eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-target-evaluation",
    data_source=data_source,
)

print(f"  Eval: {eval_object.id} | Run: {agent_eval_run.id}")
poll(eval_object.id, agent_eval_run.id, "Agent Target")


# ╔═══════════════════════════════════════════════════════════════════╗
# ║ 4. AGENT RESPONSE EVALUATION (doc section verbatim)             ║
# ╚═══════════════════════════════════════════════════════════════════╝
print("\n" + "=" * 60)
print("4. AGENT RESPONSE EVALUATION")
print("=" * 60)

# Collect response IDs (doc section verbatim)
# Generate response IDs by calling a model through the Responses API
response1 = client.responses.create(
    model=model_deployment_name,
    input="What is machine learning?",
)
print(f"  Response ID 1: {response1.id}")

response2 = client.responses.create(
    model=model_deployment_name,
    input="Explain neural networks.",
)
print(f"  Response ID 2: {response2.id}")

# Create evaluation and run (doc section verbatim)
data_source_config = {"type": "azure_ai_source", "scenario": "responses"}

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
    },
]

eval_object = client.evals.create(
    name="Agent Response Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_responses",
    "item_generation_params": {
        "type": "response_retrieval",
        "data_mapping": {"response_id": "{{item.resp_id}}"},
        "source": {
            "type": "file_content",
            "content": [
                {"item": {"resp_id": response1.id}},
                {"item": {"resp_id": response2.id}},
            ]
        },
    },
}

eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-response-evaluation",
    data_source=data_source,
)

print(f"  Eval: {eval_object.id} | Run: {eval_run.id}")
poll(eval_object.id, eval_run.id, "Agent Response")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "=" * 60)
print("ALL 4 EVALUATIONS COMPLETE")
print("=" * 60)
