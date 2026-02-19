---
title: "Managed feature store tutorial 1: Develop and register a feature set"
titleSuffix: Azure Machine Learning
description: Learn how to develop and register a feature set, the first tutorial in a series on using managed feature store in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: tutorial
author: s-polly
ms.author: scottpolly
ms.date: 01/27/2026
ms.reviewer: seramasu
ms.custom:
  - sdkv2
  - build-2023
  - ignite-2023
  - update-code2
  - sfi-image-nochange
#Customer intent: As a data scientist, I want to learn about the managed feature store so I can build and deploy a model with Azure Machine Learning by using Python and CLI or Python SDKs only in a notebook.
---

# Managed feature store tutorial 1: Develop and register a feature set

In this tutorial series, you learn how to use the managed feature store to discover, create, and operationalize Azure Machine Learning features. Features seamlessly integrate the prototyping, training, and operationalization phases of the machine learning lifecycle.

In the prototyping phase, you experiment with various features, and in the operationalization phase, you deploy models that use inference steps to look up feature data. Features serve as the connective tissue in the lifecycle.

You use an Azure Machine Learning project workspace to train inference models by using features from feature stores. Many project workspaces can share and reuse the same feature store. For more information about managed feature store, see [What is managed feature store](concept-what-is-managed-feature-store.md) and [Understand top-level entities in managed feature store](concept-top-level-entities-in-managed-feature-store.md).

## Prerequisites

* An Azure Machine Learning workspace. For more information about workspace creation, see [Quickstart: Create workspace resources](./quickstart-create-resources.md).
* Owner role on the resource group where the feature store is created.

## SDK + CLI or SDK-only tutorial tracks

This tutorial series uses an Azure Machine Learning Spark notebook for development. You can choose between two tracks to complete the tutorial series, depending on your needs.

- The SDK + CLI track uses the Python SDK for feature set development and testing, and uses Azure CLI for create, read, update, and delete (CRUD) operations. This track is useful for continuous integration and continuous delivery (CI/CD) or GitOps scenarios that use CLI and YAML.

- The SDK-only track uses only Python SDKs. This track offers pure, Python-based development and deployment.

You select a track by opening the notebook in either the **cli_and_sdk** or **sdk_only** folder of your cloned notebook. Follow the instructions in the corresponding tab in the tutorials.

#### [SDK + CLI](#tab/SDK-and-CLI-track)

The SDK + CLI track uses the Azure CLI for CRUD operations and the feature store core SDK for feature set development and testing. This approach is useful for GitOps or CI/CD scenarios that use CLI and YAML. The *conda.yml* file you upload installs these resources.

- The CLI is used for CRUD operations on feature stores, feature sets, and feature store entities.
* The feature store core SDK `azureml-featurestore` is for feature set development and consumption. The SDK performs the following operations:

  * Lists or gets a registered feature set.
  * Generates or resolves a feature retrieval specification.
  * Executes a feature set definition to generate a Spark DataFrame.
  * Generates training by using point-in-time joins.

#### [SDK-only](#tab/SDK-track)

The SDK-only track uses two SDKs. The *conda.yml* file you upload installs these SDKs.

- The feature store CRUD SDK is the same `azure-ai-ml` SDK that you use with the Azure Machine Learning workspace. A feature store is implemented as a type of workspace. Feature stores, feature sets, and feature store entities use this SDK for CRUD operations.

- The feature store core SDK `azureml-featurestore` is for feature-set development and consumption. The SDK performs the following operations:

  * Develops a feature set specification.
  * Retrieves feature data.
  * Lists or gets a registered feature set.
  * Generates and resolves feature retrieval specifications.
  * Generates training and inference data by using point-in-time joins.

---

## Tutorial 1: Develop and register a feature set

This first tutorial walks through creating a feature set specification with custom transformations. You then use that feature set to generate training data, enable materialization, and perform a backfill. You learn how to:

> [!div class="checklist"]
> * Create a new, minimal feature store resource.
> * Develop and locally test a feature set with feature transformation capability.
> * Register a feature store entity with the feature store.
> * Register the feature set that you developed with the feature store.
> * Generate a sample training DataFrame by using the features you created.
> * Enable offline materialization on the feature sets, and backfill the feature data.

