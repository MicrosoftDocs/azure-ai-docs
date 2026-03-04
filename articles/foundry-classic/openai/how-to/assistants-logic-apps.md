---
title: "Run Azure Logic Apps workflows for Assistants (classic)"
description: "Learn how to create AI Assistants that run logic app automation and integration workflows as functions in Microsoft Foundry. (classic)"
services: cognitive-services, azure-logic-apps
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 03/04/2026
recommendations: false
#Customer intent: As an AI integration developer who works with Microsoft Foundry and Azure Logic Apps, I want to run logic app workflows that perform automation and integration tasks as functions from AI Assistants in Foundry.
---

# Run automation and integration workflows as functions from AI Assistants in Microsoft Foundry (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [agent-service](../includes/agent-service.md)]

AI Assistants are effective at understanding user requests and generating responses, but they can't interact with your business systems on their own. For your assistant to complete real-world tasks such as manage data in customer databases, submit orders, send notifications, or trigger complex business processes, you need a way to execute these actions when the assistant needs to do so.

[Azure Logic Apps](/azure/logic-apps/logic-apps-overview) is an integration platform that lets you build automated workflows by using a visual designer. Rather than write custom backend code for each integration, you create logic app workflows by using a low-code interface that provides 1,400+ connectors for Azure, Microsoft, and non-Microsoft services, systems, apps, and data sources.

When you expose a logic app workflow as a function, your assistant can choose when to run the workflow, based on conversation context and user requests. With so many available integration points, your assistant can interact with nearly any business system or service your organization uses. This pattern provides a practical way to automate multistep tasks and integrate assistant conversations with your enterprise infrastructure. You also avoid building and maintaining custom APIs for every business task your assistant needs to perform. Azure Logic Apps handles authentication, retries, error handling, and monitoring for you, letting you focus on defining the workflow logic, rather than infrastructure concerns.

This guide shows how to create and set up a Consumption logic app workflow to accept inputs from your assistant, build the automation logic, and then import the workflow as a callable function from an AI Assistant in Foundry.

## Prerequisites

