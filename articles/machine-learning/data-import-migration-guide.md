---
title: Migrate Data Import to Microsoft Fabric
description: Migrate from Data Import and Data Connections in Azure Machine Learning to Microsoft Fabric Pipelines, Shortcuts, or mirroring.
#customer intent: As a data engineer, I want to migrate external data into the Azure ecosystem using Fabric pipelines so that I can integrate with multiple data sources efficiently.
author: s-polly
ms.author: scottpolly
ms.date: 02/23/2026
ms.topic: concept-article
ms.service: azure-machine-learning
ms.subservice: mldata
ms.collection: ce-skilling-fresh-tier2, ce-skilling-ai-copilot
ai-usage: ai-assisted
---

# Migrate Data Import to Microsoft Fabric

Data Import (Preview) and Data Connections (Preview) are features in Azure Machine Learning that let you bring external data into your machine learning workflows. These features are scheduled for retirement `[TO VERIFY: retirement date]`. To continue accessing external data, migrate to Microsoft Fabric.

In this article, you learn about the recommended migration paths from Data Import and Data Connections to Microsoft Fabric, and how to connect your Fabric data back to Azure Machine Learning datastores.

## Deprecation timeline

> [!IMPORTANT]
> Data Import (Preview) and Data Connections (Preview) are scheduled for retirement on `[TO VERIFY: date]`. Plan your migration before this date to avoid disruption to your data workflows.

The following table summarizes what to expect during and after the migration period:

| Milestone | Details |
|-----------|---------|
| Deprecation announced | `[TO VERIFY: date]` |
| Feature retirement | `[TO VERIFY: date]` |
| Existing import jobs | Stop running after retirement `[TO VERIFY]` |
| Replacement | Microsoft Fabric Pipelines, Shortcuts, and mirroring |

After retirement, existing Data Import schedules and Data Connections stop functioning. Migrate to Fabric before the retirement date to maintain uninterrupted access to your external data.

## Migration options

Microsoft Fabric supports more than 170 data source connectors. You can bring external data into Fabric by using one of the following options:

- **Fabric Pipelines** — Copy data to OneLake on a schedule. Pipelines support batch ETL workflows from sources like Snowflake, Amazon S3, and Azure SQL Database. For more information, see:
  - [Snowflake connector overview](/fabric/data-factory/connector-snowflake-overview)
  - [Amazon S3 connector overview](/fabric/data-factory/connector-amazon-s3-overview)
  - [Azure SQL Database connector overview](/fabric/data-factory/connector-azure-sql-database-overview)

- **Snowflake mirroring** — Access Snowflake data in OneLake in near real-time without building a pipeline. For more information, see [Mirrored databases from Snowflake](/fabric/mirroring/snowflake).

- **OneLake shortcuts** — Reference data in Amazon S3 or Azure storage without copying it. Shortcuts provide direct access with no data movement. For more information, see [Create an Amazon S3 shortcut](/fabric/onelake/create-s3-shortcut).

## Choose a migration option

The best option depends on your data source, latency requirements, and whether you need to copy data or reference it in place.

| Option | Best for | Data movement | Latency | Supported sources |
|--------|----------|---------------|---------|-------------------|
| Fabric Pipelines | Scheduled batch ETL from any source | Copies data to OneLake | Depends on schedule | 170+ connectors |
| Snowflake mirroring | Near real-time access to Snowflake | Mirrors data in OneLake | Near real-time | Snowflake only |
| OneLake shortcuts | Referencing data without copying | No data movement | Direct access | Amazon S3, Azure Data Lake Storage Gen2 |

Use the following guidance to select your migration path:

- **Choose Fabric Pipelines** when you need scheduled batch transfers from any of the 170+ supported sources, or when you need to transform data before it reaches OneLake.
- **Choose Snowflake mirroring** when you need near real-time access to Snowflake data and want to avoid managing pipeline schedules.
- **Choose OneLake shortcuts** when you want to reference data in Amazon S3 or Azure storage without copying it, and your tools can read from OneLake directly.

## Connect Fabric data to Azure Machine Learning

After your data is in Fabric, connect it to Azure Machine Learning by using one of these options:

- **OneLake datastore** — Create an Azure Machine Learning OneLake datastore to reference data directly in Fabric. This option avoids an extra copy step and keeps your data in one location. For more information, see [OneLake connection YAML reference](reference-yaml-connection-onelake.md).

- **Copy to Azure storage** — Create a Fabric pipeline to copy data to Azure Blob Storage or Azure Data Lake Storage Gen2, then create the corresponding Azure Machine Learning datastore to reference the copied data. This option is useful when your downstream tools require data in Azure storage. For more information, see [Create datastores](how-to-datastore.md).

## Related content

- [Create datastores](how-to-datastore.md)
- [Read and write data in a job](how-to-read-write-data-v2.md)
- [Import data assets](how-to-import-data-assets.md)
- [Use batch endpoints in Fabric](how-to-use-batch-fabric.md)
- [Microsoft Fabric Pipelines overview](/fabric/data-factory/activity-overview)
- [OneLake shortcuts overview](/fabric/onelake/onelake-shortcuts)