<a name="prepare-the-notebook-environment"></a>
## Clone the notebook

1. In Azure Machine Learning studio, select **Notebooks** on the left navigation menu, and then select the **Samples** tab on the **Notebooks** page.
1. Expand the **SDK v2** > **sdk** > **python** folders, right-click the **featurestore_sample** folder, and select **Clone**.

   :::image type="content" source="media/tutorial-get-started-with-feature-store/clone-featurestore-example-notebooks.png" alt-text="Screenshot that shows selection of the sample directory in Azure Machine Learning studio.":::

1. On the **Select target directory** pane, make sure **Users** > **\<your_username>** > **featurestore_sample** appears, and select **Clone**. The **featurestore_sample** clones to your workspace user directory.
1. Go to your cloned notebook on the **Files** tab of the **Notebook** page, and expand **Users** > **\<your_username>** > **featurestore_sample** > **project** > **env**.
1. Right-click the **conda.yml** file and select **Download** to download it to your computer, so you can later upload it to the server environment.

   :::image type="content" source="media/tutorial-get-started-with-feature-store/download-conda-file.png" alt-text="Screenshot that shows selection of the Conda YAML file in Azure Machine Learning studio.":::

## Prepare and start the notebook

1. On the left pane in the **Files** tab, expand **featurestore_sample** > **notebooks** > **sdk_and_cli** or **sdk_only**, depending on the track you want to run.
1. Open the first chapter of the tutorial by selecting it.
1. In the upper right area of the **Notebook** page, select the dropdown arrow next to **Compute**, and select **Serverless Spark Compute - Available**. It might take a minute or two to attach the compute.
1. On the top bar above the notebook file, select **Configure session**.

   :::image type="content" source="media/tutorial-get-started-with-feature-store/open-configure-session.png" lightbox="media/tutorial-get-started-with-feature-store/open-configure-session.png" alt-text="Screenshot that shows selections for configuring a session for a notebook.":::

1. On the **Configure session** screen, select **Python packages** on the left pane.
1. Select **Upload conda file**, and under **Select conda file**, browse to and open the *conda.yml* file you downloaded.
1. Optionally, select **Settings** in the left pane and increase the **Session timeout** length to help prevent the serverless Spark startup time from timing out.
1. Select **Apply**.

   :::image type="content" source="media/tutorial-get-started-with-feature-store/upload-conda-file.png" alt-text="Screenshot that shows the Conda file upload.":::

### Start the notebook

#### [SDK + CLI](#tab/SDK-and-CLI-track)

1. Scroll down in the notebook until you reach the first cell, and run it to start the session. The session can take up to 15 minutes to start.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=start-spark-session)]

1. In the second cell, update the `<your_user_alias>` placeholder with your username. Run the cell to set up the root directory for the sample.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=root-dir)]

1. Run the next cell to install the Azure Machine Learning CLI extension.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=install-ml-ext-cli)]

1. Run the next cell to authenticate to Azure CLI.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=auth-cli)]

1. Run the next cell to set the default Azure subscription.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=set-default-subs-cli)]

#### [SDK-only](#tab/SDK-track)

1. Scroll down in the notebook until you reach the first cell, and run it to start the session. The session can take up to 15 minutes to start.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=start-spark-session)]

1. In the second cell, update the `<your_user_alias>` placeholder with your username. Run the cell to set up the root directory for the sample.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=root-dir)]

---

## Create a minimal feature store

1. Set feature store parameters, including name, location, and other values. Provide a `<FEATURESTORE_NAME>` and then run the cell.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=fs-params)]

1. Create the feature store.

   ### [SDK and CLI track](#tab/SDK-and-CLI-track)

   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=create-fs-cli)]

   ### [SDK track](#tab/SDK-track)

   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=create-fs)]

 

1. Initialize a feature store core SDK client for Azure Machine Learning. The client is used to develop and consume features.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=init-fs-core-sdk)]

