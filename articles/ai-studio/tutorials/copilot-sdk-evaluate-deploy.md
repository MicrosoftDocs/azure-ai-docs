---
title: "Part 3: Evaluate and deploy chat app with the Azure AI SDK"
titleSuffix: Azure AI Studio
description: Evaluate and deploy a custom chat app with the prompt flow SDK. This tutorial is part 3 of a 3-part tutorial series.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: tutorial
ms.date: 11/06/2024
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can evaluate and deploy a chat app.
---

# Tutorial: Part 3 - Evaluate a custom chat application with the Azure AI Foundry SDK

In this tutorial, you use the Azure AI SDK (and other libraries) to  evaluate and deploy the chat app you built in [Part 2 of the tutorial series](copilot-sdk-build-rag.md). In this part three, you learn how to:

> [!div class="checklist"]
> - Evaluate the quality of chat app responses
> - Deploy the chat app to Azure
> - Verify the deployment

This tutorial is part three of a three-part tutorial.

## Prerequisites

- Complete [part 2 of the tutorial series](copilot-sdk-build-rag.md) to build the chat application.


## <a name="evaluate"></a> Evaluate the quality of the chat app responses

Now that you know your chat app responds well to your queries, including with chat history, it's time to evaluate how it does across a few different metrics and more data.

You use an evaluator with an evaluation dataset and the `get_chat_response()` target function, then assess the evaluation results.

Once you run an evaluation, you can then make improvements to your logic, like improving your system prompt, and observing how the chat app responses change and improve.

### Create evaluation dataset

Use the following evaluation dataset, which contains example questions and expected answers (truth).

1. Create a file called **chat_eval_data.jsonl** in your **assets** folder.
1. Paste this dataset into the file:

    :::code language="jsonl" source="~/azureai-samples-nov2024/scenarios/rag/custom-rag-app/assets/chat_eval_data.jsonl":::

### Evaluate with Azure AI evaluators

Now define an evaluation script that will:


- Generate a target function wrapper around our chat app logic.
- Load the sample `.jsonl` dataset.
- Run the evaluation, which takes the target function, and merges the evaluation dataset with the responses from the chat app.
- Generate a set of GPT-assisted metrics (relevance, groundedness, and coherence) to evaluate the quality of the chat app responses.
- Output the results locally, and logs the results to the cloud project.

The script allows you to review the results locally, by outputting the results in the command line, and to a json file.

The script also logs the evaluation results to the cloud project so that you can compare evaluation runs in the UI.

1. Create a file called **evaluate.py** in your **rag-tutorial** folder.
1. Add the following code. Update the `dataset_path` and `evaluation_name` to fit your use case.

    :::code language="python" source="~/azureai-samples-nov2024/scenarios/rag/custom-rag-app/evaluate.py":::

The main function at the end allows you to view the evaluation result locally, and gives you a link to the evaluation results in AI Studio.

### Create helper script

The evaluation script uses a helper script to define the target function and run the evaluation. Create a file called **config.py** in your main folder. Add the following code:

:::code language="python" source="~/azureai-samples-nov2024/scenarios/rag/custom-rag-app/config.py":::

### Configure the evaluation model 

Since the evaluation script calls the evaluation model many times, try to increase the number of tokens per minute that the model will accept.  

1. In your project in Azure AI Studio, select **Models + endpoints**.
1. Select **gpt-4o-mini**.
1. Select **Edit**.
1. If you have quota to increase the **Tokens per Minute Rate Limit**, try increasing it to 30. (If you're out of quota, don't worry.  The script is designed to handle limit errors.)
1. Select **Save and close**.

### Run the evaluation script

1. From your console, sign in to your Azure account with the Azure CLI:

    ```bash
    az login
    ```

1. Install the required packages:

    ```bash
    pip install azure_ai-evaluation[remote]
    ```

1. Now run the evaluation script:

    ```bash
    python evaluate.py
    ```

### Interpret the evaluation output

In the console output, you see for each question an answer and the summarized metrics. (You might see different columns in your output.)

If you weren't able to increase the tokens per minute limit for your model, you might see some time-out errors, which are expected. The evaluation script is designed to handle these errors and continue running.

```txt
====================================================
'-----Summarized Metrics-----'
{'groundedness.gpt_groundedness': 2.230769230769231,
 'groundedness.groundedness': 2.230769230769231}
'-----Tabular Result-----'
                                     outputs.response  ...           outputs.groundedness.groundedness_reason
0   Could you please specify which tent you are as...  ...  The RESPONSE fails to engage with the specific...
1   Could you please specify which camping table y...  ...  The RESPONSE does not utilize any of the infor...
2   Sorry, I only can answer queries related to ou...  ...  The RESPONSE does not relate to the CONTEXT at...
3   To properly care for your TrailWalker Hiking S...  ...  The RESPONSE provides care instructions for th...
4   The TrailMaster X4 Tent is from the OutdoorLiv...  ...  The RESPONSE accurately identifies the brand o...
5   The TrailMaster X4 Tent comes with an included...  ...  The RESPONSE accurately reflects information f...
6   Sorry, I only can answer queries related to ou...  ...  The RESPONSE does not relate to the CONTEXT at...
7   The TrailBlaze Hiking Pants are crafted from h...  ...  The RESPONSE accurately reflects part of the i...
8   The color of the TrailBlaze Hiking Pants is de...  ...  The RESPONSE accurately mentions the color of ...
9   Sorry, I only can answer queries related to ou...  ...  The RESPONSE is entirely unrelated to the CONT...
10  Sorry, I only can answer queries related to ou...  ...  The RESPONSE does not reference or relate to a...
11  The material for the PowerBurner Camping Stove...  ...  The RESPONSE does not contradict the CONTEXT b...
12  Sorry, I only can answer queries related to ou...  ...  The RESPONSE does not reference or relate to a...

[13 rows x 7 columns]
'View evaluation results in AI Studio: xxxxxx'
```

> [!NOTE]
> You may see `WARNING:opentelemetry.attributes:` - these can be safely ignored and do not affect the evaluation results.

### View evaluation results in AI Studio

Once the evaluation run completes, follow the link to view the evaluation results on the **Evaluation** page in the Azure AI Studio.

:::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/eval-studio-overview.png" alt-text="Screenshot shows evaluation overview in Azure AI Studio.":::

You can also look at the individual rows and see metric scores per row, and view the full context/documents that were retrieved. These metrics can be helpful in interpreting and debugging evaluation results.

:::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/eval-studio-rows.png" alt-text="Screenshot shows rows of evaluation results in Azure AI Studio.":::

For more information about evaluation results in AI Studio, see [How to view evaluation results in AI Studio](../how-to/evaluate-results.md).

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

## Related content

- [Learn more about the Azure AI Foundry SDK](../how-to/develop/sdk-overview.md)
