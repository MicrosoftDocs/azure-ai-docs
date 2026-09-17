---
title: Use Insights in Foundry
description: Learn how to run Insights scans, review recurring production behaviors and supporting traces, and route confirmed Insights to evaluation or optimization workflows.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: hanch
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: how-to
ms.date: 09/17/2026
ai-usage: ai-assisted
---

# Use Insights in Foundry (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Insights in Foundry analyzes traces from your production agents and organizes recurring behavior into reviewable Insights. Each Insight can include representative traces, affected agent versions, a likely cause, and a recommended next action.

Use Insights in Foundry to move from reviewing individual traces to answering broader questions:

- What important behavior is happening repeatedly?
- Which agents, versions, or conversations are affected?
- What trace evidence supports the Insight?
- What should I investigate, evaluate, or improve next?

In this article, you learn how to:

- Prepare an agent and its telemetry for Insights in Foundry.
- Run an Insights scan in the Microsoft Foundry portal.
- Review an Insight and validate its supporting evidence.
- Route a confirmed Insight to the appropriate next action.
- Run on-demand analysis and configure a schedule with the Python SDK.
- Troubleshoot common setup and result-quality issues.

## Prerequisites

Before you begin, you need:

- A Foundry project with a supported model deployment and a connected Azure Monitor Application Insights resource.
- For the Python examples, Python 3.10 or later and Azure CLI. Sign in by running `az login`.
- Permission to create role assignments at the required resource scopes, or an administrator who can assign the following roles before you run the workflow.
- For a Prompt agent, the interactive user must have the **Foundry User** role on the project. For a Hosted agent, the user must have the **Foundry Project Manager** role.
- The **Monitoring Reader** role on the connected Application Insights resource for both the interactive user and the Foundry project's managed identity.
- If the `AppGenAIContent` table is protected, the **Privileged Monitoring Data Reader** role for each identity that reads protected content, including the project's managed identity. For resource-scoped queries, assign the role on the connected Application Insights resource. For workspace-scoped queries, assign it on the linked Log Analytics workspace. For more information, see [Grant access to protected tables](/azure/azure-monitor/logs/protected-tables-configure#grant-access-to-protected-tables).
- The project's managed identity needs access to the model deployment used for analysis.
- Recent, representative traces for the selected agent.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

### Choose a suitable agent

Start with one production agent that has:

- A technical owner who can review the agent's traces and Insights.
- Representative successful and unsuccessful traffic.
- Stable agent and version identities in telemetry.
- Repeated traffic from which patterns can emerge.

### Verify trace readiness

Insights in Foundry can analyze only the evidence available in traces. Before you run a scan:

- In your Foundry project, open the agent.
- Select **Traces**, and then open the tracing experience.
- Confirm that recent production or representative test traces are visible.
- Confirm that trace timestamps fall within the analysis lookback window.

Missing identity, content, spans, tool arguments, or tool results can reduce grouping, diagnosis, and proposed-fix quality.

## How Insights in Foundry works

Insights in Foundry uses trace data from the Azure Monitor Application Insights resource connected to your Foundry project.

```text
Agent production traffic
  -> OpenTelemetry traces in Application Insights
  -> recurring behavior analysis
  -> Insight with evidence and likely cause
  -> human review
  -> evaluation, optimization, owner routing, or no action
  -> continued monitoring
```

The first analysis uses a 7-day lookback window to review existing trace history. After setup, you can run analysis on demand or enable scheduled generation, depending on the supported configuration.

Insights in Foundry doesn't require you to predefine every evaluator or alert. It complements known-condition monitoring and evaluation by finding repeated production behavior that you might not already know to test.

### Information in an Insight

Depending on the available trace data and supported configuration, an Insight can include:

