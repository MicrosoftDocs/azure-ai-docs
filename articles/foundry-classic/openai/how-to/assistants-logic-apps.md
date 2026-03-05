---
title: "Run Azure Logic Apps Workflows from Assistants (classic)"
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

[Azure Logic Apps](/azure/logic-apps/logic-apps-overview) is an integration platform that lets you build automated workflows by using a visual designer. Rather than write custom backend code for each integration, you create logic app workflows by using a low-code interface that provides 1,400+ *connectors* for Azure, Microsoft, and non-Microsoft services, systems, apps, and data sources.

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
  | [**Request** trigger](/azure/connectors/connectors-native-reqres?tabs=consumption#add-request-trigger) | The operation that specifies the conditions to meet before running any subsequent actions in the workflow. The default trigger name is **When an HTTP request is received**. <br><br>Function calling requires a REST-based API. The **Request** trigger provides a REST endpoint that a service or system can call to run the workflow. So, for function calling, you can use only workflows that start with the **Request** trigger. |
  | Trigger description | This description helps the AI assistant choose the appropriate function in Foundry. To enter this description, follow these steps in [Create a logic app resource and workflow](#create-logic-app-workflow). |
  | Trigger schema | A JSON schema that describes the expected inputs for the trigger. To enter or define this schema, follow these steps in [Create a logic app resource and workflow](#create-logic-app-workflow). <br><br>Foundry automatically imports the schema as the function definition. For more information, see [**Request** trigger](/azure/connectors/connectors-native-reqres?tabs=consumption#add-request-trigger). |
  | [**Response** action](/azure/connectors/connectors-native-reqres?tabs=consumption#add-a-response-action) | The workflow must always end with this action, which returns the response to Foundry when the workflow completes. |

  You can use logic app workflows that meet these requirements as functions that AI Assistants can call in Foundry. To implement your business logic or use case, workflows can contain any other actions from the [connectors gallery](/azure/connectors/introduction). For example, you can connect to many Azure, Microsoft, and non-Microsoft services or systems such as SAP, Salesforce, Oracle, and more. You can also connect to SaaS applications or in-house applications hosted in virtual networks. When you use these capabilities with AI Assistants, you can quickly bring in your data for Intelligent Insights powered by Azure OpenAI.

  If you don't have existing workflows, follow these high-level steps to create them:

  1. [Create a logic app resource and workflow in the Azure portal](#create-logic-app-workflow).
  1. [Import your logic app workflow as a function in the Assistants playground](#import-your-logic-apps-workflows-as-functions).

<a id="create-logic-app-workflow"></a>

## 1: Create a logic app resource

To create a new logic app resource and workflow for function calling, follow these steps:

1. In the [Azure portal](https://portal.azure.com), create a Consumption logic app resource by follow these [general steps](/azure/logic-apps/quickstart-create-example-consumption-workflow#create-a-consumption-logic-app-resource). After you open the workflow designer, return to this section.

1. On the designer, add the [**Request** trigger named **When an HTTP request is received**](/azure/connectors/connectors-native-reqres?tabs=consumption#add-request-trigger) by following these [general steps](/azure/logic-apps/add-trigger-action-workflow#add-trigger).

1. Select the **Request** trigger to open the information pane and follow these steps:

   1. On the information pane, change the trigger name to reflect the function's task, for example: `Function - Get weather forecast for today`

   1. Provide the following trigger information:

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

   For example, to get today's weather forecast for the current location, add an action from the **MSN Weather** connector. This example uses the **Get forecast for today** action.

   :::image type="content" source="../media/how-to/assistants/logic-apps/msn-weather-connector-actions.png" alt-text="Screenshot shows actions available in the MSN Weather connector." lightbox="../media/how-to/assistants/logic-apps/msn-weather-connector-actions.png":::

1. In the action information pane for the **Get forecast for today** action, follow these steps:

   1. Select inside the **Location** parameter. When the input options appear (lightning icon and function icon), select the dynamic content list option (lightning icon).

      The dynamic content list lets you select outputs from preceding operations in the workflow. In this case, you want the location value that passed through the trigger to the workflow.

   1. From the dynamic content list, under trigger section named **Function - Get weather forecast for today**, select **Location**, for example:

      :::image type="content" source="../media/how-to/assistants/logic-apps/location-dynamic-content-list.png" alt-text="Screenshot shows the action named Get forecast for today and the dynamic content list with the Location trigger output selected." lightbox="../media/how-to/assistants/logic-apps/location-dynamic-content-list.png":::

      The action now looks like the following example:

      :::image type="content" source="../media/how-to/assistants/logic-apps/location-output-added.png" alt-text="Screenshot shows the action named Get forecast for today and the dynamic content list with the Location trigger output selected." lightbox="../media/how-to/assistants/logic-apps/location-output-added.png":::

1. On the designer, add the [**Response** action](/azure/connectors/connectors-native-reqres?tabs=consumption#add-a-response-action) by following these [general steps](/azure/logic-apps/add-trigger-action-workflow#add-action).

   The workflow returns a response to Foundry by using the **Response** action.

   From the dynamic content list, you can optionally select any prior operation outputs to return to Foundry. Or, you can provide a JSON schema to return the output in a specific format.

   :::image type="content" source="../media/how-to/assistants/logic-apps/response-action.png" alt-text="Screenshot shows Response action with optional operation outputs or JSON schema to return to Foundry." lightbox="../media/how-to/assistants/logic-apps/response-action.png":::

1. On the designer toolbar, select **Save** to save the workflow.

   Your workflow is now ready to import into Foundry.

<a id="import-logic-app-workflow"></a>

## 2: Import the logic app resource as a function

To bring a logic app resource and workflow into Foundry for function calling through the Assistants playground, follow these steps:

1. In the [Foundry portal (classic)](https://ai.azure.com/), open your Foundry project.

1. On the project sidebar, select **Playgrounds**. Scroll down and select **Try the Assistants playground**. 

1. On the **Assistants playground** page, choose **Select assistant** to open an existing one or **New assistant** to create a new one.

1. In the **Setup** section, expand **Tools**. Next to **Functions**, select **+ Add function**, for example:

   :::image type="content" source="../media/how-to/assistants/logic-apps/assistants-playground-add-function.png" alt-text="Screenshot shows Foundry portal (classic) with project, assistants playground, and Add function selected." lightbox="../media/how-to/assistants/logic-apps/assistants-playground-add-function.png":::

1. On the **Add a custom function trigger** screen, select the **Logic Apps** tab, for example:

   :::image type="content" source="../media/how-to/assistants/logic-apps/select-logic-apps.png" alt-text="Screenshot shows Logic Apps tab selected." lightbox="../media/how-to/assistants/logic-apps/select-logic-apps.png":::

1. On the **Add logic app function** screen, from the logic apps list, select a logic app:

   > [!NOTE]
   >
   > The list shows only logic apps with workflows that meet the [requirements for function calling](#prerequisites).

   :::image type="content" source="../media/how-to/assistants/logic-apps/add-logic-app-function.png" alt-text="Screenshot shows logic apps list with logic app selected for function calling." lightbox="../media/how-to/assistants/logic-apps/add-logic-app-function.png":::

1. When you're finished, select **Save**.

   The portal returns you to the **Assistants playground** page. In the **Functions** section, the successfully imported logic app workflow now appears as a function that your assistant can call, based on the user prompt.

## 3: Test the logic app function

To check that the imported logic app function works as expected, follow these steps:

1. On the **Assistants playground** page, in the chat window, enter a query for today's weather forecast in Seattle, for example:

   :::image type="content" source="../media/how-to/assistants/logic-apps/playground-weather-example.png" alt-text="Screenshot shows the Assistants playground with a weather prompt example." lightbox="../media/how-to/assistants/logic-apps/playground-weather-example.png":::

1. To confirm the logic app function call, you can review the logs or the [workflow run history](/azure/logic-apps/monitor-logic-apps?tabs=consumption#review-workflow-run-history).

   The following example shows a sample log with the function call:

   :::image type="content" source="../media/how-to/assistants/logic-apps/example-log.png" alt-text="Screenshot shows log example." lightbox="../media/how-to/assistants/logic-apps/example-log.png":::

## FAQ

### What happens when you import and invoke a logic app as a function?

Azure Logic Apps publishes an OpenAPI 2.0 definition (swagger) for workflows with a **Request** trigger, based on [workflow annotations](/rest/api/logic/workflows/list-swagger). Foundry uses this swagger file to generate a function specification and populate the function definition that the AI Assistant requires. The trigger schema and description are based on what you set up in the **Request** trigger. You can edit the swagger by updating your workflow.

To view the function specification in Foundry, follow these steps:

1. On the **Assistants playground** page, in the **Setup** section, go to the **Functions** section.

1. Next to the function, from the ellipses menu (...), select **Manage**.

   :::image type="content" source="../media/how-to/assistants/logic-apps/edit-function-trigger.png" alt-text="Screenshot shows the newly imported logic app function and the Manage button selected." lightbox="../media/how-to/assistants/logic-apps/edit-function-trigger.png":::

   The following screenshot shows a sample function specification for the example function:

   :::image type="content" source="../media/how-to/assistants/logic-apps/view-function-specification.png" alt-text="Screenshot shows the function specification." lightbox="../media/how-to/assistants/logic-apps/view-function-specification.png":::

### How does authentication from Foundry to Azure Logic Apps work?

Azure Logic Apps supports the following types of authentication for inbound calls to the **Request** trigger in a logic app workflow from Foundry:

- Shared Access Signature (SAS) based authentication

  When an AI Assistant calls a function that runs a logic app workflow, Foundry sends a request to the *callback URL* in the workflow's **Request** trigger. You can get this callback URL, which includes an SAS, by using [Workflows - List callback Url](/rest/api/logic/workflows/list-callback-url) from the REST API for Azure Logic Apps.

  For SAS authentication, Azure Logic Apps also supports the following:

  - Create SAS URLs with a specified validity period.
  - Using multiple keys and rotating them as needed.

  For more information, see [Generate a Shared Access Signature (SAS) key or token](/azure/logic-apps/logic-apps-securing-a-logic-app#generate-shared-access-signatures-sas).

- Microsoft Entra ID-based OAuth authentication policy

  Azure Logic Apps supports authentication for calls to request triggers by using OAuth with Microsoft Entra ID. You can specify authentication policies to use when validating OAuth tokens. For more information, see [Enable OAuth 2.0 with Microsoft Entra ID in Azure Logic Apps](/azure/logic-apps/logic-apps-securing-a-logic-app?tabs=azure-portal#enable-oauth-20-with-microsoft-entra-id).

For more information about authentication and security for inbound calls to request-based triggers in Azure Logic Apps, see [Access for inbound calls to request-based triggers](/azure/logic-apps/logic-apps-securing-a-logic-app?tabs=azure-portal#access-for-inbound-calls-to-request-based-triggers).

## Related content

- [Learn more about Assistants](../concepts/assistants.md)
