---
title: Connect Agents to Foundry IQ Knowledge Bases
titleSuffix: Microsoft Foundry
description: Connect Foundry Agent Service to a Foundry IQ knowledge base (Azure AI Search) for grounded retrieval and citation-backed responses.
author: haileytap
ms.author: haileytapia
ms.reviewer: fsunavala
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/27/2026
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Connect a Foundry IQ knowledge base to Foundry Agent Service

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

In this article, you learn how to connect a knowledge base in Foundry IQ to an agent in Foundry Agent Service. The connection uses the [Model Context Protocol (MCP)](./tools/model-context-protocol.md) to facilitate tool calls. When invoked by the agent, the knowledge base orchestrates the following operations:

- Plans and decomposes a user query into subqueries.
- Processes the subqueries simultaneously using keyword, vector, or hybrid techniques.
- Applies semantic reranking to identify the most relevant results.
- Synthesizes the results into a unified response with source references.

The agent uses the response to ground its answers in enterprise data or web sources, ensuring factual accuracy and transparency through source attribution.

For an end-to-end example of integrating Azure AI Search and Foundry Agent Service for knowledge retrieval, see the [agentic-retrieval-pipeline-example](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/agentic-retrieval-pipeline-example) Python sample on GitHub.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | - | - | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

- An [Azure AI Search service](/azure/search/search-create-service-portal) with a [knowledge base](/azure/search/agentic-retrieval-how-to-create-knowledge-base) containing one or more [knowledge sources](/azure/search/agentic-knowledge-source-overview).
- A [Microsoft Foundry project](../../../how-to/create-projects.md) with an [LLM deployment](../../../foundry-models/how-to/create-model-deployments.md), such as `gpt-4.1-mini`.
- [Authentication and permissions](#authentication-and-permissions) on your search service and project.
- The latest preview Python SDK or the 2025-11-01-preview REST API version.

### Authentication and permissions

We recommend role-based access control for production deployments. If roles aren't feasible, skip this section and use key-based authentication instead.

#### [Microsoft Foundry](#tab/foundry)

- On the parent resource of your project, you need the **Azure AI User** role to access model deployments and create agents. **Owners** automatically get this role when they create the resource. Other users need a specific role assignment. For more information, see [Role-based access control in Foundry portal](/azure/ai-foundry/concepts/rbac-foundry).

- On the parent resource of your project, you need the **Azure AI Project Manager** role to create a project connection for MCP authentication and either **Azure AI User** or **Azure AI Project Manager** to use the MCP tool in agents.

- On your project, create a system-assigned managed identity for interactions with Azure AI Search.

#### [Azure AI Search](#tab/search)

- On your search service, assign the **Search Index Data Reader** role to your project's managed identity for read-only access to search indexes.

- If your agent needs to write documents to search indexes, also assign the **Search Index Data Contributor** role.

- For indexed content with access control lists (ACLs), include [permission metadata fields](/azure/search/search-document-level-access-overview) in your search index and pass user tokens via the `x-ms-query-source-authorization` header at query time to filter results based on the user's identity. For more information, see [Query-time ACL and RBAC enforcement](/azure/search/search-query-access-control-rbac-enforcement).

- For remote SharePoint knowledge sources, the `x-ms-query-source-authorization` header passes the user's identity, enabling SharePoint to enforce document permissions at query time. Content isn't indexed. Instead, SharePoint applies permissions directly via the Copilot Retrieval API. For more information, see [Create a remote SharePoint knowledge source](/azure/search/agentic-knowledge-source-how-to-sharepoint-remote).

---

### Required values

Use the following values in the code samples.

| Value | Where to get it | Example |
|---|---|---|
| Project endpoint (`project_endpoint`) | Find it in your project details in the Microsoft Foundry portal. | `https://your-resource.services.ai.azure.com/api/projects/your-project` |
| Project resource ID (`project_resource_id`) | Copy the project ARM resource ID from Azure portal or use Azure CLI to query the resource ID. | `/subscriptions/.../resourceGroups/.../providers/Microsoft.MachineLearningServices/workspaces/.../projects/...` |
| Azure AI Search endpoint (`search_service_endpoint`) | Find it on your Azure AI Search service **Overview** page (the service URL) in the Azure portal. | `https://your-search-service.search.windows.net` |
| Knowledge base name (`knowledge_base_name`) | Use the knowledge base name you created in Azure AI Search. | `hr-policy-kb` |
| Project connection name (`project_connection_name`) | Choose a name for the project connection you create. | `my-kb-mcp-connection` |
| Agent name (`agent_name`) | Choose a name for the agent version you create. | `hr-assistant` |
| Model deployment name (`deployed_LLM`) | Find it in your Microsoft Foundry project model deployments. | `gpt-4.1-mini` |

## Create a project connection

Create a `RemoteTool` connection on your Microsoft Foundry project. This connection uses the project's managed identity to target the MCP endpoint of the knowledge base, allowing the agent to securely communicate with Azure AI Search for retrieval operations.

### [Python](#tab/python)

```python
import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Provide connection details
credential = DefaultAzureCredential()
project_resource_id = "{project_resource_id}" # e.g. /subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{account_name}/projects/{project_name}
project_connection_name = "{project_connection_name}"
mcp_endpoint = "{search_service_endpoint}/knowledgebases/{knowledge_base_name}/mcp?api-version=2025-11-01-preview" # This endpoint enables the MCP connection between the agent and knowledge base

# Get bearer token for authentication
bearer_token_provider = get_bearer_token_provider(credential, "https://management.azure.com/.default")
headers = {
  "Authorization": f"Bearer {bearer_token_provider()}",
}

# Create project connection
response = requests.put(
  f"https://management.azure.com{project_resource_id}/connections/{project_connection_name}?api-version=2025-10-01-preview",
  headers = headers,
  json = {
    "name": project_connection_name,
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "ProjectManagedIdentity",
      "category": "RemoteTool",
      "target": mcp_endpoint,
      "isSharedToAll": True,
      "audience": "https://search.azure.com/",
      "metadata": { "ApiType": "Azure" }
    }
  }
)

response.raise_for_status()
print(f"Connection '{project_connection_name}' created or updated successfully.")
```

### [REST](#tab/rest)

Use the [Azure CLI](/cli/azure/what-is-azure-cli) to get an access token for Azure Resource Manager:

```azurecli
az account get-access-token --scope https://management.azure.com/.default --query accessToken -o tsv
```

Create the project connection by making a `PUT` request to Azure Resource Manager:

```HTTP
PUT https://management.azure.com/{project_resource_id}/connections/{project_connection_name}?api-version=2025-10-01-preview
Authorization: Bearer {management_access_token}
Content-Type: application/json

{
  "name": "{project_connection_name}",
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "ProjectManagedIdentity",
    "category": "RemoteTool",
    "target": "{search_service_endpoint}/knowledgebases/{knowledge_base_name}/mcp?api-version=2025-11-01-preview", // This endpoint enables the MCP connection between the agent and knowledge base
    "isSharedToAll": true,
    "audience": "https://search.azure.com/",
    "metadata": {
      "ApiType": "Azure"
    }
  }
}
```

---

## Optimize agent instructions for knowledge retrieval

To improve knowledge base invocations and produce citation-backed answers, start with instructions like the following:

```plaintext
You are a helpful assistant.

Use the knowledge base tool to answer user questions.
If the knowledge base doesn't contain the answer, respond with "I don't know".

When you use information from the knowledge base, include citations to the retrieved sources.
```

This instruction template optimizes for:

- **Higher MCP tool invocation rates**: Explicit directives ensure the agent consistently calls the knowledge base tool rather than relying on its training data.
- **Clear source attribution**: Citations make it easier to validate where information came from.

> [!TIP]
> While this template provides a strong foundation, evaluate and iterate on the instructions based on your specific use case and objectives. Test different variations to find what works best for your scenario.

## Create an agent with the MCP tool

Create an agent that integrates the knowledge base as an MCP tool. The agent uses a system prompt to instruct when and how to call the knowledge base. It follows instructions on how to answer questions and automatically maintains its tool configuration and settings across conversation sessions.

Add the knowledge base MCP tool with the project connection you previously created. This tool orchestrates query planning, decomposition, and retrieval across configured knowledge sources. The agent uses this tool to answer queries.

> [!NOTE]
> Azure AI Search knowledge bases expose the `knowledge_base_retrieve` MCP tool for agent integration. This is the only tool currently supported for use with Foundry Agent Service.

### [Python](#tab/python)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from azure.identity import DefaultAzureCredential

# Provide agent configuration details
credential = DefaultAzureCredential()
mcp_endpoint = "{search_service_endpoint}/knowledgebases/{knowledge_base_name}/mcp?api-version=2025-11-01-preview"
project_endpoint = "{project_endpoint}" # e.g. https://your-foundry-resource.services.ai.azure.com/api/projects/your-foundry-project
project_connection_name = "{project_connection_name}"
agent_name = "{agent_name}"
agent_model = "{deployed_LLM}" # e.g. gpt-4.1-mini

# Create project client
project_client = AIProjectClient(endpoint = project_endpoint, credential = credential)

# Define agent instructions (see "Optimize agent instructions" section for guidance)
instructions = """
You are a helpful assistant that must use the knowledge base to answer all the questions from user. You must never answer from your own knowledge under any circumstances.
Every answer must always provide annotations for using the MCP knowledge base tool and render them as: `【message_idx:search_idx†source_name】`
If you cannot find the answer in the provided knowledge base you must respond with "I don't know".
"""

# Create MCP tool with knowledge base connection
mcp_kb_tool = MCPTool(
    server_label = "knowledge-base",
    server_url = mcp_endpoint,
    require_approval = "never",
    allowed_tools = ["knowledge_base_retrieve"],
    project_connection_id = project_connection_name
)

# Create agent with MCP tool
agent = project_client.agents.create_version(
    agent_name = agent_name,
    definition = PromptAgentDefinition(
        model = agent_model,
        instructions = instructions,
        tools = [mcp_kb_tool]
    )
)

print(f"Agent '{agent_name}' created or updated successfully.")
```

### [REST](#tab/rest)

Get an access token for Microsoft Foundry:

```azurecli
az account get-access-token --scope https://ai.azure.com/.default --query accessToken -o tsv
```

Create the agent by sending a `POST` request to Foundry Agent Service:

```HTTP
POST {project_endpoint}/agents/{agent_name}/versions?api-version=2025-11-15-preview
Authorization: Bearer {foundry_access_token}
Content-Type: application/json

{
  "definition": {
    "model": "{deployed_llm}",
    "instructions": "\nYou are a helpful assistant that must use the knowledge base to answer all the questions from user. You must never answer from your own knowledge under any circumstances.\nEvery answer must always provide annotations for using the MCP knowledge base tool and render them as: `【message_idx:search_idx†source_name】`\nIf you cannot find the answer in the provided knowledge base you must respond with \"I don't know\".\n",
    "tools": [
      {
        "server_label": "knowledge-base",
        "server_url": "{search_service_endpoint}/knowledgebases/{knowledge_base_name}/mcp?api-version=2025-11-01-preview",
        "require_approval": "never",
        "allowed_tools": [
          "knowledge_base_retrieve"
        ],
        "project_connection_id": "{project_connection_name}",
        "type": "mcp"
      }
    ],
    "kind": "prompt"
  }
}
```

---

### Connect to a remote SharePoint knowledge source

[!INCLUDE [foundry-iq-limitation](../../includes/foundry-iq-limitation.md)]

Optionally, if your knowledge base includes a [remote SharePoint knowledge source](/azure/search/agentic-knowledge-source-how-to-sharepoint-remote), you must also include the `x-ms-query-source-authorization` header in the MCP tool connection.

#### [Python](#tab/python)

```python
from azure.identity import get_bearer_token_provider

# Create MCP tool with SharePoint authorization header
mcp_kb_tool = MCPTool(
    server_label = "knowledge-base",
    server_url = mcp_endpoint,
    require_approval = "never",
    allowed_tools = ["knowledge_base_retrieve"],
    project_connection_id = project_connection_name,
    headers = {
        "x-ms-query-source-authorization": get_bearer_token_provider(credential, "https://search.azure.com/.default")()
    }
)
```

#### [REST](#tab/rest)

Get an access token for Azure AI Search:

```azurecli
az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
```

Provide the header and token in the MCP tool configuration:

```HTTP
    "tools": [
      {
        "server_label": "knowledge-base",
        "server_url": "{search_service_endpoint}/knowledgebases/{knowledge_base_name}/mcp?api-version=2025-11-01-preview",
        "require_approval": "never",
        "allowed_tools": [
          "knowledge_base_retrieve"
        ],
        "project_connection_id": "{project_connection_name}",
        "type": "mcp",
        "headers": {
            "x-ms-query-source-authorization": "{search-bearer-token}"
        }
      }
    ]
```

---

## Invoke the agent with a query

Create a conversation session and send a user query to the agent. When appropriate, the agent orchestrates calls to the MCP tool to retrieve relevant content from the knowledge base. The agent then synthesizes this content into a natural-language response that cites the source documents.

### [Python](#tab/python)

```python
# Get the OpenAI client for responses and conversations
openai_client = project_client.get_openai_client()

# Create conversation
conversation = openai_client.conversations.create()

# Send request to trigger the MCP tool
response = openai_client.responses.create(
    conversation = conversation.id,
    input = """
        Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
        Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
    """,
    extra_body = {"agent": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response: {response.output_text}")
```

The output should be similar to the following:

```
Response: Suburban belts display larger December brightening than urban cores, even though absolute light levels are higher downtown, primarily because holiday lights increase most dramatically in the suburbs and outskirts of major cities. This is due to more yard space and a prevalence of single-family homes in suburban areas, which results in greater use of decorative holiday lighting. By contrast, central urban areas experience a smaller increase in lighting during the holidays, typically 20 to 30 percent brightening, because of their different building structures and possibly less outdoor space for such decorations. This pattern holds true across the United States as part of the nationally shared tradition of increased holiday lighting in December (Sources: earth_at_night_508_page_174, earth_at_night_508_page_176, earth_at_night_508_page_175).

The Phoenix nighttime street grid is sharply visible from space due to the city's layout along a regular grid of city blocks and streets with extensive street lighting. The major street grid is oriented mostly north-south, with notable diagonal thoroughfares like Grand Avenue that are also brightly lit. The illuminated grid reflects the widespread suburban and residential development fueled by automobile use in the 20th century, which led to optimal access routes to new real estate on the city's borders. Large shopping centers, strip malls, gas stations, and other commercial properties at major intersections also contribute to the brightness. Additionally, parts of the Phoenix metropolitan area remain dark where there are parks, recreational land, and agricultural fields, providing contrast that highlights the lit urban grid (Sources: earth_at_night_508_page_104, earth_at_night_508_page_105).

In contrast, large stretches of the interstate between Midwestern cities remain comparatively dim because although the transportation corridors are well-established, many rural and agricultural areas lack widespread nighttime lighting. The interstate highways are visible but do not have the same continuous bright lighting found in the dense urban grids and commercial suburban zones. The transportation network is extensive, but many roadways running through less populated regions have limited illumination, which renders them less visible in nighttime satellite imagery (Sources: earth_at_night_508_page_124, earth_at_night_508_page_125).

References:
- earth_at_night_508_page_174, earth_at_night_508_page_176, earth_at_night_508_page_175 (Holiday lighting and suburban December brightening)
- earth_at_night_508_page_104, earth_at_night_508_page_105 (Phoenix urban grid visibility)
- earth_at_night_508_page_124, earth_at_night_508_page_125 (Interstate lighting and Midwestern dim stretches)
```

### [REST](#tab/rest)

Send an empty `POST` request to create a conversation session:

```HTTP
### Create conversation
POST {project_endpoint}/openai/conversations?api-version=2025-11-15-preview
Authorization: Bearer {foundry_access_token}
Content-Type: application/json

{}
```

The response includes a conversation `id`, which you can use to send a query to the agent:

```HTTP
### Send request to trigger the MCP tool
POST {project_endpoint}/openai/responses?api-version=2025-11-15-preview
Authorization: Bearer {foundry_access_token}
Content-Type: application/json

{
    "conversation": "{conversation_id}",
    "input": "\nWhy do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?\nWhy is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?\n",
    "agent": {
        "name": "{agent_name}",
        "type": "agent_reference"
    }
}
```

The response includes metadata about the agent execution, tool calls, and the generated output. The most relevant part of the response is the `text` in the `content` field, which should be similar to the following:

```
Suburban belts display larger December brightening in nighttime lights than urban cores, even though absolute light levels are higher downtown, primarily because suburban areas have more yard space and a prevalence of single-family homes where holiday lighting decorations are more commonly used. In contrast, central urban areas see a smaller increase in lighting during the holidays\u2014typically a 20 to 30 percent brightening\u2014as the density and types of dwellings (e.g., apartment buildings) often limit outdoor decorative lighting. This phenomenon was observed across the United States and reflects cultural practices of increased holiday lighting during Christmas and New Year\u0027s, particularly in suburban and residential neighborhoods that allow for more extensive displays [source: earth_at_night_508_page_174_verbalized, earth_at_night_508_page_176_verbalized].

Regarding the visibility of the Phoenix nighttime street grid from space, the sharply visible grid reflects the regular, planned layout of city blocks and streets in the Phoenix metropolitan area, common to many cities in the central and western United States. The urban grid is illuminated by street lighting, large shopping centers, strip malls, gas stations, and industrial and commercial properties concentrated along major streets and avenues such as Grand Avenue. These well-lit thoroughfares and nodes stand out distinctly from the surrounding areas, showcasing the street pattern clearly. Large stretches of interstate highways between midwestern cities, by contrast, are comparably dim because these highways connect cities but do not have the same density of lighting or concentrated commercial/residential developments lining them as urban street grids do at night. This leads to the interstate appearing as a dimmer corridor rather than a sharply lit grid [source: earth_at_night_508_page_104_verbalized, earth_at_night_508_page_105_verbalized, earth_at_night_508_page_124_verbalized].

References:
- earth_at_night_508_page_174_verbalized
- earth_at_night_508_page_176_verbalized
- earth_at_night_508_page_104_verbalized
- earth_at_night_508_page_105_verbalized
- earth_at_night_508_page_124_verbalized
```

---

## Delete the agent and project connection

### [Python](#tab/python)

```python
# Delete the agent
project_client.agents.delete_version(agent.name, agent.version)
print(f"Agent '{agent.name}' version '{agent.version}' deleted successfully.")

# Delete the project connection (Azure Resource Manager)
import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

credential = DefaultAzureCredential()
project_resource_id = "{project_resource_id}"
project_connection_name = "{project_connection_name}"

bearer_token_provider = get_bearer_token_provider(credential, "https://management.azure.com/.default")
headers = {"Authorization": f"Bearer {bearer_token_provider()}"}

response = requests.delete(
  f"https://management.azure.com{project_resource_id}/connections/{project_connection_name}?api-version=2025-10-01-preview",
  headers=headers,
)
response.raise_for_status()
print(f"Project connection '{project_connection_name}' deleted successfully.")
```

### [REST](#tab/rest)

```HTTP
### Delete the agent
DELETE {project_endpoint}/agents/{agent_name}?api-version=2025-11-15-preview
Authorization: Bearer {foundry_access_token}

### Delete the project connection
DELETE https://management.azure.com/{project_resource_id}/connections/{project_connection_name}?api-version=2025-10-01-preview
Authorization: Bearer {management_access_token}
```

---

> [!NOTE]
> Deleting your agent and project connection doesn't delete your knowledge base or its knowledge sources. You must delete these objects separately on your Azure AI Search service. For more information, see [Delete a knowledge base](/azure/search/agentic-retrieval-how-to-create-knowledge-base?#delete-a-knowledge-base) and [Delete a knowledge source](/azure/search/agentic-knowledge-source-how-to-search-index#delete-a-knowledge-source).

## Troubleshooting

This section helps you troubleshoot common issues when connecting Foundry Agent Service to a Foundry IQ knowledge base.

### Authorization failures (401/403)

- If you get a 403 from Azure AI Search, confirm the project's managed identity has the **Search Index Data Reader** role on the search service (and **Search Index Data Contributor** if you write to indexes).
- If you get a 403 from Azure Resource Manager when you create or delete the project connection, confirm your user or service principal has permissions on the Microsoft Foundry resource and project.
- If you use keyless authentication, confirm your environment is signed in to the correct tenant and subscription.

### MCP endpoint errors (400/404)

- Confirm `search_service_endpoint` is the Azure AI Search service URL, such as `https://<name>.search.windows.net`.
- Confirm `knowledge_base_name` matches the knowledge base you created in Azure AI Search.
- Confirm you use the `2025-11-01-preview` API version for the knowledge base MCP endpoint.

### The agent doesn't ground answers

- Confirm the agent has the MCP tool configured and `allowed_tools` includes `knowledge_base_retrieve`.
- Update your agent instructions to explicitly require using the knowledge base and to return "I don't know" when retrieval doesn't contain the answer.

## Related content

- [Create a knowledge base in Azure AI Search](/azure/search/agentic-retrieval-how-to-create-knowledge-base)
- [Tutorial: Build an end-to-end agentic retrieval solution](/azure/search/agentic-retrieval-how-to-create-pipeline)
- [Foundry IQ: Unlocking ubiquitous knowledge for agents](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-unlocking-ubiquitous-knowledge-for-agents/4470812)
- [Tool best practices](../concepts/tool-best-practice.md)