| Field | Description |
| --- | --- |
| Title | A concise description of the recurring behavior or regression. |
| Category | One of the following categories: Context & memory, Cost & tokens, Hallucinations, Latency, Output quality, Reliability errors, Security & risk, or Tool call failures. |
| Severity | The potential impact of the Insight, displayed as High, Medium, or Low. Severity provides decision support and doesn't replace your organization's risk assessment. |
| Status | The current state of the Insight, such as Active. |
| Agent version and recency | The agent version represented in the evidence and the time when the Insight was created. |
| Description | An AI-generated explanation of the observed behavior and likely cause. |
| Linked traces | The broader cohort associated with the Insight. |
| Highlighted traces | Representative examples selected for review, including a summary, duration, and token count. |
| Proposed action or fix | A recommended investigation or improvement path. Availability and specificity vary by Insight and configuration. |

## Run an Insights scan in the portal

1. Sign in to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).
1. Open the Foundry project that contains your agent.
1. Select **Build** > **Agents**, and then select the agent.
1. Select the **Insights** tab.
1. Under **Configuration**, select the **Judge model** used to generate Insights.
1. Select **Run scan now**.

:::image type="content" source="../../media/observability/agent-insights/empty-state.png" alt-text="Screenshot of the Insights page before its first analysis, showing model configuration and the Run scan now action." lightbox="../../media/observability/agent-insights/empty-state.png":::

The scan starts asynchronously. Processing time varies based on traffic volume, telemetry completeness, service capacity, and the selected Judge model. You can leave the page and return later.

To enable scheduled Insight generation, select **Settings**, and then select **Insights**.

## Review generated Insights

When the analysis finishes, the **Insights** tab shows generated Insights for the selected agent.

:::image type="content" source="../../media/observability/agent-insights/insights-generated.png" alt-text="Screenshot of generated Insights and selected details, including category, severity, linked traces, evidence, and a proposed fix." lightbox="../../media/observability/agent-insights/insights-generated.png":::

Filter the list by **Severity**, **Category**, or **Status**. You can also search or sort the list.

Select **Run now** to start another scan.

Select the **History** icon next to **Run now** to review previous analysis runs.

:::image type="content" source="../../media/observability/agent-insights/insights-history-button.png" alt-text="Screenshot of the Insights toolbar with the Run now action and History icon." lightbox="../../media/observability/agent-insights/insights-history-button.png":::

The **Insights generation history** window includes both on-demand and scheduled runs. For each run, you can review its status, start and end times, duration, token usage, traces analyzed, new Insights, and updated Insights. Use the search box to find a run, or use **Prev** and **Next** to move between pages.

:::image type="content" source="../../media/observability/agent-insights/insights-generation-history.png" alt-text="Screenshot of Insights generation history showing run status, timing, token usage, analyzed traces, and new or updated Insights." lightbox="../../media/observability/agent-insights/insights-generation-history.png":::

Start with an Insight that:

- Affects an important user or business workflow.
- Has enough linked traces to indicate repetition.
- Includes representative traces that your team understands.
- Describes a behavior that the agent owner can confirm or challenge.

A large linked-trace count doesn't by itself prove business impact. Review the evidence and the affected workflow.

## Validate an Insight

Don't accept an Insight based only on its title or summary. Review its evidence before taking action.

1. Open the Insight.
2. Read the description and proposed fix.
3. Confirm the agent version, category, severity, status, and creation time.
4. Expand the highlighted traces.
5. For each highlighted trace, review its summary, duration, and token count. Then open the trace to verify the cited behavior.
6. Compare problematic examples with healthy traces.
7. Decide whether the behavior is real, important, correctly grouped, and assigned to the correct owner for further validation.

## Take action on a confirmed Insight

The available actions depend on the Insight and the supported preview configuration.

### Investigate traces

Open the highlighted or filtered trace cohort to review the complete execution path, including model operations, tool calls, timing, errors, and agent output.

### Add evaluation coverage

If the Insight confirms an important expected behavior, create or update an evaluator or dataset so you can test the behavior explicitly before and after future changes.

Evaluation validates behavior you know to test. Insights in Foundry helps identify which production behaviors should become explicit evaluation targets.

