---
title: Use datastores
titleSuffix: Azure Machine Learning
description: Learn how to use datastores to connect to Azure storage services during training with Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.author: scottpolly
author: s-polly
ms.reviewer: soumyapatro
ms.date: 01/26/2026
ms.custom: data4ml, ignite-2023, devx-track-azurecli, dev-focus
ai-usage: ai-assisted
# Customer intent: As an experienced Python developer, I need to make my data in Azure storage available to my remote compute resource to train my machine learning models.
---

# Create datastores

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, you learn how to connect to Azure data storage services by using Azure Machine Learning datastores.

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- The [Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install).
- A Machine Learning workspace.
- The required permissions to create datastores in your workspace and access your storage account (for example, workspace **Contributor** and storage **Storage Blob Data Contributor**). 
    - Workspace roles: [Access control in Azure Machine Learning](/azure/machine-learning/how-to-assign-roles?view=azureml-api-2)
    - Storage roles: [Authorize access to blob data with Microsoft Entra ID](/azure/storage/blobs/authorize-access-azure-active-directory?tabs=azure-portal)

> [!NOTE]
> Machine Learning datastores don't create the underlying storage account resources. Instead, they link an *existing* storage account for Machine Learning use. You don't need Machine Learning datastores. If you have access to the underlying data, you can use storage URIs directly.

## Verify access (Python)

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

for datastore in ml_client.datastores.list():
    print(datastore.name)
```

Lists the datastores in your workspace to confirm authentication and access.

Reference: [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python), [`DatastoreOperations.list`](/python/api/azure-ai-ml/azure.ai.ml.operations.datastoreoperations?view=azure-python#list)

## Create an Azure Blob datastore

# [Python SDK: Identity-based access](#tab/sdk-identity-based-access)

```python
from azure.ai.ml.entities import AzureBlobDatastore
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = AzureBlobDatastore(
    name="",
    description="",
    account_name="",
    container_name=""
)

