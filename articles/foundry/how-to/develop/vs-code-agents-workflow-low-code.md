---
title: "Use and migrate declarative agent workflows with Microsoft Foundry Toolkit"
description: "Edit and test existing declarative workflows in Microsoft Foundry Toolkit for Visual Studio Code, then migrate them to Agent Framework code."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 09/10/2026
ms.reviewer: erichen
ms.author: rotabor
author: bobtabor-msft
ms.custom: doc-kit-assisted
#CustomerIntent: As a developer, I want to maintain and migrate existing declarative workflows so that I can move to a supported code-based runtime.
---

# Use and migrate declarative agent workflows with Microsoft Foundry Toolkit

Use Microsoft Foundry Toolkit for Visual Studio Code to work with existing
declarative workflows and prepare them for migration. You can test a saved
workflow, edit its exported YAML, and use GitHub Copilot to help convert the
definition to Microsoft Agent Framework code.

> [!IMPORTANT]
> Declarative workflows in Microsoft Foundry are in preview and retire on
> December 1, 2026. Use Microsoft Agent Framework for new workflow development.
> This retirement doesn't affect code-based orchestration in hosted agents.
> See the [workflow migration guide](../../agents/concepts/workflow.md#migration-guide)
> for supported migration paths.

## Prerequisites

- [Install Microsoft Foundry Toolkit for Visual Studio Code](install-foundry-toolkit-visual-studio-code.md).
- [Select the Foundry project](set-up-foundry-project-visual-studio-code.md)
  that contains your existing declarative workflow.
- Access to read and run that workflow and its referenced agents. To save
  changes, you also need permission to create an agent version in the project.
  See [Foundry role-based access control](../../concepts/rbac-foundry.md).
- For code conversion, access to
  [GitHub Copilot in Visual Studio Code](https://code.visualstudio.com/docs/copilot/overview).

## View a declarative agent workflow

Find the workflow in your project's consolidated agent list.

1. In the **Foundry Toolkit** view, under **My Resources**, confirm the selected
   Foundry project.
1. Select **Agents**, and then select the **Workflow** tab.
1. Select the workflow name to open its playground.
1. Use the version selector to choose the saved version you want to inspect.

The playground shows the workflow graph and a conversation area. The graph is
read-only. Use the exported YAML or the Foundry portal to edit the definition.

## Edit an existing workflow definition

Export the definition before you edit or migrate it. Keep a copy of the
original YAML so that you can compare it with your changes.

1. Open the existing workflow in the [Foundry portal](https://ai.azure.com/).
1. In the workflow designer, switch to the **YAML** view and copy or export the
   definition. For details, see
   [Export your workflow definition](../../agents/concepts/workflow.md#before-you-migrate-export-your-workflow-definition).
1. Save the definition in your local workspace with a name ending in
   `.workflow.yaml`, such as `support.workflow.yaml`.
1. Open the file in Visual Studio Code and edit the YAML.
1. Save the file. Local file changes don't update the workflow in Foundry.

### Save a new version of the existing workflow

Before retirement, you can deploy an edited definition to the same workflow.
Confirm the project and workflow name to avoid creating a different resource.

1. Confirm that the original workflow's project is selected in Foundry Toolkit.
1. With the `.workflow.yaml` file open, select **Deploy** in the editor toolbar.
1. In **Enter workflow name**, enter the name of the existing workflow.
1. Wait for the deployment success notification.
1. Reopen the workflow from **Agents** > **Workflow** and select the new version.

Deploying with an existing workflow name creates a new version. A different
name creates a separate workflow; don't use this path to start new workflow
development.

## Test a workflow in the playground

Test the saved version that you plan to maintain or migrate. Use the same
requests later to compare the migrated implementation.

1. Open the workflow's playground and select the required version.
1. On the **Playground** tab, select **New** to start a new playground session.
1. Enter a request that exercises the workflow and send it.
1. Review the response and the execution graph. Confirm that the expected
   agents, branches, and steps run.
1. Repeat with requests that exercise different branches, missing inputs, and
   any approval steps in your workflow.

The playground runs the saved Foundry workflow. It doesn't run unsaved changes
in your local YAML file or the code that Copilot generates.

## Convert a YAML workflow to Agent Framework code

Use the playground's code-generation action to ask GitHub Copilot to convert
the selected workflow definition. Generated code is a starting point that you
must review and test.

1. In the workflow playground, select the version to migrate.
1. Select **Generate Code**.
1. Choose **Python** or **C#**.
1. Review the conversion request in Copilot Chat and follow its prompts to
   generate the code.
1. Review the generated project, dependencies, model connections, tools, and
   authentication configuration.
1. Compare its orchestration with the exported YAML. Check branching,
   variables, agent calls, and human approval steps.
1. Run the code locally and test it with the requests you used for the original
   workflow. Use Agent Inspector to inspect execution.
1. When the code behaves as required, follow
   [Create hosted agents](vs-code-agents-workflow-pro-code.md)
   to prepare a supported hosted-agent project, deploy it, and test the
   deployed version.

Code conversion doesn't deploy a hosted agent or guarantee equivalent
behavior. Keep the original definition until you complete migration and
confirm that dependent applications use the replacement.

For other migration choices, including Agent Framework declarative YAML,
Azure Logic Apps, and direct A2A connections, see the
[workflow migration guide](../../agents/concepts/workflow.md#migration-guide).

## Related content

Use these guides to choose and complete your migration:

- [Create an agent with Microsoft Foundry Toolkit](create-agent-visual-studio-code.md)
- [Microsoft Agent Framework workflows](/agent-framework/workflows/)
- [Hosted agent concepts](../../agents/concepts/hosted-agents.md)