### Review a proposed improvement

Some Insights include a proposed prompt or code change. Review the proposal against:

- The highlighted traces.
- The intended agent behavior.
- Healthy control traces.
- Security and policy requirements.
- Tests and evaluation datasets.
- Your normal source-control, review, and deployment process.

> [!NOTE]
> Concrete prompt or code proposals are available only for supported agent types and configurations and can change during preview. Code-based Hosted agents and Prompt agents are supported, with concrete fix proposals when available.

#### General guidance when agent code isn't available

When Insights in Foundry can't access editable agent instructions or source code, the proposed fix provides general remediation guidance instead of a concrete diff. Review the recommendation and apply it in the system that owns the agent implementation.

:::image type="content" source="../../media/observability/agent-insights/fix-general-advice-when-no-access-to-code.png" alt-text="Screenshot of an Insight with general remediation guidance when editable agent instructions or source code aren't available." lightbox="../../media/observability/agent-insights/fix-general-advice-when-no-access-to-code.png":::

#### Prompt agent proposed fix

For a Prompt agent, the proposed fix can show a side-by-side diff of the agent instructions.

:::image type="content" source="../../media/observability/agent-insights/fix-prompt-agent.png" alt-text="Screenshot of a Prompt agent proposed fix showing a side-by-side diff of the agent instructions." lightbox="../../media/observability/agent-insights/fix-prompt-agent.png":::

#### Code-based Hosted agent proposed fix

For a code-based Hosted agent, the proposed fix can show a side-by-side source code diff.

:::image type="content" source="../../media/observability/agent-insights/fix-code-based-hosted-agent.png" alt-text="Screenshot of a code-based Hosted agent proposed fix showing a side-by-side source code diff." lightbox="../../media/observability/agent-insights/fix-code-based-hosted-agent.png":::

When optimization is the appropriate action, use the confirmed Insight, representative traces, and evaluation objective as input to a supported optimization workflow.

### Route a dependency or platform issue

If the evidence points to a tool, model endpoint, MCP server, data source, network, or Foundry platform issue, route the Insight to the responsible owner. Don't apply an agent-side prompt or code change when the agent doesn't control the failing behavior.

Use Azure Monitor for infrastructure availability, dependency health, quotas, throttling, and other operational incident workflows.

### Resolve, dismiss, or monitor recurrence

Where supported, use the Insight status to record that an Insight is active, resolved, or dismissed. Before marking an Insight resolved, verify the change against new production evidence or a relevant evaluation.

## Use the code samples

The following Python examples show the core SDK calls for an existing registered agent. They use the same APIs as the complete [on-demand sample][on-demand-sample] and [scheduled sample][scheduled-sample] in the Azure SDK for Python repository.

Run the setup first, then use the on-demand or scheduled workflow in the same Python session. The examples keep the monitor and its Insights available for review. They don't create an agent, generate traces, or delete existing monitors.

### Set up the Python client

Before you run the examples:

- Complete the [prerequisites](#prerequisites), including model and telemetry access for the project's managed identity.
- Select an agent with ingested traces from the last three hours for the on-demand example. For an external agent, the emitted OpenTelemetry agent ID must match its registered `otel_agent_id`.
- Set the following environment variables in your shell.

| Variable | Value |
| --- | --- |
| `FOUNDRY_PROJECT_ENDPOINT` | Your Foundry project endpoint. |
| `FOUNDRY_AGENT_NAME` | The exact name of your existing registered agent, not a name prefix. |
| `FOUNDRY_MODEL_NAME` | The deployment name of the model used to analyze traces. |

Install version 2.6.1 or later of the Azure AI Projects client library and Azure Identity:

```bash
python -m pip install "azure-ai-projects>=2.6.1" azure-identity
```

Create the client with `allow_preview=True` to use the preview operations under `beta.agent_insight_monitors`.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=credential,
    allow_preview=True,
)
monitor_operations = project_client.beta.agent_insight_monitors
```

Reference: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential).

Create a monitor with scheduling disabled. This configuration lets you start analysis explicitly before enabling recurring runs.

If the agent already has a monitor, skip creation and use `monitor = monitor_operations.get("<monitor-id>")` instead. This approach preserves its current settings, runs, and Insights.

```python
from azure.ai.projects.models import AgentInsightMonitorCreate

