---
title: Connect to external data sources and assets (preview)
titleSuffix: Azure Machine Learning
description: Learn how to create connections to connect to external data sources and other assets for training with Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.author: scottpolly
author: s-polly
ms.reviewer: ambadal
ms.date: 12/22/2025
ms.custom:
  - data4ml
  - devx-track-azurecli
  - sfi-image-nochange
  - sfi-ropc-blocked
# Customer intent: As an experienced data scientist with Python skills, I need to make my data located in external sources outside of Azure available to the Azure Machine Learning platform so I can train my machine learning models.
---

# Create external connections (preview)

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, you learn how to connect to external data sources to make their data available to Azure Machine Learning. You also see how to connect to several external nondata assets. You can use the Azure Machine Learning CLI, the Azure Machine Learning SDK for Python, or Machine Learning studio to create these connections.

An Azure Machine Learning connection securely stores usernames and passwords as secrets in a key vault. Azure connections serve as key vault proxies, and interactions with the connections are direct interactions with Azure Key Vault. Key Vault role-based access control (RBAC) manages access to the data resources. You don't need to deal directly with the credentials after they're stored in the key vault.

You have the option to store credentials in a YAML file, and to use the Azure CLI or Python SDK command lines to override the stored credentials. However, it's best to avoid credential storage in a file, because a security breach could lead to a credential leak.

Azure supports connections to the following external sources for data availability:

- Snowflake DB
- Amazon S3
- Azure SQL DB

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

## Prerequisites

- An Azure subscription with the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure Machine Learning workspace.

# [Azure CLI](#tab/cli)

- To run the CLI commands, the Azure CLI and the `ml` extension version 2.15.1 or later installed. If you have an older Azure CLI version or extension, use the following code to uninstall it and install the new one.

  ```azurecli
  az extension remove -n ml
  az extension add -n ml --yes
  az extension show -n ml 2.15.1
  ```

# [Python SDK](#tab/python)

- To run the Python SDK commands, the [Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install) with the `azure-ai-ml` version 1.5.0 or later package installed. If you have an older SDK package, use the following code to uninstall it and install the new one.

  ```python
  pip uninstall azure-ai-ml
  pip install azure-ai-ml
  pip show azure-ai-ml 1.5.0
  ```

---

## Create data connections using Azure CLI or Python SDK

You can create data connections by assembling a YAML file that defines the connection, and then running an Azure CLI or Python SDK command that calls the YAML file to create the connection. For Python SDK, you can also specify the connection information directly in a Python script without using a YAML file.

### Create a Snowflake DB connection that uses username/password authentication

The following YAML file defines a Snowflake DB connection that uses username/password authentication. To create the file, provide a `<connection-name>`, and replace the `<account>`, `<database>`, `<warehouse>`, and `<role>` placeholders with the appropriate values from your Snowflake account. If you don't provide a `<role>`, the value defaults to `PUBLIC`. 

For `credentials`, you can store the Snowflake database user name and password in this file, or for better security, leave the values blank and provide them in the command line that creates the connection. Save the file with a name like *my_snowflakedb_connection.yaml*.

The following YAML file defines a Snowflake DB connection with username/password authentication:

```yaml
$schema: http://azureml/sdk-2-0/Connection.json
type: snowflake
name: <connection-name>

target: jdbc:snowflake://<account>.snowflakecomputing.com/?db=<database>&warehouse=<warehouse>&role=<role>
credentials:
    type: username_password
    username: <username>
    password: <password>
```

# [Azure CLI](#tab/cli)

To create the connection, run one of the following CLI command lines, providing your YAML filename in the `<yaml-filename>` placeholder.

To use the username and password stored in the YAML file, run the following command:

```azurecli
az ml connection create --file <yaml-filename>.yaml
```

Or to provide the username and password as part of the command line, run the following command, entering your `<username>` and `<password>` for the placeholders:

