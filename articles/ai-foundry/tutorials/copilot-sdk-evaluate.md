---
title: "Part 3: Evaluate a chat app with the Azure AI SDK"
titleSuffix: Azure AI Foundry
description: Evaluate and deploy a custom chat app with the prompt flow SDK. This tutorial is part 3 of a 3-part tutorial series.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: tutorial
ms.date: 04/07/2025
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley

#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can evaluate and deploy a chat app.
---

# Tutorial: Part 3 - Evaluate a custom chat application with the Azure AI Foundry SDK

In this tutorial, you use the [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) SDK (and other libraries) to  evaluate the chat app you built in [Part 2 of the tutorial series](copilot-sdk-build-rag.md). In this part three, you learn how to:

> [!div class="checklist"]
> - Create an evaluation dataset
> - Evaluate the chat app with Azure AI evaluators
> - Iterate and improve your app


This tutorial is part three of a three-part tutorial.

## Prerequisites

[!INCLUDE [hub-only-tutorial](../includes/hub-only-tutorial.md)]

- Complete [part 2 of the tutorial series](copilot-sdk-build-rag.md) to build the chat application.

- Use the same **[!INCLUDE [hub](../includes/hub-project-name.md)]** you created in part 1. 

- Make sure you've completed the steps to [add telemetry logging](copilot-sdk-build-rag.md#logging) from part 2.

## <a name="evaluate"></a> Evaluate the quality of the chat app responses

Now that you know your chat app responds well to your queries, including with chat history, it's time to evaluate how it does across a few different metrics and more data.

You use an evaluator with an evaluation dataset and the `get_chat_response()` target function, then assess the evaluation results.

Once you run an evaluation, you can then make improvements to your logic, like improving your system prompt, and observing how the chat app responses change and improve.

### Create evaluation dataset

Use the following evaluation dataset, which contains example questions and expected answers (truth).

1. Create a file called **chat_eval_data.jsonl** in your **assets** folder.
1. Paste this dataset into the file:

    :::code language="jsonl" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/assets/chat_eval_data.jsonl":::

## Evaluate with Azure AI evaluators

Now define an evaluation script that will:

- Generate a target function wrapper around our chat app logic.
- Load the sample `.jsonl` dataset.
- Run the evaluation, which takes the target function, and merges the evaluation dataset with the responses from the chat app.
- Generate a set of GPT-assisted metrics (relevance, groundedness, and coherence) to evaluate the quality of the chat app responses.
- Output the results locally, and logs the results to the cloud project.

The script allows you to review the results locally, by outputting the results in the command line, and to a json file.

The script also logs the evaluation results to the cloud project so that you can compare evaluation runs in the UI.

1. Create a file called **evaluate.py** in your main folder.
1. Add the following code to import the required libraries, create a project client, and configure some settings: 

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/evaluate.py" id="imports_and_config":::

1. Add code to create a wrapper function that implements the evaluation interface for query and response evaluation:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/evaluate.py" id="evaluate_wrapper":::

1. Finally, add code to run the evaluation, view the results locally, and gives you a link to the evaluation results in Azure AI Foundry portal:
 
    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/evaluate.py" id="run_evaluation":::

### Configure the evaluation model

Since the evaluation script calls the model many times, you might want to increase the number of tokens per minute for the evaluation model.  

In Part 1 of this tutorial series, you created an **.env** file that specifies the name of the evaluation model, `gpt-4o-mini`.  Try to increase the tokens per minute limit for this model, if you have available quota. If you don't have enough quota to increase the value, don't worry.  The script is designed to handle limit errors.

1. In your project in Azure AI Foundry portal, select **Models + endpoints**.
1. Select **gpt-4o-mini**.  
1. Select **Edit**.
1. If you have quota to increase the **Tokens per Minute Rate Limit**, try increasing it to 30 or above. 
1. Select **Save and close**.

### Run the evaluation script

1. From your console, sign in to your Azure account with the Azure CLI:

    ```bash
    az login
    ```

1. Install the required package:

    ```bash
    pip install azure-ai-evaluation[remote]
    ```

1. Now run the evaluation script:

    ```bash
    python evaluate.py
    ```

Expect the evaluation to take a few minutes to complete.

### Interpret the evaluation output

In the console output, you see an answer for each question, followed by a table with summarized metrics. (You might see different columns in your output.)

If you weren't able to increase the tokens per minute limit for your model, you might see some time-out errors, which are expected. The evaluation script is designed to handle these errors and continue running.  

> [!NOTE]
> You may also see many `WARNING:opentelemetry.attributes:` - these can be safely ignored and do not affect the evaluation results.

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
('View evaluation results in Azure AI Foundry portal: '
 'https://xxxxxxxxxxxxxxxxxxxxxxx')
```


### View evaluation results in Azure AI Foundry portal

Once the evaluation run completes, follow the link to view the evaluation results on the **Evaluation** page in the Azure AI Foundry portal.

:::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/eval-studio-overview.png" alt-text="Screenshot shows evaluation overview in Azure AI Foundry portal.":::

You can also look at the individual rows and see metric scores per row, and view the full context/documents that were retrieved. These metrics can be helpful in interpreting and debugging evaluation results.

:::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/eval-studio-rows.png" alt-text="Screenshot shows rows of evaluation results in Azure AI Foundry portal.":::

For more information about evaluation results in Azure AI Foundry portal, see [How to view evaluation results in Azure AI Foundry portal](../how-to/evaluate-results.md).

## Iterate and improve

Notice that the responses are not well grounded. In many cases, the model replies with a question rather than an answer. This is a result of the prompt template instructions. 
 
* In your **assets/grounded_chat.prompty** file, find the sentence "If the question is not related to outdoor/camping gear and clothing, just say 'Sorry, I only can answer queries related to outdoor/camping gear and clothing. So, how can I help?'"
* Change the sentence to "If the question is related to outdoor/camping gear and clothing but vague, try to answer based on the reference documents, then ask for clarifying questions."  
* Save the file and re-run the evaluation script.

Try other modifications to the prompt template, or try different models, to see how the changes affect the evaluation results.

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

## Related content

- [Learn more about the Azure AI Foundry SDK](../how-to/develop/sdk-overview.md)
