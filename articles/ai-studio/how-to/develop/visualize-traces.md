---
title: Visualize your traces
titleSuffix: Azure AI Studio
description: This article provides instructions on how to visualize your traces.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 11/19/2024
ms.reviewer: amipatel
ms.author: lagayhar  
author: lgayhardt
---

# Visualize your traces

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

After instrumenting your application to log traces, let's walkthrough how you can view your traces in both local and cloud solutions to debug your application.

## View your traces for local debugging

To enable traces locally, you have two options:  

1. Using **Prompty**, you can trace your application with the **Azure AI Inference SDK**, which offers enhanced visibility and simplified troubleshooting for LLM-based applications. This method follows the OpenTelemetry specification, capturing and visualizing the internal execution details of any AI application, thereby enhancing the overall development experience. To learn more, see [Debugging Prompty](https://prompty.ai/docs/getting-started/debugging-prompty).
2. **Aspire Dashboard** : A free & open-source OpenTelemetry dashboard for deep insights into your apps on your local development machine. To learn more, see [Aspire Dashboard](https://aspiredashboard.com/#start ).

## View your traces in Azure AI Studio

Before you can log to Azure AI Studio, attach an Application Insights resource to your project.

1. Navigate to your project in [Azure AI Studio](https://ai.azure.com/).
1. Select the **Tracing** page on the left hand side.
1. Select **Create New** to attach a new Application Insights resource to your project.
1. Supply a name and select **Create**.

(Screenshot or gif placeholder - here)

After creating and connecting your Application Insights resource, grab the connection string from **Manage data source**. You'll need to provide this connection string to log traces here.

(Screenshot or gif placeholder - here)
:::image type="content" source="../../media/how-to/tracing/" alt-text="Screenshot of [ADD LINK TEXT]." lightbox="../../media/how-to/tracing/":::

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
    print("Enable it via the 'Tracing' tab in your AI Studio project page.")
    exit()
    
configure_azure_monitor(connection_string=application_insights_connection_string)
```

Finally, run an inferencing call. The call is logged to Azure AI Studio. This code prints a link to the traces.

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

Select the link and begin viewing traces in Azure AI Studio!

### Debug and filter traces

In your project, you can filter your traces as you see fit.

(Placeholder for gif/pic)
:::image type="content" source="../../media/how-to/tracing/" alt-text="Screenshot of [ADD LINK TEXT]." lightbox="../../media/how-to/tracing/":::

By selecting a trace, I can step through each span and identify issues while observing how my application is responding.

(Placeholder for gif/pic)
:::image type="content" source="../../media/how-to/tracing/" alt-text="Screenshot of [ADD LINK TEXT]." lightbox="../../media/how-to/tracing/":::

### Update your attached Application Insights resource

 To update the Application Insights resource that is attached to your project, go to **Manage data source** and **Edit** to switch to a new Application Insights resource.

 (Placeholder for gif/pic)
:::image type="content" source="../../media/how-to/tracing/" alt-text="Screenshot of [ADD LINK TEXT]." lightbox="../../media/how-to/tracing/":::

## View your traces in Azure Monitor

If you logged traces using the previous code snippet, then you're all set to view your traces in Azure Monitor Application Insights. You can open in Application Insights from **Manage data source** and use the **Transaction Search** to further investigate.

(Placeholder for gif/pic)
:::image type="content" source="../../media/how-to/tracing/" alt-text="Screenshot of [ADD LINK TEXT]." lightbox="../../media/how-to/tracing/":::

Refer to [Azure Monitor OpenTelemetry documentation](/azure/azure-monitor/app/opentelemetry-enable) for more details on how to send Azure AI Inference traces to Azure Monitor and create Azure Monitor resource.

### View your generative AI spans and traces

From Azure AI studio project, you can also open your custom dashboard that will provide you with insights specifically to help you monitor your generative AI application.

(Placeholder for gif/pic)
:::image type="content" source="../../media/how-to/tracing/" alt-text="Screenshot of [ADD LINK TEXT]." lightbox="../../media/how-to/tracing/":::

In this Azure Workbook, you can view your Gen AI spans and jump into the extensive **Transaction search** view to deep dive and investigate.

(Placeholder for gif/pic)
:::image type="content" source="../../media/how-to/tracing/" alt-text="Screenshot of [ADD LINK TEXT]." lightbox="../../media/how-to/tracing/":::

Learn more about using this workbook to monitor your application, see [Azure Workbook documentation](/azure/azure-monitor/visualize/workbooks-create-workbook).

## Related content

- 
- 