```azurecli
az ml connection create --file <yaml-filename>.yaml --set credentials.username="<username>" credentials.password="<password>"
```

# [Python SDK](#tab/python)

You can use the Python SDK to call the YAML file that defines the connection, or you can specify the connection information directly without using a YAML file.

To create the Snowflake connection by calling a YAML file, run the following script, replacing the `<yaml-filename>` placeholder with your YAML filename.

```python
from azure.ai.ml import MLClient, load_workspace_connection

ml_client = MLClient.from_config()

wps_connection = load_workspace_connection(source="./<yaml-filename>.yaml")
wps_connection.credentials.username="<username>"
wps_connection.credentials.password="<password>"
ml_client.connections.create_or_update(workspace_connection=wps_connection)

```

You can also directly specify the connection information in a Python script without using a YAML file. In the following script, provide a `<connection-name>`, and replace the `<account>`, `<database>`, `<warehouse>`, and `<role>` placeholders with the appropriate values from your Snowflake account.

If you don't provide a `<role>`, the value defaults to `PUBLIC`. For the username-password authentication type, the name/password values should be URL-encoded.

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration

import urllib.parse
username = urllib.parse.quote(os.environ["SNOWFLAKEDB_USERNAME"], safe="")
password = urllib.parse.quote(os.environ["SNOWFLAKEDB_PASSWORD"], safe="")

target= "jdbc:snowflake://<account>.snowflakecomputing.com/?db=<database>&warehouse=<warehouse>&role=<role>"
name= <connection-name>
wps_connection = WorkspaceConnection(name= name,
type="snowflake",
target= target,
credentials= UsernamePasswordConfiguration(username=username, password=password)
)

ml_client.connections.create_or_update(workspace_connection=wps_connection)

```

---

### Create a Snowflake DB connection that uses OAuth

You can use the Azure CLI or Python SDK to create a Snowflake DB connection that uses a service principal for OAuth to authenticate.

> [!IMPORTANT]
> Before you can create the connection using OAuth, you must first [Configure Azure to issue OAuth tokens on behalf of the client](https://community.snowflake.com/s/article/Create-External-OAuth-Token-Using-Azure-AD-For-The-OAuth-Client-Itself). This configuration creates the required service principal for the OAuth connection. To create the connection, you need the following information:
>
> - **Client ID**: The ID of the service principal
> - **Client Secret**: The service principal secret
> - **Tenant ID**: The ID of the Microsoft Entra ID tenant

# [Azure CLI](#tab/cli)

The following YAML file defines a Snowflake DB connection that uses OAuth. To create the file, provide a `<connection-name>`, and replace the `<account>`, `<database>`, `<warehouse>`, and `<service-principal-scope>` placeholders with the appropriate values from your Snowflake account.

For credentials, provide your `<client-id>`, `<client-secret>`, and `<tenant_id>` for the corresponding placeholders.

```yaml
name: <connection-name>
type: snowflake
target: jdbc:snowflake://<account>.snowflakecomputing.com/?db=<database>&warehouse=<warehouse>&scope=<service-principal-scope>
credentials:
  type: service_principal
  client_id: <client-id>
  client_secret: <client-secret>
  tenant_id: <tenant-id>
```

To create the connection using the credential information stored in the YAML file, run the following command, replacing the `<yaml-filename>` placeholder with your YAML filename.

```azurecli
az ml connection create --file <yaml-filename>.yaml
```

To override the information in the YAML file or provide credentials in the command line, run the following command, entering your `<client-id>`, `<client-secret>`, and `<tenant-id>` values for the placeholders:

```azurecli
az ml connection create --file <yaml-filename>.yaml --set credentials.client_id="<client-id>" credentials.client_secret="<client-secret>" credentials.tenant_id="<tenant-id>"
```

# [Python SDK](#tab/python)

You can use the Python SDK to call the YAML file that defines the connection, or you can specify the connection information directly without using a YAML file.

To create the OAuth connection by calling a YAML file, run the following script, replacing the `<yaml-filename>` placeholder with your YAML filename. You can optionally override or provide the `<wps_connection.credentials>` values:

```python
from azure.ai.ml import MLClient, load_workspace_connection

