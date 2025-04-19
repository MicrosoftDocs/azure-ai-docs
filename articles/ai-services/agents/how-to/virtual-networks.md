---
title: 'How to use a virtual network with the Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to use your own virtual network with the Azure AI Agent Service. 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 02/24/2025
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.custom: azure-ai-agents
---

# Create a new network-secured agent with user-managed identity

Azure AI Agent Service offers a standard agent configuration with private networking, allowing you to bring your own (BYO) private virtual network. This setup creates an isolated network environment that lets you securely access data and perform actions while maintaining full control over your network infrastructure. This guide provides a step-by-step walkthrough of the setup process and outlines all necessary requirements.

> [!NOTE]
> Standard setup with private networking can only be configured by deploying the Bicep template described in this article. Once deployed, agents must be created using the SDK or REST API. You can't use the Azure AI Foundry portal to create agents in a project with private networking enabled.

## Benefits

- **No public egress**: foundational infrastructure ensures the right authentication and security for your agents and tools, without you having to do trusted service bypass.

- **Container injection**: allows the platform network to host APIs and inject a subnet into your network, enabling local communication of your Azure resources within the same virtual network.

- **Private resource access**: If your resources are marked as private and nondiscoverable from the internet, the platform network can still access them, provided the necessary credentials and authorization are in place.

### Known limitations

- Azure Blob Storage: Using Azure Blob Storage files with the File Search tool isn't supported.

## Prerequisites

