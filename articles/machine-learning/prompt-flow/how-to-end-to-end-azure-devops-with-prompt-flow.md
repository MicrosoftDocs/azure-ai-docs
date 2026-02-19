---
title: GenAIOps with prompt flow and Azure DevOps
titleSuffix: Azure Machine Learning
description: Use Azure Machine Learning to set up an end-to-end Azure DevOps and GenAIOps pipeline to run a prompt flow.
services: machine-learning
author: lgayhardt
ms.author: lagayhar
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
ms.reviewer: sooryar
ms.date: 10/18/2024
ms.custom:
  - cli-v2
  - sdk-v2
  - ignite-2023
  - build-2024
ms.update-cycle: 365-days
---

# GenAIOps with prompt flow and Azure DevOps

As the demand for LLM-infused applications soars, organizations need a cohesive and streamlined process to manage the end-to-end lifecycle of these apps. Generative Artificial Intelligence Operations (GenAIOps), sometimes called *LLMOps*, is a cornerstone of efficient prompt engineering and LLM-infused application development and deployment.

This article shows how Azure Machine Learning lets you integrate with Azure DevOps to automate the LLM-infused application development lifecycle with *prompt flow*. Prompt flow provides a streamlined and structured approach to developing LLM-infused applications. Its well-defined process and lifecycle guide you through the process of building, testing, optimizing, and deploying flows, culminating in the creation of fully functional LLM-infused solutions.

## GenAIOps prompt flow features

