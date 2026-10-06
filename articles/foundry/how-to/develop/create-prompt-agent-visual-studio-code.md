---
title: "Create a prompt agent with Microsoft Foundry Toolkit for Visual Studio Code"
description: "Create, test, and version prompt agents with Agent Builder in Microsoft Foundry Toolkit. Add tools, review conversations, evaluate, and generate client code."
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
#CustomerIntent: As a developer, I want to create and refine a prompt agent in Agent Builder so that I can integrate a tested configuration into my application.
---

# Create a prompt agent with Microsoft Foundry Toolkit for Visual Studio Code

Use Agent Builder in Microsoft Foundry Toolkit for Visual Studio Code to
configure a prompt agent's model, instructions, and tools. Test the agent in
the playground, save changes as versions, and generate client code to call it
from an application.

This article starts with prompt agents saved in Foundry. Agent Builder also
supports [locally stored prompts](#work-with-local-prompts), which have
different storage, tool, and evaluation options. For code-based alternatives,
see [Create an agent](create-agent-visual-studio-code.md).

## Prerequisites

- [Install Microsoft Foundry Toolkit for Visual Studio Code](install-foundry-toolkit-visual-studio-code.md).
- [Select a Foundry project](set-up-foundry-project-visual-studio-code.md).
  You need permission to create agents and use the project's models and tools.
  See [Foundry role-based access control](../../concepts/rbac-foundry.md).
- A model deployment in that project. See
  [Set up Foundry resources](../../tutorials/quickstart-create-foundry-resources.md).

Local prompt development doesn't require a Foundry project unless you use
Foundry resources.

## Create a prompt agent

Start with a model and instructions, then save and test the agent before
adding tools.

1. In the **Foundry Toolkit** view, select **Developer Tools** > **Build** >
   **Create Agent**.
1. Select **Build an agent** to open Agent Builder.
1. Under **Basic Information**, enter an **Agent name**. Start and end the name
   with a letter or number. You can use hyphens between them.
1. Select a Foundry-hosted model from **Model**. Use **Browse models** if you
   need to add a model.
1. In **Instructions**, describe the task, required behavior, and expected
   response. For example, ask the agent to summarize a software issue by
   identifying the reported problem, reproduction steps, and expected
   behavior. Tell it to ask for missing information instead of inventing details.
1. Select **Save to Foundry**.
1. On the **Playground** tab, enter a request and select **Send message**.
   Ask a follow-up question to test the conversation.
1. Review whether the response follows your instructions. Refine the
   instructions, save, and repeat as needed.

   :::image type="content" source="../../media/how-to/create-prompt-agent-vs-code/agent-builder.png" alt-text="Screenshot of Agent Builder with a saved Foundry prompt agent, version selector, model, instructions, tool, and playground conversation." lightbox="../../media/how-to/create-prompt-agent-vs-code/agent-builder.png":::

If Developer Tools uses **Group by Resource**, **Create Agent** is under
**Agent Dev Tools** instead of **Build**. Another entry point is
**My Resources** > **Agents** > **Prompt Agent** > **Add Prompt Agent**.
Select an existing agent in that list to edit it.

### Choose where to save

The available save actions depend on the selected model and tools.

| Configuration | Save destination |
| --- | --- |
| Foundry-hosted model without tools. | **Save to Foundry**, with **Save to Local** available in the save menu. |
| Foundry-hosted model with Foundry tools. | **Save to Foundry**. |
| A model from another provider, or a configuration with local tools. | **Save to Local**. |

The **Microsoft Foundry** and **Local** badges show where the agent is stored.
A locally stored prompt can still call a cloud model. Local storage doesn't
mean that inference runs on your machine.

## Save drafts and versions

Agent Builder separates local recovery drafts from saved agent versions.

| Action | Result |
| --- | --- |
| Edit the configuration. | Agent Builder stores a local recovery draft. This action doesn't create a Foundry version. |
| Run a new, unsaved agent. | Agent Builder validates the agent name and model, and saves the agent before the first run. It prefers Foundry when the configuration supports that destination. |
| Select **Save to Foundry** after editing a saved Foundry agent. | Agent Builder saves the configuration as a new version in the project. |

If Agent Builder finds a recovery draft, choose **Restore Draft** or **Discard**.
Save important changes explicitly before switching agents or versions.

You can test unsaved changes to an existing Foundry agent. That run uses the
edited configuration rather than a saved agent-version reference. Save before
you rely on version-linked conversations, tracing, or generated client code.

> [!IMPORTANT]
> **Save to Foundry** saves an agent version. It doesn't publish an agent
> application with a stable application endpoint. For that separate operation,
> see [Publish an agent application](../../agents/how-to/agent-applications.md).

### Select an agent version

Use the version selector next to the agent name to load a saved version.
Foundry agent versions are immutable. To keep edits made from an earlier
version, select **Save to Foundry** to create a new version.

The selected version determines the conversation history shown in Agent
Builder and the version referenced by generated client code. For service
versioning details, see
[Save changes as versions](../../agents/concepts/development-lifecycle.md#save-changes-as-versions).

## Add tools to a Foundry agent

Tools connect the agent to information and actions outside the model. Available
tools depend on the model, your permissions, and the resources in your project.
Use [Tool Catalog](https://code.visualstudio.com/docs/intelligentapps/tool-catalog)
to configure shared connections and authentication, then attach them in Agent Builder.

1. Open a saved Foundry agent on the **Playground** tab.
1. In **Tool**, select **+** > **Add tools**.
1. In **Select a tool**, choose a connection from **Configured**, or use
   **Catalog** to find a tool.
1. Complete the required configuration, then select **Add Tool**.
1. Select **Save to Foundry**.
1. Send a request that requires the tool, and review its inputs and results.
   If the agent requests approval, select **Approve** or **Deny** for that call.

To review the tool-call approval settings for an MCP tool, open its options and select **Configure**. You can require approval, approve all tools automatically, or approve specific tools automatically. Review the choice before saving.

Approval settings don't grant access to the underlying service. For service permissions, see [Agent identity concepts](../../agents/concepts/agent-identity.md).

## Use a toolbox (preview)

A [toolbox](../../agents/concepts/toolbox-overview.md) groups reusable tools
behind a managed MCP endpoint. Skills and tool search are preview features.

> [!NOTE]
> Toolbox integration in prompt agents is in preview and off by default.
> In Visual Studio Code settings, enable
> `windowsaistudio.enableToolboxInPromptAgent` to show toolbox attachment controls.

An agent uses either a toolbox or individual Foundry tools. Attaching a
toolbox replaces its individual tools. With a toolbox attached, **Add tools**
adds tools inside that toolbox.

Toolbox edits are staged until you save the agent, when they create a new
toolbox version. Toolboxes are shared resources; review both the toolbox and
agent changes before saving.

1. Open a saved Foundry agent.
1. In **Tool**, select **+** > **Browse toolboxes**.
1. Select a toolbox, and review its version, tools, and skills.
1. Select **Add**.
1. Expand the toolbox card to inspect its contents and review approval settings.
1. Select **Save to Foundry**, then test a request that uses its tools.

   :::image type="content" source="../../media/how-to/create-prompt-agent-vs-code/select-toolbox.png" alt-text="Screenshot of the Select a toolbox dialog showing toolbox names, versions, and tool and skill counts." lightbox="../../media/how-to/create-prompt-agent-vs-code/select-toolbox.png":::

You can also select **Add to Prompt Agent** from the Toolbox resource list.
For toolbox creation and shared connections, see
[Tool Catalog](https://code.visualstudio.com/docs/intelligentapps/tool-catalog).

### Manage an attached toolbox

Use the toolbox card's **More options** menu, and then save the agent after you make changes.

| Action | Effect |
| --- | --- |
| **Configure** | Change tool-call approval settings for this agent. |
| **Switch version** | Select another version of the attached toolbox. |
| **Replace** | Choose a different toolbox. |
| **Remove** | Detach the toolbox from this agent. |
| **Opt out** | Keep its tools as individual agent tools. The agent no longer has access to toolbox skills, tool search, and versioning and reuse as a set. |

## Connect another agent with A2A (preview)

Agent-to-Agent (A2A) connections let a prompt agent invoke an A2A-compatible
agent as a tool. You can attach one directly or through a toolbox. Direct
attachment doesn't require the toolbox opt-in setting.

1. Open a saved Foundry agent.
1. In **Tool**, select **+** > **Add agent (A2A)**.
1. In **Connect an A2A agent**, choose the appropriate tab.

   | Tab | What to provide |
   | --- | --- |
   | **Configured** | Select an existing A2A connection. This tab appears when configured connections exist. |
   | **Catalog** | Select an agent from the Foundry account catalog. Complete the agent-card and authentication steps when prompted. |
   | **Custom** | Enter a name, a valid HTTPS endpoint, and the agent-card path. Select **Authenticate when retrieving agent card** if required. |

1. Complete the dialog to connect or add the agent.
1. Select **Save to Foundry**, then test a request that requires the connection.

   :::image type="content" source="../../media/how-to/create-prompt-agent-vs-code/connect-agent-to-agent.png" alt-text="Screenshot of the Custom tab in Connect an A2A agent, with name, HTTPS endpoint, agent-card path, and authentication fields." lightbox="../../media/how-to/create-prompt-agent-vs-code/connect-agent-to-agent.png":::

For endpoint setup, agent cards, identity options, and permissions, see
[Enable an A2A endpoint](../../agents/how-to/enable-agent-to-agent-endpoint.md).

## Review conversations and switch agents

The **Playground** contains the current test conversation. Select
**Clear all messages** to start a fresh conversation.

For a saved Foundry agent, select **Conversations** to review history for the
selected version. Select a conversation to inspect its messages and response
details. Opening history doesn't resume that conversation in the playground.

:::image type="content" source="../../media/how-to/create-prompt-agent-vs-code/conversations.png" alt-text="Screenshot of the Conversations tab showing conversation IDs, status, token usage, and start times." lightbox="../../media/how-to/create-prompt-agent-vs-code/conversations.png":::

Use the agent selector at the top of Agent Builder to switch between local
prompts and Foundry prompt agents. Check the storage badge and version after
switching. The **Conversations** tab is available for saved Foundry agents,
not local prompts.

## Generate and improve instructions

Use **Generate** to draft instructions from a task description or **Improve**
to revise existing instructions. When the field is empty, **Inspire me** can
provide a starting idea.

1. Select a model that supports instruction generation.
1. Under **Instructions**, select **Generate** if the field is empty, or
   **Improve** if it contains instructions.
1. Describe the task or change. For an existing Foundry agent, improvement
   suggestions are optional.
1. Select **Generate** or **Improve** in the dialog.
1. Review the revised instructions and test representative requests.
1. Select **Save to Foundry** to keep the configuration.

For saved Foundry agents, these actions use Foundry Prompt Optimizer. If the
optimization API doesn't support the model, the Toolkit falls back to standard
prompt generation when supported. Selecting a Foundry model in a new draft
doesn't by itself make the draft a saved Foundry agent.

## Evaluate a Foundry prompt agent

Save the configuration you want to evaluate, and then select **Evaluation**.

- Select **Scaffold Evaluation Code** to generate a local Python evaluation project. Follow the generated instructions to configure and run it.
- Select the **Foundry** link for guided evaluation setup.

Review the generated evaluation configuration before running it. The scaffold identifies the agent by name; don't assume it pins the version you selected in Agent Builder.

This tab differs from the local prompt dataset view. For service evaluation guidance, see [Evaluate your agents](../../observability/how-to/evaluate-agent.md).

## Generate client code

After saving a Foundry agent, use the **View Code** menu to call it from an
application.

| Action | Output |
| --- | --- |
| **View Code** | A Python project that calls the existing agent. Choose a folder, then follow its `README.md` for dependencies, configuration, and authentication. |
| **View Snippets** | A Python snippet in an editor that calls the existing agent. |

Both outputs reference the selected saved version. Save your edits before
generating code if the application needs the revised configuration.

Client code doesn't convert a prompt agent into a hosted agent. For direct
SDK use, see the [prompt-agent quickstart](../../agents/quickstarts/prompt-agent.md).

## Work with local prompts

Choose local storage to use a model from another provider or test local tools.
Select a model, enter instructions, and select **Save to Local**. With a
Foundry model, use the save menu when local storage is available.

Use **Save to Local** to keep local changes. Local saves don't create Foundry
versions or Foundry conversation-history records.

### Connect local tools

For a local prompt, select **Tool** > **+** > **MCP Server** to choose a server
and its tools. For configuration and runtime requirements, see
[Connect a local MCP server](https://code.visualstudio.com/docs/intelligentapps/tool-catalog#_connect-a-local-mcp-server-tool).

To test a function schema without implementing an external service:

1. Select **Tool** > **+** > **Custom Tool**.
1. Choose **By Example** or **Upload Existing Schema**.
1. Provide the schema, name, and description, then add the tool.
1. Enter a mock response in the tool card.
1. Run the prompt and inspect how the model uses the response.

A mock response doesn't call an external API. A configured MCP server can
execute its tools.

### Configure structured output

For a local prompt with a model that supports structured output:

1. Open **Settings** next to the model selector.
1. Under **Structure Output**, select `json_schema`.
1. In **Select JSON Schema**, choose **Use Example** or **Upload File**.
1. Review the schema and select **Select**.
1. Save the local prompt and run a request to inspect its output.

Available formats depend on the model. These steps apply to local prompt
execution, not the response schema of a saved Foundry prompt agent.

### Evaluate local prompts with dataset variables

For a saved local prompt, the **Evaluation** tab provides dataset-based evaluation. Use variables in instructions to run the same prompt with different dataset values.

For example, `Summarize the issue for {{audience}}.` uses a dataset column named `audience`. Supply a value for each test case. The local batch runner substitutes that value when it runs the prompt.

The Agent Builder playground doesn't have a separate Variables panel. For dataset import, evaluators, and result comparison, see [Evaluate models, prompts, and agents](https://code.visualstudio.com/docs/intelligentapps/evaluation).

### Generate code for a local prompt

Select **View Code** to generate model integration code. Available SDK, authentication, and language choices depend on the provider and model. These options differ from the Foundry agent client project and snippet actions.

## Related content

Use these guides to develop and publish your agent:

- [Create an agent with Microsoft Foundry Toolkit](create-agent-visual-studio-code.md)
- [Agent development lifecycle](../../agents/concepts/development-lifecycle.md)
- [Publish an agent application](../../agents/how-to/agent-applications.md)
