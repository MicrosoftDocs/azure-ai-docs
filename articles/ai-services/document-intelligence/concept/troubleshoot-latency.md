---
title: Troubleshoot latency issues with Document Intelligence API
titleSuffix: Azure AI services
description: Learn troubleshooting tips, remedial solutions, and best practices to address Document Intelligence latency issues.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: troubleshooting
ms.date: 02/03/2025
ms.author: lajanuar
---

# Troubleshooting latency issues in Azure AI Document Intelligence

This article presents troubleshooting tips, remedial solutions, and best practices to address Document Intelligence latency issues. Your applications can encounter latency with using the Document Intelligence service. Latency refers to the duration an API server takes to handle and process an incoming request before delivering the response to the client. The time required to analyze a document varies based on its size (such as the number of pages) and the content on each page. Document Intelligence operates as a multitenant service, ensuring that latency for similar documents is generally comparable, though not always identical. Variability in latency and performance is an inherent characteristic of any microservice-based, stateless, asynchronous service, especially when processing images and large documents on a large scale. Despite continuous efforts to increase hardware capacity and enhance scalability, some latency issues can still arise during runtime.

> [!NOTE]
> Azure AI services doesn't offer a Service Level Agreement (SLA) for latency.
> The asynchronous nature of the API allows you to retrieve results for up to 24 hours after the operation is sent to our backend with the request Id returned by the POST operation. If you are unable to retrieve the result within your normal polling sequence, store the request Id and attempt at a different time before retrying. Please refer to our service page for more guidance.

## Check Azure region status

If you're experiencing latency issues, the first to check [Azure status](https://azure.status.microsoft/status) to determine whether there is an ongoing outage or issue impacting your services.

* All active events are listed under the `Current Impact` tab.

* You can also check your resource in the host region. Go to Geography → Products And Services → AI + Machine Learning → Azure AI Document Intelligence and check the status for your region:

   :::image type="content" source="../media/latency/azure-status.png" alt-text="Screenshot of the Microsoft Azure status page" lightbox="../media/azure-status.png":::

## Check file size

The size of the files you may be sending through the request API. The service parallelizes processing, larger files can lead to longer processing time. Please normalize your measurement as latency per page. Consider raising the issue if you see sustained periods (more than an hour) with latency per page consistently being above 15s.

## Check Azure Blob storage latency

Latency in Azure Storage operations is affected by the size of the request. Larger operations take more time to complete due to the increased volume of data transferred over the network and processed by Azure Storage.

Azure Storage provides two latency metrics for block blobs in the Azure portal:

   * End-to-end (E2E) latency measures the interval from when Azure Storage receives the first packet of the request until Azure Storage receives a client acknowledgment on the last packet of the response.

   * Server latency measures the interval from when Azure Storage receives the last packet of the request until the first packet of the response is returned from Azure Storage.

To view latency metrics, navigate to your storage resource in the Azure portal:

* On the left navigation window, select **Insights** from the **Monitoring** drop-down menu.

* The insights tab opens a window that includes a chart showing both `E2E` and `Server` latency metrics:

   :::image type="content" source="../media/latency/azure-storage.png" alt-text="Screenshot of Azure Storage latency metrics in the Azure portal.":::


For more information, *see* [Latency in Blob storage](/azure/storage/blobs/storage-blobs-latency).


## Check monitoring metrics for your resource

You can monitor performance metrics and set up alerts for your Document Intelligence resource in the Azure portal. To view latency metrics, navigate to your Document Intelligence resource in the Azure portal:

* On the **Overview** page, select **Monitoring**, select the time period, and review the **Request latency** metrics on page.

   :::image type="content" source="../media/latency/azure-portal-monitoring.png" alt-text="Screenshot of Azure usage monitoring metrics in the Azure portal.":::

