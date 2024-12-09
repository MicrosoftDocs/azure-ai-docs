--- 
title: Interactive data wrangling with Apache Spark in Azure Machine Learning
titleSuffix: Azure Machine Learning
description: Learn how to use Apache Spark to wrangle data with Azure Machine Learning
author: fbsolo-ms1
ms.author: franksolomon
ms.reviewer: yogipandey
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.date: 09/26/2024
ms.custom: template-how-to
---

# Interactive Data Wrangling with Apache Spark in Azure Machine Learning

Data wrangling becomes one of the most important aspects of machine learning projects. The integration of Azure Machine Learning integration with Azure Synapse Analytics provides access to an Apache Spark pool - backed by Azure Synapse - for interactive data wrangling that uses Azure Machine Learning Notebooks.

In this article, you learn how to handle data wrangling using

- Serverless Spark compute
- Attached Synapse Spark pool

## Prerequisites
- An Azure subscription; if you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free) before you begin.
- An Azure Machine Learning workspace. Visit [Create workspace resources](./quickstart-create-resources.md) for more information.
- An Azure Data Lake Storage (ADLS) Gen 2 storage account. Visit [Create an Azure Data Lake Storage (ADLS) Gen 2 storage account](/azure/storage/blobs/create-data-lake-storage-account) for more information.
- (Optional): An Azure Key Vault. Visit [Create an Azure Key Vault](/azure/key-vault/general/quick-create-portal) for more information.
- (Optional): A Service Principal. Visit [Create a Service Principal](/azure/active-directory/develop/howto-create-service-principal-portal) for more information.
- (Optional): [An attached Synapse Spark pool in the Azure Machine Learning workspace](./how-to-manage-synapse-spark-pool.md).

Before you start your data wrangling tasks, learn about the process of storing secrets

- Azure Blob storage account access key
- Shared Access Signature (SAS) token
- Azure Data Lake Storage (ADLS) Gen 2 service principal information

in the Azure Key Vault. You also need to know how to handle role assignments in the Azure storage accounts. The following sections in this document describe these concepts. Then, we explore the details of interactive data wrangling, using the Spark pools in Azure Machine Learning Notebooks.

> [!TIP]
> To learn about Azure storage account role assignment configuration, or if you access data in your storage accounts using user identity passthrough, visit [Add role assignments in Azure storage accounts](./apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) for more information.

## Interactive Data Wrangling with Apache Spark

For interactive data wrangling with Apache Spark in Azure Machine Learning Notebooks, Azure Machine Learning offers serverless Spark compute and [attached Synapse Spark pool](./how-to-manage-synapse-spark-pool.md). The serverless Spark compute doesn't require creation of resources in the Azure Synapse workspace. Instead, a fully managed serverless Spark compute becomes directly available in the Azure Machine Learning Notebooks. Use of a serverless Spark compute is the easiest way to access a Spark cluster in Azure Machine Learning.

### Serverless Spark compute in Azure Machine Learning Notebooks

A serverless Spark compute is available in Azure Machine Learning Notebooks by default. To access it in a notebook, select **Serverless Spark Compute** under **Azure Machine Learning Serverless Spark** from the **Compute** selection menu.

The Notebooks UI also provides options for Spark session configuration for the serverless Spark compute. To configure a Spark session:

1. Select **Configure session** at the top of the screen.
1. Select **Apache Spark version** from the dropdown menu.
    > [!IMPORTANT]
    > Azure Synapse Runtime for Apache Spark: Announcements
    > * Azure Synapse Runtime for Apache Spark 3.2:
    >   * EOLA Announcement Date: July 8, 2023
    >   * End of Support Date: July 8, 2024. After this date, the runtime will be disabled.
    > * Apache Spark 3.3:
    >   * EOLA Announcement Date: July 12, 2024
    >   * End of Support Date: March 31, 2025. After this date, the runtime will be disabled.
    > * For continued support and optimal performance, we advise migration to **Apache Spark 3.4**
1. Select **Instance type** from the dropdown menu. These types are currently supported:
    - `Standard_E4s_v3`
    - `Standard_E8s_v3`
    - `Standard_E16s_v3`
    - `Standard_E32s_v3`
    - `Standard_E64s_v3`
1. Input a Spark **Session timeout** value, in minutes.
1. Select whether or not you want to **Dynamically allocate executors**
1. Select the number of **Executors** for the Spark session.
1. Select **Executor size** from the dropdown menu.
1. Select **Driver size** from the dropdown menu.
1. To use a Conda file to configure a Spark session, check the **Upload conda file** checkbox. Then, select **Browse**, and choose the Conda file with the Spark session configuration you want.
1. Add **Configuration settings** properties, input values in the **Property** and **Value** textboxes, and select **Add**.
1. Select **Apply**.
1. In the **Configure new session?** pop-up, select **Stop session**.