1. Grant your user identity the **AzureML Data Scientist** role on the feature store. Get your Microsoft Entra object ID value from the Azure portal as described in [Find the user object ID](/partner-center/find-ids-and-domain-names#find-the-user-object-id).

1. Run the following cell to assign the **AzureML Data Scientist** role to your user identity, so that it can create resources in the feature store workspace. Replace the `<USER_AAD_OBJECTID>` placeholder with your Microsoft Entra object ID. The permissions might need some time to propagate.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=assign-aad-ds-role-cli)]  

   For more information about access control, see [Manage access control for managed feature store](./how-to-setup-access-control-feature-store.md).

## Prototype and develop a feature set

This notebook uses sample data hosted in a publicly accessible blob container, which you can read into Spark only through a `wasbs` driver. If you create feature sets by using your own source data, host them in an Azure Data Lake Storage account, and use an `abfss` driver in the data path.

### Explore the transactions source data

Build a feature set named `transactions` that has rolling window aggregate-based features.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=explore-txn-src-data)]

### Locally develop the feature set

A feature set specification is a self-contained definition of a feature set that you can locally develop and test. Create the following rolling window aggregate features:

* `transactions three-day count`
* `transactions amount three-day avg`
* `transactions amount three-day sum`
* `transactions seven-day count`
* `transactions amount seven-day avg`
* `transactions amount seven-day sum`

[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=develop-txn-fset-locally)]

Review the feature transformation code file: *featurestore/featuresets/transactions/transformation_code/transaction_transform.py*. Note the rolling aggregation defined for the features. This file is a Spark transformer. For more information about the feature set and transformations, see [What is managed feature store?](./concept-what-is-managed-feature-store.md)

### Export as a feature set specification

To register the feature set specification with the feature store, you save that specification in a specified location and format, which supports source control.
[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=dump-transactions-fs-spec)]

To see the *featurestore/featuresets/accounts/spec/FeaturesetSpec.yaml* specification, open the generated `transactions` feature set specification from the file tree. The specification contains these elements:

* `source`: A reference to a storage resource. In this case, it's a parquet file in a blob storage resource.
* `features`: A list of features and their datatypes. If you provide transformation code, the code must return a DataFrame that maps to the features and datatypes.
* `index_columns`: The join keys required to access values from the feature set.

## Register a feature store entity

Entities help enforce the best practice of using the same join key definition across feature sets that use the same logical entities. Examples of entities include `accounts` and `customers`. Entities are typically created once and then reused across feature sets. To learn more, see [Understand top-level entities in managed feature store](./concept-top-level-entities-in-managed-feature-store.md).

#### [SDK + CLI](#tab/SDK-and-CLI-track)

Create an `account` entity that has the join key `accountID` of type `string`. Register the `account` entity with the feature store.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=register-acct-entity-cli)]

#### [SDK-only](#tab/SDK-track)

`MLClient` is used to create, read, update, and delete a feature store asset. This notebook code cell sample searches for the feature store you created in an earlier step. You can't reuse the same `ml_client` value that you used earlier, because that value is scoped at the resource group level. Proper scoping is essential for feature store creation.

1. Initialize the feature store CRUD client. In the following code sample, the client is scoped at feature store level.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=init-fset-crud-client)]

1. Create an `account` entity that has the join key `accountID` of type `string`. Register the `account` entity with the feature store.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=register-acct-entity)]

---

## Register the feature set with the feature store

The following code registers a feature set asset with the feature store. You can then reuse that asset and easily share it. Registration of a feature set asset offers managed capabilities, including versioning and materialization. Later tutorials in this series cover managed capabilities.

#### [SDK + CLI](#tab/SDK-and-CLI-track)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=register-txn-fset-cli)]

#### [SDK-only](#tab/SDK-track)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=register-txn-fset)]

---

## Explore the feature store UI

Feature store asset creation and updates can happen only through the SDK and CLI. You can use the Machine Learning UI to search or browse through the feature store.

