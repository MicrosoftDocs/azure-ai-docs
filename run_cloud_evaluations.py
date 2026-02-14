"""
Run all 4 cloud evaluation types from the Microsoft Foundry SDK docs.

Evaluation types:
  1. Dataset evaluation — evaluate pre-computed responses inline
  2. Model target evaluation — send queries to gpt-4o-mini, evaluate responses
  3. Agent target evaluation — send queries to code-agent, evaluate responses
  4. Agent response evaluation — generate response IDs from code-agent, then evaluate by ID

Results are NOT deleted so you can inspect them in the Foundry portal.
"""

import time
from pprint import pprint

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ENDPOINT = "https://aprilk-swedencentral-resource.services.ai.azure.com/api/projects/aprilk-swedencentral"
MODEL_DEPLOYMENT = "gpt-4o-mini"
AGENT_NAME = "code-agent"

# ---------------------------------------------------------------------------
# Client setup
# ---------------------------------------------------------------------------
project_client = AIProjectClient(
    endpoint=ENDPOINT,
    credential=DefaultAzureCredential(),
)
client = project_client.get_openai_client()

print("=" * 60)
print("Cloud Evaluation — 4 Types")
print("=" * 60)


# ---------------------------------------------------------------------------
# Helper: poll an eval run to completion
# ---------------------------------------------------------------------------
def poll_eval_run(client, eval_id, run_id, label=""):
    """Poll until the run completes or fails, then print results."""
    print(f"\n{'─' * 50}")
    print(f"Polling {label} (eval={eval_id}, run={run_id})...")
    while True:
        run = client.evals.runs.retrieve(run_id=run_id, eval_id=eval_id)
        if run.status in ("completed", "failed", "canceled"):
            break
        print(f"  Status: {run.status} — waiting 10s...")
        time.sleep(10)

    print(f"  Final status: {run.status}")
    if run.status == "completed":
        output_items = list(
            client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_id)
        )
        pprint(output_items)
        report_url = getattr(run, "report_url", None)
        if report_url:
            print(f"  Report URL: {report_url}")
    else:
        print(f"  Run did not complete successfully. Status: {run.status}")
        # Print whatever info is available
        pprint(run)

    return run


# ===================================================================
# 1. DATASET EVALUATION
# ===================================================================
print("\n" + "=" * 60)
print("1. Dataset Evaluation")
print("=" * 60)

dataset_data_source_config = DataSourceConfigCustom(
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
    include_sample_schema=True,
)

dataset_testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": MODEL_DEPLOYMENT,
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
        "initialization_parameters": {
            "deployment_name": MODEL_DEPLOYMENT,
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "f1",
        "evaluator_name": "builtin.f1_score",
    },
]

dataset_eval = client.evals.create(
    name="dataset-evaluation",
    data_source_config=dataset_data_source_config,
    testing_criteria=dataset_testing_criteria,
)
print(f"Created eval: {dataset_eval.id}")

# Inline data for the dataset evaluation run
dataset_source = SourceFileContent(
    type="file_content",
    content=[
        SourceFileContentContent(
            item={
                "query": "What is machine learning?",
                "response": "Machine learning is a subset of AI that enables systems to learn from data.",
                "ground_truth": "Machine learning is a type of artificial intelligence that learns from data to make predictions.",
            }
        ),
        SourceFileContentContent(
            item={
                "query": "Explain neural networks.",
                "response": "Neural networks are computing systems inspired by biological neural networks in the brain.",
                "ground_truth": "Neural networks are a set of algorithms modeled after the human brain, designed to recognize patterns.",
            }
        ),
        SourceFileContentContent(
            item={
                "query": "What is deep learning?",
                "response": "Deep learning uses multi-layered neural networks to model complex patterns in data.",
                "ground_truth": "Deep learning is a subset of machine learning that uses neural networks with many layers.",
            }
        ),
    ],
)

dataset_run = client.evals.runs.create(
    eval_id=dataset_eval.id,
    name="dataset-run",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl",
        source=dataset_source,
    ),
)
print(f"Created run: {dataset_run.id}")
poll_eval_run(client, dataset_eval.id, dataset_run.id, "Dataset Evaluation")


# ===================================================================
# 2. MODEL TARGET EVALUATION
# ===================================================================
print("\n" + "=" * 60)
print("2. Model Target Evaluation")
print("=" * 60)

model_input_messages = {
    "type": "template",
    "template": [
        {
            "type": "message",
            "role": "user",
            "content": {
                "type": "input_text",
                "text": "{{item.query}}",
            },
        }
    ],
}

model_target = {
    "type": "azure_ai_model",
    "model": MODEL_DEPLOYMENT,
    "sampling_params": {
        "top_p": 1.0,
        "max_completion_tokens": 2048,
    },
}

