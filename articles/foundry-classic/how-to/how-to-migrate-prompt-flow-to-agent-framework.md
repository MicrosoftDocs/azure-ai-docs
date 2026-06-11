---
title: Audit, rebuild, and validate your Prompt Flow workflow in Microsoft Agent Framework for Foundry (classic)
titleSuffix: Microsoft Foundry
description: Export your Prompt Flow, re-implement it with Microsoft Agent Framework WorkflowBuilder and Executor classes, and validate output parity using the Azure AI Evaluation SDK.
author: scottpolly
ms.author: scottpolly
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 04/15/2026
ai-usage: ai-assisted
#CustomerIntent: As a developer migrating from Prompt Flow on Microsoft Foundry, I want to rebuild my workflow in Microsoft Agent Framework and validate that the outputs match so that I can migrate with confidence.
---

# Audit, rebuild, and validate your Prompt Flow workflow in Microsoft Agent Framework for Foundry (classic)

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

This article walks you through the first three phases of the Prompt Flow to Microsoft Agent Framework migration for Microsoft Foundry users: auditing your existing flow, rebuilding it in Agent Framework, and validating output parity. For the migration overview and concept mapping, see [Migrate from Prompt Flow to Microsoft Agent Framework](prompt-flow-migration-overview.md).

> [!NOTE]
> Microsoft Agent Framework (`agent-framework` 1.0) is generally available as of April 3, 2026. The migration patterns in this article cover the most common Prompt Flow node types.

## Prerequisites

- Python 3.10 or later.
- An Azure subscription with a Foundry project and a deployed chat model.
- Azure CLI installed and authenticated (`az login` completed).
- Install the required packages:

    ```bash
    pip install agent-framework>=1.0.0 agent-framework-foundry \
        azure-ai-evaluation pandas python-dotenv
    ```

- For RAG workflows, also install the required packages:

    ```bash
    pip install agent-framework-azure-ai-search
    ```

- A `.env` file at your project root with the following variables.

    ```text
    FOUNDRY_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com
    FOUNDRY_MODEL=<your-deployment-name>
    ```

- For RAG workflows, add the required variables.

    ```text
    AZURE_AI_SEARCH_ENDPOINT=https://<your-search>.search.windows.net
    AZURE_AI_SEARCH_INDEX_NAME=<your-index>
    AZURE_AI_SEARCH_API_KEY=<your-search-key>
    ```

- For parity validation, add the required variables.

    ```text
    AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
    AZURE_OPENAI_API_KEY=<your-key>
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<your-deployment>
    ```

    > [!NOTE]
    > The `SimilarityEvaluator` from the Azure AI Evaluation SDK requires Azure OpenAI credentials, even when your workflow uses `FoundryChatClient`.

## Audit and map your existing flow

Before writing any Agent Framework code, document what you have.

### Export your flow structure

Run the Prompt Flow CLI to export your flow:

```bash
pf flow build --source <your-flow-directory> --output ./flow_export --format docker
```

Open `flow_export/flow/flow.dag.yaml`. It lists every node with:

- **type**: `llm`, `python`, or `prompt`
- **inputs**: what data each node receives
- **outputs**: what it passes downstream

Keep this file open while working through the rebuild step.

### Map each node to its Agent Framework equivalent

Walk through each node in your exported YAML and identify the matching Agent Framework pattern:

