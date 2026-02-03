---
title: Build a workflow in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how to build a workflow in Microsoft Foundry to orchestrate agents, add nodes, and use Power Fx and JSON schema outputs.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - build-2025
  - code01
  - pilot-ai-workflow-jan-2026 
ms.topic: how-to
ms.date: 11/05/2025
ms.reviewer: fniedtner
ms.author: ssalgado
manager: nitinme
author: ssalgadodev
ai-usage: ai-assisted
#customer intent: As a developer, I want to learn how to build a workflow so that I can solve real-world problems collaboratively.
---

# Build a workflow in Microsoft Foundry

Workflows are UI-based tools in Microsoft Foundry. Use them to create declarative, predefined sequences of actions that orchestrate agents and business logic in a visual builder.

Workflows enable you to build intelligent automation systems that seamlessly blend AI agents with business processes in a visual manner. Traditional single-agent systems are limited in their ability to handle complex, multifaceted tasks. By orchestrating multiple agents, each with specialized skills or roles, you can create systems that are more robust, adaptive, and capable of solving real-world problems collaboratively.

## Prerequisites

- [!INCLUDE [azure-subscription](../../../includes/azure-subscription.md)]
- A project in Microsoft Foundry. For more information, see [Create projects](../../../how-to/create-projects.md).
- Access to create and run workflows in your Foundry project. For more information, see [Azure role-based access control (RBAC) in Foundry](../../../concepts/rbac-foundry.md).

## When to use workflows

Use workflows when you want to:

- Orchestrate multiple agents in a repeatable process.
- Add branching logic (for example, if/else) and variable handling without writing code.
- Create human-in-the-loop steps (for example, approvals or clarifying questions).

If you want to edit workflow YAML in Visual Studio Code or run workflows in a local playground, see:

- [Work with Declarative (Low-code) Agent workflows in Visual Studio Code](../how-to/vs-code-agents-workflow-low-code.md)
- [Work with Hosted (Pro-code) Agent workflows in Visual Studio Code](../how-to/vs-code-agents-workflow-pro-code.md)

## Workflow concepts

To create a workflow in Foundry, you can begin with a blank workflow or select one of the templates of predefined orchestration patterns:

| Pattern    | Description                                                        | Typical use case                                         |
|------------|--------------------------------------------------------------------|----------------------------------------------------------|
| Human in the loop  | Asks the user a question and awaits user input to proceed | Creating approval requests during workflow execution and waiting for human approval, or obtaining information from the user |
| Sequential | Passes the result from one agent to the next in a defined order   | Step-by-step workflows, pipelines, or multiple-stage processing |
| Group chat    | Dynamically passes control between agents based on context or rules| Dynamic workflows, escalation, fallback, or expert handoff scenarios |

For more information, see [Microsoft Agent Framework workflow orchestrations](/agent-framework/user-guide/workflows/orchestrations/overview).

## Create a workflow

The following steps show you how to create a sequential type of workflow as an example:

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]

1. On the upper-right menu, select **Build**.

1. Select **Create new workflow** > **Sequential**.

