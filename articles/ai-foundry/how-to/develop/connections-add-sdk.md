---
title: How to add a new connection in Azure AI Foundry portal using the Azure Machine Learning SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to add connections to other resources using the Azure Machine Learning SDK.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 03/17/2025
ms.reviewer: dantaylo
ms.author: larryfr
author: Blackmist
---

# Add a new connection using the Azure Machine Learning SDK

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you learn how to add a new connection to [Azure AI Foundry](https://ai.azure.com) using the Azure Machine Learning SDK.

Connections are a way to authenticate and consume both Microsoft and other resources within your Azure AI Foundry projects. For example, connections can be used for prompt flow, training data, and deployments. [Connections can be created](../../how-to/connections-add.md) exclusively for one project or shared with all projects in the same Azure AI Foundry hub. For more information, see [How to add a new connection in Azure AI Foundry portal](../connections-add.md).

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure AI Foundry](https://azure.microsoft.com/free/) today.
- An Azure AI Foundry hub. For information on creating a hub, see [Create Azure AI Foundry resources with the SDK](./create-hub-project-sdk.md).
- A resource to create a connection to. For example, an AI Services resource. The examples in this article use placeholders that you must replace with your own values when running the code.

## Set up your environment

[!INCLUDE [SDK setup](../../includes/development-environment-config.md)]

## Authenticating with Microsoft Entra ID

There are various authentication methods for the different connection types. When you use Microsoft Entra ID, in addition to creating the connection you might also need to grant Azure role-based access control permissions before the connection can be used. For more information, visit [Role-based access control](../../concepts/rbac-azure-ai-foundry.md#scenario-connections-using-microsoft-entra-id-authentication).

[!INCLUDE [Azure Key Vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]

## Azure OpenAI in Foundry Models

The following example creates an Azure OpenAI in Azure AI Foundry Models connection.

> [!TIP]
> To connect to Azure OpenAI and more AI services with one connection, you can use the [AI services connection](#azure-ai-services) instead.

```python
from azure.ai.ml.entities import AzureOpenAIConnection, ApiKeyConfiguration
from azure.ai.ml.entities import UsernamePasswordConfiguration

name = "XXXXXXXXX"

target = "https://XXXXXXXXX.cognitiveservices.azure.com/"

resource_id= "Azure-resource-id"

# Microsoft Entra ID
credentials = None
# Uncomment the following if you need to use API key instead
# api_key= "my-key"
# credentials = ApiKeyConfiguration(key=api_key)

wps_connection = AzureOpenAIConnection(
    name=name,
    azure_endpoint=target,
    credentials=credentials,
    resource_id = resource_id,
    is_shared=False
)
ml_client.connections.create_or_update(wps_connection)
```

## Azure AI services

The following example creates an Azure AI services connection. This example creates one connection for the AI services documented in the [Connect to Azure AI services](../../../ai-services/connect-services-ai-foundry-portal.md) article. The same connection also supports Azure OpenAI.

```python
from azure.ai.ml.entities import AzureAIServicesConnection, ApiKeyConfiguration
from azure.ai.ml.entities import UsernamePasswordConfiguration

name = "my-ai-services"

target = "https://XXXXXXXXX.cognitiveservices.azure.com/"
resource_id=""

# Microsoft Entra ID
credentials = None
# Uncomment the following if you need to use API key instead
# api_key= "my-key"
# credentials = ApiKeyConfiguration(key=api_key)

wps_connection = AzureAIServicesConnection(
    name=name,
    endpoint=target,
    credentials=credentials,
    ai_services_resource_id=resource_id,
)
ml_client.connections.create_or_update(wps_connection)
```

## Azure AI Search

The following example creates an Azure AI Search connection:

```python
from azure.ai.ml.entities import AzureAISearchConnection, ApiKeyConfiguration
from azure.ai.ml.entities import UsernamePasswordConfiguration

name = "my_aisearch_demo_connection"
target = "https://XXXXXXXXX.search.windows.net"

# Microsoft Entra ID
credentials = None
# Uncomment the following if you need to use API key instead
# api_key= "my-key"
# credentials = ApiKeyConfiguration(key=api_key)

wps_connection = AzureAISearchConnection(
    name=name,
    endpoint=target,
    credentials=credentials,
)
ml_client.connections.create_or_update(wps_connection)
```

## Azure AI Content Safety

The following example creates an Azure AI Content Safety connection:

```python
from azure.ai.ml.entities import AzureContentSafetyConnection, ApiKeyConfiguration
from azure.ai.ml.entities import UsernamePasswordConfiguration

name = "my_content_safety"

target = "https://XXXXXXXXX.cognitiveservices.azure.com/"
api_key = "XXXXXXXXX"

wps_connection = AzureContentSafetyConnection(
    name=name,
    endpoint=target,
    credentials=ApiKeyConfiguration(key=api_key),
    #api_version="1234"
)
ml_client.connections.create_or_update(wps_connection)
```

## Serverless model (preview)

The following example creates a serverless endpoint connection:

```python
from azure.ai.ml.entities import ServerlessConnection

name = "my_maas_apk"

endpoint = "https://XXXXXXXXX.eastus2.inference.ai.azure.com/"
api_key = "XXXXXXXXX"
wps_connection = ServerlessConnection(
    name=name,
    endpoint=endpoint,
    api_key=api_key,

)
ml_client.connections.create_or_update(wps_connection)
```

## Azure Blob Storage

The following example creates an Azure Blob Storage connection. This connection is authenticated with an account key or a SAS token:

```python
from azure.ai.ml.entities import AzureBlobStoreConnection, SasTokenConfiguration,AccountKeyConfiguration
from azure.ai.ml.entities import UsernamePasswordConfiguration


name = "my_blobstore"
url = "https://XXXXXXXXX.blob.core.windows.net/mycontainer/"

wps_connection = AzureBlobStoreConnection(
    name=name,
    container_name="XXXXXXXXX",
    account_name="XXXXXXXXX",
    url=url,
    #credentials=None
    credentials=SasTokenConfiguration(sas_token="XXXXXXXXX")
    #credentials=AccountKeyConfiguration(account_key="XXXXXXXXX")
)
ml_client.connections.create_or_update(wps_connection)
```

## Azure Data Lake Storage Gen 2

The following example creates Azure Data Lake Storage Gen 2 connection. This connection is authenticated with a Service Principal:

```python
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration, ServicePrincipalConfiguration

sp_config = ServicePrincipalConfiguration(
    tenant_id="XXXXXXXXXXXX",
    client_id="XXXXXXXXXXXXX",
    client_secret="XXXXXXXXXXXXXXXk" # your-client-secret
    
)
name = "myadlsgen2"

target = "https://ambadaladlsgen2.core.windows.net/dummycont"

wps_connection = WorkspaceConnection(
    name=name,
    type="azure_data_lake_gen2",
    target=target,
    credentials=None
    
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

## Microsoft OneLake

The following example creates a Microsoft OneLake connection. This connection is authenticated with a Service Principal:

```python
from azure.ai.ml.entities import MicrosoftOneLakeWorkspaceConnection, OneLakeArtifact
from azure.ai.ml.entities import ServicePrincipalConfiguration

sp_config = ServicePrincipalConfiguration(
    tenant_id="XXXXXXXXXXX",
    client_id="XXXXXXXXXXXXXXXXXX",
    client_secret="XXXXXXXXXXXXXXXX" # your-client-secret
)
name = "my_onelake_sp"

artifact = OneLakeArtifact(
    name="XXXXXXXXX",
    type="lake_house"
   
)

wps_connection = MicrosoftOneLakeWorkspaceConnection(
    name=name,
    artifact=artifact,
    one_lake_workspace_name="XXXXXXXXXXXXXXXXX",
    endpoint="XXXXXXXXX.dfs.fabric.microsoft.com"
    credentials=sp_config
    
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

## Serp

The following example creates a Serp connection:

```python
from azure.ai.ml.entities import SerpConnection

name = "my_serp_apk"
api_key = "XXXXXXXXX"

wps_connection = SerpConnection(
    name=name,
    api_key=api_key,
)
ml_client.connections.create_or_update(wps_connection)
```

## OpenAI

The following example creates an OpenAI (not Azure OpenAI) connection:

```python
from azure.ai.ml.entities import OpenAIConnection

name = "my_oai_apk"
api_key = "XXXXXXXX"

wps_connection = OpenAIConnection(
    name=name,
    api_key=api_key,
)
ml_client.connections.create_or_update(wps_connection)
```

## Custom

The following example creates custom connection:

```python
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration, ApiKeyConfiguration


name = "my_custom"

target = "https://XXXXXXXXX.core.windows.net/mycontainer"

wps_connection = WorkspaceConnection(
    name=name,
    type="custom",
    target=target,
    credentials=ApiKeyConfiguration(key="XXXXXXXXX"),    
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

## List connections

To list all connections, use the following example:

```python
from azure.ai.ml.entities import Connection, AzureOpenAIConnection, ApiKeyConfiguration
connection_list = ml_client.connections.list()
for conn in connection_list:
  print(conn)
```

## Delete connections

To delete a connection, use the following example:

```python
name = "my-connection"

ml_client.connections.delete(name)
```

## Related content

- [Get started building a chat app using the prompt flow SDK](../../quickstarts/get-started-code.md)
- [Work with projects in VS Code](vscode.md)

