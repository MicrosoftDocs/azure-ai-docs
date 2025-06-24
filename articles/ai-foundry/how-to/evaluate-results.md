---
title: View Evaluation Results in the Azure AI Foundry Portal
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to view evaluation results in the Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 05/19/2025
ms.reviewer: mithigpe
ms.author: lagayhar
author: lgayhardt
---

# View evaluation results in the Azure AI Foundry portal

You can use the Azure AI Foundry portal evaluation page to visualize and assess your results. You can use it as a control center to optimize, troubleshoot, and select the ideal AI model for your deployment needs. The portal can help you with data-driven decision-making and performance enhancement in your Azure AI Foundry projects. You can access and interpret the results from various sources, including your flow, the playground quick test session, evaluation submission UI, and SDK. You have the flexibility to interact with your results in a way that best suits your workflow and preferences.

After you visualize your evaluation results, you can dive into a thorough examination. You can view individual results and compare these results across multiple evaluation runs. You can identify trends, patterns, and discrepancies, which helps you gain invaluable insights into the performance of your AI system under various conditions.

In this article, you learn how to:

- View evaluation result and metrics.
- Compare evaluation results.
- Improve performance.

## Find your evaluation results

After you submit your evaluation, you can locate the submitted evaluation run within the run list. Navigate to the **Evaluation** page.

You can monitor and manage your evaluation runs within the run list. You have the flexibility to modify the columns by using the column editor and implement filters, and you can customize and create your own version of the run list. Additionally, you can swiftly review the aggregated evaluation metrics across the runs and perform quick comparisons.

:::image type="content" source="../media/evaluations/view-results/evaluation-run-list.png" alt-text="Screenshot that shows the evaluation run list." lightbox="../media/evaluations/view-results/evaluation-run-list.png":::

> [!TIP]
> You can view an evaluation run with any version of the `promptflow-evals` SDK or `azure-ai-evaluation` versions 1.0.0b1, 1.0.0b2, 1.0.0b3. Enable the **Show all runs** toggle to locate the run.

For a deeper understanding of how evaluation metrics are derived, you can access a comprehensive explanation by selecting the **Learn more about metrics** option. This detailed resource provides insights into the calculation and interpretation of the metrics that are used in the evaluation process.

:::image type="content" source="../media/evaluations/view-results/learn-more-metrics.png" alt-text="Screenshot that shows details of the evaluation metrics." lightbox="../media/evaluations/view-results/learn-more-metrics.png":::

When you review the table of evaluation runs, you can select a specific one, which takes you to the run detail page. Here, you can access comprehensive information, including evaluation details such as test dataset, task type, prompt, temperature, and more. You can also view the metrics associated with each data sample. The metrics dashboard provides a visual representation of the pass rate for a dataset across each metric tested.

[!INCLUDE [FDP-backward-compatibility-azure-openai](../includes/fdp-backward-compatibility-azure-openai.md)]

### Metric dashboard

In the **Metric dashboard** section, aggregate views are broken down by metrics that include **AI quality (AI Assisted)**, **Risk and safety (preview)**, **AI Quality (NLP)**, and **Custom** (when applicable). Results are measured as percentages of pass/fail based on the criteria selected when the evaluation was created. For more in-depth information on metric definitions and how they're calculated, see [What are evaluators?](../concepts/observability.md#what-are-evaluators).

- For **AI quality (AI Assisted)** metrics, results are aggregated by calculating an average across all the scores for each metric. If you calculate by using the **Groundedness Pro** metric, the output is binary and the aggregated score is passing rate, which is calculated by `(#trues / #instances) × 100`.
    :::image type="content" source="../media/evaluations/view-results/ai-quality-ai-assisted-chart.png" alt-text="Screenshot that shows the AI quality (AI Assisted) metrics dashboard tab." lightbox="../media/evaluations/view-results/ai-quality-ai-assisted-chart.png":::
- For **Risk and safety (preview)** metrics, results are aggregated by calculating a defect rate for each metric.
  - For content harm metrics, the defect rate is defined as the percentage of instances in your test dataset that surpass a threshold on the severity scale over the whole dataset size. By default, the threshold value is `Medium`.
  - For protected material and indirect attack, the defect rate is calculated as the percentage of instances where the output is `true` by using the formula `(Defect Rate = (#trues / #instances) × 100)`.
    :::image type="content" source="../media/evaluations/view-results/risk-and-safety-chart.png" alt-text="Screenshot that shows the risk and safety metrics dashboard tab." lightbox="../media/evaluations/view-results/risk-and-safety-chart.png":::
- For **AI quality (NLP)** metrics, results are aggregated by calculating an average across all the scores for each metric.
     :::image type="content" source="../media/evaluations/view-results/ai-quality-nlp-chart.png" alt-text="Screenshot that shows the AI quality (NLP) dashboard tab." lightbox="../media/evaluations/view-results/ai-quality-nlp-chart.png":::

### Detailed metrics result table

Within the data section, you can conduct a comprehensive examination of each individual data sample and the associated metrics. Here, you can scrutinize the generated output and its corresponding evaluation metric score. You can also see if it passed based on the passing grade when the test was run. With this level of detail, you can make data-driven decisions and take specific actions to improve your model's performance.