ml_client = MLClient.from_config()

wps_connection = load_workspace_connection(source="./<yaml-filename>.yaml")
wps_connection.credentials.client_id="<client-id>"
wps_connection.credentials.client_secret="<client-secret>"
wps_connection.credentials.tenant_id="<tenant-id>"
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

You can also directly specify the OAuth connection information in a Python script without using a YAML file. In the following script, provide a `<connection-name>`, and replace the `<account>`, `<database>`, `<warehouse>`, and `<role>` placeholders with the appropriate values from your Snowflake account. Enter your `<client-id>`, `<client-secret>`, and `<tenant-id>` values for those placeholders.

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import ServicePrincipalConfiguration

target= "jdbc:snowflake://<account>.snowflakecomputing.com/?db=<database>&warehouse=<warehouse>&role=<role>"
name= <connection-name>
auth = ServicePrincipalConfiguration(client_id="<client-id>", client_secret="<client-secret>", tenant_id="<tenant-id>")
wps_connection = WorkspaceConnection(name= name,
                                     type="snowflake",
                                     target=target,
                                     credentials=auth
)

ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

---

### Create an Azure SQL DB connection

The following YAML file defines an Azure SQL DB connection. To create the file, provide a `<connection-name>`, and replace the `<server>`, `<port>`, and `<database>` placeholders with the appropriate values from your Azure SQL database.

For `credentials`, you can store the Azure SQL database user name and password in this file, or for better security, leave the values blank and provide them in the command line that creates the connection. Save the file with a name like *my_azure_sql_db_connection.yaml*.

```yaml
$schema: http://azureml/sdk-2-0/Connection.json

type: azure_sql_db
name: <connection-name>

target: Server=tcp:<server>,<port>;Database=<database>;Trusted_Connection=False;Encrypt=True;Connection Timeout=30
credentials:
    type: sql_auth
    username: <username>
    password: <password>
```

# [Azure CLI](#tab/cli)

To create the connection, run one of the following CLI command lines, providing your YAML filename for the `<yaml-filename>` placeholder.

To use the username and password stored in the YAML file, run the following command:

```azurecli
az ml connection create --file <yaml-filename>.yaml
```

Or to provide the username and password as part of the command line, run the following command, entering your `<username>` and `<password>` for the placeholders:

```azurecli
az ml connection create --file <yaml-filename>.yaml --set credentials.username="<username>" credentials.password="<password>"
```

# [Python SDK](#tab/python)

You can use the Python SDK to call the YAML file that defines the connection, or you can specify the connection information directly without using a YAML file.

To create the Snowflake connection by calling a YAML file, run the following script, replacing the `<yaml-filename>` placeholder with your YAML filename.

```python
from azure.ai.ml import MLClient, load_workspace_connection

ml_client = MLClient.from_config()

wps_connection = load_workspace_connection(source="./<yaml-filename>.yaml")
wps_connection.credentials.username="<username>"
wps_connection.credentials.password="<password>"
ml_client.connections.create_or_update(workspace_connection=wps_connection)

```

You can also directly specify the connection information in a Python script without using a YAML file. In the following script, provide a `<connection-name>`, and replace the `<server>`, `<port>`, and `<database>` placeholders with the appropriate values for your Azure SQL database. For the username-password authentication type, the name/password values should be URL-encoded.

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration

import urllib.parse
username = urllib.parse.quote(os.environ["MYSQL_USERNAME"], safe="")
password = urllib.parse.quote(os.environ["MYSQL_PASSWORD"], safe="")

