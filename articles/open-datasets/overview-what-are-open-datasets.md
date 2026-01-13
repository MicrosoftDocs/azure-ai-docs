---
title: What are open datasets? Curated public datasets
description: Learn about Azure Open Datasets, curated datasets from the public domain such as weather, census, holidays, and location to enrich predictive solutions.
ms.service: azure-open-datasets
ms.topic: overview
author: s-polly
ms.author: scottpolly
ms.date: 10/28/2025
---

# What are Azure Open Datasets and how can you use them?

[Azure Open Datasets](https://azure.microsoft.com/services/open-datasets/) are curated public datasets that you can add to scenario-specific features to machine learning solutions, for more accurate models. Open Datasets are available in the cloud, on Microsoft Azure. They're integrated into Azure Machine Learning and readily available to Azure Databricks. You can also access the datasets through APIs and you can use them in other products, such as Power BI and Azure Data Factory.

Datasets include public-domain data for weather, census, holidays, public safety, and location that help you train machine learning models and enrich predictive solutions. You can also share your public datasets through Azure Open Datasets.

:::image type="content" source="./media/overview-what-are-open-datasets/open-datasets-components.png" lightbox="./media/overview-what-are-open-datasets/open-datasets-components.png" alt-text="Diagram that shows the Azure Open Datasets service Building blocks.":::

## Curated, prepared datasets

Curated open public datasets in Azure Open Datasets are optimized for consumption in machine learning workflows.

For more information about the available datasets, visit the [Azure Open Datasets Catalog](https://azure.microsoft.com/services/open-datasets/catalog/) resource.

Data scientists often spend most their time cleaning and preparing data for advanced analytics. To save you time, open Datasets are copied to the Azure cloud, and then preprocessed. At regular intervals, data is pulled from the sources - for example, by an FTP connection to the National Oceanic and Atmospheric Administration (NOAA). Next, the data is parsed into a structured format, and then enriched as needed, with features such as ZIP Code or the locations of the nearest weather stations.

Datasets are cohosted with cloud compute in Azure, to make access and manipulation easier.  

Here are examples of available datasets:

### Transportation

|Dataset         | Description                                    |
|----------------|------------------------------------------------|
| [NYC Taxi & Limousine Commission - yellow taxi trip records](dataset-taxi-yellow.md) | The yellow taxi trip records include pick-up and drop-off dates/times, pick-up and drop-off locations, trip distances, itemized fares, rate types, payment types, and driver-reported passenger counts. |
| [NYC Taxi & Limousine Commission - green taxi trip records](dataset-taxi-green.md) | The green taxi trip records include pick-up and drop-off dates/times, pick-up and drop-off locations, trip distances, itemized fares, rate types, payment types, and driver-reported passenger counts. |

## Labor and economics

| Dataset | Description |
|--|--|
| [US Labor Force Statistics](dataset-us-labor-force.md) | US Labor Force Statistics provides Labor Force Statistics, labor force participation rates, and the civilian noninstitutional population by age, gender, race, and ethnic groups in the United States. |
| [US National Employment Hours and Earnings](dataset-us-national-employment-earnings.md) | The Current Employment Statistics (CES) program produces detailed industry estimates of nonfarm employment, hours, and earnings of workers on payrolls in the United States. |

## Access to datasets

With an Azure account, you can access open datasets through code or through the Azure service interface. The data is colocated with Azure cloud compute resources for use in your machine learning solutions.  

Open Datasets are available through the Azure Machine Learning UI and SDK. Open Datasets also provide Azure Notebooks and Azure Databricks notebooks that can connect data to Azure Machine Learning and Azure Databricks. Datasets can also be accessed through a Python SDK.

However, you don't need an Azure account to access Open Datasets; you can access them from any Python environment with or without Spark.

## Request or contribute datasets

If you can't find the data you want, email us to [request a dataset](mailto:aod@microsoft.com?Subject=Request%20dataset%3A%20%3Creplace%20with%20dataset%20name%3E&Body=%0AYour%20name%20and%20institution%3A%20%0A%0ADataset%20name%3A%0A%20%0ADataset%20description%3A%20%0A%3Cfill%20in%20a%20brief%20description%20and%20share%20any%20web%20links%20of%20the%20dataset%3E%20%0A%0ADataset%20size%3A%20%0A%3Chow%20much%20space%20does%20the%20dataset%20need%20today%20and%20how%20much%20is%20it%20expected%20to%20grow%20each%20year%3E%20%0A%0ADataset%20file%20formats%3A%20%0A%3Ccurrent%20dataset%20file%20formats%2C%20and%20optionally%2C%20any%20formats%20that%20the%20dataset%20must%20be%20transformed%20to%20for%20easy%20access%3E%0A%0ALicense%3A%20%0A%3Cwhat%20is%20the%20license%20or%20terms%20and%20conditions%20governing%20the%20distribution%20of%20this%20dataset%3E%0A%0AUse%20cases%3A%20%0A%3CExplain%20some%20common%20use%20of%20the%20dataset.%20E.g.%20weather%20dataset%20can%20be%20useful%20in%20demand%20forecasting%20and%20predictive%20maintenance%20scenarios%3E%20%0A%0AAny%20additional%20information%20you%20want%20us%20to%20know%3A%0A) or [contribute a dataset](mailto:aod@microsoft.com?Subject=Contribute%20dataset%3A%20%3Creplace%20with%20dataset%20name%3E&Body=%0AYour%20name%20and%20institution%3A%20%0A%0ADataset%20name%3A%0A%20%0ADataset%20description%3A%20%0A%3Cfill%20in%20a%20brief%20description%20and%20share%20any%20web%20links%20of%20the%20dataset%3E%20%0A%0ADataset%20size%3A%20%0A%3Chow%20much%20space%20does%20the%20dataset%20need%20today%20and%20how%20much%20is%20it%20expected%20to%20grow%20each%20year%3E%20%0A%0ADataset%20file%20formats%3A%20%0A%3Ccurrent%20dataset%20file%20formats%2C%20and%20optionally%2C%20any%20formats%20that%20the%20dataset%20must%20be%20transformed%20to%20for%20easy%20access%3E%0A%0ALicense%3A%20%0A%3Cwhat%20is%20the%20license%20or%20terms%20and%20conditions%20governing%20the%20distribution%20of%20this%20dataset%3E%0A%0AUse%20cases%3A%20%0A%3CExplain%20some%20common%20use%20of%20the%20dataset.%20E.g.%20weather%20dataset%20can%20be%20useful%20in%20demand%20forecasting%20and%20predictive%20maintenance%20scenarios%3E%20%0A%0AAny%20additional%20information%20you%20want%20us%20to%20know%3A%0A). 

## Next steps
* [Azure Open Datasets Catalog](https://azure.microsoft.com/services/open-datasets/catalog/)
* [Python SDK for Open Datasets](/python/api/azureml-opendatasets/azureml.opendatasets)
