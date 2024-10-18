---
title: GenAIOps with prompt flow and GitHub
titleSuffix: Azure Machine Learning
description: Use Azure Machine Learning to set up an end-to-end GitHub and GenAIOps pipeline that runs a web classification prompt flow.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: chenlujiao
ms.date: 10/17/2024
---

# GenAIOps with prompt flow and GitHub

As the demand for LLM-infused applications soars, organizations need of a cohesive and streamlined process to manage the end-to-end lifecycle of these apps. Generative Artificial Intelligence Operations (GenAIOps), sometimes called *LLMOps*, has become the cornerstone of efficient prompt engineering and LLM-infused application development and deployment.

This article shows how Azure Machine Learning lets you integrate with GitHub to automate the LLM-infused application development lifecycle with prompt flow. Prompt flow provides a streamlined and structured approach to developing LLM-infused applications. Its well-defined process and lifecycle guide you through the process of building, testing, optimizing, and deploying flows, culminating in the creation of fully functional LLM-infused solutions.

## GenAIOps prompt flow features

GenAIOps with prompt flow uses a GenAIOps template and guidance to help you build LLM-infused apps by using prompt flow. GenAIOps with prompt flow has capabilities for simple or complex LLM-infused apps, and is customizable to the needs of the application.

GenAIOps with prompt flow provides the following features:

- **Centralized code hosting**. The repository supports hosting code for multiple prompt flows, providing a single repository for all your flows. This repo is like a library for your flows, making it easy to find, access, and collaborate on different projects.

- **Lifecycle management**. Each flow has its own lifecycle, providing a smooth transition from local experimentation to production deployment.

- **Variant and hyperparameter experimentation**. Variants and hyperparameters are like ingredients in a recipe. The platform allows you to experiment with different combinations of variants across multiple nodes in a flow. Experiment with multiple variants and hyperparameters to easily evaluate flow variants.

- **Multiple deployment targets**. The platform supports deployment of flows to Azure App Services, Kubernetes, Azure Managed computes, driven through configuration to ensure that your flows can scale as needed. The platform also generates Docker images infused with your flow and compute session for deployment to any target platform and operating system that supports Docker.

  :::image type="content" source="./media/how-to-end-to-end-azure-devops-with-prompt-flow/endpoints.png" alt-text="Screenshot of endpoints." lightbox = "./media/how-to-end-to-end-azure-devops-with-prompt-flow/endpoints.png":::

- **A/B deployment**. Seamlessly implement A/B deployments,letting you easily compare different flow versions. This platform facilitates A/B deployment for prompt flow as in traditional website A/B testing. You can easily compare different versions of a flow in a real-world setting to determine which version performs best.

    :::image type="content" source="./media/how-to-end-to-end-azure-devops-with-prompt-flow/a-b-deployments.png" alt-text="Screenshot of deployments." lightbox = "./media/how-to-end-to-end-azure-devops-with-prompt-flow/a-b-deployments.png":::

- **Many-to-many dataset to flow relationships**. Accommodate multiple datasets for each standard and evaluation flow, ensuring versatility in flow test and evaluation. The platform is designed to accommodate multiple datasets for each flow.

- **Conditional data and model registration**. The platform creates a new dataset version for the Azure Machine Learning data asset and flows in the model registry only when there's a change in them.

- **Comprehensive reporting**. Generate detailed reports for each variant configuration, allowing you to make informed decisions. The platform provides detailed metrics collection, experiments, and variant bulk runs for all runs and experiments, enabling data-driven decisions for CSV and HTML files.

  :::image type="content" source="./media/how-to-end-to-end-azure-devops-with-prompt-flow/metrics.png" alt-text="Screenshot of metrics report." lightbox = "./media/how-to-end-to-end-azure-devops-with-prompt-flow/metrics.png":::

GenAIOps with prompt flow provides the following other features for customization:

