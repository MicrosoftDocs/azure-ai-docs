---
title: "Debug agents with Agent Inspector in Microsoft Foundry Toolkit"
description: "Connect to a local agent in Microsoft Foundry Toolkit for Visual Studio Code, inspect responses and tool calls, and export diagnostic events."
author: MuyangAmigo
ms.author: junjieli
ms.service: microsoft-foundry
ms.subservice: foundry-sdk
ms.topic: how-to
ms.date: 09/17/2026
ai-usage: ai-assisted
---

<!-- Adapted from Microsoft Corporation's vscode-docs agent-inspector.md at
https://github.com/microsoft/vscode-docs/blob/33dbfb5b51f12069af24a3315a257e5c2f4a87eb/docs/intelligentapps/agent-inspector.md.
Source text and accompanying screenshots are licensed under CC BY 3.0 US:
https://creativecommons.org/licenses/by/3.0/us/. Adapted for Microsoft Learn. -->

# Debug agents with Agent Inspector in Microsoft Foundry Toolkit

Agent Inspector in Microsoft Foundry Toolkit for Visual Studio Code lets you send requests to a local agent, inspect model and tool activity, and debug your code. Use it to investigate unexpected responses before you deploy a change.

This workflow is useful for [hosted agents](../../agents/concepts/hosted-agents.md), which run your custom code in Foundry Agent Service. Local inspection helps you debug that code. Before production use, also test the deployed agent with its runtime identity, configuration, and network access.

In this article, you connect to a local agent, investigate a request, and save diagnostic events. The main path uses the Responses protocol. Available views depend on the protocol and diagnostics that your agent server provides.

## Prerequisites

- Visual Studio Code with the current public Foundry Toolkit extension. See [Install Foundry Toolkit](install-foundry-toolkit-visual-studio-code.md).
- A local agent project with its dependencies, model configuration, and credentials set up. To start from a sample, follow the [hosted-agent quickstart](../../agents/quickstarts/quickstart-hosted-agent.md?pivots=vscode) through local testing.
- The debugger required by your project. The Python sample uses the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and `debugpy`. Other languages and samples have different requirements.

