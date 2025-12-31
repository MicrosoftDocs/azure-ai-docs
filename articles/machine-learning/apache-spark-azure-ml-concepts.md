---
title: "Apache Spark in Azure Machine Learning"
titleSuffix: Azure Machine Learning
description: This article explains the available options to access Apache Spark in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: concept-article
author: s-polly
ms.author: scottpolly 
ms.reviewer: soumyapatro
ms.date: 11/13/2025
ms.custom: cliv2, sdkv2, build-2023
#Customer intent: As a full-stack machine learning pro, I want to use Apache Spark in Azure Machine Learning.
---

# Apache Spark in Azure Machine Learning

Azure Machine Learning integration with Azure Synapse Analytics provides easy access to distributed computation resources through the Apache Spark framework. This integration offers these Apache Spark computing experiences:

- Serverless Spark compute
- Attached Synapse Spark pool

## Serverless Spark compute

With the Apache Spark framework, Azure Machine Learning serverless Spark compute is the easiest way to accomplish distributed computing tasks in the Azure Machine Learning environment. Azure Machine Learning offers a fully managed, serverless, on-demand Apache Spark compute cluster. You don't need to create both an Azure Synapse workspace and a Synapse Spark pool.

You can define resources, including instance type and the Apache Spark runtime version. Use those resources to access serverless Spark compute in Azure Machine Learning notebooks for:

