---
title: Azure Document Intelligence in Foundry Tools known issues
titlesuffix: Foundry Tools
description: Known and common issues with Azure Document Intelligence in Foundry Tools.
ai-usage: ai-assisted
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: reference
ms.date: 04/09/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD025 -->
# Azure Document Intelligence known issues and troubleshooting

Azure Document Intelligence is updated continuously, and service changes can affect feature behavior and capability limits. This article tracks known issues in Azure Document Intelligence, describes their impact, and provides mitigation or resolution guidance. Before you submit a support request, review the list to determine whether your issue is a known condition and to identify the recommended remediation.

## Service-level outages and notifications

Azure status and Azure Service Health publish service-level outages and regional disruptions. Use these services to validate current impact, track incident lifecycle updates, and configure proactive notifications for your subscriptions and resources.

* **Service-level outages**: [Azure status page](https://azure.status.microsoft/status).
* **Outage notifications and alerts**: [Azure Service Health Portal](https://azure.microsoft.com/status/).

## Current known issues

The following table lists active, service-confirmed issues in Azure Document Intelligence. Each entry includes the issue category, observed behavior, documented workaround, and initial publish date.

| Issue ID | Category | Title | Description | Workaround | Publication date |
| --- | --- | --- | --- | --- | --- |
| **1001** | File types | `Content Is Not Supported Error With Excel Files` | Excel files are documented as a supported input type. Requests can fail with **Content isn't supported** when file content exceeds an internal character limit. This condition usually occurs with large or densely populated spreadsheets. | **Excel files larger than *~8,000,000 characters* are rejected**.<br><br>Split large Excel files into smaller files and submit them separately.<br><br>Switch to Azure [Content Understanding](../../content-understanding/overview.md), which uses improved parser logic for these files. | April  2026 |
 | **1002** | Encryption | `ServiceUnavailable error when using CMK` | Operations that rely on **Customer‑Managed Keys (CMK)** can intermittently fail with a **service unavailable** error. This failure occurs when the storage service uses stale cached identity or key material. | **Option A:** Refresh the `CMK` cache. Disable and re-enable `CMK`, assign a new key, or associate a new managed identity.<br><br>**Option B:** Switch to **Microsoft-Managed Keys (MMK)**: Navigate to your Document Intelligence resource in the [Azure portal](https://portal.azure.com/). Select **Resource Management** → **Encryption** -> Encryption type: **Microsoft Managed Keys**. | April  2026 |
| **1003** | Model management | `Model Exists Error When Model Copy` | Copying a custom model can fail with a **Model Exists** error. This error occurs when a broken or partially created model remains on the target resource. Customers can't resolve this condition themselves. | No customer-side workaround is available.<br><br>Submit a [support request](mailto:formrecog_contact@microsoft.com) so the product group can remove the broken model from the backend. | April  2026 |
| **1004** | Model training | `HTTP 500 – InternalServerError during model training (Neural or Template, Preview/GA APIs)` | Model training can fail with **HTTP 500 / InternalServerError**. This failure typically occurs when managed identity isn't configured correctly on the resource, especially in newer training flows. | Enable **Managed Identity** on your Document Intelligence resource.<br><br>Verify that the identity has the required permissions.<br><br>Follow the official [managed-identity configuration guidance](../authentication/managed-identities.md). | April  2026 |
| **1005** | Model training | `Model training stuck in *Not started* status` | If a model training job fails before execution, the failed job may remain visible in the model list with status **Not started**. This state results from backend lifecycle handling, not customer configuration. | The backend automatically clears failed training jobs after approximately seven (7) days.<br><br>If earlier removal is required, submit an [Azure portal support request](https://ms.portal.azure.com/?quickstart=true#view/Microsoft_Azure_Support/HelpAndSupportBlade/~/overview) so Customer Support Services (CSS) / Product Groups (PG) can manually remove the stale training entry. | April  2026 |

## Related content

* [Azure Service Health Portal](/azure/service-health/service-health-portal-update)

* [Azure Status overview](/azure/service-health/azure-status-overview)

* [What's new in Document Intelligence - Foundry Tools | Microsoft Learn](../whats-new.md)