1. An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
2. [Python 3.8 or later](https://www.python.org/)
3. Ensure that the individual deploying the template has the [Azure AI Developer role](/azure/ai-foundry/concepts/rbac-azure-ai-foundry) assigned at the resource group level where the template is being deployed.
4. Additionally, to deploy the template, you need to have the preset [Role Based Access Administrator](/azure/role-based-access-control/built-in-roles/privileged#role-based-access-control-administrator) role at the subscription level.
    * The **Owner** role at the subscription level satisfies this requirement.
    * The specific admin role that is needed is `Microsoft.Authorization/roleAssignments/write`
5. Ensure that each team member who wants to use the Agent Playground or SDK to create or edit agents has been assigned the built-in **Azure AI Developer** [RBAC role](../../../ai-foundry/concepts/rbac-azure-ai-foundry.md) for the project.
    * Note: assign these roles after the template has been deployed
    * The minimum set of permissions required is: **agents/*/read**, **agents/*/action**, **agents/*/delete**  
5. Install [the Azure CLI and the machine learning extension](/azure/machine-learning/how-to-configure-cli). If you have the CLI already installed, make sure it's updated to the latest version.
6. Register providers. The following providers must be registered:
    * `Microsoft.KeyVault`
    * `Microsoft.CognitiveServices`
    * `Microsoft.Storage`
    * `Microsoft.MachineLearningServices`
    * `Microsoft.Search`
    * `Microsoft.Network`
    * `Microsoft.App`
    * To use Bing Search tool: `Microsoft.Bing`

    ```console
       az provider register --namespace 'Microsoft.KeyVault'
       az provider register --namespace 'Microsoft.CognitiveServices'
       az provider register --namespace 'Microsoft.Storage'
       az provider register --namespace 'Microsoft.MachineLearningServices'
       az provider register --namespace 'Microsoft.Search'
       # only to use Grounding with Bing Search tool
       az provider register --namespace 'Microsoft.Bing'
    ```

## Create a new network-secured agent with user-managed identity

**Network secured setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage. The following bicep template provides:

* Resources for the hub, project, storage account, key vault, AI Services, and Azure AI Search are created for you. The AI Services, AI Search, and Azure Blob Storage account are connected to your project/hub, and a gpt-4o-mini model is deployed in the westus2 region.
* Customer-owned resources are secured with a provisioned managed network and authenticated with a user-managed identity with the necessary RBAC (Role-Based Access Control) permissions. Private links and DNS (Domain Name System) zones are created on behalf of the customer to ensure network connectivity.

<br/>

<details>
<summary><b> Bicep Technical Details</b>
</summary>   

**The Bicep template automates the following configurations and resource provisions:**
* Creates a [User Assigned Identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp#create-a-user-assigned-managed-identity).
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
   * Azure resources subnet
      * Enables service endpoints for:
         * `Microsoft.KeyVault`
         * `Microsoft.Storage`
         * `Microsoft.CognitiveServices`
   * Agent resources subnet
      * Configured with subnet delegations for:
         * `Microsoft.app/environments` 
* Provisions dependent resources
   * Azure Key Vault, Azure Storage, Azure OpenAI/AI Services, and Azure AI Search resources are created.
   * All resources are configured with:
      * Disabled public network access
      * Private endpoints in the Azure Resource subnet
      * Private DNS integration enabled
      * User assigned identity for authentication
* Creates a hub and project using the resources provisioned and configures them to use the Agent Resource Subnet.  
   * Accomplished by configuring the `capabilityHost` (a subresource of hub/project) to use the Agent Resource Subnet for network isolation and secure communication. 
</details>

### Option 1: autodeploy the bicep template

| Template | Description   | Autodeploy |
| ------------------- | -----------------------------------------------| -----------------------|
| `network-secured-agent.bicep`  | Deploy a network secured agent setup that uses user-managed identity authentication on the Agent connections. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Fmain%2Fscenarios%2FAgents%2Fsetup%2Fnetwork-secured-agent-thread-storage%2Fazuredeploy.json)

### Option 2: manually deploy the bicep template

1. To manually run the bicep templates, [download the template from GitHub](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Agents/setup/network-secured-agent-thread-storage). Download the following from the `network-secured-agent` folder:
    1. `main.bicep`
    1. `azuredeploy.parameters.json`
    1. `modules-network-secured folder`
1. To authenticate to your Azure subscription from the Azure CLI, use the following command: 

    ```console
    az login
    ```

1. Create a resource group:

    ```console
    az group create --name {my_resource_group} --location eastus
    ```

    Make sure you have the Azure AI Developer role for the resource group you created. 

1. Using the resource group you created in the previous step and one of the template files (`network-secured-agent`), run one of the following commands: 

    1. To use default resource names, run:

        ```console
        az deployment group create --resource-group {my_resource_group} --template-file main.bicep
        ```

    1. To specify custom names for the hub, project, storage account, and/or Azure AI service resources run the following command. A randomly generated suffix is added to prevent accidental duplication.

        ```console
        az deployment group create --resource-group {my_resource_group} --template-file main.bicep --parameters aiHubName='your-hub-name' aiProjectName='your-project-name' storageName='your-storage-name' aiServicesName='your-ai-services-name' 
    
        ```

    1. To customize other parameters, including the OpenAI model deployment, download, and edit the `azuredeploy.parameters.json` file, then run:
    
        ```console
        az deployment group create --resource-group {my_resource_group} --template-file main.bicep --parameters @azuredeploy.parameters.json 
        ```

## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent's ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model's context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread's Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

> [!TIP]
> The following code shows how to create and run an agent using the Python Azure SDK. For additional languages, see the [quickstart](../quickstart.md).

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

For example, your connection string might look something like:

`eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name`

Set this connection string as an environment variable named `PROJECT_CONNECTION_STRING`.

> [!NOTE]
> The following code sample shows creating an agent using Python. See the [quickstart](../quickstart.md) for examples in other programming languages.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from typing import Any
from pathlib import Path

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# It should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery"
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name
# You will need to login to your Azure subscription using the Azure CLI "az login" command, and set the environment variables.

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
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
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
```

## Next steps

Once you've provisioned your agent, you can add tools such as [Grounding with Bing Search](./tools/bing-grounding.md) to enhance their capabilities.
