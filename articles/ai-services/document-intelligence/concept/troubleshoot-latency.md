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

   :::image type="content" source="../media/azure-status.png" alt-text="Screenshot of the Microsoft Azure status page" lightbox="../media/azure-status.png":::

## Check file size

the size of the files you may be sending through the request API. The service parallelizes processing, larger files can lead to longer processing time. Please normalize your measurement as latency per page. Consider raising the issue if you see sustained periods (more than an hour) with latency per page consistently being above 15s.

## Check for latency in Azure Blob storage

Azure Storage latency is related to request rates for Azure Storage operations. In practice, request rates do not always scale so linearly, due to overhead in the client from task scheduling, context switching, and so forth. On the service side, there can be variability in latency due to pressure on the Azure Storage system, differences in the storage media used, noise from other workloads, maintenance tasks, and other factors. Finally, the network connection between the client and the server may affect Azure Storage latency due to congestion, rerouting, or other disruptions. For more information, *see* [Latency im Blob storage](/azure/storage/blobs/storage-blobs-latency).

## Check monitoring metrics in the Azure portal