- An Azure account and subscription. [Get a free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- A [Microsoft Foundry project](/azure/foundry-classic/how-to/create-projects?tabs=foundry).

  This project organizes your work and saves the state while you build your AI apps and solutions.

- A [Consumption logic app resource and workflow](/azure/logic-apps/quickstart-create-example-consumption-workflow) that meets the following requirements:

  | Requirement | Description |
  |-------------|-------------|
  | Hosting option | Uses the Consumption hosting option. |
  | Azure subscription | Uses the same subscription as your Foundry project. |
  | Azure resource group | Uses the same resource group as your Foundry project. |
  | [**Request** trigger](/azure/connectors/connectors-native-reqres#add-request-trigger) | The operation that specifies the conditions to meet before running any subsequent actions in the workflow. The default trigger name is **When an HTTP request is received**. <br><br>Function calling requires a REST-based API. The **Request** trigger provides a REST endpoint that a service or system can call to run the workflow. So, for function calling, you can use only workflows that start with the **Request** trigger. |
  | Trigger description | This description helps the AI assistant choose the appropriate function in Foundry. To enter this description, follow these steps in [Create a logic app resource and workflow](#create-logic-app-workflow). |
  | Trigger schema | A JSON schema that describes the expected inputs for the trigger. To enter or define this schema, follow these steps in [Create a logic app resource and workflow](#create-logic-app-workflow). <br><br>Foundry automatically imports the schema as the function definition. For more information, see [**Request** trigger](/azure/connectors/connectors-native-reqres#add-request-trigger). |
  | [**Response** action](/azure/connectors/connectors-native-reqres#add-a-response-action) | The workflow must always end with this action, which returns the response to Foundry when the workflow completes. |

  Workflows that meet these requirements should eligible for calling as functions from AI Assistants in Microsoft Foundry. Workflows can contain any other actions from the [1,400+ connectors gallery](/connectors/), including runtime-native, built-in operations, that implement the logic for your business scenario.

  If you don't have existing workflows, follow these high-level steps to create them:

  1. [Create a logic app resource and workflow in the Azure portal](#create-logic-app-workflow).
  1. [Import your logic app workflow as a function in the Assistants Playground](#import-your-logic-apps-workflows-as-functions).

<a id="create-logic-app-workflow"></a>

## Create a logic app resource and workflow in the Azure portal

To create a new logic app resource and workflow for function calling, follow these steps:

1. In the [Azure portal](https://portal.azure.com), create a Consumption logic app resource by follow these [general steps](/azure/logic-apps/quickstart-create-example-consumption-workflow#create-a-consumption-logic-app-resource). After you open the workflow designer, return to this section.

1. On the designer, add the [**Request** trigger named **When an HTTP request is received**](/azure/connectors/connectors-native-reqres?tabs=consumption) by following these [general steps](/azure/logic-apps/add-trigger-action-workflow).

1. Select the **Request** trigger to open the information pane and follow these steps:

   1. On the information pane, change the trigger name to reflect the function's task, for example: `Function - Get weather forecast for today`

   1. Provide the following values:

   | Parameter | Description |
   |-----------|-------------|
   | **Description** | Enter a useful description about the task that the workflow performs, for example: <br><br>`This trigger and workflow gets the weather forecast for today from MSN Weather`. |
   | **Request Body JSON Schema** | Enter a JSON schema that specifies the expected inputs. <br><br>If you don't have a schema, select **Use sample payload to generate schema**, provide sample input, and select **Done**. |

   The following image shows an example trigger with a task-relevant name, description, and schema:

   :::image type="content" source="../media/how-to/assistants/logic-apps/request-trigger.png" alt-text="Screenshot shows the Azure portal, Consumption workflow designer, and Request trigger with example name, description, and schema." lightbox="media/how-to/assistants/logic-apps/request-trigger.png":::

1. On the designer toolbar, select **Save** to save the workflow.

   When you save a **Request** trigger for the first time, the designer generates the **HTTP URL** for the trigger's REST endpoint.

   :::image type="content" source="../media/how-to/assistants/logic-apps/rest-endpoint-url.png" alt-text="Screenshot shows Request trigger and HTTP URL for the REST endpoint." lightbox="../media/how-to/assistants/logic-apps/rest-endpoint-url.png":::

1. Based your business use case or logic, add one or more actions in this workflow.

   For example, using the MSN weather connector to get the weather forecast for the current location.

    :::image type="content" source="../media/how-to/assistants/logic-apps/create-logic-app-5.png" alt-text="A screenshot showing the MSN weather connector." lightbox="../media/how-to/assistants/logic-apps/create-logic-app-5.png":::

    In the action to **get forecast for today**, we are using the **location** property that was passed to this workflow as an input.

    :::image type="content" source="../media/how-to/assistants/logic-apps/create-logic-app-6.png" alt-text="A screenshot showing the location property." lightbox="../media/how-to/assistants/logic-apps/create-logic-app-6.png":::

1. Configure the [response](/azure/connectors/connectors-native-reqres#add-a-response-action). The workflow needs to return the response back to Foundry. This is done using Response action.

    :::image type="content" source="../media/how-to/assistants/logic-apps/create-logic-app-7.png" alt-text="A screenshot showing the response action." lightbox="../media/how-to/assistants/logic-apps/create-logic-app-7.png":::

     In the response action, you can pick the output from any of the prior steps. You can optionally also provide a JSON schema if you want to return the output in a specific format.
    
    :::image type="content" source="../media/how-to/assistants/logic-apps/create-logic-app-7.png" alt-text="A screenshot showing the comment box to specify a JSON schema." lightbox="../media/how-to/assistants/logic-apps/create-logic-app-7.png":::

1. The workflow is now ready. In Foundry, you can import this function using the **Add function** feature in the Assistants playground.

## Import your Logic Apps workflows as functions

Here are the steps to import your Logic Apps workflows as function in the Assistants playground in Foundry:

1. In Foundry, select **Playgrounds** from the left pane, and then **Assistants playground**. Select an existing Assistant or create a new one. After you have configured the assistant with a name and instructions, you are ready to add a function. Select **+ Add function**. 

    :::image type="content" source="../media/how-to/assistants/logic-apps/assistants-playground-add-function.png" alt-text="A screenshot showing the Assistant playground with the add function button." lightbox="../media/how-to/assistants/logic-apps/assistants-playground-add-function.png":::

1. The **Add function** option opens a screen with two tabs. Navigate to the tab for Logic Apps to browse your workflows with a request trigger. Select the workflow from list and select **Save**.  

    > [!NOTE]
    > This list only shows the consumption SKU workflows and with a request trigger.

    :::image type="content" source="../media/how-to/assistants/logic-apps/import-logic-apps.png" alt-text="A screenshot showing the menu for adding functions." lightbox="../media/how-to/assistants/logic-apps/import-logic-apps.png":::

You have now successfully imported your workflow and it is ready to be invoked. The function specification is generated based on the logic apps workflow swagger and includes the schema and description based on what you configured in the request trigger action.

:::image type="content" source="../media/how-to/assistants/logic-apps/edit-function.png" alt-text="A screenshot showing the imported workflow." lightbox="../media/how-to/assistants/logic-apps/edit-function.png":::

The workflow now will be invoked by the Azure OpenAI Assistants based on the user prompt. Below is an example where the workflow is invoked automatically based on user prompt to get the weather.

:::image type="content" source="../media/how-to/assistants/logic-apps/playground-weather-example.png" alt-text="A screenshot showing a weather prompt example." lightbox="../media/how-to/assistants/logic-apps/playground-weather-example.png":::

You can confirm the invocation by looking at the logs as well as your [workflow run history](/azure/logic-apps/monitor-logic-apps?tabs=consumption.md#review-workflow-run-history).

:::image type="content" source="../media/how-to/assistants/logic-apps/example-log.png" alt-text="A screenshot showing a logging example." lightbox="../media/how-to/assistants/logic-apps/example-log.png":::

## FAQ 

**What are Logic App connectors?**

Azure Logic Apps has connectors to hundreds of line-of-business (LOB) applications and databases including but not limited to: SAP, Salesforce, Oracle, SQL, and more. You can also connect to SaaS applications or your in-house applications hosted in virtual networks. These out of box connectors provide operations to send and receive data in multiple formats. Leveraging these capabilities with Azure OpenAI assistants, you should be able to quickly bring your data for Intelligent Insights powered by Azure OpenAI.

**What happens when a Logic Apps is imported in Foundry  and invoked**

The Logic Apps swagger file is used to populate function definitions. Azure Logic App publishes an OpenAPI 2.0 definition (swagger) for workflows with a request trigger based on [annotations on the workflow](/rest/api/logic/workflows/list-swagger). Users are able to modify the content of this swagger by updating their workflow. Foundry uses this to generate the function definitions that the Assistant requires.  

**How does authentication from Foundry to Logic Apps work?**

Logic Apps supports two primary types of authentications to invoke a request trigger.

* Shared Access Signature (SAS) based authentication.
    
    Users can obtain a callback URL containing a SAS using the [list callback URL](/rest/api/logic/workflows/list-callback-url) API. Logic Apps also supports using multiple keys and rotating them as needed. Logic Apps also supports creating SAS URLs with a specified validity period. For more information, see the [Logic Apps documentation](/azure/logic-apps/logic-apps-securing-a-logic-app#generate-shared-access-signatures-sas).

* Microsoft Entra ID-based OAuth base authentication policy.

    Logic Apps also supports authentication trigger invocations with Microsoft Entra ID OAuth, where you can specify authentication policies to be used in validating OAuth tokens. For more information, see the [Logic Apps documentation](/azure/logic-apps/logic-apps-securing-a-logic-app#generate-shared-access-signatures-sas).

When Azure OpenAI Assistants require invoking a Logic App as part of function calling, Foundry will retrieve the callback URL with the SAS to invoke the workflow. 

## See also

* [Learn more about Assistants](../concepts/assistants.md)