1. Open the [Azure Machine Learning global landing page](https://ml.azure.com/home).
1. Select **Feature stores** on the left pane.
1. From the list of accessible feature stores, select the feature store you created earlier in this tutorial.

## Assign the Storage Blob Data Reader role

The **Storage Blob Data Reader** role must be assigned to your user account to ensure that the user account can read materialized feature data from the offline materialization store.

Get information about the offline materialization store from the feature store UI **Overview** page. The values for the storage account `<SUBSCRIPTION_ID>`, storage account `<RESOURCE_GROUP>`, and `<STORAGE_ACCOUNT_NAME>` for the offline materialization store are located in the **Offline materialization store** card.

   :::image type="content" source="media/tutorial-get-started-with-feature-store/offline-store-information.png" lightbox="media/tutorial-get-started-with-feature-store/offline-store-information.png" alt-text="Screenshot that shows offline store account information on feature store Overview page.":::

#### [SDK + CLI](#tab/SDK-and-CLI-track)

Run the following code cell for role assignment. The permissions might need some time to propagate.
[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=grant-rbac-to-user-identity-cli)]

#### [SDK-only](#tab/SDK-track)

1. Get your Microsoft Entra object ID value from the Azure portal as described in [Find the user object ID](/partner-center/find-ids-and-domain-names#find-the-user-object-id).

1. Run the following code cell for role assignment. The permissions might need some time to propagate.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=grant-rbac-to-user-identity)]

---

For more information about access control, see [Manage access control for managed feature store](how-to-setup-access-control-feature-store.md).

## Generate a training data DataFrame

Generate a training data DataFrame by using the registered feature set.

1. Load observation data captured during the event itself.

   Observation data typically involves the core data used for training and inferencing, which joins with the feature data to create the full training data resource. The following data has core transaction data including transaction ID, account ID, and transaction amount values. Because you use the data for training, it also has an appended target variable `is_fraud`.

   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=load-obs-data)]

1. Get the registered feature set and list its features.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=get-txn-fset)]

   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=print-txn-fset-sample-values)]

1. Select the features to become part of the training data, and use the feature store SDK to generate the training data itself. A point-in-time join appends the features to the training data.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=select-features-and-gen-training-data)]

## Enable offline materialization

Materialization computes the feature values for a feature window and stores those values in a materialization store. All feature queries can then use those values from the materialization store.

Without materialization, a feature set query applies transformations to the source on the fly and computes the features before returning the values. This process works well for the prototyping phase. However, for training and inference operations in a production environment, materializing the features provides greater reliability and availability.

The default blob store for the feature store is an Azure Data Lake Storage (ADLS) container. A feature store is always created with an offline materialization store and a user-assigned managed identity (UAI).

If a feature store is created with parameter default values `offline_store=None` and `materialization_identity=None`, the system performs the following setup:
1. Creates an ADLS container as the offline store.
1. Creates a UAI and assigns it to the feature store as the materialization identity.
1. Assigns required role-based access control (RBAC) permissions to the UAI on the offline store.

Optionally, you can use an existing ADLS container as the offline store by defining the `offline_store` parameter. Only ADLS containers are supported for offline materialization stores.

Optionally, you can provide an existing UAI by defining a `materialization_identity` parameter. The required RBAC permissions are assigned to the UAI on the offline store during the feature store creation.

The following code sample shows the creation of a feature store with user-defined `offline_store` and `materialization_identity` parameters.