The session configuration changes persist and become available to another notebook session that is started using the serverless Spark compute.

> [!TIP]
>
> If you use session-level Conda packages, you can [improve](./apache-spark-azure-ml-concepts.md#improving-session-cold-start-time-while-using-session-level-conda-packages) the Spark session *cold start* time if you set the configuration variable `spark.hadoop.aml.enable_cache` to **true**. A session cold start with session level Conda packages typically takes 10 to 15 minutes when the session starts for the first time. However, subsequent session cold starts with the configuration variable set to true typically take three to five minutes.

### Import and wrangle data from Azure Data Lake Storage (ADLS) Gen 2

You can access and wrangle data stored in Azure Data Lake Storage (ADLS) Gen 2 storage accounts with `abfss://` data URIs. To do this, you must follow one of the two data access mechanisms:

- User identity passthrough
- Service principal-based data access

> [!TIP]
> Data wrangling with a serverless Spark compute, and user identity passthrough to access data in an Azure Data Lake Storage (ADLS) Gen 2 storage account, requires the smallest number of configuration steps.

To start interactive data wrangling with the user identity passthrough:

- Verify that the user identity has **Contributor** and **Storage Blob Data Contributor** [role assignments](./apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Data Lake Storage (ADLS) Gen 2 storage account.

- To use the serverless Spark compute, select **Serverless Spark Compute** under **Azure Machine Learning Serverless Spark** from the **Compute** selection menu.

- To use an attached Synapse Spark pool, select an attached Synapse Spark pool under **Synapse Spark pools** from the **Compute** selection menu.

- This Titanic data wrangling code sample shows use of a data URI in format `abfss://<FILE_SYSTEM_NAME>@<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net/<PATH_TO_DATA>` with `pyspark.pandas` and `pyspark.ml.feature.Imputer`.

    ```python
    import pyspark.pandas as pd
    from pyspark.ml.feature import Imputer

    df = pd.read_csv(
        "abfss://<FILE_SYSTEM_NAME>@<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net/data/titanic.csv",
        index_col="PassengerId",
    )
    imputer = Imputer(inputCols=["Age"], outputCol="Age").setStrategy(
        "mean"
    )  # Replace missing values in Age column with the mean value
    df.fillna(
        value={"Cabin": "None"}, inplace=True
    )  # Fill Cabin column with value "None" if missing
    df.dropna(inplace=True)  # Drop the rows which still have any missing value
    df.to_csv(
        "abfss://<FILE_SYSTEM_NAME>@<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net/data/wrangled",
        index_col="PassengerId",
    )
    ```

    > [!NOTE]
    > This Python code sample uses `pyspark.pandas`. Only the Spark runtime version 3.2 or later supports this.

To wrangle data by access through a service principal:

1. Verify that the service principal has **Contributor** and **Storage Blob Data Contributor** [role assignments](./apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Data Lake Storage (ADLS) Gen 2 storage account.
1. [Create Azure Key Vault secrets](./apache-spark-environment-configuration.md#store-azure-storage-account-credentials-as-secrets-in-azure-key-vault) for the service principal tenant ID, client ID and client secret values.
1. In the **Compute** selection menu, select **Serverless Spark compute** under **Azure Machine Learning Serverless Spark**. You can also select an attached Synapse Spark pool under **Synapse Spark pools** from the **Compute** selection menu.
1. Set the service principal tenant ID, client ID and client secret values in the configuration, and execute the following code sample.
     - The `get_secret()` call in the code depends on name of the Azure Key Vault, and the names of the Azure Key Vault secrets created for the service principal tenant ID, client ID and client secret. Set these corresponding property name/values in the configuration:
       - Client ID property: `fs.azure.account.oauth2.client.id.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net`
       - Client secret property: `fs.azure.account.oauth2.client.secret.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net`
       - Tenant ID property: `fs.azure.account.oauth2.client.endpoint.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net`
       - Tenant ID value: `https://login.microsoftonline.com/<TENANT_ID>/oauth2/token`

        ```python
        from pyspark.sql import SparkSession

        sc = SparkSession.builder.getOrCreate()
        token_library = sc._jvm.com.microsoft.azure.synapse.tokenlibrary.TokenLibrary

        # Set up service principal tenant ID, client ID and secret from Azure Key Vault
        client_id = token_library.getSecret("<KEY_VAULT_NAME>", "<CLIENT_ID_SECRET_NAME>")
        tenant_id = token_library.getSecret("<KEY_VAULT_NAME>", "<TENANT_ID_SECRET_NAME>")
        client_secret = token_library.getSecret("<KEY_VAULT_NAME>", "<CLIENT_SECRET_NAME>")

        # Set up service principal which has access of the data
        sc._jsc.hadoopConfiguration().set(
            "fs.azure.account.auth.type.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net", "OAuth"
        )
        sc._jsc.hadoopConfiguration().set(
            "fs.azure.account.oauth.provider.type.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net",
            "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        )
        sc._jsc.hadoopConfiguration().set(
            "fs.azure.account.oauth2.client.id.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net",
            client_id,
        )
        sc._jsc.hadoopConfiguration().set(
            "fs.azure.account.oauth2.client.secret.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net",
            client_secret,
        )
        sc._jsc.hadoopConfiguration().set(
            "fs.azure.account.oauth2.client.endpoint.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net",
            "https://login.microsoftonline.com/" + tenant_id + "/oauth2/token",
        )
        ```

1. Using the Titanic data, import and the wrangle data using the data URI in the `abfss://<FILE_SYSTEM_NAME>@<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net/<PATH_TO_DATA>` format, as shown in the code sample.

### Import and wrangle data from Azure Blob storage

You can access Azure Blob storage data with either the storage account access key or a shared access signature (SAS) token. You should [store these credentials in the Azure Key Vault as a secret](./apache-spark-environment-configuration.md#store-azure-storage-account-credentials-as-secrets-in-azure-key-vault), and set them as properties in the session configuration.

To start interactive data wrangling:
1. At the Azure Machine Learning studio left panel, select **Notebooks**.
1. In the **Compute** selection menu, select **Serverless Spark compute** under **Azure Machine Learning Serverless Spark**. You can also select an attached Synapse Spark pool under **Synapse Spark pools** from the **Compute** selection menu.
1. To configure the storage account access key or a shared access signature (SAS) token for data access in Azure Machine Learning Notebooks:

     - For the access key, set the `fs.azure.account.key.<STORAGE_ACCOUNT_NAME>.blob.core.windows.net` property, as shown in this code snippet:

        ```python
        from pyspark.sql import SparkSession

        sc = SparkSession.builder.getOrCreate()
        token_library = sc._jvm.com.microsoft.azure.synapse.tokenlibrary.TokenLibrary
        access_key = token_library.getSecret("<KEY_VAULT_NAME>", "<ACCESS_KEY_SECRET_NAME>")
        sc._jsc.hadoopConfiguration().set(
            "fs.azure.account.key.<STORAGE_ACCOUNT_NAME>.blob.core.windows.net", access_key
        )
        ```
     - For the SAS token, set the `fs.azure.sas.<BLOB_CONTAINER_NAME>.<STORAGE_ACCOUNT_NAME>.blob.core.windows.net` property, as shown in this code snippet:
   
        ```python
        from pyspark.sql import SparkSession

        sc = SparkSession.builder.getOrCreate()
        token_library = sc._jvm.com.microsoft.azure.synapse.tokenlibrary.TokenLibrary
        sas_token = token_library.getSecret("<KEY_VAULT_NAME>", "<SAS_TOKEN_SECRET_NAME>")
        sc._jsc.hadoopConfiguration().set(
            "fs.azure.sas.<BLOB_CONTAINER_NAME>.<STORAGE_ACCOUNT_NAME>.blob.core.windows.net",
            sas_token,
        )
        ```
        > [!NOTE]
        > The `get_secret()` calls in the earlier code snippets require the name of the Azure Key Vault, and the names of the secrets created for the Azure Blob storage account access key or SAS token.

2. Execute the data wrangling code in the same notebook. Format the data URI as `wasbs://<BLOB_CONTAINER_NAME>@<STORAGE_ACCOUNT_NAME>.blob.core.windows.net/<PATH_TO_DATA>`, similar to what this code snippet shows:

    ```python
    import pyspark.pandas as pd
    from pyspark.ml.feature import Imputer

    df = pd.read_csv(
        "wasbs://<BLOB_CONTAINER_NAME>@<STORAGE_ACCOUNT_NAME>.blob.core.windows.net/data/titanic.csv",
        index_col="PassengerId",
    )
    imputer = Imputer(inputCols=["Age"], outputCol="Age").setStrategy(
        "mean"
    )  # Replace missing values in Age column with the mean value
    df.fillna(
        value={"Cabin": "None"}, inplace=True
    )  # Fill Cabin column with value "None" if missing
    df.dropna(inplace=True)  # Drop the rows which still have any missing value
    df.to_csv(
        "wasbs://<BLOB_CONTAINER_NAME>@<STORAGE_ACCOUNT_NAME>.blob.core.windows.net/data/wrangled",
        index_col="PassengerId",
    )
    ```

    > [!NOTE]
    > This Python code sample uses `pyspark.pandas`. Only the Spark runtime version 3.2 or later supports this.

### Import and wrangle data from Azure Machine Learning Datastore

To access data from [Azure Machine Learning Datastore](how-to-datastore.md), define a path to data on the datastore with [URI format](how-to-create-data-assets.md?tabs=cli#create-data-assets) `azureml://datastores/<DATASTORE_NAME>/paths/<PATH_TO_DATA>`. To wrangle data from an Azure Machine Learning Datastore in a Notebooks session interactively:

1. Select **Serverless Spark compute** under **Azure Machine Learning Serverless Spark** from the **Compute** selection menu, or select an attached Synapse Spark pool under **Synapse Spark pools** from the **Compute** selection menu.
1. This code sample shows how to read and wrangle Titanic data from an Azure Machine Learning Datastore, using `azureml://` datastore URI, `pyspark.pandas`, and `pyspark.ml.feature.Imputer`.

    ```python
    import pyspark.pandas as pd
    from pyspark.ml.feature import Imputer

    df = pd.read_csv(
        "azureml://datastores/workspaceblobstore/paths/data/titanic.csv",
        index_col="PassengerId",
    )
    imputer = Imputer(inputCols=["Age"], outputCol="Age").setStrategy(
        "mean"
    )  # Replace missing values in Age column with the mean value
    df.fillna(
        value={"Cabin": "None"}, inplace=True
    )  # Fill Cabin column with value "None" if missing
    df.dropna(inplace=True)  # Drop the rows which still have any missing value
    df.to_csv(
        "azureml://datastores/workspaceblobstore/paths/data/wrangled",
        index_col="PassengerId",
    )
    ```

    > [!NOTE]
    > This Python code sample uses `pyspark.pandas`. Only the Spark runtime version 3.2 or later supports this.

The Azure Machine Learning datastores can access data using Azure storage account credentials

- access key
- SAS token
- service principal

or they use credential-less data access. Depending on the datastore type and the underlying Azure storage account type, select an appropriate authentication mechanism to ensure data access. This table summarizes the authentication mechanisms to access data in the Azure Machine Learning datastores:

|Storage account type|Credential-less data access|Data access mechanism|Role assignments|
| ------------------------ | ------------------------ | ------------------------ | ------------------------ |
|Azure Blob|No|Access key or SAS token|No role assignments needed|
|Azure Blob|Yes|User identity passthrough<sup>__*__</sup>|User identity should have [appropriate role assignments](./apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Blob storage account|
|Azure Data Lake Storage (ADLS) Gen 2|No|Service principal|Service principal should have [appropriate role assignments](./apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Data Lake Storage (ADLS) Gen 2 storage account|
|Azure Data Lake Storage (ADLS) Gen 2|Yes|User identity passthrough|User identity should have [appropriate role assignments](./apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Data Lake Storage (ADLS) Gen 2 storage account|

<sub>__*__</sub> User identity passthrough works for credential-less datastores that point to Azure Blob storage accounts, only if [soft delete](/azure/storage/blobs/soft-delete-blob-overview) is not enabled.

## Accessing data on the default file share

The default file share is mounted to both serverless Spark compute and attached Synapse Spark pools.

:::image type="content" source="media/interactive-data-wrangling-with-apache-spark-azure-ml/default-file-share.png" alt-text="Screenshot showing use of a file share.":::

In Azure Machine Learning studio, files in the default file share are shown in the directory tree under the **Files** tab. Notebook code can directly access files stored in this file share with the `file://` protocol, along with the absolute path of the file, without more configurations. This code snippet shows how to access a file stored on the default file share:

```python
import os
import pyspark.pandas as pd
from pyspark.ml.feature import Imputer

abspath = os.path.abspath(".")
file = "file://" + abspath + "/Users/<USER>/data/titanic.csv"
print(file)
df = pd.read_csv(file, index_col="PassengerId")
imputer = Imputer(
    inputCols=["Age"],
    outputCol="Age").setStrategy("mean") # Replace missing values in Age column with the mean value
df.fillna(value={"Cabin" : "None"}, inplace=True) # Fill Cabin column with value "None" if missing
df.dropna(inplace=True) # Drop the rows which still have any missing value
output_path = "file://" + abspath + "/Users/<USER>/data/wrangled"
df.to_csv(output_path, index_col="PassengerId")
```

> [!NOTE]
> This Python code sample uses `pyspark.pandas`. Only the Spark runtime version 3.2 or later supports this.

## Next steps

- [Code samples for interactive data wrangling with Apache Spark in Azure Machine Learning](https://github.com/Azure/azureml-examples/tree/main/sdk/python/data-wrangling)
- [Optimize Apache Spark jobs in Azure Synapse Analytics](/azure/synapse-analytics/spark/apache-spark-performance)
- [What are Azure Machine Learning pipelines?](./concept-ml-pipelines.md)
- [Submit Spark jobs in Azure Machine Learning](./how-to-submit-spark-jobs.md)
