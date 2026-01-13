---
title: Develop prompt flow
titleSuffix: Azure Machine Learning
description: Learn how to develop a prompt flow and a chat flow in Azure Machine Learning studio.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar
ms.date: 09/22/2025
ms.custom:
  - ignite-2023
  - build-2024
  - sfi-image-nochange
ms.update-cycle: 365-days
---
# Develop prompt flow

Prompt flow is a development tool that streamlines the development cycle of AI applications that are powered by Large Language Models (LLMs). In this article, you learn how to create and develop a prompt flow and a chat flow in Azure Machine Learning studio.

As the momentum for LLM-based AI applications grows, prompt flow provides a comprehensive solution that simplifies the process of prototyping, experimenting, iterating, and deploying AI applications. By using prompt flow, you can:

- Orchestrate executable flows with LLMs, prompts, and Python tools through a visualized graph.
- Easily test, debug, and iterate your flows.
- Create prompt variants and compare their performance.

## Create and develop your prompt flow

To create a prompt flow, select **Prompt flow** in the Azure Machine Learning studio left navigation, and then select **Create** on the **Prompt flow** page.

On the **Create a new flow** screen, you can create a flow by:

- Creating a **Standard**, **Chat**, or **Evaluation** flow from a template.
- Cloning an available sample from the **Explore gallery**.
- Importing an existing flow from local files or a file share.

:::image type="content" source="./media/how-to-develop-flow/gallery.png" alt-text="Screenshot of prompt flow creation from scratch or gallery." lightbox ="./media/how-to-develop-flow/gallery.png":::

To create a flow, select **Create** or **Clone** on the flow card you want. On the next screen pane, you can change the new flow name if you want, and then select **Create** or **Clone**. The new flow opens in the authoring UI.

### Compute session

Before you begin authoring, start the compute session by selecting **Start compute session** at the top of the flow authoring page. A compute session is necessary for flow execution. The compute session manages the computing resources required for the application to run, including a Docker image that contains all necessary dependency packages.

:::image type="content" source="./media/how-to-develop-flow/start-compute-session.png" alt-text="Screenshot of start compute session in studio." lightbox ="./media/how-to-develop-flow/start-compute-session.png":::

### Authoring page

The compute session can take a few minutes to start. While the compute session is starting, inspect the parts of the flow authoring page.

- The **Flow** or *flatten* view on the left side of the page is the main working area where you author the flow. In the flatten view, you can edit nodes, tools, prompts, and inputs; run nodes or the whole flow; and define and view outputs.

- **Files** at top right shows the folder and file structure of the flow. Each flow has a folder that contains a *flow.dag.yaml* file, source code files, and system folders. You can add, edit, delete, upload, or download files for testing, deployment, or collaboration.

- The **Graph** view at lower right visualizes the flow structure. You can zoom in or out or use auto layout. You can't edit this view directly, but you can select a node to locate and edit it in the flatten view.

### Flow input and output

In the **Inputs** and **Outputs** sections, you can view, add or remove, and edit inputs and outputs.

- Flow input is the data passed into the flow as a whole. You define the input schema by specifying the name and type, and you set the value of each input to test the flow. You can reference the flow input in the flow nodes by using `${input.<input name>}`.

- Flow output is the data produced by the flow as a whole, which summarizes the results of flow execution. You can define the flow output value by referencing a single node output using the syntax `${<node name>.output}` or `${<node name>.output.<field name>}`. You can view and export the output result table after a flow run or batch run completes.

### Flow tools

In a flow, you can consume different kinds of tools, such as LLM, Python, Prompt, Serp API, and Content Safety. Selecting a tool adds a new node for that tool to the end of the flow. You must specify the node name and set necessary configurations. You can use the node controls to change the node's position in the flow.

#### Node inputs and outputs

The LLM and Prompt tools use Jinja as a templating language to dynamically generate the prompt. For example, you can use `{{}}` to enclose your input name instead of using fixed text, so it can be replaced on the fly.

You can set node **Inputs** and **Outputs** in the following ways:

- Set the input **Value** directly.
- Reference the flow input using `${input.<input name>}`.
- Reference the node output using `${<node name>.output}` or `${<node name>.output.<field name>}`.

After you finish composing a prompt or Python script, select **Validate and parse input** for the system to automatically parse the node input based on the prompt template and Python function input.

You can link nodes by referencing node output. For example, you can reference the LLM node output in the Python node input so the Python node consumes the LLM node output. In the **Graph** view, you can see the two nodes linked together.