```python
   import os
   from azure.ai.ml import MLClient
   from azure.ai.ml.identity import AzureMLOnBehalfOfCredential
   from azure.ai.ml.entities import (
      ManagedIdentityConfiguration,
      FeatureStore,
      MaterializationStore,
   )
   from azure.mgmt.msi import ManagedServiceIdentityClient

   # Get an existing offline store
   storage_subscription_id = "<OFFLINE_STORAGE_SUBSCRIPTION_ID>"
   storage_resource_group_name = "<OFFLINE_STORAGE_RESOURCE_GROUP>"
   storage_account_name = "<OFFLINE_STORAGE_ACCOUNT_NAME>"
   storage_file_system_name = "<OFFLINE_STORAGE_CONTAINER_NAME>"

   # Get ADLS container ARM ID
   gen2_container_arm_id = "/subscriptions/{sub_id}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account}/blobServices/default/containers/{container}".format(
      sub_id=storage_subscription_id,
      rg=storage_resource_group_name,
      account=storage_account_name,
      container=storage_file_system_name,
   )

   offline_store = MaterializationStore(
      type="azure_data_lake_gen2",
      target=gen2_container_arm_id,
   )

   # Get an existing UAI
   uai_subscription_id = "<UAI_SUBSCRIPTION_ID>"
   uai_resource_group_name = "<UAI_RESOURCE_GROUP>"
   uai_name = "<FEATURE_STORE_UAI_NAME>"

   msi_client = ManagedServiceIdentityClient(
      AzureMLOnBehalfOfCredential(), uai_subscription_id
   )

   managed_identity = msi_client.user_assigned_identities.get(
      uai_resource_group_name, uai_name
   )

   # Get UAI information
   uai_principal_id = managed_identity.principal_id
   uai_client_id = managed_identity.client_id
   uai_arm_id = managed_identity.id

   materialization_identity1 = ManagedIdentityConfiguration(
      client_id=uai_client_id, principal_id=uai_principal_id, resource_id=uai_arm_id
   )

   # Create a feature store
   featurestore_name = "<FEATURE_STORE_NAME>"
   featurestore_location = "<AZURE_REGION>"
   featurestore_subscription_id = os.environ["AZUREML_ARM_SUBSCRIPTION"]
   featurestore_resource_group_name = os.environ["AZUREML_ARM_RESOURCEGROUP"]

   ml_client = MLClient(
      AzureMLOnBehalfOfCredential(),
      subscription_id=featurestore_subscription_id,
      resource_group_name=featurestore_resource_group_name,
   )

   # Use existing ADLS Gen2 container and UAI
   fs = FeatureStore(
      name=featurestore_name,
      location=featurestore_location,
      offline_store=offline_store,
      materialization_identity=materialization_identity1,
   )

   fs_poller = ml_client.feature_stores.begin_update(fs)

   print(fs_poller.result()) 
```

After you enable feature set materialization on the transactions feature set, you can perform a backfill. You can also schedule recurrent materialization jobs. For more information, see the third tutorial in this series, [Enable recurrent materialization & run batch inference](tutorial-enable-recurrent-materialization-run-batch-inference.md).

### Set spark.sql.shuffle.partitions in the YAML file

The Spark configuration `spark.sql.shuffle.partitions` is an optional parameter that can affect the number of Parquet files generated per day when the feature set is materialized into the offline store. The default value of this parameter is 200.

As a best practice, avoid generation of many small Parquet files. If offline feature retrieval becomes slow after feature set materialization, open the corresponding folder in the offline store. Check whether the issue involves too many small Parquet files per day, and adjust the value of this parameter according to the feature data size.

> [!NOTE]
> The sample data used in this notebook is small. Therefore, the `spark.sql.shuffle.partitions` parameter is set to `1` in the *featureset_asset_offline_enabled.yaml* file.

#### [SDK + CLI](#tab/SDK-and-CLI-track)
[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=enable-offline-mat-txns-fset-cli)]

You can also save the feature set asset as a YAML resource.

#### [SDK-only](#tab/SDK-track)
[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=enable-offline-mat-txns-fset)]

You can also save the feature set asset as a YAML resource.
   [!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=dump-txn-fset-yaml)]

---

## Backfill data for the transactions feature set

Materialization computes the feature values for a feature window, and stores these computed values in a materialization store. Feature materialization increases the reliability and availability of the computed values. All feature queries now use the values from the materialization store. This step performs a one-time backfill for a feature window of 18 months.

> [!NOTE]
> You might need to determine a backfill data window value. The window must match the window of your training data. For example, to use 18 months of data for training, you must retrieve features for 18 months. This means you should backfill for an 18-month window.

The following code cell materializes data by current status `None` or `Incomplete` for the defined feature window. You can provide a list of more than one data status, for example `["None", "Incomplete"]`, in a single backfill job.

#### [SDK + CLI](#tab/SDK-and-CLI-track)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_and_cli/1.Develop-feature-set-and-register.ipynb?name=backfill-txns-fset-cli)]  