monitor = monitor_operations.create(
    AgentInsightMonitorCreate(
        agent_name=os.environ["FOUNDRY_AGENT_NAME"],
        model_deployment_name=os.environ["FOUNDRY_MODEL_NAME"],
        enabled=False,
    )
)
print(f"Monitor ID: {monitor.id}")
```

Reference: [AgentInsightMonitorCreate](/python/api/azure-ai-projects/azure.ai.projects.models.agentinsightmonitorcreate), [BetaAgentInsightMonitorsOperations][monitor-operations].

Save the monitor ID. Don't delete an existing monitor to rerun these examples. Deleting a monitor also removes its runs, Insights, and state.

### Run analysis on demand

Use the monitor from setup to analyze traces from the last three hours. The run starts asynchronously; `poller.result()` waits for completion.

```python
import uuid

from azure.ai.projects.models import AgentInsightRunCreate

poller = monitor_operations.begin_create_run(
    monitor.id,
    AgentInsightRunCreate(lookback_hours=3),
    operation_id=str(uuid.uuid4()),
)
run_id = poller.details["run_id"]
print(f"Run ID: {run_id}")

run_result = poller.result()
completed_run = monitor_operations.get_run(monitor.id, run_id)
print(f"Run status: {completed_run.status}")
print(f"Traces in window: {run_result.traces_in_window}")
print(f"Traces analyzed: {run_result.traces_analyzed}")
print(f"Insights created: {run_result.insights_created}")
print(f"Insights updated: {run_result.insights_updated}")
print(f"Insights reopened: {run_result.insights_reopened}")
print(f"Total tokens: {run_result.token_usage.total_tokens}")
```

Reference: [AgentInsightRunCreate](/python/api/azure-ai-projects/azure.ai.projects.models.agentinsightruncreate), [BetaAgentInsightMonitorsOperations][monitor-operations].

The output shows the run status, trace counts, Insight counts, and token usage. Counts depend on your agent's traces; a successful run doesn't guarantee new Insights.

### Review and resolve an Insight

After analysis completes, list the monitor's Insights with their details:

```python
insights = list(
    monitor_operations.list_insights(monitor.id, include_details=True)
)
print(f"Insights available: {len(insights)}")
for insight in insights:
    print(f"{insight.id}: {insight.title}")
    print(f"Severity: {insight.severity}; status: {insight.status}")
    print(f"Linked traces: {insight.trace_count}")
    if insight.details:
        print(insight.details.recommended_actions.proposed_fix.text)
```

Reference: [BetaAgentInsightMonitorsOperations][monitor-operations].

Review the supporting traces and proposed action before changing status. After you validate a fix, replace `<insight-id>` with the ID you reviewed and run this optional step:

```python
from azure.ai.projects.models import AgentInsightStatus, AgentInsightUpdate

resolved_insight = monitor_operations.update_insight(
    monitor.id,
    "<insight-id>",
    AgentInsightUpdate(status=AgentInsightStatus.RESOLVED),
)
print(f"Insight status: {resolved_insight.status}")
```

Reference: [AgentInsightUpdate](/python/api/azure-ai-projects/azure.ai.projects.models.agentinsightupdate), [BetaAgentInsightMonitorsOperations][monitor-operations].

This records your review decision. It doesn't apply the proposed fix or change your agent.

### Run analysis on a schedule

To enable recurring analysis, update the monitor from setup with a six-hour interval. You don't need to run on-demand analysis first.

```python
from azure.ai.projects.models import AgentInsightMonitorUpdate

