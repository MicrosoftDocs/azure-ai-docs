---
title: What are deployment templates?
titleSuffix: Azure Machine Learning
description: Learn how deployment templates package the infrastructure settings that your registered models need so that consumers can deploy them consistently to managed online endpoints.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: concept-article
ms.custom: build-2026
author: s-polly
ms.author: scottpolly
ms.date: 05/12/2026
ms.reviewer: sehan
ai-usage: ai-assisted
---

# What are deployment templates?

A *deployment template* is a reusable, registry-scoped artifact that packages the infrastructure and runtime settings that a model needs to serve traffic on a managed online endpoint. As a model author, you publish a deployment template alongside your model so that consumers can deploy the model consistently without learning every infrastructure detail. As a consumer, you deploy the model with a short YAML or REST payload because the deployment template already specifies the environment, environment variables, probes, and other settings.

[!INCLUDE [machine-learning-preview-old-json-schema-note](includes/machine-learning-preview-old-json-schema-note.md)]

## Why use deployment templates?

Deployment templates help you separate the concerns of model authoring from model consumption:

- **Reusability.** Author a deployment template once and reuse it across many models in the registry, or across many versions of the same model.
- **Guardrails.** Restrict the instance types that consumers can use by setting `allowed_instance_types` on the template, and restrict which deployment templates a consumer can apply by setting `allowed_deployment_templates` on the model.
- **Consistency.** Every consumer who deploys the model gets the same environment image, scoring port, probes, and request settings, which reduces drift across deployments.
- **Decoupled lifecycle.** Update a deployment template version without changing the model artifact, then point the model's `default_deployment_template` to the new version when you want consumers to pick it up.

## Key concepts

A deployment template has the following characteristics:

- **Registry-scoped.** Deployment templates live in an Azure Machine Learning registry, not in a workspace. You reference them by their registry asset URI: `azureml://registries/<registry-name>/deploymenttemplates/<template-name>/versions/<version>`.
- **Versioned.** Each deployment template has a name and a version. Consumers reference a specific version, so updates to the template don't change running deployments until consumers redeploy.
- **Type `Managed`.** Deployment templates currently support the `Managed` type, which targets [managed online endpoints](concept-endpoints-online.md).
- **Bound to a registry environment.** The `environment` field on a deployment template must reference a registry-scoped environment. Workspace-scoped environments and inline environment definitions aren't supported.

A model that uses deployment templates has two related fields:

- `default_deployment_template` — the deployment template that's applied when a consumer deploys the model without specifying an override.
- `allowed_deployment_templates` — an optional list of deployment templates that consumers can choose from as overrides. When set, an override at deployment time must reference one that matches the patterns of these templates.

A deployment that references a model with a `default_deployment_template` can override it by setting `properties."azureml.deploymentTemplateOverride"` to the registry asset URI of the override template.

## Workflow at a glance

The end-to-end flow has three roles: the environment owner, the model author, and the model consumer. The same person can play all three roles.

1. **Create an environment.** The environment owner creates an environment in a workspace and shares it to a registry.
1. **Create a deployment template.** The model author creates a deployment template in the registry that references the registry-scoped environment, and sets infrastructure properties such as `default_instance_type`, `allowed_instance_types`, scoring path and port, environment variables, and probes.
1. **Register the model.** The model author registers the model in the registry while uploading model weights and setting `default_deployment_template` (and optionally `allowed_deployment_templates`) on the model.
1. **Deploy the model.** The consumer creates a managed online endpoint in a workspace and creates a deployment that references the registry model. The deployment uses the model's default deployment template, or specifies an override that's in the model's allowed list.

For step-by-step instructions, see:

- [Manage models with deployment templates](how-to-manage-models-deployment-templates.md) (model author)
- [Deploy models that use deployment templates](how-to-deploy-models-deployment-template.md) (model consumer)

## Relationship with environments and models

Deployment templates sit between environments and models in the registry:

- An **environment** describes the container image and Python dependencies that run your scoring code. A registry-scoped environment can be referenced by many deployment templates.
- A **deployment template** describes how to run a model on a managed online endpoint, by referencing one registry-scoped environment plus infrastructure settings.
- A **model** in the registry can pin one default deployment template and optionally restrict the set of allowed deployment template overrides. Different models can reuse the same deployment template, or pin different deployment templates.

## Mutability

Deployment templates and models follow different mutability rules so that a deployment template version stays a stable, reproducible target while a model version can pick up updated infrastructure pairings.

- **Deployment template version is immutable.** After you create a version of a deployment template, only the `tags` and `description` fields on that version can be updated in place. Fields that affect runtime behavior — such as `environment`, `environment_variables`, `default_instance_type`, `allowed_instance_types`, `request_settings`, `liveness_probe`, and `readiness_probe` — are immutable. To change any of these, create a new version of the deployment template. This guarantees that a consumer who pins to a specific deployment template version always gets the same infrastructure configuration.
- **Model version is mutable for deployment template references.** On an existing model version, you can update `default_deployment_template` and `allowed_deployment_templates` to point to new deployment templates or to new versions of an existing deployment template. You don't need to create a new model version to roll out a new infrastructure configuration; bump the deployment template version instead and update the model's pointers, unless you opt to create a new model version.

## Limitations and considerations

- Deployment templates are in preview. Schema and behavior can change.
- Deployment templates support the `Managed` type only. Use them with [managed online endpoints](concept-endpoints-online.md), not with Kubernetes online endpoints or batch endpoints.
- The `environment` field must reference a registry-scoped environment. Share workspace environments to a registry before you reference them.
- The model's `allowed_deployment_templates` list is author guidance, not an enforced restriction. A model author uses it to publish a curated set of validated override templates, but the platform doesn't block a deployment that overrides with a template outside the list.
- An `instance_type` specified on a deployment must be in the deployment template's `allowed_instance_types` list, when that list is set on the template.

## Related content

- [Manage models with deployment templates](how-to-manage-models-deployment-templates.md)
- [Deploy models that use deployment templates](how-to-deploy-models-deployment-template.md)
- [CLI (v2) deployment template YAML schema](reference-yaml-deployment-template.md)
- [CLI (v2) model YAML schema](reference-yaml-model.md)
- [CLI (v2) managed online deployment YAML schema](reference-yaml-deployment-managed-online.md)
- [Online endpoints](concept-endpoints-online.md)