target= "Server=tcp:<server>,<port>;Database=<database>;Trusted_Connection=False;Encrypt=True;Connection Timeout=30"
# add the sql servername, port address and database

name= <connection-name>
wps_connection = WorkspaceConnection(name= name,
type="azure_sql_db",
target= target,
credentials= UsernamePasswordConfiguration(username=username, password=password)
)

ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

---
### Create an Amazon S3 connection

The following YAML file defines an Amazon S3 connection. To create the file, provide a `<connection-name>`, and replace the `<s3-bucket-name>`, `<access-key-id>`, and `<secret-access-key>` placeholders with the appropriate values from your Amazon S3 account.  Save the file with a name like *my_amazon_s3_connection.yaml*.

```yaml
$schema: http://azureml/sdk-2-0/Connection.json

type: s3
name: <connection-name>

target: <s3-bucket-name>
credentials:
    type: access_key
    access_key_id: <access-key-id>
    secret_access_key: <secret-access-key>
```

# [Azure CLI](#tab/cli)

To create the connection, run the following CLI command, providing your YAML filename for the `<yaml-filename>` placeholder.

```azurecli
az ml connection create --file <yaml-filename>.yaml
```

# [Python SDK](#tab/python)

You can use the Python SDK to call the YAML file that defines the connection, or you can specify the connection information directly without using a YAML file.

To create the Amazon S3 connection by calling a YAML file, run the following script, replacing the `<yaml-filename>` placeholder with your YAML filename.

```python
from azure.ai.ml import MLClient, load_workspace_connection

ml_client = MLClient.from_config()

wps_connection = load_workspace_connection(source="./<yaml-filename>.yaml")
ml_client.connections.create_or_update(workspace_connection=wps_connection)

```

To specify the connection information directly in the following Python script without using a YAML file, provide a `<connection-name>`, and replace the `<s3-bucket-name>`, `<access-key-id>`, and `<secret-access-key>` placeholders with the appropriate values for your Amazon S3 account.

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import AccessKeyConfiguration

target=<s3-bucket-name>
name=<connection-name>
wps_connection=WorkspaceConnection(name=name,
type="s3",
target= target,
credentials= AccessKeyConfiguration(access_key_id="<access-key-id>",secret_access_key="<secret-access-key>")
)

ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

---

## Create nondata connections using Azure CLI or Python SDK

You can also use Azure CLI or Python SDK to create the following connections for Azure Machine Learning. These connections aren't for data, but connect to external services to use in your code.

- Git
- Python feed
- Azure Container Registry
- API key connection
- Generic container registry

### Git

# [Azure CLI](#tab/cli)

You can define a Git connection by using one of the following YAML files. Name the file something like *connection.yml*.

To connect using a personal access token (PAT), provide a `<connection-name>`, and replace the `<account>`, `<repo>`, and `<PAT>` placeholders with the values for your Git account, repo, and PAT.

```yml
name: <connection-name>
type: git
target: https://github.com/<account>/<repo>
credentials:
   type: pat
   pat: <PAT>
```

To connect to a public repo without using credentials, provide a `<connection-name>`, and replace the `<account>`, and `<repo>` placeholders with your values.

```yml
name: <connection-name>
type: git
target: https://github.com/<account>/<repo>
```

To create the Azure Machine Learning connection, run the following command, providing your YAML filename for the `<yaml-filename>` placeholder.

```azurecli
az ml connection create --file <yaml-filename>.yaml
```

# [Python SDK](#tab/python)

The following script creates a Git connection to a GitHub repo. You use a GitHub PAT to authenticate the connection. Provide a `<connection-name>`, and replace the `<account>`, `<repo>`, and `<PAT>` placeholders with your values.