For an existing project, the [Foundry Toolkit Copilot tools](https://code.visualstudio.com/docs/intelligentapps/copilot-tools#agent-code-gen-tool) can help prepare the configuration. Review the generated files and follow the project's `README.md`. Don't replace its launch files with a generic configuration.

> [!IMPORTANT]
> A local agent can call cloud models and live tools. Use non-sensitive test inputs, check tool permissions, and account for charges from configured services. Inspector doesn't replace tools with mocks.

## Connect and debug

Start the agent server before you connect Inspector. Use your project's generated launch configuration to align the server, working directory, interpreter, and debugger.

1. Start the agent with its documented debug configuration. For the hosted-agent Python sample, select **Debug Local Agent HTTP Server** and press **F5**.
1. If Inspector isn't open, select **Foundry Toolkit** in the Activity Bar, then **Developer Tools** > **Build** > **Agent Inspector**.
1. Check the endpoint in the Inspector header. The current Python scaffold uses `http://localhost:8088`. For a different server port, select the pencil button beside the endpoint, enter the port, and select **Connect**.
1. Confirm that the header shows **Connected**. Inspector automatically detects the Responses or Invocations protocol when the endpoint is reachable.
1. Set a breakpoint in your agent code and send a message in the playground. Inspect variables when execution pauses, then continue and review the response.

:::image type="content" source="../../media/how-to/vs-code-agent-inspector/connect-and-debug.png" alt-text="Screenshot of the local agent debug configuration and Agent Inspector connected to localhost on port 8088 with a successful response." lightbox="../../media/how-to/vs-code-agent-inspector/connect-and-debug.png":::

Opening Inspector alone doesn't launch a server or attach a debugger. The generated Python configuration uses port 5679 for the debugger and port 8088 for agent HTTP requests. These ports are separate from the [OTLP tracing ports](vs-code-tracing.md#collector-endpoints).

### Connect to a generic Responses endpoint

Inspector can connect to a local generic Responses endpoint without the full development diagnostics interface. You can inspect the Responses events that the server sends, but the workflow graph and its input and output view aren't available.

A successful connection doesn't mean that the server supplies source locations, token usage, or reasoning.

### Send an HTTP invocation

Use HTTP invocations when your agent accepts a custom request body rather than a conversational message. The server's request format and response protocol determine how Inspector sends and displays the result.

1. Connect to your running HTTP invocations server. Inspector detects the protocol automatically.
1. Enter the request body required by your agent. If the server exposes a compatible OpenAPI specification, Inspector can fill in an example. Review it before sending, or follow the sample's request format if no example is available.
1. Select the **Request settings** gear beside the input to set **Content-Type** and **Accept** as required by the server. For example, use `application/json` for a JSON body and `text/event-stream` when the server supports a streaming response.
1. Select **Send** and inspect the response status and body.
1. Switch between **Preview** for formatted output and **Raw** for the underlying response. The details pane also includes **I/O** and **LLM Calls**. Model, tool, and token details depend on recognized server events, so not every response fills every tab.

Inspector handles a normal HTTP response, a stream of server-sent events, or an asynchronous response. For an asynchronous `202 Accepted` response, it polls the invocation until completion or failure. Selecting a response format doesn't add streaming or asynchronous support to your server.

For a streaming response, **Stop** disconnects the client stream. For a polled invocation, **Cancel** sends a cancellation request to the server. Neither action guarantees that the agent process or an external tool operation has stopped.

This view isn't a WebSocket client. Activity Protocol samples use a different playground. See [Choose another protocol or sample](https://code.visualstudio.com/docs/intelligentapps/hosted-agents#choose-another-protocol-or-sample) for the appropriate local testing path.

## Use the Inspector

Start with a request that exercises the behavior you want to understand. For a weather tool, for example, ask for information that requires that tool, rather than a general answer the model can produce without it.

1. Send the request in the playground and review the streaming response.
1. Use the details tabs to find the slow or failing operation.
1. Inspect the relevant event or tool call, change your code or configuration, and repeat the request.

Press **Enter** to send or **Shift+Enter** to add a newline. To recall an earlier request, place the caret at the start of the input and press **Up Arrow**. Press **Down Arrow** at the end to move toward newer requests and return to your unsent draft.

You can edit a recalled request before sending it. Input history is a convenience within Inspector, not a durable store of saved prompts.

| View | Use it to |
| --- | --- |
| **Overview** | Follow the latency waterfall and ordered run timeline. Select all runs or one run to distinguish model and tool activity from time between runs. |
| **Tokens** | Review reported input and output token usage. Missing usage data isn't a zero-token result. |
| **Events** | Inspect parsed Responses events, including errors, function calls, and results. Search by event type or JSON content and filter by category. |
| **Tools** | Inspect tool calls grouped by response run, including status, call ID, arguments, and results. |

The response footer shows model, duration, token usage, and timestamp information when provided. Reasoning text and reasoning summaries appear in separate collapsible sections when the agent emits them. Inspector doesn't generate missing reasoning or expose information that the model provider doesn't return.

### Inspect tools and permissions

Use **Tools** to check whether the agent called the expected tool with the expected arguments and received a result. A successful model response doesn't prove that a tool ran. If your code uses a mock, the displayed result is still a mock result.

:::image type="content" source="../../media/how-to/vs-code-agent-inspector/inspect-tools.png" alt-text="Screenshot of the Tools tab with calls grouped by run and an expanded tool call showing its arguments and result." lightbox="../../media/how-to/vs-code-agent-inspector/inspect-tools.png":::

When a response pauses for Model Context Protocol (MCP) approval or OAuth consent, pending requests appear above the message input. Grant only the access you intend to allow.

For an MCP tool call, select **Show arguments**, review the inputs, and then select **Approve** or **Deny**. **Approve all** and **Deny all** apply to the pending requests, not a permanent tool approval policy.

For OAuth consent, complete both browser authorization and Inspector confirmation:

1. Select **Open consent** for the pending request.
1. Complete authorization in the browser, return to Inspector, and select **Consent done**. To decline authorization, select **Cancel** instead.
1. Resolve the remaining consent requests. Use **All done**, when available, only after completing authorization for all opened requests.

Opening a consent page alone doesn't resume the request. Inspector waits for a decision on each pending consent before checking the server again. Requests can reappear if the server still needs authorization.

Check the subsequent tool result, not only the approval, to confirm completion. For connection and authentication setup, see [Tool Catalog](https://code.visualstudio.com/docs/intelligentapps/tool-catalog). Don't change tool credentials or permissions solely to make a diagnostic error disappear.

### Inspect workflows and source code

For supported Microsoft Agent Framework workflows, the development server can provide workflow diagnostics and source locations. Inspector uses this information to show the execution graph and help you navigate to your code.

1. Select a workflow node to inspect the available inputs and outputs.
1. Double-click the node to open its source location.
1. Set a breakpoint and repeat the request to inspect the operation in the debugger.

You can test LangGraph workflows in the playground, but workflow visualization isn't supported for them. A server without workflow metadata can still return useful response events.

### Investigate failures with Copilot

Use the error actions in **Events** to prepare a focused request for GitHub Copilot instead of copying the entire conversation.

1. Find the failed event and review its details for sensitive content before sharing them.
1. Select **Fix** beside the failed event to prepare a prompt for that failure. For several failures, narrow the list with search and category filters, then select **Resolve with Copilot**. This action includes the visible failures.
1. Review the prepared prompt in GitHub Copilot Chat before sending it. Review any proposed changes, then rerun the original agent request to confirm the result.

These actions don't require the OTLP collector. Preparing a diagnostic prompt doesn't fix the agent or rerun the failed operation.

:::image type="content" source="../../media/how-to/vs-code-agent-inspector/diagnostic-events.png" alt-text="Screenshot of the Events tab with failed responses, search and filter controls, export actions, and diagnostic details prepared in Copilot Chat." lightbox="../../media/how-to/vs-code-agent-inspector/diagnostic-events.png":::

### Save diagnostic events

Save an event snapshot to compare a failure with a later run or share a focused reproduction.

1. In **Events**, narrow the list with the search field and category filter.
1. Select **Copy visible events** to copy the filtered events as JSONL. Alternatively, select **Download visible events** to open the export in VS Code.
1. For the opened export, use **File** > **Save As** to save a copy in a location you control before closing the document. The opened export is a temporary file, not a permanent download.

The snapshot contains the events visible when you select the action, not future events from the running agent. It doesn't save an agent version, deploy code, or create cloud trace history.

> [!CAUTION]
> Events can include prompts, responses, tool arguments, results, and error details. Review and redact sensitive content before saving or sharing an export.

### Start a fresh conversation

Select **Clear Chat** to start a new conversation and clear the chat, Events, and Details state. Export any diagnostic events you need first. Refreshing the same connected agent preserves its inspection state, while changing agents clears stale state.

For Responses, **Clear Chat** is disabled while a response actively streams. It remains available when the turn pauses for approval or consent. It isn't a general command to stop your agent.

Don't rely on local Inspector state as a durable conversation archive. The server owns conversation persistence, which can differ between local development and a deployed hosted agent. Clearing Inspector doesn't delete traces already collected locally or stored in Application Insights.

## How Inspector and tracing differ

Inspector communicates with your local server over HTTP and streams response events. A compatible development server also supplies a separate diagnostics stream for workflow details and source navigation. The debugger attaches to your running process independently.

These live diagnostics don't require the local OTLP collector. Inspector's **Traces** tab opens the separate tracing viewer. It doesn't turn protocol events into stored OpenTelemetry spans.

To collect spans for later analysis, configure [local tracing](vs-code-tracing.md#set-up-instrumentation). For deployed agents, use [hosted-agent traces](vs-code-tracing.md#view-hosted-agent-traces).

After local testing, [deploy the hosted agent](vs-code-agents-workflow-pro-code.md#deploy-the-hosted-agent). Test it separately because its identity, environment, and network access differ from your local process.

## Troubleshooting

| Issue | What to check |
| --- | --- |
| Inspector can't connect. | Check the agent terminal for startup errors. Confirm the interpreter, dependencies, and HTTP port, then reconnect to the port the server reports. Opening Inspector doesn't start the process. |
| A request succeeds but breakpoints aren't hit. | Confirm the debugger is attached to the process serving the request and uses the correct source directory. For Python, see [debugging troubleshooting](https://code.visualstudio.com/docs/python/debugging#troubleshooting). |
| The graph or source navigation is missing. | Confirm that the server and workflow provide development diagnostics and source locations. Generic Responses inspection doesn't provide these capabilities. LangGraph workflows work in the playground without workflow visualization. |
| Tool results are missing. | Check **Events** for failures and pending approvals. Confirm that the request requires a tool and that the tool is configured and reachable. |
| Token or reasoning details are missing. | Check what the model and server emit. Inspector can only display the information they provide. |
| Remote images are blocked. | Select **Load Remote Images** only if you want Inspector to fetch them from remote hosts. This display permission isn't a tool approval. Unsupported URLs or content can still fail to load. A missing image doesn't necessarily mean the agent request failed. |
| The response stream is interrupted. | Review the partial response and failure details. Reconnect if needed and review pending approvals before retrying. A retry can repeat live tool actions. |
| Inspector has events but the tracing viewer is empty. | Protocol events and OTLP spans are different. [Configure instrumentation and start the collector](vs-code-tracing.md#set-up-instrumentation). |

## Related content

- [Collect and inspect traces in Foundry Toolkit](vs-code-tracing.md).
- [Create hosted agent workflows in VS Code](vs-code-agents-workflow-pro-code.md).
- [Launch the browser-based Agent Inspector with the Azure Developer CLI](../../agents/how-to/agent-inspector.md).
