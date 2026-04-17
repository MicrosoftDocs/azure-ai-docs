---
title: Audit, rebuild, and validate your Prompt Flow workflow in Microsoft Agent Framework
titleSuffix: Azure Machine Learning
description: Export your Prompt Flow, re-implement it with Microsoft Agent Framework WorkflowBuilder and Executor classes, and validate output parity using the Azure AI Evaluation SDK.
author: scottpolly
ms.author: scottpolly
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
ms.date: 04/15/2026
ai-usage: ai-assisted
#CustomerIntent: As a developer migrating from Prompt Flow, I want to rebuild my workflow in Microsoft Agent Framework and validate that the outputs match so that I can migrate with confidence.
---

# Audit, rebuild, and validate your Prompt Flow workflow in Microsoft Agent Framework

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

This article walks you through the first three phases of the Prompt Flow to Microsoft Agent Framework migration: auditing your existing flow, rebuilding it in Agent Framework, and validating output parity. For the migration overview and concept mapping, see [Migrate from Prompt Flow to Microsoft Agent Framework](migrate-prompt-flow-to-agent-framework.md).


## Prerequisites

- Python 3.10 or later.
- An Azure subscription with an Azure OpenAI resource and a deployed chat model.
- Azure CLI installed and authenticated (`az login` completed).
- Install the required packages:

    ```bash
    pip install agent-framework>=1.0.0 azure-ai-evaluation pandas python-dotenv
    ```

- For RAG workflows, also install:

    ```bash
    pip install agent-framework-azure-ai-search
    ```

