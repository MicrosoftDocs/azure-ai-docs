---
title: Bing COVID-19
description: Learn how to use the Bing COVID-19 dataset in Azure Open Datasets.
ms.service: azure-open-datasets
ms.topic: sample
ms.reviewer: scottpolly
ms.date: 10/28/2025
---

# Bing COVID-19

Bing COVID-19 data includes confirmed, fatal, and recovered cases from all regions, updated daily. The [Bing COVID-19 Tracker](https://bing.com/covid) reflects this data.

Bing collects data from multiple trusted, reliable sources, including:

- [BNO News](https://bnonews.com/index.php/2020/04/the-latest-coronavirus-cases/)
- [Centers for Disease Control and Prevention (CDC)](https://www.cdc.gov/covid/index.html)
- National/regional and state public health departments
- [Wikipedia](https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic)
- The [World Health Organization (WHO)](https://www.who.int/emergencies/diseases/novel-coronavirus-2019)
- [24/7 Wall St.](https://247wallst.com/)

[!INCLUDE [Open Dataset usage notice](./includes/open-datasets-usage-note.md)]

## Datasets

Modified Bing COVID-19 datasets are available in CSV, JSON, JSON-Lines, and Parquet:

- [CSV](https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.csv)
- [JSON](https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.json)
- [JSON-Lines](https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.jsonl)
- [Parquet](https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.parquet)

All modified datasets have ISO 3166 subdivision codes and load times added. They use lower case column names with underscore separators.

[CSV-format raw data](https://pandemicdatalake.blob.core.windows.net/public/raw/covid-19/bing_covid-19_data/latest/Bing-COVID19-Data.csv)

Earlier versions of modified and raw data are available at [this resource](https://github.com/microsoft/Bing-COVID-19-Data/commits/).

## Data volume
All datasets receive daily updates. As of March 5, 2023 they contained 4,766,737 rows. The dataset is available in these file formats:

- CSV (560.3 MB)
- JSON (1515.6 MB)
- JSONL (1506.2 MB)
- Parquet (55.4 MB)

## License and use rights attribution

The data is available strictly for educational and academic purposes under [these terms and conditions](https://github.com/microsoft/Bing-COVID-19-Data/blob/master/LICENSE.txt). Valid purposes include:

- academic institutions
- government agencies
- medical research

Data used or cited in publications should include an attribution to **'Bing COVID-19 Tracker'**, with a link to [www.bing.com/covid](https://www.bing.com/covid).

## Contact

For any questions or feedback about this or other datasets in the COVID-19 Data Lake contact [askcovid19dl@microsoft.com](mailto:askcovid19dl@microsoft.com).

## Columns

| Name             | Data type | Unique    | Values (sample)                    | Description                                                          |
|------------------|-----------|-----------|------------------------------------|----------------------------------------------------------------------|
| admin_region_1   | string    | 864       | Texas Georgia                      | Region within country_region                                         |
| admin_region_2   | string    | 3,143     | Washington County Jefferson County | Region within admin_region_1                                         |
| confirmed        | int       | 120,692   | 1 2                                | Confirmed case count for the region                                  |
| confirmed_change | int       | 12,120    | 1 2                                | Change of confirmed case count from the previous day                 |
| country_region   | string    | 237       | United States India                | Country/region                                                       |
| deaths           | int       | 20,616    | 1 2                                | Death case count for the region                                      |
| deaths_change    | smallint  | 1,981     | 1 2                                | Change of death count from the previous day                          |
| id               | int       | 1,783,534 | 742546 69019298                    | Unique identifier                                                    |
| iso_subdivision  | string    | 484       | US-TX US-GA                        | Two-part ISO subdivision code                                        |
| iso2             | string    | 226       | US IN                              | 2 letter country code identifier                                     |
| iso3             | string    | 226       | USA IND                            | 3 letter country code identifier                                     |
| latitude         | double    | 5,675     | 42.28708 19.59852                  | Latitude of the centroid of the region                               |
| load_time        | timestamp | 1         | 2021-04-26 00:06:34.719000         | The date and time the file was loaded from the Bing source on GitHub |
| longitude        | double    | 5,693     | -2.5396 -155.5186                  | Longitude of the centroid of the region                              |
| recovered        | int       | 73,287    | 1 2                                | Recovered count for the region                                       |
| recovered_change | int       | 10,441    | 1 2                                | Change of recovered case count from the previous day                 |
| updated          | date      | 457       | 2021-04-23 2021-04-22              | The as at date for the record                                        |

## Preview

| id     | updated    | confirmed | deaths | iso2 | iso3 | country_region | admin_region_1 | iso_subdivision | admin_region_2 | load_time             | confirmed_change | deaths_change |
|--------|------------|-----------|--------|------|------|----------------|----------------|-----------------|----------------|-----------------------|------------------|---------------|
| 338995 | 2020-01-21 | 262       | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM |                  |               |
| 338996 | 2020-01-22 | 313       | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 51               | 0             |
| 338997 | 2020-01-23 | 578       | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 265              | 0             |
| 338998 | 2020-01-24 | 841       | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 263              | 0             |
| 338999 | 2020-01-25 | 1320      | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 479              | 0             |
| 339000 | 2020-01-26 | 2014      | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 694              | 0             |
| 339001 | 2020-01-27 | 2798      | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 784              | 0             |
| 339002 | 2020-01-28 | 4593      | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 1795             | 0             |
| 339003 | 2020-01-29 | 6065      | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 1472             | 0             |
| 339004 | 2020-01-30 | 7818      | 0      | null | null | Worldwide      | null           | null            | null           | 4/26/2021 12:06:34 AM | 1753             | 0             |

## Data access - Azure Notebooks

# [azure-storage](#tab/azure-storage)

<!-- nbstart https://opendatasets-api.azure.com/discoveryapi/OpenDataset/DownloadNotebook?serviceType=AzureNotebooks&package=azure-storage&registryId=bing-covid-19-data -->

> [!NOTE]
> This notebook documents the URLs and sample code to access the [**Bing COVID-19 Dataset**](https://github.com/microsoft/Bing-COVID-19-Data).

Use these URLs to get specific file formats hosted on Azure Blob Storage:

- [CSV](https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.csv)
- [JSON](https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.json)
- [JSON-Lines](https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.jsonl)
- [Parquet](https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.parquet)

Download the dataset file using the built-in capability of Pandas to download from an HTTP URL. Pandas has readers for various file formats:

[pandas.read_parquet](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_parquet.html)

[pandas.read_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)

```python
import pandas as pd
import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt

df = pd.read_parquet("https://pandemicdatalake.blob.core.windows.net/public/curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.parquet")
df.head(10)
```

To verify that the updated column has a datetime format, check the data types of the various fields:

```python
df.dtypes
```

Review the Worldwide data. To visualize the data, build some charts:

```python
df_Worldwide=df[df['country_region']=='Worldwide']
```

```python
df_Worldwide_pivot=df_Worldwide.pivot_table(df_Worldwide, index=['country_region','updated'])

df_Worldwide_pivot
```

```python
df_Worldwide.plot(kind='line',x='updated',y="confirmed",grid=True)
df_Worldwide.plot(kind='line',x='updated',y="deaths",grid=True)
df_Worldwide.plot(kind='line',x='updated',y="confirmed_change",grid=True)
df_Worldwide.plot(kind='line',x='updated',y="deaths_change",grid=True)
```

<!-- nbend -->

# [pyspark](#tab/pyspark)

A sample isn't available for this platform / package combination.

---

## Data Access - Azure Databricks

# [azure-storage](#tab/azure-storage)

A sample isn't available for this platform / package combination.

# [pyspark](#tab/pyspark)

<!-- nbstart https://opendatasets-api.azure.com/discoveryapi/OpenDataset/DownloadNotebook?serviceType=AzureDatabricks&package=pyspark&registryId=bing-covid-19-data -->

```python
# Azure storage access info
blob_account_name = "pandemicdatalake"
blob_container_name = "public"
blob_relative_path = "curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.parquet"
blob_sas_token = r""
```

```python
# Allow SPARK to read from Blob remotely
wasbs_path = 'wasbs://%s@%s.blob.core.windows.net/%s' % (blob_container_name, blob_account_name, blob_relative_path)
spark.conf.set(
  'fs.azure.sas.%s.%s.blob.core.windows.net' % (blob_container_name, blob_account_name),
  blob_sas_token)
print('Remote blob path: ' + wasbs_path)
```

```python
# SPARK read parquet, note that it won't load any data yet by now
df = spark.read.parquet(wasbs_path)
print('Register the DataFrame as a SQL temporary view: source')
df.createOrReplaceTempView('source')
```

```python
# Display top 10 rows
print('Displaying top 10 rows: ')
display(spark.sql('SELECT * FROM source LIMIT 10'))
```

<!-- nbend -->

---

## Data Access - Azure Synapse

# [azure-storage](#tab/azure-storage)

A sample isn't available for this platform / package combination.

# [pyspark](#tab/pyspark)

<!-- nbstart https://opendatasets-api.azure.com/discoveryapi/OpenDataset/DownloadNotebook?serviceType=AzureSynapse&package=pyspark&registryId=bing-covid-19-data -->

```python
# Azure storage access info
blob_account_name = "pandemicdatalake"
blob_container_name = "public"
blob_relative_path = "curated/covid-19/bing_covid-19_data/latest/bing_covid-19_data.parquet"
blob_sas_token = r""
```

```python
# Allow SPARK to read from Blob remotely
wasbs_path = 'wasbs://%s@%s.blob.core.windows.net/%s' % (blob_container_name, blob_account_name, blob_relative_path)
spark.conf.set(
  'fs.azure.sas.%s.%s.blob.core.windows.net' % (blob_container_name, blob_account_name),
  blob_sas_token)
print('Remote blob path: ' + wasbs_path)
```

```python
# SPARK read parquet, note that it won't load any data yet by now
df = spark.read.parquet(wasbs_path)
print('Register the DataFrame as a SQL temporary view: source')
df.createOrReplaceTempView('source')
```

```python
# Display top 10 rows
print('Displaying top 10 rows: ')
display(spark.sql('SELECT * FROM source LIMIT 10'))
```

<!-- nbend -->

---

## Next steps

View the rest of the datasets in the [Open Datasets catalog](./dataset-catalog.md).
