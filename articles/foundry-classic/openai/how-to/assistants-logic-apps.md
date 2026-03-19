---
title: Run Workflows from Assistants in Foundry (classic)
description: Run automation workflows as functions from assistants in Microsoft Foundry Agent Service (classic). Connect to 1,400+ services and systems without custom code.
services: cognitive-services, azure-logic-apps
manager: nitinme
author: alvinashcraft
ms.author: aashcraft
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 03/04/2026
ai-usage: ai-assisted
ms.custom: azure-ai-agents
#Customer intent: As an AI integration developer who works with Azure Logic Apps and Microsoft Foundry, I want to run workflows to perform tasks as functions from assistants with Foundry Agent Service (classic).
---

# Run workflows as functions from assistants in Foundry Agent Service (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [agent-service](../includes/agent-service.md)]

In Microsoft Foundry, you can extend AI assistants to work with your business or enterprise systems and to complete real-world tasks. On their own, assistants can't directly manage data in customer databases, submit orders, send notifications, or trigger complex business processes when they need to do so.

[Azure Logic Apps](/azure/logic-apps/logic-apps-overview) is an integration platform lets you build automated workflows by using a visual designer. Rather than writing custom backend code for each integration, create logic app workflows from 1,400+ *connectors* that can access Azure, Microsoft, and non-Microsoft services, systems, apps, and data sources, such as SAP, Salesforce, and Oracle.

When you expose a logic app workflow as a callable function, your assistant chooses when to run the workflow based on chat conversation context and user prompts. With so many integration options, your assistant can work with nearly any business system or service your organization uses. This pattern provides a practical way to automate multistep tasks and integrate assistant conversations with your enterprise infrastructure. You don't need to build and maintain custom APIs for every business task that your assistant needs to perform. Azure Logic Apps handles authentication, retries, error handling, and monitoring, so you can focus on workflow logic rather than infrastructure.

