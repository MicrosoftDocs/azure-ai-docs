---
title: "Part 3: Evaluate a chat app with the Azure AI SDK"
titleSuffix: Microsoft Foundry
description: Evaluate and deploy a custom chat app with the prompt flow SDK. This tutorial is part 3 of a 3-part tutorial series.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
  - hub-only
  - dev-focus
ms.topic: tutorial
ai-usage: ai-assisted
ms.date: 12/16/2025
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley

#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can evaluate and deploy a chat app.
---

# Tutorial: Part 3 - Evaluate a custom chat application with the Microsoft Foundry SDK

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In this tutorial, you evaluate the chat app you built in [Part 2 of the tutorial series](copilot-sdk-build-rag.md). You assess your app's quality across multiple metrics and then iterate on improvements. In this part, you:

> [!div class="checklist"]
> - Create an evaluation dataset
> - Evaluate the chat app with Azure AI evaluators
> - Iterate and improve your app

This tutorial builds on [Part 2: Build a custom chat app with the Microsoft Foundry SDK](copilot-sdk-build-rag.md).

## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

- Complete [Part 2 of the tutorial series](copilot-sdk-build-rag.md) to build the chat application.
- Use the same **hub-based** project you created in Part 1.
- **Azure AI permissions**: Owner or Contributor role to modify model endpoint rate limits and run evaluation jobs.
- Make sure you complete the steps to [add telemetry logging](copilot-sdk-build-rag.md#add-telemetry-logging) from Part 2.

## Create evaluation dataset

Use the following evaluation dataset, which contains example questions and expected answers. Use this dataset with an evaluator and the `get_chat_response()` target function to assess your chat app's performance across relevance, groundedness, and coherence metrics.

1. Create a file named **chat_eval_data.jsonl** in your **assets** folder.
1. Paste this dataset into the file:

    :::code language="jsonl" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/assets/chat_eval_data.jsonl":::

    References: [JSONL format for evaluation datasets](../how-to/evaluate-results.md).

## Evaluate with Azure AI evaluators

Create an evaluation script that generates a target function wrapper, loads your dataset, runs the evaluation, and logs results to your Foundry project.

1. Create a file named **evaluate.py** in your main folder.
1. Add the following code to import the required libraries, create a project client, and configure some settings:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/evaluate.py" id="imports_and_config":::

    References: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.DefaultAzureCredential), [azure-ai-evaluation](https://pypi.org/project/azure-ai-evaluation/).

1. Add code to create a wrapper function that implements the evaluation interface for query and response evaluation:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/evaluate.py" id="evaluate_wrapper":::

    References: [azure-ai-evaluation](https://pypi.org/project/azure-ai-evaluation/), evaluation target functions.

1. Finally, add code to run the evaluation, view the results locally, and get a link to the evaluation results in Foundry portal:
 
    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/evaluate.py" id="run_evaluation":::

    References: [azure-ai-evaluation](https://pypi.org/project/azure-ai-evaluation/), [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient).

### Configure the evaluation model

The evaluation script calls the model many times. Consider increasing the number of tokens per minute for the evaluation model.  

In Part 1 of this tutorial series, you created an **.env** file that specifies the name of the evaluation model, `gpt-4o-mini`.  Try to increase the tokens per minute limit for this model, if you have available quota. If you don't have enough quota to increase the value, don't worry.  The script is designed to handle limit errors.

1. In your project in Foundry portal, select **Models + endpoints**.
1. Select **gpt-4o-mini**.  
1. Select **Edit**.
1. If you have quota, increase the **Tokens per Minute Rate Limit** to 30 or more. 
1. Select **Save and close**.

### Run the evaluation script

1. From your console, sign in to your Azure account by using the Azure CLI:

    ```bash
    az login
    ```

1. Install the required packages:

    ```bash
    pip install openai
    pip install azure-ai-evaluation[remote]
    ```

    References: [azure-ai-evaluation SDK](https://pypi.org/project/azure-ai-evaluation/), Evaluation SDK documentation.

### Verify your evaluation setup

Before running the full evaluation (which takes 5–10 minutes), verify that the SDK and your project connection are working by running this quick test:

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Test that you can connect to your project
project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)
print("Evaluation SDK is ready! You can now run evaluate.py")
```

If you see `"Evaluation SDK is ready!"`, your setup is complete and you can proceed.

References: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.DefaultAzureCredential).

### Start the evaluation

* Run the evaluation script:

    ```bash
    python evaluate.py
    ```

The evaluation takes 5–10 minutes to complete. You might see timeout warnings and rate-limit errors. The script handles these errors automatically and continues processing.

### Interpret the evaluation output

In the console output, you see an answer for each question, followed by a table with summarized metrics showing relevance, groundedness, and coherence scores. Scores range from 0 (worst) to 4 (best) for GPT-assisted metrics. Look for low groundedness scores to identify responses that aren't well-supported by the reference documents, and low relevance scores to identify off-topic responses.

You might see many `WARNING:opentelemetry.attributes:` messages and timeout errors. You can safely ignore these messages. They don't affect the evaluation results. The evaluation script is designed to handle rate-limit errors and continue processing.

The evaluation results output also includes a link to view detailed results in the Foundry portal, where you can compare evaluation runs side-by-side and track improvements over time.

```Text
====================================================
'-----Summarized Metrics-----'
{'groundedness.gpt_groundedness': 1.6666666666666667,
 'groundedness.groundedness': 1.6666666666666667}
'-----Tabular Result-----'
                                     outputs.response  ... line_number
0   Could you specify which tent you are referring...  ...           0
1   Could you please specify which camping table y...  ...           1
2   Sorry, I only can answer queries related to ou...  ...           2
3   Could you please clarify which aspects of care...  ...           3
4   Sorry, I only can answer queries related to ou...  ...           4
5   The TrailMaster X4 Tent comes with an included...  ...           5
6                                            (Failed)  ...           6
7   The TrailBlaze Hiking Pants are crafted from h...  ...           7
8   Sorry, I only can answer queries related to ou...  ...           8
9   Sorry, I only can answer queries related to ou...  ...           9
10  Sorry, I only can answer queries related to ou...  ...          10
11  The PowerBurner Camping Stove is designed with...  ...          11
12  Sorry, I only can answer queries related to ou...  ...          12

[13 rows x 8 columns]
('View evaluation results in Foundry portal: '
 'https://xxxxxxxxxxxxxxxxxxxxxxx')
```

## Iterate and improve

The evaluation results reveal that responses often aren't well-grounded in the reference documents. To improve groundedness, modify your system prompt in the **assets/grounded_chat.prompty** file to encourage the model to use the reference documents more directly.

**Current prompt (problematic)**:
```
If the question is not related to outdoor/camping gear and clothing, just say 'Sorry, I only can answer queries related to outdoor/camping gear and clothing. So, how can I help?'
If the question is related to outdoor/camping gear and clothing but vague, ask clarifying questions.
```

**Improved prompt**:
```
If the question is related to outdoor/camping gear and clothing, answer based on the reference documents provided.
If you cannot find information in the reference documents, say: 'I don't have information about that specific topic. Let me help with related products or try a different question.'
For vague questions, ask clarifying questions to better assist.
```

After updating the prompt:

1. Save the file.
1. Run the evaluation script again:

    ```bash
    python evaluate.py
    ```

1. Compare the new evaluation results to the previous run. You should see improved groundedness scores.

Try additional modifications like:
- Changing the system prompt to focus on accuracy over completeness
- Testing with a different model (for example, `gpt-4-turbo` if available)
- Adjusting the context retrieval to return more relevant documents

Each iteration helps you understand which changes improve specific metrics.

## Clean up resources

To avoid incurring unnecessary Azure costs, delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

## Related content

- [Learn more about the Microsoft Foundry SDK](../how-to/develop/sdk-overview.md)
