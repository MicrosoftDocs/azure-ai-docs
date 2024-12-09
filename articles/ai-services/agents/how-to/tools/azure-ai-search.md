---
title: 'How to BYO AI Search index with the Azure AI Search tool'
titleSuffix: Azure OpenAI
description: Learn how to use Agents file search.
services: azure-ai-agent service
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 11/20/2024
author: fosteramanda
ms.author: fosteramanda
recommendations: false
zone_pivot_groups: selection-azure-ai-search
---

# BYO AI Search index with the Azure AI Search tool
::: zone pivot="overview"

Use an existing Azure AI Search index with the agent's Azure AI Search tool.

> [!NOTE] Azure AI Search indexes must meet the following requirements:
> - The index must contain at least one searchable & retrievable text field (type Edm.String) 
> - The index must contain at least one searchable vector field (type Collection(Edm.Single)) 
> - The index must use a vector profile/integrated vectorization

## Search types

**Index without semantic configuration**
- By default, the Azure AI Search tool runs a hybrid search (keyword + vector) on all text fields. 
<br>

**Index with semantic configuration**
- By default, the Azure AI Search tool can uses semantic or hybrid + semantic search on all text fields.

## File Types
The Azure AI Search tool currently only supports indexes with unstructured data. If you have structured data in your index, we cannot make any guarantees on the quality of the search results.
::: zone-end

::: zone pivot="setup"
## Setup: Create an agent that can use an existing Azure AI Search index
#### 1. Existing Azure AI Search index
One prerequite of using the Azure AI Search tool is to have an existing Azure AI Search index. If you don't have an existing index, you can create one in the Azure portal or via REST API.
-  [Quickstart: Create a vector index using the Azure portal](../../../search/search-get-started-portal-import-vectors.md)
- [Quickstart: Create a vector index using REST API](../../../search/search-get-started-vector.md)
#### 2. Complete the agent setup
- **Option 1: Standard Agent Setup using existing AI Search resource** If you want your agent to uses an existing AI Search resource to create new indexes or bring existing ones you should use the [standard agent setup and add your AI Search resourc ID](../../quickstart.md). 
- You can provide your Azure AI Search resource ID in the bicep file. Your resource ID should be in the format: `/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}`.
- **Option 2: Standard Agent Setup** If you want to create a new Azure AI Search resource for you agents to use when creating new indexes follow the [standard agent setup](../../quickstart.md).
- **Option 3: Basic Agent Setup** If you want your agent to use multitenant search and storage resources fully managed by Microsoft and connect your AI Search index later use the [basic agent setup](../../quickstart.md).

#### 3. Create a project connection to the Azure AI Search resource with the index you want to use
If you already connected the AI Search resource that contains the index you want to use to your project, skip this step.

1. In the Azure Portal, navigate to the AI Search resource that contains the index you want to use.
2. Make sure your ACS resource is set to “Both” API key and RBAC access control.
    :::image type="content" source="../../media/tools/ai-search/acs-azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/acs-azure-portal.png":::

3. In Azure AI Foundry, navigate to the project you created in the agent setup and Click on **Open in management center**.
    :::image type="content" source="../../media/tools/ai-search/project-studio.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/project-studio.png":::
4. Click on the **Connections** tab.
5. Click on **Add Connection**.
 :::image type="content" source="../../media/tools/ai-search/project-connections-page.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/project-connections-page.png":::
6. Select **Azure AI Search**.
 :::image type="content" source="../../media/tools/ai-search/select-acs.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/select-acs.png":::
1. Select the Azure AI Search resource that has the index you want to use and fill in the required fields. Both Managed Identity and Key-based authentication are supported. Once all the fields are filled in, click **Add connection**.
:::image type="content" source="../../media/tools/ai-search/acs-connection2.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/acs-connection2.png":::
1. Verify that the connection was successfully created.
:::image type="content" source="../../media/tools/ai-search/success-acs-connection.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/success-acs-connection.png":::
::: zone-end

::: zone pivot="code-examples"

## Quickstart – Use an existing Azure AI Search index with the Azure AI Search tool

In this quickstart, you'll learn how to use an existing Azure AI Search index with the Azure AI Search tool.

### Prerequisites
1. One prerequite of using the Azure AI Search tool is to have an existing Azure AI Search index. If you don't have an existing index, you can create one in the Azure portal or via REST API.
    - [Quickstart: Create a vector index using the Azure portal](../../../search/search-get-started-portal-import-vectors.md)
    - [Quickstart: Create a vector index using REST API](../../../search/search-get-started-vector.md)
2. Complete the [agent setup](../../quickstart.md).
3. Create a project connection to the Azure AI Search resource with the index you want to use.

### Step 1: Create an Azure AI Client

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import AzureAISearchTool

# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery" 
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-hub-name

connection_string = os.environ["PROJECT_CONNECTION_STRING"] 

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=connection_string,
)

```
### Step 2: Get the connection id for the Azure AI Search resource

Get the connection id of the Azure AI Search connection in the project. You can use the code snippet below to print the connection id of all the Azure AI Search connections in the project. 
```python
# AI Search resource connection id
# This code prints out the connection id of all the Azure AI Search connections in the project
# If you have more than one AI search connection, make sure to select the correct one that contains the index you want to use.
conn_list = project_client.connections.list()
conn_id = ""
for conn in conn_list:
    if conn.connection_type == "CognitiveSearch":
        print(f"Connection ID: {conn.id}")
```
The second way to get the connection id is to navigate to the project in the Azure AI Foundry and click on the **Connected resources** tab and then select your Azure AI Search resource.
:::image type="content" source="../../media/tools/ai-search/success-acs-connection.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/success-acs-connection.png":::
In the URL, you will see the wsid=/subscription/your-subscription-id..., this is the connection id you need to use. Copy everything that comes after wsid=.
:::image type="content" source="../../media/tools/ai-search/connection-id.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/connection-id.png":::

### Setep 3: Configure the Azure AI Search tool
Using the connection id you got in the previous step, you can now configure the Azure AI Search tool to use your Azure AI Search index.
```python
# TO DO: replace this value with the connection id of the search index
conn_id =  "/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-azure-ai-search-connection-name>"

# Initialize agent AI search tool and add the search index connection id and index name
# TO DO: replace <your-index-name> with the name of the index you want to use
ai_search = AzureAISearchTool()
ai_search.add_index(conn_id, "<your-index-name>")
```

### Step 4: Create an agent with the Azure AI Search tool enabled

# Create agent with AI search tool
```python
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-assistant",
    instructions="You are a helpful assistant",
    tools=ai_search.definitions,
    tool_resources = ai_search.resources,
    headers={"x-ms-enable-preview": "true"},
)
print(f"Created agent, ID: {agent.id}")
```

### Step 5: Ask the Agent questions about data in the index
For example, assuming the index contains health care plan information.
```python
# Create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")
 
# Create a message
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="what are my health insurance plan coverage types?",
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
    
assistant_message = ""
for message in messages.data:
    if message["role"] == "assistant":
        assistant_message = message["content"][0]["text"]["value"]

# Get the last message from the sender
print(f"Assistant response: {assistant_message}")
```

::: zone-end
