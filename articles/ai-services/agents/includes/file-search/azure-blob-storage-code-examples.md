## Quickstart – Use existing files in Azure Blob Storage with file search
In this example, we’ll use Azure AI Agent Service to create an agent that can help answer questions on information from files in Azure Blob Storage.

###  Prerequisites 
Complete the [standard agent setup](../../quickstart.md).

> [!NOTE]
> Azure Blob Storage is only available with the standard agent setup. The basic agent setup does not support this file source.

### Step 1: Create a project client
```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, VectorStoreDataSource, VectorStoreDataSourceAssetType
from azure.identity import DefaultAzureCredential


# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

credential = DefaultAzureCredential()
project_client = AIProjectClient.from_connection_string(
    credential=credential, conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)
```
### Step 2: Upload local files to your project Azure Blob Storage container
We will upload the local file to your project Azure Blob Storage container. This is the same storage account you connected to your agent during the agent setup. 
The project asset ID is the URI of the uploaded file and we print out this value. If you create more agents in the same project that want to use the uploaded file, you can reuse this asset ID.
That way you don't need to upload the file again.
```python
# We will upload the local file to your project Azure Blob Storage container and will use it for vector store creation.
_, asset_uri = project_client.upload_file("C:\\Users\\fosteramanda\\Downloads\\hub bicep\\azure-ai-agents\\data\\product_info_1.md")
print(f"Uploaded file, asset URI: {asset_uri}")

# create a vector store with no file and wait for it to be processed
ds = VectorStoreDataSource(asset_identifier=asset_uri, asset_type=VectorStoreDataSourceAssetType.URI_ASSET)
vector_store = project_client.agents.create_vector_store_and_poll(data_sources=[ds], name="sample_vector_store-3")
print(f"Created vector store, vector store ID: {vector_store.id}")
```
### Step 3: Create agent_1 with access to the file search tool

```python
# create a file search tool
file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

# notices that FileSearchTool as tool and tool_resources must be added or the assistant unable to search the file
agent_1 = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-assistant",
    instructions="You are helpful assistant",
    tools=file_search_tool.definitions,
    tool_resources=file_search_tool.resources,
)
# [END upload_file_and_create_agent_with_file_search]
print(f"Created agent_1, agent_1 ID: {agent_1.id}")

thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

message = project_client.agents.create_message(
    thread_id=thread.id, role="user", content="What feature does Smart Eyewear offer?"
)
print(f"Created message, message ID: {message.id}")

run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent_1.id)

project_client.agents.delete_vector_store(vector_store.id)
print("Deleted vector store")

project_client.agents.delete_agent(agent.id)
print("Deleted agent")

messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
```

### Step 4: Create second vector store using the previously uploaded file
```python

# create a vector store with no file and wait for it to be processed
ds_2 = VectorStoreDataSource(asset_identifier=asset_uri, asset_type=VectorStoreDataSourceAssetType.URI_ASSET)
vector_store_2 = project_client.agents.create_vector_store_and_poll(data_sources=[ds_2], name="sample_vector_store_2")
print(f"Created vector store, vector store ID: {vector_store.id}")

```

### Step 5: Create agent_2 with access to the file search tool
```python
file_search_tool_2 = FileSearchTool(vector_store_ids=[vector_store_2.id])
# notices that FileSearchTool as tool and tool_resources must be added or the assistant unable to search the file
agent_2 = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-assistant",
    instructions="You are helpful assistant",
    tools=file_search_tool_2.definitions,
    tool_resources=file_search_tool_2.resources,
)
# [END upload_file_and_create_agent_with_file_search]
print(f"Created agent, agent ID: {agent_2.id}")
```