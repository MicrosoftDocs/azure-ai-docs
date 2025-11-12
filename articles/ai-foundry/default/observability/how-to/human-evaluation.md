---
title: Human Evaluation for Microsoft Foundry Agents
titleSuffix: Microsoft Foundry
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/18/2025
description: Learn how to set up human evaluation for your Microsoft Foundry agents, create templates, and analyze results to improve agent performance.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: peichengshi
---
# Set up human evaluation for your agents (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

In this article, you’ll learn how to set up human evaluation for your Foundry agent. As an agent builder, you can create evaluation question templates focused on key aspects of interest and enable them to be answered for each agent response in the agent’s preview experience. This enables human evaluations by peers, data scientists, or compliance team members based on the defined templates. Once evaluations are completed, you can view and download the results directly from the Foundry portal for further analysis.

## Prerequisites

Before you begin:

- You have access to the **Microsoft Foundry portal**.
- You have one or more agents built.
- You have configured Application Insights for your project

## Create a human evaluation template

To begin human evaluation for your Foundry agent, you’ll first define a template that contains the set of questions you want human reviewers to complete based on agent responses.

### Steps to create a template

1. Select the agent you want to evaluate from the agent table in the **Agents** tab.  
2. Navigate to the **Human Evaluation** tab under **Evaluation**.  
3. Select **Create new template** to start the template creation process.  
4. In the **Create Human Evaluation Template** pop-up, assign a name and description, edit or delete sample questions, and add new questions based on your evaluation goals. Supported question types include thumbs up/down, slider, multiple choice, and free-form text.  
5. After configuring the template, select **Create** to finalize it.

## Manage your evaluation templates

You can create multiple evaluation templates based on your assessment needs. The template table allows you to edit, delete, and set templates as active or inactive.

### Manage templates

- You can edit a template using the **Edit** button in the template table. The template opens in an editable pop-up for updates.  
- You can delete a template using the **Delete** button in the template table.  
   > [!NOTE]
   > Once deleted, the template and its associated evaluation results cannot be retrieved from the UI.  
- To set a template as active, select **Set as active** in the template table. Only one template can be active at any given time. Activating a new template automatically deactivates the previous one. You can also deactivate the current active template to stop capturing human evaluation results by selecting **Set as inactive**.

## Conduct human evaluation

Once the evaluation template is configured and set as active for the target agent, human reviewers can begin their evaluation using the preview web app functionality.

> [!NOTE]
> Human reviewers need access to the Foundry project where the agent resides in to interact with the preview web app.

### Steps to conduct human evaluation

1. Select **Preview** in the top-right corner of the agent builder experience to open the agent in a web app interface.  
2. Start testing the agent by entering input and selecting **Send** to trigger an agent run.  
3. After the agent responds, select the **Feedback** button to provide human evaluation for that response.  
   - A side panel appears, displaying the evaluation template configured by the agent builder.  
   - Reviewers can answer some or all questions in the form.  
4. When finished, select **Save** to store the evaluation data for agent builders to review.  
   - Select **Cancel** to discard the answers.  
5. Continue evaluating additional responses by interacting with the agent for new outputs or navigating to previous responses.  
   - Reviewers can skip evaluations for certain responses or provide multiple evaluations for the same agent response as needed.  

## Review human evaluation results

Once human reviewers have completed their evaluations, agent builders can preview and download the results for further analysis through the Foundry portal.

### Steps to review results

1. Navigate to the template table within the **Human Evaluation** tab and select the template you want to review results for.  
2. After selecting a template, all corresponding evaluation results will appear under the **Evaluation Results** section. Each instance is displayed with its timestamp for reference.  
3. Select an evaluation instance to view its JSON summary in the **JSON Output** section. The JSON includes:
   - Timestamp  
   - User prompt  
   - Agent response  
   - Questions from the evaluation template  
   - Reviewer answers  
4. To download all evaluation results for a template, select **Download Results** after selecting the template. The results are exported as a CSV file containing all information from the JSON view for each evaluation instance.

> [!NOTE]
> Evaluation data is stored in Application Insights and will follow its retention policy. Download and persist the data elsewhere if you need to keep it long term.

## Related content

- [Evaluate your AI agents locally with the Azure AI Evaluation SDK](../../..//how-to/develop/agent-evaluate-sdk.md)
- [Agent tracing overview](../concepts/trace-agent-concept.md)
