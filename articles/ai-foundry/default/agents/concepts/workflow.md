---
title: Build a Workflow in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: This article explains how to build a Workflow in Microsoft Foundry using agents. 
ms.service: azure-ai-foundry
ms.custom:
  - build-2025
  - code01
ms.topic: tutorial
ms.date: 11/05/2025
ms.reviewer: fniedtner
ms.author: ssalgado
manager: nitinme
author: ssalgadodev
#customer intent: As a developer, I want to learn how to build a workflow.
---

# Build a workflow in Microsoft Foundry

Workflows is a UI-based tool in Foundry to create declarative, predefined sequences of actions including agents, as in Microsoft Agent Framework Workflows.

Workflows enable you to build intelligent automation systems that seamlessly blend AI agents with business processes, in a visual manner. Traditional single-agent systems are limited in their ability to handle complex, multi-faceted tasks. By orchestrating multiple agents, each with specialized skills or roles, you can create systems that are more robust, adaptive, and capable of solving real-world problems collaboratively.

## Prerequisites

* [!INCLUDE [azure-subscription](../../../includes/azure-subscription.md)]
* A **project in Microsoft Foundry** 

## Create a workflow

In Foundry, you can choose to create a blank workflow or choose from one of the premade configured options. For this tutorial, we'll be creating a Sequential workflow. If you want to learn more about different types of workflows, see the [workflow concepts](#workflow-concepts) section of this article. 