#### [SDK-only](#tab/SDK-track)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=backfill-txns-fset)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=stream-mat-job-logs)]

---

> [!TIP]
> - The `timestamp` column should follow `yyyy-MM-ddTHH:mm:ss.fffZ` format. 
> - The `feature_window_start_time` and `feature_window_end_time` granularity is limited to seconds. Milliseconds in the `datetime` object are ignored.
> - A materialization job is submitted only if data in the feature window matches the `data_status` defined when submitting the job.

Print sample data from the feature set. The output information shows that the data was retrieved from the materialization store. The `get_offline_features()` method retrieves the training and inference data and also uses the materialization store by default.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/featurestore_sample/notebooks/sdk_only/1.Develop-feature-set-and-register.ipynb?name=sample-txns-fset-data)]

## Further explore offline feature materialization

You can explore feature materialization status for a feature set in the **Materialization jobs** UI.

1. Open the [Azure Machine Learning global landing page](https://ml.azure.com/home).
1. Select **Feature stores** on the left pane.
1. From the list of accessible feature stores, select the feature store you performed backfill for.
1. Select the **Materialization jobs** tab.

   :::image type="content" source="media/tutorial-get-started-with-feature-store/feature-set-materialization-ui.png" lightbox="media/tutorial-get-started-with-feature-store/feature-set-materialization-ui.png" alt-text="Screenshot that shows the feature set Materialization jobs UI.":::

Data materialization status can be:

- Complete (green)
- Incomplete (red)
- Pending (blue)
- None (gray)

A *data interval* represents a contiguous portion of data with same data materialization status. For example, the earlier snapshot has 16 data intervals in the offline materialization store. The data can have a maximum of 2,000 data intervals. If your data contains more than 2,000 data intervals, create a new feature set version.

During backfill, a new materialization job is submitted for each data interval that falls within the defined feature window. No job is submitted if a materialization job is already pending or running for a data interval that isn't backfilled.

You can retry a failed materialization job.

> [!NOTE]
> To get the job ID of a failed materialization job:
> 1. Navigate to the feature set **Materialization jobs** UI.
> 1. Select the **Display name** of a specific job with **Status** of **Failed**.
> 1. Under the **Name** property on the job **Overview** page, locate the job ID starting with `Featurestore-Materialization-`.

#### [SDK + CLI](#tab/SDK-and-CLI-track)

```AzureCLI
az ml feature-set backfill --by-job-id <JOB_ID_OF_FAILED_MATERIALIZATION_JOB> --name <FEATURE_SET_NAME> --version <VERSION>  --feature-store-name <FEATURE_STORE_NAME> --resource-group <RESOURCE_GROUP>
```

#### [SDK-only](#tab/SDK-track)

```python

poller = fs_client.feature_sets.begin_backfill(
    name="transactions",
    version=version,
    job_id="<JOB_ID_OF_FAILED_MATERIALIZATION_JOB>",
)
print(poller.result().job_ids)
```

---

### Update an offline materialization store

If an offline materialization store must be updated at the feature store level, all feature sets in the feature store should have offline materialization disabled.

If offline materialization is disabled on a feature set, materialization status of the data already materialized in the offline materialization store resets. The reset renders data that is already materialized unusable. You must resubmit materialization jobs after enabling offline materialization.

## Clean up

The fifth tutorial in this series, [Develop a feature set with a custom source](tutorial-develop-feature-set-with-custom-source.md#clean-up), describes how to delete the resources.

## Next step

This tutorial built the training data with features from the feature store, enabled materialization to offline feature store, and performed a backfill.

The next tutorial in the series, [Experiment and train models by using features](tutorial-experiment-train-models-using-features.md), shows you how to run model training using these features.

## Related content

- [What is managed feature store?](concept-what-is-managed-feature-store.md)
- [Understand top-level entities in managed feature store](concept-top-level-entities-in-managed-feature-store.md).
- [Manage access control for managed feature store](how-to-setup-access-control-feature-store.md).
- [Troubleshoot managed feature store](troubleshooting-managed-feature-store.md).
- [CLI (v2) YAML schemas](reference-yaml-overview.md)
