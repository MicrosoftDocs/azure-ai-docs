"""Batch evaluation harness (placeholder metrics).
[TO VERIFY] Replace heuristic scoring with official evaluation SDK calls.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from .config import settings

try:
    from azure.identity import DefaultAzureCredential  # type: ignore
    from azure.ai.projects import AIProjectClient  # [TO VERIFY]
except Exception:  # pragma: no cover
    DefaultAzureCredential = object  # type: ignore
    AIProjectClient = object  # type: ignore

EVAL_FILE = Path(__file__).parent.parent.parent / "assets" / "eval_questions.jsonl"


def groundedness_score(response: str) -> float:
    # Placeholder: naive heuristic
    return 1.0 if len(response.split()) > 3 else 0.0


def run_eval(agent_id: str):  # [TO VERIFY threading / run APIs]
    credential = DefaultAzureCredential()
    client = AIProjectClient(endpoint=settings.project_endpoint, credential=credential)
    rows = []
    for line in EVAL_FILE.read_text().splitlines():
        record = json.loads(line)
        try:
            thread = client.threads.create()  # [TO VERIFY]
            client.messages.create(thread_id=thread.id, role="user", content=record["question"])  # [TO VERIFY]
            run = client.runs.create(thread_id=thread.id, assistant_id=agent_id)  # [TO VERIFY]
            # Poll (simplistic)
            for _ in range(60):
                status_obj = client.runs.get(thread_id=thread.id, run_id=run.id)  # [TO VERIFY]
                status = getattr(status_obj, "status", None)
                if status in {"succeeded", "failed", "completed"}:
                    break
                time.sleep(1)
            messages = client.messages.list(thread_id=thread.id)  # [TO VERIFY]
            final = getattr(messages[-1], "content", "") if messages else ""
        except Exception as e:  # noqa: BLE001
            final = f"[EVAL ERROR] {e}"
        rows.append({
            "id": record["id"],
            "question": record["question"],
            "response": final,
            "groundedness": groundedness_score(final),
        })
    return rows


def main():
    settings.validate()
    agent_id = "[TO VERIFY_AGENT_ID]"  # Replace with dynamic retrieval or parameter
    results = run_eval(agent_id)
    for r in results:
        print(r)


if __name__ == "__main__":  # pragma: no cover
    main()
