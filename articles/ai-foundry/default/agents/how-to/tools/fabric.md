---
title: "How to use the data agents in Microsoft Fabric for the Microsoft AI Foundry Agent Service"
titleSuffix: Azure AI Foundry
description: Learn how to perform data analytics in Microsoft Foundry with the Fabric data agent.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 11/13/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom:
  - build-2025
---

# Use the Microsoft Fabric data agent (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

Integrate your Azure AI Foundry Agent with the [**Microsoft Fabric data agent**](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. The Fabric data agent transforms enterprise data into conversational Question/Answer systems, allowing users to interact with the data through chat and uncover data-driven and actionable insights. 

You need to first build and publish a Fabric data agent and then connect your Fabric data agent with the published endpoint. When a user sends a query, the will first determine if the Fabric data agent should be leveraged or not. If so, it will use the end user’s identity to generate queries over data they have access to. Lastly, the agent will generate responses based on queries returned from Fabric data agents. With Identity Passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection.

## Prerequisites
> [!NOTE]
> * The model you selected in Azure AI Foundry Agent setup is only used for agent orchestration and response generation. It doesn't impact which model Fabric data agent uses for NL2SQL operation.
> * To help your model invoke your Microsoft Fabric tool in the expected way, make sure you update agent instructions with descriptions of your Fabric data agent and what data it can access. An example is "for customer and product sales related data, please use the Fabric tool". We recommend using a smaller AI model such as `gpt-4o-mini`. You can also use `tool_choice` parameter in SDK or API to force Fabric tool to be invoked at each run. 

* You have created and published a [Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312910)

* Developers and end users have at least `Azure AI User` RBAC role. 

* Developers and end users have at least `READ` access to the Fabric data agent and the underlying data sources it connects with.

* Your Fabric Data Agent and Azure AI Foundry Agent need to be in the same tenant.

* The Fabric data agent only supports user identity authentication. Service Principal Name (SPN) authentication is not supported.

* Your Azure AI Foundry Project endpoint.

* The name of your Microsoft Fabric connection name. 

## Code example

> [!NOTE]
> - To run this code you will need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.
> - Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    MicrosoftFabricAgentTool,
    FabricDataAgentToolParameters,
    ToolProjectConnection,
)

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant.",
            tools=[
                MicrosoftFabricAgentTool(
                    fabric_dataagent_preview=FabricDataAgentToolParameters(
                        project_connections=[
                            ToolProjectConnection(project_connection_id=os.environ["FABRIC_PROJECT_CONNECTION_ID"])
                        ]
                    )
                )
            ],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    user_input = input("Enter your question for Fabric (e.g., 'Tell me about sales records'): \n")

    response = openai_client.responses.create(
        tool_choice="required",
        input=user_input,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    print(f"Response output: {response.output_text}")
```

> [!NOTE]
> * Make sure you have **published** the data agent in Fabric.

## Next steps

[See the full sample for Fabric data agent.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_fabric.py)