Some potential action items based on the evaluation metrics could include:

- **Pattern recognition**: By filtering for numerical values and metrics, you can drill down to samples with lower scores. Investigate these samples to identify recurring patterns or issues in your model's responses. For one example, you might notice that low scores often occur when the model generates content on a certain topic.
- **Model refinement**: Use the insights from lower-scoring samples to improve the system prompt instruction or fine-tune your model. If you observe consistent issues with, for example, coherence or relevance, you can also adjust the model's training data or parameters accordingly.
- **Column customization**: You can use the column editor to create a customized view of the table, focusing on the metrics and data that are most relevant to your evaluation goals. The column editor can streamline your analysis and help you spot trends more effectively.
- **Keyword search**: You can use the search box to look for specific words or phrases in the generated output, and to pinpoint issues or patterns related to particular topics or keywords. Then, you can address them specifically.

The metrics detail table offers a wealth of data that can guide your model improvement efforts. You can recognize patterns, customize your view for efficient analysis, and refine your model based on identified issues.

Here are some examples of the metrics results for the question-answering scenario:

:::image type="content" source="../media/evaluations/view-results/metrics-details-qa.png" alt-text="Screenshot that shows metrics results for the question-answering scenario." lightbox="../media/evaluations/view-results/metrics-details-qa.png":::

Some evaluations have sub-evaluators, which allow you to view the JSON of the results from the sub-evaluations. To view the results, select **View in JSON**.

:::image type="content" source="../media/evaluations/view-results/evaluation-view-json.png" alt-text="Screenshot that shows detailed metrics results with JSON selected." lightbox="../media/evaluations/view-results/evaluation-view-json.png":::

View the JSON in the **JSON Preview**:

:::image type="content" source="../media/evaluations/view-results/evaluation-view-sub-evaluators.png" alt-text="Screenshot that shows the JSON preview." lightbox="../media/evaluations/view-results/evaluation-view-sub-evaluators.png":::

Here are some examples of the metrics results for the conversation scenario. To review the results throughout a multi-turn conversation, select **View evaluation results per turn** in the **Conversation** column.

:::image type="content" source="../media/evaluations/view-results/evaluation-view-multi-turn-button.png" alt-text="Screenshot that shows metrics results for the conversation scenario." lightbox="../media/evaluations/view-results/evaluation-view-multi-turn-button.png":::

When you select **View evaluation results per turn**, you see the following screen:

:::image type="content" source="../media/evaluations/view-results/metric-per-turn.png" alt-text="Screenshot that shows the evaluation results per turn." lightbox="../media/evaluations/view-results/metric-per-turn.png":::

For a safety evaluation in a multi-modal scenario (text and images), you can better understand the evaluation result by reviewing the images from both the input and output in the detailed metrics result table. Because multi-modal evaluation is currently supported only for conversation scenarios, you can select **View evaluation results per turn** to examine the input and output for each turn.  

:::image type="content" source="../media/evaluations/view-results/image-per-turn-pop-up.png" alt-text="Screenshot that shows the image dialog from the conversation column." lightbox="../media/evaluations/view-results/image-per-turn-pop-up.png":::

Select the image to expand and view it. By default, all images are blurred to protect you from potentially harmful content. To view the image clearly, turn on the **Check blur image** toggle.

:::image type="content" source="../media/evaluations/view-results/image-check-blur-image.png" alt-text="Screenshot that shows a blurred image and the Check blur image toggle." lightbox="../media/evaluations/view-results/image-check-blur-image.png":::

Evaluation results might have different meanings for different audiences. For example, safety evaluations might generate a label for **Low** severity of violent content that might not align to a human reviewer's definition of how severe that specific violent content might be. The passing grade set during the creation of the evaluation determines whether a pass or fail is assigned. There's a **Human feedback** column where you can select a thumbs up or thumbs down icon as you review your evaluation results. You can use this column to log which instances were approved or flagged as incorrect by a human reviewer.

:::image type="content" source="../media/evaluations/view-results/risk-safety-metric-human-feedback.png" alt-text="Screenshot that shows risk and safety metrics results with human feedback." lightbox="../media/evaluations/view-results/risk-safety-metric-human-feedback.png":::

To understand each content risk metric, you can view metric definitions by navigating back to the **Report** section, or you can review the test in the **Metric dashboard** section.

If there's something wrong with the run, you can also use the logs to debug your evaluation run.

Here are some examples of logs that you can use to debug your evaluation run:

:::image type="content" source="../media/evaluations/view-results/evaluation-log.png" alt-text="Screenshot that shows logs that you can use to debug your evaluation run." lightbox="../media/evaluations/view-results/evaluation-log.png":::

If you're evaluating a prompt flow, you can select the **View in flow** button to go to the evaluated flow page and update your flow. For example, you can add extra meta prompt instructions, or change some parameters and reevaluate.  

## Compare the evaluation results

To facilitate a comprehensive comparison between two or more runs, you can select the desired runs and initiate the process. Select either the **Compare** button or, for a general detailed dashboard view, the **Switch to dashboard view** button. You're empowered to analyze and contrast the performance and outcomes of multiple runs, allowing for more informed decision making and targeted improvements.