#### LLM nodes

For an Azure OpenAI LLM node, you need to select **Connection**, **Api**, and **deployment_name**, and set the **Prompt**. You use the connection to securely store and manage secret keys or other sensitive credentials required for interacting with Azure OpenAI.

If you don't already have a connection, create it before you add the LLM node, and make sure the Azure OpenAI resource has a **chat** or **completion** deployment. For more information, see [Set up a connection](get-started-prompt-flow.md#set-up-a-connection) and [Create a resource and deploy a model using Azure OpenAI](/azure/cognitive-services/openai/how-to/create-resource).

#### Python nodes

To use the Python tool, you need to set the Python script, input value, and other configurations. A new Python node provides the following boilerplate Python function that defines inputs and outputs.

```python
from promptflow import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    return 'hello ' + input1
```

### Conditional control

Prompt flow offers conditional control, which lets you set conditions for the execution of any node in a flow.

Conditional control provides the capability to associate each node in a flow with an *activate config*. This configuration is a `when` statement that determines when a node should be executed. The power of this feature is realized in complex flows where the execution of certain tasks depends on the outcome of previous tasks. By using conditional control, you can configure your specific nodes to execute only when the specified conditions are met.

Set the activate config for a node by selecting the **Activate config** button in the node card. Add a **When** statement and set the condition. You can set the conditions by referencing the flow input or a node output. For example, you can set the condition `${input.<input name>}` or `${<node name>.output}` as specific values. If the condition isn't met, the node is skipped and the node status appears as **Bypassed**.

:::image type="content" source="./media/how-to-develop-flow/conditional-flow.png" alt-text="Screenshot of setting activate config to enable conditional control." lightbox ="./media/how-to-develop-flow/conditional-flow.png":::
## Test a flow

You can test a flow by running a single node or running the whole flow.

- To run a single node, select the **Run** icon on the node card. When the node run completes, you can quickly check the results in the node **Outputs** section.
- To run the whole flow, select **Run** at the top of the page.

### Flow outputs

After you select **Run** to execute the flow, you can see the run status in the banner at the top of the page. Select **View outputs** in the top banner or the top menu bar to view detailed input, output, flow execution, and orchestration information.

:::image type="content" source="./media/how-to-develop-flow/view-flow-output.png" alt-text=" Screenshot of view output button in two locations." lightbox ="./media/how-to-develop-flow/view-flow-output.png":::

After the flow run completes, you can select **View outputs** to check all historical outputs on the **Outputs** screen.

:::image type="content" source="./media/how-to-develop-flow/authoring-test-result.png" alt-text="Screenshot of flow test result." lightbox ="./media/how-to-develop-flow/authoring-test-result.png":::

#### Trace

Tracing is disabled by default, to enable tracing you need to set the environment variable `PF_DISABLE_TRACING` to `false`. One way you can do this is by adding the following to the python node:

```python
import os
os.environ["PF_DISABLE_TRACING"] = "false"
```

Select the **Trace** tab on the **Outputs** screen to see a graph that provides information about the duration and associated token cost of the flow. Select **flow** under **node name** to see detailed flow overview information in the right pane.

