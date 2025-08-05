---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 08/05/2025
ms.custom: include
---

### Set up your environment

[!INCLUDE [SDK setup](development-environment-config.md)]

### Authenticating with Microsoft Entra ID

There are various authentication methods for the different connection types. When you use Microsoft Entra ID, in addition to creating the connection you might also need to grant Azure role-based access control permissions before the connection can be used. For more information, visit [Role-based access control](../concepts/rbac-azure-ai-foundry.md#scenario-connections-using-microsoft-entra-id-authentication).

[!INCLUDE [Azure Key Vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]

### Model and service connections

## [Azure OpenAI](#tab/aoai)

The following example uses the [AzureOpenAIConnection](/python/api/azure-ai-ml/azure.ai.ml.entities.azureopenaiconnection) class to create an Azure OpenAI in Azure AI Foundry Models connection.

> [!TIP]
> To connect to Azure OpenAI and more AI services with one connection, you can use the AI services connection instead.

```python
from azure.ai.ml.entities import AzureOpenAIConnection
name = "XXXXXXXXX"

target = "https://XXXXXXXXX.cognitiveservices.azure.com/"

resource_id= "Azure-resource-id"

# Microsoft Entra ID
credentials = None

wps_connection = AzureOpenAIConnection(
    name=name,
    azure_endpoint=target,
    credentials=credentials,
    resource_id = resource_id,
    is_shared=False
)
ml_client.connections.create_or_update(wps_connection)
```

## [AI services](#tab/ai-services)

The following example uses the [AzureAIServicesConnection](/python/api/azure-ai-ml/azure.ai.ml.entities.azureaiservicesconnection) class to create an Azure AI services connection. This example creates one connection for the AI services documented in the [Connect to Azure AI services](../../ai-services/connect-services-ai-foundry-portal.md) article. The same connection also supports Azure OpenAI.

```python
from azure.ai.ml.entities import AzureAIServicesConnection

name = "my-ai-services"

target = "https://my.cognitiveservices.azure.com/"
resource_id=""

# Microsoft Entra ID
credentials = None


wps_connection = AzureAIServicesConnection(
    name=name,
    endpoint=target,
    credentials=credentials,
    ai_services_resource_id=resource_id,
)
ml_client.connections.create_or_update(wps_connection)
```

## [Search](#tab/search)

The following example uses the [AzureAISearchConnection](/python/api/azure-ai-ml/azure.ai.ml.entities.azureaisearchconnection) class to create an Azure AI Search connection:

```python
from azure.ai.ml.entities import AzureAISearchConnection

name = "my_aisearch_demo_connection"
target = "https://my.search.windows.net"

# Microsoft Entra ID
credentials = None


wps_connection = AzureAISearchConnection(
    name=name,
    endpoint=target,
    credentials=credentials,
)
ml_client.connections.create_or_update(wps_connection)
```

## [Content Safety](#tab/content-safety)

The following example creates an Azure AI Content Safety connection:

```python
from azure.ai.ml.entities import AzureContentSafetyConnection, ApiKeyConfiguration

name = "my_content_safety"

target = "https://my.cognitiveservices.azure.com/"
api_key = "XXXXXXXXX"

wps_connection = AzureContentSafetyConnection(
    name=name,
    endpoint=target,
    credentials=ApiKeyConfiguration(key=api_key),
    #api_version="1234"
)
ml_client.connections.create_or_update(wps_connection)
```

## [Serverless model (preview)](#tab/serverless)

The following example creates a serverless endpoint connection:

```python
from azure.ai.ml.entities import ServerlessConnection

name = "my_maas_apk"

endpoint = "https://my.eastus2.inference.ai.azure.com/"
api_key = "XXXXXXXXX"
wps_connection = ServerlessConnection(
    name=name,
    endpoint=endpoint,
    api_key=api_key,

)
ml_client.connections.create_or_update(wps_connection)
```

---

### Data and storage connections

## [Blob Storage](#tab/blob)

The following example uses the [AzureBlobStoreConnection](/python/api/azure-ai-ml/azure.ai.ml.entities.azureblobstoreconnection) class to create an Azure Blob Storage connection. This connection is authenticated with an account key or a SAS token:

```python
from azure.ai.ml.entities import AzureBlobStoreConnection, SasTokenConfiguration,AccountKeyConfiguration


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

## [ADL Gen 2](#tab/adl2)

The following example creates Azure Data Lake Storage Gen 2 connection. This connection is authenticated with a Service Principal:

```python
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import ServicePrincipalConfiguration

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
    credentials=sp_config
    
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

## [Microsoft OneLake](#tab/onelake)

The following example uses the [MicrosoftOneLakeWorkspaceConnection](/python/api/azure-ai-ml/azure.ai.ml.entities.microsoftonelakeconnection) class to create a Microsoft OneLake connection. This connection is authenticated with a Service Principal:

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

---

### Other connections

## [Serp](#tab/serp)

The following example uses the [SerpConnection](/python/api/azure-ai-ml/azure.ai.ml.entities.serpconnection) class:

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

## [OpenAI](#tab/openai)

The following example uses the [OpenAIConnection](/python/api/azure-ai-ml/azure.ai.ml.entities.openaiconnection) class to create an OpenAI (not Azure OpenAI) connection:

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

## [Custom](#tab/custom)

The following example uses the [ApiKeyConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.apikeyconnection) class to create custom connection:

```python
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import ApiKeyConfiguration


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
---

### List connections

To list all connections, use the following example:

```python
from azure.ai.ml.entities import Connection, AzureOpenAIConnection, ApiKeyConfiguration
connection_list = ml_client.connections.list()
for conn in connection_list:
  print(conn)
```

### Delete connections

To delete a connection, use the following example:

```python
name = "my-connection"

ml_client.connections.delete(name)
```