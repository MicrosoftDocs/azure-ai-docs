---
title: Manage Agents at Scale in Microsoft Foundry Control Plane
description: Learn how to manage agents by using Microsoft Foundry Control Plane.
author: santiagxf
ms.author: scottpolly
ms.reviewer: fasantia
ms.date: 01/02/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Manage agents at scale

Microsoft Foundry Control Plane provides centralized management and observability for agents running across various platforms and infrastructures.

This article explains how to manage agents across a subscription by using Foundry Control Plane.

## Agent inventory

The **Assets** pane provides a unified, searchable table of all AI assets across projects within a subscription. This inventory brings together critical metadata and health indicators, so you can assess and act on your AI estate efficiently.

Foundry Control Plane automatically discovers [supported agents](#supported-agent-platforms) within resources in the selected subscription and displays them on the **Agents** tab. To view them, select **Operate** > **Assets** > **Agents**.

:::image type="content" source="media/how-to-manage-agents/inventory-all-agents.png" alt-text="Screenshot of the tab that contains an inventory of agents." lightbox="media/how-to-manage-agents/inventory-all-agents.png":::

The following information appears:

| Column | Description | Agent platform |
| ------ | ----------- | ------------ |
| **Name** | The name of the agent or the agentic resource. | All |
| **Source** | The source platform where the agent or resource was discovered. See the [list of supported platforms](#supported-agent-platforms) later in this article. | All |
| **Project** | The Foundry project associated with the agent. For custom agents, it's the project where the agent was registered. | Foundry<br><br>Custom |
| **Status** | Refers to a broad range of conditions, including operational, health, or lifecycle status of the agent. Agents transition to different values, depending on the platform and [lifecycle operations](#lifecycle-operations). Possible values are: <ul><li>[Running](#start-and-stop-agents)</li><li>[Stopped](#start-and-stop-agents)</li><li>[Blocked](#block-and-unblock-agents)</li><li>[Unblocked](#block-and-unblock-agents)</li><li>[Unknown](#handle-unknown-states)</li></ul> | All |
| **Version** | The version of the agent asset. | Foundry |
| **Published as** | Indicates if the agent was [published as an agent application](../agents/how-to/publish-agent.md). Published agents in Foundry have their own endpoint for invocation. | Foundry |
| **Error rate** | The proportion of failed runs compared to successful ones in the last month. This column requires [observability configured](#observability-of-agents). | All |
| **Estimated cost** | The estimated cost of the agent executions in the last month, based on the number of tokens consumed. This column requires [observability configured](#observability-of-agents). | Foundry |
| **Token usage** | The estimated tokens consumed by the runs in the last month. This column requires [observability configured](#observability-of-agents). | Foundry |
| **Runs** | The number of executions in the last month. This column requires [observability configured](#observability-of-agents). | All |
| **Monitoring features** | The number of monitoring features that are enabled in the agent. See [The three stages of GenAIOps evaluation](../../concepts/observability.md#the-three-stages-of-genaiops-evaluation). | Foundry |
| **Entra ID** | The Microsoft Entra Agent ID application and object ID associated with the agent. An agent identity is a special service principal in Microsoft Entra ID. It represents an identity that the agent identity blueprint created and is authorized to impersonate. See [Agent identity concepts in Microsoft Foundry](../agents/concepts/agent-identity.md). | Foundry |

### Permissions model

Foundry Control Plane automatically discovers agents that users have access to. Because Foundry Control Plane aggregates information across resources within the subscription, different users might see different agents listed on the **Assets** pane, depending on the access level on each of those resources.

## Supported agent platforms

Foundry Control Plane automatically discovers agents in the following platforms:

> [!div class="checklist"]
>
> * Foundry agents, including [prompt-based agents](../../agents/overview.md), [workflows](../agents/concepts/workflow.md), and [hosted agents](../agents/concepts/hosted-agents.md)
> * [Azure SRE Agent](/azure/sre-agent/)
> * [Azure Logic Apps agent loops](/azure/logic-apps/agent-workflows-concepts)
> * [Custom agents](register-custom-agent.md)

### Foundry agents

Foundry Control Plane can help you manage agents across all your Foundry projects. When you create an agent or workflow in a Foundry project, the agent appears in the inventory. Foundry Control Plane lists all the agents across all the projects within a subscription.

For each agent, the information includes:

* The latest version of the agent.
* Versions [published as agent applications](../agents/how-to/publish-agent.md).

In this way, you can monitor versions consumed by your users and new versions under development. The following example shows multiple Foundry agents listed. Version 6 of the `format-agent` agent was published, but version 7 (latest) is still under development.

:::image type="content" source="media/how-to-manage-agents/inventory-foundry-agent.png" alt-text="Screenshot of multiple Foundry agents listed in an inventory." lightbox="media/how-to-manage-agents/inventory-foundry-agent.png":::

> [!NOTE]
> Foundry classic agents and Azure OpenAI assistants aren't supported.

### Azure SRE Agent

Azure SRE Agent helps you maintain the health and performance of your Azure resources through AI-powered monitoring and assistance. Agents continuously watch your resources for problems, provide troubleshooting help, and suggest remediation steps in a natural-language chat interface. [Learn more about Azure SRE Agent](/azure/sre-agent/).

Foundry Control Plane discovers Azure SRE Agent resources in your subscription and displays them in the inventory.

### Azure Logic Apps agent loop

Azure Logic Apps supports workflows that complete tasks by using agent loops with large language models (LLMs). An agent loop uses an iterative process to solve complex, multistep problems. [Learn more about workflows with AI agents and models in Logic Apps](/azure/logic-apps/agent-workflows-concepts).

Foundry Control Plane discovers Logic Apps resources that contain agent loop workflows and lists them in the inventory.

> [!NOTE]
> Observability features, including traces and metrics, aren't supported in Logic Apps agent loops.

### Custom agents

For agentic platforms that Foundry Control Plane doesn't support, you can manually register agents in a Foundry project to enable management.

Registering custom agents that run in Azure compute services or other cloud environments can help you gain visibility into their operations and control their behavior. You can register a custom agent in Foundry Control Plane and develop the agent in the technology of your choice, for both platform and infrastructure solutions.

[Learn how to register an agent in Foundry Control Plane](register-custom-agent.md) to enable management.

## Observability of agents

Foundry Control Plane uses the Application Insights resources that host your agents to help you monitor and diagnose those agents. When such data is available, Foundry Control Plane can:

* Compute runs and error rates.
* Compute usage metrics, including token usage and cost.
* Collect execution traces.

If you don't see such information for your agent, you need to [configure Application Insights](monitoring-across-fleet.md#configure-monitoring). Ensure that you also have [the appropriate permissions to view Application Insights data and cost metrics](monitoring-across-fleet.md#prerequisites).

> [!TIP]
> We strongly advise configuring Application Insights for each of the resources that host agents. For Foundry agents, Application Insights is configured per Foundry project. However, you can connect multiple Foundry projects to the same Application Insights resources to optimize those resources.

### View traces

You can view traces and logs sent to Foundry. Traces are stored in Application Insights, and you can query them by using the Foundry portal or any other compatible tool.

To view them:

1. On the toolbar, select **Operate**.

1. On the left pane, select **Assets**.

1. Select the agent.

1. Select the **Traces** tab. The tab shows one entry for each call made to the agent.

   Two columns contain IDs associated with the call: **Trace ID** and **Conversation ID**. Traces are stored in Application Insights and contain data to diagnose behavior. The **Conversation ID** column applies for Foundry agents. It contains the *conversation* associated with the trace. Conversations are stored in the Foundry service.

    :::image type="content" source="media/how-to-manage-agents/inventory-traces-list.png" alt-text="Screenshot of the traces associated with one agent." lightbox="media/how-to-manage-agents/inventory-traces-list.png":::

1. To see the details, select a value in the **Trace ID** column.

    :::image type="content" source="media/how-to-manage-agents/inventory-traces-view.png" alt-text="Screenshot of a single trace with LLM calls." lightbox="media/how-to-manage-agents/inventory-traces-view.png":::

    > [!TIP]
    > Custom agents require extra configuration to show details, including tools and LLM spans. Learn more at [Instrument custom code agents](register-custom-agent.md#instrument-custom-code-agents).

## Lifecycle operations

Foundry Control Plane helps organizations control agents to manage usage and infrastructure cost. Different agent platforms support different operations.

The following table summarizes supported actions for each platform. A foundry agent's support depends on the agent type and its publishing state.

| Platform | Agent type | Published | Supported actions | Notes |
| -------- | ---------- | --------- | ----------------- | ----- |
| Foundry | Prompt<br><br>Workflow | No | None | Unpublished agents don't have dedicated deployments, and they use the project's endpoint to receive requests. Their lifecycle is attached to the project's lifecycle. To stop an unpublished prompt agent or workflow, you must delete it. |
| Foundry | Hosted | No | Start/stop | Stopping a hosted agent stops the deployment associated with it. Any compute attached to it is deallocated. |
| Foundry | Prompt<br><br>Workflow<br><br>Hosted | Yes | Start/stop | Stopping a published agent stops the deployment associated with it. It deallocates any compute attached. |
| Azure SRE Agent | Not applicable | Not applicable | Start/stop | |
| Azure Logic Apps | Not applicable | Not applicable | Start/stop | You can stop an Azure Logic Apps agent loop by stopping the Logic Apps resource that hosts it. Stopping a Logic Apps resource stops all the workflows associated with it. |
| Custom | Not applicable | Not applicable | Block/unblock | Foundry doesn't have access to the underlying infrastructure where the agent runs, so start and stop operations aren't available. However, Foundry can block incoming requests to the agent. Blocking a request prevents clients from consuming it. |

### Start and stop agents

Stopping an agent stops the infrastructure that's associated with it and moves the agent to the **Stopped** state.

Stopping an agent deprovisions its infrastructure and prevents new runs. Any workflows or resources connected to this agent can't access it. This operation *doesn't terminate existing runs*.

To stop an agent:

1. On the toolbar, select **Operate**.

1. On the left pane, select **Assets**.

1. Select the agent that you want to stop. The information pane appears.

1. Select **Update status**, and then select **Stop**.

    :::image type="content" source="media/how-to-manage-agents/how-to-manage-agents-stop.png" alt-text="Screenshot of steps for stopping an agent." lightbox="media/how-to-manage-agents/how-to-manage-agents-stop.png":::

1. Confirm the operation.

After you stop the agent, the **Status** value of the agent in Foundry is **Stopped**.

To start the agent:

1. Select **Update status**, and then select **Start**.

1. Confirm the operation.

### Block and unblock agents

For [custom agents](register-custom-agent.md), Foundry doesn't have access to the underlying infrastructure where the agent runs, so start and stop operations aren't available. However, Foundry can block incoming requests to the agent. Blocking a request prevents clients from consuming it. This capability allows administrators to disable an agent if it misbehaves.

To block incoming requests to your agent:

1. On the toolbar, select **Operate**.

1. On the left pane, select **Assets**.

1. Select the agent that you want to block. The information pane appears.

1. Select **Update status**, and then select **Block**.

    :::image type="content" source="media/register-custom-agent/register-custom-agent-block.png" alt-text="Screenshot of steps for blocking incoming requests to an agent." lightbox="media/register-custom-agent/register-custom-agent-block.png":::

1. Confirm the operation.

After you block the agent, the **Status** value of the agent in Foundry is **Blocked**. Agents in the **Blocked** state run in their associated infrastructure but can't take incoming requests. Foundry blocks any attempt to communicate with the agent.

To unblock the agent:

1. Select **Update status**, and then select **Unblock**.

1. Confirm the operation.

### Handle unknown states

Under certain circumstances, agents can display the status **Unknown**. In those cases, Foundry Control Plane can't determine the status of the agent either because the source platform is unavailable or because the agent failed to report its state back.

## Related content

* [What is Microsoft Foundry Control Plane?](overview.md)
* [Monitor agent health and performance across your fleet](monitoring-across-fleet.md)