```python
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration, PatTokenConfiguration

name = "<connection-name>"

target = "https://github.com/<account>/<repo>"

wps_connection = WorkspaceConnection(
    name=name,
    type="git",
    target=target,
    credentials=PatTokenConfiguration(pat="<PAT>"),
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

---

### Python feed

# [Azure CLI](#tab/cli)

You can define a Python feed connection by using one of the following YAML files. Name the file something like *connection.yml*.

To connect using a personal access token (PAT), provide a `<connection-name>`, and replace the `<feed-url>` and `<PAT>` placeholders with the values for your feed.

```yml
name: <connection-name>
type: python_feed
target: https://<feed-url>
credentials:
   type: pat
   pat: <PAT>
```

To connect using a username and password, provide a `<connection-name>`, and replace the `<feed-url>`, `<username>`, and `<password>` placeholders with the values for your feed.

```yml
name: <connection-name>
type: python_feed
target: https://<feed-url>
credentials:
   type: username_password
   username: <username>
   password: <password>
```

To connect to a public feed without using credentials, provide a `<connection-name>`, and replace the `<feed-url>` placeholder with your Python feed URL.

```yml
name: <connection-name>
type: python_feed
target: https://<feed-url>
```

To create the Azure Machine Learning connection, run the following command, providing your YAML filename for the `<yaml-filename>` placeholder.

```azurecli
az ml connection create --file <yaml-filename>.yaml
```

# [Python SDK](#tab/python)

The following script creates a Python feed connection. Provide a `<connection-name>`, and replace the `<feed-url>` placeholder with your feed URL.

You can use a PAT or user name and password to authenticate the connection, or connect to a public feed without credentials. For the PAT authentication type, provide your PAT for the `<PAT>` placeholder. For the username-password authentication type, the name/password values should be URL-encoded. 

To use the username/password authentication or no-authentication, uncomment the appropriate line or lines and comment out the `credentials=PatTokenConfiguration(pat="<PAT>"),` line in the following script.

```python
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration, PatTokenConfiguration

# import urllib.parse
# username = urllib.parse.quote(os.environ["FEED_USERNAME"], safe="")
# password = urllib.parse.quote(os.environ["FEED_PASSWORD"], safe="")

name = "<connection-name>"

target = "https://<feed-url>"

