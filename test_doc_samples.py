"""Test all code samples from cloud-evaluation.md against live endpoint."""
import os
import sys
import time
import json
import subprocess
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
    SourceFileID,
)

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment_name = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=endpoint, credential=credential)
client = project_client.get_openai_client()

# Parse endpoint for cURL
# https://<account>.services.ai.azure.com/api/projects/<project>
parts = endpoint.replace("https://", "").split("/")
ACCOUNT = parts[0].split(".services.ai.azure.com")[0]
PROJECT = parts[-1]

# Get token for cURL using Python credential (more reliable than az cli in venv)
from azure.identity import AzureCliCredential
_cred = AzureCliCredential()
TOKEN = _cred.get_token("https://ai.azure.com/.default").token
print(f"Token obtained: {TOKEN[:20]}...")

created_evals = []
results = {}

def wait_for_run(client, eval_id, run_id, label):
    for _ in range(60):
        run = client.evals.runs.retrieve(run_id=run_id, eval_id=eval_id)
        if run.status in ("completed", "failed"):
            print(f"  [{label}] status={run.status} results={run.result_counts}")
            return run
        time.sleep(5)
    print(f"  [{label}] Timed out")
    return None

def curl_post(path, data):
    """POST to the evaluation API via cURL."""
    import tempfile
    url = f"https://{ACCOUNT}.services.ai.azure.com/api/projects/{PROJECT}/openai/{path}?api-version=v1"
    # Write JSON to temp file to avoid shell escaping issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        tmpfile = f.name
    try:
        result = subprocess.run(
            f'curl --silent --request POST --url "{url}" --header "Authorization: Bearer {TOKEN}" --header "Content-Type: application/json" --data @{tmpfile}',
            capture_output=True, text=True, shell=True
        )
        try:
            return json.loads(result.stdout)
        except:
            print(f"  cURL error: {result.stdout[:200]}")
            return None
    finally:
        os.unlink(tmpfile)

def cleanup():
    for eid in created_evals:
        try:
            client.evals.delete(eval_id=eid)
        except:
            pass

# ============================================================
# TEST 1: Dataset Evaluation (Python)
# ============================================================
print("\n=== TEST 1: Dataset Evaluation (Python) ===")
try:
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
        include_sample_schema=True,
    )

    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "coherence",
            "evaluator_name": "builtin.coherence",
            "initialization_parameters": {"deployment_name": model_deployment_name},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "violence",
            "evaluator_name": "builtin.violence",
            "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
            "initialization_parameters": {"deployment_name": model_deployment_name},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "f1",
            "evaluator_name": "builtin.f1_score",
        },
    ]

    eval_object = client.evals.create(
        name="doc-test-dataset",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )
    created_evals.append(eval_object.id)

    eval_run = client.evals.runs.create(
        eval_id=eval_object.id,
        name="dataset-run",
        data_source=CreateEvalJSONLRunDataSourceParam(
            type="jsonl",
            source=SourceFileContent(
                type="file_content",
                content=[
                    SourceFileContentContent(item={"query": "What is the capital of France?", "response": "Paris.", "ground_truth": "Paris"}),
                    SourceFileContentContent(item={"query": "What is 2+2?", "response": "4", "ground_truth": "4"}),
                ],
            ),
        ),
    )
    run = wait_for_run(client, eval_object.id, eval_run.id, "Dataset-Py")
    results["dataset-python"] = "PASS" if run and run.status == "completed" else "FAIL"
    print(f"  ✓ {results['dataset-python']}")
except Exception as e:
    results["dataset-python"] = f"FAIL: {e}"
    print(f"  ✗ {results['dataset-python']}")

# ============================================================
# TEST 2: Dataset Evaluation (cURL)
# ============================================================
print("\n=== TEST 2: Dataset Evaluation (cURL) ===")
try:
    resp = curl_post("evals", {
        "name": "curl-test-dataset",
        "data_source_config": {
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "response": {"type": "string"},
                    "ground_truth": {"type": "string"}
                },
                "required": []
            },
            "include_sample_schema": True
        },
        "testing_criteria": [
            {
                "type": "azure_ai_evaluator",
                "name": "coherence",
                "evaluator_name": "builtin.coherence",
                "initialization_parameters": {"deployment_name": model_deployment_name}
            }
        ]
    })
    assert resp and "id" in resp, f"Create eval failed: {resp}"
    eval_id = resp["id"]
    created_evals.append(eval_id)
    print(f"  Eval created: {eval_id}")

    run_resp = curl_post(f"evals/{eval_id}/runs", {
        "name": "dataset-run",
        "data_source": {
            "type": "jsonl",
            "source": {
                "type": "file_content",
                "content": [
                    {"item": {"query": "What is the capital of France?", "response": "Paris.", "ground_truth": "Paris"}},
                    {"item": {"query": "What is 2+2?", "response": "4", "ground_truth": "4"}}
                ]
            }
        }
    })
    assert run_resp and "id" in run_resp, f"Create run failed: {run_resp}"
    print(f"  Run created: {run_resp['id']} status: {run_resp.get('status')}")
    results["dataset-curl"] = "PASS"
    print(f"  ✓ {results['dataset-curl']}")