- [Interactive Spark code development](./interactive-data-wrangling-with-apache-spark-azure-ml.md)
- [Running machine learning pipelines with a Spark component](./how-to-submit-spark-jobs.md#spark-component-in-a-pipeline-job)
- [Spark batch job submissions](./how-to-submit-spark-jobs.md)

### Points to consider

Serverless Spark compute works well for most user scenarios that require quick access to distributed computing resources through Apache Spark. However, to make an informed decision, consider the advantages and disadvantages of this approach.

Advantages:
  
- No dependencies on creation of other Azure resources for Apache Spark (Azure Synapse infrastructure operates under the hood).
- No required subscription permissions to create Azure Synapse-related resources.
- No need for SQL pool quotas.

Disadvantages:

- No persistent Hive metastore. Serverless Spark compute supports only in-memory Spark SQL.
- No available tables or databases.
- No Azure Purview integration.
- No available linked services.
- Fewer data sources and connectors.
- No pool-level configuration.
- No pool-level library management.
- Only partial support for `mssparkutils`.

### Network configuration

To use network isolation with Azure Machine Learning and serverless Spark compute, use a [managed virtual network](how-to-managed-network.md).

### Inactivity periods and tear-down mechanism

At first launch, a serverless Spark compute (*cold start*) resource might need three to five minutes to start the Spark session itself. This delay happens because the automated serverless Spark compute resource, backed by Azure Synapse, needs time to provision. After the serverless Spark compute is provisioned and an Apache Spark session starts, subsequent code executions (*warm start*) don't experience this delay.

The Spark session configuration offers an option that defines a session timeout (in minutes). The Spark session ends after an inactivity period that exceeds the user-defined timeout. If another Spark session doesn't start in the following 10 minutes, the system tears down the resources provisioned for the serverless Spark compute.

After the system tears down the serverless Spark compute resource, submission of the next job requires a *cold start*. The following visualization shows some session inactivity period and cluster teardown scenarios.

:::image type="content" source="./media/apache-spark-azure-ml-concepts/spark-session-timeout-teardown.png" lightbox="./media/apache-spark-azure-ml-concepts/spark-session-timeout-teardown.png" alt-text="Expandable diagram that shows scenarios for Apache Spark session inactivity period and cluster teardown.":::

### Session-level Conda packages
A Conda dependency YAML file can define many session-level Conda packages in a session configuration. A session times out if it needs more than 15 minutes to install the Conda packages defined in the YAML file. Check whether a required package is already available in the Azure Synapse base image. To do this, visit these resources to determine *packages available in the base image for* the Apache Spark version in use:
- [Azure Synapse Runtime for Apache Spark 3.5](https://github.com/microsoft/synapse-spark-runtime/tree/main/Synapse/spark3.5)
- [Azure Synapse Runtime for Apache Spark 3.4](https://github.com/microsoft/synapse-spark-runtime/tree/main/Synapse/spark3.4)
- [Azure Synapse Runtime for Apache Spark 3.3](https://github.com/microsoft/synapse-spark-runtime/tree/main/Synapse/spark3.3)


> [!NOTE]
> For a session-level Conda package:
> - The *Cold start* needs about 10 to 15 minutes.
> - The *Warm start*, using same Conda package, needs about one minute.
> - The *Warm start*, with a different Conda package, needs about 10 to 15 minutes.
> - If you install a large package, or a package that needs a long installation time, it might impact the Spark instance startup time.
> - Alteration of the PySpark, Python, Scala/Java, .NET, or Spark version isn't supported.
> - Docker images aren't supported.

### Improving session cold start time while using session-level Conda packages
Set the `spark.hadoop.aml.enable_cache` configuration variable to `true` to improve the Spark session *cold start* time. With session-level Conda packages, the session *cold start* typically takes 10 to 15 minutes when the session starts for the first time. However, subsequent session *cold starts* take three to five minutes. Define the configuration variable in the **Configure session** user interface, under **Configuration settings**.

:::image type="content" source="./media/apache-spark-azure-ml-concepts/spark-session-enable-cache.png" lightbox="./media/apache-spark-azure-ml-concepts/spark-session-enable-cache.png" alt-text="Expandable diagram that shows the Spark session configuration tag that enables cache.":::

## Attached Synapse Spark pool

When you create a Spark pool in an Azure Synapse workspace, you can access it in the Azure Machine Learning workspace with the attached Synapse Spark pool. This option is good for users who want to reuse an existing Synapse Spark pool.

To attach a Synapse Spark pool to an Azure Machine Learning workspace, you need to complete [more steps](./how-to-manage-synapse-spark-pool.md) before you can use the pool in Azure Machine Learning for:

- [Interactive Spark code development](./interactive-data-wrangling-with-apache-spark-azure-ml.md)
- [Spark batch job submission](./how-to-submit-spark-jobs.md)
- [Running machine learning pipelines with a Spark component](./how-to-submit-spark-jobs.md#spark-component-in-a-pipeline-job)

An attached Synapse Spark pool provides access to native Azure Synapse features. You're responsible for provisioning, attaching, configuring, and managing the Synapse Spark pool.

The Spark session configuration for an attached Synapse Spark pool also offers an option to define a session timeout (in minutes). The session timeout behavior resembles the description in [the previous section](#inactivity-periods-and-tear-down-mechanism), except that the associated resources are never torn down after the session timeout.

## Defining Spark cluster size

In Azure Machine Learning Spark jobs, you can define the Spark cluster size with three parameter values:

- Number of executors
- Executor cores
- Executor memory

Consider an Azure Machine Learning Apache Spark executor as equivalent to Azure Spark worker nodes. An example can explain these parameters. If you define the number of executors as 6 (equivalent to six worker nodes), the number of executor cores as 4, and executor memory as 28 GB, your Spark job has access to a cluster with 24 cores in total and 168 GB of memory.

## Ensuring resource access for Spark jobs

To access data and other resources, a Spark job can use either a managed identity or a user identity passthrough. This table summarizes the mechanisms that Spark jobs use to access resources.

|Spark pool|Supported identities|Default identity|
| ---------- | -------------------- | ---------------- |
|Serverless Spark compute|User identity, user-assigned managed identity attached to the workspace|User identity|
|Attached Synapse Spark pool|User identity, user-assigned managed identity attached to the attached Synapse Spark pool, system-assigned managed identity of the attached Synapse Spark pool|System-assigned managed identity of the attached Synapse Spark pool|

[This article](./apache-spark-environment-configuration.md#ensuring-resource-access-for-spark-jobs) describes resource access for Spark jobs. In a notebook session, both the serverless Spark compute and the attached Synapse Spark pool rely on user identity passthrough for data access during [interactive data wrangling](./interactive-data-wrangling-with-apache-spark-azure-ml.md).

> [!NOTE]
> - To ensure successful Spark job execution, assign **Contributor** and **Storage Blob Data Contributor** roles (on the Azure storage account used for data input and output) to the identity that you use for the Spark job submission.
> - If an [attached Synapse Spark pool](./how-to-manage-synapse-spark-pool.md) points to a Synapse Spark pool in an Azure Synapse workspace, and that workspace has an associated managed virtual network, [configure a managed private endpoint to a storage account](/azure/synapse-analytics/security/connect-to-a-secure-storage-account). This configuration helps ensure data access.

## Next steps

- [Attach and manage a Synapse Spark pool in Azure Machine Learning](./how-to-manage-synapse-spark-pool.md)
- [Interactive data wrangling with Apache Spark in Azure Machine Learning](./interactive-data-wrangling-with-apache-spark-azure-ml.md)
- [Submit Spark jobs in Azure Machine Learning](./how-to-submit-spark-jobs.md)
- [Code samples for Spark jobs using the Azure Machine Learning CLI](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/spark)
- [Code samples for Spark jobs using the Azure Machine Learning Python SDK](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/spark)
