--- 
title: Interactive data wrangling with Apache Spark
titleSuffix: Azure Machine Learning
description: Learn how to use Apache Spark to wrangle data with Azure Machine Learning.
author: s-polly
ms.author: scottpolly
ms.reviewer: soumyapatro
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.date: 01/30/2026
ms.custom: template-how-to
#customer intent: As a data scientist, I want to learn how to set up and configure Spark serverless compute sessions in Azure Machine Learning studio so I can easily access and wrangle data from various sources.
---

# Interactive data wrangling with Apache Spark

Data wrangling is an important aspect of machine learning projects. In this article, you learn how to do interactive data wrangling by running Azure Machine Learning notebooks on a serverless Apache Spark compute backed by Azure Synapse.

This article explains how to attach and configure a serverless Spark compute. The article then shows how to use the serverless Spark compute to access and wrangle data from several sources.

## Prerequisites
- Owner or role-assignment permissions in an Azure subscription. You can [create a free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure Machine Learning workspace. For more information, see [Create workspace resources](./quickstart-create-resources.md).
- The [titanic.csv dataset](https://github.com/Azure/azureml-examples/tree/main/sdk/python/data-wrangling/data) uploaded to the default file share in your workspace.
- An Azure Data Lake Storage Gen 2 storage account. For more information, see [Create an Azure Data Lake Storage Gen 2 storage account](/azure/storage/blobs/create-data-lake-storage-account).
- The following [role assignments](apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) granted:
  - For Azure Storage account access, **Contributor** and **Storage Blob Data Contributor** roles in the Azure Storage account.
  - For Azure Key Vault secret access, **Key Vault Secrets User** role in the key vault.

For more information, see:
- [Create an Azure Key Vault](/azure/key-vault/general/quick-create-portal)
- [Create a service principal](/azure/active-directory/develop/howto-create-service-principal-portal)
- [Attach a Synapse Spark pool in the Azure Machine Learning workspace](how-to-manage-synapse-spark-pool.md)

## Use serverless Spark compute in notebook sessions

Using a serverless Spark compute is the easiest way to access a Spark cluster for interactive data wrangling. A fully managed serverless Spark compute attached to a [Synapse Spark pool](how-to-manage-synapse-spark-pool.md) is directly available in Azure Machine Learning notebooks.

To use any of the following data access and wrangling sources and methods, attach the Spark serverless compute by selecting **Azure Machine Learning Serverless Spark** > **Serverless Spark Compute - Available** next to **Compute** at the top of the file or notebook page. It can take a minute or two for the compute to attach to the session.

### Configure a serverless Spark session

Once you attach the serverless Spark compute, you can optionally configure the Spark session by setting or changing several values. To configure the Spark session:

1. Select **Configure session** at upper left on the file or notebook page.
1. On the **Configure session** screen, change any of the following settings:
   - In the **Compute** pane:
     - Change the machine size by selecting a different size from the dropdown menu under **Node size**. 
     - Select whether or not to **Dynamically allocate executors**.
     - Select the number of **Executors** for the Spark session.
     - Select a different **Executor size** if available from the dropdown menu.

   - In the **Settings** pane:
     - Change the **Apache Spark version** to a different version than 3.4 if available.
     - Change the **Session timeout** value in minutes to a higher number to help prevent session timeouts.
     - Under **Configuration settings**, add **Property** name/value settings to configure the session as needed.
       >[!TIP]
       >If you use session-level Conda packages, adding the `spark.hadoop.aml.enable_cache` configuration property with value `true` can [improve the Spark session cold start time](apache-spark-azure-ml-concepts.md#improving-session-cold-start-time-while-using-session-level-conda-packages). A session cold start with session level Conda packages typically takes 10 to 15 minutes the first time. Subsequent session cold starts with the configuration variable set to true typically take three to five minutes.

   - In the **Python packages** pane:
     - To use a Conda file to configure your session, select **Upload conda file**. Next to **Select conda file**, select **Browse**, and then browse to and open the appropriate Conda YAML file on your machine to upload it.
     - To use a custom environment, select **Custom environment** and select a custom environment under **Environment type**. For more information, see [Manage software environments](how-to-manage-environments-in-studio.md).
1. To apply all configurations, select **Apply**.

The session configuration changes persist and are available to other notebook sessions that use the attached serverless Spark compute.

## Import and wrangle data from Azure Data Lake Storage

To access and wrangle data stored in Azure Data Lake Storage storage accounts, you use a `abfss://` protocol URI with either *user identity passthrough* or *service principal-based* access. User identity passthrough requires no added configuration.

To use either method, the user identity or service principal must have **Contributor** and **Storage Blob Data Contributor** [role assignments](apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Data Lake Storage account.

For user identity passthrough, run the following data wrangling code sample to use a data URI in format `abfss://<FILE_SYSTEM_NAME>@<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net/<PATH_TO_DATA>` with `pyspark.pandas` and `pyspark.ml.feature.Imputer`. Replace the `<STORAGE_ACCOUNT_NAME>` placeholder with the name of your Azure Data Lake Storage account and `<FILE_SYSTEM_NAME>` with the name of the data container.

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

### Use a service principal

To use a service principal to access and wrangle data from Azure Data Lake Storage, first set up the service principal as follows:

1. [Create a service principal](/azure/active-directory/develop/howto-create-service-principal-portal) and [assign it the necessary Storage Blob Data Contributor and Key Vault Secrets User roles](/azure/active-directory/develop/howto-create-service-principal-portal#assign-a-role-to-the-application).
1. Obtain the service principal tenant ID, client ID, and client secret values from the app registration and [create Azure Key Vault secrets](apache-spark-environment-configuration.md#store-azure-storage-account-credentials-as-secrets-in-azure-key-vault) for the values.
1. Set the service principal tenant ID, client ID, and client secret by adding the following property name/value pairs in the session configuration. Replace `<STORAGE_ACCOUNT_NAME>` with your storage account name and `<TENANT_ID>` with the service principal tenant ID.

   |Property name|Value|
   |-------------|-----|
   |`fs.azure.account.oauth2.client.id.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net`|Application (client) ID value|
   |`fs.azure.account.oauth2.client.endpoint.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net`|`https://login.microsoftonline.com/<TENANT_ID>/oauth2/token`|
   |`fs.azure.account.oauth2.client.secret.<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net`|Client secret value|

1. Run the following code. The `get_secret()` call in the code depends on the Key Vault name and the names of the Key Vault secrets created for the service principal tenant ID, client ID and client secret.

   ```python
   from pyspark.sql import SparkSession

   sc = SparkSession.builder.getOrCreate()
   token_library = sc._jvm.com.microsoft.azure.synapse.tokenlibrary.TokenLibrary

   # Set up service principal tenant ID, client ID, and secret from Azure Key Vault
   client_id = token_library.getSecret("<KEY_VAULT_NAME>", "<CLIENT_ID_SECRET_NAME>")
   tenant_id = token_library.getSecret("<KEY_VAULT_NAME>", "<TENANT_ID_SECRET_NAME>")
   client_secret = token_library.getSecret("<KEY_VAULT_NAME>", "<CLIENT_SECRET_NAME>")

   # Set up a service principal that has access to the data
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

1. Import and wrangle the *titanic.csv* data using a data URI in the `abfss://<FILE_SYSTEM_NAME>@<STORAGE_ACCOUNT_NAME>.dfs.core.windows.net/<PATH_TO_DATA>` format, as shown in the code sample. Replace the `<STORAGE_ACCOUNT_NAME>` placeholder with the name of your Azure Data Lake Storage account and `<FILE_SYSTEM_NAME>` with the name of the data container.

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

## Import and wrangle data from Azure Blob storage

You can access Azure Blob storage data with either the *storage account access key* or a *shared access signature (SAS) token*. [Store the credential in Azure Key Vault as a secret](apache-spark-environment-configuration.md#store-azure-storage-account-credentials-as-secrets-in-azure-key-vault), and set it as a property in the Spark session configuration.

1. Run one of the following code snippets. The `get_secret()` calls in the code snippets require the name of the key vault and the names of the secrets created for the Azure Blob storage account access key or SAS token.

   - To configure a storage account access key, set the `fs.azure.account.key.<STORAGE_ACCOUNT_NAME>.blob.core.windows.net` property as shown in the following code snippet:

     ```python
     from pyspark.sql import SparkSession
     
     sc = SparkSession.builder.getOrCreate()
     token_library = sc._jvm.com.microsoft.azure.synapse.tokenlibrary.TokenLibrary
     access_key = token_library.getSecret("<KEY_VAULT_NAME>", "<ACCESS_KEY_SECRET_NAME>")
     sc._jsc.hadoopConfiguration().set(
         "fs.azure.account.key.<STORAGE_ACCOUNT_NAME>.blob.core.windows.net", access_key
     )
     ```

   - To configure a SAS token, set the `fs.azure.sas.<BLOB_CONTAINER_NAME>.<STORAGE_ACCOUNT_NAME>.blob.core.windows.net` property as shown in the following code snippet:

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

1. Run the following data wrangling code with the data URI formatted as `wasbs://<BLOB_CONTAINER_NAME>@<STORAGE_ACCOUNT_NAME>.blob.core.windows.net/<PATH_TO_DATA>`.

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

## Import and wrangle data from an Azure Machine Learning datastore

To access data from an [Azure Machine Learning datastore](how-to-datastore.md), you define a path to data on the datastore with the [URI format](how-to-create-data-assets.md?tabs=cli#create-data-assets) `azureml://datastores/<DATASTORE_NAME>/paths/<PATH_TO_DATA>`.

Run the following code sample to read and wrangle *titanic.csv* data from an Azure Machine Learning datastore using `azureml://` datastore URI, `pyspark.pandas`, and `pyspark.ml.feature.Imputer`.

```python
import pyspark.pandas as pd
from pyspark.ml.feature import Imputer

df = pd.read_csv(
    "azureml://datastores/<DATASTORE_NAME>/paths/data/titanic.csv",
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
    "azureml://datastores/<DATASTORE_NAME>/paths/data/wrangled",
    index_col="PassengerId",
)
```

Azure Machine Learning datastores can access data using an Azure storage account access key, SAS token, service principal credentials, or credentialless data access. Select the appropriate authentication mechanism depending on datastore type and underlying Azure storage account type.

The following table summarizes the authentication mechanisms for accessing data in Azure Machine Learning datastores:

|Storage account type|Credentialless data access|Data access mechanism|Role assignments|
| ------------------------ | ------------------------ | ------------------------ | ------------------------ |
|Azure Blob|No|Access key or SAS token|No role assignments needed.|
|Azure Blob|Yes|User identity passthrough\*|User identity should have [appropriate role assignments](apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Blob storage account.|
|Azure Data Lake Storage|No|Service principal|Service principal should have [appropriate role assignments](apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Data Lake Storage storage account.|
|Azure Data Lake Storage|Yes|User identity passthrough|User identity should have [appropriate role assignments](./apache-spark-environment-configuration.md#add-role-assignments-in-azure-storage-accounts) in the Azure Data Lake Storage storage account.|

\* User identity passthrough works for credentialless datastores that point to Azure Blob storage accounts only if [soft delete](/azure/storage/blobs/soft-delete-blob-overview) isn't enabled.

## Access data on the default file share

In Azure Machine Learning studio, your default workspace file share is the directory tree under the **Files** tab in **Notebooks**. Notebook code can directly access files stored in this file share with the `file://` protocol, using the absolute path of the file without other configuration. The default file share is mounted to both serverless Spark compute and attached Synapse Spark pools.

:::image type="content" source="media/interactive-data-wrangling-with-apache-spark-azure-ml/default-file-share.png" lightbox="media/interactive-data-wrangling-with-apache-spark-azure-ml/default-file-share.png" alt-text="Screenshot showing use of a file share.":::

The following code snippet accesses and wrangles data from the *titanic.csv* file stored in a *data* folder directly under the user name on the default file share. Replace the `<USER>` placeholder with your user name.

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

## Related content

- [Code samples for interactive data wrangling with Apache Spark in Azure Machine Learning](https://github.com/Azure/azureml-examples/tree/main/sdk/python/data-wrangling)
- [Optimize Apache Spark jobs in Azure Synapse Analytics](/azure/synapse-analytics/spark/apache-spark-performance)
- [What are Azure Machine Learning pipelines?](./concept-ml-pipelines.md)
- [Submit Spark jobs in Azure Machine Learning](./how-to-submit-spark-jobs.md)