scheduled_monitor = monitor_operations.update(
    monitor.id,
    AgentInsightMonitorUpdate(enabled=True, run_interval_hours=6),
)
print(f"Schedule enabled: {scheduled_monitor.enabled}")
print(f"Run interval hours: {scheduled_monitor.run_interval_hours}")
print(f"Next scheduled run: {scheduled_monitor.next_scheduled_run_at}")
```

Reference: [AgentInsightMonitorUpdate](/python/api/azure-ai-projects/azure.ai.projects.models.agentinsightmonitorupdate), [BetaAgentInsightMonitorsOperations][monitor-operations].

This method returns the schedule settings, not analysis results. Enabling the schedule can start a run immediately. The schedule remains enabled after your Python session ends and can incur model charges.

To stop future scheduled runs, disable the monitor:

```python
from azure.ai.projects.models import AgentInsightMonitorUpdate

monitor_operations.update(
    monitor.id,
    AgentInsightMonitorUpdate(enabled=False),
)
```

Reference: [AgentInsightMonitorUpdate](/python/api/azure-ai-projects/azure.ai.projects.models.agentinsightmonitorupdate), [BetaAgentInsightMonitorsOperations][monitor-operations].

Disabling scheduling doesn't cancel a run that's already active. Use `list_runs` to find active runs and `cancel_run` if you need to stop them.

### Close the clients

When you finish the examples, close the client and credential. This releases local connections; it doesn't delete the monitor or disable its schedule.

```python
project_client.close()
credential.close()
```

Reference: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential).

### Run the complete samples

Use the [on-demand sample][on-demand-sample] or [scheduled sample][scheduled-sample] for a self-contained demonstration. Download the selected script and [agent_insights_util.py][sample-utilities] into the same directory, and then follow the script's installation and environment-variable instructions.

Unlike the preceding excerpts, each complete sample:

- Registers a temporary external agent with a unique name.
- Emits fictional traces and waits for ingestion. Trace generation doesn't execute tools or call a model; Insights analysis uses your model deployment.
- Deletes its own monitor and agent in `finally`. Ingested telemetry remains in Application Insights under its normal retention policy.

The complete samples also require `APP_INSIGHTS_RESOURCE_ID` for ingestion queries. Their optional `FOUNDRY_AGENT_NAME` is a name prefix, not an existing agent name.

The scheduled sample shows how to enable a schedule and read its settings. It doesn't wait for scheduled analysis. Its cleanup disables the schedule and cancels active runs before deletion, so it doesn't leave recurring analysis enabled.

[on-demand-sample]: https://github.com/Azure/azure-sdk-for-python/blob/fedc3ab96021c2b0d42496cb4ddf0c476f77b63d/sdk/ai/azure-ai-projects/samples/agent_insights/sample_agent_insights_on_demand.py
[scheduled-sample]: https://github.com/Azure/azure-sdk-for-python/blob/fedc3ab96021c2b0d42496cb4ddf0c476f77b63d/sdk/ai/azure-ai-projects/samples/agent_insights/sample_agent_insights_scheduled.py
[sample-utilities]: https://github.com/Azure/azure-sdk-for-python/blob/fedc3ab96021c2b0d42496cb4ddf0c476f77b63d/sdk/ai/azure-ai-projects/samples/agent_insights/agent_insights_util.py
[monitor-operations]: /python/api/azure-ai-projects/azure.ai.projects.operations.betaagentinsightmonitorsoperations

## Troubleshoot Insights in Foundry

### Insights in Foundry isn't available or a scan can't start

Check that:

- Insights in Foundry is available in the selected subscription and region.
- The project uses a supported Foundry project type.
- You can see recent traces in the connected Application Insights resource.
- The project is connected to the intended Application Insights resource.
- You assigned the required user and managed-identity roles at the correct scopes.
- You can read protected trace content when required.
- Role assignments have propagated.
- The selected insight-generation model is available and has quota.

A `404` response from the preview API can indicate that Insights in Foundry isn't enabled for the selected subscription context. A `403` response indicates that the endpoint is reachable but the caller isn't authorized.

### The first analysis is still running

Analysis runs asynchronously. Confirm that the lookback window contains traces, and then return later. Don't reset or repeatedly reenable the monitor while a run is active.

If the state doesn't change within the expected processing period, record:

- Subscription and project identifiers.
- Agent name and version.
- Monitor and run IDs.
- Start time in UTC.
- Request ID from a failed API response, when available.
- A screenshot of the current state.

Don't include credentials, access tokens, connection strings, or unredacted sensitive content.

### No Insights were generated

The absence of generated Insights doesn't necessarily mean that setup failed. The selected traffic might not contain a repeated pattern with enough evidence.

Check that:

- The lookback window contains sufficient traffic.
- Traces include both healthy and problematic behavior.
- Agent and version identities are consistent.
- Model, tool, and workflow spans are present.
- The expected behavior occurs in more than one trace.
- Filters aren't hiding completed Insights.

If you know a repeated issue exists, collect the expected behavior, UTC window, agent version, and representative trace IDs before requesting support.

### An Insight appears incorrect

On the **Insights** page, select **Give feedback** to report a result-quality issue.

Classify the problem before reporting it:

- False positive unsupported by the traces.
- Expected behavior presented as a problem.
- Incorrect category or severity.
- Correct symptom with an incorrect likely cause.
- Proposed action that the named owner can't execute.
- Unrelated issues merged together.
- One issue duplicated across multiple Insights or agent versions.
- Evidence contradicted by healthy control traces.

Include the Insight ID, agent version, UTC time window, and relevant trace IDs in the report.

### Trace content is missing

Insights in Foundry can't reconstruct content or spans that it didn't capture, and it can't read data without the required authorization.

Verify instrumentation and access to:

- Agent and version identity.
- User request and agent response, subject to your data policy.
- Model calls.
- Tool arguments and results.
- Workflow and subagent spans.
- Protected generative AI content tables.

## Responsible use and limitations

Insights in Foundry uses AI to identify patterns, infer likely causes, and recommend actions. Results can be incomplete or incorrect.

- Review the supporting traces before accepting an Insight.
- Validate proposed prompt, code, tool, workflow, or configuration changes before deployment.
- Don't use Insights in Foundry as your only production monitoring, security, safety, or compliance control.
- Insights aren't guaranteed to be real time.
- Insights in Foundry might miss real issues or combine unrelated behavior.
- Category, severity, ownership, likely cause, and proposed actions are decision support, not authoritative classifications.
- A valid symptom can be attributed to the wrong agent, dependency, or platform layer.
- Infrastructure outages, endpoint availability, quotas, and dependency incidents remain Azure Monitor or service-owner responsibilities.
- Insight generation depends on trace completeness, identity, permissions, model availability, and service capacity.
- An Insights run analyzes an agent's traces over a lookback window and doesn't support every incident-scoped investigation workflow.
- Supported agent types, models, regions, limits, prices, and UI can change during preview.
- Follow your organization's requirements for confidentiality, privacy, security, compliance, responsible AI, and data residency.

## Pricing

Insights in Foundry can incur charges for the model deployment used to generate Insights.

## Related content

- [Set up tracing](trace-agent-setup.md)
- [Monitor agents](how-to-monitor-agents-dashboard.md)
- [Evaluate agents](evaluate-agent.md)
- [Agent Insights Python samples](https://github.com/Azure/azure-sdk-for-python/tree/fedc3ab96021c2b0d42496cb4ddf0c476f77b63d/sdk/ai/azure-ai-projects/samples/agent_insights)
- [Agent optimizer overview](../../agents/concepts/agent-optimizer-overview.md)
- [Insights in Foundry REST API specification](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/ai-foundry/data-plane/Foundry/src/agent-insights/routes.tsp)