- **Bring-your-own-flows (BYOF)** provides a complete platform for developing multiple use-cases related to LLM-infused applications.
- **Configuration based development** means there's no need to write extensive boilerplate code.
- **Prompt experimentation and evaluation** executes both locally and in the cloud.
- **Notebooks for local prompt evaluation** provide a library of functions for local experimentation.
- **Endpoint testing** within the pipeline after deployment checks endpoint availability and readiness.
- **Optional human-in-loop** validates prompt metrics before deployment.

## GenAIOps stages

The GenAIOps lifecycle comprises four distinct stages:

- **Initialization**. Clearly define the business objective, gather relevant data samples, establish a basic prompt structure, and craft a flow that enhances its capabilities.

- **Experimentation**. Apply the flow to sample data, assess the prompt's performance, and refine the flow as needed. Continuously iterate until satisfied with the results.

- **Evaluation and refinement**. Benchmark the flow's performance using a larger dataset, evaluate the prompt's effectiveness, and make refinements accordingly. Progress to the next stage if the results meet the desired standards.

- **Deployment**. Optimize the flow for efficiency and effectiveness, deploy it in a production environment including A/B deployment, monitor its performance, gather user feedback, and use this information to further enhance the flow.

By adhering to this structured methodology, prompt flow empowers you to confidently develop, rigorously test, fine-tune, and deploy flows, leading to the creation of robust and sophisticated AI applications.

