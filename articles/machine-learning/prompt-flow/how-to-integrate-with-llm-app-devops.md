---
title: Integrate prompt flow with DevOps for LLM-based applications
titleSuffix: Azure Machine Learning
description: Integrate prompt flow with DevOps to enhance your LLM-based application development workflows in Azure Machine Learning.
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar
ms.date: 11/01/2024
ms.custom:
  - ignite-2023
  - build-2024
  - sfi-image-nochange
ms.update-cycle: 365-days
---

# Integrate prompt flow with DevOps for LLM-based applications

Azure Machine Learning prompt flow is a developer-friendly and easy-to-use code-first method to develop and iterate flows for large language model (LLM)-based application development. Prompt flow provides an SDK and CLI, a Visual Studio Code extension, and a flow authoring UI. These tools facilitate local flow development, local flow run and evaluation run triggering, and transitioning flows between local and cloud workspace environments.

You can combine the prompt flow experience and code capabilities with developer operations (DevOps) to enhance your LLM-based application development workflows. This article focuses on integrating prompt flow and DevOps for Azure Machine Learning LLM-based applications.

The following diagram shows the interaction of local and cloud-based prompt flow development with DevOps.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/devops-process.png" alt-text="Diagram showing the following flow: create flow, develop and test flow, versioning in code repo, submit runs to cloud, and debut and iteration." border="false" lightbox = "./media/how-to-integrate-with-llm-app-devops/devops-process.png":::

## Prerequisites

- An Azure Machine Learning workspace. To create one, see [Create resources to get started](../quickstart-create-resources.md).

