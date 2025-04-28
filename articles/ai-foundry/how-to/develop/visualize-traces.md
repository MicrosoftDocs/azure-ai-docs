---
title: Visualize your traces
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to visualize your traces.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 02/28/2025
ms.reviewer: amipatel
ms.author: lagayhar
author: lgayhardt
---

# Visualize your traces (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

After instrumenting your application to log traces, let's walkthrough how you can view your traces in both local and cloud solutions to debug your application.

## View your traces for local debugging

To enable traces locally, you have two options:  

1. Using **Prompty**, you can trace your application with the **Azure AI Inference SDK**, which offers enhanced visibility and simplified troubleshooting for LLM-based applications. This method follows the OpenTelemetry specification, capturing and visualizing the internal execution details of any AI application, thereby enhancing the overall development experience. To learn more, see [Debugging Prompty](https://prompty.ai/docs/getting-started/debugging-prompty).
2. **Aspire Dashboard** : A free & open-source OpenTelemetry dashboard for deep insights into your apps on your local development machine. To learn more, see [Aspire Dashboard](https://aspiredashboard.com/#start ).

## View your traces in Azure AI Foundry portal

Before you can log to Azure AI Foundry portal, attach an Application Insights resource to your project.

1. Navigate to your project in [Azure AI Foundry portal](https://ai.azure.com/).
1. Select the **Tracing** page on the left hand side.
1. Select **Create New** to attach a new Application Insights resource to your project.
1. Supply a name and select **Create**.

:::image type="content" source="../../media/trace/visualize/tracing-setup-overview.gif" alt-text="Animation of going to tracing and creating an Application Insight resource." lightbox="../../media/trace/visualize/tracing-setup-overview.gif":::

Next, install the `opentelemetry` SDK:

```python
%pip install azure-monitor-opentelemetry
```

Now enable tracing with output to the console:

```python
import os
from azure.monitor.opentelemetry import configure_azure_monitor

os.environ['AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED'] = 'true'
# Enable Azure Monitor tracing
application_insights_connection_string = project.telemetry.get_connection_string()
if not application_insights_connection_string:
    print("Application Insights was not enabled for this project.")
    print("Enable it via the 'Tracing' tab in your Azure AI Foundry project page.")
    exit()
    
configure_azure_monitor(connection_string=application_insights_connection_string)
```

Finally, run an inferencing call. The call is logged to Azure AI Foundry. This code prints a link to the traces.

```python
response = chat.complete(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an AI assistant that is a travel planning expert especially with National Parks."},
        {"role": "user", "content": "Hey, can you recommend me trails I should go on when I visit Mount Rainier?"},
    ]
)

print("View traces at:")
print(f"https://ai.azure.com/tracing?wsid=/subscriptions/{project.scope['subscription_id']}/resourceGroups/{project.scope['resource_group_name']}/providers/Microsoft.MachineLearningServices/workspaces/{project.scope['project_name']}")
```

Select the link and begin viewing traces in Azure AI Foundry portal!

### Debug and filter traces

In your project, you can filter your traces as you see fit.

By selecting a trace, I can step through each span and identify issues while observing how my application is responding.

:::image type="content" source="../../media/trace/visualize/debug-filter-tracing.gif" alt-text="Animation of filtering traces in the portal." lightbox="../../media/trace/visualize/debug-filter-tracing.gif":::

### Update your attached Application Insights resource

 To update the Application Insights resource that is attached to your project, go to **Manage data source** and **Edit** to switch to a new Application Insights resource.

:::image type="content" source="../../media/trace/visualize/tracing-manage-data-source.png" alt-text="Screenshot of manage data sources pop-up highlighting the edit button." lightbox="../../media/trace/visualize/tracing-manage-data-source.png":::

## View your traces in Azure Monitor

If you logged traces using the previous code snippet, then you're all set to view your traces in Azure Monitor Application Insights. You can open in Application Insights from **Manage data source** and use the **End-to-end transaction details view** to further investigate.

For more information on how to send Azure AI Inference traces to Azure Monitor and create Azure Monitor resource, see [Azure Monitor OpenTelemetry documentation](/azure/azure-monitor/app/opentelemetry-enable).

### View your generative AI spans and traces

From Azure AI Foundry project, you can also open your custom dashboard that provides you with insights specifically to help you monitor your generative AI application.

In this Azure Workbook, you can view your Gen AI spans and jump into the Azure Monitor **End-to-end transaction details view** to deep dive and investigate.

Learn more about using this workbook to monitor your application, see [Azure Workbook documentation](/azure/azure-monitor/visualize/workbooks-create-workbook).

## Related content

- [Trace your application with Azure AI Inference SDK](./trace-local-sdk.md)
