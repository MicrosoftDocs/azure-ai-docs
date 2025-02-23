---
title: 'Set up an agent with standard setup and your own vnet in the Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to use your own vnet with the Azure AI Agent Service. 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 02/22/2025
author: fosteramanda
ms.author: fosteramanda
ms.custom: azure-ai-agents
---

# QuickStart: Create a new network-secured agent with user-managed identity

## Prerequisites

1. An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
2. [Python 3.8 or later](https://www.python.org/)
3. Make sure the person deploying the template has the role: **Contributor** assigned at the resource group level, and they're deploying this template in that specific resource group (specific role). [Learn more](https://learn.microsoft.com/azure/ai-studio/concepts/rbac-ai-studio)
4. To deploy the bicep template and configure RBAC (Role-Based Access Control), you need to have the role: **Role Based Access Administrator** at the subscription level.  
    * Note: The **Owner** role at the subscription level satisfies this requirement.
5. Install [the Azure CLI and the machine learning extension](/azure/machine-learning/how-to-configure-cli). If you have the CLI already installed, make sure it's updated to the latest version.
6. Register providers
    The following providers must be registered:

    * Microsoft.KeyVault
    * Microsoft.CognitiveServices
    * Microsoft.Storage
    * Microsoft.MachineLearningServices
    * Microsoft.Search
    * Microsoft.Network
    * To use Bing Search tool: Microsoft.Bing

    ```console
       az provider register --namespace 'Microsoft.KeyVault'
       az provider register --namespace 'Microsoft.CognitiveServices'
       az provider register --namespace 'Microsoft.Storage'
       az provider register --namespace 'Microsoft.MachineLearningServices'
       az provider register --namespace 'Microsoft.Search'
       # only to use Grounding with Bing Search tool
       az provider register --namespace 'Microsoft.Bing'
    ```

## Deploy the Bicep Template

**Network Secured Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage.

* Resources for the hub, project, storage account, key vault, AI Services, and Azure AI Search are created for you. The AI Services, AI Search, and Azure Blob Storage account are connected to your project/hub, and a gpt-4o-mini model is deployed in the westus2 region.
* Customer-owned resources are secured with a provisioned managed network and authenticated with a User Managed Identity with the necessary RBAC permissions. Private links and DNS zones are created on behalf of the customer to ensure network connectivity.

<br/>

<details>
<summary><b> Bicep Technical Details</b>
</summary>   

**The Bicep template automates the following configurations and resource provisions:*** Creates a User Assigned Identity. [Learn more](../../../azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp#create-a-user-assigned-managed-identity)
  * The User Assigned Managed Identity requires the following Role-Based Access Roles: 
    * KeyVault Secret Officer
    * KeyVault Contributor
    * Storage Blob Data Owner
    * Storage Queue Data Contributor
    * Cognitive Services Contributor
    * Cognitive Services OpenAI User
    * Search Index Data Contributor
    * Search Service Contributor

* Configures a managed virtual network with two subnet resources:
   * Azure Resource Subnet
      * Enables Service Endpoints for:
         * Microsoft.KeyVault
         * Microsoft.Storage
         * Microsoft.CognitiveServices
   * Agent Resource Subnet
      * Configured with Subnet Delegations for:
         * Microsoft.app/environments 
* Provisions Dependent Resources
   * Azure Key Vault, Azure Storage, AOAI/AI Services, and Azure AI Search resources are created.
   * All resources are configured with:
      * Disabled public network access
      * Private endpoints in the Azure Resource subnet
      * Private DNS integration enabled
      * User Assigned Identity for authentication
* Creates a hub and project using the resources provisioned and configures them to use the Agent Resource Subnet.  
   * Accomplished by configuring the capabilityHost (a subresource of hub/project) to use the Agent Resource Subnet for network isolation and secure communication. 
</details>

<br/>

### Option 1: Autodeploy the Bicep Template

| Template | Description   | Autodeploy |
| ------------------- | -----------------------------------------------| -----------------------|
| `network-secured-agent.bicep`  | Deploy a network secured agent setup that uses User Managed Identity authentication on the Agent Connections. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fnetwork-secured-agent%2Fazuredeploy.json)

### Option 2: Manually Deploy the Bicep Template

1. To manually run the bicep templates, [download the template from GitHub](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.azure-ai-agent-service/network-secured-agent). Download the following from the network-secured-agent folder:
    1. main.bicep
    1. azuredeploy.parameters.json
    1. modules-network-secured folder
1. To authenticate to your Azure subscription from the Azure CLI, use the following command: 

    ```console
        az login
    ```

1. Create a resource group

    ```console
        az group create --name {my_resource_group} --location eastus
    ```

    Make sure you have the role Azure AI Developer on the resource group you created. 
1. Using the resource group you created in the previous step and one of the template files (either basic-agent-keys.bicep or basic-agent-identity.bicep), run one of the following commands: 

    1. To use default resource names, run:

    ```console
        az deployment group create --resource-group {my_resource_group} --template-file main.bicep
    ```

    1. To specify custom names for the hub, project, storage account, and/or Azure AI service resources (Note: a randomly generated suffix is added to prevent accidental duplication), run:

    ```console
        az deployment group create --resource-group {my_resource_group} --template-file main.bicep --parameters aiHubName='your-hub-name' aiProjectName='your-project-name' storageName='your-storage-name' aiServicesName='your-ai-services-name' 

    ```

     1. To customize other parameters, including the OpenAI model deployment, download and edit the azuredeploy.parameters.json file, then run:

    ```console
        az deployment group create --resource-group {my_resource_group} --template-file main.bicep --parameters @azuredeploy.parameters.json 
    ```

## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

**The following code shows how to create and run an agent using Python (Azure SDK):**

* C#: See the [C# quickstart](../includes/quickstart-csharp.md)
* Python OpenAI SDK: See the [Python OpenAI SDK quickstart](../includes/quickstart-python-openai.md)

Run the following commands to install the python packages.

```console
pip install azure-ai-projects
pip install azure-identity
```
Next, to authenticate your API requests and run the program, use the [az login](/cli/azure/authenticate-azure-cli-interactively) command to sign into your Azure subscription.

```azurecli
az login
```

Use the following code to create and run an agent. To run this code, you need to create a connection string using information from your project. This string is in the format:

`<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>`

[!INCLUDE [connection-string-portal](../includes/connection-string-portal.md)]

`HostName` can be found by navigating to your `discovery_url` and removing the leading `https://` and trailing `/discovery`. To find your `discovery_url`, run this CLI command:

```azurecli
az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
```

For example, your connection string may look something like:

`eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name`

Set this connection string as an environment variable named `PROJECT_CONNECTION_STRING`.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from typing import Any
from pathlib import Path

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery"
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Create an instance of the CodeInterpreterTool
    code_interpreter = CodeInterpreterTool()

    # The CodeInterpreterTool needs to be included in creation of the agent
    agent = project_client.agents.create_agent(
        model="gpt-4o-mini",
        name="my-agent",
        instructions="You are helpful agent",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Could you please create a bar chart for the operating profit using the following data and provide the file to me? Company A: $1.2 million, Company B: $2.5 million, Company C: $3.0 million, Company D: $1.8 million",
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # Get messages from the thread
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")

    # Get the last message from the sender
    last_msg = messages.get_last_text_message_by_role("assistant")
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")

    # Generate an image file for the bar chart
    for image_content in messages.image_contents:
        print(f"Image File ID: {image_content.image_file.file_id}")
        file_name = f"{image_content.image_file.file_id}_image_file.png"
        project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / file_name}")

    # Print the file path(s) from the messages
    for file_path_annotation in messages.file_path_annotations:
        print(f"File Paths:")
        print(f"Type: {file_path_annotation.type}")
        print(f"Text: {file_path_annotation.text}")
        print(f"File ID: {file_path_annotation.file_path.file_id}")
        print(f"Start Index: {file_path_annotation.start_index}")
        print(f"End Index: {file_path_annotation.end_index}")
        project_client.agents.save_file(file_id=file_path_annotation.file_path.file_id, file_name=Path(file_path_annotation.text).name)

    # Delete the agent once done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