- A local Python environment with the Azure Machine Learning Python SDK v2 installed, created by following the instructions at [Getting started](https://github.com/Azure/azureml-examples/tree/sdk-preview/sdk#getting-started).

  >[!NOTE]
  >This environment is separate from the environment the compute session uses to run the flow, which you define as part of the flow. For more information, see [Manage prompt flow compute session in Azure Machine Learning studio](how-to-manage-compute-session.md).

- Visual Studio Code with the Python and Prompt flow extensions installed.

  :::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-source-file-raw-file.png" alt-text="Screenshot of the Python and Prompt flow extensions in Visual Studio Code."

## Use a code-first experience in prompt flow

Developing LLM-based applications usually follows a standardized application engineering process that includes source code repositories and continuous integration/continuous deployment (CI/CD) pipelines. This process promotes streamlined development, version control, and collaboration among team members.

Integrating DevOps with the prompt flow code experience offers code developers a more efficient GenAIOps or LLMOps iteration process, with the following key features and benefits:

- **Flow versioning in the code repository**. You can define flow files in YAML format, and they stay aligned with referenced source files in the same folder structure.

- **Flow run integration with CI/CD pipelines**. You can seamlessly integrate prompt flow into your CI/CD pipelines and delivery process by using the prompt flow CLI or SDK to automatically trigger flow runs.

- **Smooth transition between local and cloud**. You can easily export your flow folder to your local or upstream code repository for version control, local development, and sharing. You can also effortlessly import the flow folder back into Azure Machine Learning for further authoring, testing, and deployment using cloud resources.

### Access prompt flow code

Each prompt flow has a flow folder structure containing essential code files that define the flow. The folder structure organizes your flow, facilitating smoother transitions between local and cloud.

Azure Machine Learning provides a shared file system for all workspace users. Upon flow creation, a corresponding flow folder is automatically generated and stored in the *Users/\<username>/promptflow* directory.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-folder-created-in-file-share-storage.png" alt-text="Screenshot of standard flow creation showing a new flow." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-folder-created-in-file-share-storage.png":::

### Work with flow code files

Once you create a flow in Azure Machine Learning studio, you can view, edit, and manage the flow files in the **Files** section of the flow authoring page. Any modifications you make to the files reflect directly in the file share storage.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-file-explorer.png" alt-text="Screenshot of a standard flow authoring page highlighting the Files pane." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-file-explorer.png":::

The flow folder for an LLM-based flow contains the following key files.

- *flow.dag.yaml* is the primary flow definition file in YAML format. This file is integral to authoring and defining the prompt flow. The file includes information about inputs, outputs, nodes, tools, and variants the flow uses.

- User-managed source code files in Python (*.py*) or Jinja 2 (*.jinja2*) format configure the tools and nodes in the flow. The Python tool uses Python files to define custom Python logic. The prompt tool and LLM tool use Jinja 2 files to define prompt context.

- Nonsource files like utility and data files can be included in the flow folder along with the source files.

To view and edit the raw code of the *flow.dag.yaml* and source files in the file editor, turn on **Raw file mode**.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-day-yaml-raw-file.png" alt-text="Screenshot of Raw file mode on a standard flow." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-day-yaml-raw-file.png":::

Alternatively, you can access and edit all your flow folders and files from the Azure Machine Learning studio **Notebooks** page.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/notebook-user-path.png" alt-text="Screenshot of Notebooks in Azure Machine Learning with the prompt flow folder showing the files." lightbox = "./media/how-to-integrate-with-llm-app-devops/notebook-user-path.png":::

### Download and check in prompt flow code

To check your flow into your code repository, export the flow folder from Azure Machine Learning studio to your local machine. Select the download icon in the **Files** section of the flow authoring page to download a ZIP package containing all the flow files. You can then check that file into your code repository or unzip it to work with the files locally.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-export.png" alt-text="Screenshot showing the download icon in the Files explorer.":::

For more information about DevOps integration with Azure Machine Learning, see [Git integration for Azure Machine Learning](../concept-train-model-git-integration.md).

## Develop and test locally

As you refine and fine-tune your flow or prompts during iterative development, you can carry out multiple iterations locally within your code repository. The VS Code community version, VS Code Prompt flow extension, and prompt flow local SDK and CLI facilitate pure local development and testing without Azure binding.

Working locally allows you to make and test changes quickly, without needing to update the main code repository each time. For more details and guidance on using local versions, consult the [Prompt flow GitHub community](https://github.com/microsoft/promptflow).

### Use the VS Code Prompt flow extension

By using the Prompt flow VS Code extension, you can easily author your flow locally in the VS Code editor with a similar UI experience as in the cloud.

To edit files locally in VS Code with the Prompt flow extension:

1. In VS Code with the Prompt flow extension enabled, open a prompt flow folder.
1. Open the *flow.dag.yaml* file and select the **Visual editor** link at the top of the file.

   :::image type="content" source="./media/how-to-integrate-with-llm-app-devops/select-visual-editor.png" alt-text="Screenshot of the Visual editor link at the top of a flow definition file in VS Code." lightbox = "./media/how-to-integrate-with-llm-app-devops/select-visual-editor.png":::

1. Use the prompt flow visual editor to make changes to your flow, such as tuning the prompts in variants or adding more nodes.

   :::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-test-output.png" alt-text="Screenshot of the visual prompt flow editor in VS Code." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-test-output.png":::

1. To test your flow, select the **Run** icon at the top of the visual editor, or to test any node, select the **Run** icon at the top of the node.

   :::image type="content" source="./media/how-to-integrate-with-llm-app-devops/run-flow-visual-editor.png" alt-text="Screenshot of VS Code showing running the flow or a node in the visual editor. " lightbox = "./media/how-to-integrate-with-llm-app-devops/run-flow-visual-editor.png":::

### Use the prompt flow SDK and CLI

If you prefer to work directly in code, or use Jupyter, PyCharm, Visual Studio, or another integrated development environment (IDE), you can directly modify the YAML code in the *flow.dag.yaml* file.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-directory-and-yaml.png" alt-text="Screenshot of a YAML file in VS Code highlighting the default input and flow directory." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-directory-and-yaml.png":::

You can then trigger a single flow run for testing by using the prompt flow CLI or SDK in the terminal as follows.

# [Azure CLI](#tab/cli)

To trigger a run from the working directory, run the following code:

```sh
pf flow test --flow <directory-name>
```

# [Python SDK](#tab/python)

```python
from promptflow import PFClient

pf_client = PFClient()

flow_path = "<directory-name>"

# Test flow
flow_inputs = {"<input-type>": "<input-value>", "<input-type>": "<input-value>"}
flow_result = pf_client.test(flow=flow_path, inputs=inputs)
print(f"Flow outputs: {flow_result}")

# Test node in the flow
node_name = "<node-name>"  # The node name in the flow.
node_inputs = {"<node-input-type>": "<node-input-value>"}
node_result = pf_client.test(flow=flow_path, inputs=node_inputs, node=node_name)
print(f"Node outputs: {node_result}")
```

---

The return values are the test logs and outputs.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-test-output-cli.png" alt-text="Screenshot of the flow test output in PowerShell." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-test-output-cli.png":::

<a name="submitting-runs-to-the-cloud-from-local-repository"></a>
### Submit runs to the cloud from a local repository

Once you're satisfied with the results of your local testing, you can use the prompt flow CLI or SDK to submit runs to the cloud from the local repository. The following procedure and code are based on the [Web Classification demo project](https://github.com/Azure/llmops-gha-demo/tree/main/promptflow/web-classification) in GitHub. You can clone the project repo or download the prompt flow code to your local machine.

#### Install the prompt flow SDK 

Install the Azure prompt flow SDK/CLI by running `pip install promptflow[azure] promptflow-tools`.

If you're using the demo project, get the SDK and other necessary packages by installing [requirements.txt](https://github.com/Azure/llmops-gha-demo/blob/main/promptflow/web-classification/requirements.txt) with<br>`pip install -r <path>/requirements.txt`.

<a name="connect-to-azure-machine-learning-workspace"></a>
#### Connect to your Azure Machine Learning workspace

# [Azure CLI](#tab/cli)

```sh
az login
```

# [Python SDK](#tab/python)

Import required libraries and packages, configure credentials, and get a handle to the workspace.

```python
import json

# Import required libraries
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Import azure promptflow apis
from promptflow.azure import PFClient

# Configure credential
try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential if DefaultAzureCredential doesn't work
    credential = InteractiveBrowserCredential()

# Get a handle to the workspace from the current credential or config.json in the parent directory
pf = PFClient.from_config(
    credential=credential,
)
```

---

#### Upload the flow and create a run

# [Azure CLI](#tab/cli)

Prepare the *run.yml* file to define the configuration for this flow run in the cloud.

```yaml
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Run.schema.json
flow: <path-to-flow>
data: <path-to-flow>/<data-file>.jsonl

column_mapping:
  url: ${data.url}

# Define cloud compute resource

resources:
  instance_type: <compute-type>

# If using compute instance compute type, also specify instance name
#  compute: <compute-instance-name> 

# Specify connections

  <node-name>:
    connection: <connection-name>
    deployment_name: <deployment-name>
```

You can specify the connection and deployment name for each tool in the flow that requires a connection. If you don't specify the connection and deployment name, the tool uses the connection and deployment in the *flow.dag.yaml* file. Use the following code to format connections:

```yaml
...
connections:
  <node-name>:
    connection: <connection-name>
      deployment_name: <deployment-name>
...

```

Create the run.

```sh
pfazure run create --file run.yml
```

# [Python SDK](#tab/python)

Load the flow, define resources and connections, and create the run.

```python
flow = "<path-to-flow>"
data = "<path-to-flow>/<data-file>.jsonl"

# Define compute resource instance type when using serverless compute

# resources = {"instance_type": "serverless"}

# Also specify compute instance name when using a compute instance

# resources={
#     "instance_type": "<compute-instance-type>",
#     "compute": "<compute-instance-name>"
# }

# Specify the connection and deployment name for each tool in the flow that requires a connection

connections = {"<node-name>":
                  {"connection": <connection-name>,
                  "deployment_name": <deployment-name>},
               "<node-name>":
                  {"connection": <connection-name>,
                  "deployment_name": <deployment-name>}
                }

# Create the run

run = Run(
    flow=flow,
    data=data,
    column_mapping={
        "url": "${data.url}"
    }, 

    connections=connections,
    # To customize identity, you can provide it in identity

    # identity={
    #     "type": "managed",
    # }
)

base_run = pf.runs.create_or_update(run=run)
```

---

#### Create an evaluation flow run

# [Azure CLI](#tab/cli)

Prepare the *run_evaluation.yml* file to define the configuration for this evaluation flow run in the cloud.

```yaml
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Run.schema.json
flow: <path-to-flow>
data: <path-to-flow>/<data-file>.jsonl
run: <id-of-base-flow-run>
column_mapping:
  <input-name>: ${data.<column-from-test-dataset>}
  <input-name>: ${run.outputs.<column-from-run-output>}

resources:
  instance_type: <compute-type>
  compute: <compute_instance_name> 

connections:
  <node-name>:
    connection: <connection-name>
    deployment_name: <deployment-name>
  <node-name>:
    connection: <connection-name>
    deployment_name: <deployment-name>

```

Create the evaluation run.

```sh
pfazure run create --file run_evaluation.yml
```

# [Python SDK](#tab/python)

Load the evaluation flow and create the run.

```python
flow = "<path-to-flow>"
data = "<path-to-flow>/<data-file>.jsonl"

resources={
    "instance_type": "<compute-instance-type>",
    "compute": "<compute-instance-name>"
    }

connections = {"<node-name>":
                  {"connection": <connection-name>,
                  "deployment_name": <deployment-name>},
               "<node-name>":
                  {"connection": <connection-name>,
                  "deployment_name": <deployment-name>}
                }
eval_run = Run(
    flow=flow,
    data=data,
    run=<base-run-id>,
    column_mapping={
        "<input-name>": "${data.<column-from-test-dataset>}",
        "<input-name>": "${run.outputs.<column-from-run-output>}",
    },
    connections=connections,
    identity={
        "type": "managed",
    }
)

eval_run = pf.runs.create_or_update(run=eval_run)
```

---

### View run results 

Submitting the flow run to the cloud returns the cloud URL of the run. You can open the URL to view the run results in Azure Machine Learning studio. You can also run the following CLI or SDK commands to view run results.

#### Stream the logs

# [Azure CLI](#tab/cli)

```sh
pfazure run stream --name <run-name>
```

# [Python SDK](#tab/python)

```python
pf.stream("<run-name>")
```

---

#### View run outputs

# [Azure CLI](#tab/cli)

```sh
pfazure run show-details --name <run-name>
```

# [Python SDK](#tab/python)

```python
details = pf.get_details("<run-name>")
details.head(10)
```

---

#### View evaluation run metrics

# [Azure CLI](#tab/cli)

```sh
pfazure run show-metrics --name <evaluation-run-name>
```

# [Python SDK](#tab/python)

```python
pf.get_metrics("<evaluation-run-name>")
```
---

## Integrate with DevOps

A combination of a local development environment and a version control system such as Git is typically most effective for iterative development. You can make modifications and test your code locally, then commit the changes to Git. This process creates an ongoing record of your changes and offers the ability to revert to earlier versions if necessary.

When you need to share flows across different environments, you can push them to a cloud-based code repository like GitHub or Azure Repos. This strategy lets you access the most recent code version from any location and provides tools for collaboration and code management.

By following these practices, teams can create a seamless, efficient, and productive collaborative environment for prompt flow development.

For example end-to-end LLMOps pipelines that execute web classification flows, see [Set up end to end GenAIOps with prompt Flow and GitHub](how-to-end-to-end-llmops-with-prompt-flow.md) and the GitHub [Web Classification demo project](https://github.com/Azure/llmops-gha-demo/tree/main/promptflow/web-classification).

### Trigger flow runs in CI pipelines

Once you successfully develop and test your flow and check it in as the initial version, you're ready for tuning and testing iterations. At this stage, you can trigger flow runs, including batch testing and evaluation runs, by using the prompt flow CLI to automate steps in your CI pipeline.

Throughout the lifecycle of your flow iterations, you can use the CLI to automate the following operations:

- Running the prompt flow after a pull request
- Running prompt flow evaluation to ensure results are high quality
- Registering prompt flow models
- Deploying prompt flow models

<a name="go-back-to-studio-ui-for-continuous-development"></a>
### Use the studio UI for continuous development

At any point in flow development, you can go back to the Azure Machine Learning studio UI and use cloud resources and experiences to make changes to your flow.

To continue developing and working with the most up-to-date versions of the flow files, you can access a terminal on the **Notebook** page and pull the latest flow files from your repository. Or, you can directly import a local flow folder as a new draft flow to seamlessly transition between local and cloud development.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-import-local-upload.png" alt-text="Screenshot of the Create a new flow screen with Upload to local highlighted." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-import-local-upload.png":::

### Deploy the flow as an online endpoint

The last step in going to production is to deploy your flow as an online endpoint in Azure Machine Learning. This process allows you to integrate your flow into your application and makes it available to use. For more information on how to deploy your flow, see [Deploy flows to Azure Machine Learning managed online endpoint for real-time inference](how-to-deploy-to-code.md).

## Collaborate on flow development

Collaboration among team members can be essential when developing a LLM-based application with prompt flow. Team members might be authoring and testing the same flow, working on different facets of the flow, or making iterative changes and enhancements concurrently. This collaboration requires an efficient and streamlined approach to sharing code, tracking modifications, managing versions, and integrating changes into the final project.

The prompt flow SDK/CLI and the VS Code Prompt flow extension facilitate easy collaboration on code-based flow development within a source code repository. You can use a cloud-based source control system like GitHub or Azure Repos for tracking changes, managing versions, and integrating these modifications into the final project.

### Follow collaborative development best practices

1. Set up a centralized code repository.

   The first step of the collaborative process involves setting up a code repository as the base for project code, including prompt flow code. This centralized repository enables efficient organization, change tracking, and collaboration among team members.

1. Author and single test your flow locally in VS Code with the Prompt flow extension.

   Once the repository is set up, team members can use VS Code with the Prompt flow extension for local authoring and single input testing of the flow. The standardized integrated development environment promotes collaboration among multiple members working on different aspects of the flow.

   :::image type="content" source="media/how-to-integrate-with-llm-app-devops/prompt-flow-local-develop.png" alt-text="Screenshot of local development." lightbox = "media/how-to-integrate-with-llm-app-devops/prompt-flow-local-develop.png":::

1. Use the `pfazure` CLI or SDK to submit batch runs and evaluation runs from local flows to the cloud.

   After local development and testing, team members can use the prompt flow CLI/SDK to submit and evaluate batch and evaluation runs to the cloud. This process enables cloud compute usage, persistent results storage, endpoint creation for deployments, and efficient management in the studio UI.

   :::image type="content" source="media/how-to-integrate-with-llm-app-devops/pfazure-run.png" alt-text="Screenshot of pfazure command to submit run to cloud." lightbox = "media/how-to-integrate-with-llm-app-devops/pfazure-run.png":::

1. View and manage run results in the Azure Machine Learning studio workspace UI.

   After they submit runs to the cloud, team members can access the studio UI to view the results and manage experiments efficiently. The cloud workspace provides a centralized location for gathering and managing run history, logs, snapshots, comprehensive results, and instance level inputs and outputs.
   
   :::image type="content" source="media/how-to-integrate-with-llm-app-devops/pfazure-run-snapshot.png" alt-text="Screenshot of cloud run snapshot." lightbox = "media/how-to-integrate-with-llm-app-devops/pfazure-run-snapshot.png":::

1. Use the **Runs** list that records all run history to easily compare the results of different runs, aiding in quality analysis and necessary adjustments.

   :::image type="content" source="media/how-to-integrate-with-llm-app-devops/cloud-run-list.png" alt-text="Screenshot of run list in workspace." lightbox = "media/how-to-integrate-with-llm-app-devops/cloud-run-list.png":::

1. Continue to use local iterative development.

   After analyzing the results of experiments, team members can return to the local environment and code repository for more development and fine-tuning, and iteratively submit subsequent runs to the cloud. This iterative approach ensures consistent enhancement until the team is satisfied with the quality for production.

1. Use one-step deployment to production in the studio.

   Once the team is fully confident in the quality of the flow, they can seamlessly deploy it as an online endpoint in a robust cloud environment. Deployment as an online endpoint can be based on a run snapshot, allowing stable and secure serving, further resource allocation and usage tracking, and log monitoring in the cloud.

   :::image type="content" source="media/how-to-integrate-with-llm-app-devops/deploy-from-snapshot.png" alt-text="Screenshot of deploying flow from a run snapshot." lightbox = "media/how-to-integrate-with-llm-app-devops/deploy-from-snapshot.png":::

   The Azure Machine Learning studio **Deploy** wizard helps you easily configure your deployment.

   :::image type="content" source="media/how-to-integrate-with-llm-app-devops/deploy-wizard.png" alt-text="Screenshot of deploy wizard." lightbox = "media/how-to-integrate-with-llm-app-devops/deploy-wizard.png":::

## Related content

- [Set up end-to-end GenAIOps with prompt flow and GitHub](how-to-end-to-end-llmops-with-prompt-flow.md)
- [Prompt flow CLI documentation for Azure](https://microsoft.github.io/promptflow/reference/pfazure-command-reference.html)