except Exception as e:
    results["dataset-curl"] = f"FAIL: {e}"
    print(f"  ✗ {results['dataset-curl']}")

# ============================================================
# TEST 3: Model Target (Python)
# ============================================================
print("\n=== TEST 3: Model Target (Python) ===")
try:
    input_messages = {
        "type": "template",
        "template": [
            {"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}}
        ]
    }
    target = {
        "type": "azure_ai_model",
        "model": model_deployment_name,
        "sampling_params": {"top_p": 1.0, "max_completion_tokens": 2048},
    }

    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
        include_sample_schema=True,
    )
    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "coherence",
            "evaluator_name": "builtin.coherence",
            "initialization_parameters": {"deployment_name": model_deployment_name},
            "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "violence",
            "evaluator_name": "builtin.violence",
            "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"},
        },
    ]
    eval_object = client.evals.create(name="doc-test-model-target", data_source_config=data_source_config, testing_criteria=testing_criteria)
    created_evals.append(eval_object.id)

    data_source = {
        "type": "azure_ai_target_completions",
        "source": {"type": "file_content", "content": [{"item": {"query": "What is the capital of France?"}}, {"item": {"query": "How do I reverse a string in Python?"}}]},
        "input_messages": input_messages,
        "target": target,
    }
    eval_run = client.evals.runs.create(eval_id=eval_object.id, name="model-target-run", data_source=data_source)
    run = wait_for_run(client, eval_object.id, eval_run.id, "ModelTarget-Py")
    results["model-target-python"] = "PASS" if run and run.status == "completed" else "FAIL"
    print(f"  ✓ {results['model-target-python']}")
except Exception as e:
    results["model-target-python"] = f"FAIL: {e}"
    print(f"  ✗ {results['model-target-python']}")