| Prompt Flow node type | Agent Framework equivalent | Sample pattern |
|---|---|---|
| LLM node | `FoundryChatClient().as_agent(instructions=...)` inside an `Executor` | [Linear flow](#linear-flow-input-node--llm-node) |
| Python node | Python logic inside an `Executor` `@handler` method | [Python node](#python-code-node) |
| Prompt node | String formatting inside an `Executor` `@handler` | [Python node](#python-code-node) |
| If / conditional node | `.add_edge(source_exec, target_exec, condition=fn)` | [Conditional flow](#conditional-flow) |
| Parallel nodes | `.add_fan_out_edges(source_exec, [targets])` + `.add_fan_in_edges([sources], target_exec)` | [Parallel flow](#parallel-flow-with-fan-out-and-fan-in) |
| Embed Text + Vector Lookup | `AzureAISearchContextProvider` via `context_providers=[...]` | [RAG pipeline](#rag-pipeline) |
| Python tool node | Python function registered via `tools=[fn]` | [Function tools](#function-tools) |
| Multi-step specialist routing | Multi-agent with conditional edges | [Multi-agent handoff](#multi-agent-handoff) |

### Map connections to environment variables

Prompt Flow connections become environment variables in Agent Framework. `FoundryChatClient` reads `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL` from the environment, and uses `DefaultAzureCredential` for authentication.

**Checklist before rebuilding:**

- [ ] `flow.dag.yaml` exported and reviewed.
- [ ] Every node has a mapped Agent Framework equivalent.
- [ ] `.env` file populated.
- [ ] You know which sample patterns match your flow.

## Rebuild in Agent Framework

Every Agent Framework workflow follows the same three-step pattern:

1. **Define Executors.** Create one class per logical step, each with a `@handler` method.
1. **Build the workflow.** Instantiate executors, then wire them with `WorkflowBuilder(start_executor=...)` and `.add_edge()`.
1. **Run.** Call `await workflow.run(input)` and read output from `result.get_outputs()`.

The following samples each cover a specific Prompt Flow pattern. Use the mapping table from the previous section to identify which patterns apply to your flow, then jump to the relevant subsection:

Use only the samples that match your exported flow nodes:

- **Input + LLM only**: [Linear flow](#linear-flow-input-node--llm-node)
- **Custom Python logic**: [Python code node](#python-code-node)
- **If/conditional branching**: [Conditional flow](#conditional-flow)
- **Parallel processing**: [Parallel flow](#parallel-flow-with-fan-out-and-fan-in)
- **Search/retrieval**: [RAG pipeline](#rag-pipeline)
- **Tool calling**: [Function tools](#function-tools)
- **Multi-specialist routing**: [Multi-agent handoff](#multi-agent-handoff)

Start with Linear flow to learn the base pattern, then add only the sections your flow requires.

### Linear flow: Input node + LLM node

This sample migrates the simplest Prompt Flow pattern: an Input node connected to an LLM node.

```python
"""Prompt Flow equivalent: [Input node] --> [LLM node]"""

import asyncio
import os

from dotenv import load_dotenv
from typing_extensions import Never
from azure.identity import DefaultAzureCredential

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.foundry import FoundryChatClient

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
        self._agent = FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["FOUNDRY_MODEL"],
            credential=DefaultAzureCredential(),
        ).as_agent(
            name="QAAgent",
            instructions="You are a helpful assistant. Answer concisely.",
        )

    @handler
    async def call_llm(
        self, question: str, ctx: WorkflowContext[Never, str]
    ) -> None:
        result = await self._agent.run(question)
        await ctx.yield_output(result)


input_exec = InputExecutor(id="input")
llm_exec = LLMExecutor(id="llm")

workflow = (
    WorkflowBuilder(name="LinearWorkflow", start_executor=input_exec)
    .add_edge(input_exec, llm_exec)
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

Expected output (varies by model):

```output
Retrieval-augmented generation (RAG) is a technique that combines ...
```

Key points:

- `FoundryChatClient` targets Foundry project endpoints (`*.services.ai.azure.com`).
- `DefaultAzureCredential` works for both local development (Azure CLI auth) and production (managed identity).
- `WorkflowContext[str]` sends a `str` downstream via `ctx.send_message()`.
- `WorkflowContext[Never, str]` yields the final workflow output via `ctx.yield_output()`.

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


cleaner = TextCleanerExecutor(id="cleaner")
output = OutputExecutor(id="output")

workflow = (
    WorkflowBuilder(name="PythonNodeWorkflow", start_executor=cleaner)
    .add_edge(cleaner, output)
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


classify = ClassifyExecutor(id="classify")
safe_handler = SafeHandlerExecutor(id="safe")
flagged_handler = FlaggedHandlerExecutor(id="flagged")

workflow = (
    WorkflowBuilder(name="ConditionalWorkflow", start_executor=classify)
    .add_edge(classify, safe_handler, condition=is_safe)
    .add_edge(classify, flagged_handler, condition=is_unsafe)
    .build()
)
```

Expected output for safe input (`"Hello world"`):

```output
Processed: Hello world
```

Expected output for unsafe input (`"bad_word detected"`):

```output
Flagged for review: bad_word detected
```

Key points:

- Condition functions receive the exact message passed to `ctx.send_message()`.
- Use named functions, not lambdas, for readability and testability.
- Two edges leave `ClassifyExecutor`, but only one fires per run.

### Parallel flow with fan-out and fan-in

The fan-out process broadcasts one message to multiple executors concurrently. The fan-in process waits for all upstream executors before proceeding.

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


dispatch = DispatchExecutor(id="dispatch")
path_a = PathAExecutor(id="path_a")
path_b = PathBExecutor(id="path_b")
aggregator = AggregatorExecutor(id="aggregate")

workflow = (
    WorkflowBuilder(name="ParallelWorkflow", start_executor=dispatch)
    .add_fan_out_edges(dispatch, [path_a, path_b])
    .add_fan_in_edges([path_a, path_b], aggregator)
    .build()
)
```

For the input `"hello"`, the expected output is:

```output
PathA: HELLO | PathB: olleh
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
from azure.identity import DefaultAzureCredential

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.foundry import FoundryChatClient
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
        self._agent = FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["FOUNDRY_MODEL"],
            credential=DefaultAzureCredential(),
        ).as_agent(
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


rag_exec = RAGExecutor(id="rag")

workflow = (
    WorkflowBuilder(name="RAGWorkflow", start_executor=rag_exec)
    .build()
)
```

### Function tools

Python functions registered through `tools=[]` replace Prompt Flow's Python tool nodes. The agent decides autonomously which tools to call based on the user question.

```python
"""Prompt Flow equivalent: [LLM node] --> [Python tool node]"""

import asyncio
import os

from dotenv import load_dotenv
from typing_extensions import Never
from azure.identity import DefaultAzureCredential

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.foundry import FoundryChatClient

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
        self._agent = FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["FOUNDRY_MODEL"],
            credential=DefaultAzureCredential(),
        ).as_agent(
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


tool_exec = ToolAgentExecutor(id="tool_agent")

workflow = (
    WorkflowBuilder(name="FunctionToolsWorkflow", start_executor=tool_exec)
    .build()
)
```

> [!TIP]
> Tool function docstrings drive agent behavior. The agent uses the docstring to decide when and how to call each function. Missing or vague docstrings lead to unreliable tool use.

### Multi-agent handoff

A triage agent classifies input and routes it to specialist agents by using conditional edges.

```python
"""Prompt Flow equivalent:
[Classify node] --> [SpecialistA LLM] (if billing)
                --> [SpecialistB LLM] (if technical)
"""

import asyncio
import os

from dotenv import load_dotenv
from typing_extensions import Never
from azure.identity import DefaultAzureCredential

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.foundry import FoundryChatClient

load_dotenv()

# Share a single client across all agents.
_client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ["FOUNDRY_MODEL"],
    credential=DefaultAzureCredential(),
)

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


triage_exec = TriageExecutor(id="triage")
billing_exec = BillingExecutor(id="billing")
technical_exec = TechnicalExecutor(id="technical")

workflow = (
    WorkflowBuilder(name="MultiAgentHandoffWorkflow", start_executor=triage_exec)
    .add_edge(triage_exec, billing_exec, condition=is_billing)
    .add_edge(triage_exec, technical_exec, condition=is_technical)
    .build()
)
```

Key points:

- Share a single `FoundryChatClient()` instance across multiple agents. Creating separate clients wastes connection resources.
- The tagged string pattern (`"category||payload"`) lets condition functions route on the prefix while downstream executors extract the original question.

## Validate output parity

Run your captured Prompt Flow outputs and the new Agent Framework workflow against the same test inputs. Then, score semantic similarity by using the Azure AI Evaluation SDK.

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
> Use `query=`, `response=`, and `ground_truth=` as keyword arguments to the evaluator. If you use incorrect kwargs, the evaluator compares the wrong fields and scores near zero.

### Interpret scores

| Score range | Meaning | Action |
|---|---|---|
| < 3.5 | Outputs diverge | Check for missing prompt context or unmigrated nodes. |
| 3.5 to 4.5 | Minor phrasing differences | Generally acceptable. |
| > 4.5 | Strong semantic match | Safe to proceed to deployment. |

When your mean similarity score is consistently ≥ 3.5, proceed to [Deploy and operate your migrated Agent Framework workflow](how-to-deploy-migrated-agent-framework-workflow.md).

## Troubleshooting

### `ModuleNotFoundError: No module named 'agent_framework'`

The package isn't installed or a prerelease version is conflicting. Uninstall and reinstall cleanly:

```bash
pip uninstall agent-framework agent-framework-core agent-framework-foundry -y
pip install agent-framework>=1.0.0 agent-framework-foundry
```

### `CredentialUnavailableError` or `ClientAuthenticationError`

`DefaultAzureCredential` tries multiple credential sources in order. If all sources fail, the error message lists every attempted credential.

1. Confirm your Azure CLI session is current: `az account show`.
1. Verify your account has access to the Foundry project: `az account set --subscription <your-subscription-id>`.
1. For managed identity in Container Apps, ensure the identity has the **Cognitive Services User** role on your Foundry resource.

### `AzureOpenAIChatClient` doesn't work with my Foundry endpoint

`AzureOpenAIChatClient` targets raw Azure OpenAI endpoints (`https://<resource>.openai.azure.com`). For Foundry project endpoints (`https://<resource>.services.ai.azure.com`), use `FoundryChatClient`:

```python
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ["FOUNDRY_MODEL"],
    credential=DefaultAzureCredential(),
)
```

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

Check that you're using the correct kwargs.

```python
# Correct
evaluator(query=question, response=maf_answer, ground_truth=pf_answer)

# Incorrect (compares wrong fields)
evaluator(answer=maf_answer, ground_truth=pf_answer)
```

### No traces appearing in Application Insights

For tracing troubleshooting, see [Deploy and operate your migrated Agent Framework workflow](how-to-deploy-migrated-agent-framework-workflow.md#troubleshooting).

## Related content

- [Deploy and operate your migrated Agent Framework workflow](how-to-deploy-migrated-agent-framework-workflow.md)
- [Migrate from Prompt Flow to Microsoft Agent Framework](prompt-flow-migration-overview.md)
- [Configure tracing for AI agent frameworks](../../foundry/observability/how-to/trace-agent-framework.md)
- [Microsoft Agent Framework on GitHub](https://github.com/microsoft/agent-framework)
- [Azure AI Evaluation SDK reference](/python/api/overview/azure/ai-evaluation-readme)