ml_client.create_or_update(store)
```

Creates or updates a datastore that points to the specified blob container by using identity-based access.

Reference: [`AzureBlobDatastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.azureblobdatastore?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [Python SDK: Account key](#tab/sdk-account-key)

```python
from azure.ai.ml.entities import AzureBlobDatastore
from azure.ai.ml.entities import AccountKeyConfiguration
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = AzureBlobDatastore(
    name="blob_protocol_example",
    description="Datastore pointing to a blob container using HTTPS.",
    account_name="mytestblobstore",
    container_name="data-container",
    protocol="https",
    credentials=AccountKeyConfiguration(
        account_key="aaaaaaaa-0b0b-1c1c-2d2d-333333333333"
    ),
)

ml_client.create_or_update(store)
```

Creates or updates a datastore that points to the specified blob container by using an account key.

Reference: [`AzureBlobDatastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.azureblobdatastore?view=azure-python), [`AccountKeyConfiguration`](/python/api/azure-ai-ml/azure.ai.ml.entities.accountkeyconfiguration?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [Python SDK: SAS](#tab/sdk-SAS)

```python
from azure.ai.ml.entities import AzureBlobDatastore
from azure.ai.ml.entities import SasTokenConfiguration
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = AzureBlobDatastore(
    name="blob_sas_example",
    description="Datastore pointing to a blob container using a SAS token.",
    account_name="mytestblobstore",
    container_name="data-container",
    credentials=SasTokenConfiguration(
        sas_token= "?xx=A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u&xx=C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1wx&xx=Ff6Gg~7Hh8.-Ii9Jj0Kk1Ll2Mm3Nn4_Oo5Pp6Qq7&xx=N7oP8qR9sT0uV1wX2yZ3aB4cD5eF6g&xxx=Ee5Ff~6Gg7.-Hh8Ii9Jj0Kk1Ll2Mm3_Nn4Oo5Pp6&xxx=C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1w"
    ),
)

ml_client.create_or_update(store)
```

Creates or updates a datastore that points to the specified blob container by using a SAS token.

Reference: [`AzureBlobDatastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.azureblobdatastore?view=azure-python), [`SasTokenConfiguration`](/python/api/azure-ai-ml/azure.ai.ml.entities.sastokenconfiguration?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [CLI: Identity-based access](#tab/cli-identity-based-access)
Create the following YAML file (update the appropriate values):

```yaml
# my_blob_datastore.yml
$schema: https://azuremlschemas.azureedge.net/latest/azureBlob.schema.json
name: my_blob_ds # add your datastore name here
type: azure_blob
description: here is a description # add a datastore description here
account_name: my_account_name # add the storage account name here
container_name: my_container_name # add the storage container name here
```

Defines the blob datastore configuration in a YAML file. Provide the datastore name, storage account name, and container name.

Reference: [azureBlob.schema.json](https://azuremlschemas.azureedge.net/latest/azureBlob.schema.json)

Create the Machine Learning datastore in the Azure CLI:

```azurecli
az ml datastore create --file my_blob_datastore.yml
```

Creates or updates the blob datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)

# [CLI: Account key](#tab/cli-account-key)
Create this YAML file (update the appropriate values):

```yaml
# my_blob_datastore.yml
$schema: https://azuremlschemas.azureedge.net/latest/azureBlob.schema.json
name: blob_example
type: azure_blob
description: Datastore pointing to a blob container.
account_name: mytestblobstore
container_name: data-container
credentials:
  account_key: aaaaaaaa-0b0b-1c1c-2d2d-333333333333
```

Defines the blob datastore configuration that uses an account key for access.

Reference: [azureBlob.schema.json](https://azuremlschemas.azureedge.net/latest/azureBlob.schema.json)

Create the Machine Learning datastore in the CLI:

```azurecli
az ml datastore create --file my_blob_datastore.yml
```

Creates or updates the blob datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)

# [CLI: SAS](#tab/cli-sas)
Create this YAML file (update the appropriate values):

```yaml
# my_blob_datastore.yml
$schema: https://azuremlschemas.azureedge.net/latest/azureBlob.schema.json
name: blob_sas_example
type: azure_blob
description: Datastore pointing to a blob container using a SAS token.
account_name: mytestblobstore
container_name: data-container
credentials:
  sas_token: "?xx=A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u&xx=C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1wx&xx=Ff6Gg~7Hh8.-Ii9Jj0Kk1Ll2Mm3Nn4_Oo5Pp6Qq7&xx=N7oP8qR9sT0uV1wX2yZ3aB4cD5eF6g&xxx=Ee5Ff~6Gg7.-Hh8Ii9Jj0Kk1Ll2Mm3_Nn4Oo5Pp6&xxx=C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1w"
```

Defines the blob datastore configuration that uses a SAS token for access.

Reference: [azureBlob.schema.json](https://azuremlschemas.azureedge.net/latest/azureBlob.schema.json)

Create the Machine Learning datastore in the CLI:

```azurecli
az ml datastore create --file my_blob_datastore.yml
```

Creates or updates the blob datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)
---

## Create an Azure Data Lake Storage Gen2 datastore

# [Python SDK: Identity-based access](#tab/sdk-adls-identity-access)

```python
from azure.ai.ml.entities import AzureDataLakeGen2Datastore
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = AzureDataLakeGen2Datastore(
    name="",
    description="",
    account_name="",
    filesystem=""
)

ml_client.create_or_update(store)
```

Creates or updates a datastore that points to the specified ADLS Gen2 filesystem by using identity-based access.

Reference: [`AzureDataLakeGen2Datastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.azuredatalakegen2datastore?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [Python SDK: Service principal](#tab/sdk-adls-sp)

```python
from azure.ai.ml.entities import AzureDataLakeGen2Datastore
from azure.ai.ml.entities._datastore.credentials import ServicePrincipalCredentials

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = AzureDataLakeGen2Datastore(
    name="adls_gen2_example",
    description="Datastore pointing to an Azure Data Lake Storage Gen2 instance.",
    account_name="mytestdatalakegen2",
    filesystem="my-gen2-container",
     credentials=ServicePrincipalCredentials(
        tenant_id= "bbbbcccc-1111-dddd-2222-eeee3333ffff",
        client_id= "44445555-eeee-6666-ffff-7777aaaa8888",
        client_secret= "Cc3Dd~4Ee5.-Ff6Gg7Hh8Ii9Jj0Kk1_Ll2Mm3Nn4",
    ),
)

ml_client.create_or_update(store)
```

Creates or updates a datastore that points to the specified ADLS Gen2 filesystem by using a service principal.

Reference: [`AzureDataLakeGen2Datastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.azuredatalakegen2datastore?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [CLI: Identity-based access](#tab/cli-adls-identity-based-access)
Create this YAML file (update the values):

```yaml
# my_adls_datastore.yml
$schema: https://azuremlschemas.azureedge.net/latest/azureDataLakeGen2.schema.json
name: adls_gen2_credless_example
type: azure_data_lake_gen2
description: Datastore pointing to an Azure Data Lake Storage Gen2 instance.
account_name: mytestdatalakegen2
filesystem: my-gen2-container
```

Defines the ADLS Gen2 datastore configuration in a YAML file. Provide the datastore name, storage account name, and filesystem.

Reference: [azureDataLakeGen2.schema.json](https://azuremlschemas.azureedge.net/latest/azureDataLakeGen2.schema.json)

Create the Machine Learning datastore in the CLI:

```azurecli
az ml datastore create --file my_adls_datastore.yml
```

Creates or updates the ADLS Gen2 datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)

# [CLI: Service principal](#tab/cli-adls-sp)
Create this YAML file (update the values):

```yaml
# my_adls_datastore.yml
$schema: https://azuremlschemas.azureedge.net/latest/azureDataLakeGen2.schema.json
name: adls_gen2_example
type: azure_data_lake_gen2
description: Datastore pointing to an Azure Data Lake Storage Gen2 instance.
account_name: mytestdatalakegen2
filesystem: my-gen2-container
credentials:
  tenant_id: bbbbcccc-1111-dddd-2222-eeee3333ffff
  client_id: 44445555-eeee-6666-ffff-7777aaaa8888
  client_secret: Cc3Dd~4Ee5.-Ff6Gg7Hh8Ii9Jj0Kk1_Ll2Mm3Nn4
```

Defines the ADLS Gen2 datastore configuration that uses a service principal for access.

Reference: [azureDataLakeGen2.schema.json](https://azuremlschemas.azureedge.net/latest/azureDataLakeGen2.schema.json)

Create the Machine Learning datastore in the CLI:

```azurecli
az ml datastore create --file my_adls_datastore.yml
```

Creates or updates the ADLS Gen2 datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)
---

## Create an Azure Files datastore

# [Python SDK: Account key](#tab/sdk-azfiles-accountkey)

```python
from azure.ai.ml.entities import AzureFileDatastore
from azure.ai.ml.entities import AccountKeyConfiguration
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = AzureFileDatastore(
    name="file_example",
    description="Datastore pointing to an Azure File Share.",
    account_name="mytestfilestore",
    file_share_name="my-share",
    credentials=AccountKeyConfiguration(
        account_key= "aaaaaaaa-0b0b-1c1c-2d2d-333333333333"
    ),
)

ml_client.create_or_update(store)
```

Creates or updates a datastore that points to the specified Azure Files share by using an account key.

Reference: [`AzureFileDatastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.azurefiledatastore?view=azure-python), [`AccountKeyConfiguration`](/python/api/azure-ai-ml/azure.ai.ml.entities.accountkeyconfiguration?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [Python SDK: SAS](#tab/sdk-azfiles-sas)

```python
from azure.ai.ml.entities import AzureFileDatastore
from azure.ai.ml.entities import SasTokenConfiguration
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = AzureFileDatastore(
    name="file_sas_example",
    description="Datastore pointing to an Azure File Share using a SAS token.",
    account_name="mytestfilestore",
    file_share_name="my-share",
    credentials=SasTokenConfiguration(
        sas_token="?xx=A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u&xx=C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1wx&xx=Ff6Gg~7Hh8.-Ii9Jj0Kk1Ll2Mm3Nn4_Oo5Pp6Qq7&xx=N7oP8qR9sT0uV1wX2yZ3aB4cD5eF6g&xxx=Ee5Ff~6Gg7.-Hh8Ii9Jj0Kk1Ll2Mm3_Nn4Oo5Pp6&xxx=C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1w"
    ),
)

ml_client.create_or_update(store)
```

Creates or updates a datastore that points to the specified Azure Files share by using a SAS token.

Reference: [`AzureFileDatastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.azurefiledatastore?view=azure-python), [`SasTokenConfiguration`](/python/api/azure-ai-ml/azure.ai.ml.entities.sastokenconfiguration?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [CLI: Account key](#tab/cli-azfiles-account-key)
Create this YAML file (update the values):

```yaml
# my_files_datastore.yml
$schema: https://azuremlschemas.azureedge.net/latest/azureFile.schema.json
name: file_example
type: azure_file
description: Datastore pointing to an Azure File Share.
account_name: mytestfilestore
file_share_name: my-share
credentials:
  account_key: aaaaaaaa-0b0b-1c1c-2d2d-333333333333
```

Defines the Azure Files datastore configuration that uses an account key for access.

Reference: [azureFile.schema.json](https://azuremlschemas.azureedge.net/latest/azureFile.schema.json)

Create the Machine Learning datastore in the CLI:

```azurecli
az ml datastore create --file my_files_datastore.yml
```

Creates or updates the Azure Files datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)

# [CLI: SAS](#tab/cli-azfiles-sas)
Create this YAML file (update the values):

```yaml
# my_files_datastore.yml
$schema: https://azuremlschemas.azureedge.net/latest/azureFile.schema.json
name: file_sas_example
type: azure_file
description: Datastore pointing to an Azure File Share using a SAS token.
account_name: mytestfilestore
file_share_name: my-share
credentials:
  sas_token: "?xx=A1bC2dE3fH4iJ5kL6mN7oP8qR9sT0u&xx=C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1wx&xx=Ff6Gg~7Hh8.-Ii9Jj0Kk1Ll2Mm3Nn4_Oo5Pp6Qq7&xx=N7oP8qR9sT0uV1wX2yZ3aB4cD5eF6g&xxx=Ee5Ff~6Gg7.-Hh8Ii9Jj0Kk1Ll2Mm3_Nn4Oo5Pp6&xxx=C2dE3fH4iJ5kL6mN7oP8qR9sT0uV1w"
```

Defines the Azure Files datastore configuration that uses a SAS token for access.

Reference: [azureFile.schema.json](https://azuremlschemas.azureedge.net/latest/azureFile.schema.json)

Create the Machine Learning datastore in the CLI:

```azurecli
az ml datastore create --file my_files_datastore.yml
```

Creates or updates the Azure Files datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)
---

## Create a OneLake (Microsoft Fabric) datastore (preview)

This section describes various options to create a OneLake datastore. The OneLake datastore is part of Microsoft Fabric. Currently, Machine Learning supports connection to Microsoft Fabric lakehouse artifacts in the **Files** folder that include folders or files and Amazon S3 shortcuts. For more information about lakehouses, see [What is a lakehouse in Microsoft Fabric?](/fabric/data-engineering/lakehouse-overview).

Creating a OneLake datastore requires the following information from your Microsoft Fabric instance:

- Endpoint
- Workspace GUID
- Artifact GUID

 The following screenshots show how to retrieve these required information resources from your Microsoft Fabric instance.

:::image type="content" source="media/how-to-datastore/onelake-properties.png" alt-text="Screenshot that shows how to click into artifact properties of Microsoft Fabric workspace artifact in Microsoft Fabric UI." lightbox="./media/how-to-datastore/onelake-properties.png":::

You find **Endpoint**, **Workspace GUID**, and **Artifact GUID** in the **URL** and **ABFS path** from the **Properties** page:

- **URL format**: `https://{your_one_lake_endpoint}/{your_one_lake_workspace_guid}/{your_one_lake_artifact_guid}/Files`
- **ABFS path format**: `abfss://{your_one_lake_workspace_guid}@{your_one_lake_endpoint}/{your_one_lake_artifact_guid}/Files`

:::image type="content" source="media/how-to-datastore/onelake-url-abfs-path.png" alt-text="Screenshot that shows URL and ABFS path of a OneLake artifact in Microsoft Fabric UI." lightbox="./media/how-to-datastore/onelake-url-abfs-path.png":::

## Create a OneLake datastore

# [Python SDK: Identity-based access](#tab/sdk-onelake-identity-access)

```python
from azure.ai.ml.entities import OneLakeDatastore, OneLakeArtifact
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = OneLakeDatastore(
    name="onelake_example_id",
    description="Datastore pointing to a Microsoft Fabric artifact.",
    one_lake_workspace_name="bbbbbbbb-7777-8888-9999-cccccccccccc", #{your_one_lake_workspace_guid}
    endpoint="msit-onelake.dfs.fabric.microsoft.com", #{your_one_lake_endpoint}
    artifact=OneLakeArtifact(
        name="cccccccc-8888-9999-0000-dddddddddddd/Files", #{your_one_lake_artifact_guid}/Files
        type="lake_house"
    ),
)

ml_client.create_or_update(store)
```

Creates or updates a OneLake datastore that points to the specified lakehouse by using identity-based access.

Reference: [`OneLakeDatastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.onelakedatastore?view=azure-python), [`OneLakeArtifact`](/python/api/azure-ai-ml/azure.ai.ml.entities.onelakeartifact?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [Python SDK: Service principal](#tab/sdk-onelake-sp)

```python
from azure.ai.ml.entities import OneLakeDatastore, OneLakeArtifact
from azure.ai.ml.entities._datastore.credentials import ServicePrincipalCredentials
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

store = OneLakeDatastore(
    name="onelake_example_sp",
    description="Datastore pointing to a Microsoft Fabric artifact.",
    one_lake_workspace_name="bbbbbbbb-7777-8888-9999-cccccccccccc", #{your_one_lake_workspace_guid}
    endpoint="msit-onelake.dfs.fabric.microsoft.com", #{your_one_lake_endpoint}
    artifact=OneLakeArtifact(
        name="cccccccc-8888-9999-0000-dddddddddddd/Files", #{your_one_lake_artifact_guid}/Files
        type="lake_house"
    ),
    credentials=ServicePrincipalCredentials(
        tenant_id= "bbbbcccc-1111-dddd-2222-eeee3333ffff",
        client_id= "44445555-eeee-6666-ffff-7777aaaa8888",
        client_secret= "Cc3Dd~4Ee5.-Ff6Gg7Hh8Ii9Jj0Kk1_Ll2Mm3Nn4",
    ),
)

ml_client.create_or_update(store)
```

Creates or updates a OneLake datastore that points to the specified lakehouse by using a service principal.

Reference: [`OneLakeDatastore`](/python/api/azure-ai-ml/azure.ai.ml.entities.onelakedatastore?view=azure-python), [`OneLakeArtifact`](/python/api/azure-ai-ml/azure.ai.ml.entities.onelakeartifact?view=azure-python), [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

# [CLI: Identity-based access](#tab/cli-onelake-identity-based-access)
Create the following YAML file. Update the values:

```yaml
# my_onelake_datastore.yml
$schema: http://azureml/sdk-2-0/OneLakeDatastore.json
name: onelake_example_id
type: one_lake
description: Datastore pointing to a OneLake lakehouse.
one_lake_workspace_name: "eeeeffff-4444-aaaa-5555-bbbb6666cccc"
endpoint: "msit-onelake.dfs.fabric.microsoft.com"
artifact:
  type: lake_house
  name: "1111bbbb-22cc-dddd-ee33-ffffff444444/Files"
```

Defines the OneLake datastore configuration in a YAML file. Provide the workspace, endpoint, and artifact values.

Reference: [OneLakeDatastore.json](http://azureml/sdk-2-0/OneLakeDatastore.json)

Create the Machine Learning datastore in the CLI:

```azurecli
az ml datastore create --file my_onelake_datastore.yml
```

Creates or updates the OneLake datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)

# [CLI: Service principal](#tab/cli-onelake-sp)
Create the following YAML file. Update the values:

```yaml
# my_onelakesp_datastore.yml
$schema: http://azureml/sdk-2-0/OneLakeDatastore.json
name: onelake_example_id
type: one_lake
description: Datastore pointing to a OneLake lakehouse.
one_lake_workspace_name: "eeeeffff-4444-aaaa-5555-bbbb6666cccc"
endpoint: "msit-onelake.dfs.fabric.microsoft.com"
artifact:
  type: lake_house
  name: "1111bbbb-22cc-dddd-ee33-ffffff444444/Files"
credentials:
  tenant_id: bbbbcccc-1111-dddd-2222-eeee3333ffff
  client_id: 44445555-eeee-6666-ffff-7777aaaa8888
  client_secret: Cc3Dd~4Ee5.-Ff6Gg7Hh8Ii9Jj0Kk1_Ll2Mm3Nn4
```

Defines the OneLake datastore configuration that uses a service principal for access.

Reference: [OneLakeDatastore.json](http://azureml/sdk-2-0/OneLakeDatastore.json)

Create the Machine Learning datastore in the CLI:

```azurecli
az ml datastore create --file my_onelakesp_datastore.yml
```

Creates or updates the OneLake datastore in your workspace by using the YAML file.

Reference: [`az ml datastore create`](/cli/azure/ml/datastore?view=azure-cli-latest)
---

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| 403 or AuthorizationFailed when creating a datastore | Missing role assignment for the workspace or storage account | Verify you have the required workspace and storage roles, then retry the command. |
| Authentication failed for `DefaultAzureCredential` | No valid credential source found | Run `az login`, or configure environment variables for a service principal. |
| Storage access denied when using identity-based access | Storage account lacks data-plane permissions for your identity | Assign the correct storage data role to your identity, then retry. |

## Next steps

- [Access data in a job](how-to-read-write-data-v2.md#access-data-in-a-job)
- [Create and manage data assets](how-to-create-data-assets.md#create-and-manage-data-assets)
- [Import data assets (preview)](how-to-import-data-assets.md#import-data-assets-preview)
- [Data administration](how-to-administrate-data-authentication.md#data-administration)