The GenAIOps Prompt Flow template formalizes this structured methodology by using a code-first approach and helps you build LLM-infused apps using prompt flow tools and process and the [GenAIOps prompt flow features](#genaiops-prompt-flow-features). The repository for this template is available at [GenAIOps with prompt flow template](https://github.com/microsoft/llmops-promptflow-template).

## GenAIOps process flow

:::image type="content" source="./media/how-to-end-to-end-llmops-with-prompt-flow/large-language-model-operations-prompt-flow-process.png" alt-text="Screenshot of GenAIOps prompt flow process." lightbox = "./media/how-to-end-to-end-llmops-with-prompt-flow/large-language-model-operations-prompt-flow-process.png":::

1. In the initialization stage, you develop flows, prepare and curate data, and update GenAIOps related configuration files.
1. After local development using Visual Studio Code with the Prompt Flow extension, you raise a pull request (PR) from the feature branch to the development branch, which executes the build validation pipeline and the experimentation flows.
1. The PR is manually approved and code is merged to the development branch.
1. After the PR merges to the development branch, the continuous integration (CI) pipeline for the dev environment executes. The CI pipeline executes both the experimentation and evaluation flows in sequence and registers the flows in the Azure Machine Learning Registry apart from other steps in the pipeline.
1. After the CI pipeline execution completes, a continuous deployment (CD) trigger executes the CD pipeline, which deploys the standard flow from Azure Machine Learning Registry as an Azure Machine Learning online endpoint. The pipeline then runs integration and smoke tests on the deployed flow.
1. A release branch is created from the development branch, or a PR is raised from the development branch to the release branch.
1. The PR is manually approved and code is merged to the release branch. After the PR is merged to the release branch, the CI pipeline for the prod environment executes. The pipeline executes both the experimentation and evaluation flows in sequence and registers the flows in Azure Machine Learning Registry apart from other steps in the pipeline.
1. After the CI pipeline execution completes, a CD trigger executes the CD pipeline, which deploys the standard flow from Azure Machine Learning Registry as an Azure Machine Learning online endpoint. The pipeline then runs integration and smoke tests on the deployed flow.

## Create a GenAIOps prompt flow

In the rest of this article, you can learn GenAIOps with prompt flow by following the end-to-end samples provided, which help you build LLM-infused applications using prompt flow and GitHub. The primary objective is to provide assistance in the development of these applications by using the capabilities of prompt flow and GenAIOps.

### Prerequisites

- An Azure subscription with the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/).
- An Azure Machine Learning workspace.
- [Git version 2.27 or newer](https://git-scm.com/downloads) running on your local machine, with a GitHub source control repository.
- An understanding of [how to integrate GenAIOps with prompt flow](how-to-integrate-with-llm-app-devops.md).

### Set up a prompt flow connection

Prompt flow uses a connection resource to connect to Azure OpenAI, OpenAI, or Azure AI Search endpoints. You can create a connection through the prompt flow portal UI or by using the REST API. For more information, see [Connections in prompt flow](./concept-connections.md).

Follow the instructions at [Set up connections for prompt flow](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/Azure_devops_how_to_setup.md#setup-connections-for-prompt-flow) to create the connection. The sample flows use a connection called `aoai`, so give your connection that name.

### Set up a compute session

Prompt flow uses a compute session to execute the flow. Create and start the compute session before you execute the prompt flow.

### Set up the GitHub repository

Follow the instructions at [Set up the GitHub repo](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#set-up-github-repo) to create a forked repo in your GitHub organization. This repo uses two branches, `main` and `development`, for code promotions and pipeline execution.

Follow the instructions at [Clone the repo](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#cloning-the-repo) to create a new local repository. This clone helps you create a new feature branch from the development branch and incorporate changes.

### Set up authentication between GitHub and Azure

Follow the instructions at [Set up authentication with Azure and GitHub](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#set-up-authentication-with-azure-and-github) to use a previously-created service principal to set up authentication between the GitHub repository and Azure services.

This step configures a GitHub secret that stores the service principal information. The workflows in the repository can read the connection information by using the secret name to connect to Azure automatically. For more information, see [Use GitHub Actions to connect to Azure](/azure/developer/github/connect-from-azure).

### Test the pipeline

Follow the instructions at [How to set up the repo with Github Workflows](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#cloning-the-repos) to test the pipelines. The process involves the following steps:

1. You raise a PR from a feature branch to the development branch.
1. The PR pipeline executes automatically due to the branch policy configuration.
1. The PR is merged to the development branch.
1. The associated `dev` pipeline executes, resulting in full CI and CD execution and provisioning or updating of the Azure Machine Learning endpoints.

The outputs should look similar to those at [Example prompt run, evaluation, and deployment scenario](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#example-prompt-run-evaluation-and-deployment-scenario).

### Use local execution

To use the capabilities of local execution, follow these steps.

1. Clone the repository as follows:

   ```bash
   git clone https://github.com/microsoft/llmops-promptflow-template.git
   ```

1. Create an *.env* file at the top folder level and add the following lines. Update the values for `<experiment name`>, `<connection name>`, `<api key>` and `<api base or endpoint>`. All the flow examples in the example repo use the AzureOpenAI connection named `aoai`. Add connection names as needed.

   ```bash
   experiment_name=<experiment name>
   <connection name 1>={ "api_key": "<api key>","api_base": "<api base or endpoint>","api_type": "azure","api_version": "2023-03-15-preview"}
   <connection name 2>={ "api_key": "<api key>","api_base": "<api base or endpoint>","api_type": "azure","api_version": "2023-03-15-preview"}
   ```
1. Prepare the local conda or virtual environment to install the dependencies.

   ```bash
   python -m pip install promptflow promptflow-tools promptflow-sdk jinja2 promptflow[azure] openai promptflow-sdk[builtins] python-dotenv
   ```

1. Bring or write your flows into the template based on instructions at [How to onboard new flows](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/how_to_onboard_new_flows.md).

1. Write Python scripts similar to the provided examples in the *local_execution* folder.

## Related content

- [GenAIOps with prompt flow template](https://github.com/microsoft/llmops-promptflow-template)
- [Prompt flow open source repository](https://github.com/microsoft/promptflow)
- [Install and set up Python SDK v2](/python/api/overview/azure/ai-ml-readme)
- [Install and set up Python CLI v2](../how-to-configure-cli.md)
