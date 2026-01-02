---
title: "Manage agents in Microsoft Foundry Control Plane"
description: "Learn how to manage agents using Microsoft Foundry Control Plane."
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

# Manage agents

The Microsoft Foundry Control Plane provides centralized management and observability for agents running across different platforms and infrastructures.

This article explains how to manage agents using Microsoft Foundry Control Plane.

## Agents inventory

The **Assets** page provides a unified, searchable table of all AI assets across projects within a subscription. It brings together critical metadata and health indicators, so you can assess and act on your AI estate efficiently.

Control Plane automatically discovers [supported agents](#supported-agent-platforms) within resources in the selected subscription and displays them in the **Operate > Assets > Agents** page.

:::image type="content" source="media/how-to-manage-agents/inventory-all-agents.png" alt-text="Screenshot of the inventory page listing multiple agents." lightbox="media/how-to-manage-agents/inventory-all-agents.png":::

The following information is displayed:

| Column | Description | Applies to |
|--------|-------------|------------|
| **Name** | The name of the agent or the agentic resource. | All |
| **Source** | The source platform from where the agent or resource was discovered. | All |
| **Project** | The Foundry project associated with the agent. For custom agents, it's the project where the agent was registered to. | Foundry<br />Custom | 
| **Status** | It refers to a broad range of conditions, including operational, health, or lifecycle, of the agent. Agents transition to different *status* depending on the platform, the agent condition, and [lifecycle operations](#lifecycle-operations). Possible values are: <ul><li>Running</li><li>Stopped</li><li>Blocked</li><li>Unblocked</li><li>Unknown</li></ul> | All |
| **Version** | The version of the agent asset. | Foundry |
| **Published as** | Indicates if the agent was published as an agent application. Published agents in Foundry have their own endpoint for invocation. | Foundry |
| **Error rate** | The proportion of failed runs compared to successful ones in the last month. This column requires [observability configured](#observe-agents). | All |
| **Estimated cost** | The estimated cost of the agent executions in the last month, based on the number of tokens consumed. This column requires [observability configured](#observe-agents). | Foundry |
| **Token usage** | The estimated tokens consumed by the runs in the last month. This column requires [observability configured](#observe-agents). | Foundry |
| **Runs** | The number of executions in the last month. This column requires [observability configured](#observe-agents). | All |
| **Monitoring features** | The number of monitoring features that are enabled in the agent. See [The three stages of GenAIOps evaluation](../observability/concepts/observability.md#the-three-stages-of-genaiops-evaluation). | Foundry |
| **Entra ID** | Microsoft Entra ID Agent ID application and object ID associated with the agent. An agent identity is a special service principal in Microsoft Entra ID. It represents an identity that the agent identity blueprint created and is authorized to impersonate. Learn more about [Agent identity concepts in Microsoft Foundry](../agents/concepts/agent-identity.md). | Foundry |

### Permission's model

Control Plane automatically discovers agents that users have access to. Because Control Plane aggregates information across resources within the subscription, different users may see different agents listed in the **Assets** page depending on the access level on each of those resources.

## Supported agent platforms

Control Plane automatically discovers agents in the following platforms:

> [!div class="checklist"]
> * Foundry agents, including [prompt-based agents](../../agents/concepts/overview.md), [workflows](../../agents/concepts/workflow.md), and [hosted-agents](../../agents/concepts/hosted-agents.md). 
> * [Azure SRE Agent](/azure/sre-agent/)
> * [Azure LogicApp agent loops](/azure/logic-apps/agent-workflows-concepts)

For agentic platforms not supported by Control Plane, you can [manually register the agent in a Microsoft Foundry project](register-custom-agent.md) to enable management.

### Foundry agents

Control Plane can help you manage agents across all your Foundry projects. When you create an agent or workflow in a Foundry project, the agent shows in the inventory page. Control Plane lists all the agents across all the projects within a subscription.

For each agent, you see:

* The latest version of the agent.

* Versions published as agent applications.

In this way, you can monitor versions consumed by your users and new versions under development. The following example shows multiple Foundry agents listed. Agent `format-agent` version 6 has been published, however, version 7 (latest) is still under development. 

:::image type="content" source="media/how-to-manage-agents/inventory-foundry-agent.png" alt-text="Screenshot of the inventory page listing multiple Foundry agents." lightbox="media/how-to-manage-agents/inventory-foundry-agent.png":::

> [!NOTE]
> Foundry classic agents and Azure OpenAI Assistants are not supported.

### Azure SRE agent

Azure SRE Agent helps you maintain the health and performance of your Azure resources through AI-powered monitoring and assistance. Agents continuously watch your resources for problems, provide troubleshooting help, and suggest remediation steps in a natural-language chat interface. Learn more about [Azure SRE Agent](/azure/sre-agent/).

Control Plane discovers Azure SRE agent resources in your subscription and shows them in the inventory page.

### Azure Logic Apps agent loop

Azure Logic Apps supports workflows that complete tasks by using agent loops with large language models (LLMs). An agent loop uses an iterative process to solve complex, multi-step problems. Learn more about [Workflows with AI agents and models in Azure Logic Apps](/azure/logic-apps/agent-workflows-concepts).

Control Plane discovers Azure Logic Apps resources containing agent loop workflows and lists them in the inventory page.

> [!NOTE]
> Observability features, including traces and metrics, are not supported in Azure Logic Apps agent loops.

### Custom agents

You can register custom agents—running in Azure compute services or other cloud environments—to gain visibility into their operations and control their behavior. You can register a custom agent in the Control Plane and develop the agent in the technology of your choice, both platform and infrastructure solutions.

Learn how to [register an agent in Control Plane](register-custom-agent.md) to enable management.

## Observe agents

Control Plane uses the Azure Application Insights associated with the resources hosting your agent to help you monitor and diagnose your agents. When such telemetry is available, Control Plane can:

* Compute runs and error rates
* Compute usage metrics, including token usage and cost
* Collect execution traces to diagnose behaviors

If you don't see such information for your agent, you need to configure Azure Application Insights.

> [!TIP]
> We strongly advise configuring Azure Application Insights for each of the resources hosting agents. For Foundry agents, Azure Applications Insights is configured per Foundry project. However, you can connect multiple Foundry projects to the same Azure Applications Insights to optimize resources.

Learn more about [Monitor agent health and performance across your fleet](monitoring-across-fleet.md).

### View traces

You can view traces and logs sent to Foundry. To view them:

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the agent.

1. Select the **Traces** tab.

1. You see one entry for each HTTP call made to the agent.

    :::image type="content" source="media/how-to-manage-agents/inventory-traces-list.png" alt-text="Screenshot of the inventory page listing multiple Foundry agents." lightbox="media/how-to-manage-agents/inventory-traces-list.png":::

1. To see the details, select an entry: 

    :::image type="content" source="media/how-to-manage-agents/inventory-traces-view.png" alt-text="Screenshot of a single trace with LLM calls." lightbox="media/how-to-manage-agents/inventory-traces-view.png":::

    > [!TIP]
    > Custom agents require extra configuration to see details including tools and LLMs spans. Learn more at [Instrument custom code agents](register-custom-agent.md#instrument-custom-code-agents).


## Lifecycle operations

Control Plane helps organizations to control agents to manage usage and infrastructure cost. Different agent platforms support different operations.

### Stop/start agents

Stopping an agent stops the infrastructure that is associated with this agent and moves the agent to the **Stopped** state.

Stopping an agent deprovisions its infrastructure, terminating existing runs and preventing new runs. Any workflows or resources connected to this agent can't access it.

The following platforms support stopping agents:

| Platform | Agent kind | Published | Supported actions | Notes        |
|----------|------------|-----------|-------------------|--------------|
| Foundry | Prompt agent<br />Workflow | No | None | Unpublished agents don't have dedicated deployments and they use the project's endpoint to receive requests. Hence, their lifecycle is attached to the project's lifecycle. To stop an unpublished prompt agent or workflow, you must delete them. |
| Foundry | Hosted agent | No | Start/stop | Stopping a hosted agent stops the deployment associated with it. Any compute attached to it is deallocated. |
| Foundry | Prompt agent<br />Workflow<br />Hosted agent | Yes | Start/stop | Stopping a published agent stops the deployment associated with it. It deallocates any compute attached. |
| Azure SRE | Interactive | NA | Start/stop | |
| Azure Logic Apps | Workflow | NA | Start/stop | You can start/stop an Azure Logic Apps agent loop by stopping the LogicApp resource that hosts them. Stopping a LogicApp resources stops all the workflows associated with it. |

To stop an agent:

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the agent you want to stop. The information panel appears.

1. Select **Update status** and then select **Stop**.

    :::image type="content" source="media/how-to-manage-agents/how-to-manage-agents-stop.png" alt-text="Screenshot of how to block incoming requests to the agent." lightbox="media/how-to-manage-agents/how-to-manage-agents-stop.png":::

1. Confirm the operation.

After you stopped the agent, the **Status** of the agent in Foundry shows as **Stopped**.

To start the agent:

1. Select **Update status** and then select **Start**.

1. Confirm the operation.

### Block and unblock agents

For [custom agents](register-custom-agent.md), Foundry doesn't have access to the underlying infrastructure where the agent runs, so start and stop operations aren't available. However, Foundry can block incoming requests to the agent, preventing clients from consuming it. This capability allows administrators to disable an agent if it misbehaves.

To block incoming requests to your agent:

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the agent you want to block. The information panel appears.

1. Select **Update status** and then select **Block**.

    :::image type="content" source="media/register-custom-agent/register-custom-agent-block.png" alt-text="Screenshot of how to block incoming requests to the agent." lightbox="media/register-custom-agent/register-custom-agent-block.png":::

1. Confirm the operation.

After you block the agent, the **Status** of the agent in Foundry shows as **Blocked**. Agents in the **Blocked** state run in their associated infrastructure but can't take incoming requests. Foundry blocks any attempt to interface with the agent.

To unblock the agent:

1. Select **Update status** and then select **Unblock**.

1. Confirm the operation.


## Related content

- [What is the Microsoft Foundry Control Plane?](overview.md)
- [Monitor agents across your fleet](monitoring-across-fleet.md)
