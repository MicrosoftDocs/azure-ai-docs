---
title: Tune prompts using variants in prompt flow
titleSuffix: Azure Machine Learning
description: Learn how to tune prompts using variants in prompt flow with Azure Machine Learning studio.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - ignite-2023
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar
ms.date: 06/30/2026
ms.update-cycle: 365-days
---

# Tune prompts by using variants

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

Crafting a good prompt is a challenging task that requires creativity, clarity, and relevance. A good prompt elicits the desired output from a pretrained language model, while a bad prompt leads to inaccurate, irrelevant, or nonsensical outputs. Therefore, tune prompts to optimize their performance and robustness for different tasks and domains.

The [concept of variants](concept-variants.md) helps you test the model's behavior under different conditions, such as different wording, formatting, context, temperature, or top-k. You can compare and find the best prompt and configuration that maximizes the model's accuracy, diversity, or coherence.

In this article, you learn how to use variants to tune prompts and evaluate the performance of different variants.

## Prerequisites

Before reading this article, review:

- [Quick Start Guide](get-started-prompt-flow.md)
- [How to bulk test and evaluate a flow](how-to-bulk-test-evaluate-flow.md)

## How do you tune prompts by using variants?

This article uses the **Web Classification** sample flow as an example.

1. Open the sample flow and remove the **prepare_examples** node as a starting point.

    :::image type="content" source="./media/how-to-tune-prompts-using-variants/flow-graph.png" alt-text="Screenshot of Web Classification example flow to demonstrate variants. " lightbox = "./media/how-to-tune-prompts-using-variants/flow-graph.png":::

1. Use the following prompt as a baseline prompt in the **classify_with_llm** node.

```
Your task is to classify a given url into one of the following types:
Movie, App, Academic, Channel, Profile, PDF or None based on the text content information.
The classification will be based on the url, the webpage text content summary, or both.

For a given URL : {{url}}, and text content: {{text_content}}.
Classify above url to complete the category and indicate evidence.

The output shoule be in this format: {"category": "App", "evidence": "Both"} 
OUTPUT:
```

To optimize this flow, you can try multiple approaches. The following two directions are good places to start:

- For the **classify_with_llm** node:
    Community members and research papers say that a lower temperature gives higher precision but less creativity and surprise. So, a lower temperature works best for classification tasks. Also, few-shot prompting can increase LLM performance. Test how your flow behaves when you change the temperature from 1 to 0, and when the prompt includes few-shot examples.

- For the **summarize_text_content** node:
    Test your flow's behavior when you change the summary length from 100 words to 300 words. Check if more text content helps improve the performance.

### Create variants

1. Select **Show variants** button on the upper right of the LLM node. The existing LLM node is `variant_0` and is the default variant.
1. Select the **Clone** button on `variant_0` to generate `variant_1`. Then, you can configure parameters to different values or update the prompt on `variant_1`.
1. Repeat the step to create more variants.
1. Select **Hide variants** to stop adding more variants. All variants are folded. The default variant is shown for the node.

For the **classify_with_llm** node, based on `variant_0`:

- Create `variant_1` where the temperature is changed from 1 to 0.
- Create `variant_2` where temperature is 0 and you can use the following prompt including few-shots examples.


```
Your task is to classify a given url into one of the following types:
Movie, App, Academic, Channel, Profile, PDF or None based on the text content information.
The classification will be based on the url, the webpage text content summary, or both.

Here are a few examples:

URL: https://play.google.com/store/apps/details?id=com.spotify.music 
Text content: Spotify is a free music and podcast streaming app with millions of songs, albums, and original podcasts. It also offers audiobooks, so users can enjoy thousands of stories. It has a variety of features such as creating and sharing music playlists, discovering new music, and listening to popular and exclusive podcasts. It also has a Premium subscription option which allows users to download and listen offline, and access ad-free music. It is available on all devices and has a variety of genres and artists to choose from. 
OUTPUT: {"category": "App", "evidence": "Both"} 
        
URL: https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw 
Text content: NFL Sunday Ticket is a service offered by Google LLC that allows users to watch NFL games on YouTube. It is available in 2023 and is subject to the terms and privacy policy of Google LLC. It is also subject to YouTube's terms of use and any applicable laws. 
OUTPUT: {"category": "Channel", "evidence": "URL"} 
        
URL: https://arxiv.org/abs/2303.04671 
Text content: Visual ChatGPT is a system that enables users to interact with ChatGPT by sending and receiving not only languages but also images, providing complex visual questions or visual editing instructions, and providing feedback and asking for corrected results. It incorporates different Visual Foundation Models and is publicly available. Experiments show that Visual ChatGPT opens the door to investigating the visual roles of ChatGPT with the help of Visual Foundation Models. 
OUTPUT: {"category": "Academic", "evidence": "Text content"} 
        
URL: https://ab.politiaromana.ro/ 
Text content: There is no content available for this text. 
OUTPUT: {"category": "None", "evidence": "None"}
        
For a given URL : {{url}}, and text content: {{text_content}}.
Classify above url to complete the category and indicate evidence.
OUTPUT:    
```