This article shows how to create and set up a workflow in Azure Logic Apps as a tool for your assistant in Foundry Agent Service.

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

  You can use logic app workflows that meet these requirements as functions that AI assistants can call in Foundry. To implement your business logic or use case, workflows can contain any other actions from the [connectors gallery](/azure/connectors/introduction). For example, you can connect to many Azure, Microsoft, and non-Microsoft services or systems, such as SAP, Salesforce, Oracle, and so on. You can also connect to SaaS applications or in-house applications hosted in virtual networks. When you use these capabilities with AI assistants, you can quickly bring in your data for Intelligent Insights powered by Azure OpenAI.

  If you don't have existing workflows, follow these high-level steps to create them:

  1. [Create a logic app resource and workflow in the Azure portal](#create-logic-app-workflow).
  1. [Import your logic app workflow as a function in the Assistants playground](#import-logic-app-workflow).

- Set up the following environment variables with information from your Foundry project:

  ```bash
  export PROJECT_ENDPOINT="<your_project_endpoint>"
  export MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
  export SUBSCRIPTION_ID="<your_Azure_subscription_ID>"
  export resource_group_name="<your_resource_group_name>"
  ```

:::zone pivot="portal"

<a id="create-logic-app-workflow"></a>

## 1: Create a logic app resource

To create a logic app resource and workflow for function calling, follow these steps:

1. In the [Azure portal](https://portal.azure.com), create a Consumption logic app resource by following these [general steps](/azure/logic-apps/quickstart-create-example-consumption-workflow#create-a-consumption-logic-app-resource). After you open the workflow designer, return to this section.

1. On the designer, add the [**Request** trigger named **When an HTTP request is received**](/azure/connectors/connectors-native-reqres?tabs=consumption#add-request-trigger) by following these [general steps](/azure/logic-apps/add-trigger-action-workflow#add-trigger).

1. Select the **Request** trigger to open the information pane and follow these steps:

   1. On the information pane, change the trigger name to reflect the function's task, for example: `Function - Get weather forecast for today`

   1. Provide the following trigger information:

   | Parameter | Description |
   |-----------|-------------|
   | **Description** | Enter a useful description about the task that the workflow performs, for example: <br><br>`This trigger and workflow gets the weather forecast for today from MSN Weather`. |
   | **Request Body JSON Schema** | Enter a JSON schema that specifies the expected inputs. <br><br>If you don't have a schema, select **Use sample payload to generate schema**, provide sample input, and select **Done**. |

   The following image shows an example trigger with a task-relevant name, description, and schema:

   :::image type="content" source="../media/how-to/assistants/logic-apps/request-trigger.png" alt-text="Screenshot that shows the Azure portal, Consumption workflow designer, and Request trigger with example name, description, and schema." lightbox="../media/how-to/assistants/logic-apps/request-trigger.png":::

1. On the designer toolbar, select **Save** to save the workflow.

   When you save a **Request** trigger for the first time, the designer generates the **HTTP URL** for the trigger's REST endpoint.

   :::image type="content" source="../media/how-to/assistants/logic-apps/rest-endpoint-url.png" alt-text="Screenshot that shows the Request trigger and HTTP URL for the REST endpoint." lightbox="../media/how-to/assistants/logic-apps/rest-endpoint-url.png":::

1. Based on your business use case or logic, add one or more actions in this workflow.

   For example, to get today's weather forecast for the current location, add an action from the **MSN Weather** connector. This example uses the **Get forecast for today** action.

   :::image type="content" source="../media/how-to/assistants/logic-apps/msn-weather-connector-actions.png" alt-text="Screenshot that shows actions available in the MSN Weather connector." lightbox="../media/how-to/assistants/logic-apps/msn-weather-connector-actions.png":::

1. In the action information pane for the **Get forecast for today** action, follow these steps:

   1. Select inside the **Location** parameter. When the input options appear (lightning icon and function icon), select the dynamic content list option (lightning icon).

      The dynamic content list lets you select outputs from preceding operations in the workflow. In this case, you want the location value that passed through the trigger to the workflow.

   1. From the dynamic content list, under trigger section named **Function - Get weather forecast for today**, select **Location**, for example:

      :::image type="content" source="../media/how-to/assistants/logic-apps/location-dynamic-content-list.png" alt-text="Screenshot that shows the action named Get forecast for today and the dynamic content list with the Location trigger output selected." lightbox="../media/how-to/assistants/logic-apps/location-dynamic-content-list.png":::

      The action now looks like the following example:

      :::image type="content" source="../media/how-to/assistants/logic-apps/location-output-added.png" alt-text="Screenshot that shows the action named Get forecast for today and with the resolved Location trigger output." lightbox="../media/how-to/assistants/logic-apps/location-output-added.png":::

1. On the designer, add the [**Response** action](/azure/connectors/connectors-native-reqres?tabs=consumption#add-a-response-action) by following these [general steps](/azure/logic-apps/add-trigger-action-workflow#add-action).

   The workflow returns a response to Foundry by using the **Response** action.

1. From the dynamic content list, optionally select any prior operation outputs to return to Foundry. Or, you can provide a JSON schema to return the output in a specific format.

   :::image type="content" source="../media/how-to/assistants/logic-apps/response-action.png" alt-text="Screenshot that shows Response action with optional operation outputs or JSON schema to return to Foundry." lightbox="../media/how-to/assistants/logic-apps/response-action.png":::

1. On the designer toolbar, select **Save** to save the workflow.

   Your workflow is now ready to import into Foundry.

<a id="import-logic-app-workflow"></a>

## 2: Import the logic app resource as a function

To bring a logic app resource and workflow into Foundry for function calling through the Assistants playground, follow these steps:

1. In the [Foundry portal (classic)](https://ai.azure.com/), open your Foundry project.

1. On the project sidebar, select **Playgrounds**. Scroll down and select **Try the Assistants playground**. 

1. On the **Assistants playground** page, open an existing assistant or create a new one.

1. In the **Setup** section, expand **Tools**. Next to **Functions**, select **+ Add function**, for example:

   :::image type="content" source="../media/how-to/assistants/logic-apps/assistants-playground-add-function.png" alt-text="Screenshot that shows Foundry portal (classic) with project, assistants playground, and Add function selected." lightbox="../media/how-to/assistants/logic-apps/assistants-playground-add-function.png":::

1. On the **Add a custom function trigger** screen, select the **Logic Apps** tab, for example:

   :::image type="content" source="../media/how-to/assistants/logic-apps/select-logic-apps.png" alt-text="Screenshot that shows Logic Apps tab selected." lightbox="../media/how-to/assistants/logic-apps/select-logic-apps.png":::

1. On the **Add logic app function** screen, from the logic apps list, select a logic app:

   > [!NOTE]
   >
   > The list shows only logic apps with workflows that meet the [requirements for function calling](#prerequisites).

   :::image type="content" source="../media/how-to/assistants/logic-apps/add-logic-app-function.png" alt-text="Screenshot that shows logic apps list with logic app selected for function calling." lightbox="../media/how-to/assistants/logic-apps/add-logic-app-function.png":::

1. When you finish, select **Save**.

   The portal returns you to the **Assistants playground** page. In the **Functions** section, the successfully imported logic app workflow now appears as a function that your assistant can call, based on the user prompt.

## 3: Test the logic app function

To confirm that the imported logic app function works as expected, follow these steps:

1. On the **Assistants playground** page, in the chat window, enter a query for today's weather forecast in Seattle, for example:

   :::image type="content" source="../media/how-to/assistants/logic-apps/playground-weather-example.png" alt-text="Screenshot that shows the Assistants playground with a weather prompt example." lightbox="../media/how-to/assistants/logic-apps/playground-weather-example.png":::

1. To confirm the logic app function call, review the logs or the [workflow run history](/azure/logic-apps/monitor-logic-apps?tabs=consumption#review-workflow-run-history).

   The following example shows a sample log with the function call:

   :::image type="content" source="../media/how-to/assistants/logic-apps/example-log.png" alt-text="Screenshot that shows log example." lightbox="../media/how-to/assistants/logic-apps/example-log.png":::

:::zone-end

:::zone pivot="python"

## Create a project client

Create a client object to connect to your Foundry project.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Create the project client
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

## Register the logic app

Provide the trigger name and details to register the logic app resource. To find the `AzureLogicAppTool` utility code, visit the [full sample on GitHub](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples-classic/python/getting-started-agents/logic_apps/user_logic_apps.py).

```python
from user_logic_apps import AzureLogicAppTool

# Logic app details
LOGIC_APP_NAME = "your_logic_app_name"
TRIGGER_NAME = "your_trigger_name"

# Register the logic app with the agent tool utility
subscription_id = os.environ["SUBSCRIPTION_ID"]
resource_group = os.environ["resource_group_name"]

logic_app_tool = AzureLogicAppTool(subscription_id, resource_group)
logic_app_tool.register_logic_app(LOGIC_APP_NAME, TRIGGER_NAME)
print(f"Registered logic app '{LOGIC_APP_NAME}' with trigger '{TRIGGER_NAME}'.")
```

## Create an agent with the logic app tool

Create an agent and attach the logic app as a function tool.

```python
from azure.ai.agents.models import ToolSet, FunctionTool
from user_functions import fetch_current_datetime
from user_logic_apps import create_send_email_function

# Create the logic app function for the agent toolset
send_email_func = create_send_email_function(
    logic_app_tool, LOGIC_APP_NAME
)

functions_to_use = {fetch_current_datetime, send_email_func}

# Build and assign the toolset
functions = FunctionTool(functions=functions_to_use)
toolset = ToolSet()
toolset.add(functions)

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="SendEmailAgent",
    instructions="You are a specialized agent for sending emails.",
    toolset=toolset,
)
print(f"Created agent, ID: {agent.id}")
```

## Create a thread

Create a thread and add a user message to start the conversation.

```python
RECIPIENT_EMAIL = "your_recipient@example.com"

# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create a message in the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"Send an email to {RECIPIENT_EMAIL} with the current date and time.",
)
print(f"Created message, ID: {message.id}")
```

## Run the agent and check the output

Create a run and confirm that the agent uses the logic app tool to complete the task.

```python
# Run the agent on the thread
run = project_client.agents.runs.create_and_process(
    thread_id=thread.id, agent_id=agent.id
)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and display all messages
messages = project_client.agents.messages.list(thread_id=thread.id)
for msg in messages:
    if msg.text_messages:
        last_text = msg.text_messages[-1]
        print(f"{msg.role}: {last_text.text.value}")
```

## Clean up resources

Delete the agent when you're done to clean up resources.

```python
# Delete the agent
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
```

:::zone-end

## FAQ

### What happens when you add a logic app workflow as a function?

Azure Logic Apps publishes an OpenAPI 2.0 definition (swagger) for workflows with a **Request** trigger, based on [workflow annotations](/rest/api/logic/workflows/list-swagger). Foundry uses this swagger file to generate a function specification and populate the function definition that the AI assistant requires. The trigger schema and description come from the configuration you set up in the **Request** trigger. You can edit the swagger by updating your workflow.

To view the function specification in Foundry, follow these steps:

1. On the **Assistants playground** page, in the **Setup** section, go to the **Functions** section.

1. Next to the function, from the ellipses menu (...), select **Manage**.

   :::image type="content" source="../media/how-to/assistants/logic-apps/edit-function-trigger.png" alt-text="Screenshot that shows the newly imported logic app function and the Manage button selected." lightbox="../media/how-to/assistants/logic-apps/edit-function-trigger.png":::

   The following screenshot shows a sample function specification for the example function:

   :::image type="content" source="../media/how-to/assistants/logic-apps/view-function-specification.png" alt-text="Screenshot that shows the function specification." lightbox="../media/how-to/assistants/logic-apps/view-function-specification.png":::

### How does authentication work for calls from Foundry to Azure Logic Apps?

Azure Logic Apps supports the following types of authentication for inbound calls from Foundry to the **Request** trigger in a logic app workflow:

- Shared Access Signature (SAS) based authentication

  When an AI assistant calls a function that runs a logic app workflow, Foundry sends a request to the *callback URL* in the workflow's **Request** trigger. You can get this callback URL, which includes an SAS, by using [Workflows - List callback Url](/rest/api/logic/workflows/list-callback-url) from the REST API for Azure Logic Apps.

  For SAS authentication, Azure Logic Apps also supports the following tasks:

  - Create SAS URLs with a specified validity period.
  - Use multiple keys and rotate them as needed.

  For more information, see [Generate a Shared Access Signature (SAS) key or token](/azure/logic-apps/logic-apps-securing-a-logic-app#generate-shared-access-signatures-sas).

- Microsoft Entra ID-based OAuth authentication policy

  Azure Logic Apps supports authentication for calls to request triggers by using OAuth with Microsoft Entra ID. You can specify authentication policies to use when validating OAuth tokens. For more information, see [Enable OAuth 2.0 with Microsoft Entra ID in Azure Logic Apps](/azure/logic-apps/logic-apps-securing-a-logic-app?tabs=azure-portal#enable-oauth-20-with-microsoft-entra-id).

For more information about securing inbound calls in Azure Logic Apps, see [Access for inbound calls to request-based triggers](/azure/logic-apps/logic-apps-securing-a-logic-app?tabs=azure-portal#access-for-inbound-calls-to-request-based-triggers).

## Related content

- [Full sample for Azure Logic Apps integration](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_logic_apps.py)
- [Learn more about Assistants](../concepts/assistants.md)
- [Learn more about Azure Logic Apps](/azure/logic-apps/logic-apps-overview)
- [Agent tools overview](overview.md)
