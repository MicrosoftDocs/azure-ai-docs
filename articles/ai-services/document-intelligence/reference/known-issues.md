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
| **1001** | File types | `Content Is Not Supported Error With Excel Files` | Although Excel files are documented as a supported input type, requests fail with **Content isn't supported** when the Excel content exceeds an internal character limit. This behavior typically happens with large or heavily populated spreadsheets. | Excel files exceeding **~8,000,000 characters** are rejected. Split the Excel file into multiple smaller files and submit them separately.<br><br>or<br><br>Switch to Azure Content Understanding, which has an improved parser logic for these files | April  2026 |
| **1002** | Encryption | `ServiceUnavailable error when using CMK` | Document Intelligence operations that rely on **Customer‑Managed Keys (CMK)** may intermittently fail with **service unavailable** error due to stale identity or key material cached by the storage service. | **Option A:** Force a refresh of the `CMK` cache by disabling and re‑enabling `CMK`, assigning a new key, or associating a new managed identity.  <br>  <br>**Option B:** Switch to **Microsoft‑Managed Keys (MMK)** via _Document Intelligence Resource → Management → Encryption → Microsoft Managed Keys. | April  2026 |
| **1003** | Model management | `Model Exists Error When Model Copy` | Copying a custom model can fail with a **Model Exists** error caused by a broken or partially created model on the target resource. Customers can't resolve this condition themselves. | No customer‑side workaround. Raise a support request so the product group can clean up the broken model on the backend. | April  2026 |
| **1004** | Model training | `HTTP 500 – InternalServerError during model training (Neural or Template, Preview/GA APIs)` | Model training may fail with **HTTP 500 / InternalServerError** when the resource isn't correctly configured with managed identity, especially for newer training flows. | Enable **Managed Identity** on the Document Intelligence resource and ensure it has the required permissions, following official managed‑identity configuration guidance. | April  2026 |
| **1005** | Model training | `Model training stuck in *Not started* status` | When a model training job fails before execution, the failed job may remain visible in the model list with status **Not started**. This behavior is a backend lifecycle behavior and not caused by customer configuration. | The backend automatically clears failed training jobs after approximately seven (7) days. If earlier removal is required, customer must raise a support request so CSS/PG can manually remove the stale training entry. | April  2026 |

## Related content

* [Azure Service Health Portal](/azure/service-health/service-health-portal-update)

* [Azure Status overview](/azure/service-health/azure-status-overview)

* [What's new in Document Intelligence - Foundry Tools | Microsoft Learn](../whats-new.md)