:::image type="content" source="../media/evaluations/view-results/evaluation-list-compare.png" alt-text="Screenshot that shows the option to compare evaluations." lightbox="../media/evaluations/view-results/evaluation-list-compare.png":::

In the dashboard view, you have access to two valuable components: the metric distribution comparison **Chart** and the comparison **Table**. You can use these tools to perform a side-by-side analysis of the selected evaluation runs. You can compare various aspects of each data sample with ease and precision.

> [!NOTE]
> Older evaluation runs will, by default, have matching rows between columns. However, newly run evaluations have to be intentionally configured to have matching columns during evaluation creation. Ensure the same name is used as the **Criteria Name** across all evaluations you want to compare.

The following screenshot shows the experience when the fields are the same:  

:::image type="content" source="../media/evaluations/view-results/evaluation-criteria-name-match.png" alt-text="Screenshot that shows automated evaluations when the fields are the same." lightbox="../media/evaluations/view-results/evaluation-criteria-name-match.png":::

When a user doesn't use the same **Criteria Name** in creating the evaluation, fields don't match, which causes the platform to be unable to directly compare the results:

:::image type="content" source="../media/evaluations/view-results/evaluation-criteria-name-mismatch.png" alt-text="Screenshot that shows automated evaluations when the fields aren't the same." lightbox="../media/evaluations/view-results/evaluation-criteria-name-mismatch.png":::

Within the comparison **Table**, you can establish a baseline for your comparison by hovering over the specific run you want to use as the reference point and set as baseline. You can also activate the **Show delta** toggle to readily visualize the differences between the baseline run and the other runs for numerical values. Additionally, you can select the **Show only difference** toggle so that the table displays only the rows that differ among the selected runs, aiding in the identification of distinct variations.

By using these comparison features, you can make an informed decision to select the best version:

- **Baseline comparison**: By setting a baseline run, you can identify a reference point against which to compare the other runs. You can see how each run deviates from your chosen standard.
- **Numerical value assessment**: Enabling the **Show delta** option helps you understand the extent of the differences between the baseline and other runs. This information can help you evaluate how various runs perform in terms of specific evaluation metrics.
- **Difference isolation**: The **Show only difference** feature streamlines your analysis by highlighting only the areas where there are discrepancies between runs. This information can be instrumental in pinpointing where improvements or adjustments are needed.

By using these comparison tools effectively, you can identify which version of your model or system performs the best in relation to your defined criteria and metrics, ultimately assisting you in selecting the most optimal option for your application.

:::image type="content" source="../media/evaluations/view-results/comparison-table.png" alt-text="Screenshot that shows side-by-side evaluation results." lightbox="../media/evaluations/view-results/comparison-table.png":::

## Measure jailbreak vulnerability

Evaluating jailbreak vulnerability is a comparative measurement, not an AI-assisted metric. Run evaluations on two different, red-teamed datasets: a baseline adversarial test dataset versus the same adversarial test dataset with jailbreak injections in the first turn. You can use the adversarial data simulator to generate the dataset with or without jailbreak injections. Ensure the **Criteria Name** is the same for each evaluation metric when you configure the runs.

To understand if your application is vulnerable to jailbreak, you can specify the baseline and then turn on the **Jailbreak defect rates** toggle in the comparison table. The jailbreak defect rate is the percentage of instances in your test dataset where a jailbreak injection generated a higher severity score for *any* content risk metric with respect to a baseline over the whole dataset size. You can select multiple evaluations in your **Compare** dashboard to view the difference in defect rates.

:::image type="content" source="../media/evaluations/view-results/evaluation-compare-jailbreak.png" alt-text="Screenshot that shows side-by-side evaluation results with jailbreak defect toggled on." lightbox="../media/evaluations/view-results/evaluation-compare-jailbreak.png":::

> [!TIP]
> Jailbreak defect rate is comparatively calculated only for datasets of the same size and only when all runs include content risk and safety metrics.

## Understand the built-in evaluation metrics

Understanding the built-in metrics is vital for assessing the performance and effectiveness of your AI application. By gaining insights into these key measurement tools, you're better equipped to interpret the results, make informed decisions, and fine-tune your application to achieve optimal outcomes. Refer to [Evaluation and Monitoring Metrics](../concepts/evaluation-metrics-built-in.md) to learn more about the following aspects:

- The significance of each metric
- How it's calculated
- Its role in evaluating different aspects of your model
- How to interpret the results to make data-driven improvements

## Related content

Learn more about how to evaluate your generative AI applications:

- [Evaluate your generative AI apps via the playground](../how-to/evaluate-prompts-playground.md)
- [Evaluate your generative AI apps with the Azure AI Foundry portal or SDK](../how-to/evaluate-generative-ai-app.md)
- [Create evaluations specifically with OpenAI evaluation graders in Azure OpenAI Hub](../../ai-services/openai/how-to/evaluations.md)

Learn more about [harm mitigation techniques](../concepts/evaluation-approach-gen-ai.md).
