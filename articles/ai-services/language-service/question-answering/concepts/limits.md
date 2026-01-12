---
title: Limits and boundaries - custom question answering
description: Custom question answering has meta-limits for parts of the knowledge base and service. It's important to keep your knowledge base within those limits in order to test and publish.
ms.service: azure-ai-language
author: laujan
ms.author: lajanuar
ms.topic: limits-and-quotas
ms.date: 12/11/2025
---

# Project limits and boundaries

The following custom question answering limits are a combination of the [Azure AI Search pricing tier limits](/azure/search/search-limits-quotas-capacity) and custom question answering limits. Both sets of limits affect how many projects you can create per resource and how large each project can grow.

## Projects

The maximum number of projects is based on [Azure AI Search tier limits](/azure/search/search-limits-quotas-capacity).

Choose the appropriate [Azure search SKU](https://azure.microsoft.com/pricing/details/search/) for your scenario. Typically, you decide the number of projects you need based on number of different subject domains. One subject domain (for a single language) should be in one project.

With custom question answering, you have a choice to set up your language resource in a single language or multiple languages. 
  > [!IMPORTANT]
  > You can publish N-1 projects with a single language resource or N-2 projects with multiple language resources in a single tier. The `N` notation is the maximum indexes allowed in the tier.
  > Also check the maximum size and the number of documents allowed per tier.

For example, if your tier has 15 allowed indexes, you can publish 14 projects of the same language (one index per published project). The 15th index is used for all the projects for authoring and testing. If you choose to have projects in different languages, then you can only publish seven projects.


## Extraction limits

### File naming constraints

File names may not include the following characters:

|Don't use character|
|--|
|Single quote `'`|
|Double quote `"`|

### Maximum file size

|Format|Max file size (MB)|
|--|--|
|`.docx`|10|
|`.pdf`|25|
|`.tsv`|10|
|`.txt`|10|
|`.xlsx`|3|

### Maximum number of files

> [!NOTE]
> Custom question answering currently has no limits on the number of sources that can be added. Throughput is currently capped at 10 text records per second for both management APIs and prediction APIs.
> If you use the F0 tier, upload is limited to three files.

### Maximum number of deep-links from URL

The maximum number of deep-links that can be crawled for extraction of question answer pairs from a URL page is **20**.

## Metadata limits

Metadata is presented as a text-based `key:value` pair, such as `product:windows 10`. Metadata is stored and compared in lower case. The maximum number of metadata fields is based on your **[Azure AI Search tier limits](/azure/search/search-limits-quotas-capacity)**.

If you choose to projects with multiple languages in a single language resource, there's a dedicated test index per project. So the limit is applied per project in Azure Language.

|**Azure AI Search tier** | **Free** | **Basic** |**S1** | **S2**| **S3** |**S3 HD**|
|---|---|---|---|---|---|----|
|Maximum metadata fields per Language (per project)|1,000|100*|1,000|1,000|1,000|1,000|

If you don't choose the option to have projects with multiple different languages, then the limits are applied across all projects in Azure Language.

|**Azure AI Search tier** | **Free** | **Basic** |**S1** | **S2**| **S3** |**S3 HD**|
|---|---|---|---|---|---|----|
|Maximum metadata fields per Language (across all projects)|1,000|100*|1,000|1,000|1,000|1,000|

### By name and value

The length and acceptable characters for metadata name and value are listed in the following table.

|Item|Allowed chars|Regex pattern match|Max chars|
|--|--|--|--|
|Name (key)|Allows<br>Alphanumeric (letters and digits)<br>`_` (underscore)<br> Must not contain spaces.|`^[a-zA-Z0-9_]+$`|100|
|Value|Allows everything except<br>`:` (colon)<br>`|` (vertical pipe)<br>Only one value allowed.|`^[^:|]+$`|500|
|||||

## Project content limits
Overall limits on the content in the project:
* Length of answer text: 25,000 characters
* Length of question text: 1,000 characters
* Length of metadata key text: 100 characters
* Length of metadata value text: 500 characters
* Supported characters for metadata name: Alphabets, digits, and `_`
* Supported characters for metadata value: All except `:` and `|`
* Length of file name: 200
* Supported file formats: ".tsv", ".pdf", ".txt", ".docx", ".xlsx".
* Maximum number of alternate questions: 300
* Maximum number of question-answer pairs: Depends on the **[Azure AI Search tier](/azure/search/search-limits-quotas-capacity#document-limits)** chosen. A question and answer pair maps to a document on Azure AI Search index.
* URL/HTML page: 1 million characters

## Create project call limits:

The limits for each create project action, that is, selecting *Create new project* or calling the REST API to create a project are as follows:

* Recommended maximum number of alternate questions per answer: 300
* Maximum number of URLs: 10
* Maximum number of files: 10
* Maximum number of QnAs permitted per call: 1000

## Update project call limits

The limits for each update action, that is, selecting *Save* or calling the REST API with an update request are as follows:

* Length of each source name: 300
* Recommended maximum number of alternate questions added or deleted: 300
* Maximum number of metadata fields added or deleted: 10
* Maximum number of URLs that can be refreshed: 5
* Maximum number of QnAs permitted per call: 1000

## Add unstructured file limits

> [!NOTE]
> * If you need to use larger files than the limit allows, you can break the file into smaller files before sending them to the API.

The limits when unstructured files are used to *Create new project* or call the REST API to create a project are as follows:

* Length of file: The service extracts the first 32,000 characters.
* Maximum three responses per file.

## Prebuilt custom question answering limits

> [!NOTE]
> * A document is a single string of text characters.
> * To use larger documents than the limit allows, you can break the text into smaller chunks before sending them to the API.

The limits when the REST API is used to answer a question without having to create a project is as follows:

* Number of documents: 5
* Maximum size of a single document:  5,120 characters
* Maximum three responses per document.