### Build a workflow quickstart

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Select **Build** in the upper-right navigation.
1. Select **Create new workflow** and **Sequential**.
1. Assign an agent to the agent nodes by selecting each agent node in the workflow and selecting the [desired agent](#add-existing-agent) or [create a new one](#create-new-agent).
1. When you make changes to the workflow, select **Save** in the visualizer to save any changes.
1. Select **Run Workflow**.
1. Interact with the workflow in the chat window.
1. (Optional) you can add new nodes to your workflow with steps found in the [adding nodes to your workflow](#add-nodes-to-your-workflow) section.

> [!IMPORTANT]
> Workflows aren't saved automatically. Select **Save** every time you want to save changes to your workflow.

## Workflow concepts

To start creating a new workflow, you can begin with a blank workflow or select one of the templates of pre-defined orchestration patterns [Microsoft Agent Framework Workflows Orchestrations | Microsoft Learn](/agent-framework/user-guide/workflows/orchestrations/overview).

| Pattern    | Description                                                        | Typical Use Case                                         |
|------------|--------------------------------------------------------------------|----------------------------------------------------------|
| Human in the loop  | Asks user a question and awaits user input to proceed. | Create approval requests during workflow execution and wait for human approval, obtain information form the user. |
| Sequential | Passes the result from one agent to the next in a defined order.   | Step-by-step workflows, pipelines, multi-stage processing. |
| Group chat    | Dynamically passes control between agents based on context or rules.| Dynamic workflows, escalation, fallback, or expert handoff scenarios. |


## Add nodes to your workflow

When selecting a pre-built workflow, you should see a workflow of nodes displayed in the builder. Each node corresponds to a specific action or component and performs a step in sequence. You can modify the order of the nodes by selecting the three dots on the node and selecting **move**. You can add new nodes by selecting the **+** icon in the workspace.

Nodes define the building blocks of your workflow. Common node types include:

- **Agent**: Invoke an agent.
- **Logic**: If/Else, Go To, For Each.
- **Data Transformation**: Set Variable, Parse Value.
- **Basic chat**: Send a message or ask a question to an agent.

## Add agents to your workflow

You can add any Foundry agent from your project to the workflow. Agent nodes also allow you to create new agents, configure their model, prompt, and tools, giving them customized capabilities.
For more advanced options and comprehensive agent creation, visit the Foundry Agent tab in the Foundry portal.

### Add existing agent

1. Select the '+' sign in the workflow visualizer.
2. In the pop-up dropdown, select **Invoke agent**.
3. In the "Create new agent" window, select **existing**.
4. Type the agent name to search for existing agents in your Foundry project.
5. Select the desired agent to add it into your workflow.

### Create new agent

1. Select the '+' sign in the workflow visualizer.
2. In the pop-up dropdown, select **Invoke agent**.
3. Enter an agent name and description of what the agent does.
4. Select **Add**.
5. Configure the agent in the invoke an agent window.
6. Select **Save**.

### Configure output response format for Invoke Agent 

1. Create an **Invoke agent** node.
2. Select create a new an agent in the Invoke agent configuration window.
3. Configure the agent to output as JSON Schema in the configuration window. Select **Details**. Select the parameter icon. Then select JSON Schema as the **Text Format**.

  :::image type="content" source="../../media/workflows/select-parameters.png" alt-text="A screenshot showing the addition of a send a message action." lightbox="../../media/workflows/select-parameters.png":::

5. Copy and paste the desired JSON Schema in the **Add response format** window. You can use the math example example for this tutorial. Select **Save**.

   :::image type="content" source="../../media/workflows/response-format.png" alt-text="A screenshot showing the addition of a send a message action." lightbox="../../media/workflows/response-format.png":::

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

7. Select **Action settings**. Select **Save output json_obsject/json_schema as**. 
8. Select **Create new variable**. Choose a variable name. Select **Done**.

   :::image type="content" source="../../media/workflows/save-output.png" alt-text="A screenshot showing the addition of a send a message action." lightbox="../../media/workflows/save-output.png":::

## Additional features

- **YAML Visualizer View toggle**: The workflow will be stored in a YAML file, it can be modified in the visualizer and the YAML view. Saving will create a new version; you have access to the version history. The visualizer and the YAML are editable. You can edit the YAML file and any changes to the file will be reflected in the visualizer.
- **Versioning**: Each time you save your workflow, a new, unchangeable version is created. To view the version history or delete older versions, open the Version dropdown located to the left of the Save button.
- **Add Notes to your workflow visualizer**: You can add notes on the workflow visualizer to add additional context or information regarding your workflow. In the upper left corner of the workflow visualizer, select **Add note**.


## Create expressions using Power Fx

Power Fx is a low-code language that uses Excel-like formulas. Use Power Fx to create complex logic that allows your agents to manipulate data. For instance, a Power Fx formula can set the value of a variable, parse a string, or use an expression in a condition. For more information, see the [Power Fx overview](/power-platform/power-fx/overview) and [formula reference](/power-platform/power-fx/formula-reference-copilot-studio).

## Use variables in a formula

To use a variable in a Power Fx formula, you must add a prefix to its name to indicate the variable's scope:

- For [system variables](/microsoft-copilot-studio/authoring-variables-about?tabs=webApp), use `System.`
- For local variables, use `Local.`

### Use literal values in a formula

In addition to using variables in a Power Fx formula, you can enter literal values. To use a literal value in a formula, you must enter it in the format that corresponds to its [type](/microsoft-copilot-studio/authoring-variables-about?tabs=webApp). The following table lists the data types and the format of their corresponding literal values.

| Type             | Format examples                                                                                                                  |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| String           | `"hi"`, `"hello world!"`, `"copilot"`                                                                                            |
| Boolean          | Only `true` or `false`                                                                                                           |
| Number           | `1`, `532`, `5.258`,`-9201`                                                                                                      |
| Record and Table | `[1]`, `[45, 8, 2]`, `["cats", "dogs"]`, `{ id: 1 }`, `{ message: "hello" }`, `{ name: "John", info: { age: 25, weight: 175 } }` |
| DateTime         | `Time(5,0,23)`, `Date(2022,5,24)`, `DateTimeValue("May 10, 2022 5:00:00 PM")`                                                    |
| Choice           | Not supported                                                                                                                    |
| Blank            | Only `Blank()`                                                                                                                   |

### Common Power Fx formulas

The following table lists data types and Power Fx formulas you can use with each data type.

| Type             | Power Fx formulas                                                                                                                                                                                                                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| String           | [Text function][1]<br>[Concat and Concatenate functions][2]<br>[Len function][3]<br>[Lower, Upper, and Proper functions][4]<br>[IsMatch, Match, and MatchAll functions][5]<br>[EndsWith and StartsWith functions][6]<br>[Find function][7]<br>[Replace and Substitute function][8]                                              |
| Boolean          | [Boolean function][9]<br>[And, Or, and Not functions][10]<br>[If and Switch functions][11]                                                                                                                                                                                                                                      |
| Number           | [Decimal, Float, and Value functions][12]<br>[Int, Round, RoundDown, RoundUp, and Trunc functions][13]                                                                                                                                                                                                                          |
| Record and Table | [Concat and Concatenate functions][14]<br>[Count, CountA, CountIf, and CountRows functions][15]<br>[ForAll function][16]<br>[First, FirstN, Index, Last, and LastN functions][17]<br>[Filter, Search, and LookUp functions][18]<br>[JSON function][19]<br>[ParseJSON function][20]                                              |
| DateTime         | [Date, DateTime, and Time functions][21]<br>[DateValue, TimeValue, and DateTimeValue functions][22]<br>[Day, Month, Year, Hour, Minute, Second, and Weekday functions][23]<br>[Now, Today, IsToday, UTCNow, UTCToday, IsUTCToday functions][24]<br>[DateAdd, DateDiff, and TimeZoneOffset functions][25]<br>[Text function][26] |
| Blank            | [Blank, Coalesce, IsBlank, and IsEmpty functions][27]<br>[Error, IfError, IsError, IsBlankOrError functions][28]                                                                                                                                                                                                                |
## Use Power Fx to set a variable

In this example, a Power Fx expression stores and outputs the customer's name in capital letters.

1. Create a workflow and add an **Ask a question** node.

1. For **Enter a message** in the side settings panel, enter "What is your name?" or another message. Enter a variable name in the **Save user response as** field, for example `Var01`. Select **Done**.

:::image type="content" source="../../media/workflows/ask-a-question-node.png" alt-text="A screenshot showing the addition of a send a message action." lightbox="../../media/workflows/ask-a-question-node.png":::

1. Add a **Send message** action. Then in the side settings panel enter `{Upper(Local.Var01)}`. Select **Done**.

:::image type="content" source="../../media/workflows/variable-message.png" alt-text="A screenshot showing the variable instatiation for the send a message action." lightbox="../../media/workflows/variable-message.png":::

1. Select **Preview**

1. Send a message to the agent in the side panel to invoke the workflow.

:::image type="content" source="../../media/workflows/type-question.png" alt-text="A screenshot showing the type a question instatiation for the send a message action." lightbox="../../media/workflows/type-question.png":::


## Next Steps
* [Microsoft Foundry Agents FAQ](../../../agents/faq.yml)



 