wps_connection = WorkspaceConnection(
    name=name,
    type="python_feed",
    target=target,
    #credentials=UsernamePasswordConfiguration(username=username, password=password), 
    credentials=PatTokenConfiguration(pat="<PAT>"),

    #credentials=None
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

---

### Azure Container Registry

# [Azure CLI](#tab/cli)

Use the following YAML file to define a connection to Azure Container Registry with username/password authentication.

```yml
name: <connection-name>
type: container_registry
target: https://<container-registry-url>
credentials:
   type: username_password
   username: <username>
   password: <password>
```

Run the following command to create the connection:

```azurecli
az ml connection create --file connection.yaml
```

# [Python SDK](#tab/python)

The following example creates an Azure Container Registry connection:

```python
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration

# If using username/password, the name/password values should be url-encoded
import urllib.parse
username = os.environ["REGISTRY_USERNAME"]
password = os.environ["REGISTRY_PASSWORD"]

name = "my_acr_conn"

target = "https://iJ5kL6mN7.core.windows.net/mycontainer"

wps_connection = WorkspaceConnection(
    name=name,
    type="container_registry",
    target=target,
    credentials=UsernamePasswordConfiguration(username=username, password=password), 
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

---

### API key

The following Python example creates an API key connection:

```python
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration, ApiKeyConfiguration


name = "my_api_key"

target = "https://L6mN7oP8q.core.windows.net/mycontainer"

wps_connection = WorkspaceConnection(
    name=name,
    type="apikey",
    target=target,
    credentials=ApiKeyConfiguration(key="9sT0uV1wX"),    
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)
```

---

### Generic Container Registry

The GenericContainerRegistry workspace connection specifies an external registry, such as Nexus or Artifactory, for image builds. Environment images are pushed from the specified registry, and the previous cache is ignored.

# [Azure CLI](#tab/cli)

The following example YAML files define a generic container registry connection. Be sure to update the appropriate values.

```yml
#myenv.yml
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json 
name: docker-image-plus-conda-example 
image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04
type: python_feed
conda_file: conda_dep.yml
description: Environment created from a Docker image plus Conda environment
```

```yml
#conda_dep.yml
name: project_environment
dependencies:
  - python=3.10
  - pip:
    - azureml-defaults
channels:
  - anaconda
  - conda-forge
```

```yml
#connection.yml
name: ws_conn_generic_container_registry
type: container_registry
target: https://test-registry.com
credentials:
  type: username_password
  username: <username>
  password: <password>
```

```yml
#hello_world_job.yml
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
command: echo "hello world"
environment: azureml:<env name>@latest
```

Run the following command to create the connection using the YAML file and your credentials. Be sure to update the appropriate values.

```azurecli
az ml connection create --file connection.yaml --credentials username=<username> password=<password> --resource-group <my-resource-group> --workspace-name <my-workspace>
```

Run the following command to create the environment.

```azurecli
az ml environment create --name my-env --version 1 --file my_env.yml  --conda-file conda_dep.yml --image mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04 --resource-group <my-resource-group> --workspace-name <my-workspace>
```

Run the following command to verify that the environment was successfully created.

```azurecli
az ml environment show --name my-env --version 1 --resource-group <my-resource-group> --workspace-name <my-workspace>
```

# [Python SDK](#tab/python)

The following Python example script creates a Generic Container Registry connection.

```python
import os
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Environment
from azure.ai.ml.entities import WorkspaceConnection
from azure.ai.ml.entities import UsernamePasswordConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azure.ai.ml import command

username = os.environ["REGISTRY_USERNAME"]
password = os.environ["REGISTRY_PASSWORD"]

# Enter details of Azure Machine Learning workspace
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<WORKSPACE_NAME>"

ml_client = MLClient( DefaultAzureCredential(), subscription_id, resource_group, workspace)
credentials = UsernamePasswordConfiguration(username=username, password=password)

# Create GenericContainerRegistry workspace connection for a generic registry
ws_connection = WorkspaceConnection(name="<name>", target="<target>", type="GenericContainerRegistry", credentials=credentials)
ml_client.connections.create_or_update(ws_connection)

# Create an environment
env_docker_conda = Environment(image="<base image>", conda_file="<yml file>", name="docker-image-plus-conda-example", description="Environment created from a Docker image plus Conda environment.")
ml_client.environments.create_or_updat(env_docker_conda) 

job = command(command="echo 'hello world'", environment=env_docker_conda,display_name="v2-job-example")
returned_job = ml_client.create_or_update(job)
```

---

## Create connections using the studio

You can create data connections to Snowflake, Azure SQL DB, and Amazon S3 in Machine Learning studio, and use these connections to run data import jobs. Credentials are securely stored in the key vault associated with the workspace. The studio doesn't support creating data connections using OAuth authentication.

### Create a Snowflake DB connection

1. In your [Azure Machine Learning studio](https://ml.azure.com) workspace, select **Data** under **Assets** in the left navigation menu.
1. On the **Data** page, select the **Data Connection** tab, and then select **Connect**.

   :::image type="content" source="media/how-to-connection/create-new-data-connection.png" lightbox="media/how-to-connection/create-new-data-connection.png" alt-text="Screenshot showing the start of a new data connection in Azure Machine Learning studio.":::

1. In the **Create connection** pane, complete the following information:

   - **Service**: Select **Snowflake**.
   - **Target**: Provide the following information, using the values from your Snowflake account for the placeholders:<br>**jdbc:snowflake://\<account>.snowflakecomputing.com/?db=\<database>&warehouse=\<warehouse>&role=\<role>**.
   - **Authentication type**: Select **Username password**.
   - **Username**: Enter your Snowflake user name.
   - **Password**: Enter your Snowflake password.
   - **Connection name**: Enter a name for the Snowflake connection.

1. Optionally, select **Test Connection** to test the connection.
1. Select **Save**.

   :::image type="content" source="media/how-to-connection/create-snowflake-connection.png" lightbox="media/how-to-connection/create-snowflake-connection.png" alt-text="Screenshot showing creation of a new Snowflake connection in Azure Machine Learning studio.":::

### Create an Azure SQL DB connection

1. In your [Azure Machine Learning studio](https://ml.azure.com) workspace, select **Data** under **Assets** in the left navigation menu.
1. On the **Data** page, select the **Data Connection** tab, and then select **Connect**.
1. In the **Create connection** pane, fill in the following information:

   - **Service**: Select **AzureSqlDb**.
   - **Target**: Provide the following information, using the values from your Azure SQL database for the placeholders:<br>**Server=tcp:\<server>,\<port>;Database=\<database>;Trusted_Connection=False;Encrypt=True;Connection Timeout=30**
   - **Authentication type**: Select **Username password**.
   - **Username**: Enter your Azure SQL DB username.
   - **Password**: Enter your Azure SQL DB password.
   - **Connection name**: Enter a name for the Azure SQL DB connection.

1. Optionally, select **Test Connection** to test the connection.
1. Select **Save**.

   :::image type="content" source="media/how-to-connection/how-to-create-azuredb-connection.png" lightbox="media/how-to-connection/how-to-create-azuredb-connection.png" alt-text="Screenshot showing creation of a new Azure DB connection in Azure Machine Learning studio UI.":::

### Create an Amazon S3 connection

1. In your [Azure Machine Learning studio](https://ml.azure.com) workspace, select **Data** under **Assets** in the left navigation menu.
1. On the **Data** page, select the **Data Connection** tab, and then select **Connect**.
1. In the **Create connection** pane, fill in the following information:

   - **Service**: Select **S3**.
   - **Target**: Enter your Amazon S3 bucket name.
   - **Authentication type**: Select **Access key**.
   - **Access key ID**: Enter your Amazon S3 access key ID.
   - **Secret Access Key**: Enter your Amazon S3 Secret Access Key.
   - **Connection name**: Enter a name for the Amazon S3 connection.

1. Optionally, select **Test Connection** to test the connection.
1. Select **Save**.

   :::image type="content" source="media/how-to-connection/how-to-create-amazon-s3-connection.png" lightbox="media/how-to-connection/how-to-create-amazon-s3-connection.png" alt-text="Screenshot showing creation of a new Amazon S3 connection in Azure Machine Learning studio UI.":::

### Create nondata connections in the studio

1. Navigate to the [Azure Machine Learning studio](https://ml.azure.com/).

1. Under **Manage** in the left navigation, select **Connections** and then select **Create**.

   :::image type="content" source="media/how-to-connection/how-to-manage-connections-create.png" lightbox="media/how-to-connection/create-new-data-connection.png" alt-text="Screenshot showing the start of creating a new connection in Azure Machine Learning studio UI.":::

What type of resource do you want to connect?
1. Under **Other resources types**, select **Generic Container Registry**.
   :::image type="content" source="media/how-to-connection/how-to-connect-generic-container-registry.png" lightbox="media/how-to-connection/create-new-data-connection.png" alt-text="Screenshot highlighting the option to connect to a generic container registry in Azure Machine Learning studio UI.":::

1. Input the required information, and then select **Add connection**.
   :::image type="content" source="media/how-to-connection/how-to-connect-add-connection.png" lightbox="media/how-to-connection/create-new-data-connection.png" alt-text="Screenshot showing the input fields for connecting to a generic container registry in Azure Machine Learning studio UI.":::

## Related content

- [Import data assets](how-to-import-data-assets.md)
- [Schedule data import jobs](how-to-schedule-data-import.md)