Expand **flow** and select any step to see detailed information for that step. You can see the duration of each node execution in the span tree. For more information, see [Trace Span Specification](https://microsoft.github.io/promptflow/reference/trace-span-spec-reference.html).

:::image type="content" source="./media/how-to-develop-flow/authoring-trace.png" alt-text=" Screenshot of trace detail." lightbox ="./media/how-to-develop-flow/authoring-trace.png":::

## Develop a chat flow

A *chat flow* is a specific type of prompt flow designed for conversational application development. Chat flow builds on the standard flow capabilities to provide enhanced support for chat inputs/outputs and chat history. By using chat flow, you can easily create a chatbot that handles chat input and output.

To create a chat flow, on the **Create a new flow** screen, select **Create** on the **Chat flow** card, or select **Chat** in the **Explore gallery** and clone one of the available flows.

In a chat flow authoring page, the chat flow is tagged with a **Chat** label to distinguish it from standard and evaluation flows. To test a chat flow, you select **Chat** at the top of the page to open a **Chat** box for conversation.

:::image type="content" source="./media/how-to-develop-flow/chat-authoring-layout.png" alt-text="Screenshot of chat flow authoring page." lightbox ="./media/how-to-develop-flow/chat-authoring-layout.png":::

### Chat input, chat output, and chat history

The most important elements that differentiate a chat flow from a standard flow are the *chat input*, *chat history*, and *chat output*. Chat history and chat input are required in chat flows.

- **Chat input** refers to the messages or queries submitted by users to the chatbot. Effectively handling chat input is crucial for a successful conversation, as it involves understanding user intentions, extracting relevant information, and triggering appropriate responses.

- **Chat history** is the record of all interactions between the user and the chatbot, including both user inputs and AI-generated outputs. Maintaining chat history is essential for keeping track of the conversation context and ensuring the AI can generate contextually relevant responses.

- **Chat output** refers to the AI-generated messages that are sent to users in response to their inputs. Generating contextually appropriate and engaging chat output is vital for a positive user experience.

A chat flow can have multiple inputs. In the chat flow **Inputs** section, you mark one of the inputs as the **Chat input**, and you populate the chat input value by entering a question in the **Chat** box.

:::image type="content" source="./media/how-to-develop-flow/flow-input-output.png" alt-text="Screenshot showing the test question in the Inputs section and the Chat box." lightbox ="./media/how-to-develop-flow/flow-input-output.png":::

### Manage chat history

To help you manage chat history, `chat_history` in the **Inputs** section is reserved for representing chat history. You can't manually edit `chat_history`.

Chat history is structured as a list of inputs and outputs. All interactions in the chat box, including user chat inputs, generated chat outputs, and other flow inputs and outputs, are automatically stored in chat history. The following code shows the structure of chat history.

```json
[
{
    "inputs": {
    "<flow input 1>": "xxxxxxxxxxxxxxx",
    "<flow input 2>": "xxxxxxxxxxxxxxx",
    "<flow input N>""xxxxxxxxxxxxxxx"
    },
    "outputs": {
    "<flow output 1>": "xxxxxxxxxxxx",
    "<flow output 2>": "xxxxxxxxxxxxx",
    "<flow output M>": "xxxxxxxxxxxxx"
    }
},
{
    "inputs": {
    "<flow input 1>": "xxxxxxxxxxxxxxx",
    "<flow input 2>": "xxxxxxxxxxxxxxx",
    "<flow input N>""xxxxxxxxxxxxxxx"
    },
    "outputs": {
    "<flow output 1>": "xxxxxxxxxxxx",
    "<flow output 2>": "xxxxxxxxxxxxx",
    "<flow output M>": "xxxxxxxxxxxxx"
    }
}
]
```
> [!NOTE]
> When you conduct tests in the **Chat** box, you automatically save chat history. For batch runs, you must include chat history within the batch run dataset. If there's no chat history available, set the `chat_history` to an empty list `[]` within the batch run dataset.

To retrieve past interactions, reference `chat_history` in your prompts. You can then refer to previous inputs and outputs to create contextually relevant responses. Incorporating chat history into your prompts is essential for creating context-aware and engaging chatbot responses.

You can use the Jinja language [for-loop](https://jinja.palletsprojects.com/en/3.1.x/templates/#for) grammar to display a list of inputs and outputs from `chat_history`.

```jinja
{% for item in chat_history %}
user:
{{item.inputs.question}}
assistant:
{{item.outputs.answer}}
{% endfor %}
```

### Test with the chat box

The **Chat** box provides an interactive way to test your chat flow by simulating a conversation with your chatbot. To test your chat flow by using the **Chat** box:

1. Select **Chat** to open the **Chat** sidebar.
1. Enter test questions in the chat box at the bottom of the screen to send them to the chatbot.
1. Review the chatbot's responses to ensure they're contextually appropriate and accurate.
1. Select **View outputs** at the top of the authoring page to quickly view and debug chat inputs, outputs, and history.
1. On the **Outputs** screen, select the **Trace** tab and then select **flow** to see detailed flow overview information in the right pane. Expand **flow** and select any step to see detailed information for that step.

:::image type="content" source="./media/how-to-develop-flow/authoring-chat-trace.png" alt-text=" Screenshot of Chat flow chat box experience." lightbox ="./media/how-to-develop-flow/authoring-chat-trace.png":::

## Related content

- [Submit batch run and evaluate a flow](how-to-bulk-test-evaluate-flow.md)
- [Tune prompts using variants](how-to-tune-prompts-using-variants.md)
- [Deploy a flow as a managed online endpoint for real-time inference](how-to-deploy-for-real-time-inference.md)
