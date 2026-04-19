---
title: "Human Evaluation for Microsoft Foundry Agents"
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 04/19/2026
description: "Learn how to set up human evaluation for your Microsoft Foundry agents, create templates, and analyze results to improve agent performance."
author: lgayhardt
ms.author: lagayhar
ms.reviewer: peichengshi
ai-usage: ai-assisted
---
# Set up human evaluation for your agents (preview)
[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

This article explains how to set up human evaluation for your Foundry agent. As an agent builder, you define evaluation question templates focused on key aspects of interest. Human reviewers — peers, data scientists, or compliance team members — complete those templates for each agent response in the agent's preview experience. After reviewers submit their evaluations, you can view and download the results directly from the Foundry portal for further analysis.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with one or more [agents](../../agents/overview.md).
- [Application Insights configured](trace-agent-setup.md) for your project.
- **Azure AI Project Manager** role (or higher) on the Foundry project, to create and manage evaluation templates. For more information, see [Role-based access control in Microsoft Foundry](../../concepts/rbac-foundry.md).
- For human reviewers: **Azure AI User** role (minimum) on the Foundry project, to access the preview web app and submit feedback. [TO VERIFY: confirm with product engineering that Azure AI User is the minimum role for preview web app access.]

## Create a human evaluation template

To begin human evaluation for your Foundry agent, define a template that contains the set of questions you want human reviewers to complete based on agent responses.

1. Select the agent you want to evaluate from the agent table in the **Agents** tab.  
2. Navigate to the **Human Evaluation** tab under **Evaluation**.  
3. Select **Create new template** to start the template creation process.  
4. In the **Create Human Evaluation Template** pop-up, assign a name and description, edit or delete sample questions, and add new questions based on your evaluation goals. Supported question types include thumbs up/down, slider, multiple choice, and free-form text.

   > [!TIP]
   > Example questions by type:
   > - **Thumbs up/down:** "Was this response accurate?"
   > - **Slider (1–5):** "Rate the helpfulness of this response."
   > - **Multiple choice:** "Which best describes this response? (Correct / Partially correct / Incorrect)"
   > - **Free-form text:** "What additional context would have improved this response?"

5. After configuring the template, select **Create** to finalize it.

The new template appears in the template table with **Inactive** status. Activate it before reviewers begin evaluating.

## Manage your evaluation templates

You can create multiple evaluation templates based on your assessment needs. The template table allows you to edit, delete, and set templates as active or inactive.

- Select **Edit** in the template table to update a template. The template opens in an editable pop-up.  
- Select **Delete** to remove a template.  
   > [!NOTE]
   > Once deleted, the template and its associated evaluation results can't be retrieved from the portal.  
- To set a template as active, select **Set as active** in the template table. Only one template can be active at any given time. Activating a new template automatically deactivates the previous one. Select **Set as inactive** to stop capturing human evaluation results for the current template.

## Conduct human evaluation

After the evaluation template is configured and set as active for the target agent, human reviewers can begin their evaluation through the preview web app — a browser-based chat interface launched directly from the agent builder.

> [!NOTE]
> Human reviewers need the **Azure AI User** role on the Foundry project to access the preview web app and submit feedback.

1. Select **Preview** in the top-right corner of the agent builder to open the agent in a browser-based chat interface.  
2. Enter input and select **Send** to trigger an agent run.  
3. After the agent responds, select the **Feedback** button to provide human evaluation for that response.  
   - A side panel appears, displaying the active evaluation template.  
   - Reviewers can answer some or all questions in the form.  
4. Select **Save** to store the evaluation data, or **Cancel** to discard.  
5. Continue evaluating additional responses by entering new input or navigating to previous responses.  
   - Reviewers can skip evaluations for certain responses or submit multiple evaluations for the same response.

Saved evaluations are recorded per agent response and become available to agent builders in the **Evaluation Results** section.

## Review human evaluation results

After human reviewers complete their evaluations, agent builders can preview and download the results for further analysis through the Foundry portal.

1. Navigate to the template table within the **Human Evaluation** tab and select the template you want to review results for.  
2. All corresponding evaluation results appear under the **Evaluation Results** section. Each instance is displayed with its timestamp for reference.  
3. Select an evaluation instance to view its JSON summary in the **JSON Output** section. The JSON includes:
   - Timestamp  
   - User prompt  
   - Agent response  
   - Questions from the evaluation template  
   - Reviewer answers  
4. To download all evaluation results for a template, select **Download Results**. The results are exported as a CSV file containing all information from the JSON view for each evaluation instance.

The downloaded CSV contains one row per evaluation instance, with columns for each field from the JSON view.

> [!NOTE]
> Evaluation data is stored in Application Insights and follows its retention policy. To adjust the retention period, see [Data retention and archive in Azure Monitor Logs](/azure/azure-monitor/logs/data-retention-configure). Download and persist the data elsewhere if you need it long term.

## Related content

- [Evaluate your AI agents](evaluate-agent.md)
- [Agent tracing overview](../concepts/trace-agent-concept.md)
- [Troubleshoot evaluation and observability issues](troubleshooting.md)