> [!IMPORTANT]
> The `agent-framework` package (v1.0.0+) is generally available. The `agent-framework-azure-ai-search` package is in **preview**. For the full list of package statuses, see [Package Status](https://github.com/shshubhe/promptflow-migration-guide/blob/main/python/PACKAGE_STATUS.md).

- A `.env` file at your project root with the following variables:

    ```text
    AZURE_OPENAI_API_KEY=<your-key>
    AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<your-deployment>
    ```

- For RAG workflows, add:

    ```text
    AZURE_AI_SEARCH_ENDPOINT=https://<your-search>.search.windows.net
    AZURE_AI_SEARCH_INDEX_NAME=<your-index>
    AZURE_AI_SEARCH_API_KEY=<your-search-key>
    ```

> [!TIP]
> The examples in this article use API keys for simplicity. For production workloads, use `DefaultAzureCredential` from the `azure-identity` package instead. Install with `pip install azure-identity`. See the [Foundry client alternative](https://github.com/shshubhe/promptflow-migration-guide/tree/main/migration-guide/PromptFlow-to-MAF/phase-4-migrate-ops) in the migration samples for a token-based authentication example.

## Audit and map your existing flow

Before writing any Agent Framework code, document what you have.

### Export your flow structure

Run the Prompt Flow CLI to get a full YAML representation of your flow:

```bash
pf flow export --source <your-flow-directory> --output ./flow_export
```

Open `flow_export/flow.dag.yaml`. It lists every node with:

- **type**: `llm`, `python`, or `prompt`
- **inputs**: what data each node receives
- **outputs**: what it passes downstream

Keep this file open while working through the rebuild step.

### Map each node to its Agent Framework equivalent

Walk through each node in your exported YAML and identify the matching Agent Framework pattern:

| Prompt Flow node type | Agent Framework equivalent | Sample pattern |
|---|---|---|
| LLM node | `AzureOpenAIChatClient().as_agent(instructions=...)` inside an `Executor` | [Linear flow](#linear-flow-input-node--llm-node) |
| Python node | Python logic inside an `Executor` `@handler` method | [Python node](#python-code-node) |
| Prompt node | String formatting inside an `Executor` `@handler` | [Python node](#python-code-node) |
| If / conditional node | `.add_edge(source, target, condition=fn)` | [Conditional flow](#conditional-flow) |
| Parallel nodes | `.add_fan_out_edges()` + `.add_fan_in_edges()` | [Parallel flow](#parallel-flow-with-fan-outfan-in) |
| Embed Text + Vector Lookup | `AzureAISearchContextProvider` via `context_providers=[...]` | [RAG pipeline](#rag-pipeline) |
| Python tool node | Python function registered via `tools=[fn]` | [Function tools](#function-tools) |
| Multi-step specialist routing | Multi-agent with conditional edges | [Multi-agent handoff](#multi-agent-handoff) |

### Map connections to environment variables

Prompt Flow connections become environment variables in Agent Framework. The `AzureOpenAIChatClient` reads `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` automatically from the environment.

**Checklist before rebuilding:**

- [ ] `flow.dag.yaml` exported and reviewed.
- [ ] Every node has a mapped Agent Framework equivalent.
- [ ] `.env` file populated.
- [ ] You know which sample patterns match your flow.

## Rebuild in Agent Framework

Every Agent Framework workflow follows the same three-step pattern:

1. **Define Executors.** Create one class per logical step, each with a `@handler` method.
1. **Build the workflow.** Connect executors with `WorkflowBuilder` and `.add_edge()`.
1. **Run.** Call `await workflow.run(input)` and read output from `result.get_outputs()`.

The following samples each cover a specific Prompt Flow pattern. Use the mapping table from the previous section to identify which patterns apply to your flow, then jump to the relevant subsection:

- [Linear flow](#linear-flow-input-node--llm-node): Input + LLM
- [Python code node](#python-code-node): Custom logic
- [Conditional flow](#conditional-flow): If/else routing
- [Parallel flow](#parallel-flow-with-fan-outfan-in): Fan-out/fan-in
- [RAG pipeline](#rag-pipeline): Embed + search + LLM
- [Function tools](#function-tools): Python tool nodes
- [Multi-agent handoff](#multi-agent-handoff): Specialist routing

### Linear flow: Input node + LLM node

This sample migrates the simplest Prompt Flow pattern: an Input node connected to an LLM node.

```python
"""Prompt Flow equivalent: [Input node] --> [LLM node]"""

import asyncio

from dotenv import load_dotenv
from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()


class InputExecutor(Executor):
    """Replaces the Prompt Flow Input node."""

    @handler
    async def receive(self, question: str, ctx: WorkflowContext[str]) -> None:
        await ctx.send_message(question.strip())


class LLMExecutor(Executor):
    """Replaces the Prompt Flow LLM node."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agent = AzureOpenAIChatClient().as_agent(
            name="QAAgent",
            instructions="You are a helpful assistant. Answer concisely.",
        )

    @handler
    async def call_llm(
        self, question: str, ctx: WorkflowContext[Never, str]
    ) -> None:
        result = await self._agent.run(question)
        await ctx.yield_output(result)


workflow = (
    WorkflowBuilder(name="LinearWorkflow")
    .register_executor(lambda: InputExecutor(id="input"), name="Input")
    .register_executor(lambda: LLMExecutor(id="llm"), name="LLM")
    .add_edge("Input", "LLM")
    .set_start_executor("Input")
    .build()
)


async def main():
    result = await workflow.run(
        "What is retrieval-augmented generation?"
    )
    print(result.get_outputs()[0])


if __name__ == "__main__":
    asyncio.run(main())
```

Key points:

- `WorkflowContext[str]` sends a `str` downstream via `ctx.send_message()`.
- `WorkflowContext[Never, str]` yields the final workflow output via `ctx.yield_output()`.
- `AzureOpenAIChatClient` reads credentials from environment variables automatically.

> [!TIP]
> Save each sample as a standalone `.py` file and run it to verify. You should see a concise answer printed to stdout. If you get an error, check the [Troubleshooting](#troubleshooting) section.

### Python code node

Custom Python logic goes directly inside the `@handler` method. No separate YAML snippet or file registration is needed.

```python
"""Prompt Flow equivalent: Python node with custom logic"""

import asyncio

from dotenv import load_dotenv
from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler

load_dotenv()


class TextCleanerExecutor(Executor):
    """Replaces the Prompt Flow Python node."""

    @handler
    async def clean(
        self, text: str, ctx: WorkflowContext[str]
    ) -> None:
        cleaned = text.strip().upper()
        await ctx.send_message(cleaned)


class OutputExecutor(Executor):
    """Terminal executor that yields the final workflow output."""

    @handler
    async def output(
        self, text: str, ctx: WorkflowContext[Never, str]
    ) -> None:
        await ctx.yield_output(text)


workflow = (
    WorkflowBuilder(name="PythonNodeWorkflow")
    .register_executor(
        lambda: TextCleanerExecutor(id="cleaner"), name="Cleaner"
    )
    .register_executor(
        lambda: OutputExecutor(id="output"), name="Output"
    )
    .add_edge("Cleaner", "Output")
    .set_start_executor("Cleaner")
    .build()
)


async def main():
    result = await workflow.run("  hello from prompt flow  ")
    print(result.get_outputs()[0])  # HELLO FROM PROMPT FLOW


if __name__ == "__main__":
    asyncio.run(main())
```

### Conditional flow

Prompt Flow's `If` node maps to condition functions on edges. An edge fires only when the condition returns `True`.

```python
"""Prompt Flow equivalent: activate_config: ${classify.output} == "safe" """

import asyncio
from typing import TypedDict

from dotenv import load_dotenv
from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler

load_dotenv()


class ClassifiedMessage(TypedDict):
    label: str
    text: str


class ClassifyExecutor(Executor):
    """Replace the body with your real classification logic."""

    @handler
    async def classify(
        self, text: str, ctx: WorkflowContext[ClassifiedMessage]
    ) -> None:
        label = "unsafe" if "bad_word" in text.lower() else "safe"
        await ctx.send_message({"label": label, "text": text})


class SafeHandlerExecutor(Executor):
    @handler
    async def handle_safe(
        self, message: ClassifiedMessage,
        ctx: WorkflowContext[Never, str],
    ) -> None:
        await ctx.yield_output(f"Processed: {message['text']}")


class FlaggedHandlerExecutor(Executor):
    @handler
    async def handle_flagged(
        self, message: ClassifiedMessage,
        ctx: WorkflowContext[Never, str],
    ) -> None:
        await ctx.yield_output(f"Flagged for review: {message['text']}")


def is_safe(message: ClassifiedMessage) -> bool:
    return message["label"] == "safe"


def is_unsafe(message: ClassifiedMessage) -> bool:
    return message["label"] == "unsafe"


workflow = (
    WorkflowBuilder(name="ConditionalWorkflow")
    .register_executor(
        lambda: ClassifyExecutor(id="classify"), name="Classify"
    )
    .register_executor(
        lambda: SafeHandlerExecutor(id="safe"), name="SafeHandler"
    )
    .register_executor(
        lambda: FlaggedHandlerExecutor(id="flagged"),
        name="FlaggedHandler",
    )
    .add_edge("Classify", "SafeHandler", condition=is_safe)
    .add_edge("Classify", "FlaggedHandler", condition=is_unsafe)
    .set_start_executor("Classify")
    .build()
)
```

Key points:

- Condition functions receive the exact message passed to `ctx.send_message()`.
- Use named functions, not lambdas, for readability and testability.
- Two edges leave `ClassifyExecutor`, but only one fires per run.

### Parallel flow with fan-out/fan-in

Fan-out broadcasts one message to multiple executors concurrently. Fan-in waits for all upstream executors before proceeding.

```python
"""Prompt Flow equivalent:
[Dispatch] --> [NodeA] --> [Merge]
           --> [NodeB] --> [Merge]
"""

import asyncio

from dotenv import load_dotenv
from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler

load_dotenv()


class DispatchExecutor(Executor):
    @handler
    async def dispatch(
        self, text: str, ctx: WorkflowContext[str]
    ) -> None:
        await ctx.send_message(text)


class PathAExecutor(Executor):
    @handler
    async def process_a(
        self, text: str, ctx: WorkflowContext[str]
    ) -> None:
        await ctx.send_message(f"PathA: {text.upper()}")


class PathBExecutor(Executor):
    @handler
    async def process_b(
        self, text: str, ctx: WorkflowContext[str]
    ) -> None:
        await ctx.send_message(f"PathB: {text[::-1]}")


class AggregatorExecutor(Executor):
    """Fan-in delivers all upstream results as list[str]."""

    @handler
    async def aggregate(
        self, results: list[str], ctx: WorkflowContext[Never, str]
    ) -> None:
        combined = " | ".join(results)
        await ctx.yield_output(combined)


workflow = (
    WorkflowBuilder(name="ParallelWorkflow")
    .register_executor(
        lambda: DispatchExecutor(id="dispatch"), name="Dispatch"
    )
    .register_executor(
        lambda: PathAExecutor(id="path_a"), name="PathA"
    )
    .register_executor(
        lambda: PathBExecutor(id="path_b"), name="PathB"
    )
    .register_executor(
        lambda: AggregatorExecutor(id="aggregate"), name="Aggregate"
    )
    .add_fan_out_edges("Dispatch", ["PathA", "PathB"])
    .add_fan_in_edges(["PathA", "PathB"], "Aggregate")
    .set_start_executor("Dispatch")
    .build()
)
```

Key points:

- Every executor in `add_fan_out_edges()` must also appear in `add_fan_in_edges()`, or the aggregator fires early with a partial result.
- The fan-in handler's parameter must be typed as `list[str]` (or `list[T]`), not a single `str`.
- Result order matches the declaration order in `add_fan_in_edges()`.

### RAG pipeline

`AzureAISearchContextProvider` replaces three separate Prompt Flow nodes (Embed Text, Vector DB Lookup, LLM) in a single configuration.

```python
"""Prompt Flow equivalent:
[Embed Text] --> [Vector DB Lookup] --> [LLM node]
"""

import asyncio
import os

from dotenv import load_dotenv
from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_azure_ai_search import AzureAISearchContextProvider

load_dotenv()

search_provider = AzureAISearchContextProvider(
    endpoint=os.environ["AZURE_AI_SEARCH_ENDPOINT"],
    index_name=os.environ["AZURE_AI_SEARCH_INDEX_NAME"],
    api_key=os.environ["AZURE_AI_SEARCH_API_KEY"],
)


class RAGExecutor(Executor):
    """Replaces Embed Text, Vector DB Lookup, and LLM nodes combined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agent = AzureOpenAIChatClient().as_agent(
            name="DocQAAgent",
            instructions=(
                "You are a precise document Q&A assistant. "
                "Answer using ONLY the retrieved context provided. "
                "If the answer is not in the context, say "
                "'I don't know'."
            ),
            context_providers=[search_provider],
        )

    @handler
    async def answer(
        self, question: str, ctx: WorkflowContext[Never, str]
    ) -> None:
        result = await self._agent.run(question)
        await ctx.yield_output(result)


workflow = (
    WorkflowBuilder(name="RAGWorkflow")
    .register_executor(lambda: RAGExecutor(id="rag"), name="RAG")
    .set_start_executor("RAG")
    .build()
)
```

The `context_providers` parameter handles embedding generation and vector similarity search automatically before every `agent.run()` call.

### Function tools

Python functions registered via `tools=[]` replace Prompt Flow's Python tool nodes. The agent decides autonomously which tools to call based on the user question.

```python
"""Prompt Flow equivalent: [LLM node] --> [Python tool node]"""

import asyncio

from dotenv import load_dotenv
from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()


def get_order_status(order_id: str) -> str:
    """Look up the status of a customer order by order ID.

    Args:
        order_id: The unique order identifier.

    Returns:
        A string describing the current order status.
    """
    mock_orders = {
        "ORD-001": "Shipped, expected delivery 9 Apr 2026",
        "ORD-002": "Processing, not yet dispatched",
        "ORD-003": "Delivered on 3 Apr 2026",
    }
    return mock_orders.get(order_id, f"Order {order_id} not found.")


def get_refund_policy() -> str:
    """Return the company refund policy.

    Returns:
        A string describing the refund policy.
    """
    return (
        "Refunds are accepted within 30 days of purchase "
        "with proof of receipt."
    )


class ToolAgentExecutor(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agent = AzureOpenAIChatClient().as_agent(
            name="SupportAgent",
            instructions=(
                "You are a customer support assistant. "
                "Use the available tools to answer questions "
                "about orders and refunds. "
                "Always use a tool if the answer can be "
                "looked up. Do not guess."
            ),
            tools=[get_order_status, get_refund_policy],
        )

    @handler
    async def run(
        self, question: str, ctx: WorkflowContext[Never, str]
    ) -> None:
        result = await self._agent.run(question)
        await ctx.yield_output(result)


workflow = (
    WorkflowBuilder(name="FunctionToolsWorkflow")
    .register_executor(
        lambda: ToolAgentExecutor(id="tool_agent"), name="ToolAgent"
    )
    .set_start_executor("ToolAgent")
    .build()
)
```

> [!TIP]
> Tool function docstrings drive agent behavior. The agent uses the docstring to decide when and how to call each function. Missing or vague docstrings lead to unreliable tool use.

### Multi-agent handoff

A triage agent classifies input and routes it to specialist agents using conditional edges.

```python
"""Prompt Flow equivalent:
[Classify node] --> [SpecialistA LLM] (if billing)
                --> [SpecialistB LLM] (if technical)
"""

import asyncio

from dotenv import load_dotenv
from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()

# Share a single client across all agents.
_client = AzureOpenAIChatClient()

triage_agent = _client.as_agent(
    name="TriageAgent",
    instructions=(
        "You are a triage assistant. Classify the user message as "
        "either 'billing' or 'technical'. Reply with exactly one "
        "word: billing or technical."
    ),
)

billing_agent = _client.as_agent(
    name="BillingAgent",
    instructions=(
        "You are a billing support specialist. Answer questions "
        "about invoices, payments, and subscriptions concisely."
    ),
)

technical_agent = _client.as_agent(
    name="TechnicalAgent",
    instructions=(
        "You are a technical support specialist. Answer questions "
        "about product features, errors, and configuration concisely."
    ),
)


class TriageExecutor(Executor):
    """Classifies and routes with a tagged message: 'category||question'."""

    @handler
    async def triage(
        self, question: str, ctx: WorkflowContext[str]
    ) -> None:
        result = await triage_agent.run(question)
        category = result.strip().lower()
        if category not in ("billing", "technical"):
            category = "technical"
        await ctx.send_message(f"{category}||{question}")


class BillingExecutor(Executor):
    @handler
    async def handle(
        self, tagged: str, ctx: WorkflowContext[Never, str]
    ) -> None:
        _, question = tagged.split("||", 1)
        result = await billing_agent.run(question)
        await ctx.yield_output(result)


class TechnicalExecutor(Executor):
    @handler
    async def handle(
        self, tagged: str, ctx: WorkflowContext[Never, str]
    ) -> None:
        _, question = tagged.split("||", 1)
        result = await technical_agent.run(question)
        await ctx.yield_output(result)


def is_billing(message: str) -> bool:
    return message.startswith("billing||")


def is_technical(message: str) -> bool:
    return message.startswith("technical||")


workflow = (
    WorkflowBuilder(name="MultiAgentHandoffWorkflow")
    .register_executor(
        lambda: TriageExecutor(id="triage"), name="Triage"
    )
    .register_executor(
        lambda: BillingExecutor(id="billing"), name="Billing"
    )
    .register_executor(
        lambda: TechnicalExecutor(id="technical"), name="Technical"
    )
    .add_edge("Triage", "Billing", condition=is_billing)
    .add_edge("Triage", "Technical", condition=is_technical)
    .set_start_executor("Triage")
    .build()
)
```

Key points:

- Share a single `AzureOpenAIChatClient()` instance across multiple agents. Creating separate clients wastes connection resources.
- The tagged string pattern (`"category||payload"`) lets condition functions route on the prefix while downstream executors extract the original question.

## Validate output parity

Run your captured Prompt Flow outputs and the new Agent Framework workflow against the same test inputs, then score semantic similarity using the Azure AI Evaluation SDK.

### Prepare test inputs

1. Capture 20 to 30 real queries from your Prompt Flow application.
1. Save them as a CSV file with columns `question` and `pf_output`:

    ```csv
    question,pf_output
    What is the refund policy?,Refunds are accepted within 30 days with proof of receipt.
    How do I reset my password?,Go to Settings > Security > Reset Password.
    ```

### Run the parity check

```python
"""Compares Prompt Flow outputs against the new Agent Framework workflow."""

import asyncio
import os

import pandas as pd
from dotenv import load_dotenv
from azure.ai.evaluation import SimilarityEvaluator

load_dotenv()

# Import your rebuilt Agent Framework workflow
from your_workflow_module import workflow

SIMILARITY_THRESHOLD = 3.5


async def run_parity_check():
    model_config = {
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_key": os.environ["AZURE_OPENAI_API_KEY"],
        "azure_deployment": os.environ[
            "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"
        ],
    }

    evaluator = SimilarityEvaluator(
        model_config=model_config, threshold=3
    )

    test_data = pd.read_csv("test_inputs.csv")
    results = []

    for _, row in test_data.iterrows():
        question = row["question"]
        pf_answer = row["pf_output"]

        maf_result = await workflow.run(question)
        maf_answer = maf_result.get_outputs()[0]

        score_dict = await asyncio.to_thread(
            evaluator,
            query=question,
            response=maf_answer,
            ground_truth=pf_answer,
        )
        results.append({
            "question": question,
            "pf_output": pf_answer,
            "maf_output": maf_answer,
            "similarity": score_dict["similarity"],
        })

    df = pd.DataFrame(results)
    mean_score = df["similarity"].mean()
    print(f"\nMean similarity: {mean_score:.2f} / 5.0")

    regressions = df[df["similarity"] < SIMILARITY_THRESHOLD]
    if regressions.empty:
        print("All outputs meet the quality threshold.")
    else:
        print(f"\n{len(regressions)} answer(s) to review:")
        print(
            regressions[["question", "similarity"]]
            .to_string(index=False)
        )

    df.to_csv("parity_results.csv", index=False)
    print(f"\nFull results saved to parity_results.csv")


if __name__ == "__main__":
    asyncio.run(run_parity_check())
```

> [!IMPORTANT]
> Use `query=`, `response=`, and `ground_truth=` as keyword arguments to the evaluator. Using incorrect kwargs causes the evaluator to compare the wrong fields and score near zero.

### Interpret scores

| Score range | Meaning | Action |
|---|---|---|
| < 3.5 | Outputs diverge | Check for missing prompt context or unmigrated nodes. |
| 3.5 to 4.5 | Minor phrasing differences | Generally acceptable. |
| > 4.5 | Strong semantic match | Safe to proceed to deployment. |

Don't proceed to deployment until mean similarity is consistently ≥ 3.5.

## Troubleshooting

### `ModuleNotFoundError: No module named 'agent_framework'`

The package isn't installed or a pre-release version is conflicting. Uninstall and reinstall cleanly:

```bash
pip uninstall agent-framework agent-framework-core agent-framework-foundry -y
pip install agent-framework>=1.0.0
```

### `401 Unauthorized` when calling Azure OpenAI

Check:

1. Your `.env` file exists at the project root and is populated.
1. `load_dotenv()` is called before any client is created.
1. `AZURE_OPENAI_ENDPOINT` ends with `.openai.azure.com/` (trailing slash matters).
1. `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` matches the exact deployment name in the Azure portal (case-sensitive).

### `workflow.run()` returns a result but `get_outputs()` is empty

The terminal executor isn't calling `ctx.yield_output()`. Check:

1. The `WorkflowContext` type annotation includes a yield type: `WorkflowContext[Never, str]`.
1. `ctx.yield_output()` is actually called (no early returns or unhandled exceptions).
1. The executor is connected to the workflow graph via `add_edge()`.

### `TypeError` on `Message(text=...)`

The `text=` parameter was removed in Agent Framework 1.0. Use `contents=[...]` instead:

```python
# Correct
message = Message(role="user", contents=["Hello"])

# Incorrect (raises TypeError)
message = Message(role="user", text="Hello")
```

### Similarity scores are unexpectedly low (< 2.0)

Check that you're using the correct kwargs:

```python
# Correct
evaluator(query=question, response=maf_answer, ground_truth=pf_answer)

# Incorrect (compares wrong fields)
evaluator(answer=maf_answer, ground_truth=pf_answer)
```

Also verify that the `pf_output` column in your CSV contains the actual text output from your Prompt Flow app, not the input question.

## Related content

- [Migrate from Prompt Flow to Microsoft Agent Framework](migrate-prompt-flow-to-agent-framework.md)
- [Deploy and operate your migrated Agent Framework workflow](how-to-deploy-migrated-agent-framework-workflow.md)
- [Microsoft Agent Framework workflows documentation](/agent-framework/workflows/)
- [Azure AI Evaluation SDK reference](/python/api/overview/azure/ai-evaluation-readme)
- [PromptFlow-to-MAF migration samples](https://github.com/shshubhe/promptflow-migration-guide/tree/main/migration-guide/PromptFlow-to-MAF)