[GenAIOps with prompt flow](https://github.com/microsoft/genaiops-promptflow-template) uses a GenAIOps template and guidance to help you build LLM-infused apps by using prompt flow. GenAIOps with prompt flow has capabilities for simple or complex LLM-infused apps, and is customizable to the needs of the application.

The GenAIOps with prompt flow platform provides the following features:

- **Centralized code hosting**. The repository supports hosting code for multiple prompt flows, providing a single repository for all your flows. This repo is like a library for your flows, making it easy to find, access, and collaborate on different projects.

- **Lifecycle management**. Each flow has its own lifecycle, providing a smooth transition from local experimentation to production deployment.

- **Variant and hyperparameter experimentation**. Variants and hyperparameters are like ingredients in a recipe. The platform allows you to experiment with different combinations of variants across multiple nodes in a flow. You can experiment with multiple variants and hyperparameters to easily evaluate flow variants.

- **Multiple deployment targets**. The platform generates Docker images infused with your flow and compute session for deployment to any target platform and operating system that supports Docker. You can deploy flows to Azure App Services, Kubernetes, and Azure Managed computes, and configure them to scale as needed.

- **A/B deployment**. GenAIOps with prompt flow seamlessly implements A/B deployments, letting you easily compare different flow versions. This platform facilitates A/B deployment for prompt flow they same way as in traditional website A/B testing. You can easily compare different versions of a flow in a real-world setting to determine which version performs best.

- **Many-to-many dataset to flow relationships**. GenAIOps with prompt flow accommodates multiple datasets for each standard and evaluation flow, enabling versatility in flow test and evaluation.

- **Conditional data and model registration**. The platform registers a new dataset version for the Azure Machine Learning data asset and flows in the model registry only when there's a change in the dataset.

- **Comprehensive reporting**. GenAIOps with prompt flow generates detailed reports for each variant configuration, allowing you to make informed decisions. The platform provides detailed metrics collection, experiments, and variant bulk runs for all runs and experiments, enabling data-driven decisions for both CSV and HTML files.

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

The GenAIOps Prompt Flow template formalizes this structured methodology by using a code-first approach, and helps you build LLM-infused apps using prompt flow tools and process and GenAIOps prompt flow features. This template is available at [GenAIOps with prompt flow template](https://github.com/microsoft/genaiops-promptflow-template).

## GenAIOps process flow

:::image type="content" source="./media/how-to-end-to-end-azure-devops-with-prompt-flow/large-language-model-operations-prompt-flow-process.png" alt-text="Screenshot of GenAIOps prompt flow process." lightbox = "./media/how-to-end-to-end-azure-devops-with-prompt-flow/large-language-model-operations-prompt-flow-process.png":::

1. In the initialization stage, you develop flows, prepare and curate data, and update GenAIOps related configuration files.
1. After local development using Visual Studio Code with the Prompt Flow extension, you raise a pull request (PR) from the feature branch to the development branch, which executes the build validation pipeline and the experimentation flows.
1. The PR is manually approved and code is merged to the development branch.
1. After the PR merges to the development branch, the continuous integration (CI) pipeline for the dev environment executes. The CI pipeline executes both the experimentation and evaluation flows in sequence and registers the flows in the Azure Machine Learning Registry apart from other steps in the pipeline.
1. After the CI pipeline execution completes, a continuous deployment (CD) trigger executes the CD pipeline, which deploys the standard flow from Azure Machine Learning Registry as an Azure Machine Learning online endpoint. The pipeline then runs integration and smoke tests on the deployed flow.
1. A release branch is created from the development branch, or a PR is raised from the development branch to the release branch.
1. The PR is manually approved and code is merged to the release branch. After the PR is merged to the release branch, the CI pipeline for the production environment executes. The pipeline executes both the experimentation and evaluation flows in sequence and registers the flows in Azure Machine Learning Registry apart from other steps in the pipeline.
1. After the CI pipeline execution completes, a CD trigger executes the CD pipeline, which deploys the standard flow from Azure Machine Learning Registry as an Azure Machine Learning online endpoint. The pipeline then runs integration and smoke tests on the deployed flow.

## Create a GenAIOps prompt flow

The rest of this article shows you how to use GenAIOps with prompt flow by following the end-to-end sample in the [GenAIOps with prompt flow template repository](https://github.com/microsoft/genaiops-promptflow-template), which help you build LLM-infused applications using prompt flow and Azure DevOps. The primary objective is to provide assistance in the development of these applications by using the capabilities of prompt flow and GenAIOps.

### Prerequisites

- An Azure subscription with the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure Machine Learning workspace.
- [Git version 2.27 or newer](https://git-scm.com/downloads) running on your local machine.
- An [Azure DevOps organization](/azure/devops/organizations/accounts/create-organization) where you have the ability to create a project, an Azure Repos source control repository, and Azure Pipelines pipelines. An Azure DevOps organization helps you collaborate, plan and track your work, code, and issues, and set up CI and CD.
- An understanding of [how to integrate GenAIOps with prompt flow](how-to-integrate-with-llm-app-devops.md).

>[!NOTE]
>If you use Azure DevOps and Terraform to spin up infrastructure, you need the [Terraform extension for Azure DevOps](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.custom-terraform-tasks) installed.

### Set up a prompt flow connection

Prompt flow uses a connection resource to connect to Azure OpenAI, OpenAI, or Azure AI Search endpoints. You can create a connection through the prompt flow portal UI or by using the REST API. For more information, see [Connections in prompt flow](./concept-connections.md).

To create the connection, follow the instructions at [Set up connections for prompt flow](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/Azure_devops_how_to_setup.md#setup-connections-for-prompt-flow). The sample flows use a connection called `aoai`, so give your connection that name.

### Set up a compute session

Prompt flow uses a compute session to execute the flow. [Create and start the compute session](/azure/ai-studio/how-to/create-manage-compute-session) before you execute the prompt flow.

### Set up the Azure Repos repository

To create a forked repo in your Azure DevOps organization, follow the instructions at [Set up the GitHub repo](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#set-up-github-repo). This repo uses two branches, `main` and `development`, for code promotions and pipeline execution.

To create a new local repository, follow the instructions at [Clone the repo](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#cloning-the-repo). This clone helps you create a new feature branch from the development branch and incorporate changes.

## Set up an Azure service principal

An Azure service principal is a security identity that applications, services, and automation tools use to access Azure resources. The application or service authenticates with Azure to access resources on your behalf.

Create a service principal by following the instructions at [Create an Azure service principal](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#create-azure-service-principal). You use this service principal to configure the Azure DevOps Services connection and to allow Azure DevOps Services to authenticate and connect to Azure services. The prompt flow experiment and evaluation jobs both run under the identity of the service principal.

The setup provides the service principal with **Owner** permissions so the CD pipeline can automatically provide the newly provisioned Azure Machine Learning endpoint with access to the Azure Machine Learning workspace for reading connection information. The pipeline also adds the endpoint to the key vault policy associated with the Azure Machine Learning workspace with `get` and `list` secret permissions. You can change the **Owner** permissions to **Contributor** level permissions by changing the pipeline YAML code to remove the step related to permissions.

### Create a new Azure DevOps project

To create a new project in the Azure DevOps UI, follow the instructions at [Create a new Azure DevOps project](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/Azure_devops_how_to_setup.md#create-new-azure-devops-project).

### Set up authentication between Azure DevOps and Azure

This step configures a new Azure DevOps service connection that stores the service principal information. The project pipelines can read the connection information by using the connection name to connect to Azure automatically. To use the service principal you created to set up authentication between Azure DevOps and Azure services, follow the instructions at [Set up authentication with Azure and Azure DevOps](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md#set-up-authentication-with-azure-and-azure-devops).

### Create an Azure DevOps variable group

To create a new variable group and add a variable related to the Azure DevOps service connection, follow the instructions at [Create an Azure DevOps variable group](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/Azure_devops_how_to_setup.md#create-an-azure-devops-variable-group). The service principal name is then available to the pipelines automatically as an environment variable.

### Configure Azure Repos and Azure Pipelines

The example repository uses two branches, `main` and `development`, for code promotions and pipeline execution. To set up your own local and remote repositories to use code from the example repo, follow the instructions at [Configure Azure DevOps local and remote repositories](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/Azure_devops_how_to_setup.md#configure-azure-devops-local-and-remote-repository).

You clone both the `main` and `development` branches from the example repository, and associate the code to refer to the new Azure Repos repository. Both the PR and development pipelines are configured to execute automatically based on PR creation and merge triggers.

The branch policy for the `development` branch is configured to execute the PR pipeline for any PR raised on the development branch from a feature branch. The `dev` pipeline executes when the PR merges to the development branch, and consists of both CI and CD phases.

*Human in the loop* is also implemented within the pipelines. After the CI phase in the `dev` pipeline executes, the CD phase follows after manual approval is provided in the Azure Pipelines build execution UI.

The default time to await approval is 60 minutes, after which the pipeline is rejected and the CD phase doesn't execute. Manually approving the execution executes the CD steps of the pipeline.

The manual approval in the example pipeline is configured to send notifications to `replace@youremail.com`. Replace the placeholder with an appropriate email address.

### Test the pipeline

To test the pipelines, follow the instructions at [Test the pipelines](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/Azure_devops_how_to_setup.md#test-the-pipelines). The complete process involves the following steps:

1. You raise a PR from a feature branch to the development branch.
1. The PR pipeline executes automatically due to the branch policy configuration.
1. The PR is merged to the development branch.
1. The associated `dev` pipeline executes, resulting in full CI and CD execution and provisioning or updating of the Azure Machine Learning endpoints.

The outputs should look similar to the examples at [Example prompt run, evaluation, and deployment scenario](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/Azure_devops_how_to_setup.md#example-prompt-run-evaluation-and-deployment-scenario).

### Use local execution

To use [local execution](https://github.com/microsoft/genaiops-promptflow-template/blob/main/docs/Azure_devops_how_to_setup.md#local-execution) capabilities, follow these steps.

1. Clone the repository as follows:

   ```bash
   git clone https://github.com/microsoft/genaiops-promptflow-template.git
   ```

1. Create an *.env* file at the top folder level. Add lines for each connection, updating the values for the placeholders. The examples in the example repo use the AzureOpenAI connection named `aoai` and API version `2024-02-01`.

   ```bash
   aoai={ "api_key": "<api key>","api_base": "<api base or endpoint>","api_type": "azure","api_version": "2024-02-01"}
   <connection2>={ "api_key": "<api key>","api_base": "<api base or endpoint>","api_type": "<api type>","api_version": "<api_version>"}
   ```
1. Prepare the local conda or virtual environment to install the dependencies.

   ```bash
   python -m pip install promptflow promptflow-tools promptflow-sdk jinja2 promptflow[azure] openai promptflow-sdk[builtins] python-dotenv
   ```

1. Bring or write your flows into the template based on instructions at [How to onboard new flows](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/how_to_onboard_new_flows.md).

1. Write Python scripts in the *local_execution* folder similar to the provided examples.

## Related content

- [GenAIOps with prompt flow template](https://github.com/microsoft/genaiops-promptflow-template)
- [Prompt flow open source repository](https://github.com/microsoft/promptflow)
- [Install and set up Python SDK v2](/python/api/overview/azure/ai-ml-readme)
- [Install and set up Python CLI v2](../how-to-configure-cli.md)

