---
title: Trigger an Azure AI Foundry agent using Logic Apps
description: Use this article to learn how to trigger an AI agent when an event occurs. 
ms.date: 03/20/2025
ms.topic: how-to
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
---

# Trigger an agent using Logic Apps

To streamline your workflow, you might want to automatically invoke your AI agent when an event occurs, such as receiving a new email, or getting a new customer ticket so that your AI agent can immediately respond to the new event without manual invocation.  

To automatically invoke an agent, you can select among hundreds of [triggers](/azure/logic-apps/logic-apps-workflow-actions-triggers) in Azure Logic Apps, and the Azure AI Foundry Agent Service connector. 


## What is a trigger? 

A trigger is the first item you need to add to your workflow, which allows you to connect to a specific service. When a specific event happens in this service, the trigger will invoke connectors, in this case a connector for the Azure AI Foundry Agent service.  

For example, consider a workflow with the *Microsoft Forms* connector (which has a trigger) that connects to a specific form. Whenever this form receives a new response, the trigger will recognize it and invoke the connectors following it in the workflow. You can then pass the form response as a message to your AI agent and leverage its tools to respond or take proper actions.  

To check if a specific connector has a trigger capability, view its documentation and see if it has a **Trigger** section. For example, the [Triggers](/connectors/microsoftforms/#triggers) section of the *Microsoft Forms* connector. 

## Prerequisite 

* [An existing agent](../quickstart.md)

## Set up 

1. Go to the Logic Apps page in the [Azure portal](https://portal.azure.com/#browse/Microsoft.Logic%2Fworkflows). 
1. Create a Logic Apps resource. Provide all required information, and select the **consumption - multi-tenant** type.

### Assign proper RBAC permissions

**Logic App resource**

1. Navigate to the **identity** page in your Logic App resource.  
1. Enable system assigned managed identity. 
1. Copy the object (principal) ID.

**AI Foundry project**

1. In the Azure portal, navigate to the AI Foundry project that has the AI agent you want to use. 
1. Select **access control** and click **add role assignment**. 
1. Select at least **AI Developer** and click **Next**. 
1. Select **User, group, or service principal** and select members 
1. Paste the object ID you got from the Logic App resource to search for your Logic App resource. Then select **Finish**. 

Once you have assigned the RBAC roles, go back to Logic App resource and click **Logic App designer**. You can add a trigger of your choice to your workflow. 

## Add Azure AI Foundry Agent Service connectors 

Start by adding the Azure AI Foundry Agent service connectors to your workflow. 

1. Click **add an action** and then search for **Azure AI Foundry Agent Service**. This will let you add connectors to your workflow.

    :::image type="content" source="../media/triggers/connectors.png" alt-text="A screenshot of the actions added to a workflow." lightbox="../media/triggers/connectors.png":::

1. Depending on your use-case, choose the actions you need. 

    If you want to create a new [thread](../concepts/threads-runs-messages.md#threads) for each new event of your trigger, add the following in sequence: 

    1. Create thread 
    1. Create run 
    1. Get run 
    1. List messages 

    If you want to create a new [run](../concepts/threads-runs-messages.md#runs) in the same thread for each new event, add the following in sequence: 

    1. Create run 
    1. Get run
    1. List messages 


> [!TIP] 
> * Since the AI Foundry Agent Service takes time to respond, we recommend adding a **delay** connector between **create run** and **get run**. 
> * You can click **parameters** on the top to create reusable parameters for Subscription ID and other values to avoid repetitive work.

## Create a connection

To create a connection, provide the following information.

* **Connection name**: give your connection a name. 

* **Project name**: your AI Foundry project endpoint. The format is `http://<aiservicename>.services.ai.azure.com/api/projects/<project name>`. 

## Configure the "create thread" connector (optional)

> [!NOTE]
> The **List Agent** connector only lists all the agents you have in your AI project, you don't need to provide any information for this connector. 

The **create thread** connector creates a new [thread](../concepts/threads-runs-messages.md#threads), which is a conversation session between an Agent and a user. Threads store [messages](../concepts/threads-runs-messages.md#messages) and automatically handle truncation to fit content into a model's context. 

To configure the **create thread** connector:

**messages (optional)**: You can add the message you want the AI agent to respond to. Add the role as **user** for the message you want the agent to respond to. It can be the event payload from the trigger, for example a form response field. It can also be a constant message, for example always triggering with the phrase "*what is the latest AI news this week?*"  

**Metadata (optional)**: The set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format and querying for objects via an API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.  

**Tool resources (optional)**: In addition to the tool resources you have provided in your agent, you can provide updated tool resources only applicable to your Thread. An example of tool resource: 

```json
[
  {
    "type": "bing_grounding",
    "bing_grounding": {
      "search_configurations": [
        {
          "connection_id": "/subscriptions/<subscription-id>/resourceGroups/<your resource group name>/providers/Microsoft.CognitiveServices/accounts/<your ai service name>/projects/<your project name>/connections/<your connection name>",
          "count": 7,
          "market": "en-US",
          "set_lang": "en",
          "freshness": "7d"
        }
      ]
    }
  }
]
```

## Configure the "create run" connector

The **create run** connector creates a new [run](../concepts/threads-runs-messages.md#runs), which is an activation of an Agent to begin running based on the contents of the thread. The agent uses its configuration (such as tool resources) and the thread's messages to perform tasks by calling models and tools. As part of a run, the agent appends messages to the thread. 

To configure the **create run** connector, click on it and provide the following information:

**Thread ID (required)**: the thread ID of the thread you just created. Click the function icon to select the **ID** parameter from your previous **create thread** connector output.

:::image type="content" source="../media/triggers/create-run.png" alt-text="A screenshot of the create run connector" lightbox="../media/triggers/create-run.png":::

**Assistant id (required)**: the ID of the agent you have created. 

**Messages (optional)**: you can add the message you want the AI agent to respond to. Add the role as **user** for the message you want the agent to respond to. It can be the event payload from the trigger, for example a form response field. It can also be a constant message, for example always triggering with the phrase "*what is the latest AI news this week?*"  

> [!TIP]
> Make sure you have added the message either in the run or thread connector. Otherwise, you will run into issues. 

## Configure the "get run" connector

The **get run** connector gets and retrieves the run you just created. 

**Thread ID parameter (required)**: The thread ID of the thread you just created. Click the function icon to select the **ID** parameter from your previous **create thread** connector output. 

**Run ID (required)**: the run ID of the run you just created. Click the function icon to select the **ID** parameter from your previous **create run** connector output. 

## Configure the "list messages" connector

The **list Messages** connector lists all messages in the current thread.  

**Thread ID parameter (required)**: The thread ID of the thread you just created. Click the function icon to select the **id** parameter from your previous **create thread** connector output. 

## Get a response from the Foundry Agent Service 

To get a response, you need a custom function to retrieve the exact response body from **list message** connector. 

1. Add the **compose** connector. 

1. Add the following string function to get just the response back: 

    `body('List_Messages')['data'][0]['content'][0]['text']['value']` 

    :::image type="content" source="../media/triggers/get-response.png" alt-text="A screenshot showing the compose connector." lightbox="../media/triggers/get-response.png":::

1. Add other connectors if needed. You can click **run** and click **run history** to check the status of your runs. 