# ============================================================
# TEST 4: Model Target (cURL)
# ============================================================
print("\n=== TEST 4: Model Target (cURL) ===")
try:
    resp = curl_post("evals", {
        "name": "curl-test-model-target",
        "data_source_config": {
            "type": "custom",
            "item_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            "include_sample_schema": True
        },
        "testing_criteria": [{
            "type": "azure_ai_evaluator",
            "name": "violence",
            "evaluator_name": "builtin.violence",
            "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"}
        }]
    })
    assert resp and "id" in resp, f"Create eval failed: {resp}"
    eval_id = resp["id"]
    created_evals.append(eval_id)
    print(f"  Eval created: {eval_id}")

    run_resp = curl_post(f"evals/{eval_id}/runs", {
        "name": "model-target-run",
        "data_source": {
            "type": "azure_ai_target_completions",
            "source": {"type": "file_content", "content": [{"item": {"query": "What is the capital of France?"}}]},
            "input_messages": {"type": "template", "template": [{"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}}]},
            "target": {"type": "azure_ai_model", "model": model_deployment_name, "sampling_params": {"top_p": 1.0, "max_completion_tokens": 2048}}
        }
    })
    assert run_resp and "id" in run_resp, f"Create run failed: {run_resp}"
    print(f"  Run created: {run_resp['id']} status: {run_resp.get('status')}")
    results["model-target-curl"] = "PASS"
    print(f"  ✓ {results['model-target-curl']}")
except Exception as e:
    results["model-target-curl"] = f"FAIL: {e}"
    print(f"  ✗ {results['model-target-curl']}")

# ============================================================
# TEST 5: Agent Target (Python)
# ============================================================
print("\n=== TEST 5: Agent Target (Python) ===")
try:
    from azure.ai.agents import AgentsClient
    agents_client = AgentsClient(endpoint=endpoint, credential=credential)
    agent = agents_client.create_agent(model=model_deployment_name, name="doc-test-agent", instructions="You are a helpful assistant.")
    print(f"  Agent: {agent.id}")

    input_messages = {
        "type": "template",
        "template": [
            {"type": "message", "role": "developer", "content": {"type": "input_text", "text": "You are a helpful assistant. Answer clearly and safely."}},
            {"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}},
        ]
    }
    agent_target = {"type": "azure_ai_agent", "name": agent.id, "version": "1"}

    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
        include_sample_schema=True,
    )
    testing_criteria = [
        {"type": "azure_ai_evaluator", "name": "task_adherence", "evaluator_name": "builtin.task_adherence",
         "initialization_parameters": {"deployment_name": model_deployment_name},
         "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_items}}"}},
        {"type": "azure_ai_evaluator", "name": "violence", "evaluator_name": "builtin.violence",
         "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"}},
    ]
    eval_object = client.evals.create(name="doc-test-agent-target", data_source_config=data_source_config, testing_criteria=testing_criteria)
    created_evals.append(eval_object.id)

    data_source = {
        "type": "azure_ai_target_completions",
        "source": {"type": "file_content", "content": [{"item": {"query": "What is the capital of France?"}}]},
        "input_messages": input_messages,
        "target": agent_target,
    }
    eval_run = client.evals.runs.create(eval_id=eval_object.id, name="agent-target-run", data_source=data_source)
    run = wait_for_run(client, eval_object.id, eval_run.id, "AgentTarget-Py")
    results["agent-target-python"] = "PASS" if run and run.status == "completed" else "FAIL"
    agents_client.delete_agent(agent.id)
    print(f"  ✓ {results['agent-target-python']}")
except Exception as e:
    results["agent-target-python"] = f"FAIL: {e}"
    print(f"  ✗ {results['agent-target-python']}")

# ============================================================
# TEST 6: Agent Target (cURL)
# ============================================================
print("\n=== TEST 6: Agent Target (cURL) ===")
try:
    from azure.ai.agents import AgentsClient
    agents_client = AgentsClient(endpoint=endpoint, credential=credential)
    agent = agents_client.create_agent(model=model_deployment_name, name="doc-test-agent-curl", instructions="You are a helpful assistant.")
    
    resp = curl_post("evals", {
        "name": "curl-test-agent-target",
        "data_source_config": {
            "type": "custom",
            "item_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            "include_sample_schema": True
        },
        "testing_criteria": [{
            "type": "azure_ai_evaluator", "name": "violence", "evaluator_name": "builtin.violence",
            "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"}
        }]
    })
    assert resp and "id" in resp, f"Create eval failed: {resp}"
    eval_id = resp["id"]
    created_evals.append(eval_id)

    run_resp = curl_post(f"evals/{eval_id}/runs", {
        "name": "agent-target-run",
        "data_source": {
            "type": "azure_ai_target_completions",
            "source": {"type": "file_content", "content": [{"item": {"query": "What is the capital of France?"}}]},
            "input_messages": {"type": "template", "template": [
                {"type": "message", "role": "developer", "content": {"type": "input_text", "text": "You are a helpful assistant."}},
                {"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}}
            ]},
            "target": {"type": "azure_ai_agent", "name": agent.id, "version": "1"}
        }
    })
    assert run_resp and "id" in run_resp, f"Create run failed: {run_resp}"
    print(f"  Run created: {run_resp['id']} status: {run_resp.get('status')}")
    results["agent-target-curl"] = "PASS"
    agents_client.delete_agent(agent.id)
    print(f"  ✓ {results['agent-target-curl']}")
except Exception as e:
    results["agent-target-curl"] = f"FAIL: {e}"
    print(f"  ✗ {results['agent-target-curl']}")

# ============================================================
# TEST 7: Agent Response (Python) - eval creation only
# ============================================================
print("\n=== TEST 7: Agent Response (Python - eval create) ===")
try:
    data_source_config = {"type": "azure_ai_source", "scenario": "responses"}
    testing_criteria = [
        {"type": "azure_ai_evaluator", "name": "coherence", "evaluator_name": "builtin.coherence",
         "initialization_parameters": {"deployment_name": model_deployment_name}},
        {"type": "azure_ai_evaluator", "name": "violence", "evaluator_name": "builtin.violence"},
    ]
    eval_object = client.evals.create(name="doc-test-agent-response", data_source_config=data_source_config, testing_criteria=testing_criteria)
    created_evals.append(eval_object.id)
    print(f"  Eval created: {eval_object.id}")
    results["agent-response-python"] = "PASS (eval created, run needs real resp_ids)"
    print(f"  ✓ {results['agent-response-python']}")
except Exception as e:
    results["agent-response-python"] = f"FAIL: {e}"
    print(f"  ✗ {results['agent-response-python']}")

# ============================================================
# TEST 8: Agent Response (cURL) - eval creation only
# ============================================================
print("\n=== TEST 8: Agent Response (cURL - eval create) ===")
try:
    resp = curl_post("evals", {
        "name": "curl-test-agent-response",
        "data_source_config": {"type": "azure_ai_source", "scenario": "responses"},
        "testing_criteria": [
            {"type": "azure_ai_evaluator", "name": "violence", "evaluator_name": "builtin.violence"}
        ]
    })
    assert resp and "id" in resp, f"Create eval failed: {resp}"
    created_evals.append(resp["id"])
    print(f"  Eval created: {resp['id']}")
    results["agent-response-curl"] = "PASS (eval created)"
    print(f"  ✓ {results['agent-response-curl']}")
except Exception as e:
    results["agent-response-curl"] = f"FAIL: {e}"
    print(f"  ✗ {results['agent-response-curl']}")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
for k, v in results.items():
    icon = "✓" if "PASS" in v else "✗"
    print(f"  {icon} {k}: {v}")

cleanup()
print("\nDone!")