model_data_source_config = DataSourceConfigCustom(
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

model_testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": MODEL_DEPLOYMENT,
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

model_eval = client.evals.create(
    name="Model Target Evaluation",
    data_source_config=model_data_source_config,
    testing_criteria=model_testing_criteria,
)
print(f"Created eval: {model_eval.id}")

model_data_source = {
    "type": "azure_ai_target_completions",
    "source": {
        "type": "file_content",
        "content": [
            {"item": {"query": "What is the capital of France?"}},
            {"item": {"query": "Explain how photosynthesis works."}},
            {"item": {"query": "What are the benefits of exercise?"}},
        ],
    },
    "input_messages": model_input_messages,
    "target": model_target,
}

model_run = client.evals.runs.create(
    eval_id=model_eval.id,
    name="model-target-run",
    data_source=model_data_source,
)
print(f"Created run: {model_run.id}")
poll_eval_run(client, model_eval.id, model_run.id, "Model Target Evaluation")


# ===================================================================
# 3. AGENT TARGET EVALUATION
# ===================================================================
print("\n" + "=" * 60)
print("3. Agent Target Evaluation")
print("=" * 60)

agent_input_messages = {
    "type": "template",
    "template": [
        {
            "type": "message",
            "role": "developer",
            "content": {
                "type": "input_text",
                "text": "You are a helpful assistant. Answer clearly and safely.",
            },
        },
        {
            "type": "message",
            "role": "user",
            "content": {
                "type": "input_text",
                "text": "{{item.query}}",
            },
        },
    ],
}

agent_target = {
    "type": "azure_ai_agent",
    "name": AGENT_NAME,
}

agent_data_source_config = DataSourceConfigCustom(
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

agent_testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": MODEL_DEPLOYMENT,
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
            "deployment_name": MODEL_DEPLOYMENT,
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
    },
]

agent_eval = client.evals.create(
    name="Agent Target Evaluation",
    data_source_config=agent_data_source_config,
    testing_criteria=agent_testing_criteria,
)
print(f"Created eval: {agent_eval.id}")

agent_data_source = {
    "type": "azure_ai_target_completions",
    "source": {
        "type": "file_content",
        "content": [
            {"item": {"query": "Write a Python function to reverse a string."}},
            {"item": {"query": "Explain the difference between a list and a tuple in Python."}},
        ],
    },
    "input_messages": agent_input_messages,
    "target": agent_target,
}

agent_eval_run = client.evals.runs.create(
    eval_id=agent_eval.id,
    name="agent-target-run",
    data_source=agent_data_source,
)
print(f"Created run: {agent_eval_run.id}")
poll_eval_run(client, agent_eval.id, agent_eval_run.id, "Agent Target Evaluation")


# ===================================================================
# 4. AGENT RESPONSE EVALUATION
# ===================================================================
print("\n" + "=" * 60)
print("4. Agent Response Evaluation")
print("=" * 60)

# Step 1: Generate response IDs by calling the model via the Responses API.
# The agent response evaluation retrieves responses by ID regardless of whether
# they were generated by a model or an agent.
print("Generating response IDs via the Responses API...")

queries = [
    "What is a decorator in Python?",
    "How do you handle exceptions in Python?",
]
response_ids = []

for q in queries:
    resp = client.responses.create(
        model=MODEL_DEPLOYMENT,
        input=q,
    )
    response_ids.append(resp.id)
    print(f"  Generated response ID: {resp.id}")

# Step 2: Create evaluation and run using the response IDs
resp_data_source_config = {"type": "azure_ai_source", "scenario": "responses"}

resp_testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": MODEL_DEPLOYMENT,
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
    },
]

resp_eval = client.evals.create(
    name="Agent Response Evaluation",
    data_source_config=resp_data_source_config,
    testing_criteria=resp_testing_criteria,
)
print(f"Created eval: {resp_eval.id}")

resp_data_source = {
    "type": "azure_ai_responses",
    "item_generation_params": {
        "type": "response_retrieval",
        "data_mapping": {"response_id": "{{item.resp_id}}"},
        "source": {
            "type": "file_content",
            "content": [{"item": {"resp_id": rid}} for rid in response_ids],
        },
    },
}

resp_eval_run = client.evals.runs.create(
    eval_id=resp_eval.id,
    name="agent-response-run",
    data_source=resp_data_source,
)
print(f"Created run: {resp_eval_run.id}")
poll_eval_run(client, resp_eval.id, resp_eval_run.id, "Agent Response Evaluation")


# ===================================================================
# Summary
# ===================================================================
print("\n" + "=" * 60)
print("SUMMARY — All 4 evaluations created (not deleted)")
print("=" * 60)
print(f"1. Dataset Evaluation:        eval={dataset_eval.id}  run={dataset_run.id}")
print(f"2. Model Target Evaluation:   eval={model_eval.id}  run={model_run.id}")
print(f"3. Agent Target Evaluation:   eval={agent_eval.id}  run={agent_eval_run.id}")
print(f"4. Agent Response Evaluation: eval={resp_eval.id}  run={resp_eval_run.id}")
print("\nAll evaluations are preserved for inspection in the Foundry portal.")