1. Assign an agent to the agent nodes by selecting each agent node in the workflow and either selecting the desired agent or creating a new one. For more information, see [Add agents to your workflow](#add-agents-to-your-workflow) later in this article.

1. Select **Save** in the visualizer to save the changes.

   > [!IMPORTANT]
   > Workflows aren't saved automatically. Select **Save** every time you want to save changes to your workflow.

1. Select **Run Workflow**.

1. Interact with the workflow in the chat window.

1. Optionally, add new nodes to your workflow. The next section in this article provides information about nodes.

## Verify your workflow run

After you select **Run Workflow**, verify that:

- Each node completes in the visualizer.
- You see the expected responses in the chat window.
- Any variables you save (for example, JSON output from an agent node) contain the values you expect.

## Add nodes to your workflow

Nodes define the building blocks of your workflow. Common node types include:

- **Agent**: Invoke an agent.
- **Logic**: Use *if/else*, *go to*, or *for each*.
- **Data transformation**: Set a variable or parse a value.
- **Basic chat**: Send a message or ask a question to an agent.

When you select a prebuilt workflow, a workflow of nodes appears in the builder. Each node corresponds to a specific action or component, and it performs a step in sequence. You can modify the order of the nodes by selecting the three dots on a node and then selecting **move**. You can add new nodes by selecting the plus (**+**) icon in the workspace.

## Add agents to your workflow

You can add any Foundry agent from your project to the workflow. Agent nodes also allow you to create new agents and give them customized capabilities by configuring their model, prompt, and tools.

For advanced options and comprehensive information about agent creation, go to the **Foundry Agent** tab in the Foundry portal.

### Add an existing agent

1. In the workflow visualizer, select the plus sign.

2. In the pop-up dropdown list, select **Invoke agent**.

3. In the **Create new agent** window, select **existing**.

4. Enter the agent name to search for existing agents in your Foundry project.

5. Select the desired agent to add it into your workflow.

### Create a new agent

1. In the workflow visualizer, select the plus sign.

2. In the pop-up dropdown list, select **Invoke agent**.

3. Enter an agent name and description of what the agent does.

4. Select **Add**.

5. In the **Invoke an agent** window, configure the agent.

6. Select **Save**.

### Configure an output response format for invoking an agent

1. Create an **Invoke agent** node.

1. In the **Invoke agent** configuration window, select **Create a new agent**.

1. Configure the agent to send output as a JSON schema:

   1. Select **Details**.
   1. Select the parameter icon.
   1. For **Text format**, select **JSON Schema**.

   :::image type="content" source="../../media/workflows/select-parameters.png" alt-text="Screenshot that shows the window for configuring a JSON schema format for output." lightbox="../../media/workflows/select-parameters.png":::

1. Copy the desired JSON schema and paste it in the **Add response format** window. The following screenshot shows a math example. Select **Save**.

   :::image type="content" source="../../media/workflows/response-format.png" alt-text="Screenshot that shows the addition of a response format in JSON." lightbox="../../media/workflows/response-format.png":::

  > [!IMPORTANT]
  > Don't include secrets (passwords, keys, tokens) in JSON schemas, prompts, or saved workflow variables.

  ```json
  {
    "name": "math_response",
    "schema": {
      "type": "object",
      "properties": {
        "steps": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "explanation": {
                "type": "string"
              },
              "output": {
                "type": "string"
              }
            },
            "required": [
              "explanation",
              "output"
            ],
            "additionalProperties": false
          }
        },
        "final_answer": {
          "type": "string"
        }
      },
      "additionalProperties": false,
      "required": [
        "steps",
        "final_answer"
      ]
    },
    "strict": true
  }
  ```

1. Select **Action settings**. Then select **Save output json_object/json_schema as**.

1. Select **Create new variable**. Choose a variable name, and then select **Done**.

   :::image type="content" source="../../media/workflows/save-output.png" alt-text="Screenshot that shows options for creating a new variable in a Microsoft Foundry workflow." lightbox="../../media/workflows/save-output.png":::

## Use additional features

- **YAML visualizer view**: When you set the **YAML Visualizer View** toggle to **On**, the workflow is stored in a YAML file. You can modify it in the visualizer and the YAML view. Saving creates a new version, and you have access to the version history.

  The visualizer and the YAML are editable. Any changes to the YAML file are reflected in the visualizer.
- **Versioning**: Each time you save your workflow, a new, unchangeable version is created. To view the version history or delete older versions, open the **Version** dropdown list to the left of the **Save** button.
- **Notes on your workflow visualizer**: You can add notes on the workflow visualizer to add more context or information for your workflow. In the upper-left corner of the workflow visualizer, select **Add note**.

## Create expressions by using Power Fx

Power Fx is a low-code language that uses Excel-like formulas. Use Power Fx to create complex logic that allows your agents to manipulate data. For instance, a Power Fx formula can set the value of a variable, parse a string, or use an expression in a condition. For more information, see the [Power Fx overview](/power-platform/power-fx/overview) and [formula reference](/power-platform/power-fx/formula-reference-copilot-studio).

### Use variables in a formula

To use a variable in a Power Fx formula, you must add a prefix to its name to indicate the variable's scope:

- For system variables, use `System.`
- For local variables, use `Local.`

Here are the system variables:

| Name | Description |
|------|-------------|
| `Activity` | Information about the current activity |
| `Bot` | Information about the agent |
| `Conversation` | Information about the current conversation |
| `Conversation.Id` | Unique ID of the current conversation |
| `Conversation.LocalTimeZone` | Time zone of the user, in the IANA Time Zone Database format |
| `Conversation.LocalTimeZoneOffset` | Time offset from UTC for the current local time zone |
| `Conversation.InTestMode` | Boolean flag that represents if the conversation is happening on a test canvas |
| `ConversationId` | Unique ID of the current conversation |
| `InternalId` | Internal identifier for the system |
| `LastMessage` | Information about the previous message that the user sent |
| `LastMessage.Id` | ID of the previous message that the user sent |
| `LastMessage.Text` | Previous message that the user sent |
| `LastMessageId` | ID of the previous message that the user sent |
| `LastMessageText` | Previous message that the user sent |
| `Recognizer` | Information about intent recognition and the triggering message |
| `User` | Information about the user currently talking to the agent |
| `User.Language` | User language locale per conversation |
| `UserLanguage` | User language locale per conversation |

### Use literal values in a formula

In addition to using variables in a Power Fx formula, you can enter literal values. To use a literal value in a formula, you must enter it in the format that corresponds to its [type](/microsoft-copilot-studio/authoring-variables-about?tabs=webApp).

The following table lists the data types and the format of their corresponding literal values:

| Type             | Format examples                                                                                                                  |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| String           | `"hi"`, `"hello world!"`, `"copilot"`                                                                                            |
| Boolean          | Only `true` or `false`                                                                                                           |
| Number           | `1`, `532`, `5.258`,`-9201`                                                                                                      |
| Record and table | `[1]`, `[45, 8, 2]`, `["cats", "dogs"]`, `{ id: 1 }`, `{ message: "hello" }`, `{ name: "John", info: { age: 25, weight: 175 } }` |
| Date and time         | `Time(5,0,23)`, `Date(2022,5,24)`, `DateTimeValue("May 10, 2022 5:00:00 PM")`                                                    |
| Choice           | Not supported                                                                                                                    |
| Blank            | Only `Blank()`                                                                                                                   |

#### Common Power Fx formulas

The following table lists the Power Fx formulas that you can use with each data type.

| Type             | Power Fx formulas                                                                                                                                                                                                                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| String           | `[Text function][1]`<br>`[Concat and Concatenate functions][2]`<br>`[Len function][3]`<br>`[Lower, Upper, and Proper functions][4]`<br>`[IsMatch, Match, and MatchAll functions][5]`<br>`[EndsWith and StartsWith functions][6]`<br>`[Find function][7]`<br>`[Replace and Substitute function][8]`                                              |
| Boolean          | `[Boolean function][9]`<br>`[And, Or, and Not functions][10]`<br>`[If and Switch functions][11]`                                                                                                                                                                                                                                      |
| Number           | `[Decimal, Float, and Value functions][12]`<br>`[Int, Round, RoundDown, RoundUp, and Trunc functions][13]`                                                                                                                                                                                                                          |
| Record and table | `[Concat and Concatenate functions][14]`<br>`[Count, CountA, CountIf, and CountRows functions][15]`<br>`[ForAll function][16]`<br>`[First, FirstN, Index, Last, and LastN functions][17]`<br>`[Filter, Search, and LookUp functions][18]`<br>`[JSON function][19]`<br>`[ParseJSON function][20]`                                              |
| Date and time         | `[Date, DateTime, and Time functions][21]`<br>`[DateValue, TimeValue, and DateTimeValue functions][22]`<br>`[Day, Month, Year, Hour, Minute, Second, and Weekday functions][23]`<br>`[Now, Today, IsToday, UTCNow, UTCToday, IsUTCToday functions][24]`<br>`[DateAdd, DateDiff, and TimeZoneOffset functions][25]`<br>`[Text function][26]` |
| Blank            | `[Blank, Coalesce, IsBlank, and IsEmpty functions][27]`<br>`[Error, IfError, IsError, IsBlankOrError functions][28]`                                                                                                                                                                                                                |

### Use Power Fx to set a variable

In this example, a Power Fx expression stores and outputs the customer's name in capital letters:

1. Create a workflow and add an **Ask a question** node.

1. On the pane that appears, in the **Ask a question** box, enter **What is your name?** or another message. In the **Save user response as** box, enter a variable name; for example, `Var01`. Then select **Done**.
  
   :::image type="content" source="../../media/workflows/ask-a-question-node.png" alt-text="Screenshot that shows the configuration of a question for sending a message." lightbox="../../media/workflows/ask-a-question-node.png":::

1. Add a **Send message** action. On the pane that appears, in the **Message to send** area, enter `{Upper(Local.Var01)}`. Then select **Done**.

   :::image type="content" source="../../media/workflows/variable-message.png" alt-text="Screenshot that shows the variable instantiation for the action of sending a message." lightbox="../../media/workflows/variable-message.png":::

1. Select **Preview**.

1. On the preview pane, send a message to the agent to invoke the workflow.

   :::image type="content" source="../../media/workflows/type-question.png" alt-text="Screenshot that shows the preview of a question for the action of sending a message." lightbox="../../media/workflows/type-question.png":::

## Use Power Fx to create if/else flows

In this example, you add an if/else flow and build a condition by using system variables.

1. Create a workflow and add an **Ask a question** node.

1. Select the **+** icon and add an **if/else** flow.

1. Type `System.` in the **Condition** box to build a condition statement for each if/else branch.

   :::image type="content" source="../../media/workflows/if-else-condition.png" alt-text="A screenshot showing the system variables in the if-else condition text box." lightbox="../../media/workflows/if-else-condition.png":::

1. Select a **Next Action** for the next step in the workflow.

1. Select **Done**. Select **Save** to save your workflow.

## Troubleshooting

- If you don't see **Workflows** or you can't create or edit workflows, confirm your project access and permissions. See [Azure role-based access control (RBAC) in Foundry](../../../concepts/rbac-foundry.md).
- If your changes don't appear, confirm you selected **Save** in the visualizer.
- If a workflow run doesn't produce the output you expect, verify that each agent node has an agent assigned and that any saved outputs (for example, JSON schema outputs) are valid.


## Related content

- [Foundry Agent Service FAQ](../../../agents/faq.yml)
- [Tool best practices for Foundry agents](tool-best-practice.md)
- [Work with Declarative (Low-code) Agent workflows in Visual Studio Code](../how-to/vs-code-agents-workflow-low-code.md)
- [Work with Hosted (Pro-code) Agent workflows in Visual Studio Code](../how-to/vs-code-agents-workflow-pro-code.md)
