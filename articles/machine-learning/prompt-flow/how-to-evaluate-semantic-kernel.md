---
title: Evaluate Semantic Kernel with prompt flow
titleSuffix: Azure Machine Learning
description: Learn how to use a prompt flow to evaluate Semantic Kernel in Azure Machine Learning studio.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar
ms.date: 08/28/2026
ms.update-cycle: 365-days
ai-usage: ai-assisted
---

# Evaluate Semantic Kernel with prompt flow

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

This article describes the integration between prompt flow and [Semantic Kernel](/semantic-kernel/overview/), and demonstrates how to evaluate Semantic Kernel plugins and orchestration code by using prompt flow.

Semantic Kernel is an open-source SDK that lets you combine AI services with programming languages like C# and Python. Semantic Kernel provides [plugins](/semantic-kernel/ai-orchestration/plugins) and automatic function calling to orchestrate operations.

As you add plugins and function calls, test that they work as intended. You can use prompt flow to automate this process for an existing application.

> [!IMPORTANT]
> Semantic Kernel's Stepwise and Handlebars planners are deprecated and have been removed from current packages. The planner-based workflow shown in this article is for evaluating a legacy implementation. For current Semantic Kernel applications, use [automatic function calling](/semantic-kernel/concepts/planning#using-automatic-function-calling).

The integration of Semantic Kernel with prompt flow allows you to:

- Harness the powerful AI orchestration capabilities of Semantic Kernel to enhance the efficiency and effectiveness of your prompt flows.
- Use prompt flow evaluation and experiment management to assess the quality of your Semantic Kernel plugins and orchestration code.

## Prerequisites

- Before you start developing the flow, add the [Semantic Kernel package](/semantic-kernel/get-started/quick-start-guide/?toc=%2Fsemantic-kernel%2Ftoc.json&tabs=python) to your *requirements.txt* so the executor can install it. For more information, see [Manage prompt flow compute session](how-to-manage-compute-session.md).

- To use Semantic Kernel to consume Azure OpenAI or OpenAI resources in a prompt flow, create a custom connection.

  1. Put the keys you specified for the resources in environment variables or an *.env* file.

  1. Select **Create** from the **Connection** tab on the Azure Machine Learning studio **Prompt flow** page, and select **Custom** provider.

  1. Convert the keys from environment variables to key-value pairs in the custom connection. 

     :::image type="content" source="./media/how-to-evaluate-semantic-kernel/custom-connection-for-semantic-kernel.png" alt-text="Screenshot of custom connection." lightbox = "./media/how-to-evaluate-semantic-kernel/custom-connection-for-semantic-kernel.png":::

  You can now use this custom connection to invoke your Azure OpenAI or OpenAI model within the flow.

## Create a flow with Semantic Kernel

Similar to the [integration of LangChain with prompt flow](how-to-integrate-with-langchain.md), Semantic Kernel supports Python and can operate in a Python node within a prompt flow.

:::image type="content" source="./media/how-to-evaluate-semantic-kernel/prompt-flow-end-result.png" alt-text="Diagram of prompt flow with Semantic Kernel." border="false":::

For this legacy example, you create a flow with a Semantic Kernel planner that solves math problems. For a current implementation, replace the planner with automatic function calling and evaluate its outputs by using the same batch-testing approach.

1. From the **Prompt flow** page, select **Create**.
1. On the **Create a new flow** screen, select **Create** in the **Standard flow** tile.
1. At the top of the new flow, select **+ Python** to create a new Python node, and name the node *math_planner*.
1. Select **+** at the top of the **Files** tab to upload reference files such as the MathPlugin from the Semantic Kernel package.
1. Update the *math_planner.py* code to set up the connection and define the input and output of the planner node.

   :::image type="content" source="./media/how-to-evaluate-semantic-kernel/set-connection-in-python.png" alt-text="Screenshot of setting custom connection in python node.":::

1. Select the **Connection** object in the node input, and set the **deployment_name** for Azure OpenAI or **model_name** for OpenAI.

   :::image type="content" source="./media/how-to-evaluate-semantic-kernel/set-key-model.png" alt-text="Screenshot of setting model and key in node input.":::
   
1. Start the compute session, and select **Run** for a single test.

   :::image type="content" source="./media/how-to-evaluate-semantic-kernel/semantic-kernel-flow.png" alt-text="Screenshot of creating a flow with semantic kernel planner." lightbox = "./media/how-to-evaluate-semantic-kernel/semantic-kernel-flow.png":::

## Batch test your plugins and orchestration

Instead of manually testing each different scenario, you can automatically run large batches of tests by using prompt flow and benchmark data.

Use batches with prompt flow to run batch tests on your orchestration code that uses the math plugin. By defining several word problems, you can quickly test changes to your plugins or function calls so you catch regressions early.

:::image type="content" source="./media/how-to-evaluate-semantic-kernel/using-batch-runs-with-prompt-flow.png" alt-text="Diagram showing batch runs with prompt flow for Semantic Kernel." border="false":::

After your flow passes a single test run, you can create a batch test in prompt flow.