For the **summarize_text_content** node, based on `variant_0`, you can create `variant_1` where `100 words` is changed to `300` words in prompt.

Now, the flow looks as following, two variants for **summarize_text_content** node and three for **classify_with_llm** node.

:::image type="content" source="./media/how-to-tune-prompts-using-variants/variants.png" alt-text="Screenshot of flow authoring page when you have variants in flow. " lightbox = "./media/how-to-tune-prompts-using-variants/3-2-variants.png":::

### Run all variants with a single row of data and check outputs

To make sure all the variants run successfully and work as expected, run the flow with a single row of data to test. 

> [!NOTE]
> Each time, you can only select one LLM node with variants to run while other LLM nodes use the default variant. 

In this example, you configure variants for both **summarize_text_content** node and **classify_with_llm** node, so you need to run twice to test all the variants.

1. Select the **Run** button on the top right.
1. Select an LLM node with variants. The other LLM nodes use the default variant.
    :::image type="content" source="./media/how-to-tune-prompts-using-variants/run-select-variants.png" alt-text="Screenshot of submitting a flow run when you have variants in flow. " lightbox = "./media/how-to-tune-prompts-using-variants/run-select-variants.png":::
1. Submit the flow run.
1. After the flow run completes, check the corresponding result for each variant.
1. Submit another flow run with the other LLM node with variants, and check the outputs.
1. Change the input data (for example, use a Wikipedia page URL) and repeat the preceding steps to test variants for different data.​​​​​​​

### Evaluate variants

When you run the variants with a few single pieces of data and check the results with the naked eye, you can't see the complexity and diversity of real-world data. Meanwhile, the output isn't measurable, so it's hard to compare the effectiveness of different variants and choose the best one.

You can submit a batch run. This process tests the variants with a large amount of data and evaluates them with metrics to help you find the best fit.

1. First, prepare a dataset that's representative enough of the real-world problem you want to solve with prompt flow. In this example, it's a list of URLs and their classification ground truth. Use accuracy to evaluate the performance of variants.
1. Select **Evaluate** in the upper right of the page.
1. A wizard for **Batch run & Evaluate** appears. The first step is to select a node to run all its variants.
  
    To test how well different variants work for each node in a flow, run a batch run for each node with variants one by one. This approach helps you avoid the influence of other nodes' variants and focus on the results of this node's variants. This approach follows the rule of the controlled experiment, which means that you only change one thing at a time and keep everything else the same.

    For example, you can select **classify_with_llm** node to run all variants. The **summarize_text_content** node uses its default variant for this batch run.

1. Next, in **Batch run settings**, set the batch run name, choose a runtime, and upload the prepared data.
1. Next, in **Evaluation settings**, select an evaluation method.

    Since this flow is for classification, select **Classification Accuracy Evaluation** method to evaluate accuracy.
    
    Accuracy is calculated by comparing the predicted labels assigned by the flow (prediction) with the actual labels of data (ground truth) and counting how many of them match.

    In the **Evaluation input mapping** section, specify that ground truth comes from the category column of input dataset, and prediction comes from one of the flow outputs: category.

1. After reviewing all the settings, submit the batch run.
1. After you submit the run, select the link to go to the run detail page.

> [!NOTE]
> The run might take several minutes to complete.

### Visualize outputs

1. After the batch run and evaluation run finish, in the run detail page, select the batch runs for each variant, and then select **Visualize outputs**. You see the metrics of three variants for the **classify_with_llm** node and LLM predicted outputs for each record of data.
   :::image type="content" source="./media/how-to-tune-prompts-using-variants/visualize-outputs.png" alt-text="Screenshot of runs showing visualize outputs. " lightbox = "./media/how-to-tune-prompts-using-variants/3-2-variants.png":::
1. After you identify which variant is the best, go back to the flow authoring page and set that variant as the default variant of the node.
1. You can repeat the preceding steps to evaluate the variants of **summarize_text_content** node.

You finished the process of tuning prompts using variants. You can apply this technique to your own prompt flow to find the best variant for the LLM node.

## Next steps

- [Develop a customized evaluation flow](how-to-develop-an-evaluation-flow.md)
- [Integrate with LangChain](how-to-integrate-with-langchain.md)
- [Deploy a flow](how-to-deploy-for-real-time-inference.md)