1. Create your benchmark data in a *.jsonl* file as a list of JSON objects that contain the input and the correct ground truth.
1. In the prompt flow, select **Evaluate** from the top menu.
1. Complete the **Basic settings**, upload your data file, and complete the **Batch run settings**.
1. For this test, skip the optional **Evaluation settings** and select **Review + submit**, and then select **Submit** to submit the batch run.

   :::image type="content" source="./media/how-to-evaluate-semantic-kernel/semantic-kernel-test-data.png" alt-text="Screenshot of data of batch runs with prompt flow for Semantic Kernel." lightbox = "./media/how-to-evaluate-semantic-kernel/semantic-kernel-test-data.png":::

1. When the run finishes, select the run name on the prompt flow **Runs** page.

   :::image type="content" source="./media/how-to-evaluate-semantic-kernel/run.png" alt-text="Screenshot of the run list." lightbox = "./media/how-to-evaluate-semantic-kernel/run.png":::

1. At the top of the run page, select **Details**.

   :::image type="content" source="./media/how-to-evaluate-semantic-kernel/run-detail.png" alt-text="Screenshot of the run detail." lightbox = "./media/how-to-evaluate-semantic-kernel/run-detail.png":::

1. On the **Details** page, select the **Outputs** tab to see the results.

   :::image type="content" source="./media/how-to-evaluate-semantic-kernel/run-output.png" alt-text="Screenshot of the run output." lightbox = "./media/how-to-evaluate-semantic-kernel/run-output.png":::

## Evaluate accuracy

After you complete a batch run, you need an easy way to determine the adequacy of the test results. Use this information to develop accuracy scores that you can incrementally improve.

:::image type="content" source="./media/how-to-evaluate-semantic-kernel/evaluation-batch-run-with-prompt-flow.png" alt-text="Diagram of evaluating batch run with prompt flow." border="false":::

Evaluation flows in prompt flow enable this functionality. By using the sample evaluation flows, you can assess various metrics such as *classification accuracy*, *perceived intelligence*, and *groundedness*. You can also develop your own custom evaluators if needed.

:::image type="content" source="./media/how-to-evaluate-semantic-kernel/evaluation-sample-flows.png" alt-text="Screenshot showing evaluation flow samples." lightbox = "./media/how-to-evaluate-semantic-kernel/evaluation-sample-flows.png":::

You can quickly create an evaluation run based on a completed batch run.

1. Open your previously completed batch run, and select **Evaluate** from the top menu.
1. On **New evaluation**, select an evaluator to use, select **Next**, and configure the input mapping. Then, select **Submit**.

   :::image type="content" source="./media/how-to-evaluate-semantic-kernel/evaluation-setting.png" alt-text="Screenshot showing evaluation settings." lightbox = "./media/how-to-evaluate-semantic-kernel/evaluation-setting.png":::

After the evaluator runs, it returns a summary of results and metrics. Use runs that yield less than ideal results as motivation for immediate improvement.

To view results, select **Details** at the top of the evaluator flow run page. On **Details**, select the **Outputs** tab to view evaluation output.

:::image type="content" source="./media/how-to-evaluate-semantic-kernel/evaluation-result.png" alt-text="Screenshot showing evaluation result." lightbox = "./media/how-to-evaluate-semantic-kernel/evaluation-result.png":::

You can check the aggregated metric in the **Metrics** tab.

## Experiment for quality improvement

If your plugins and orchestration code aren't performing as expected, take steps to improve them. The following high-level recommendations can help:

- Use a current model that supports function calling and is available in your Azure OpenAI deployment.
- Improve your plugin descriptions so they're easier for the model to use.
- Provide clear instructions and representative context in the user request.

A combination of these actions can improve orchestration results. Use the enhancement and evaluation process to validate results against your benchmark data.

Throughout the process of enhancing your plugins and orchestration code in prompt flow, use the runs to monitor your experimental progress. Each iteration allows you to submit a batch run with an evaluation run at the same time.

:::image type="content" source="./media/how-to-evaluate-semantic-kernel/batch-evaluation.png" alt-text="Screenshot of batch run with evaluation." lightbox = "./media/how-to-evaluate-semantic-kernel/batch-evaluation.png":::

This capability enables you to conveniently compare the results of various runs, helping you identify which modifications are beneficial. To compare, select the runs you want to analyze, and then select **Visualize outputs**.

:::image type="content" source="./media/how-to-evaluate-semantic-kernel/compare.png" alt-text="Screenshot of compare runs." lightbox = "./media/how-to-evaluate-semantic-kernel/compare.png":::

The **Visualize outputs** screen shows a detailed table with a line-by-line comparison of the results from selected runs.

:::image type="content" source="./media/how-to-evaluate-semantic-kernel/compare-detail.png" alt-text="Screenshot of compare runs details." lightbox = "./media/how-to-evaluate-semantic-kernel/compare-detail.png":::

## Related content

- [Semantic Kernel documentation](/semantic-kernel/)
- [What is a Plugin?](/semantic-kernel/ai-orchestration/plugins)
- [Planning with automatic function calling](/semantic-kernel/concepts/planning)
- [Deploy a flow as a managed online endpoint for real-time inference](how-to-deploy-for-real-time-inference.md)
