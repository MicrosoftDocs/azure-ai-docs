---
title: Microsoft Foundry REST Reference
description: Learn how to use the Microsoft Foundry REST Reference
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: reference
ms.date: 02/19/2026
author: mrbullwinkle    
ms.author: mbullwin
---

# Microsoft Foundry

**API Version:** v1

## Authentication

**Flow:** implicit

**Authorization URL:** `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`

**Scopes:**

- `https://ai.azure.com/.default`

## Agents

### Agents - create agent

```HTTP
POST {endpoint}/agents?api-version=v1
```


Creates the agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview`, `HostedAgents=V1Preview`, `WorkflowAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | [AgentDefinition](#agentdefinition) |  | Yes |  |
| └─ kind | [AgentKind](#agentkind) |  | Yes |  |
| └─ rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The unique name that identifies the agent. Name can be used to retrieve/update/delete the agent.<br>- Must start and end with alphanumeric characters,<br>- Can contain hyphens in the middle<br>- Must not exceed 63 characters.<br>**Constraints:** maxLength: 63 | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentObject](#agentobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - list agents

```HTTP
GET {endpoint}/agents?api-version=v1
```


Returns the list of all agents.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| kind | query | No | string<br>Possible values: `prompt`, `hosted`, `container_app`, `workflow` | Filter agents by kind. If not provided, all agents are returned. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - get agent

```HTTP
GET {endpoint}/agents/{agent_name}?api-version=v1
```


Retrieves the agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent to retrieve. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentObject](#agentobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - update agent

```HTTP
POST {endpoint}/agents/{agent_name}?api-version=v1
```


Updates the agent by adding a new version if there are any changes to the agent definition.
If no changes, returns the existing agent version.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent to retrieve. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview`, `HostedAgents=V1Preview`, `WorkflowAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | [AgentDefinition](#agentdefinition) |  | Yes |  |
| └─ kind | [AgentKind](#agentkind) |  | Yes |  |
| └─ rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentObject](#agentobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - delete agent

```HTTP
DELETE {endpoint}/agents/{agent_name}?api-version=v1
```


Deletes an agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent to delete. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DeleteAgentResponse](#deleteagentresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - update agent from manifest

```HTTP
POST {endpoint}/agents/{agent_name}/import?api-version=v1
```


Updates the agent from a manifest by adding a new version if there are any changes to the agent definition.
If no changes, returns the existing agent version.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent to update. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| manifest_id | string | The manifest ID to import the agent version from. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| parameter_values | object | The inputs to the manifest that will result in a fully materialized Agent. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentObject](#agentobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - create agent version

```HTTP
POST {endpoint}/agents/{agent_name}/versions?api-version=v1
```


Create a new agent version.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The unique name that identifies the agent. Name can be used to retrieve/update/delete the agent.<br>- Must start and end with alphanumeric characters,<br>- Can contain hyphens in the middle<br>- Must not exceed 63 characters. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview`, `HostedAgents=V1Preview`, `WorkflowAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | [AgentDefinition](#agentdefinition) |  | Yes |  |
| └─ kind | [AgentKind](#agentkind) |  | Yes |  |
| └─ rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentVersionObject](#agentversionobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - list agent versions

```HTTP
GET {endpoint}/agents/{agent_name}/versions?api-version=v1
```


Returns the list of versions of an agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent to retrieve versions for. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - get agent version

```HTTP
GET {endpoint}/agents/{agent_name}/versions/{agent_version}?api-version=v1
```


Retrieves a specific version of an agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent to retrieve. |
| agent_version | path | Yes | string | The version of the agent to retrieve. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentVersionObject](#agentversionobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - delete agent version

```HTTP
DELETE {endpoint}/agents/{agent_name}/versions/{agent_version}?api-version=v1
```


Deletes a specific version of an agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent to delete. |
| agent_version | path | Yes | string | The version of the agent to delete |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DeleteAgentVersionResponse](#deleteagentversionresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - create agent version from manifest

```HTTP
POST {endpoint}/agents/{agent_name}/versions:import?api-version=v1
```


Create a new agent version from a manifest.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The unique name that identifies the agent. Name can be used to retrieve/update/delete the agent.<br>- Must start and end with alphanumeric characters,<br>- Can contain hyphens in the middle<br>- Must not exceed 63 characters. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| manifest_id | string | The manifest ID to import the agent version from. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| parameter_values | object | The inputs to the manifest that will result in a fully materialized Agent. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentVersionObject](#agentversionobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agents - create agent from manifest

```HTTP
POST {endpoint}/agents:import?api-version=v1
```


Creates an agent from a manifest.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| manifest_id | string | The manifest ID to import the agent version from. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The unique name that identifies the agent. Name can be used to retrieve/update/delete the agent.<br>- Must start and end with alphanumeric characters,<br>- Can contain hyphens in the middle<br>- Must not exceed 63 characters.<br>**Constraints:** maxLength: 63 | Yes |  |
| parameter_values | object | The inputs to the manifest that will result in a fully materialized Agent. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentObject](#agentobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Agent Containers

### Agent containers - list agent container operations

```HTTP
GET {endpoint}/agents/{agent_name}/operations?api-version=v1
```


List container operations for an agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agent containers - get agent container operation

```HTTP
GET {endpoint}/agents/{agent_name}/operations/{operation_id}?api-version=v1
```


Get the status of a container operation for an agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| operation_id | path | Yes | string | The operation ID. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentContainerOperationObject](#agentcontaineroperationobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agent containers - get agent container

```HTTP
GET {endpoint}/agents/{agent_name}/versions/{agent_version}/containers/default?api-version=v1
```


Get a container for a specific version of an agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| agent_version | path | Yes | string | The version of the agent. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentContainerObject](#agentcontainerobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agent containers - list agent version container operations

```HTTP
GET {endpoint}/agents/{agent_name}/versions/{agent_version}/containers/default/operations?api-version=v1
```


List container operations for a specific version of an agent.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| agent_version | path | Yes | string | The version of the agent. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agent containers - delete agent container

```HTTP
POST {endpoint}/agents/{agent_name}/versions/{agent_version}/containers/default:delete?api-version=v1
```


Delete a container for a specific version of an agent. If the container doesn't exist, the operation will be no-op.
The operation is a long-running operation. Following the design guidelines for long-running operations in Azure REST APIs.
https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md#action-operations

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| agent_version | path | Yes | string | The version of the agent. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 202

**Description**: The request has been accepted for processing, but processing has not yet completed. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentContainerOperationObject](#agentcontaineroperationobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| Operation-Location | string |  |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agent containers - stream agent container logs

```HTTP
POST {endpoint}/agents/{agent_name}/versions/{agent_version}/containers/default:logstream?api-version=v1
```


Container log entry streamed from the container as text chunks.
Each chunk is a UTF-8 string that may be either a plain text log line
or a JSON-formatted log entry, depending on the type of container log being streamed.
Clients should treat each chunk as opaque text and, if needed, attempt
to parse it as JSON based on their logging requirements.

For system logs, the format is JSON with the following structure:
{"TimeStamp":"2025-12-15T16:51:33Z","Type":"Normal","ContainerAppName":null,"RevisionName":null,"ReplicaName":null,"Msg":"Connecting to the events collector...","Reason":"StartingGettingEvents","EventSource":"ContainerAppController","Count":1}
{"TimeStamp":"2025-12-15T16:51:34Z","Type":"Normal","ContainerAppName":null,"RevisionName":null,"ReplicaName":null,"Msg":"Successfully connected to events server","Reason":"ConnectedToEventsServer","EventSource":"ContainerAppController","Count":1}

For console logs, the format is plain text as emitted by the container's stdout/stderr.
2025-12-15T08:43:48.72656  Connecting to the container 'agent-container'...
2025-12-15T08:43:48.75451  Successfully Connected to container: 'agent-container' [Revision: 'je90fe655aa742ef9a188b9fd14d6764--7tca06b', Replica: 'je90fe655aa742ef9a188b9fd14d6764--7tca06b-6898b9c89f-mpkjc']
2025-12-15T08:33:59.0671054Z stdout F INFO:     127.0.0.1:42588 - "GET /readiness HTTP/1.1" 200 OK
2025-12-15T08:34:29.0649033Z stdout F INFO:     127.0.0.1:60246 - "GET /readiness HTTP/1.1" 200 OK
2025-12-15T08:34:59.0644467Z stdout F INFO:     127.0.0.1:43994 - "GET /readiness HTTP/1.1" 200 OK

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| agent_version | path | Yes | string | The version of the agent. |
| kind | query | No | string<br>Possible values: `console`, `system` | console returns container stdout/stderr, system returns container app event stream. defaults to console |
| replica_name | query | No | string | When omitted, the server chooses the first replica for console logs. Required to target a specific replica. |
| tail | query | No | integer | Number of trailing lines returned. Enforced to 1-300. Defaults to 20 |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agent containers - start agent container

```HTTP
POST {endpoint}/agents/{agent_name}/versions/{agent_version}/containers/default:start?api-version=v1
```


Start a container for a specific version of an agent. If the container is already running, the operation will be no-op.
The operation is a long-running operation. Following the design guidelines for long-running operations in Azure REST APIs.
https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md#action-operations

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| agent_version | path | Yes | string | The version of the agent. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_replicas | integer | The maximum number of replicas. Defaults to 1. | No | 1 |
| min_replicas | integer | The minimum number of replicas. Defaults to 1. | No | 1 |

#### Responses

**Status Code:** 202

**Description**: The request has been accepted for processing, but processing has not yet completed. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentContainerOperationObject](#agentcontaineroperationobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| Operation-Location | string |  |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agent containers - stop agent container

```HTTP
POST {endpoint}/agents/{agent_name}/versions/{agent_version}/containers/default:stop?api-version=v1
```


Stop a container for a specific version of an agent. If the container is not running, or already stopped, the operation will be no-op.
The operation is a long-running operation. Following the design guidelines for long-running operations in Azure REST APIs.
https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md#action-operations

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| agent_version | path | Yes | string | The version of the agent. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 202

**Description**: The request has been accepted for processing, but processing has not yet completed. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentContainerOperationObject](#agentcontaineroperationobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| Operation-Location | string |  |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Agent containers - update agent container

```HTTP
POST {endpoint}/agents/{agent_name}/versions/{agent_version}/containers/default:update?api-version=v1
```


Update a container for a specific version of an agent. If the container is not running, the operation will be no-op.
The operation is a long-running operation. Following the design guidelines for long-running operations in Azure REST APIs.
https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md#action-operations

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| agent_name | path | Yes | string | The name of the agent. |
| agent_version | path | Yes | string | The version of the agent. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `ContainerAgents=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_replicas | integer | The maximum number of replicas. | No |  |
| min_replicas | integer | The minimum number of replicas. | No |  |

#### Responses

**Status Code:** 202

**Description**: The request has been accepted for processing, but processing has not yet completed. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AgentContainerOperationObject](#agentcontaineroperationobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| Operation-Location | string |  |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Connections

### Connections - list

```HTTP
GET {endpoint}/connections?api-version=v1
```


List all connections in the project, without populating connection credentials

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| connectionType | query | No | string<br>Possible values: `AzureOpenAI`, `AzureBlob`, `AzureStorageAccount`, `CognitiveSearch`, `CosmosDB`, `ApiKey`, `AppConfig`, `AppInsights`, `CustomKeys`, `RemoteTool_Preview` | List connections of this specific type |
| defaultConnection | query | No | boolean | List connections that are default connections |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| x-ms-client-request-id | False | string | An opaque, globally-unique, client-generated string identifier for the request. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedConnection](#pagedconnection) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-client-request-id |  | An opaque, globally-unique, client-generated string identifier for the request. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Connections - get

```HTTP
GET {endpoint}/connections/{name}?api-version=v1
```


Get a connection by name, without populating connection credentials

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The friendly name of the connection, provided by the user. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| x-ms-client-request-id | False | string | An opaque, globally-unique, client-generated string identifier for the request. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Connection](#connection) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-client-request-id |  | An opaque, globally-unique, client-generated string identifier for the request. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Connections - get with credentials

```HTTP
POST {endpoint}/connections/{name}/getConnectionWithCredentials?api-version=v1
```


Get a connection by name, with its connection credentials

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The friendly name of the connection, provided by the user. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| x-ms-client-request-id | False | string | An opaque, globally-unique, client-generated string identifier for the request. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Connection](#connection) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-client-request-id |  | An opaque, globally-unique, client-generated string identifier for the request. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

## Datasets

### Datasets - list latest

```HTTP
GET {endpoint}/datasets?api-version=v1
```


List the latest version of each DatasetVersion

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedDatasetVersion](#pageddatasetversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Datasets - list versions

```HTTP
GET {endpoint}/datasets/{name}/versions?api-version=v1
```


List all versions of the given DatasetVersion

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedDatasetVersion](#pageddatasetversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Datasets - get version

```HTTP
GET {endpoint}/datasets/{name}/versions/{version}?api-version=v1
```


Get the specific version of the DatasetVersion. The service returns 404 Not Found error if the DatasetVersion does not exist.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The specific version id of the DatasetVersion to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DatasetVersion](#datasetversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Datasets - delete version

```HTTP
DELETE {endpoint}/datasets/{name}/versions/{version}?api-version=v1
```


Delete the specific version of the DatasetVersion. The service returns 204 No Content if the DatasetVersion was deleted successfully or if the DatasetVersion does not exist.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The version of the DatasetVersion to delete. |


#### Responses

**Status Code:** 204

**Description**: There is no content to send for this request, but the headers may be useful. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Datasets - create or update version

```HTTP
PATCH {endpoint}/datasets/{name}/versions/{version}?api-version=v1
```


Create a new or update an existing DatasetVersion with the given version id

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The specific version id of the DatasetVersion to create or update. |

#### Request Body

**Content-Type**: application/merge-patch+json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | [DatasetType](#datasettype) | Enum to determine the type of data. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DatasetVersion](#datasetversion) | |

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DatasetVersion](#datasetversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Datasets - get credentials

```HTTP
POST {endpoint}/datasets/{name}/versions/{version}/credentials?api-version=v1
```


Get the SAS credential to access the storage account associated with a Dataset version.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The specific version id of the DatasetVersion to operate on. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AssetCredentialResponse](#assetcredentialresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Datasets - start pending upload version

```HTTP
POST {endpoint}/datasets/{name}/versions/{version}/startPendingUpload?api-version=v1
```


Start a new or get an existing pending upload of a dataset for a specific version.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The specific version id of the DatasetVersion to operate on. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionName | string | Azure Storage Account connection name to use for generating temporary SAS token | No |  |
| pendingUploadId | string | If PendingUploadId is not provided, a random GUID will be used. | No |  |
| pendingUploadType | enum | BlobReference is the only supported type.<br>Possible values: `BlobReference` | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PendingUploadResponse](#pendinguploadresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

## Deployments

### Deployments - list

```HTTP
GET {endpoint}/deployments?api-version=v1
```


List all deployed models in the project

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| modelPublisher | query | No | string | Model publisher to filter models by |
| modelName | query | No | string | Model name (the publisher specific name) to filter models by |
| deploymentType | query | No | string<br>Possible values: `ModelDeployment` | Type of deployment to filter list by |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| x-ms-client-request-id | False | string | An opaque, globally-unique, client-generated string identifier for the request. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedDeployment](#pageddeployment) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-client-request-id |  | An opaque, globally-unique, client-generated string identifier for the request. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Deployments - get

```HTTP
GET {endpoint}/deployments/{name}?api-version=v1
```


Get a deployed model.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | Name of the deployment |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| x-ms-client-request-id | False | string | An opaque, globally-unique, client-generated string identifier for the request. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Deployment](#deployment) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-client-request-id |  | An opaque, globally-unique, client-generated string identifier for the request. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

## Evaluation Taxonomies

### Evaluation taxonomies - list

```HTTP
GET {endpoint}/evaluationtaxonomies?api-version=v1
```


List evaluation taxonomies

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| inputName | query | No | string | Filter by the evaluation input name. |
| inputType | query | No | string | Filter by taxonomy input type. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedEvaluationTaxonomy](#pagedevaluationtaxonomy) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluation taxonomies - get

```HTTP
GET {endpoint}/evaluationtaxonomies/{name}?api-version=v1
```


Get an evaluation run by name.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluationTaxonomy](#evaluationtaxonomy) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluation taxonomies - delete

```HTTP
DELETE {endpoint}/evaluationtaxonomies/{name}?api-version=v1
```


Delete an evaluation taxonomy by name.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 204

**Description**: There is no content to send for this request, but the headers may be useful. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluation taxonomies - create

```HTTP
PUT {endpoint}/evaluationtaxonomies/{name}?api-version=v1
```


Create an evaluation taxonomy.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the evaluation taxonomy. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| properties | object | Additional properties for the evaluation taxonomy. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| taxonomyCategories | array of [TaxonomyCategory](#taxonomycategory) | List of taxonomy categories. | No |  |
| taxonomyInput | [EvaluationTaxonomyInput](#evaluationtaxonomyinput) | Input configuration for the evaluation taxonomy. | Yes |  |
| └─ type | [EvaluationTaxonomyInputType](#evaluationtaxonomyinputtype) | Input type of the evaluation taxonomy. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluationTaxonomy](#evaluationtaxonomy) | |

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluationTaxonomy](#evaluationtaxonomy) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluation taxonomies - update

```HTTP
PATCH {endpoint}/evaluationtaxonomies/{name}?api-version=v1
```


Update an evaluation taxonomy.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the evaluation taxonomy. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| properties | object | Additional properties for the evaluation taxonomy. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| taxonomyCategories | array of [TaxonomyCategory](#taxonomycategory) | List of taxonomy categories. | No |  |
| taxonomyInput | [EvaluationTaxonomyInputUpdate](#evaluationtaxonomyinputupdate) | Input configuration for the evaluation taxonomy. | No |  |
| └─ type | [EvaluationTaxonomyInputType](#evaluationtaxonomyinputtype) | Input type of the evaluation taxonomy. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluationTaxonomy](#evaluationtaxonomy) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

## Evaluation Rules

### Evaluation rules - list

```HTTP
GET {endpoint}/evaluationrules?api-version=v1
```


List all evaluation rules.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| actionType | query | No | string<br>Possible values: `continuousEvaluation`, `humanEvaluationPreview` | Filter by the type of evaluation rule. |
| agentName | query | No | string | Filter by the agent name. |
| enabled | query | No | boolean | Filter by the enabled status. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedEvaluationRule](#pagedevaluationrule) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluation rules - get

```HTTP
GET {endpoint}/evaluationrules/{id}?api-version=v1
```


Get an evaluation rule.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| id | path | Yes | string | Unique identifier for the evaluation rule. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluationRule](#evaluationrule) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluation rules - delete

```HTTP
DELETE {endpoint}/evaluationrules/{id}?api-version=v1
```


Delete an evaluation rule.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| id | path | Yes | string | Unique identifier for the evaluation rule. |


#### Responses

**Status Code:** 204

**Description**: There is no content to send for this request, but the headers may be useful. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluation rules - create or update

```HTTP
PUT {endpoint}/evaluationrules/{id}?api-version=v1
```


Create or update an evaluation rule.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| id | path | Yes | string | Unique identifier for the evaluation rule. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | False | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [EvaluationRuleAction](#evaluationruleaction) | Evaluation action model. | Yes |  |
| └─ type | [EvaluationRuleActionType](#evaluationruleactiontype) | Type of the evaluation action. | Yes |  |
| description | string | Description for the evaluation rule. | No |  |
| displayName | string | Display Name for the evaluation rule. | No |  |
| enabled | boolean | Indicates whether the evaluation rule is enabled. Default is true. | Yes |  |
| eventType | [EvaluationRuleEventType](#evaluationruleeventtype) | Type of the evaluation rule event. | Yes |  |
| filter | [EvaluationRuleFilter](#evaluationrulefilter) | Evaluation filter model. | No |  |
| └─ agentName | string | Filter by agent name. | Yes |  |
| id | string (read-only) | Unique identifier for the evaluation rule. | Yes |  |
| systemData | object (read-only) | System metadata for the evaluation rule. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluationRule](#evaluationrule) | |

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluationRule](#evaluationrule) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

## Evaluators

### Evaluators - list latest versions

```HTTP
GET {endpoint}/evaluators?api-version=v1
```


List the latest version of each evaluator

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| type | query | No | string<br>Possible values: `builtin`, `custom`, `all` | Filter evaluators by type. Possible values: 'all', 'custom', 'builtin'. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedEvaluatorVersion](#pagedevaluatorversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluators - list versions

```HTTP
GET {endpoint}/evaluators/{name}/versions?api-version=v1
```


List all versions of the given evaluator

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| type | query | No | string<br>Possible values: `builtin`, `custom`, `all` | Filter evaluators by type. Possible values: 'all', 'custom', 'builtin'. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedEvaluatorVersion](#pagedevaluatorversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluators - create version

```HTTP
POST {endpoint}/evaluators/{name}/versions?api-version=v1
```


Create a new EvaluatorVersion with auto incremented version id

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| categories | array of [EvaluatorCategory](#evaluatorcategory) | The categories of the evaluator | Yes |  |
| definition | [EvaluatorDefinition](#evaluatordefinition) | Base evaluator configuration with discriminator | Yes |  |
| └─ data_schema | object | The JSON schema (Draft 2020-12) for the evaluator's input data. This includes parameters like type, properties, required. | No |  |
| └─ init_parameters | object | The JSON schema (Draft 2020-12) for the evaluator's input parameters. This includes parameters like type, properties, required. | No |  |
| └─ metrics | object | List of output metrics produced by this evaluator | No |  |
| └─ type | [EvaluatorDefinitionType](#evaluatordefinitiontype) | The type of evaluator definition | Yes |  |
| description | string | The asset description text. | No |  |
| display_name | string | Display Name for evaluator. It helps to find the evaluator easily in AI Foundry. It does not need to be unique. | No |  |
| evaluator_type | [EvaluatorType](#evaluatortype) | The type of the evaluator | Yes |  |
| metadata | object | Metadata about the evaluator | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |

#### Responses

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluatorVersion](#evaluatorversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluators - get version

```HTTP
GET {endpoint}/evaluators/{name}/versions/{version}?api-version=v1
```


Get the specific version of the EvaluatorVersion. The service returns 404 Not Found error if the EvaluatorVersion does not exist.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The specific version id of the EvaluatorVersion to retrieve. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluatorVersion](#evaluatorversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluators - delete version

```HTTP
DELETE {endpoint}/evaluators/{name}/versions/{version}?api-version=v1
```


Delete the specific version of the EvaluatorVersion. The service returns 204 No Content if the EvaluatorVersion was deleted successfully or if the EvaluatorVersion does not exist.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The version of the EvaluatorVersion to delete. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 204

**Description**: There is no content to send for this request, but the headers may be useful. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Evaluators - update version

```HTTP
PATCH {endpoint}/evaluators/{name}/versions/{version}?api-version=v1
```


Update an existing EvaluatorVersion with the given version id

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The version of the EvaluatorVersion to update. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Evaluations=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| categories | array of [EvaluatorCategory](#evaluatorcategory) | The categories of the evaluator | No |  |
| description | string | The asset description text. | No |  |
| display_name | string | Display Name for evaluator. It helps to find the evaluator easily in AI Foundry. It does not need to be unique. | No |  |
| metadata | object | Metadata about the evaluator | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvaluatorVersion](#evaluatorversion) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

## Indexes

### Indexes - list latest

```HTTP
GET {endpoint}/indexes?api-version=v1
```


List the latest version of each Index

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedIndex](#pagedindex) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Indexes - list versions

```HTTP
GET {endpoint}/indexes/{name}/versions?api-version=v1
```


List all versions of the given Index

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedIndex](#pagedindex) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Indexes - get version

```HTTP
GET {endpoint}/indexes/{name}/versions/{version}?api-version=v1
```


Get the specific version of the Index. The service returns 404 Not Found error if the Index does not exist.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The specific version id of the Index to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Index](#index) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Indexes - delete version

```HTTP
DELETE {endpoint}/indexes/{name}/versions/{version}?api-version=v1
```


Delete the specific version of the Index. The service returns 204 No Content if the Index was deleted successfully or if the Index does not exist.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The version of the Index to delete. |


#### Responses

**Status Code:** 204

**Description**: There is no content to send for this request, but the headers may be useful. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Indexes - create or update version

```HTTP
PATCH {endpoint}/indexes/{name}/versions/{version}?api-version=v1
```


Create a new or update an existing Index with the given version id

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | The name of the resource |
| version | path | Yes | string | The specific version id of the Index to create or update. |

#### Request Body

**Content-Type**: application/merge-patch+json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | [IndexType](#indextype) |  | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Index](#index) | |

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Index](#index) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

## Insights

### Insights - generate

```HTTP
POST {endpoint}/insights?api-version=v1
```


Generate Insights

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Insights=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
| Repeatability-Request-ID | False | string | Unique, client-generated identifier for ensuring request idempotency. Use the same ID for retries to prevent duplicate evaluations. |
| Repeatability-First-Sent | False | string | Timestamp indicating when this request was first initiated. Used in conjunction with repeatability-request-id for idempotency control. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| displayName | string | User friendly display name for the insight. | Yes |  |
| id | string (read-only) | The unique identifier for the insights report. | Yes |  |
| metadata | [InsightsMetadata](#insightsmetadata) (read-only) | Metadata about the insights. | Yes |  |
| └─ completedAt | string | The timestamp when the insights were completed. | No |  |
| └─ createdAt | string | The timestamp when the insights were created. | Yes |  |
| request | [InsightRequest](#insightrequest) | The request of the insights report. | Yes |  |
| └─ type | [InsightType](#insighttype) | The type of request. | Yes |  |
| result | [InsightResult](#insightresult) (read-only) | The result of the insights. | No |  |
| └─ type | [InsightType](#insighttype) | The type of insights result. | Yes |  |
| state | [Azure.Core.Foundations.OperationState](#azurecorefoundationsoperationstate) (read-only) | Enum describing allowed operation states. | Yes |  |

#### Responses

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Insight](#insight) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Insights - list

```HTTP
GET {endpoint}/insights?api-version=v1
```


List all insights in reverse chronological order (newest first).

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| type | query | No | string<br>Possible values: `EvaluationRunClusterInsight`, `AgentClusterInsight`, `EvaluationComparison` | Filter by the type of analysis. |
| evalId | query | No | string | Filter by the evaluation ID. |
| runId | query | No | string | Filter by the evaluation run ID. |
| agentName | query | No | string | Filter by the agent name. |
| includeCoordinates | query | No | boolean | Whether to include coordinates for visualization in the response. Defaults to false. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Insights=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedInsight](#pagedinsight) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Insights - get

```HTTP
GET {endpoint}/insights/{id}?api-version=v1
```


Get a specific insight by Id.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| id | path | Yes | string | The unique identifier for the insights report. |
| includeCoordinates | query | No | boolean | Whether to include coordinates for visualization in the response. Defaults to false. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Insights=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Insight](#insight) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

## Memory Stores

### Create memory store

```HTTP
POST {endpoint}/memory_stores?api-version=v1
```


Create a memory store.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | [MemoryStoreDefinition](#memorystoredefinition) | Base definition for memory store configurations. | Yes |  |
| └─ kind | [MemoryStoreKind](#memorystorekind) | The kind of the memory store. | Yes |  |
| description | string | A human-readable description of the memory store.<br>**Constraints:** maxLength: 512 | No |  |
| metadata | object | Arbitrary key-value metadata to associate with the memory store. | No |  |
| name | string | The name of the memory store.<br>**Constraints:** maxLength: 256 | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [MemoryStoreObject](#memorystoreobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### List memory stores

```HTTP
GET {endpoint}/memory_stores?api-version=v1
```


List all memory stores.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Update memory store

```HTTP
POST {endpoint}/memory_stores/{name}?api-version=v1
```


Update a memory store.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| name | path | Yes | string | The name of the memory store to update. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A human-readable description of the memory store.<br>**Constraints:** maxLength: 512 | No |  |
| metadata | object | Arbitrary key-value metadata to associate with the memory store. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [MemoryStoreObject](#memorystoreobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Get memory store

```HTTP
GET {endpoint}/memory_stores/{name}?api-version=v1
```


Retrieve a memory store.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| name | path | Yes | string | The name of the memory store to retrieve. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [MemoryStoreObject](#memorystoreobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Delete memory store

```HTTP
DELETE {endpoint}/memory_stores/{name}?api-version=v1
```


Delete a memory store.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| name | path | Yes | string | The name of the memory store to delete. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DeleteMemoryStoreResponse](#deletememorystoreresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Get update result

```HTTP
GET {endpoint}/memory_stores/{name}/updates/{update_id}?api-version=v1
```


Get memory store update result.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| name | path | Yes | string | The name of the memory store. |
| update_id | path | Yes | string | The ID of the memory update operation. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [MemoryStoreUpdateResponse](#memorystoreupdateresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Delete scope memories

```HTTP
POST {endpoint}/memory_stores/{name}:delete_scope?api-version=v1
```


Delete all memories associated with a specific scope from a memory store.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| name | path | Yes | string | The name of the memory store. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| scope | string | The namespace that logically groups and isolates memories to delete, such as a user ID. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [MemoryStoreDeleteScopeResponse](#memorystoredeletescoperesponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Search memories

```HTTP
POST {endpoint}/memory_stores/{name}:search_memories?api-version=v1
```


Search for relevant memories from a memory store based on conversation context.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| name | path | Yes | string | The name of the memory store to search. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.InputItem](#openaiinputitem) | Items for which to search for relevant memories. | No |  |
| options | [MemorySearchOptions](#memorysearchoptions) | Memory search options. | No |  |
| └─ max_memories | integer | Maximum number of memory items to return. | No |  |
| previous_search_id | string | The unique ID of the previous search request, enabling incremental memory search from where the last operation left off. | No |  |
| scope | string | The namespace that logically groups and isolates memories, such as a user ID. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [MemoryStoreSearchResponse](#memorystoresearchresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Update memories

```HTTP
POST {endpoint}/memory_stores/{name}:update_memories?api-version=v1
```


Update memory store with conversation memories.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| name | path | Yes | string | The name of the memory store to update. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `MemoryStores=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.InputItem](#openaiinputitem) | Conversation items from which to extract memories. | No |  |
| previous_update_id | string | The unique ID of the previous update request, enabling incremental memory updates from where the last operation left off. | No |  |
| scope | string | The namespace that logically groups and isolates memories, such as a user ID. | Yes |  |
| update_delay | integer | Timeout period before processing the memory update in seconds.<br>If a new update request is received during this period, it will cancel the current request and reset the timeout.<br>Set to 0 to immediately trigger the update without delay.<br>Defaults to 300 (5 minutes). | No | 300 |

#### Responses

**Status Code:** 202

**Description**: The request has been accepted for processing, but processing has not yet completed. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [MemoryStoreUpdateResponse](#memorystoreupdateresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| Operation-Location | string | The location for monitoring the operation state. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Conversations

### Create conversation

```HTTP
POST {endpoint}/openai/v1/conversations
```


Create a conversation.
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.InputItem](#openaiinputitem) |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationResource](#openaiconversationresource) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### List conversations

```HTTP
GET {endpoint}/openai/v1/conversations
```


Returns the list of all conversations.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| agent_name | query | No | string | Filter by agent name. If provided, only items associated with the specified agent will be returned. |
| agent_id | query | No | string | Filter by agent ID in the format `name:version`. If provided, only items associated with the specified agent ID will be returned. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Update conversation

```HTTP
POST {endpoint}/openai/v1/conversations/{conversation_id}
```


Update a conversation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| conversation_id | path | Yes | string | The id of the conversation to update. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationResource](#openaiconversationresource) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Get conversation

```HTTP
GET {endpoint}/openai/v1/conversations/{conversation_id}
```


Retrieves a conversation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| conversation_id | path | Yes | string | The id of the conversation to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationResource](#openaiconversationresource) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Delete conversation

```HTTP
DELETE {endpoint}/openai/v1/conversations/{conversation_id}
```


Deletes a conversation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| conversation_id | path | Yes | string | The id of the conversation to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeletedConversationResource](#openaideletedconversationresource) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Create conversation items

```HTTP
POST {endpoint}/openai/v1/conversations/{conversation_id}/items
```


Create items in a conversation with the given ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| conversation_id | path | Yes | string | The id of the conversation on which the item needs to be created. |
| include | query | No | array | Additional fields to include in the response.<br>See the `include` parameter for listing Conversation items for more information. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.Item](#openaiitem) | The items to add to the conversation. You may add up to 20 items at a time. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationItemList](#openaiconversationitemlist) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### List conversation items

```HTTP
GET {endpoint}/openai/v1/conversations/{conversation_id}/items
```


List all items for a conversation with the given ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| conversation_id | path | Yes | string | The id of the conversation on which the items needs to be listed. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| item_type | query | No | string<br>Possible values: `message`, `output_message`, `file_search_call`, `computer_call`, `computer_call_output`, `web_search_call`, `function_call`, `function_call_output`, `reasoning`, `compaction`, `image_generation_call`, `code_interpreter_call`, `local_shell_call`, `local_shell_call_output`, `shell_call`, `shell_call_output`, `apply_patch_call`, `apply_patch_call_output`, `mcp_list_tools`, `mcp_approval_request`, `mcp_approval_response`, `mcp_call`, `custom_tool_call_output`, `custom_tool_call`, `structured_outputs`, `oauth_consent_request`, `memory_search_call`, `workflow_action` | Filter by item type. If provided, only items of the specified type will be returned. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Get conversation item

```HTTP
GET {endpoint}/openai/v1/conversations/{conversation_id}/items/{item_id}
```


Get a single item from a conversation with the given IDs.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| conversation_id | path | Yes | string | The ID of the conversation that contains the item. |
| item_id | path | Yes | string | The id of the conversation item to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.OutputItem](#openaioutputitem) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Delete conversation item

```HTTP
DELETE {endpoint}/openai/v1/conversations/{conversation_id}/items/{item_id}
```


Delete an item from a conversation with the given IDs.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| conversation_id | path | Yes | string | The id of the conversation on which the item needs to be deleted from. |
| item_id | path | Yes | string | The id of the conversation item to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationResource](#openaiconversationresource) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Evals

### Evals - list evals

```HTTP
GET {endpoint}/openai/v1/evals
```

List all evaluations
List evaluations for a project.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| after | query | No | string | Identifier for the last run from the previous pagination request. |
| limit | query | No | integer | Number of runs to retrieve. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order for runs by timestamp. Use `asc` for ascending order or `desc` for descending order. Defaults to `asc`. |
| order_by | query | No | string<br>Possible values: `created_at`, `updated_at` | Evals can be ordered by creation time or last updated time.<br>Use `created_at` for creation time or `updated_at` for last updated time. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - create eval

```HTTP
POST {endpoint}/openai/v1/evals
```

Create evaluation
Create the structure of an evaluation that can be used to test a model's performance.
An evaluation is a set of testing criteria and the config for a data source, which dictates the schema of the data used in the evaluation. After creating an evaluation, you can run it on different models and model parameters. We support several types of graders and datasources.
For more information, see the 
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source_config | [OpenAI.CreateEvalCustomDataSourceConfig](#openaicreateevalcustomdatasourceconfig) or [OpenAI.CreateEvalLogsDataSourceConfig](#openaicreateevallogsdatasourceconfig) or [OpenAI.CreateEvalStoredCompletionsDataSourceConfig](#openaicreateevalstoredcompletionsdatasourceconfig) or [AzureAIDataSourceConfig](#azureaidatasourceconfig) | The configuration for the data source used for the evaluation runs. Dictates the schema of the data used in the evaluation. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the evaluation. | No |  |
| properties | object | Set of immutable 16 key-value pairs that can be attached to an object for storing additional information.<br>    Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| testing_criteria | array of [OpenAI.EvalGraderLabelModel](#openaievalgraderlabelmodel) or [OpenAI.EvalGraderStringCheck](#openaievalgraderstringcheck) or [OpenAI.EvalGraderTextSimilarity](#openaievalgradertextsimilarity) or [OpenAI.EvalGraderPython](#openaievalgraderpython) or [OpenAI.EvalGraderScoreModel](#openaievalgraderscoremodel) or [EvalGraderAzureAIEvaluator](#evalgraderazureaievaluator) | A list of graders for all eval runs in this group. Graders can reference variables in the data source using double curly braces notation, like `{{item.variable_name}}`. To reference the model's output, use the `sample` namespace (ie, `{{sample.output_text}}`). | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Eval](#eval) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - delete eval

```HTTP
DELETE {endpoint}/openai/v1/evals/{eval_id}
```

Delete an evaluation
Delete an evaluation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DeleteEvalResponse](#deleteevalresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - get eval

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}
```

Get an evaluation
Get an evaluation by ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Eval](#eval) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - update eval

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}
```

Update an evaluation
Update certain properties of an evaluation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation to update. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string |  | No |  |
| properties | object | Set of immutable 16 key-value pairs that can be attached to an object for storing additional information.<br>    Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Eval](#eval) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - list runs

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs
```

Get a list of runs for an evaluation
Get a list of runs for an evaluation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation to retrieve runs for. |
| after | query | No | string | Identifier for the last run from the previous pagination request. |
| limit | query | No | integer | Number of runs to retrieve. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order for runs by timestamp. Use `asc` for ascending order or `desc` for descending order. Defaults to `asc`. |
| status | query | No | string<br>Possible values: `queued`, `in_progress`, `completed`, `canceled`, `failed` . Filter runs by status. One of `queued`, `in_progress`,  `failed`, `completed`, `canceled`. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - create eval run

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}/runs
```

Create evaluation run


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation to create a run for. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source | [OpenAI.CreateEvalJsonlRunDataSource](#openaicreateevaljsonlrundatasource) or [OpenAI.CreateEvalCompletionsRunDataSource](#openaicreateevalcompletionsrundatasource) or [OpenAI.CreateEvalResponsesRunDataSource](#openaicreateevalresponsesrundatasource) or [EvalRunDataSource](#evalrundatasource) | Details about the run's data source. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the run. | No |  |
| properties | object | Set of immutable 16 key-value pairs that can be attached to an object for storing additional information.<br>    Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRun](#evalrun) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - delete eval run

```HTTP
DELETE {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}
```

Delete evaluation run
Delete an eval run.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation to delete the run from. |
| run_id | path | Yes | string | The ID of the run to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DeleteEvalRunResponse](#deleteevalrunresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - get eval run

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}
```

Get an evaluation run
Get an evaluation run by ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation to retrieve runs for. |
| run_id | path | Yes | string | The ID of the run to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRun](#evalrun) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - cancel eval run

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}
```

Cancel evaluation run
Cancel an ongoing evaluation run.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation whose run you want to cancel. |
| run_id | path | Yes | string | The ID of the run to cancel. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRun](#evalrun) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - get eval run output items

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}/output_items
```

Get evaluation run output items
Get a list of output items for an evaluation run.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string | The ID of the run to retrieve output items for. |
| after | query | No | string | Identifier for the last run from the previous pagination request. |
| limit | query | No | integer | Number of runs to retrieve. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order for runs by timestamp. Use `asc` for ascending order or `desc` for descending order. Defaults to `asc`. |
| status | query | No | string<br>Possible values: `fail`, `pass` | Filter output items by status. Use `failed` to filter by failed output<br>items or `pass` to filter by passed output items. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Evals - get eval run output item

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}/output_items/{output_item_id}
```

Get an output item of an evaluation run
Get an evaluation run output item by ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| eval_id | path | Yes | string | The ID of the evaluation to retrieve runs for. |
| run_id | path | Yes | string | The ID of the run to retrieve. |
| output_item_id | path | Yes | string | The ID of the output item to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRunOutputItem](#evalrunoutputitem) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Fine-Tuning

### Create fine tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs?api-version=v1
```


Creates a fine-tuning job which begins the process of creating a new model from a given dataset.

Response includes details of the enqueued job including job status and the name of the fine-tuned models once complete.

[Learn more about fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [OpenAI.CreateFineTuningJobRequestHyperparameters](#openaicreatefinetuningjobrequesthyperparameters) |  | No |  |
| └─ batch_size | string or [OpenAI.integer](#openaiinteger) |  | No | auto |
| └─ learning_rate_multiplier | string or [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ n_epochs | string or [OpenAI.integer](#openaiinteger) |  | No | auto |
| integrations | array of [OpenAI.CreateFineTuningJobRequestIntegrations](#openaicreatefinetuningjobrequestintegrations) | A list of integrations to enable for your fine-tuning job. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string (see valid models below) | The name of the model to fine-tune. You can select one of the<br>  [supported models](https://platform.openai.com/docs/guides/fine-tuning#which-models-can-be-fine-tuned). | Yes |  |
| seed | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| suffix | string (nullable) | A string of up to 64 characters that will be added to your fine-tuned model name.<br>  For example, a `suffix` of "custom-model-name" would produce a model name like `ft:gpt-4o-mini:openai:custom-model-name:7p4lURel`.<br>**Constraints:** minLength: 1, maxLength: 64 | No |  |
| training_file | string | The ID of an uploaded file that contains training data.<br>  See [upload file](https://platform.openai.com/docs/api-reference/files/create) for how to upload a file.<br>  Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose `fine-tune`.<br>  The contents of the file should differ depending on if the model uses the [chat](https://platform.openai.com/docs/api-reference/fine-tuning/chat-input), [completions](https://platform.openai.com/docs/api-reference/fine-tuning/completions-input) format, or if the fine-tuning method uses the [preference](https://platform.openai.com/docs/api-reference/fine-tuning/preference-input) format.<br>  See the [fine-tuning guide](https://platform.openai.com/docs/guides/model-optimization) for more details. | Yes |  |
| validation_file | string (nullable) | The ID of an uploaded file that contains validation data.<br>  If you provide this file, the data is used to generate validation<br>  metrics periodically during fine-tuning. These metrics can be viewed in<br>  the fine-tuning results file.<br>  The same data should not be present in both train and validation files.<br>  Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`.<br>  See the [fine-tuning guide](https://platform.openai.com/docs/guides/model-optimization) for more details. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### List paginated fine tuning jobs

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs?api-version=v1
```


List your organization's fine-tuning jobs

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| after | query | No | string | Identifier for the last job from the previous pagination request. |
| limit | query | No | integer | Number of fine-tuning jobs to retrieve. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListPaginatedFineTuningJobsResponse](#openailistpaginatedfinetuningjobsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Retrieve fine tuning job

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}?api-version=v1
```


Get info about a fine-tuning job.

[Learn more about fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Cancel fine tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/cancel?api-version=v1
```


Immediately cancel a fine-tune job.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to cancel. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### List fine tuning job checkpoints

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints?api-version=v1
```


List checkpoints for a fine-tuning job.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to get checkpoints for. |
| after | query | No | string | Identifier for the last checkpoint ID from the previous pagination request. |
| limit | query | No | integer | Number of checkpoints to retrieve. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFineTuningJobCheckpointsResponse](#openailistfinetuningjobcheckpointsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### List fine tuning job events

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/events?api-version=v1
```


Get fine-grained status updates for a fine-tuning job.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to get events for. |
| after | query | No | string | Identifier for the last event from the previous pagination request. |
| limit | query | No | integer | Number of events to retrieve. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFineTuningJobEventsResponse](#openailistfinetuningjobeventsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Pause fine tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/pause?api-version=v1
```


Pause a running fine-tune job.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to pause. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Resume fine tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/resume?api-version=v1
```


Resume a paused fine-tune job.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to resume. |
| api-version | query | Yes | string | The API version to use for this operation. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Responses

### Create response - create response stream

```HTTP
POST {endpoint}/openai/v1/responses
```


Creates a model response. Creates a model response (streaming response).
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| background | boolean (nullable) |  | No |  |
| conversation | [OpenAI.ConversationParam](#openaiconversationparam) (nullable) | The conversation that this response belongs to. Items from this conversation are prepended to `input_items` for this response request.<br>Input items and output items from this response are automatically added to this conversation after this response completes. | No |  |
| include | array of [OpenAI.IncludeEnum](#openaiincludeenum) |  | No |  |
| input | [OpenAI.InputParam](#openaiinputparam) | Text, image, or file inputs to the model, used to generate a response.<br>Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Image inputs](https://platform.openai.com/docs/guides/images)<br>- [File inputs](https://platform.openai.com/docs/guides/pdf-files)<br>- [Conversation state](https://platform.openai.com/docs/guides/conversation-state)<br>- [Function calling](https://platform.openai.com/docs/guides/function-calling) | No |  |
| instructions | string (nullable) |  | No |  |
| max_output_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| max_tool_calls | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| model | string | The model deployment to use for the creation of this response. | No |  |
| parallel_tool_calls | boolean (nullable) |  | No | True |
| previous_response_id | string (nullable) |  | No |  |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| prompt_cache_retention | enum | <br>Possible values: `in-memory`, `24h` | No |  |
| reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| └─ generate_summary | enum | <br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | <br>Possible values: `auto`, `concise`, `detailed` | No |  |
| safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| service_tier | [OpenAI.ServiceTier](#openaiservicetier) | Specifies the processing type used for serving the request.<br>- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.<br>- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.<br>- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.<br>- When not set, the default behavior is 'auto'.<br>When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter. | No |  |
| store | boolean (nullable) |  | No | True |
| stream | boolean (nullable) |  | No |  |
| stream_options | [OpenAI.ResponseStreamOptions](#openairesponsestreamoptions) (nullable) | Options for streaming responses. Only set this when you set `stream: true`. | No |  |
| └─ include_obfuscation | boolean | When true, stream obfuscation will be enabled. Stream obfuscation adds<br>  random characters to an `obfuscation` field on streaming delta events to<br>  normalize payload sizes as a mitigation to certain side-channel attacks.<br>  These obfuscation fields are included by default, but add a small amount<br>  of overhead to the data stream. You can set `include_obfuscation` to<br>  false to optimize for bandwidth if you trust the network links between<br>  your application and the OpenAI API. | No |  |
| structured_inputs | object | The structured inputs to the response that can participate in prompt template substitution or tool argument bindings. | No |  |
| temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) |  | No |  |
| tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| top_logprobs | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| truncation | enum | <br>Possible values: `auto`, `disabled` | No |  |
| user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Response](#openairesponse) | |
|text/event-stream | [OpenAI.CreateResponseStreamingResponse](#openaicreateresponsestreamingresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### List responses

```HTTP
GET {endpoint}/openai/v1/responses
```


Returns the list of all responses.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| agent_name | query | No | string | Filter by agent name. If provided, only items associated with the specified agent will be returned. |
| agent_id | query | No | string | Filter by agent ID in the format `name:version`. If provided, only items associated with the specified agent ID will be returned. |
| conversation_id | query | No | string | Filter by conversation ID. If provided, only responses associated with the specified conversation will be returned. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Compact response conversation

```HTTP
POST {endpoint}/openai/v1/responses/compact
```


Produces a compaction of a responses conversation.
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string or array of [OpenAI.InputItem](#openaiinputitem) |  | No |  |
| instructions | string (nullable) |  | No |  |
| model | [OpenAI.ModelIdsCompaction](#openaimodelidscompaction) | Model ID used to generate the response, like `gpt-5` or `o3`. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models) to browse and compare available models. | Yes |  |
| previous_response_id | string (nullable) |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.CompactResource](#openaicompactresource) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Get response - get response stream

```HTTP
GET {endpoint}/openai/v1/responses/{response_id}
```


Retrieves a model response with the given ID. Retrieves a model response with the given ID (streaming response).

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| response_id | path | Yes | string |  |
| include[] | query | No | array |  |
| stream | query | No | boolean |  |
| starting_after | query | No | integer |  |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| accept | False | string<br>Possible values: `text/event-stream` |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Response](#openairesponse) | |
|text/event-stream | [OpenAI.CreateResponseStreamingResponse](#openaicreateresponsestreamingresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Delete response

```HTTP
DELETE {endpoint}/openai/v1/responses/{response_id}
```


Deletes a model response.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| response_id | path | Yes | string | The ID of the response to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [DeleteResponseResult](#deleteresponseresult) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### Cancel response

```HTTP
POST {endpoint}/openai/v1/responses/{response_id}/cancel
```


Cancels a model response.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| response_id | path | Yes | string | The ID of the response to cancel. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Response](#openairesponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

### List input items

```HTTP
GET {endpoint}/openai/v1/responses/{response_id}/input_items
```


Returns a list of input items for a given response.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| response_id | path | Yes | string |  |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | The response data for a requested list of items.|

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Redteams

### Redteams - list

```HTTP
GET {endpoint}/redTeams/runs?api-version=v1
```


List a redteam by name.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `RedTeams=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedRedTeam](#pagedredteam) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Redteams - get

```HTTP
GET {endpoint}/redTeams/runs/{name}?api-version=v1
```


Get a redteam by name.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| name | path | Yes | string | Identifier of the red team run. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `RedTeams=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [RedTeam](#redteam) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Redteams - create

```HTTP
POST {endpoint}/redTeams/runs:run?api-version=v1
```


Creates a redteam run.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `RedTeams=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| applicationScenario | string | Application scenario for the red team operation, to generate scenario specific attacks. | No |  |
| attackStrategies | array of [AttackStrategy](#attackstrategy) | List of attack strategies or nested lists of attack strategies. | No |  |
| displayName | string | Name of the red-team run. | No |  |
| id | string (read-only) | Identifier of the red team run. | Yes |  |
| numTurns | integer | Number of simulation rounds. | No |  |
| properties | object | Red team's properties. Unlike tags, properties are add-only. Once added, a property cannot be removed. | No |  |
| riskCategories | array of [RiskCategory](#riskcategory) | List of risk categories to generate attack objectives for. | No |  |
| simulationOnly | boolean | Simulation-only or Simulation + Evaluation. Default false, if true the scan outputs conversation not evaluation result. | No | False |
| status | string (read-only) | Status of the red-team. It is set by service and is read-only. | No |  |
| tags | object | Red team's tags. Unlike properties, tags are fully mutable. | No |  |
| target | [TargetConfig](#targetconfig) | Abstract class for target configuration. | Yes |  |
| └─ type | string | Type of the model configuration. | Yes |  |

#### Responses

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [RedTeam](#redteam) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Schedules

### Schedules - list

```HTTP
GET {endpoint}/schedules?api-version=v1
```


List all schedules.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| type | query | No | string<br>Possible values: `Evaluation`, `Insight` | Filter by the type of schedule. |
| enabled | query | No | boolean | Filter by the enabled status. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Schedules=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedSchedule](#pagedschedule) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Schedules - delete

```HTTP
DELETE {endpoint}/schedules/{id}?api-version=v1
```


Delete a schedule.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| id | path | Yes | string | Identifier of the schedule. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Schedules=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 204

**Description**: There is no content to send for this request, but the headers may be useful. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Schedules - get

```HTTP
GET {endpoint}/schedules/{id}?api-version=v1
```


Get a schedule by id.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| id | path | Yes | string | Identifier of the schedule. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Schedules=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Schedule](#schedule) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Schedules - create or update

```HTTP
PUT {endpoint}/schedules/{id}?api-version=v1
```


Create or update operation template.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| id | path | Yes | string | Identifier of the schedule. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Schedules=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | Description of the schedule. | No |  |
| displayName | string | Name of the schedule. | No |  |
| enabled | boolean | Enabled status of the schedule. | Yes |  |
| id | string (read-only) | Identifier of the schedule. | Yes |  |
| properties | object | Schedule's properties. Unlike tags, properties are add-only. Once added, a property cannot be removed. | No |  |
| provisioningStatus | [ScheduleProvisioningStatus](#scheduleprovisioningstatus) (read-only) | Schedule provisioning status. | No |  |
| systemData | object (read-only) | System metadata for the resource. | Yes |  |
| tags | object | Schedule's tags. Unlike properties, tags are fully mutable. | No |  |
| task | [ScheduleTask](#scheduletask) | Schedule task model. | Yes |  |
| └─ configuration | object | Configuration for the task. | No |  |
| └─ type | [ScheduleTaskType](#scheduletasktype) | Type of the task. | Yes |  |
| trigger | [Trigger](#trigger) | Base model for Trigger of the schedule. | Yes |  |
| └─ type | [TriggerType](#triggertype) | Type of the trigger. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Schedule](#schedule) | |

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Schedule](#schedule) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Schedules - list runs

```HTTP
GET {endpoint}/schedules/{id}/runs?api-version=v1
```


List all schedule runs.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| api-version | query | Yes | string | The API version to use for this operation. |
| id | path | Yes | string | Identifier of the schedule. |
| type | query | No | string<br>Possible values: `Evaluation`, `Insight` | Filter by the type of schedule. |
| enabled | query | No | boolean | Filter by the enabled status. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Schedules=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [PagedScheduleRun](#pagedschedulerun) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Azure.Core.Foundations.ErrorResponse](#azurecorefoundationserrorresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| x-ms-error-code | string | String error code indicating what went wrong. |

### Schedules - get run

```HTTP
GET {endpoint}/schedules/{schedule_id}/runs/{run_id}?api-version=v1
```


Get a schedule run by id.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Foundry Project endpoint in the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}".<br>If you only have one Project in your Foundry Hub, or to target the default Project<br>in your Hub, use the form<br>"https://{ai-services-account-name}.services.ai.azure.com/api/projects/_project" |
| schedule_id | path | Yes | string | The unique identifier of the schedule. |
| run_id | path | Yes | string | The unique identifier of the schedule run. |
| api-version | query | Yes | string | The API version to use for this operation. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Foundry-Features | True | string<br>Possible values: `Schedules=V1Preview` | A feature flag opt-in required when using preview operations or modifying persisted preview resources. |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ScheduleRun](#schedulerun) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ApiErrorResponse](#apierrorresponse) | |

## Components

### A2APreviewTool

An agent implementing the A2A protocol.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_card_path | string | The path to the agent card relative to the `base_url`.<br>If not provided, defaults to  `/.well-known/agent-card.json` | No |  |
| base_url | string | Base URL of the agent. | No |  |
| project_connection_id | string | The connection ID in the project for the A2A server.<br>The connection stores authentication and other connection details needed to connect to the A2A server. | No |  |
| type | enum | The type of the tool. Always `"a2a_preview`.<br>Possible values: `a2a_preview` | Yes |  |

### AISearchIndexResource

A AI Search Index resource.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filter | string | filter string for search resource. [Learn more here](https://learn.microsoft.com/azure/search/search-filters). | No |  |
| index_asset_id | string | Index asset id for search resource. | No |  |
| index_name | string | The name of an index in an IndexResource attached to this agent. | No |  |
| project_connection_id | string | An index connection ID in an IndexResource attached to this agent. | No |  |
| query_type | [AzureAISearchQueryType](#azureaisearchquerytype) | Available query types for Azure AI Search tool. | No |  |
| top_k | integer | Number of documents to retrieve from search and present to the model. | No |  |

### AgentClusterInsightRequest

Insights on set of Agent Evaluation Results

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agentName | string | Identifier for the agent. | Yes |  |
| modelConfiguration | [InsightModelConfiguration](#insightmodelconfiguration) | Configuration of the model used in the insight generation. | No |  |
| └─ modelDeploymentName | string | The model deployment to be evaluated. Accepts either the deployment name alone or with the connection name as `{connectionName}/<modelDeploymentName>`. | Yes |  |
| type | enum | The type of request.<br>Possible values: `AgentClusterInsight` | Yes |  |

### AgentClusterInsightResult

Insights from the agent cluster analysis.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| clusterInsight | [ClusterInsightResult](#clusterinsightresult) | Insights from the cluster analysis. | Yes |  |
| type | enum | The type of insights result.<br>Possible values: `AgentClusterInsight` | Yes |  |

### AgentContainerObject

The details of the container of a specific version of an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container | [ContainerDetails](#containerdetails) (read-only) | Detailed information about the container. | No |  |
| └─ health_state | string | The health state of the container. | Yes |  |
| └─ provisioning_error | string | The provisioning error of the container, if any. | No |  |
| └─ provisioning_state | string | The provisioning state of the container. | Yes |  |
| └─ replicas | array of [ContainerReplica](#containerreplica) | The list of replicas in the container. | Yes |  |
| └─ state | string | The state of the container. | Yes |  |
| └─ updated_on | string | The last update time of the container. | Yes |  |
| created_at | string | The creation time of the container. | Yes |  |
| error_message | string (read-only) | The error message if the container failed to operate, if any. | No |  |
| id | string (read-only) | The identifier of the container. | No |  |
| max_replicas | integer | The maximum number of replicas for the container. Default is 1. | No |  |
| min_replicas | integer | The minimum number of replicas for the container. Default is 1. | No |  |
| object | enum | The object type, which is always 'agent.container'.<br>Possible values: `agent.container` | Yes |  |
| status | [AgentContainerStatus](#agentcontainerstatus) (read-only) | Status of the container of a specific version of an agent. | Yes |  |
| updated_at | string | The last update time of the container. | Yes |  |

### AgentContainerOperationError

The error details of the container operation, if any.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The error code of the container operation, if any. | Yes |  |
| message | string | The error message of the container operation, if any. | Yes |  |
| type | string | The error type of the container operation, if any. | Yes |  |

### AgentContainerOperationObject

The container operation for a specific version of an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_id | string | The ID of the agent. | Yes |  |
| agent_version_id | string | The ID of the agent version. | Yes |  |
| container | [AgentContainerObject](#agentcontainerobject) | The details of the container of a specific version of an agent. | No |  |
| └─ container | [ContainerDetails](#containerdetails) (read-only) | The detailed container information. | No |  |
| └─ created_at | string (read-only) | The creation time of the container. | Yes |  |
| └─ error_message | string (read-only) | The error message if the container failed to operate, if any. | No |  |
| └─ id | string (read-only) | The identifier of the container. | No |  |
| └─ max_replicas | integer | The maximum number of replicas for the container. Default is 1. | No |  |
| └─ min_replicas | integer | The minimum number of replicas for the container. Default is 1. | No |  |
| └─ object | enum | The object type, which is always 'agent.container'.<br>Possible values: `agent.container` | Yes |  |
| └─ status | [AgentContainerStatus](#agentcontainerstatus) (read-only) | The status of the container of a specific version of an agent. | Yes |  |
| └─ updated_at | string (read-only) | The last update time of the container. | Yes |  |
| error | [AgentContainerOperationError](#agentcontaineroperationerror) | The error details of the container operation, if any. | No |  |
| └─ code | string | The error code of the container operation, if any. | Yes |  |
| └─ message | string | The error message of the container operation, if any. | Yes |  |
| └─ type | string | The error type of the container operation, if any. | Yes |  |
| id | string | The ID of the container operation. This id is unique identifier across the system. | Yes |  |
| status | [AgentContainerOperationStatus](#agentcontaineroperationstatus) | Status of the container operation for a specific version of an agent. | Yes |  |

### AgentContainerOperationStatus

Status of the container operation for a specific version of an agent.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `NotStarted`<br>`InProgress`<br>`Succeeded`<br>`Failed` |

### AgentContainerStatus

Status of the container of a specific version of an agent.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `Starting`<br>`Running`<br>`Stopping`<br>`Stopped`<br>`Failed`<br>`Deleting`<br>`Deleted`<br>`Updating` |

### AgentDefinition


### Discriminator for AgentDefinition

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `prompt` | [PromptAgentDefinition](#promptagentdefinition) |
| `workflow` | [WorkflowAgentDefinition](#workflowagentdefinition) |
| `hosted` | [HostedAgentDefinition](#hostedagentdefinition) |
| `container_app` | [ContainerAppAgentDefinition](#containerappagentdefinition) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [AgentKind](#agentkind) |  | Yes |  |
| rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| └─ rai_policy_name | string | The name of the RAI policy to apply. | Yes |  |

### AgentKind

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `prompt`<br>`hosted`<br>`container_app`<br>`workflow` |

### AgentObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique identifier of the agent. | Yes |  |
| name | string | The name of the agent.<br>**Constraints:** maxLength: 63 | Yes |  |
| object | enum | The object type, which is always 'agent'.<br>Possible values: `agent` | Yes |  |
| versions | object | The latest version of the agent. | Yes |  |
| └─ latest | [AgentVersionObject](#agentversionobject) |  | Yes |  |

### AgentProtocol

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `activity_protocol`<br>`responses` |

### AgentReference

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| type | enum | <br>Possible values: `agent_reference` | Yes |  |
| version | string | The version identifier of the agent. | No |  |

### AgentTaxonomyInput

Input configuration for the evaluation taxonomy when the input type is agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| riskCategories | array of [RiskCategory](#riskcategory) | List of risk categories to evaluate against. | Yes |  |
| target | [Target](#target) | Base class for targets with discriminator support. | Yes |  |
| └─ type | string | The type of target. | Yes |  |
| type | enum | Input type of the evaluation taxonomy.<br>Possible values: `agent` | Yes |  |

### AgentTaxonomyInputUpdate

Input configuration for the evaluation taxonomy when the input type is agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| riskCategories | array of [RiskCategory](#riskcategory) | List of risk categories to evaluate against. | No |  |
| target | [TargetUpdate](#targetupdate) | Base class for targets with discriminator support. | No |  |
| └─ type | string | The type of target. | Yes |  |
| type | enum | Input type of the evaluation taxonomy.<br>Possible values: `agent` | Yes |  |

### AgentVersionObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (seconds) when the agent was created. | Yes |  |
| definition | [AgentDefinition](#agentdefinition) |  | Yes |  |
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| id | string | The unique identifier of the agent version. | Yes |  |
| metadata | object (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| name | string | The name of the agent. Name can be used to retrieve/update/delete the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| object | enum | The object type, which is always 'agent.version'.<br>Possible values: `agent.version` | Yes |  |
| version | string | The version identifier of the agent. Agents are immutable and every update creates a new version while keeping the name same. | Yes |  |

### AgenticIdentityPreviewCredentials

Agentic identity credential definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The credential type<br>Possible values: `AgenticIdentityToken_Preview` | Yes |  |

### ApiErrorResponse

Error response for API failures.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | [OpenAI.Error](#openaierror) |  | Yes |  |

### ApiKeyCredentials

API Key Credential definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| key | string (read-only) | API Key | No |  |
| type | enum | The credential type<br>Possible values: `ApiKey` | Yes |  |

### AssetCredentialResponse

Represents a reference to a blob for consumption

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| blobReference | [BlobReference](#blobreference) | Blob reference details. | Yes |  |
| └─ blobUri | string | Blob URI path for client to upload data. Example: ``https://blob.windows.core.net/Container/Path`` | Yes |  |
| └─ credential | [SasCredential](#sascredential) | Credential info to access the storage account. | Yes |  |
| └─ storageAccountArmId | string | ARM ID of the storage account to use. | Yes |  |

### AssetId

Identifier of a saved asset.

**Type**: string


### AttackStrategy

Strategies for attacks.

| Property | Value |
|----------|-------|
| **Description** | Strategies for attacks. |
| **Type** | string |
| **Values** | `easy`<br>`moderate`<br>`difficult`<br>`ascii_art`<br>`ascii_smuggler`<br>`atbash`<br>`base64`<br>`binary`<br>`caesar`<br>`character_space`<br>`jailbreak`<br>`ansi_attack`<br>`character_swap`<br>`suffix_append`<br>`string_join`<br>`unicode_confusable`<br>`unicode_substitution`<br>`diacritic`<br>`flip`<br>`leetspeak`<br>`rot13`<br>`morse`<br>`url`<br>`baseline`<br>`indirect_jailbreak`<br>`tense`<br>`multi_turn`<br>`crescendo` |

### Azure.Core.Foundations.Error

The error object.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | One of a server-defined set of error codes. | Yes |  |
| details | array of [Azure.Core.Foundations.Error](#azurecorefoundationserror) | An array of details about specific errors that led to this reported error. | No |  |
| innererror | [Azure.Core.Foundations.InnerError](#azurecorefoundationsinnererror) | An object containing more specific information about the error. As per Azure REST API guidelines - https://aka.ms/AzureRestApiGuidelines#handling-errors. | No |  |
| └─ code | string | One of a server-defined set of error codes. | No |  |
| └─ innererror | [Azure.Core.Foundations.InnerError](#azurecorefoundationsinnererror) | Inner error. | No |  |
| message | string | A human-readable representation of the error. | Yes |  |
| target | string | The target of the error. | No |  |

### Azure.Core.Foundations.ErrorResponse

A response containing error details.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | [Azure.Core.Foundations.Error](#azurecorefoundationserror) | The error object. | Yes |  |
| └─ code | string | One of a server-defined set of error codes. | Yes |  |
| └─ details | array of [Azure.Core.Foundations.Error](#azurecorefoundationserror) | An array of details about specific errors that led to this reported error. | No |  |
| └─ innererror | [Azure.Core.Foundations.InnerError](#azurecorefoundationsinnererror) | An object containing more specific information than the current object about the error. | No |  |
| └─ message | string | A human-readable representation of the error. | Yes |  |
| └─ target | string | The target of the error. | No |  |

### Azure.Core.Foundations.InnerError

An object containing more specific information about the error. As per Azure REST API guidelines - https://aka.ms/AzureRestApiGuidelines#handling-errors.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | One of a server-defined set of error codes. | No |  |
| innererror | [Azure.Core.Foundations.InnerError](#azurecorefoundationsinnererror) | An object containing more specific information about the error. As per Azure REST API guidelines - https://aka.ms/AzureRestApiGuidelines#handling-errors. | No |  |
| └─ code | string | One of a server-defined set of error codes. | No |  |
| └─ innererror | [Azure.Core.Foundations.InnerError](#azurecorefoundationsinnererror) | Inner error. | No |  |

### Azure.Core.Foundations.OperationState

Enum describing allowed operation states.

| Property | Value |
|----------|-------|
| **Description** | Enum describing allowed operation states. |
| **Type** | string |
| **Values** | `NotStarted`<br>`Running`<br>`Succeeded`<br>`Failed`<br>`Canceled` |

### Azure.Core.uuid

Universally Unique Identifier

**Type**: string

**Format**: uuid


### AzureAIAgentTarget

Represents a target specifying an Azure AI agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The unique identifier of the Azure AI agent. | Yes |  |
| tool_descriptions | array of [ToolDescription](#tooldescription) | The parameters used to control the sampling behavior of the agent during text generation. | No |  |
| type | enum | The type of target, always `azure_ai_agent`.<br>Possible values: `azure_ai_agent` | Yes |  |
| version | string | The version of the Azure AI agent. | No |  |

### AzureAIAgentTargetUpdate

Represents a target specifying an Azure AI agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The unique identifier of the Azure AI agent. | No |  |
| tool_descriptions | array of [ToolDescription](#tooldescription) | The parameters used to control the sampling behavior of the agent during text generation. | No |  |
| type | enum | The type of target, always `azure_ai_agent`.<br>Possible values: `azure_ai_agent` | Yes |  |
| version | string | The version of the Azure AI agent. | No |  |

### AzureAIDataSourceConfig

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| scenario | enum | Data schema scenario.<br>Possible values: `red_team`, `responses`, `traces_preview`, `synthetic_data_gen_preview` | Yes |  |
| schema | object | The overall object JSON schema for the run data source items. | Yes |  |
| type | enum | The object type, which is always `azure_ai_source`.<br>Possible values: `azure_ai_source` | Yes |  |

### AzureAIModelTarget

Represents a target specifying an Azure AI model for operations requiring model selection.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| model | string | The unique identifier of the Azure AI model. | No |  |
| sampling_params | [ModelSamplingParams](#modelsamplingparams) | Represents a set of parameters used to control the sampling behavior of a language model during text generation. | No |  |
| └─ max_completion_tokens | integer | The maximum number of tokens allowed in the completion. | Yes |  |
| └─ seed | integer | The random seed for reproducibility. | Yes |  |
| └─ temperature | number | The temperature parameter for sampling. | Yes |  |
| └─ top_p | number | The top-p parameter for nucleus sampling. | Yes |  |
| type | enum | The type of target, always `azure_ai_model`.<br>Possible values: `azure_ai_model` | Yes |  |

### AzureAIModelTargetUpdate

Represents a target specifying an Azure AI model for operations requiring model selection.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| model | string | The unique identifier of the Azure AI model. | No |  |
| sampling_params | [ModelSamplingParamsUpdate](#modelsamplingparamsupdate) | Represents a set of parameters used to control the sampling behavior of a language model during text generation. | No |  |
| └─ max_completion_tokens | integer | The maximum number of tokens allowed in the completion. | No |  |
| └─ seed | integer | The random seed for reproducibility. | No |  |
| └─ temperature | number | The temperature parameter for sampling. | No |  |
| └─ top_p | number | The top-p parameter for nucleus sampling. | No |  |
| type | enum | The type of target, always `azure_ai_model`.<br>Possible values: `azure_ai_model` | Yes |  |

### AzureAIResponsesEvalRunDataSource

Represents a data source for evaluation runs that are specific to Continuous Evaluation scenarios.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| event_configuration_id | string | The event configuration name associated with this evaluation run. | Yes |  |
| item_generation_params | [ResponseRetrievalItemGenerationParams](#responseretrievalitemgenerationparams) | Represents the parameters for response retrieval item generation. | Yes |  |
| └─ data_mapping | object | Mapping from source fields to response_id field, required for retrieving chat history. | Yes |  |
| └─ max_num_turns | integer | The maximum number of turns of chat history to evaluate. | Yes |  |
| └─ source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) | The source from which JSONL content is read. | Yes |  |
| └─ type | enum | The type of item generation parameters, always `response_retrieval`.<br>Possible values: `response_retrieval` | Yes |  |
| max_runs_hourly | integer | Maximum number of evaluation runs allowed per hour. | Yes |  |
| type | enum | The type of data source, always `azure_ai_responses`.<br>Possible values: `azure_ai_responses` | Yes |  |

### AzureAISearchIndex

Azure AI Search Index Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| name | string (read-only) | The name of the resource | Yes |  |
| type | enum | Type of index<br>Possible values: `AzureSearch` | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### AzureAISearchIndexUpdate

Azure AI Search Index Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | enum | Type of index<br>Possible values: `AzureSearch` | Yes |  |

### AzureAISearchQueryType

Available query types for Azure AI Search tool.

| Property | Value |
|----------|-------|
| **Description** | Available query types for Azure AI Search tool. |
| **Type** | string |
| **Values** | `simple`<br>`semantic`<br>`vector`<br>`vector_simple_hybrid`<br>`vector_semantic_hybrid` |

### AzureAISearchTool

The input definition information for an Azure AI search tool as used to configure an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| azure_ai_search | [AzureAISearchToolResource](#azureaisearchtoolresource) | A set of index resources used by the `azure_ai_search` tool. | Yes |  |
| └─ indexes | array of [AISearchIndexResource](#aisearchindexresource) | The indices attached to this agent. There can be a maximum of 1 index<br>resource attached to the agent.<br>**Constraints:** maxItems: 1 | Yes |  |
| type | enum | The object type, which is always 'azure_ai_search'.<br>Possible values: `azure_ai_search` | Yes |  |

### AzureAISearchToolResource

A set of index resources used by the `azure_ai_search` tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| indexes | array of [AISearchIndexResource](#aisearchindexresource) | The indices attached to this agent. There can be a maximum of 1 index<br>resource attached to the agent. | Yes |  |

### AzureFunctionBinding

The structure for keeping storage queue name and URI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| storage_queue | [AzureFunctionStorageQueue](#azurefunctionstoragequeue) | The structure for keeping storage queue name and URI. | Yes |  |
| └─ queue_name | string | The name of an Azure function storage queue. | Yes |  |
| └─ queue_service_endpoint | string | URI to the Azure Storage Queue service allowing you to manipulate a queue. | Yes |  |
| type | enum | The type of binding, which is always 'storage_queue'.<br>Possible values: `storage_queue` | Yes |  |

### AzureFunctionDefinition

The definition of Azure function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | object | The definition of azure function and its parameters. | Yes |  |
| └─ description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| └─ name | string | The name of the function to be called. | Yes |  |
| └─ parameters | object | The parameters the functions accepts, described as a JSON Schema object. | Yes |  |
| input_binding | [AzureFunctionBinding](#azurefunctionbinding) | The structure for keeping storage queue name and URI. | Yes |  |
| └─ storage_queue | [AzureFunctionStorageQueue](#azurefunctionstoragequeue) | Storage queue. | Yes |  |
| └─ type | enum | The type of binding, which is always 'storage_queue'.<br>Possible values: `storage_queue` | Yes |  |
| output_binding | [AzureFunctionBinding](#azurefunctionbinding) | The structure for keeping storage queue name and URI. | Yes |  |
| └─ storage_queue | [AzureFunctionStorageQueue](#azurefunctionstoragequeue) | Storage queue. | Yes |  |
| └─ type | enum | The type of binding, which is always 'storage_queue'.<br>Possible values: `storage_queue` | Yes |  |

### AzureFunctionStorageQueue

The structure for keeping storage queue name and URI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| queue_name | string | The name of an Azure function storage queue. | Yes |  |
| queue_service_endpoint | string | URI to the Azure Storage Queue service allowing you to manipulate a queue. | Yes |  |

### AzureFunctionTool

The input definition information for an Azure Function Tool, as used to configure an Agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| azure_function | [AzureFunctionDefinition](#azurefunctiondefinition) | The definition of Azure function. | Yes |  |
| └─ function | object | The definition of azure function and its parameters. | Yes |  |
|   └─ description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
|   └─ name | string | The name of the function to be called. | Yes |  |
|   └─ parameters | object | The parameters the functions accepts, described as a JSON Schema object. | Yes |  |
| └─ input_binding | [AzureFunctionBinding](#azurefunctionbinding) | Input storage queue. The queue storage trigger runs a function as messages are added to it. | Yes |  |
| └─ output_binding | [AzureFunctionBinding](#azurefunctionbinding) | Output storage queue. The function writes output to this queue when the input items are processed. | Yes |  |
| type | enum | The object type, which is always 'browser_automation'.<br>Possible values: `azure_function` | Yes |  |

### AzureOpenAIModelConfiguration

Azure OpenAI model configuration. The API version would be selected by the service for querying the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| modelDeploymentName | string | Deployment name for AOAI model. Example: gpt-4o if in AIServices or connection based `connection_name/deployment_name` (e.g. `my-aoai-connection/gpt-4o`). | Yes |  |
| type | enum | <br>Possible values: `AzureOpenAIModel` | Yes |  |

### BaseCredentials

A base class for connection credentials


### Discriminator for BaseCredentials

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `ApiKey` | [ApiKeyCredentials](#apikeycredentials) |
| `AAD` | [EntraIDCredentials](#entraidcredentials) |
| `CustomKeys` | [CustomCredential](#customcredential) |
| `SAS` | [SASCredentials](#sascredentials) |
| `None` | [NoAuthenticationCredentials](#noauthenticationcredentials) |
| `AgenticIdentityToken_Preview` | [AgenticIdentityPreviewCredentials](#agenticidentitypreviewcredentials) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [CredentialType](#credentialtype) (read-only) | The credential type used by the connection | Yes |  |

### BingCustomSearchConfiguration

A bing custom search configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| count | integer | The number of search results to return in the bing api response | No |  |
| freshness | string | Filter search results by a specific time range. See [accepted values here](https://learn.microsoft.com/bing/search-apis/bing-web-search/reference/query-parameters). | No |  |
| instance_name | string | Name of the custom configuration instance given to config. | Yes |  |
| market | string | The market where the results come from. | No |  |
| project_connection_id | string | Project connection id for grounding with bing search | Yes |  |
| set_lang | string | The language to use for user interface strings when calling Bing API. | No |  |

### BingCustomSearchPreviewTool

The input definition information for a Bing custom search tool as used to configure an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bing_custom_search_preview | [BingCustomSearchToolParameters](#bingcustomsearchtoolparameters) | The bing custom search tool parameters. | Yes |  |
| └─ search_configurations | array of [BingCustomSearchConfiguration](#bingcustomsearchconfiguration) | The project connections attached to this tool. There can be a maximum of 1 connection<br>resource attached to the tool.<br>**Constraints:** maxItems: 1 | Yes |  |
| type | enum | The object type, which is always 'bing_custom_search_preview'.<br>Possible values: `bing_custom_search_preview` | Yes |  |

### BingCustomSearchToolParameters

The bing custom search tool parameters.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| search_configurations | array of [BingCustomSearchConfiguration](#bingcustomsearchconfiguration) | The project connections attached to this tool. There can be a maximum of 1 connection<br>resource attached to the tool. | Yes |  |

### BingGroundingSearchConfiguration

Search configuration for Bing Grounding

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| count | integer | The number of search results to return in the bing api response | No |  |
| freshness | string | Filter search results by a specific time range. See [accepted values here](https://learn.microsoft.com/bing/search-apis/bing-web-search/reference/query-parameters). | No |  |
| market | string | The market where the results come from. | No |  |
| project_connection_id | string | Project connection id for grounding with bing search | Yes |  |
| set_lang | string | The language to use for user interface strings when calling Bing API. | No |  |

### BingGroundingSearchToolParameters

The bing grounding search tool parameters.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| search_configurations | array of [BingGroundingSearchConfiguration](#binggroundingsearchconfiguration) | The search configurations attached to this tool. There can be a maximum of 1<br>search configuration resource attached to the tool. | Yes |  |

### BingGroundingTool

The input definition information for a bing grounding search tool as used to configure an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bing_grounding | [BingGroundingSearchToolParameters](#binggroundingsearchtoolparameters) | The bing grounding search tool parameters. | Yes |  |
| └─ search_configurations | array of [BingGroundingSearchConfiguration](#binggroundingsearchconfiguration) | The search configurations attached to this tool. There can be a maximum of 1<br>search configuration resource attached to the tool.<br>**Constraints:** maxItems: 1 | Yes |  |
| type | enum | The object type, which is always 'bing_grounding'.<br>Possible values: `bing_grounding` | Yes |  |

### BlobReference

Blob reference details.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| blobUri | string | Blob URI path for client to upload data. Example: ``https://blob.windows.core.net/Container/Path`` | Yes |  |
| credential | [SasCredential](#sascredential) | SAS Credential definition | Yes |  |
| └─ sasUri | string (read-only) | SAS uri | Yes |  |
| └─ type | enum | Type of credential<br>Possible values: `SAS` | Yes |  |
| storageAccountArmId | string | ARM ID of the storage account to use. | Yes |  |

### BrowserAutomationPreviewTool

The input definition information for a Browser Automation Tool, as used to configure an Agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| browser_automation_preview | [BrowserAutomationToolParameters](#browserautomationtoolparameters) | Definition of input parameters for the Browser Automation Tool. | Yes |  |
| └─ connection | [BrowserAutomationToolConnectionParameters](#browserautomationtoolconnectionparameters) | The project connection parameters associated with the Browser Automation Tool. | Yes |  |
| type | enum | The object type, which is always 'browser_automation_preview'.<br>Possible values: `browser_automation_preview` | Yes |  |

### BrowserAutomationToolConnectionParameters

Definition of input parameters for the connection used by the Browser Automation Tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| project_connection_id | string | The ID of the project connection to your Azure Playwright resource. | Yes |  |

### BrowserAutomationToolParameters

Definition of input parameters for the Browser Automation Tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connection | [BrowserAutomationToolConnectionParameters](#browserautomationtoolconnectionparameters) | Definition of input parameters for the connection used by the Browser Automation Tool. | Yes |  |
| └─ project_connection_id | string | The ID of the project connection to your Azure Playwright resource. | Yes |  |

### CaptureStructuredOutputsTool

A tool for capturing structured outputs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| outputs | [StructuredOutputDefinition](#structuredoutputdefinition) | A structured output that can be produced by the agent. | Yes |  |
| └─ description | string | A description of the output to emit. Used by the model to determine when to emit the output. | Yes |  |
| └─ name | string | The name of the structured output. | Yes |  |
| └─ schema | object | The JSON schema for the structured output. | Yes |  |
| └─ strict | boolean (nullable) | Whether to enforce strict validation. Default `true`. | Yes |  |
| type | enum | The type of the tool. Always `capture_structured_outputs`.<br>Possible values: `capture_structured_outputs` | Yes |  |

### ChartCoordinate

Coordinates for the analysis chart.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| size | integer | Size of the chart element. | Yes |  |
| x | integer | X-axis coordinate. | Yes |  |
| y | integer | Y-axis coordinate. | Yes |  |

### ChatSummaryMemoryItem

A memory item containing a summary extracted from conversations.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string | The content of the memory. | Yes |  |
| kind | enum | The kind of the memory item.<br>Possible values: `chat_summary` | Yes |  |
| memory_id | string | The unique ID of the memory item. | Yes |  |
| scope | string | The namespace that logically groups and isolates memories, such as a user ID. | Yes |  |
| updated_at | integer | The last update time of the memory item. | Yes |  |

### ClusterInsightResult

Insights from the cluster analysis.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| clusters | array of [InsightCluster](#insightcluster) | List of clusters identified in the insights. | Yes |  |
| coordinates | object |   Optional mapping of IDs to 2D coordinates used by the UX for visualization.<br><br>  The map keys are string identifiers (for example, a cluster id or a sample id)<br>  and the values are the coordinates and visual size for rendering on a 2D chart.<br><br>  This property is omitted unless the client requests coordinates (for example,<br>  by passing `includeCoordinates=true` as a query parameter).<br><br>  Example:<br>  ```<br>  {<br>    "cluster-1": { "x": 12, "y": 34, "size": 8 },<br>    "sample-123": { "x": 18, "y": 22, "size": 4 }<br>  }<br>  ```<br><br>  Coordinates are intended only for client-side visualization and do not<br>  modify the canonical insights results. | No |  |
| summary | [InsightSummary](#insightsummary) | Summary of the error cluster analysis. | Yes |  |
| └─ method | string | Method used for clustering. | Yes |  |
| └─ sampleCount | integer | Total number of samples analyzed. | Yes |  |
| └─ uniqueClusterCount | integer | Total number of unique clusters. | Yes |  |
| └─ uniqueSubclusterCount | integer | Total number of unique subcluster labels. | Yes |  |
| └─ usage | [ClusterTokenUsage](#clustertokenusage) | Token usage while performing clustering analysis | Yes |  |

### ClusterTokenUsage

Token usage for cluster analysis

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| inputTokenUsage | integer | input token usage | Yes |  |
| outputTokenUsage | integer | output token usage | Yes |  |
| totalTokenUsage | integer | total token usage | Yes |  |

### CodeBasedEvaluatorDefinition

Code-based evaluator definition using python code

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_text | string | Inline code text for the evaluator | Yes |  |
| data_schema | object | The JSON schema (Draft 2020-12) for the evaluator's input data. This includes parameters like type, properties, required. | No |  |
| init_parameters | object | The JSON schema (Draft 2020-12) for the evaluator's input parameters. This includes parameters like type, properties, required. | No |  |
| metrics | object | List of output metrics produced by this evaluator | No |  |
| type | enum | <br>Possible values: `code` | Yes |  |

### CompletionMessageToolCallChunk

Tool call details within a message.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [FunctionToolCall](#functiontoolcall) | Details of a function tool call. | No |  |
| └─ arguments | string | The arguments to call the function with, as generated by the model in JSON format. | Yes |  |
| └─ name | string | The name of the function to call. | Yes |  |
| id | string | The Id for the tool call. | Yes |  |
| type | enum | The type of tool call, which is always "function".<br>Possible values: `function` | Yes |  |

### Connection

Response from the list and get connections operations

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| credentials | [BaseCredentials](#basecredentials) (read-only) | A base class for connection credentials | Yes |  |
| └─ type | [CredentialType](#credentialtype) (read-only) | The type of credential used by the connection | Yes |  |
| id | string (read-only) | A unique identifier for the connection, generated by the service | Yes |  |
| isDefault | boolean (read-only) | Whether the connection is tagged as the default connection of its type | Yes |  |
| metadata | object (read-only) | Metadata of the connection | Yes |  |
| name | string (read-only) | The friendly name of the connection, provided by the user. | Yes |  |
| target | string (read-only) | The connection URL to be used for this service | Yes |  |
| type | [ConnectionType](#connectiontype) (read-only) | The Type (or category) of the connection | Yes |  |

### ConnectionType

The Type (or category) of the connection

| Property | Value |
|----------|-------|
| **Description** | The Type (or category) of the connection |
| **Type** | string |
| **Values** | `AzureOpenAI`<br>`AzureBlob`<br>`AzureStorageAccount`<br>`CognitiveSearch`<br>`CosmosDB`<br>`ApiKey`<br>`AppConfig`<br>`AppInsights`<br>`CustomKeys`<br>`RemoteTool_Preview` |

### ContainerAppAgentDefinition

The container app agent definition.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container_app_resource_id | string | The resource ID of the Azure Container App that hosts this agent. Not mutable across versions. | Yes |  |
| container_protocol_versions | array of [ProtocolVersionRecord](#protocolversionrecord) | The protocols that the agent supports for ingress communication of the containers. | Yes |  |
| ingress_subdomain_suffix | string | The suffix to apply to the app subdomain when sending ingress to the agent. This can be a label (e.g., '---current'), a specific revision (e.g., '--0000001'), or empty to use the default endpoint for the container app. | Yes |  |
| kind | enum | <br>Possible values: `container_app` | Yes |  |
| rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| └─ rai_policy_name | string | The name of the RAI policy to apply. | Yes |  |

### ContainerDetails

Detailed information about the container.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| health_state | string | The health state of the container. | Yes |  |
| provisioning_error | string | The provisioning error of the container, if any. | No |  |
| provisioning_state | string | The provisioning state of the container. | Yes |  |
| replicas | array of [ContainerReplica](#containerreplica) | The list of replicas in the container. | Yes |  |
| state | string | The state of the container. | Yes |  |
| updated_on | string | The last update time of the container. | Yes |  |

### ContainerLogKind

The type of logs to stream from a container.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `console`<br>`system` |

### ContainerReplica

Information about a container replica.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container_state | string | The container state of the replica. | Yes |  |
| name | string | The name of the replica. | Yes |  |
| state | string | The state of the replica. | Yes |  |

### ContinuousEvaluationRuleAction

Evaluation rule action for continuous evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evalId | string | Eval Id to add continuous evaluation runs to. | Yes |  |
| maxHourlyRuns | integer | Maximum number of evaluation runs allowed per hour. | No |  |
| type | enum | <br>Possible values: `continuousEvaluation` | Yes |  |

### CosmosDBIndex

CosmosDB Vector Store Index Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| name | string (read-only) | The name of the resource | Yes |  |
| type | enum | Type of index<br>Possible values: `CosmosDBNoSqlVectorStore` | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### CosmosDBIndexUpdate

CosmosDB Vector Store Index Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | enum | Type of index<br>Possible values: `CosmosDBNoSqlVectorStore` | Yes |  |

### CreateAgentFromManifestRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| manifest_id | string | The manifest ID to import the agent version from. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The unique name that identifies the agent. Name can be used to retrieve/update/delete the agent.<br>- Must start and end with alphanumeric characters,<br>- Can contain hyphens in the middle<br>- Must not exceed 63 characters.<br>**Constraints:** maxLength: 63 | Yes |  |
| parameter_values | object | The inputs to the manifest that will result in a fully materialized Agent. | Yes |  |

### CreateAgentRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | [AgentDefinition](#agentdefinition) |  | Yes |  |
| └─ kind | [AgentKind](#agentkind) |  | Yes |  |
| └─ rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The unique name that identifies the agent. Name can be used to retrieve/update/delete the agent.<br>- Must start and end with alphanumeric characters,<br>- Can contain hyphens in the middle<br>- Must not exceed 63 characters.<br>**Constraints:** maxLength: 63 | Yes |  |

### CreateAgentVersionFromManifestRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| manifest_id | string | The manifest ID to import the agent version from. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| parameter_values | object | The inputs to the manifest that will result in a fully materialized Agent. | Yes |  |

### CreateAgentVersionRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | [AgentDefinition](#agentdefinition) |  | Yes |  |
| └─ kind | [AgentKind](#agentkind) |  | Yes |  |
| └─ rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |

### CreateEvalRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source_config | [OpenAI.CreateEvalCustomDataSourceConfig](#openaicreateevalcustomdatasourceconfig) or [OpenAI.CreateEvalLogsDataSourceConfig](#openaicreateevallogsdatasourceconfig) or [OpenAI.CreateEvalStoredCompletionsDataSourceConfig](#openaicreateevalstoredcompletionsdatasourceconfig) or [AzureAIDataSourceConfig](#azureaidatasourceconfig) | The configuration for the data source used for the evaluation runs. Dictates the schema of the data used in the evaluation. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the evaluation. | No |  |
| properties | object | Set of immutable 16 key-value pairs that can be attached to an object for storing additional information.<br>    Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| testing_criteria | array of [OpenAI.EvalGraderLabelModel](#openaievalgraderlabelmodel) or [OpenAI.EvalGraderStringCheck](#openaievalgraderstringcheck) or [OpenAI.EvalGraderTextSimilarity](#openaievalgradertextsimilarity) or [OpenAI.EvalGraderPython](#openaievalgraderpython) or [OpenAI.EvalGraderScoreModel](#openaievalgraderscoremodel) or [EvalGraderAzureAIEvaluator](#evalgraderazureaievaluator) | A list of graders for all eval runs in this group. Graders can reference variables in the data source using double curly braces notation, like `{{item.variable_name}}`. To reference the model's output, use the `sample` namespace (ie, `{{sample.output_text}}`). | Yes |  |

### CreateEvalRunRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source | [OpenAI.CreateEvalJsonlRunDataSource](#openaicreateevaljsonlrundatasource) or [OpenAI.CreateEvalCompletionsRunDataSource](#openaicreateevalcompletionsrundatasource) or [OpenAI.CreateEvalResponsesRunDataSource](#openaicreateevalresponsesrundatasource) or [EvalRunDataSource](#evalrundatasource) | Details about the run's data source. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the run. | No |  |
| properties | object | Set of immutable 16 key-value pairs that can be attached to an object for storing additional information.<br>    Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |

### CredentialType

The credential type used by the connection

| Property | Value |
|----------|-------|
| **Description** | The credential type used by the connection |
| **Type** | string |
| **Values** | `ApiKey`<br>`AAD`<br>`SAS`<br>`CustomKeys`<br>`None`<br>`AgenticIdentityToken_Preview` |

### CronTrigger

Cron based trigger.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| endTime | string | End time for the cron schedule in ISO 8601 format. | No |  |
| expression | string | Cron expression that defines the schedule frequency. | Yes |  |
| startTime | string | Start time for the cron schedule in ISO 8601 format. | No |  |
| timeZone | string | Time zone for the cron schedule. | No | UTC |
| type | enum | <br>Possible values: `Cron` | Yes |  |

### CustomCredential

Custom credential definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The credential type<br>Possible values: `CustomKeys` | Yes |  |

> This object also accepts additional properties of type: **string**


### DailyRecurrenceSchedule

Daily recurrence schedule.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hours | array of integer | Hours for the recurrence schedule. | Yes |  |
| type | enum | Daily recurrence type.<br>Possible values: `Daily` | Yes |  |

### DataSourceConfig

Base class for run data sources with discriminator support.


### Discriminator for DataSourceConfig

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| schema | object | The overall object JSON schema for the run data source items. | Yes |  |
| type | string | The data source type discriminator. | Yes |  |

### DatasetType

Enum to determine the type of data.

| Property | Value |
|----------|-------|
| **Description** | Enum to determine the type of data. |
| **Type** | string |
| **Values** | `uri_file`<br>`uri_folder` |

### DatasetVersion

DatasetVersion Definition


### Discriminator for DatasetVersion

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `uri_file` | [FileDatasetVersion](#filedatasetversion) |
| `uri_folder` | [FolderDatasetVersion](#folderdatasetversion) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionName | string | The Azure Storage Account connection name. Required if startPendingUploadVersion was not called before creating the Dataset | No |  |
| dataUri | string | URI of the data ([example](https://go.microsoft.com/fwlink/?linkid=2202330))<br>**Constraints:** minLength: 1, pattern: `[a-zA-Z0-9_]` | Yes |  |
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| isReference | boolean (read-only) | Indicates if the dataset holds a reference to the storage, or the dataset manages storage itself. If true, the underlying data will not be deleted when the dataset version is deleted | No |  |
| name | string (read-only) | The name of the resource | Yes |  |
| type | [DatasetType](#datasettype) | Enum to determine the type of data. | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### DatasetVersionUpdate

DatasetVersion Definition


### Discriminator for DatasetVersionUpdate

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `uri_file` | [FileDatasetVersionUpdate](#filedatasetversionupdate) |
| `uri_folder` | [FolderDatasetVersionUpdate](#folderdatasetversionupdate) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | [DatasetType](#datasettype) | Enum to determine the type of data. | Yes |  |

### DayOfWeek

Days of the week for recurrence schedule.

| Property | Value |
|----------|-------|
| **Description** | Days of the week for recurrence schedule. |
| **Type** | string |
| **Values** | `Sunday`<br>`Monday`<br>`Tuesday`<br>`Wednesday`<br>`Thursday`<br>`Friday`<br>`Saturday` |

### DeleteAgentResponse

A deleted agent Object

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | Whether the agent was successfully deleted. | Yes |  |
| name | string | The name of the agent. | Yes |  |
| object | enum | The object type. Always 'agent.deleted'.<br>Possible values: `agent.deleted` | Yes |  |

### DeleteAgentVersionResponse

A deleted agent version Object

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | Whether the agent was successfully deleted. | Yes |  |
| name | string | The name of the agent. | Yes |  |
| object | enum | The object type. Always 'agent.version.deleted'.<br>Possible values: `agent.version.deleted` | Yes |  |
| version | string | The version identifier of the agent. | Yes |  |

### DeleteEvalResponse

A deleted evaluation Object

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | Whether the eval was successfully deleted. | Yes |  |
| eval_id | string | id of the eval. | Yes |  |
| object | enum | The object type. Always 'eval.deleted'.<br>Possible values: `eval.deleted` | Yes |  |

### DeleteEvalRunResponse

A deleted evaluation run Object.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | Whether the eval was successfully deleted. | No |  |
| object | enum | The object type. Always 'eval.deleted'.<br>Possible values: `eval.deleted` | No |  |
| run_id | string | id of the eval. | No |  |

### DeleteMemoryStoreResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | Whether the memory store was successfully deleted. | Yes |  |
| name | string | The name of the memory store. | Yes |  |
| object | enum | The object type. Always 'memory_store.deleted'.<br>Possible values: `memory_store.deleted` | Yes |  |

### DeleteResponseResult

The result of a delete response operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | enum | Always return true<br>Possible values: `True` | Yes |  |
| id | string | The operation ID. | Yes |  |
| object | enum | Always return 'response'.<br>Possible values: `response` | Yes |  |

### Deployment

Model Deployment Definition


### Discriminator for Deployment

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `ModelDeployment` | [ModelDeployment](#modeldeployment) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string (read-only) | Name of the deployment | Yes |  |
| type | [DeploymentType](#deploymenttype) |  | Yes |  |

### DeploymentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `ModelDeployment` |

### EntraIDCredentials

Entra ID credential definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The credential type<br>Possible values: `AAD` | Yes |  |

### Eval

An Eval object with a data source config and testing criteria.
An Eval represents a task to be done for your LLM integration.
Like:
- Improve the quality of my chatbot
- See how well my chatbot handles customer support
- Check if o4-mini is better at my usecase than gpt-4o

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the eval was created. | Yes |  |
| created_by | string | the name of the person who created the run. | No |  |
| data_source_config | [OpenAI.CreateEvalCustomDataSourceConfig](#openaicreateevalcustomdatasourceconfig) or [OpenAI.CreateEvalLogsDataSourceConfig](#openaicreateevallogsdatasourceconfig) or [OpenAI.CreateEvalStoredCompletionsDataSourceConfig](#openaicreateevalstoredcompletionsdatasourceconfig) or [AzureAIDataSourceConfig](#azureaidatasourceconfig) | Configuration of data sources used in runs of the evaluation. | Yes |  |
| id | string | Unique identifier for the evaluation. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| modified_at | [integer](#integer) |  | No |  |
| name | string | The name of the evaluation. | Yes |  |
| object | enum | The object type.<br>Possible values: `eval` | Yes |  |
| properties | object | Set of immutable 16 key-value pairs that can be attached to an object for storing additional information.<br>    Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| testing_criteria | array of [OpenAI.EvalGraderLabelModel](#openaievalgraderlabelmodel) or [OpenAI.EvalGraderStringCheck](#openaievalgraderstringcheck) or [OpenAI.EvalGraderTextSimilarity](#openaievalgradertextsimilarity) or [OpenAI.EvalGraderPython](#openaievalgraderpython) or [OpenAI.EvalGraderScoreModel](#openaievalgraderscoremodel) or [EvalGraderAzureAIEvaluator](#evalgraderazureaievaluator) | A list of testing criteria. | Yes |  |

### EvalCsvFileIdSource

Represents a reference to an uploaded CSV file used as a source for evaluation data.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The identifier of the uploaded CSV file. | Yes |  |
| type | enum | The type of source, always `file_id`.<br>Possible values: `file_id` | Yes |  |

### EvalCsvRunDataSource

Represents a CSV data source for evaluation runs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| source | [EvalCsvFileIdSource](#evalcsvfileidsource) | Represents a reference to an uploaded CSV file used as a source for evaluation data. | Yes |  |
| └─ id | string | The identifier of the uploaded CSV file. | Yes |  |
| └─ type | enum | The type of source, always `file_id`.<br>Possible values: `file_id` | Yes |  |
| type | enum | The type of data source, always `csv`.<br>Possible values: `csv` | Yes |  |

### EvalGraderAzureAIEvaluator

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_mapping | object | The model to use for the evaluation. Must support structured outputs. | No |  |
| evaluator_name | string | The name of the evaluator. | Yes |  |
| evaluator_version | string | The version of the evaluator. Latest version if not specified. | No |  |
| initialization_parameters | object | The initialization parameters for the evaluation. Must support structured outputs. | No |  |
| name | string | The name of the grader. | Yes |  |
| type | enum | The object type, which is always `azure_ai_evaluator`.<br>Possible values: `azure_ai_evaluator` | Yes |  |

### EvalResult

Result of the evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | name of the check | Yes |  |
| passed | boolean | indicates if the check passed or failed | Yes |  |
| score | number | score | Yes |  |
| type | string | type of the check | Yes |  |

### EvalRun

A schema representing an evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | Unix timestamp (in seconds) when the evaluation run was created. | Yes |  |
| created_by | string | the name of the person who created the run. | No |  |
| data_source | [OpenAI.CreateEvalJsonlRunDataSource](#openaicreateevaljsonlrundatasource) or [OpenAI.CreateEvalCompletionsRunDataSource](#openaicreateevalcompletionsrundatasource) or [OpenAI.CreateEvalResponsesRunDataSource](#openaicreateevalresponsesrundatasource) or [EvalRunDataSource](#evalrundatasource) | Information about the run's data source. | Yes |  |
| error | [OpenAI.EvalApiError](#openaievalapierror) | An object representing an error response from the Eval API. | Yes |  |
| eval_id | string | The identifier of the associated evaluation. | Yes |  |
| id | string | Unique identifier for the evaluation run. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| model | string | The model that is evaluated, if applicable. | Yes |  |
| modified_at | [integer](#integer) |  | No |  |
| name | string | The name of the evaluation run. | Yes |  |
| object | enum | The type of the object. Always "eval.run".<br>Possible values: `eval.run` | Yes |  |
| per_model_usage | array of [OpenAI.EvalRunPerModelUsage](#openaievalrunpermodelusage) | Usage statistics for each model during the evaluation run. | Yes |  |
| per_testing_criteria_results | array of [OpenAI.EvalRunPerTestingCriteriaResults](#openaievalrunpertestingcriteriaresults) | Results per testing criteria applied during the evaluation run. | Yes |  |
| properties | object | Set of immutable 16 key-value pairs that can be attached to an object for storing additional information.<br>    Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| report_url | string | The URL to the rendered evaluation run report on the UI dashboard. | Yes |  |
| result_counts | [OpenAI.EvalRunResultCounts](#openaievalrunresultcounts) |  | Yes |  |
| └─ errored | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| └─ failed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| └─ passed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| └─ total | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| status | string | The status of the evaluation run. | Yes |  |

### EvalRunDataSource

Base class for run data sources with discriminator support.


### Discriminator for EvalRunDataSource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `azure_ai_traces_preview` | [TracesPreviewEvalRunDataSource](#tracespreviewevalrundatasource) |
| `azure_ai_synthetic_data_gen_preview` | [SyntheticDataGenerationPreviewEvalRunDataSource](#syntheticdatagenerationpreviewevalrundatasource) |
| `azure_ai_responses` | [AzureAIResponsesEvalRunDataSource](#azureairesponsesevalrundatasource) |
| `azure_ai_target_completions` | [TargetCompletionEvalRunDataSource](#targetcompletionevalrundatasource) |
| `csv` | [EvalCsvRunDataSource](#evalcsvrundatasource) |
| `azure_ai_red_team` | [RedTeamEvalRunDataSource](#redteamevalrundatasource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | string | The data source type discriminator. | Yes |  |

### EvalRunOutputItem

A schema representing an evaluation run output item.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | Unix timestamp (in seconds) when the evaluation run was created. | Yes |  |
| datasource_item | object | Details of the input data source item. | Yes |  |
| datasource_item_id | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| eval_id | string | The identifier of the evaluation group. | Yes |  |
| id | string | Unique identifier for the evaluation run output item. | Yes |  |
| object | enum | The type of the object. Always "eval.run.output_item".<br>Possible values: `eval.run.output_item` | Yes |  |
| results | array of [EvalRunOutputItemResult](#evalrunoutputitemresult) | A list of grader results for this output item. | Yes |  |
| run_id | string | The identifier of the evaluation run associated with this output item. | Yes |  |
| sample | [OpenAI.EvalRunOutputItemSample](#openaievalrunoutputitemsample) |  | Yes |  |
| └─ error | [OpenAI.EvalApiError](#openaievalapierror) | An object representing an error response from the Eval API. | Yes |  |
| └─ finish_reason | string |  | Yes |  |
| └─ input | array of [EvalRunOutputItemSampleInput](#evalrunoutputitemsampleinput) |  | Yes |  |
| └─ max_completion_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| └─ model | string |  | Yes |  |
| └─ output | array of [EvalRunOutputItemSampleOutput](#evalrunoutputitemsampleoutput) |  | Yes |  |
| └─ seed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| └─ usage | [OpenAI.EvalRunOutputItemSampleUsage](#openaievalrunoutputitemsampleusage) |  | Yes |  |
| status | string | The status of the evaluation run. | Yes |  |

### EvalRunOutputItemResult

A single grader result for an evaluation run output item.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| label | string | The label associated with the test criteria metric (e.g., "pass", "fail", "good", "bad"). | No |  |
| metric | string | The name of the metric (e.g., "fluency", "f1_score"). | No |  |
| name | string | The name of the grader. | Yes |  |
| passed | boolean | Whether the grader considered the output a pass. | Yes |  |
| properties | object | Additional details about the test criteria metric. | No |  |
| reason | string | The reason for the test criteria metric. | No |  |
| sample | object (nullable) | Optional sample or intermediate data produced by the grader. | No |  |
| score | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| threshold | number | The threshold used to determine pass/fail for this test criteria, if it is numerical. | No |  |
| type | string | The grader type (for example, "string-check-grader"). | No |  |

> This object also accepts additional properties.


### EvalRunOutputItemSampleInput

A message in the evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string |  | Yes |  |
| role | string |  | Yes |  |
| tool_calls | array of [CompletionMessageToolCallChunk](#completionmessagetoolcallchunk) | Tool calls made within the message, if any. | Yes |  |

### EvalRunOutputItemSampleOutput

A message in the evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string |  | No |  |
| role | string |  | No |  |
| tool_calls | array of [CompletionMessageToolCallChunk](#completionmessagetoolcallchunk) | Tool calls made within the message, if any. | Yes |  |

### EvalRunResultCompareItem

Metric comparison for a treatment against the baseline.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deltaEstimate | number | Estimated difference between treatment and baseline. | Yes |  |
| pValue | number | P-value for the treatment effect. | Yes |  |
| treatmentEffect | [TreatmentEffectType](#treatmenteffecttype) | Treatment Effect Type. | Yes |  |
| treatmentRunId | string | The treatment run ID. | Yes |  |
| treatmentRunSummary | [EvalRunResultSummary](#evalrunresultsummary) | Summary statistics of a metric in an evaluation run. | Yes |  |
| └─ average | number | Average value of the metric in the evaluation run. | Yes |  |
| └─ runId | string | The evaluation run ID. | Yes |  |
| └─ sampleCount | integer | Number of samples in the evaluation run. | Yes |  |
| └─ standardDeviation | number | Standard deviation of the metric in the evaluation run. | Yes |  |

### EvalRunResultComparison

Comparison results for treatment runs against the baseline.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| baselineRunSummary | [EvalRunResultSummary](#evalrunresultsummary) | Summary statistics of a metric in an evaluation run. | Yes |  |
| └─ average | number | Average value of the metric in the evaluation run. | Yes |  |
| └─ runId | string | The evaluation run ID. | Yes |  |
| └─ sampleCount | integer | Number of samples in the evaluation run. | Yes |  |
| └─ standardDeviation | number | Standard deviation of the metric in the evaluation run. | Yes |  |
| compareItems | array of [EvalRunResultCompareItem](#evalrunresultcompareitem) | List of comparison results for each treatment run. | Yes |  |
| evaluator | string | Name of the evaluator for this testing criteria. | Yes |  |
| metric | string | Metric being evaluated. | Yes |  |
| testingCriteria | string | Name of the testing criteria. | Yes |  |

### EvalRunResultSummary

Summary statistics of a metric in an evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| average | number | Average value of the metric in the evaluation run. | Yes |  |
| runId | string | The evaluation run ID. | Yes |  |
| sampleCount | integer | Number of samples in the evaluation run. | Yes |  |
| standardDeviation | number | Standard deviation of the metric in the evaluation run. | Yes |  |

### EvaluationComparisonInsightRequest

Evaluation Comparison Request

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| baselineRunId | string | The baseline run ID for comparison. | Yes |  |
| evalId | string | Identifier for the evaluation. | Yes |  |
| treatmentRunIds | array of string | List of treatment run IDs for comparison. | Yes |  |
| type | enum | The type of request.<br>Possible values: `EvaluationComparison` | Yes |  |

### EvaluationComparisonInsightResult

Insights from the evaluation comparison.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| comparisons | array of [EvalRunResultComparison](#evalrunresultcomparison) | Comparison results for each treatment run against the baseline. | Yes |  |
| method | string | The statistical method used for comparison. | Yes |  |
| type | enum | The type of insights result.<br>Possible values: `EvaluationComparison` | Yes |  |

### EvaluationResultSample

A sample from the evaluation result.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| correlationInfo | object | Info about the correlation for the analysis sample. | Yes |  |
| evaluationResult | [EvalResult](#evalresult) | Result of the evaluation. | Yes |  |
| └─ name | string | name of the check | Yes |  |
| └─ passed | boolean | indicates if the check passed or failed | Yes |  |
| └─ score | number | score | Yes |  |
| └─ type | string | type of the check | Yes |  |
| features | object | Features to help with additional filtering of data in UX. | Yes |  |
| id | string | The unique identifier for the analysis sample. | Yes |  |
| type | enum | Evaluation Result Sample Type<br>Possible values: `EvaluationResultSample` | Yes |  |

### EvaluationRule

Evaluation rule model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [EvaluationRuleAction](#evaluationruleaction) | Evaluation action model. | Yes |  |
| └─ type | [EvaluationRuleActionType](#evaluationruleactiontype) | Type of the evaluation action. | Yes |  |
| description | string | Description for the evaluation rule. | No |  |
| displayName | string | Display Name for the evaluation rule. | No |  |
| enabled | boolean | Indicates whether the evaluation rule is enabled. Default is true. | Yes |  |
| eventType | [EvaluationRuleEventType](#evaluationruleeventtype) | Type of the evaluation rule event. | Yes |  |
| filter | [EvaluationRuleFilter](#evaluationrulefilter) | Evaluation filter model. | No |  |
| └─ agentName | string | Filter by agent name. | Yes |  |
| id | string (read-only) | Unique identifier for the evaluation rule. | Yes |  |
| systemData | object (read-only) | System metadata for the evaluation rule. | Yes |  |

### EvaluationRuleAction

Evaluation action model.


### Discriminator for EvaluationRuleAction

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `continuousEvaluation` | [ContinuousEvaluationRuleAction](#continuousevaluationruleaction) |
| `humanEvaluationPreview` | [HumanEvaluationPreviewRuleAction](#humanevaluationpreviewruleaction) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [EvaluationRuleActionType](#evaluationruleactiontype) | Type of the evaluation action. | Yes |  |

### EvaluationRuleActionType

Type of the evaluation action.

| Property | Value |
|----------|-------|
| **Description** | Type of the evaluation action. |
| **Type** | string |
| **Values** | `continuousEvaluation`<br>`humanEvaluationPreview` |

### EvaluationRuleEventType

Type of the evaluation rule event.

| Property | Value |
|----------|-------|
| **Description** | Type of the evaluation rule event. |
| **Type** | string |
| **Values** | `responseCompleted`<br>`manual` |

### EvaluationRuleFilter

Evaluation filter model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agentName | string | Filter by agent name. | Yes |  |

### EvaluationRunClusterInsightRequest

Insights on set of Evaluation Results

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evalId | string | Evaluation Id for the insights. | Yes |  |
| modelConfiguration | [InsightModelConfiguration](#insightmodelconfiguration) | Configuration of the model used in the insight generation. | No |  |
| └─ modelDeploymentName | string | The model deployment to be evaluated. Accepts either the deployment name alone or with the connection name as `{connectionName}/<modelDeploymentName>`. | Yes |  |
| runIds | array of string | List of evaluation run IDs for the insights. | Yes |  |
| type | enum | The type of insights request.<br>Possible values: `EvaluationRunClusterInsight` | Yes |  |

### EvaluationRunClusterInsightResult

Insights from the evaluation run cluster analysis.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| clusterInsight | [ClusterInsightResult](#clusterinsightresult) | Insights from the cluster analysis. | Yes |  |
| type | enum | The type of insights result.<br>Possible values: `EvaluationRunClusterInsight` | Yes |  |

### EvaluationScheduleTask

Evaluation task for the schedule.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| configuration | object | Configuration for the task. | No |  |
| evalId | string | Identifier of the evaluation group. | Yes |  |
| evalRun | object | The evaluation run payload. | Yes |  |
| type | enum | <br>Possible values: `Evaluation` | Yes |  |

### EvaluationTaxonomy

Evaluation Taxonomy Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| name | string (read-only) | The name of the resource | Yes |  |
| properties | object | Additional properties for the evaluation taxonomy. | No |  |
| taxonomyCategories | array of [TaxonomyCategory](#taxonomycategory) | List of taxonomy categories. | No |  |
| taxonomyInput | [EvaluationTaxonomyInput](#evaluationtaxonomyinput) | Input configuration for the evaluation taxonomy. | Yes |  |
| └─ type | [EvaluationTaxonomyInputType](#evaluationtaxonomyinputtype) | Input type of the evaluation taxonomy. | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### EvaluationTaxonomyCreateOrUpdate

Evaluation Taxonomy Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| properties | object | Additional properties for the evaluation taxonomy. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| taxonomyCategories | array of [TaxonomyCategory](#taxonomycategory) | List of taxonomy categories. | No |  |
| taxonomyInput | [EvaluationTaxonomyInput](#evaluationtaxonomyinput) | Input configuration for the evaluation taxonomy. | Yes |  |
| └─ type | [EvaluationTaxonomyInputType](#evaluationtaxonomyinputtype) | Input type of the evaluation taxonomy. | Yes |  |

### EvaluationTaxonomyInput

Input configuration for the evaluation taxonomy.


### Discriminator for EvaluationTaxonomyInput

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `agent` | [AgentTaxonomyInput](#agenttaxonomyinput) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [EvaluationTaxonomyInputType](#evaluationtaxonomyinputtype) | Type of the evaluation taxonomy input. | Yes |  |

### EvaluationTaxonomyInputType

Type of the evaluation taxonomy input.

| Property | Value |
|----------|-------|
| **Description** | Type of the evaluation taxonomy input. |
| **Type** | string |
| **Values** | `agent`<br>`policy` |

### EvaluationTaxonomyInputUpdate

Input configuration for the evaluation taxonomy.


### Discriminator for EvaluationTaxonomyInputUpdate

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `agent` | [AgentTaxonomyInputUpdate](#agenttaxonomyinputupdate) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [EvaluationTaxonomyInputType](#evaluationtaxonomyinputtype) | Type of the evaluation taxonomy input. | Yes |  |

### EvaluationTaxonomyUpdate

Evaluation Taxonomy Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| properties | object | Additional properties for the evaluation taxonomy. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| taxonomyCategories | array of [TaxonomyCategory](#taxonomycategory) | List of taxonomy categories. | No |  |
| taxonomyInput | [EvaluationTaxonomyInputUpdate](#evaluationtaxonomyinputupdate) | Input configuration for the evaluation taxonomy. | No |  |
| └─ type | [EvaluationTaxonomyInputType](#evaluationtaxonomyinputtype) | Input type of the evaluation taxonomy. | Yes |  |

### EvaluatorCategory

The category of the evaluator

| Property | Value |
|----------|-------|
| **Description** | The category of the evaluator |
| **Type** | string |
| **Values** | `quality`<br>`safety`<br>`agents` |

### EvaluatorDefinition

Base evaluator configuration with discriminator


### Discriminator for EvaluatorDefinition

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `code` | [CodeBasedEvaluatorDefinition](#codebasedevaluatordefinition) |
| `prompt` | [PromptBasedEvaluatorDefinition](#promptbasedevaluatordefinition) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_schema | object | The JSON schema (Draft 2020-12) for the evaluator's input data. This includes parameters like type, properties, required. | No |  |
| init_parameters | object | The JSON schema (Draft 2020-12) for the evaluator's input parameters. This includes parameters like type, properties, required. | No |  |
| metrics | object | List of output metrics produced by this evaluator | No |  |
| type | [EvaluatorDefinitionType](#evaluatordefinitiontype) | The type of evaluator definition | Yes |  |

### EvaluatorDefinitionType

The type of evaluator definition

| Property | Value |
|----------|-------|
| **Description** | The type of evaluator definition |
| **Type** | string |
| **Values** | `prompt`<br>`code`<br>`prompt_and_code`<br>`service`<br>`openai_graders` |

### EvaluatorMetric

Evaluator Metric

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| desirable_direction | [EvaluatorMetricDirection](#evaluatormetricdirection) | The direction of the metric indicating whether a higher value is better, a lower value is better, or neutral | No |  |
| is_primary | boolean | Indicates if this metric is primary when there are multiple metrics. | No |  |
| max_value | number | Maximum value for the metric. If not specified, it is assumed to be unbounded. | No |  |
| min_value | number | Minimum value for the metric | No |  |
| type | [EvaluatorMetricType](#evaluatormetrictype) | The type of the evaluator | No |  |

### EvaluatorMetricDirection

The direction of the metric indicating whether a higher value is better, a lower value is better, or neutral

| Property | Value |
|----------|-------|
| **Description** | The direction of the metric indicating whether a higher value is better, a lower value is better, or neutral |
| **Type** | string |
| **Values** | `increase`<br>`decrease`<br>`neutral` |

### EvaluatorMetricType

The type of the evaluator

| Property | Value |
|----------|-------|
| **Description** | The type of the evaluator |
| **Type** | string |
| **Values** | `ordinal`<br>`continuous`<br>`boolean` |

### EvaluatorType

The type of the evaluator

| Property | Value |
|----------|-------|
| **Description** | The type of the evaluator |
| **Type** | string |
| **Values** | `builtin`<br>`custom` |

### EvaluatorVersion

Evaluator Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| categories | array of [EvaluatorCategory](#evaluatorcategory) | The categories of the evaluator | Yes |  |
| created_at | string (read-only) | Creation date/time of the evaluator | Yes |  |
| created_by | string (read-only) | Creator of the evaluator | Yes |  |
| definition | [EvaluatorDefinition](#evaluatordefinition) | Base evaluator configuration with discriminator | Yes |  |
| └─ data_schema | object | The JSON schema (Draft 2020-12) for the evaluator's input data. This includes parameters like type, properties, required. | No |  |
| └─ init_parameters | object | The JSON schema (Draft 2020-12) for the evaluator's input parameters. This includes parameters like type, properties, required. | No |  |
| └─ metrics | object | List of output metrics produced by this evaluator | No |  |
| └─ type | [EvaluatorDefinitionType](#evaluatordefinitiontype) | The type of evaluator definition | Yes |  |
| display_name | string | Display Name for evaluator. It helps to find the evaluator easily in AI Foundry. It does not need to be unique. | No |  |
| evaluator_type | [EvaluatorType](#evaluatortype) | The type of the evaluator | Yes |  |
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| metadata | object | Metadata about the evaluator | No |  |
| modified_at | string (read-only) | Last modified date/time of the evaluator | Yes |  |
| name | string (read-only) | The name of the resource | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### EvaluatorVersionCreate

Evaluator Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| categories | array of [EvaluatorCategory](#evaluatorcategory) | The categories of the evaluator | Yes |  |
| definition | [EvaluatorDefinition](#evaluatordefinition) | Base evaluator configuration with discriminator | Yes |  |
| └─ data_schema | object | The JSON schema (Draft 2020-12) for the evaluator's input data. This includes parameters like type, properties, required. | No |  |
| └─ init_parameters | object | The JSON schema (Draft 2020-12) for the evaluator's input parameters. This includes parameters like type, properties, required. | No |  |
| └─ metrics | object | List of output metrics produced by this evaluator | No |  |
| └─ type | [EvaluatorDefinitionType](#evaluatordefinitiontype) | The type of evaluator definition | Yes |  |
| description | string | The asset description text. | No |  |
| display_name | string | Display Name for evaluator. It helps to find the evaluator easily in AI Foundry. It does not need to be unique. | No |  |
| evaluator_type | [EvaluatorType](#evaluatortype) | The type of the evaluator | Yes |  |
| metadata | object | Metadata about the evaluator | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |

### EvaluatorVersionUpdate

Evaluator Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| categories | array of [EvaluatorCategory](#evaluatorcategory) | The categories of the evaluator | No |  |
| description | string | The asset description text. | No |  |
| display_name | string | Display Name for evaluator. It helps to find the evaluator easily in AI Foundry. It does not need to be unique. | No |  |
| metadata | object | Metadata about the evaluator | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |

### FabricDataAgentToolParameters

The fabric data agent tool parameters.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| project_connections | array of [ToolProjectConnection](#toolprojectconnection) | The project connections attached to this tool. There can be a maximum of 1 connection<br>resource attached to the tool. | No |  |

### FileDatasetVersion

FileDatasetVersion Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionName | string | The Azure Storage Account connection name. Required if startPendingUploadVersion was not called before creating the Dataset | No |  |
| dataUri | string | URI of the data ([example](https://go.microsoft.com/fwlink/?linkid=2202330))<br>**Constraints:** minLength: 1, pattern: `[a-zA-Z0-9_]` | Yes |  |
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| isReference | boolean (read-only) | Indicates if the dataset holds a reference to the storage, or the dataset manages storage itself. If true, the underlying data will not be deleted when the dataset version is deleted | No |  |
| name | string (read-only) | The name of the resource | Yes |  |
| type | enum | Dataset type<br>Possible values: `uri_file` | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### FileDatasetVersionUpdate

FileDatasetVersion Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | enum | Dataset type<br>Possible values: `uri_file` | Yes |  |

### FolderDatasetVersion

FileDatasetVersion Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionName | string | The Azure Storage Account connection name. Required if startPendingUploadVersion was not called before creating the Dataset | No |  |
| dataUri | string | URI of the data ([example](https://go.microsoft.com/fwlink/?linkid=2202330))<br>**Constraints:** minLength: 1, pattern: `[a-zA-Z0-9_]` | Yes |  |
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| isReference | boolean (read-only) | Indicates if the dataset holds a reference to the storage, or the dataset manages storage itself. If true, the underlying data will not be deleted when the dataset version is deleted | No |  |
| name | string (read-only) | The name of the resource | Yes |  |
| type | enum | Dataset type<br>Possible values: `uri_folder` | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### FolderDatasetVersionUpdate

FileDatasetVersion Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | enum | Dataset type<br>Possible values: `uri_folder` | Yes |  |

### FunctionToolCall

Details of a function tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | The arguments to call the function with, as generated by the model in JSON format. | Yes |  |
| name | string | The name of the function to call. | Yes |  |

### HostedAgentDefinition

The hosted agent definition.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container_protocol_versions | array of [ProtocolVersionRecord](#protocolversionrecord) | The protocols that the agent supports for ingress communication of the containers. | Yes |  |
| cpu | string | The CPU configuration for the hosted agent. | Yes |  |
| environment_variables | object | Environment variables to set in the hosted agent container. | No |  |
| image | string | The image ID for the agent, applicable to image-based hosted agents. | No |  |
| kind | enum | <br>Possible values: `hosted` | Yes |  |
| memory | string | The memory configuration for the hosted agent. | Yes |  |
| rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| └─ rai_policy_name | string | The name of the RAI policy to apply. | Yes |  |
| tools | array of [OpenAI.Tool](#openaitool) | An array of tools the hosted agent's model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter. | No |  |

### HourlyRecurrenceSchedule

Hourly recurrence schedule.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `Hourly` | Yes |  |

### HumanEvaluationPreviewRuleAction

Evaluation rule action for human evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| templateId | [AssetId](#assetid) | Identifier of a saved asset. | Yes |  |
| type | enum | <br>Possible values: `humanEvaluationPreview` | Yes |  |

### Index

Index resource Definition


### Discriminator for Index

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `AzureSearch` | [AzureAISearchIndex](#azureaisearchindex) |
| `ManagedAzureSearch` | [ManagedAzureAISearchIndex](#managedazureaisearchindex) |
| `CosmosDBNoSqlVectorStore` | [CosmosDBIndex](#cosmosdbindex) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| name | string (read-only) | The name of the resource | Yes |  |
| type | [IndexType](#indextype) |  | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### IndexType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `AzureSearch`<br>`CosmosDBNoSqlVectorStore`<br>`ManagedAzureSearch` |

### IndexUpdate

Index resource Definition


### Discriminator for IndexUpdate

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `AzureSearch` | [AzureAISearchIndexUpdate](#azureaisearchindexupdate) |
| `ManagedAzureSearch` | [ManagedAzureAISearchIndexUpdate](#managedazureaisearchindexupdate) |
| `CosmosDBNoSqlVectorStore` | [CosmosDBIndexUpdate](#cosmosdbindexupdate) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | [IndexType](#indextype) |  | Yes |  |

### Insight

The response body for cluster insights.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| displayName | string | User friendly display name for the insight. | Yes |  |
| id | string (read-only) | The unique identifier for the insights report. | Yes |  |
| metadata | [InsightsMetadata](#insightsmetadata) (read-only) | Metadata about the insights. | Yes |  |
| └─ completedAt | string | The timestamp when the insights were completed. | No |  |
| └─ createdAt | string | The timestamp when the insights were created. | Yes |  |
| request | [InsightRequest](#insightrequest) | The request of the insights report. | Yes |  |
| └─ type | [InsightType](#insighttype) | The type of request. | Yes |  |
| result | [InsightResult](#insightresult) (read-only) | The result of the insights. | No |  |
| └─ type | [InsightType](#insighttype) | The type of insights result. | Yes |  |
| state | [Azure.Core.Foundations.OperationState](#azurecorefoundationsoperationstate) (read-only) | Enum describing allowed operation states. | Yes |  |

### InsightCluster

A cluster of analysis samples.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | Description of the analysis cluster. | Yes |  |
| id | string | The id of the analysis cluster. | Yes |  |
| label | string | Label for the cluster | Yes |  |
| samples | array of [InsightSample](#insightsample) | List of samples that belong to this cluster. Empty if samples are part of subclusters. | No |  |
| subClusters | array of [InsightCluster](#insightcluster) | List of subclusters within this cluster. Empty if no subclusters exist. | No |  |
| suggestion | string | Suggestion for the cluster | Yes |  |
| suggestionTitle | string | The title of the suggestion for the cluster | Yes |  |
| weight | integer | The weight of the analysis cluster. This indicate number of samples in the cluster. | Yes |  |

### InsightModelConfiguration

Configuration of the model used in the insight generation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| modelDeploymentName | string | The model deployment to be evaluated. Accepts either the deployment name alone or with the connection name as `{connectionName}/<modelDeploymentName>`. | Yes |  |

### InsightRequest

The request of the insights report.


### Discriminator for InsightRequest

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `EvaluationRunClusterInsight` | [EvaluationRunClusterInsightRequest](#evaluationrunclusterinsightrequest) |
| `AgentClusterInsight` | [AgentClusterInsightRequest](#agentclusterinsightrequest) |
| `EvaluationComparison` | [EvaluationComparisonInsightRequest](#evaluationcomparisoninsightrequest) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [InsightType](#insighttype) | The request of the insights. | Yes |  |

### InsightResult

The result of the insights.


### Discriminator for InsightResult

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `EvaluationComparison` | [EvaluationComparisonInsightResult](#evaluationcomparisoninsightresult) |
| `EvaluationRunClusterInsight` | [EvaluationRunClusterInsightResult](#evaluationrunclusterinsightresult) |
| `AgentClusterInsight` | [AgentClusterInsightResult](#agentclusterinsightresult) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [InsightType](#insighttype) | The request of the insights. | Yes |  |

### InsightSample

A sample from the analysis.


### Discriminator for InsightSample

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `EvaluationResultSample` | [EvaluationResultSample](#evaluationresultsample) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| correlationInfo | object | Info about the correlation for the analysis sample. | Yes |  |
| features | object | Features to help with additional filtering of data in UX. | Yes |  |
| id | string | The unique identifier for the analysis sample. | Yes |  |
| type | [SampleType](#sampletype) | The type of sample used in the analysis. | Yes |  |

### InsightScheduleTask

Insight task for the schedule.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| configuration | object | Configuration for the task. | No |  |
| insight | [Insight](#insight) | The response body for cluster insights. | Yes |  |
| └─ displayName | string | User friendly display name for the insight. | Yes |  |
| └─ id | string (read-only) | The unique identifier for the insights report. | Yes |  |
| └─ metadata | [InsightsMetadata](#insightsmetadata) (read-only) | Metadata about the insights report. | Yes |  |
| └─ request | [InsightRequest](#insightrequest) | Request for the insights analysis. | Yes |  |
| └─ result | [InsightResult](#insightresult) (read-only) | The result of the insights report. | No |  |
| └─ state | [Azure.Core.Foundations.OperationState](#azurecorefoundationsoperationstate) (read-only) | The current state of the insights. | Yes |  |
| type | enum | <br>Possible values: `Insight` | Yes |  |

### InsightSummary

Summary of the error cluster analysis.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| method | string | Method used for clustering. | Yes |  |
| sampleCount | integer | Total number of samples analyzed. | Yes |  |
| uniqueClusterCount | integer | Total number of unique clusters. | Yes |  |
| uniqueSubclusterCount | integer | Total number of unique subcluster labels. | Yes |  |
| usage | [ClusterTokenUsage](#clustertokenusage) | Token usage for cluster analysis | Yes |  |
| └─ inputTokenUsage | integer | input token usage | Yes |  |
| └─ outputTokenUsage | integer | output token usage | Yes |  |
| └─ totalTokenUsage | integer | total token usage | Yes |  |

### InsightType

The request of the insights.

| Property | Value |
|----------|-------|
| **Description** | The request of the insights. |
| **Type** | string |
| **Values** | `EvaluationRunClusterInsight`<br>`AgentClusterInsight`<br>`EvaluationComparison` |

### InsightsMetadata

Metadata about the insights.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completedAt | string | The timestamp when the insights were completed. | No |  |
| createdAt | string | The timestamp when the insights were created. | Yes |  |

### ItemGenerationParams

Represents the set of parameters used to control item generation operations.


### Discriminator for ItemGenerationParams

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `red_team` | [RedTeamItemGenerationParams](#redteamitemgenerationparams) |
| `red_team_seed_prompts` | [RedTeamSeedPromptsItemGenerationParams](#redteamseedpromptsitemgenerationparams) |
| `red_team_taxonomy` | [RedTeamTaxonomyItemGenerationParams](#redteamtaxonomyitemgenerationparams) |
| `response_retrieval` | [ResponseRetrievalItemGenerationParams](#responseretrievalitemgenerationparams) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [ItemGenerationParamsType](#itemgenerationparamstype) | The types of parameters for red team item generation. | Yes |  |

### ItemGenerationParamsType

The types of parameters for red team item generation.

| Property | Value |
|----------|-------|
| **Description** | The types of parameters for red team item generation. |
| **Type** | string |
| **Values** | `red_team`<br>`response_retrieval`<br>`red_team_seed_prompts`<br>`red_team_taxonomy`<br>`synthetic_data_gen_preview` |

### ManagedAzureAISearchIndex

Managed Azure AI Search Index Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string (read-only) | Asset ID, a unique identifier for the asset | No |  |
| name | string (read-only) | The name of the resource | Yes |  |
| type | enum | Type of index<br>Possible values: `ManagedAzureSearch` | Yes |  |
| version | string (read-only) | The version of the resource | Yes |  |

### ManagedAzureAISearchIndexUpdate

Managed Azure AI Search Index Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The asset description text. | No |  |
| tags | object | Tag dictionary. Tags can be added, removed, and updated. | No |  |
| type | enum | Type of index<br>Possible values: `ManagedAzureSearch` | Yes |  |

### MemoryItem

A single memory item stored in the memory store, containing content and metadata.


### Discriminator for MemoryItem

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `user_profile` | [UserProfileMemoryItem](#userprofilememoryitem) |
| `chat_summary` | [ChatSummaryMemoryItem](#chatsummarymemoryitem) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string | The content of the memory. | Yes |  |
| kind | [MemoryItemKind](#memoryitemkind) | Memory item kind. | Yes |  |
| memory_id | string | The unique ID of the memory item. | Yes |  |
| scope | string | The namespace that logically groups and isolates memories, such as a user ID. | Yes |  |
| updated_at | integer | The last update time of the memory item. | Yes |  |

### MemoryItemKind

Memory item kind.

| Property | Value |
|----------|-------|
| **Description** | Memory item kind. |
| **Type** | string |
| **Values** | `user_profile`<br>`chat_summary` |

### MemoryOperation

Represents a single memory operation (create, update, or delete) performed on a memory item.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [MemoryOperationKind](#memoryoperationkind) | Memory operation kind. | Yes |  |
| memory_item | [MemoryItem](#memoryitem) | A single memory item stored in the memory store, containing content and metadata. | Yes |  |
| └─ content | string | The content of the memory. | Yes |  |
| └─ kind | [MemoryItemKind](#memoryitemkind) | The kind of the memory item. | Yes |  |
| └─ memory_id | string | The unique ID of the memory item. | Yes |  |
| └─ scope | string | The namespace that logically groups and isolates memories, such as a user ID. | Yes |  |
| └─ updated_at | integer | The last update time of the memory item. | Yes |  |

### MemoryOperationKind

Memory operation kind.

| Property | Value |
|----------|-------|
| **Description** | Memory operation kind. |
| **Type** | string |
| **Values** | `create`<br>`update`<br>`delete` |

### MemorySearchItem

A retrieved memory item from memory search.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| memory_item | [MemoryItem](#memoryitem) | A single memory item stored in the memory store, containing content and metadata. | Yes |  |
| └─ content | string | The content of the memory. | Yes |  |
| └─ kind | [MemoryItemKind](#memoryitemkind) | The kind of the memory item. | Yes |  |
| └─ memory_id | string | The unique ID of the memory item. | Yes |  |
| └─ scope | string | The namespace that logically groups and isolates memories, such as a user ID. | Yes |  |
| └─ updated_at | integer | The last update time of the memory item. | Yes |  |

### MemorySearchOptions

Memory search options.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_memories | integer | Maximum number of memory items to return. | No |  |

### MemorySearchPreviewTool

A tool for integrating memories into the agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| memory_store_name | string | The name of the memory store to use. | Yes |  |
| scope | string | The namespace used to group and isolate memories, such as a user ID.<br>Limits which memories can be retrieved or updated.<br>Use special variable `{{$userId}}` to scope memories to the current signed-in user. | Yes |  |
| search_options | [MemorySearchOptions](#memorysearchoptions) | Memory search options. | No |  |
| └─ max_memories | integer | Maximum number of memory items to return. | No |  |
| type | enum | The type of the tool. Always `memory_search_preview`.<br>Possible values: `memory_search_preview` | Yes |  |
| update_delay | integer | Time to wait before updating memories after inactivity (seconds). Default 300. | No | 300 |

### MemorySearchToolCallItemParam

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| results | array of [MemorySearchItem](#memorysearchitem) | The results returned from the memory search. | No |  |
| type | enum | <br>Possible values: `memory_search_call` | Yes |  |

### MemorySearchToolCallItemResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| response_id | string | The response on which the item is created. | No |  |
| results | array of [MemorySearchItem](#memorysearchitem) | The results returned from the memory search. | No |  |
| status | enum | The status of the memory search tool call. One of `in_progress`,<br>`searching`, `completed`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | <br>Possible values: `memory_search_call` | Yes |  |

### MemoryStoreDefaultDefinition

Default memory store implementation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chat_model | string | The name or identifier of the chat completion model deployment used for memory processing. | Yes |  |
| embedding_model | string | The name or identifier of the embedding model deployment used for memory processing. | Yes |  |
| kind | enum | The kind of the memory store.<br>Possible values: `default` | Yes |  |
| options | [MemoryStoreDefaultOptions](#memorystoredefaultoptions) | Default memory store configurations. | No |  |
| └─ chat_summary_enabled | boolean | Whether to enable chat summary extraction and storage. Default is true. | Yes | True |
| └─ user_profile_details | string | Specific categories or types of user profile information to extract and store. | No |  |
| └─ user_profile_enabled | boolean | Whether to enable user profile extraction and storage. Default is true. | Yes | True |

### MemoryStoreDefaultOptions

Default memory store configurations.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chat_summary_enabled | boolean | Whether to enable chat summary extraction and storage. Default is true. | Yes | True |
| user_profile_details | string | Specific categories or types of user profile information to extract and store. | No |  |
| user_profile_enabled | boolean | Whether to enable user profile extraction and storage. Default is true. | Yes | True |

### MemoryStoreDefinition

Base definition for memory store configurations.


### Discriminator for MemoryStoreDefinition

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `default` | [MemoryStoreDefaultDefinition](#memorystoredefaultdefinition) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [MemoryStoreKind](#memorystorekind) | The type of memory store implementation to use. | Yes |  |

### MemoryStoreDeleteScopeResponse

Response for deleting memories from a scope.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | Whether the deletion operation was successful. | Yes |  |
| name | string | The name of the memory store. | Yes |  |
| object | enum | The object type. Always 'memory_store.scope.deleted'.<br>Possible values: `memory_store.scope.deleted` | Yes |  |
| scope | string | The scope from which memories were deleted. | Yes |  |

### MemoryStoreKind

The type of memory store implementation to use.

| Property | Value |
|----------|-------|
| **Description** | The type of memory store implementation to use. |
| **Type** | string |
| **Values** | `default` |

### MemoryStoreObject

A memory store that can store and retrieve user memories.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (seconds) when the memory store was created. | Yes |  |
| definition | [MemoryStoreDefinition](#memorystoredefinition) | Base definition for memory store configurations. | Yes |  |
| └─ kind | [MemoryStoreKind](#memorystorekind) | The kind of the memory store. | Yes |  |
| description | string | A human-readable description of the memory store.<br>**Constraints:** maxLength: 512 | No |  |
| id | string | The unique identifier of the memory store. | Yes |  |
| metadata | object | Arbitrary key-value metadata to associate with the memory store. | No |  |
| name | string | The name of the memory store.<br>**Constraints:** maxLength: 256 | Yes |  |
| object | enum | The object type, which is always 'memory_store'.<br>Possible values: `memory_store` | Yes |  |
| updated_at | integer | The Unix timestamp (seconds) when the memory store was last updated. | Yes |  |

### MemoryStoreOperationUsage

Usage statistics of a memory store operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| embedding_tokens | integer | The number of embedding tokens. | Yes |  |
| input_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| input_tokens_details | [OpenAI.ResponseUsageInputTokensDetails](#openairesponseusageinputtokensdetails) |  | Yes |  |
| └─ cached_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| output_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| output_tokens_details | [OpenAI.ResponseUsageOutputTokensDetails](#openairesponseusageoutputtokensdetails) |  | Yes |  |
| └─ reasoning_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| total_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### MemoryStoreSearchResponse

Memory search response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| memories | array of [MemorySearchItem](#memorysearchitem) | Related memory items found during the search operation. | Yes |  |
| search_id | string | The unique ID of this search request. Use this value as previous_search_id in subsequent requests to perform incremental searches. | Yes |  |
| usage | [MemoryStoreOperationUsage](#memorystoreoperationusage) | Usage statistics of a memory store operation. | Yes |  |
| └─ embedding_tokens | integer | The number of embedding tokens. | Yes |  |
| └─ input_tokens | [OpenAI.integer](#openaiinteger) | The number of input tokens. | Yes |  |
| └─ input_tokens_details | [OpenAI.ResponseUsageInputTokensDetails](#openairesponseusageinputtokensdetails) | A detailed breakdown of the input tokens. | Yes |  |
| └─ output_tokens | [OpenAI.integer](#openaiinteger) | The number of output tokens. | Yes |  |
| └─ output_tokens_details | [OpenAI.ResponseUsageOutputTokensDetails](#openairesponseusageoutputtokensdetails) | A detailed breakdown of the output tokens. | Yes |  |
| └─ total_tokens | [OpenAI.integer](#openaiinteger) | The total number of tokens used. | Yes |  |

### MemoryStoreUpdateCompletedResult

Memory update result.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| memory_operations | array of [MemoryOperation](#memoryoperation) | A list of individual memory operations that were performed during the update. | Yes |  |
| usage | [MemoryStoreOperationUsage](#memorystoreoperationusage) | Usage statistics of a memory store operation. | Yes |  |
| └─ embedding_tokens | integer | The number of embedding tokens. | Yes |  |
| └─ input_tokens | [OpenAI.integer](#openaiinteger) | The number of input tokens. | Yes |  |
| └─ input_tokens_details | [OpenAI.ResponseUsageInputTokensDetails](#openairesponseusageinputtokensdetails) | A detailed breakdown of the input tokens. | Yes |  |
| └─ output_tokens | [OpenAI.integer](#openaiinteger) | The number of output tokens. | Yes |  |
| └─ output_tokens_details | [OpenAI.ResponseUsageOutputTokensDetails](#openairesponseusageoutputtokensdetails) | A detailed breakdown of the output tokens. | Yes |  |
| └─ total_tokens | [OpenAI.integer](#openaiinteger) | The total number of tokens used. | Yes |  |

### MemoryStoreUpdateResponse

Provides the status of a memory store update operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | [OpenAI.Error](#openaierror) |  | No |  |
| └─ additionalInfo | object |  | No |  |
| └─ code | string (nullable) |  | Yes |  |
| └─ debugInfo | object |  | No |  |
| └─ details | array of [OpenAI.Error](#openaierror) |  | No |  |
| └─ message | string |  | Yes |  |
| └─ param | string (nullable) |  | No |  |
| └─ type | string |  | No |  |
| result | [MemoryStoreUpdateCompletedResult](#memorystoreupdatecompletedresult) | Memory update result. | No |  |
| └─ memory_operations | array of [MemoryOperation](#memoryoperation) | A list of individual memory operations that were performed during the update. | Yes |  |
| └─ usage | [MemoryStoreOperationUsage](#memorystoreoperationusage) | Usage statistics associated with the memory update operation. | Yes |  |
| status | [MemoryStoreUpdateStatus](#memorystoreupdatestatus) | Status of a memory store update operation. | Yes |  |
| superseded_by | string | The update_id the operation was superseded by when status is "superseded". | No |  |
| update_id | string | The unique ID of this update request. Use this value as previous_update_id in subsequent requests to perform incremental updates. | Yes |  |

### MemoryStoreUpdateStatus

Status of a memory store update operation.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `queued`<br>`in_progress`<br>`completed`<br>`failed`<br>`superseded` |

### MicrosoftFabricPreviewTool

The input definition information for a Microsoft Fabric tool as used to configure an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| fabric_dataagent_preview | [FabricDataAgentToolParameters](#fabricdataagenttoolparameters) | The fabric data agent tool parameters. | Yes |  |
| └─ project_connections | array of [ToolProjectConnection](#toolprojectconnection) | The project connections attached to this tool. There can be a maximum of 1 connection<br>resource attached to the tool.<br>**Constraints:** maxItems: 1 | No |  |
| type | enum | The object type, which is always 'fabric_dataagent_preview'.<br>Possible values: `fabric_dataagent_preview` | Yes |  |

### ModelDeployment

Model Deployment Definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| capabilities | object (read-only) | Capabilities of deployed model | Yes |  |
| connectionName | string (read-only) | Name of the connection the deployment comes from | No |  |
| modelName | string (read-only) | Publisher-specific name of the deployed model | Yes |  |
| modelPublisher | string (read-only) | Name of the deployed model's publisher | Yes |  |
| modelVersion | string (read-only) | Publisher-specific version of the deployed model | Yes |  |
| name | string (read-only) | Name of the deployment | Yes |  |
| sku | [Sku](#sku) (read-only) | Sku information | Yes |  |
| └─ capacity | integer | Sku capacity | Yes |  |
| └─ family | string | Sku family | Yes |  |
| └─ name | string | Sku name | Yes |  |
| └─ size | string | Sku size | Yes |  |
| └─ tier | string | Sku tier | Yes |  |
| type | enum | The type of the deployment<br>Possible values: `ModelDeployment` | Yes |  |

### ModelSamplingParams

Represents a set of parameters used to control the sampling behavior of a language model during text generation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_completion_tokens | integer | The maximum number of tokens allowed in the completion. | Yes |  |
| seed | integer | The random seed for reproducibility. | Yes |  |
| temperature | number | The temperature parameter for sampling. | Yes |  |
| top_p | number | The top-p parameter for nucleus sampling. | Yes |  |

### ModelSamplingParamsUpdate

Represents a set of parameters used to control the sampling behavior of a language model during text generation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_completion_tokens | integer | The maximum number of tokens allowed in the completion. | No |  |
| seed | integer | The random seed for reproducibility. | No |  |
| temperature | number | The temperature parameter for sampling. | No |  |
| top_p | number | The top-p parameter for nucleus sampling. | No |  |

### MonthlyRecurrenceSchedule

Monthly recurrence schedule.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| daysOfMonth | array of integer | Days of the month for the recurrence schedule. | Yes |  |
| type | enum | Monthly recurrence type.<br>Possible values: `Monthly` | Yes |  |

### NoAuthenticationCredentials

Credentials that do not require authentication

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The credential type <br>Possible values: `None` | Yes |  |

### OAuthConsentRequestOutputItem

Request from the service for the user to perform OAuth consent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| consent_link | string | The link the user can use to perform OAuth consent. | Yes |  |
| id | string |  | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| server_label | string | The server label for the OAuth consent request. | Yes |  |
| type | enum | <br>Possible values: `oauth_consent_request` | Yes |  |

### OneTimeTrigger

One-time trigger.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| timeZone | string | Time zone for the one-time trigger. | No | UTC |
| triggerAt | string | Date and time for the one-time trigger in ISO 8601 format. | Yes |  |
| type | enum | <br>Possible values: `OneTime` | Yes |  |

### OpenAI.Annotation

An annotation that applies to a span of output text.


### Discriminator for OpenAI.Annotation

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `file_citation` | [OpenAI.FileCitationBody](#openaifilecitationbody) |
| `url_citation` | [OpenAI.UrlCitationBody](#openaiurlcitationbody) |
| `container_file_citation` | [OpenAI.ContainerFileCitationBody](#openaicontainerfilecitationbody) |
| `file_path` | [OpenAI.FilePath](#openaifilepath) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.AnnotationType](#openaiannotationtype) |  | Yes |  |

### OpenAI.AnnotationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `file_citation`<br>`url_citation`<br>`container_file_citation`<br>`file_path` |

### OpenAI.ApplyPatchCallOutputStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `completed`<br>`failed` |

### OpenAI.ApplyPatchCallOutputStatusParam

Outcome values reported for apply_patch tool call outputs.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `completed`<br>`failed` |

### OpenAI.ApplyPatchCallStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed` |

### OpenAI.ApplyPatchCallStatusParam

Status values reported for apply_patch tool calls.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed` |

### OpenAI.ApplyPatchCreateFileOperation

Instruction describing how to create a file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| diff | string | Diff to apply. | Yes |  |
| path | string | Path of the file to create. | Yes |  |
| type | enum | Create a new file with the provided diff.<br>Possible values: `create_file` | Yes |  |

### OpenAI.ApplyPatchCreateFileOperationParam

Instruction for creating a new file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| diff | string | Unified diff content to apply when creating the file.<br>**Constraints:** maxLength: 10485760 | Yes |  |
| path | string | Path of the file to create relative to the workspace root.<br>**Constraints:** minLength: 1 | Yes |  |
| type | enum | The operation type. Always `create_file`.<br>Possible values: `create_file` | Yes |  |

### OpenAI.ApplyPatchDeleteFileOperation

Instruction describing how to delete a file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| path | string | Path of the file to delete. | Yes |  |
| type | enum | Delete the specified file.<br>Possible values: `delete_file` | Yes |  |

### OpenAI.ApplyPatchDeleteFileOperationParam

Instruction for deleting an existing file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| path | string | Path of the file to delete relative to the workspace root.<br>**Constraints:** minLength: 1 | Yes |  |
| type | enum | The operation type. Always `delete_file`.<br>Possible values: `delete_file` | Yes |  |

### OpenAI.ApplyPatchFileOperation

One of the create_file, delete_file, or update_file operations applied via apply_patch.


### Discriminator for OpenAI.ApplyPatchFileOperation

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `create_file` | [OpenAI.ApplyPatchCreateFileOperation](#openaiapplypatchcreatefileoperation) |
| `delete_file` | [OpenAI.ApplyPatchDeleteFileOperation](#openaiapplypatchdeletefileoperation) |
| `update_file` | [OpenAI.ApplyPatchUpdateFileOperation](#openaiapplypatchupdatefileoperation) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ApplyPatchFileOperationType](#openaiapplypatchfileoperationtype) |  | Yes |  |

### OpenAI.ApplyPatchFileOperationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `create_file`<br>`delete_file`<br>`update_file` |

### OpenAI.ApplyPatchOperationParam

One of the create_file, delete_file, or update_file operations supplied to the apply_patch tool.


### Discriminator for OpenAI.ApplyPatchOperationParam

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `create_file` | [OpenAI.ApplyPatchCreateFileOperationParam](#openaiapplypatchcreatefileoperationparam) |
| `delete_file` | [OpenAI.ApplyPatchDeleteFileOperationParam](#openaiapplypatchdeletefileoperationparam) |
| `update_file` | [OpenAI.ApplyPatchUpdateFileOperationParam](#openaiapplypatchupdatefileoperationparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ApplyPatchOperationParamType](#openaiapplypatchoperationparamtype) |  | Yes |  |

### OpenAI.ApplyPatchOperationParamType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `create_file`<br>`delete_file`<br>`update_file` |

### OpenAI.ApplyPatchToolParam

Allows the assistant to create, delete, or update files using unified diffs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the tool. Always `apply_patch`.<br>Possible values: `apply_patch` | Yes |  |

### OpenAI.ApplyPatchUpdateFileOperation

Instruction describing how to update a file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| diff | string | Diff to apply. | Yes |  |
| path | string | Path of the file to update. | Yes |  |
| type | enum | Update an existing file with the provided diff.<br>Possible values: `update_file` | Yes |  |

### OpenAI.ApplyPatchUpdateFileOperationParam

Instruction for updating an existing file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| diff | string | Unified diff content to apply to the existing file.<br>**Constraints:** maxLength: 10485760 | Yes |  |
| path | string | Path of the file to update relative to the workspace root.<br>**Constraints:** minLength: 1 | Yes |  |
| type | enum | The operation type. Always `update_file`.<br>Possible values: `update_file` | Yes |  |

### OpenAI.ApproximateLocation

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| city | string (nullable) |  | No |  |
| country | string (nullable) |  | No |  |
| region | string (nullable) |  | No |  |
| timezone | string (nullable) |  | No |  |
| type | enum | The type of location approximation. Always `approximate`.<br>Possible values: `approximate` | Yes |  |

### OpenAI.ChatCompletionTool

A function tool that can be used to generate a response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.FunctionObject](#openaifunctionobject) |  | Yes |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatModel

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `gpt-5.2`<br>`gpt-5.2-2025-12-11`<br>`gpt-5.2-chat-latest`<br>`gpt-5.2-pro`<br>`gpt-5.2-pro-2025-12-11`<br>`gpt-5.1`<br>`gpt-5.1-2025-11-13`<br>`gpt-5.1-codex`<br>`gpt-5.1-mini`<br>`gpt-5.1-chat-latest`<br>`gpt-5`<br>`gpt-5-mini`<br>`gpt-5-nano`<br>`gpt-5-2025-08-07`<br>`gpt-5-mini-2025-08-07`<br>`gpt-5-nano-2025-08-07`<br>`gpt-5-chat-latest`<br>`gpt-4.1`<br>`gpt-4.1-mini`<br>`gpt-4.1-nano`<br>`gpt-4.1-2025-04-14`<br>`gpt-4.1-mini-2025-04-14`<br>`gpt-4.1-nano-2025-04-14`<br>`o4-mini`<br>`o4-mini-2025-04-16`<br>`o3`<br>`o3-2025-04-16`<br>`o3-mini`<br>`o3-mini-2025-01-31`<br>`o1`<br>`o1-2024-12-17`<br>`o1-preview`<br>`o1-preview-2024-09-12`<br>`o1-mini`<br>`o1-mini-2024-09-12`<br>`gpt-4o`<br>`gpt-4o-2024-11-20`<br>`gpt-4o-2024-08-06`<br>`gpt-4o-2024-05-13`<br>`gpt-4o-audio-preview`<br>`gpt-4o-audio-preview-2024-10-01`<br>`gpt-4o-audio-preview-2024-12-17`<br>`gpt-4o-audio-preview-2025-06-03`<br>`gpt-4o-mini-audio-preview`<br>`gpt-4o-mini-audio-preview-2024-12-17`<br>`gpt-4o-search-preview`<br>`gpt-4o-mini-search-preview`<br>`gpt-4o-search-preview-2025-03-11`<br>`gpt-4o-mini-search-preview-2025-03-11`<br>`chatgpt-4o-latest`<br>`codex-mini-latest`<br>`gpt-4o-mini`<br>`gpt-4o-mini-2024-07-18`<br>`gpt-4-turbo`<br>`gpt-4-turbo-2024-04-09`<br>`gpt-4-0125-preview`<br>`gpt-4-turbo-preview`<br>`gpt-4-1106-preview`<br>`gpt-4-vision-preview`<br>`gpt-4`<br>`gpt-4-0314`<br>`gpt-4-0613`<br>`gpt-4-32k`<br>`gpt-4-32k-0314`<br>`gpt-4-32k-0613`<br>`gpt-3.5-turbo`<br>`gpt-3.5-turbo-16k`<br>`gpt-3.5-turbo-0301`<br>`gpt-3.5-turbo-0613`<br>`gpt-3.5-turbo-1106`<br>`gpt-3.5-turbo-0125`<br>`gpt-3.5-turbo-16k-0613` |

### OpenAI.ClickButtonType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `left`<br>`right`<br>`wheel`<br>`back`<br>`forward` |

### OpenAI.ClickParam

A click action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| button | [OpenAI.ClickButtonType](#openaiclickbuttontype) |  | Yes |  |
| type | enum | Specifies the event type. For a click action, this property is always `click`.<br>Possible values: `click` | Yes |  |
| x | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| y | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.CodeInterpreterContainerAuto

Configuration for a code interpreter container. Optionally specify the IDs of the files to run the code on.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_ids | array of string | An optional list of uploaded files to make available to your code. | No |  |
| memory_limit | [OpenAI.ContainerMemoryLimit](#openaicontainermemorylimit) (nullable) |  | No |  |
| type | enum | Always `auto`.<br>Possible values: `auto` | Yes |  |

### OpenAI.CodeInterpreterOutputImage

The image output from the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the output. Always `image`.<br>Possible values: `image` | Yes |  |
| url | string | The URL of the image output from the code interpreter. | Yes |  |

### OpenAI.CodeInterpreterOutputLogs

The logs output from the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logs | string | The logs output from the code interpreter. | Yes |  |
| type | enum | The type of the output. Always `logs`.<br>Possible values: `logs` | Yes |  |

### OpenAI.CodeInterpreterTool

A tool that runs Python code to help generate a response to a prompt.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container | string or [OpenAI.CodeInterpreterContainerAuto](#openaicodeinterpretercontainerauto) | The code interpreter container. Can be a container ID or an object that<br>specifies uploaded file IDs to make available to your code, along with an<br>optional `memory_limit` setting.<br>If not provided, the service assumes auto. | No |  |
| type | enum | The type of the code interpreter tool. Always `code_interpreter`.<br>Possible values: `code_interpreter` | Yes |  |

### OpenAI.CompactResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | Unix timestamp (in seconds) when the compacted conversation was created. | Yes |  |
| id | string | The unique identifier for the compacted response. | Yes |  |
| object | enum | The object type. Always `response.compaction`.<br>Possible values: `response.compaction` | Yes |  |
| output | array of [OpenAI.OutputItem](#openaioutputitem) | The compacted list of output items. This is a list of all user messages, followed by a single compaction item. | Yes |  |
| usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | Yes |  |
| └─ input_tokens | [OpenAI.integer](#openaiinteger) | The number of input tokens. | Yes |  |
| └─ input_tokens_details | [OpenAI.ResponseUsageInputTokensDetails](#openairesponseusageinputtokensdetails) | A detailed breakdown of the input tokens. | Yes |  |
| └─ output_tokens | [OpenAI.integer](#openaiinteger) | The number of output tokens. | Yes |  |
| └─ output_tokens_details | [OpenAI.ResponseUsageOutputTokensDetails](#openairesponseusageoutputtokensdetails) | A detailed breakdown of the output tokens. | Yes |  |
| └─ total_tokens | [OpenAI.integer](#openaiinteger) | The total number of tokens used. | Yes |  |

### OpenAI.CompactResponseMethodPublicBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string or array of [OpenAI.InputItem](#openaiinputitem) |  | No |  |
| instructions | string (nullable) |  | No |  |
| model | [OpenAI.ModelIdsCompaction](#openaimodelidscompaction) | Model ID used to generate the response, like `gpt-5` or `o3`. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models) to browse and compare available models. | Yes |  |
| previous_response_id | string (nullable) |  | No |  |

### OpenAI.ComparisonFilter

A filter used to compare a specified attribute key to a given value using a defined comparison operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| key | string | The key to compare against the value. | Yes |  |
| type | enum | Specifies the comparison operator: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `nin`.<br>  - `eq`: equals<br>  - `ne`: not equal<br>  - `gt`: greater than<br>  - `gte`: greater than or equal<br>  - `lt`: less than<br>  - `lte`: less than or equal<br>  - `in`: in<br>  - `nin`: not in<br>Possible values: `eq`, `ne`, `gt`, `gte`, `lt`, `lte` | Yes |  |
| value | string or [OpenAI.numeric](#openainumeric) or boolean or array of [OpenAI.ComparisonFilterValueItems](#openaicomparisonfiltervalueitems) | The value to compare against the attribute key; supports string, number, or boolean types. | Yes |  |

### OpenAI.ComparisonFilterValueItems

**Type**: string or [OpenAI.numeric](#openainumeric)


### OpenAI.CompoundFilter

Combine multiple filters using `and` or `or`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | array of [OpenAI.ComparisonFilter](#openaicomparisonfilter) or object | Array of filters to combine. Items can be `ComparisonFilter` or `CompoundFilter`. | Yes |  |
| type | enum | Type of operation: `and` or `or`.<br>Possible values: `and`, `or` | Yes |  |

### OpenAI.ComputerAction


### Discriminator for OpenAI.ComputerAction

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `click` | [OpenAI.ClickParam](#openaiclickparam) |
| `double_click` | [OpenAI.DoubleClickAction](#openaidoubleclickaction) |
| `drag` | [OpenAI.Drag](#openaidrag) |
| `keypress` | [OpenAI.KeyPressAction](#openaikeypressaction) |
| `move` | [OpenAI.Move](#openaimove) |
| `screenshot` | [OpenAI.Screenshot](#openaiscreenshot) |
| `scroll` | [OpenAI.Scroll](#openaiscroll) |
| `type` | [OpenAI.Type](#openaitype) |
| `wait` | [OpenAI.Wait](#openaiwait) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ComputerActionType](#openaicomputeractiontype) |  | Yes |  |

### OpenAI.ComputerActionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `click`<br>`double_click`<br>`drag`<br>`keypress`<br>`move`<br>`screenshot`<br>`scroll`<br>`type`<br>`wait` |

### OpenAI.ComputerCallSafetyCheckParam

A pending safety check for the computer call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string (nullable) |  | No |  |
| id | string | The ID of the pending safety check. | Yes |  |
| message | string (nullable) |  | No |  |

### OpenAI.ComputerEnvironment

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `windows`<br>`mac`<br>`linux`<br>`ubuntu`<br>`browser` |

### OpenAI.ComputerScreenshotContent

A screenshot of a computer.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string (nullable) |  | Yes |  |
| image_url | string |  | Yes |  |
| type | enum | Specifies the event type. For a computer screenshot, this property is always set to `computer_screenshot`.<br>Possible values: `computer_screenshot` | Yes |  |

### OpenAI.ComputerScreenshotImage

A computer screenshot image used with the computer use tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The identifier of an uploaded file that contains the screenshot. | No |  |
| image_url | string | The URL of the screenshot image. | No |  |
| type | enum | Specifies the event type. For a computer screenshot, this property is<br>  always set to `computer_screenshot`.<br>Possible values: `computer_screenshot` | Yes |  |

### OpenAI.ComputerUsePreviewTool

A tool that controls a virtual computer.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| display_height | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| display_width | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| environment | [OpenAI.ComputerEnvironment](#openaicomputerenvironment) |  | Yes |  |
| type | enum | The type of the computer use tool. Always `computer_use_preview`.<br>Possible values: `computer_use_preview` | Yes |  |

### OpenAI.ContainerFileCitationBody

A citation for a container file used to generate a model response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container_id | string | The ID of the container file. | Yes |  |
| end_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| file_id | string | The ID of the file. | Yes |  |
| filename | string | The filename of the container file cited. | Yes |  |
| start_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the container file citation. Always `container_file_citation`.<br>Possible values: `container_file_citation` | Yes |  |

### OpenAI.ContainerMemoryLimit

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `1g`<br>`4g`<br>`16g`<br>`64g` |

### OpenAI.ConversationItem

A single item within a conversation. The set of possible types are the same as the `output` type of a [Response object](https://platform.openai.com/docs/api-reference/responses/object#responses/object-output).


### Discriminator for OpenAI.ConversationItem

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `message` | [OpenAI.ConversationItemMessage](#openaiconversationitemmessage) |
| `function_call` | [OpenAI.ConversationItemFunctionToolCallResource](#openaiconversationitemfunctiontoolcallresource) |
| `function_call_output` | [OpenAI.ConversationItemFunctionToolCallOutputResource](#openaiconversationitemfunctiontoolcalloutputresource) |
| `file_search_call` | [OpenAI.ConversationItemFileSearchToolCall](#openaiconversationitemfilesearchtoolcall) |
| `web_search_call` | [OpenAI.ConversationItemWebSearchToolCall](#openaiconversationitemwebsearchtoolcall) |
| `image_generation_call` | [OpenAI.ConversationItemImageGenToolCall](#openaiconversationitemimagegentoolcall) |
| `computer_call` | [OpenAI.ConversationItemComputerToolCall](#openaiconversationitemcomputertoolcall) |
| `computer_call_output` | [OpenAI.ConversationItemComputerToolCallOutputResource](#openaiconversationitemcomputertoolcalloutputresource) |
| `reasoning` | [OpenAI.ConversationItemReasoningItem](#openaiconversationitemreasoningitem) |
| `code_interpreter_call` | [OpenAI.ConversationItemCodeInterpreterToolCall](#openaiconversationitemcodeinterpretertoolcall) |
| `local_shell_call` | [OpenAI.ConversationItemLocalShellToolCall](#openaiconversationitemlocalshelltoolcall) |
| `local_shell_call_output` | [OpenAI.ConversationItemLocalShellToolCallOutput](#openaiconversationitemlocalshelltoolcalloutput) |
| `shell_call` | [OpenAI.ConversationItemFunctionShellCall](#openaiconversationitemfunctionshellcall) |
| `shell_call_output` | [OpenAI.ConversationItemFunctionShellCallOutput](#openaiconversationitemfunctionshellcalloutput) |
| `apply_patch_call` | [OpenAI.ConversationItemApplyPatchToolCall](#openaiconversationitemapplypatchtoolcall) |
| `apply_patch_call_output` | [OpenAI.ConversationItemApplyPatchToolCallOutput](#openaiconversationitemapplypatchtoolcalloutput) |
| `mcp_list_tools` | [OpenAI.ConversationItemMcpListTools](#openaiconversationitemmcplisttools) |
| `mcp_approval_request` | [OpenAI.ConversationItemMcpApprovalRequest](#openaiconversationitemmcpapprovalrequest) |
| `mcp_approval_response` | [OpenAI.ConversationItemMcpApprovalResponseResource](#openaiconversationitemmcpapprovalresponseresource) |
| `mcp_call` | [OpenAI.ConversationItemMcpToolCall](#openaiconversationitemmcptoolcall) |
| `custom_tool_call` | [OpenAI.ConversationItemCustomToolCall](#openaiconversationitemcustomtoolcall) |
| `custom_tool_call_output` | [OpenAI.ConversationItemCustomToolCallOutput](#openaiconversationitemcustomtoolcalloutput) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ConversationItemType](#openaiconversationitemtype) |  | Yes |  |

### OpenAI.ConversationItemApplyPatchToolCall

A tool call that applies file diffs by creating, deleting, or updating files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the apply patch tool call. Populated when this item is returned via API. | Yes |  |
| operation | [OpenAI.ApplyPatchFileOperation](#openaiapplypatchfileoperation) | One of the create_file, delete_file, or update_file operations applied via apply_patch. | Yes |  |
| └─ type | [OpenAI.ApplyPatchFileOperationType](#openaiapplypatchfileoperationtype) |  | Yes |  |
| status | [OpenAI.ApplyPatchCallStatus](#openaiapplypatchcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call`.<br>Possible values: `apply_patch_call` | Yes |  |

### OpenAI.ConversationItemApplyPatchToolCallOutput

The output emitted by an apply patch tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call output. | No |  |
| id | string | The unique ID of the apply patch tool call output. Populated when this item is returned via API. | Yes |  |
| output | string (nullable) |  | No |  |
| status | [OpenAI.ApplyPatchCallOutputStatus](#openaiapplypatchcalloutputstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call_output`.<br>Possible values: `apply_patch_call_output` | Yes |  |

### OpenAI.ConversationItemCodeInterpreterToolCall

A tool call to run code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string (nullable) |  | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| id | string | The unique ID of the code interpreter tool call. | Yes |  |
| outputs | array of [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) or [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) |  | Yes |  |
| status | enum | The status of the code interpreter tool call. Valid values are `in_progress`, `completed`, `incomplete`, `interpreting`, and `failed`.<br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | The type of the code interpreter tool call. Always `code_interpreter_call`.<br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.ConversationItemComputerToolCall

A tool call to a computer use tool. See the
[computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| id | string | The unique ID of the computer call. | Yes |  |
| pending_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The pending safety checks for the computer call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the computer call. Always `computer_call`.<br>Possible values: `computer_call` | Yes |  |

### OpenAI.ConversationItemComputerToolCallOutputResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| acknowledged_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The safety checks reported by the API that have been acknowledged by the<br>  developer. | No |  |
| call_id | string | The ID of the computer tool call that produced the output. | Yes |  |
| id | string | The ID of the computer tool call output. | No |  |
| output | [OpenAI.ComputerScreenshotImage](#openaicomputerscreenshotimage) | A computer screenshot image used with the computer use tool. | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the computer tool call output. Always `computer_call_output`.<br>Possible values: `computer_call_output` | Yes |  |

### OpenAI.ConversationItemCustomToolCall

A call to a custom tool created by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | An identifier used to map this custom tool call to a tool call output. | Yes |  |
| id | string | The unique ID of the custom tool call in the OpenAI platform. | No |  |
| input | string | The input for the custom tool call generated by the model. | Yes |  |
| name | string | The name of the custom tool being called. | Yes |  |
| type | enum | The type of the custom tool call. Always `custom_tool_call`.<br>Possible values: `custom_tool_call` | Yes |  |

### OpenAI.ConversationItemCustomToolCallOutput

The output of a custom tool call from your code, being sent back to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The call ID, used to map this custom tool call output to a custom tool call. | Yes |  |
| id | string | The unique ID of the custom tool call output in the OpenAI platform. | No |  |
| output | string or array of [OpenAI.FunctionAndCustomToolCallOutput](#openaifunctionandcustomtoolcalloutput) | The output from the custom tool call generated by your code.<br>  Can be a string or an list of output content. | Yes |  |
| type | enum | The type of the custom tool call output. Always `custom_tool_call_output`.<br>Possible values: `custom_tool_call_output` | Yes |  |

### OpenAI.ConversationItemFileSearchToolCall

The results of a file search tool call. See the
[file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the file search tool call. | Yes |  |
| queries | array of string | The queries used to search for files. | Yes |  |
| results | array of [OpenAI.FileSearchToolCallResults](#openaifilesearchtoolcallresults) |  | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`,<br>  `searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | The type of the file search tool call. Always `file_search_call`.<br>Possible values: `file_search_call` | Yes |  |

### OpenAI.ConversationItemFunctionShellCall

A tool call that executes one or more shell commands in a managed environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.FunctionShellAction](#openaifunctionshellaction) | Execute a shell command. | Yes |  |
| └─ commands | array of string |  | Yes |  |
| └─ max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| └─ timeout_ms | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the shell tool call. Populated when this item is returned via API. | Yes |  |
| status | [OpenAI.LocalShellCallStatus](#openailocalshellcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `shell_call`.<br>Possible values: `shell_call` | Yes |  |

### OpenAI.ConversationItemFunctionShellCallOutput

The output of a shell tool call that was emitted.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The identifier of the actor that created the item. | No |  |
| id | string | The unique ID of the shell call output. Populated when this item is returned via API. | Yes |  |
| max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| output | array of [OpenAI.FunctionShellCallOutputContent](#openaifunctionshellcalloutputcontent) | An array of shell call output contents | Yes |  |
| type | enum | The type of the shell call output. Always `shell_call_output`.<br>Possible values: `shell_call_output` | Yes |  |

### OpenAI.ConversationItemFunctionToolCallOutputResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call output. Populated when this item<br>  is returned via API. | No |  |
| output | string or array of [OpenAI.FunctionAndCustomToolCallOutput](#openaifunctionandcustomtoolcalloutput) | The output from the function call generated by your code.<br>  Can be a string or an list of output content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call output. Always `function_call_output`.<br>Possible values: `function_call_output` | Yes |  |

### OpenAI.ConversationItemFunctionToolCallResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call. | No |  |
| name | string | The name of the function to run. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call. Always `function_call`.<br>Possible values: `function_call` | Yes |  |

### OpenAI.ConversationItemImageGenToolCall

An image generation request made by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the image generation call. | Yes |  |
| result | string (nullable) |  | Yes |  |
| status | enum | The status of the image generation call.<br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | The type of the image generation call. Always `image_generation_call`.<br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.ConversationItemList

A list of Conversation items.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.ConversationItem](#openaiconversationitem) | A list of conversation items. | Yes |  |
| first_id | string | The ID of the first item in the list. | Yes |  |
| has_more | boolean | Whether there are more items available. | Yes |  |
| last_id | string | The ID of the last item in the list. | Yes |  |
| object | enum | The type of object returned, must be `list`.<br>Possible values: `list` | Yes |  |

### OpenAI.ConversationItemLocalShellToolCall

A tool call to run a command on the local shell.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| id | string | The unique ID of the local shell call. | Yes |  |
| status | enum | The status of the local shell call.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the local shell call. Always `local_shell_call`.<br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.ConversationItemLocalShellToolCallOutput

The output of a local shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| output | string | A JSON string of the output of the local shell tool call. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the local shell tool call output. Always `local_shell_call_output`.<br>Possible values: `local_shell_call_output` | Yes |  |

### OpenAI.ConversationItemMcpApprovalRequest

A request for human approval of a tool invocation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| id | string | The unique ID of the approval request. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | The type of the item. Always `mcp_approval_request`.<br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.ConversationItemMcpApprovalResponseResource

A response to an MCP approval request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string | The ID of the approval request being answered. | Yes |  |
| approve | boolean | Whether the request was approved. | Yes |  |
| id | string | The unique ID of the approval response | Yes |  |
| reason | string (nullable) |  | No |  |
| type | enum | The type of the item. Always `mcp_approval_response`.<br>Possible values: `mcp_approval_response` | Yes |  |

### OpenAI.ConversationItemMcpListTools

A list of tools available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the list. | Yes |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array of [OpenAI.MCPListToolsTool](#openaimcplisttoolstool) | The tools available on the server. | Yes |  |
| type | enum | The type of the item. Always `mcp_list_tools`.<br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.ConversationItemMcpToolCall

An invocation of a tool on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string (nullable) |  | No |  |
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the tool call. | Yes |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string (nullable) |  | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| status | [OpenAI.MCPToolCallStatus](#openaimcptoolcallstatus) |  | No |  |
| type | enum | The type of the item. Always `mcp_call`.<br>Possible values: `mcp_call` | Yes |  |

### OpenAI.ConversationItemMessage

A message to or from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.MessageContent](#openaimessagecontent) | The content of the message | Yes |  |
| id | string | The unique ID of the message. | Yes |  |
| role | [OpenAI.MessageRole](#openaimessagerole) |  | Yes |  |
| status | [OpenAI.MessageStatus](#openaimessagestatus) |  | Yes |  |
| type | enum | The type of the message. Always set to `message`.<br>Possible values: `message` | Yes |  |

### OpenAI.ConversationItemReasoningItem

A description of the chain of thought used by a reasoning model while generating
a response. Be sure to include these items in your `input` to the Responses API
for subsequent turns of a conversation if you are manually
[managing context](https://platform.openai.com/docs/guides/conversation-state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.ReasoningTextContent](#openaireasoningtextcontent) | Reasoning text content. | No |  |
| encrypted_content | string (nullable) |  | No |  |
| id | string | The unique identifier of the reasoning content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| summary | array of [OpenAI.Summary](#openaisummary) | Reasoning summary content. | Yes |  |
| type | enum | The type of the object. Always `reasoning`.<br>Possible values: `reasoning` | Yes |  |

### OpenAI.ConversationItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`function_call`<br>`function_call_output`<br>`file_search_call`<br>`web_search_call`<br>`image_generation_call`<br>`computer_call`<br>`computer_call_output`<br>`reasoning`<br>`code_interpreter_call`<br>`local_shell_call`<br>`local_shell_call_output`<br>`shell_call`<br>`shell_call_output`<br>`apply_patch_call`<br>`apply_patch_call_output`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`mcp_approval_response`<br>`mcp_call`<br>`custom_tool_call`<br>`custom_tool_call_output` |

### OpenAI.ConversationItemWebSearchToolCall

The results of a web search tool call. See the
[web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) or [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) or [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) | An object describing the specific action taken in this web search call.<br>  Includes details on how the model used the web (search, open_page, find). | Yes |  |
| id | string | The unique ID of the web search tool call. | Yes |  |
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | The type of the web search tool call. Always `web_search_call`.<br>Possible values: `web_search_call` | Yes |  |

### OpenAI.ConversationParam

The conversation that this response belongs to. Items from this conversation are prepended to `input_items` for this response request.
Input items and output items from this response are automatically added to this conversation after this response completes.

**Type**: string or [OpenAI.ConversationParam-2](#openaiconversationparam-2)

The conversation that this response belongs to. Items from this conversation are prepended to `input_items` for this response request.
Input items and output items from this response are automatically added to this conversation after this response completes.


### OpenAI.ConversationParam-2

The conversation that this response belongs to.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the conversation. | Yes |  |

### OpenAI.ConversationReference

The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the conversation that this response was associated with. | Yes |  |

### OpenAI.ConversationResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The time at which the conversation was created, measured in seconds since the Unix epoch. | Yes |  |
| id | string | The unique ID of the conversation. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| object | enum | The object type, which is always `conversation`.<br>Possible values: `conversation` | Yes |  |

### OpenAI.CreateChatCompletionRequestResponseFormat

An object specifying the format that the model must output.
Setting to `{ "type": "json_schema", "json_schema": {...} }` enables
Structured Outputs which ensures the model will match your supplied JSON
schema. Learn more in the [Structured Outputs
guide](https://platform.openai.com/docs/guides/structured-outputs).
Setting to `{ "type": "json_object" }` enables the older JSON mode, which
ensures the message the model generates is valid JSON. Using `json_schema`
is preferred for models that support it.


### Discriminator for OpenAI.CreateChatCompletionRequestResponseFormat

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `text` | [OpenAI.CreateChatCompletionRequestResponseFormatResponseFormatText](#openaicreatechatcompletionrequestresponseformatresponseformattext) |
| `json_object` | [OpenAI.CreateChatCompletionRequestResponseFormatResponseFormatJsonObject](#openaicreatechatcompletionrequestresponseformatresponseformatjsonobject) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.CreateChatCompletionRequestResponseFormatType](#openaicreatechatcompletionrequestresponseformattype) |  | Yes |  |

### OpenAI.CreateChatCompletionRequestResponseFormatResponseFormatJsonObject

JSON object response format. An older method of generating JSON responses.
Using `json_schema` is recommended for models that support it. Note that the
model will not generate JSON without a system or user message instructing it
to do so.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `json_object`.<br>Possible values: `json_object` | Yes |  |

### OpenAI.CreateChatCompletionRequestResponseFormatResponseFormatText

Default response format. Used to generate text responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.CreateChatCompletionRequestResponseFormatType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`json_schema`<br>`json_object` |

### OpenAI.CreateConversationBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.InputItem](#openaiinputitem) |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |

### OpenAI.CreateEvalCompletionsRunDataSource

A CompletionsRunDataSource object describing a model sampling configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | [OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesTemplate](#openaicreateevalcompletionsrundatasourceinputmessagestemplate) or [OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesItemReference](#openaicreateevalcompletionsrundatasourceinputmessagesitemreference) | Used when sampling from a model. Dictates the structure of the messages passed into the model. Can either be a reference to a prebuilt trajectory (ie, `item.input_trajectory`), or a template with variable references to the `item` namespace. | No |  |
| model | string | The name of the model to use for generating completions (e.g. "o3-mini"). | No |  |
| sampling_params | [OpenAI.CreateEvalCompletionsRunDataSourceSamplingParams](#openaicreateevalcompletionsrundatasourcesamplingparams) |  | No |  |
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) or [OpenAI.EvalStoredCompletionsSource](#openaievalstoredcompletionssource) | Determines what populates the `item` namespace in this run's data source. | Yes |  |
| type | enum | The type of run data source. Always `completions`.<br>Possible values: `completions` | Yes |  |

### OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesItemReference

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_reference | string |  | Yes |  |
| type | enum | <br>Possible values: `item_reference` | Yes |  |

### OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesTemplate

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| template | array of [OpenAI.EasyInputMessage](#openaieasyinputmessage) or [OpenAI.EvalItem](#openaievalitem) |  | Yes |  |
| type | enum | <br>Possible values: `template` | Yes |  |

### OpenAI.CreateEvalCompletionsRunDataSourceSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_completion_tokens | [OpenAI.integer](#openaiinteger) |  | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| response_format | [OpenAI.ResponseFormatText](#openairesponseformattext) or [OpenAI.ResponseFormatJsonSchema](#openairesponseformatjsonschema) or [OpenAI.ResponseFormatJsonObject](#openairesponseformatjsonobject) |  | No |  |
| seed | [OpenAI.integer](#openaiinteger) |  | No | 42 |
| temperature | [OpenAI.numeric](#openainumeric) |  | No | 1 |
| tools | array of [OpenAI.ChatCompletionTool](#openaichatcompletiontool) |  | No |  |
| top_p | [OpenAI.numeric](#openainumeric) |  | No | 1 |

### OpenAI.CreateEvalCustomDataSourceConfig

A CustomDataSourceConfig object that defines the schema for the data source used for the evaluation runs.
This schema is used to define the shape of the data that will be:
- Used to define your testing criteria and
- What data is required when creating a run

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include_sample_schema | boolean | Whether the eval should expect you to populate the sample namespace (ie, by generating responses off of your data source) | No |  |
| item_schema | object | The json schema for each row in the data source. | Yes |  |
| type | enum | The type of data source. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.CreateEvalJsonlRunDataSource

A JsonlRunDataSource object with that specifies a JSONL file that matches the eval

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) | Determines what populates the `item` namespace in the data source. | Yes |  |
| type | enum | The type of data source. Always `jsonl`.<br>Possible values: `jsonl` | Yes |  |

### OpenAI.CreateEvalLogsDataSourceConfig

A data source config which specifies the metadata property of your logs query.
This is usually metadata like `usecase=chatbot` or `prompt-version=v2`, etc.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Metadata filters for the logs data source. | No |  |
| type | enum | The type of data source. Always `logs`.<br>Possible values: `logs` | Yes |  |

### OpenAI.CreateEvalResponsesRunDataSource

A ResponsesRunDataSource object describing a model sampling configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | [OpenAI.CreateEvalResponsesRunDataSourceInputMessagesTemplate](#openaicreateevalresponsesrundatasourceinputmessagestemplate) or [OpenAI.CreateEvalResponsesRunDataSourceInputMessagesItemReference](#openaicreateevalresponsesrundatasourceinputmessagesitemreference) | Used when sampling from a model. Dictates the structure of the messages passed into the model. Can either be a reference to a prebuilt trajectory (ie, `item.input_trajectory`), or a template with variable references to the `item` namespace. | No |  |
| model | string | The name of the model to use for generating completions (e.g. "o3-mini"). | No |  |
| sampling_params | [OpenAI.CreateEvalResponsesRunDataSourceSamplingParams](#openaicreateevalresponsesrundatasourcesamplingparams) |  | No |  |
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) or [OpenAI.EvalResponsesSource](#openaievalresponsessource) | Determines what populates the `item` namespace in this run's data source. | Yes |  |
| type | enum | The type of run data source. Always `responses`.<br>Possible values: `responses` | Yes |  |

### OpenAI.CreateEvalResponsesRunDataSourceInputMessagesItemReference

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_reference | string |  | Yes |  |
| type | enum | <br>Possible values: `item_reference` | Yes |  |

### OpenAI.CreateEvalResponsesRunDataSourceInputMessagesTemplate

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| template | array of object or [OpenAI.EvalItem](#openaievalitem) |  | Yes |  |
| type | enum | <br>Possible values: `template` | Yes |  |

### OpenAI.CreateEvalResponsesRunDataSourceSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_completion_tokens | [OpenAI.integer](#openaiinteger) |  | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| seed | [OpenAI.integer](#openaiinteger) |  | No | 42 |
| temperature | [OpenAI.numeric](#openainumeric) |  | No | 1 |
| text | [OpenAI.CreateEvalResponsesRunDataSourceSamplingParamsText](#openaicreateevalresponsesrundatasourcesamplingparamstext) |  | No |  |
| tools | array of [OpenAI.Tool](#openaitool) |  | No |  |
| top_p | [OpenAI.numeric](#openainumeric) |  | No | 1 |

### OpenAI.CreateEvalResponsesRunDataSourceSamplingParamsText

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.TextResponseFormatConfiguration](#openaitextresponseformatconfiguration) | An object specifying the format that the model must output.<br>Configuring `{ "type": "json_schema" }` enables Structured Outputs,<br>which ensures the model will match your supplied JSON schema. Learn more in the<br><br>The default format is `{ "type": "text" }` with no additional options.<br>*Not recommended for gpt-4o and newer models:**<br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | No |  |

### OpenAI.CreateEvalStoredCompletionsDataSourceConfig

Deprecated in favor of LogsDataSourceConfig.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Metadata filters for the stored completions data source. | No |  |
| type | enum | The type of data source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### OpenAI.CreateFineTuningJobRequest


**Valid models:**

```
babbage-002
davinci-002
gpt-3.5-turbo
gpt-4o-mini
```

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [OpenAI.CreateFineTuningJobRequestHyperparameters](#openaicreatefinetuningjobrequesthyperparameters) |  | No |  |
| └─ batch_size | string or [OpenAI.integer](#openaiinteger) |  | No | auto |
| └─ learning_rate_multiplier | string or [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ n_epochs | string or [OpenAI.integer](#openaiinteger) |  | No | auto |
| integrations | array of [OpenAI.CreateFineTuningJobRequestIntegrations](#openaicreatefinetuningjobrequestintegrations) | A list of integrations to enable for your fine-tuning job. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string (see valid models below) | The name of the model to fine-tune. You can select one of the<br>  [supported models](https://platform.openai.com/docs/guides/fine-tuning#which-models-can-be-fine-tuned). | Yes |  |
| seed | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| suffix | string (nullable) | A string of up to 64 characters that will be added to your fine-tuned model name.<br>  For example, a `suffix` of "custom-model-name" would produce a model name like `ft:gpt-4o-mini:openai:custom-model-name:7p4lURel`.<br>**Constraints:** minLength: 1, maxLength: 64 | No |  |
| training_file | string | The ID of an uploaded file that contains training data.<br>  See [upload file](https://platform.openai.com/docs/api-reference/files/create) for how to upload a file.<br>  Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose `fine-tune`.<br>  The contents of the file should differ depending on if the model uses the [chat](https://platform.openai.com/docs/api-reference/fine-tuning/chat-input), [completions](https://platform.openai.com/docs/api-reference/fine-tuning/completions-input) format, or if the fine-tuning method uses the [preference](https://platform.openai.com/docs/api-reference/fine-tuning/preference-input) format.<br>  See the [fine-tuning guide](https://platform.openai.com/docs/guides/model-optimization) for more details. | Yes |  |
| validation_file | string (nullable) | The ID of an uploaded file that contains validation data.<br>  If you provide this file, the data is used to generate validation<br>  metrics periodically during fine-tuning. These metrics can be viewed in<br>  the fine-tuning results file.<br>  The same data should not be present in both train and validation files.<br>  Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`.<br>  See the [fine-tuning guide](https://platform.openai.com/docs/guides/model-optimization) for more details. | No |  |

### OpenAI.CreateFineTuningJobRequestHyperparameters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or [OpenAI.integer](#openaiinteger) |  | No |  |
| learning_rate_multiplier | string or [OpenAI.numeric](#openainumeric) |  | No |  |
| n_epochs | string or [OpenAI.integer](#openaiinteger) |  | No |  |

### OpenAI.CreateFineTuningJobRequestIntegrations

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `wandb` | Yes |  |
| wandb | [OpenAI.CreateFineTuningJobRequestIntegrationsWandb](#openaicreatefinetuningjobrequestintegrationswandb) |  | Yes |  |

### OpenAI.CreateFineTuningJobRequestIntegrationsWandb

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| entity | string (nullable) |  | No |  |
| name | string (nullable) |  | No |  |
| project | string |  | Yes |  |
| tags | array of string |  | No |  |

### OpenAI.CreateResponseStreamingResponse

**Type**: [OpenAI.ResponseAudioDeltaEvent](#openairesponseaudiodeltaevent) or [OpenAI.ResponseAudioTranscriptDeltaEvent](#openairesponseaudiotranscriptdeltaevent) or [OpenAI.ResponseCodeInterpreterCallCodeDeltaEvent](#openairesponsecodeinterpretercallcodedeltaevent) or [OpenAI.ResponseCodeInterpreterCallInProgressEvent](#openairesponsecodeinterpretercallinprogressevent) or [OpenAI.ResponseCodeInterpreterCallInterpretingEvent](#openairesponsecodeinterpretercallinterpretingevent) or [OpenAI.ResponseContentPartAddedEvent](#openairesponsecontentpartaddedevent) or [OpenAI.ResponseCreatedEvent](#openairesponsecreatedevent) or [OpenAI.ResponseErrorEvent](#openairesponseerrorevent) or [OpenAI.ResponseFileSearchCallInProgressEvent](#openairesponsefilesearchcallinprogressevent) or [OpenAI.ResponseFileSearchCallSearchingEvent](#openairesponsefilesearchcallsearchingevent) or [OpenAI.ResponseFunctionCallArgumentsDeltaEvent](#openairesponsefunctioncallargumentsdeltaevent) or [OpenAI.ResponseInProgressEvent](#openairesponseinprogressevent) or [OpenAI.ResponseFailedEvent](#openairesponsefailedevent) or [OpenAI.ResponseIncompleteEvent](#openairesponseincompleteevent) or [OpenAI.ResponseOutputItemAddedEvent](#openairesponseoutputitemaddedevent) or [OpenAI.ResponseReasoningSummaryPartAddedEvent](#openairesponsereasoningsummarypartaddedevent) or [OpenAI.ResponseReasoningSummaryTextDeltaEvent](#openairesponsereasoningsummarytextdeltaevent) or [OpenAI.ResponseReasoningTextDeltaEvent](#openairesponsereasoningtextdeltaevent) or [OpenAI.ResponseRefusalDeltaEvent](#openairesponserefusaldeltaevent) or [OpenAI.ResponseTextDeltaEvent](#openairesponsetextdeltaevent) or [OpenAI.ResponseWebSearchCallInProgressEvent](#openairesponsewebsearchcallinprogressevent) or [OpenAI.ResponseWebSearchCallSearchingEvent](#openairesponsewebsearchcallsearchingevent) or [OpenAI.ResponseImageGenCallGeneratingEvent](#openairesponseimagegencallgeneratingevent) or [OpenAI.ResponseImageGenCallInProgressEvent](#openairesponseimagegencallinprogressevent) or [OpenAI.ResponseImageGenCallPartialImageEvent](#openairesponseimagegencallpartialimageevent) or [OpenAI.ResponseMCPCallArgumentsDeltaEvent](#openairesponsemcpcallargumentsdeltaevent) or [OpenAI.ResponseMCPCallFailedEvent](#openairesponsemcpcallfailedevent) or [OpenAI.ResponseMCPCallInProgressEvent](#openairesponsemcpcallinprogressevent) or [OpenAI.ResponseMCPListToolsFailedEvent](#openairesponsemcplisttoolsfailedevent) or [OpenAI.ResponseMCPListToolsInProgressEvent](#openairesponsemcplisttoolsinprogressevent) or [OpenAI.ResponseOutputTextAnnotationAddedEvent](#openairesponseoutputtextannotationaddedevent) or [OpenAI.ResponseQueuedEvent](#openairesponsequeuedevent) or [OpenAI.ResponseCustomToolCallInputDeltaEvent](#openairesponsecustomtoolcallinputdeltaevent) or [OpenAI.ResponseAudioDoneEvent](#openairesponseaudiodoneevent) or [OpenAI.ResponseAudioTranscriptDoneEvent](#openairesponseaudiotranscriptdoneevent) or [OpenAI.ResponseCodeInterpreterCallCodeDoneEvent](#openairesponsecodeinterpretercallcodedoneevent) or [OpenAI.ResponseCodeInterpreterCallCompletedEvent](#openairesponsecodeinterpretercallcompletedevent) or [OpenAI.ResponseCompletedEvent](#openairesponsecompletedevent) or [OpenAI.ResponseContentPartDoneEvent](#openairesponsecontentpartdoneevent) or [OpenAI.ResponseFileSearchCallCompletedEvent](#openairesponsefilesearchcallcompletedevent) or [OpenAI.ResponseFunctionCallArgumentsDoneEvent](#openairesponsefunctioncallargumentsdoneevent) or [OpenAI.ResponseOutputItemDoneEvent](#openairesponseoutputitemdoneevent) or [OpenAI.ResponseReasoningSummaryPartDoneEvent](#openairesponsereasoningsummarypartdoneevent) or [OpenAI.ResponseReasoningSummaryTextDoneEvent](#openairesponsereasoningsummarytextdoneevent) or [OpenAI.ResponseReasoningTextDoneEvent](#openairesponsereasoningtextdoneevent) or [OpenAI.ResponseRefusalDoneEvent](#openairesponserefusaldoneevent) or [OpenAI.ResponseTextDoneEvent](#openairesponsetextdoneevent) or [OpenAI.ResponseWebSearchCallCompletedEvent](#openairesponsewebsearchcallcompletedevent) or [OpenAI.ResponseImageGenCallCompletedEvent](#openairesponseimagegencallcompletedevent) or [OpenAI.ResponseMCPCallArgumentsDoneEvent](#openairesponsemcpcallargumentsdoneevent) or [OpenAI.ResponseMCPCallCompletedEvent](#openairesponsemcpcallcompletedevent) or [OpenAI.ResponseMCPListToolsCompletedEvent](#openairesponsemcplisttoolscompletedevent) or [OpenAI.ResponseCustomToolCallInputDoneEvent](#openairesponsecustomtoolcallinputdoneevent)


### OpenAI.CustomGrammarFormatParam

A grammar defined by the user.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | string | The grammar definition. | Yes |  |
| syntax | [OpenAI.GrammarSyntax1](#openaigrammarsyntax1) |  | Yes |  |
| type | enum | Grammar format. Always `grammar`.<br>Possible values: `grammar` | Yes |  |

### OpenAI.CustomTextFormatParam

Unconstrained free-form text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Unconstrained text format. Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.CustomToolParam

A custom tool that processes input using a specified format. Learn more about   [custom tools](https://platform.openai.com/docs/guides/function-calling#custom-tools)

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | Optional description of the custom tool, used to provide more context. | No |  |
| format | [OpenAI.CustomToolParamFormat](#openaicustomtoolparamformat) | The input format for the custom tool. Default is unconstrained text. | No |  |
| └─ type | [OpenAI.CustomToolParamFormatType](#openaicustomtoolparamformattype) |  | Yes |  |
| name | string | The name of the custom tool, used to identify it in tool calls. | Yes |  |
| type | enum | The type of the custom tool. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.CustomToolParamFormat

The input format for the custom tool. Default is unconstrained text.


### Discriminator for OpenAI.CustomToolParamFormat

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `text` | [OpenAI.CustomTextFormatParam](#openaicustomtextformatparam) |
| `grammar` | [OpenAI.CustomGrammarFormatParam](#openaicustomgrammarformatparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.CustomToolParamFormatType](#openaicustomtoolparamformattype) |  | Yes |  |

### OpenAI.CustomToolParamFormatType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`grammar` |

### OpenAI.DeletedConversationResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `conversation.deleted` | Yes |  |

### OpenAI.DetailEnum

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `low`<br>`high`<br>`auto` |

### OpenAI.DoubleClickAction

A double click action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a double click action, this property is always set to `double_click`.<br>Possible values: `double_click` | Yes |  |
| x | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| y | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.Drag

A drag action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| path | array of [OpenAI.DragPoint](#openaidragpoint) | An array of coordinates representing the path of the drag action. Coordinates will appear as an array<br>  of objects, eg<br>  ```<br>  [<br>    { x: 100, y: 200 },<br>    { x: 200, y: 300 }<br>  ]<br>  ``` | Yes |  |
| type | enum | Specifies the event type. For a drag action, this property is<br>  always set to `drag`.<br>Possible values: `drag` | Yes |  |

### OpenAI.DragPoint

An x/y coordinate pair, e.g. `{ x: 100, y: 200 }`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| x | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| y | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.EasyInputMessage

A message input to the model with a role indicating instruction following
hierarchy. Instructions given with the `developer` or `system` role take
precedence over instructions given with the `user` role. Messages with the
`assistant` role are presumed to have been generated by the model in previous
interactions.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or [OpenAI.InputMessageContentList](#openaiinputmessagecontentlist) | Text, image, or audio input to the model, used to generate a response.<br>  Can also contain previous assistant responses. | Yes |  |
| role | enum | The role of the message input. One of `user`, `assistant`, `system`, or<br>  `developer`.<br>Possible values: `user`, `assistant`, `system`, `developer` | Yes |  |
| status | enum | The status of item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the message input. Always `message`.<br>Possible values: `message` | Yes |  |

### OpenAI.Error

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| additionalInfo | object |  | No |  |
| code | string (nullable) |  | Yes |  |
| debugInfo | object |  | No |  |
| details | array of [OpenAI.Error](#openaierror) |  | No |  |
| message | string |  | Yes |  |
| param | string (nullable) |  | No |  |
| type | string |  | No |  |

### OpenAI.EvalApiError

An object representing an error response from the Eval API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The error code. | Yes |  |
| message | string | The error message. | Yes |  |

### OpenAI.EvalGraderLabelModel

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array of [OpenAI.EvalItem](#openaievalitem) |  | Yes |  |
| labels | array of string | The labels to assign to each item in the evaluation. | Yes |  |
| model | string | The model to use for the evaluation. Must support structured outputs. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| passing_labels | array of string | The labels that indicate a passing result. Must be a subset of labels. | Yes |  |
| type | enum | The object type, which is always `label_model`.<br>Possible values: `label_model` | Yes |  |

### OpenAI.EvalGraderPython

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_tag | string | The image tag to use for the python script. | No |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | [OpenAI.numeric](#openainumeric) |  | No |  |
| source | string | The source code of the python script. | Yes |  |
| type | enum | The object type, which is always `python`.<br>Possible values: `python` | Yes |  |

### OpenAI.EvalGraderScoreModel

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array of [OpenAI.EvalItem](#openaievalitem) | The input messages evaluated by the grader. Supports text, output text, input image, and input audio content blocks, and may include template strings. | Yes |  |
| model | string | The model to use for the evaluation. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | [OpenAI.numeric](#openainumeric) |  | No |  |
| range | array of [OpenAI.numeric](#openainumeric) | The range of the score. Defaults to `[0, 1]`. | No |  |
| sampling_params | [OpenAI.EvalGraderScoreModelSamplingParams](#openaievalgraderscoremodelsamplingparams) |  | No |  |
| └─ max_completions_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| └─ seed | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| type | enum | The object type, which is always `score_model`.<br>Possible values: `score_model` | Yes |  |

### OpenAI.EvalGraderScoreModelSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_completions_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| seed | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No |  |
| top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |

### OpenAI.EvalGraderStringCheck

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string | The input text. This may include template strings. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | Yes |  |
| reference | string | The reference text. This may include template strings. | Yes |  |
| type | enum | The object type, which is always `string_check`.<br>Possible values: `string_check` | Yes |  |

### OpenAI.EvalGraderTextSimilarity

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evaluation_metric | enum | The evaluation metric to use. One of `cosine`, `fuzzy_match`, `bleu`,<br>  `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`,<br>  or `rouge_l`.<br>Possible values: `cosine`, `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | Yes |  |
| input | string | The text being graded. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| reference | string | The text being graded against. | Yes |  |
| type | enum | The type of grader.<br>Possible values: `text_similarity` | Yes |  |

### OpenAI.EvalItem

A message input to the model with a role indicating instruction following
hierarchy. Instructions given with the `developer` or `system` role take
precedence over instructions given with the `user` role. Messages with the
`assistant` role are presumed to have been generated by the model in previous
interactions.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | [OpenAI.EvalItemContent](#openaievalitemcontent) | Inputs to the model - can contain template strings. Supports text, output text, input images, and input audio, either as a single item or an array of items. | Yes |  |
| role | enum | The role of the message input. One of `user`, `assistant`, `system`, or<br>  `developer`.<br>Possible values: `user`, `assistant`, `system`, `developer` | Yes |  |
| type | enum | The type of the message input. Always `message`.<br>Possible values: `message` | No |  |

### OpenAI.EvalItemContent

Inputs to the model - can contain template strings. Supports text, output text, input images, and input audio, either as a single item or an array of items.

**Type**: [OpenAI.EvalItemContentItem](#openaievalitemcontentitem) or [OpenAI.EvalItemContentArray](#openaievalitemcontentarray)

Inputs to the model - can contain template strings. Supports text, output text, input images, and input audio, either as a single item or an array of items.


### OpenAI.EvalItemContentArray

A list of inputs, each of which may be either an input text, output text, input
image, or input audio object.

**Array of**: [OpenAI.EvalItemContentItem](#openaievalitemcontentitem)


### OpenAI.EvalItemContentItem

A single content item: input text, output text, input image, or input audio.

**Type**: [OpenAI.EvalItemContentText](#openaievalitemcontenttext) or [OpenAI.EvalItemContentItemObject](#openaievalitemcontentitemobject)

A single content item: input text, output text, input image, or input audio.


### OpenAI.EvalItemContentItemObject

A single content item: input text, output text, input image, or input audio.


### Discriminator for OpenAI.EvalItemContentItemObject

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `output_text` | [OpenAI.EvalItemContentOutputText](#openaievalitemcontentoutputtext) |
| `input_image` | [OpenAI.EvalItemInputImage](#openaievaliteminputimage) |
| `input_audio` | [OpenAI.InputAudio](#openaiinputaudio) |
| `input_text` | [OpenAI.EvalItemContentItemObjectInputTextContent](#openaievalitemcontentitemobjectinputtextcontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.EvalItemContentItemObjectType](#openaievalitemcontentitemobjecttype) |  | Yes |  |

### OpenAI.EvalItemContentItemObjectInputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.EvalItemContentItemObjectType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `input_text`<br>`output_text`<br>`input_image`<br>`input_audio` |

### OpenAI.EvalItemContentOutputText

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.EvalItemContentText

A text input to the model.

**Type**: string


### OpenAI.EvalItemInputImage

An image input block used within EvalItem content arrays.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | string | The detail level of the image to be sent to the model. One of `high`, `low`, or `auto`. Defaults to `auto`. | No |  |
| image_url | string | The URL of the image input. | Yes |  |
| type | enum | The type of the image input. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.EvalJsonlFileContentSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.EvalJsonlFileContentSourceContent](#openaievaljsonlfilecontentsourcecontent) | The content of the jsonl file. | Yes |  |
| type | enum | The type of jsonl source. Always `file_content`.<br>Possible values: `file_content` | Yes |  |

### OpenAI.EvalJsonlFileContentSourceContent

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item | object |  | Yes |  |
| sample | object |  | No |  |

### OpenAI.EvalJsonlFileIdSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The identifier of the file. | Yes |  |
| type | enum | The type of jsonl source. Always `file_id`.<br>Possible values: `file_id` | Yes |  |

### OpenAI.EvalResponsesSource

A EvalResponsesSource object describing a run data source configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_after | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| created_before | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| instructions_search | string (nullable) |  | No |  |
| metadata | object (nullable) |  | No |  |
| model | string (nullable) |  | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) (nullable) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No |  |
| tools | array of string |  | No |  |
| top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No |  |
| type | enum | The type of run data source. Always `responses`.<br>Possible values: `responses` | Yes |  |
| users | array of string |  | No |  |

### OpenAI.EvalRunOutputItemSample

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | [OpenAI.EvalApiError](#openaievalapierror) | An object representing an error response from the Eval API. | Yes |  |
| finish_reason | string |  | Yes |  |
| input | array of [EvalRunOutputItemSampleInput](#evalrunoutputitemsampleinput) |  | Yes |  |
| max_completion_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| model | string |  | Yes |  |
| output | array of [EvalRunOutputItemSampleOutput](#evalrunoutputitemsampleoutput) |  | Yes |  |
| seed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| temperature | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| top_p | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| usage | [OpenAI.EvalRunOutputItemSampleUsage](#openaievalrunoutputitemsampleusage) |  | Yes |  |

### OpenAI.EvalRunOutputItemSampleUsage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cached_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| completion_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| prompt_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| total_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.EvalRunPerModelUsage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cached_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| completion_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| invocation_count | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| model_name | string |  | Yes |  |
| prompt_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| total_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.EvalRunPerTestingCriteriaResults

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| failed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| passed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| testing_criteria | string |  | Yes |  |

### OpenAI.EvalRunResultCounts

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| errored | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| failed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| passed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| total | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.EvalStoredCompletionsSource

A StoredCompletionsRunDataSource configuration describing a set of filters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_after | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| created_before | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| limit | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| model | string (nullable) |  | No |  |
| type | enum | The type of source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### OpenAI.FileCitationBody

A citation to a file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The ID of the file. | Yes |  |
| filename | string | The filename of the file cited. | Yes |  |
| index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the file citation. Always `file_citation`.<br>Possible values: `file_citation` | Yes |  |

### OpenAI.FilePath

A path to a file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The ID of the file. | Yes |  |
| index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the file path. Always `file_path`.<br>Possible values: `file_path` | Yes |  |

### OpenAI.FileSearchTool

A tool that searches for relevant content from uploaded files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | [OpenAI.Filters](#openaifilters) (nullable) |  | No |  |
| max_num_results | [OpenAI.integer](#openaiinteger) |  | No |  |
| ranking_options | [OpenAI.RankingOptions](#openairankingoptions) |  | No |  |
| └─ hybrid_search | [OpenAI.HybridSearchOptions](#openaihybridsearchoptions) | Weights that control how reciprocal rank fusion balances semantic embedding matches versus sparse keyword matches when hybrid search is enabled. | No |  |
| └─ ranker | [OpenAI.RankerVersionType](#openairankerversiontype) | The ranker to use for the file search. | No |  |
| └─ score_threshold | [OpenAI.numeric](#openainumeric) | The score threshold for the file search, a number between 0 and 1. Numbers closer to 1 will attempt to return only the most relevant results, but may return fewer results. | No |  |
| type | enum | The type of the file search tool. Always `file_search`.<br>Possible values: `file_search` | Yes |  |
| vector_store_ids | array of string | The IDs of the vector stores to search. | Yes |  |

### OpenAI.FileSearchToolCallResults

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard. Keys are strings<br>with a maximum length of 64 characters. Values are strings with a maximum<br>length of 512 characters, booleans, or numbers. | No |  |
| file_id | string |  | No |  |
| filename | string |  | No |  |
| score | number |  | No |  |
| text | string |  | No |  |

### OpenAI.Filters

**Type**: [OpenAI.ComparisonFilter](#openaicomparisonfilter) or [OpenAI.CompoundFilter](#openaicompoundfilter)


### OpenAI.FineTuneDPOHyperparameters

The hyperparameters used for the DPO fine-tuning job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or [OpenAI.integer](#openaiinteger) | Number of examples in each batch. A larger batch size means that model parameters are updated less frequently, but with lower variance. | No |  |
| beta | string or [OpenAI.numeric](#openainumeric) | The beta value for the DPO method. A higher beta value will increase the weight of the penalty between the policy and reference model. | No |  |
| learning_rate_multiplier | string or [OpenAI.numeric](#openainumeric) | Scaling factor for the learning rate. A smaller learning rate may be useful to avoid overfitting. | No |  |
| n_epochs | string or [OpenAI.integer](#openaiinteger) | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. | No |  |

### OpenAI.FineTuneDPOMethod

Configuration for the DPO fine-tuning method.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [OpenAI.FineTuneDPOHyperparameters](#openaifinetunedpohyperparameters) | The hyperparameters used for the DPO fine-tuning job. | No |  |

### OpenAI.FineTuneMethod

The method used for fine-tuning.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| dpo | [OpenAI.FineTuneDPOMethod](#openaifinetunedpomethod) | Configuration for the DPO fine-tuning method. | No |  |
| reinforcement | [OpenAI.FineTuneReinforcementMethod](#openaifinetunereinforcementmethod) | Configuration for the reinforcement fine-tuning method. | No |  |
| supervised | [OpenAI.FineTuneSupervisedMethod](#openaifinetunesupervisedmethod) | Configuration for the supervised fine-tuning method. | No |  |
| type | enum | The type of method. Is either `supervised`, `dpo`, or `reinforcement`.<br>Possible values: `supervised`, `dpo`, `reinforcement` | Yes |  |

### OpenAI.FineTuneReinforcementHyperparameters

The hyperparameters used for the reinforcement fine-tuning job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or [OpenAI.integer](#openaiinteger) | Number of examples in each batch. A larger batch size means that model parameters are updated less frequently, but with lower variance. | No |  |
| compute_multiplier | string or [OpenAI.numeric](#openainumeric) | Multiplier on amount of compute used for exploring search space during training. | No |  |
| eval_interval | string or [OpenAI.integer](#openaiinteger) | The number of training steps between evaluation runs. | No |  |
| eval_samples | string or [OpenAI.integer](#openaiinteger) | Number of evaluation samples to generate per training step. | No |  |
| learning_rate_multiplier | string or [OpenAI.numeric](#openainumeric) | Scaling factor for the learning rate. A smaller learning rate may be useful to avoid overfitting. | No |  |
| n_epochs | string or [OpenAI.integer](#openaiinteger) | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. | No |  |
| reasoning_effort | enum | Level of reasoning effort.<br>Possible values: `default`, `low`, `medium`, `high` | No |  |

### OpenAI.FineTuneReinforcementMethod

Configuration for the reinforcement fine-tuning method.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | [OpenAI.GraderStringCheck](#openaigraderstringcheck) or [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) or [OpenAI.GraderPython](#openaigraderpython) or [OpenAI.GraderScoreModel](#openaigraderscoremodel) or [OpenAI.GraderMulti](#openaigradermulti) | The grader used for the fine-tuning job. | Yes |  |
| hyperparameters | [OpenAI.FineTuneReinforcementHyperparameters](#openaifinetunereinforcementhyperparameters) | The hyperparameters used for the reinforcement fine-tuning job. | No |  |

### OpenAI.FineTuneSupervisedHyperparameters

The hyperparameters used for the fine-tuning job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or [OpenAI.integer](#openaiinteger) | Number of examples in each batch. A larger batch size means that model parameters are updated less frequently, but with lower variance. | No |  |
| learning_rate_multiplier | string or [OpenAI.numeric](#openainumeric) | Scaling factor for the learning rate. A smaller learning rate may be useful to avoid overfitting. | No |  |
| n_epochs | string or [OpenAI.integer](#openaiinteger) | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. | No |  |

### OpenAI.FineTuneSupervisedMethod

Configuration for the supervised fine-tuning method.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [OpenAI.FineTuneSupervisedHyperparameters](#openaifinetunesupervisedhyperparameters) | The hyperparameters used for the fine-tuning job. | No |  |

### OpenAI.FineTuningIntegration

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the integration being enabled for the fine-tuning job<br>Possible values: `wandb` | Yes |  |
| wandb | [OpenAI.FineTuningIntegrationWandb](#openaifinetuningintegrationwandb) |  | Yes |  |
| └─ entity | string (nullable) |  | No |  |
| └─ name | string (nullable) |  | No |  |
| └─ project | string |  | Yes |  |
| └─ tags | array of string |  | No |  |

### OpenAI.FineTuningIntegrationWandb

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| entity | string (nullable) |  | No |  |
| name | string (nullable) |  | No |  |
| project | string |  | Yes |  |
| tags | array of string |  | No |  |

### OpenAI.FineTuningJob

The `fine_tuning.job` object represents a fine-tuning job that has been created through the API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the fine-tuning job was created. | Yes |  |
| error | [OpenAI.FineTuningJobError](#openaifinetuningjoberror) (nullable) |  | Yes |  |
| └─ code | string |  | Yes |  |
| └─ message | string |  | Yes |  |
| └─ param | string (nullable) |  | Yes |  |
| estimated_finish | integer |  | No |  |
| fine_tuned_model | string (nullable) |  | Yes |  |
| finished_at | integer |  | Yes |  |
| hyperparameters | [OpenAI.FineTuningJobHyperparameters](#openaifinetuningjobhyperparameters) |  | Yes |  |
| └─ batch_size | string or [OpenAI.integer](#openaiinteger) |  | No | auto |
| └─ learning_rate_multiplier | string or [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ n_epochs | string or [OpenAI.integer](#openaiinteger) |  | No | auto |
| id | string | The object identifier, which can be referenced in the API endpoints. | Yes |  |
| integrations | array of [OpenAI.FineTuningIntegration](#openaifinetuningintegration) |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string | The base model that is being fine-tuned. | Yes |  |
| object | enum | The object type, which is always "fine_tuning.job".<br>Possible values: `fine_tuning.job` | Yes |  |
| organization_id | string | The organization that owns the fine-tuning job. | Yes |  |
| result_files | array of string | The compiled results file ID(s) for the fine-tuning job. You can retrieve the results with the [Files API](https://platform.openai.com/docs/api-reference/files/retrieve-contents). | Yes |  |
| seed | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| status | enum | The current status of the fine-tuning job, which can be either `validating_files`, `queued`, `running`, `succeeded`, `failed`, or `cancelled`.<br>Possible values: `validating_files`, `queued`, `running`, `succeeded`, `failed`, `cancelled` | Yes |  |
| trained_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| training_file | string | The file ID used for training. You can retrieve the training data with the [Files API](https://platform.openai.com/docs/api-reference/files/retrieve-contents). | Yes |  |
| validation_file | string (nullable) |  | Yes |  |

### OpenAI.FineTuningJobCheckpoint

The `fine_tuning.job.checkpoint` object represents a model checkpoint for a fine-tuning job that is ready to use.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the checkpoint was created. | Yes |  |
| fine_tuned_model_checkpoint | string | The name of the fine-tuned checkpoint model that is created. | Yes |  |
| fine_tuning_job_id | string | The name of the fine-tuning job that this checkpoint was created from. | Yes |  |
| id | string | The checkpoint identifier, which can be referenced in the API endpoints. | Yes |  |
| metrics | [OpenAI.FineTuningJobCheckpointMetrics](#openaifinetuningjobcheckpointmetrics) |  | Yes |  |
| └─ full_valid_loss | [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ full_valid_mean_token_accuracy | [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ step | [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ train_loss | [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ train_mean_token_accuracy | [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ valid_loss | [OpenAI.numeric](#openainumeric) |  | No |  |
| └─ valid_mean_token_accuracy | [OpenAI.numeric](#openainumeric) |  | No |  |
| object | enum | The object type, which is always "fine_tuning.job.checkpoint".<br>Possible values: `fine_tuning.job.checkpoint` | Yes |  |
| step_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.FineTuningJobCheckpointMetrics

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| full_valid_loss | [OpenAI.numeric](#openainumeric) |  | No |  |
| full_valid_mean_token_accuracy | [OpenAI.numeric](#openainumeric) |  | No |  |
| step | [OpenAI.numeric](#openainumeric) |  | No |  |
| train_loss | [OpenAI.numeric](#openainumeric) |  | No |  |
| train_mean_token_accuracy | [OpenAI.numeric](#openainumeric) |  | No |  |
| valid_loss | [OpenAI.numeric](#openainumeric) |  | No |  |
| valid_mean_token_accuracy | [OpenAI.numeric](#openainumeric) |  | No |  |

### OpenAI.FineTuningJobError

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string |  | Yes |  |
| message | string |  | Yes |  |
| param | string (nullable) |  | Yes |  |

### OpenAI.FineTuningJobEvent

Fine-tuning job event object

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the fine-tuning job was created. | Yes |  |
| data | [OpenAI.FineTuningJobEventData](#openaifinetuningjobeventdata) |  | No |  |
| id | string | The object identifier. | Yes |  |
| level | enum | The log level of the event.<br>Possible values: `info`, `warn`, `error` | Yes |  |
| message | string | The message of the event. | Yes |  |
| object | enum | The object type, which is always "fine_tuning.job.event".<br>Possible values: `fine_tuning.job.event` | Yes |  |
| type | enum | The type of event.<br>Possible values: `message`, `metrics` | No |  |

### OpenAI.FineTuningJobEventData

**Type**: object


### OpenAI.FineTuningJobHyperparameters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or [OpenAI.integer](#openaiinteger) |  | No |  |
| learning_rate_multiplier | string or [OpenAI.numeric](#openainumeric) |  | No |  |
| n_epochs | string or [OpenAI.integer](#openaiinteger) |  | No |  |

### OpenAI.FunctionAndCustomToolCallOutput


### Discriminator for OpenAI.FunctionAndCustomToolCallOutput

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `input_text` | [OpenAI.FunctionAndCustomToolCallOutputInputTextContent](#openaifunctionandcustomtoolcalloutputinputtextcontent) |
| `input_image` | [OpenAI.FunctionAndCustomToolCallOutputInputImageContent](#openaifunctionandcustomtoolcalloutputinputimagecontent) |
| `input_file` | [OpenAI.FunctionAndCustomToolCallOutputInputFileContent](#openaifunctionandcustomtoolcalloutputinputfilecontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.FunctionAndCustomToolCallOutputType](#openaifunctionandcustomtoolcalloutputtype) |  | Yes |  |

### OpenAI.FunctionAndCustomToolCallOutputInputFileContent

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string | The content of the file to be sent to the model. | No |  |
| file_id | string (nullable) |  | No |  |
| file_url | string | The URL of the file to be sent to the model. | No |  |
| filename | string | The name of the file to be sent to the model. | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.FunctionAndCustomToolCallOutputInputImageContent

An image input to the model. Learn about [image inputs](https://platform.openai.com/docs/guides/vision).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | [OpenAI.ImageDetail](#openaiimagedetail) |  | Yes |  |
| file_id | string (nullable) |  | No |  |
| image_url | string |  | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.FunctionAndCustomToolCallOutputInputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.FunctionAndCustomToolCallOutputType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `input_text`<br>`input_image`<br>`input_file` |

### OpenAI.FunctionCallItemStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`incomplete` |

### OpenAI.FunctionObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| name | string | The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64. | Yes |  |
| parameters | [OpenAI.FunctionParameters](#openaifunctionparameters) | The parameters the functions accepts, described as a JSON Schema object. See the [guide](https://platform.openai.com/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.<br>Omitting `parameters` defines a function with an empty parameter list. | No |  |
| strict | boolean (nullable) |  | No |  |

### OpenAI.FunctionParameters

The parameters the functions accepts, described as a JSON Schema object. See the [guide](https://platform.openai.com/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.
Omitting `parameters` defines a function with an empty parameter list.

**Type**: object


### OpenAI.FunctionShellAction

Execute a shell command.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| commands | array of string |  | Yes |  |
| max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| timeout_ms | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |

### OpenAI.FunctionShellActionParam

Commands and limits describing how to run the shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| commands | array of string | Ordered shell commands for the execution environment to run. | Yes |  |
| max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| timeout_ms | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |

### OpenAI.FunctionShellCallItemStatus

Status values reported for shell tool calls.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`incomplete` |

### OpenAI.FunctionShellCallOutputContent

The content of a shell tool call output that was emitted.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_by | string | The identifier of the actor that created the item. | No |  |
| outcome | [OpenAI.FunctionShellCallOutputOutcome](#openaifunctionshellcalloutputoutcome) | Represents either an exit outcome (with an exit code) or a timeout outcome for a shell call output chunk. | Yes |  |
| └─ type | [OpenAI.FunctionShellCallOutputOutcomeType](#openaifunctionshellcalloutputoutcometype) |  | Yes |  |
| stderr | string | The standard error output that was captured. | Yes |  |
| stdout | string | The standard output that was captured. | Yes |  |

### OpenAI.FunctionShellCallOutputContentParam

Captured stdout and stderr for a portion of a shell tool call output.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| outcome | [OpenAI.FunctionShellCallOutputOutcomeParam](#openaifunctionshellcalloutputoutcomeparam) | The exit or timeout outcome associated with this shell call. | Yes |  |
| └─ type | [OpenAI.FunctionShellCallOutputOutcomeParamType](#openaifunctionshellcalloutputoutcomeparamtype) |  | Yes |  |
| stderr | string | Captured stderr output for the shell call.<br>**Constraints:** maxLength: 10485760 | Yes |  |
| stdout | string | Captured stdout output for the shell call.<br>**Constraints:** maxLength: 10485760 | Yes |  |

### OpenAI.FunctionShellCallOutputExitOutcome

Indicates that the shell commands finished and returned an exit code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| exit_code | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The outcome type. Always `exit`.<br>Possible values: `exit` | Yes |  |

### OpenAI.FunctionShellCallOutputExitOutcomeParam

Indicates that the shell commands finished and returned an exit code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| exit_code | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The outcome type. Always `exit`.<br>Possible values: `exit` | Yes |  |

### OpenAI.FunctionShellCallOutputOutcome

Represents either an exit outcome (with an exit code) or a timeout outcome for a shell call output chunk.


### Discriminator for OpenAI.FunctionShellCallOutputOutcome

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `timeout` | [OpenAI.FunctionShellCallOutputTimeoutOutcome](#openaifunctionshellcalloutputtimeoutoutcome) |
| `exit` | [OpenAI.FunctionShellCallOutputExitOutcome](#openaifunctionshellcalloutputexitoutcome) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.FunctionShellCallOutputOutcomeType](#openaifunctionshellcalloutputoutcometype) |  | Yes |  |

### OpenAI.FunctionShellCallOutputOutcomeParam

The exit or timeout outcome associated with this shell call.


### Discriminator for OpenAI.FunctionShellCallOutputOutcomeParam

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `timeout` | [OpenAI.FunctionShellCallOutputTimeoutOutcomeParam](#openaifunctionshellcalloutputtimeoutoutcomeparam) |
| `exit` | [OpenAI.FunctionShellCallOutputExitOutcomeParam](#openaifunctionshellcalloutputexitoutcomeparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.FunctionShellCallOutputOutcomeParamType](#openaifunctionshellcalloutputoutcomeparamtype) |  | Yes |  |

### OpenAI.FunctionShellCallOutputOutcomeParamType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `timeout`<br>`exit` |

### OpenAI.FunctionShellCallOutputOutcomeType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `timeout`<br>`exit` |

### OpenAI.FunctionShellCallOutputTimeoutOutcome

Indicates that the shell call exceeded its configured time limit.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The outcome type. Always `timeout`.<br>Possible values: `timeout` | Yes |  |

### OpenAI.FunctionShellCallOutputTimeoutOutcomeParam

Indicates that the shell call exceeded its configured time limit.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The outcome type. Always `timeout`.<br>Possible values: `timeout` | Yes |  |

### OpenAI.FunctionShellToolParam

A tool that allows the model to execute shell commands.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the shell tool. Always `shell`.<br>Possible values: `shell` | Yes |  |

### OpenAI.FunctionTool

Defines a function in your own code the model can choose to call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string (nullable) |  | No |  |
| name | string | The name of the function to call. | Yes |  |
| parameters | object (nullable) |  | Yes |  |
| strict | boolean (nullable) |  | Yes |  |
| type | enum | The type of the function tool. Always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.GraderLabelModel

A LabelModelGrader object which uses a model to assign labels to each item
in the evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array of [OpenAI.EvalItem](#openaievalitem) |  | Yes |  |
| labels | array of string | The labels to assign to each item in the evaluation. | Yes |  |
| model | string | The model to use for the evaluation. Must support structured outputs. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| passing_labels | array of string | The labels that indicate a passing result. Must be a subset of labels. | Yes |  |
| type | enum | The object type, which is always `label_model`.<br>Possible values: `label_model` | Yes |  |

### OpenAI.GraderMulti

A MultiGrader object combines the output of multiple graders to produce a single score.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| calculate_output | string | A formula to calculate the output based on grader results. | Yes |  |
| graders | [OpenAI.GraderStringCheck](#openaigraderstringcheck) or [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) or [OpenAI.GraderPython](#openaigraderpython) or [OpenAI.GraderScoreModel](#openaigraderscoremodel) or [OpenAI.GraderLabelModel](#openaigraderlabelmodel) |  | Yes |  |
| name | string | The name of the grader. | Yes |  |
| type | enum | The object type, which is always `multi`.<br>Possible values: `multi` | Yes |  |

### OpenAI.GraderPython

A PythonGrader object that runs a python script on the input.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_tag | string | The image tag to use for the python script. | No |  |
| name | string | The name of the grader. | Yes |  |
| source | string | The source code of the python script. | Yes |  |
| type | enum | The object type, which is always `python`.<br>Possible values: `python` | Yes |  |

### OpenAI.GraderScoreModel

A ScoreModelGrader object that uses a model to assign a score to the input.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array of [OpenAI.EvalItem](#openaievalitem) | The input messages evaluated by the grader. Supports text, output text, input image, and input audio content blocks, and may include template strings. | Yes |  |
| model | string | The model to use for the evaluation. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| range | array of [OpenAI.numeric](#openainumeric) | The range of the score. Defaults to `[0, 1]`. | No |  |
| sampling_params | [OpenAI.EvalGraderScoreModelSamplingParams](#openaievalgraderscoremodelsamplingparams) |  | No |  |
| └─ max_completions_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| └─ seed | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| type | enum | The object type, which is always `score_model`.<br>Possible values: `score_model` | Yes |  |

### OpenAI.GraderStringCheck

A StringCheckGrader object that performs a string comparison between input and reference using a specified operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string | The input text. This may include template strings. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | Yes |  |
| reference | string | The reference text. This may include template strings. | Yes |  |
| type | enum | The object type, which is always `string_check`.<br>Possible values: `string_check` | Yes |  |

### OpenAI.GraderTextSimilarity

A TextSimilarityGrader object which grades text based on similarity metrics.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evaluation_metric | enum | The evaluation metric to use. One of `cosine`, `fuzzy_match`, `bleu`,<br>  `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`,<br>  or `rouge_l`.<br>Possible values: `cosine`, `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | Yes |  |
| input | string | The text being graded. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| reference | string | The text being graded against. | Yes |  |
| type | enum | The type of grader.<br>Possible values: `text_similarity` | Yes |  |

### OpenAI.GrammarSyntax1

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `lark`<br>`regex` |

### OpenAI.HybridSearchOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| embedding_weight | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| text_weight | [OpenAI.numeric](#openainumeric) |  | Yes |  |

### OpenAI.ImageDetail

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `low`<br>`high`<br>`auto` |

### OpenAI.ImageGenTool

A tool that generates images using the GPT image models.


**Valid models:**

```
gpt-image-1
gpt-image-1-mini
```

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Background type for the generated image. One of `transparent`,<br>  `opaque`, or `auto`. Default: `auto`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| input_fidelity | [OpenAI.InputFidelity](#openaiinputfidelity) (nullable) | Control how much effort the model will exert to match the style and features, especially facial features, of input images. This parameter is only supported for `gpt-image-1`. Unsupported for `gpt-image-1-mini`. Supports `high` and `low`. Defaults to `low`. | No |  |
| input_image_mask | [OpenAI.ImageGenToolInputImageMask](#openaiimagegentoolinputimagemask) |  | No |  |
| └─ file_id | string |  | No |  |
| └─ image_url | string |  | No |  |
| model | string (see valid models below) |  | No |  |
| moderation | enum | Moderation level for the generated image. Default: `auto`.<br>Possible values: `auto`, `low` | No |  |
| output_compression | [OpenAI.integer](#openaiinteger) |  | No | 100 |
| output_format | enum | The output format of the generated image. One of `png`, `webp`, or<br>  `jpeg`. Default: `png`.<br>Possible values: `png`, `webp`, `jpeg` | No |  |
| partial_images | [OpenAI.integer](#openaiinteger) |  | No |  |
| quality | enum | The quality of the generated image. One of `low`, `medium`, `high`,<br>  or `auto`. Default: `auto`.<br>Possible values: `low`, `medium`, `high`, `auto` | No |  |
| size | enum | The size of the generated image. One of `1024x1024`, `1024x1536`,<br>  `1536x1024`, or `auto`. Default: `auto`.<br>Possible values: `1024x1024`, `1024x1536`, `1536x1024`, `auto` | No |  |
| type | enum | The type of the image generation tool. Always `image_generation`.<br>Possible values: `image_generation` | Yes |  |

### OpenAI.ImageGenToolInputImageMask

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string |  | No |  |
| image_url | string |  | No |  |

### OpenAI.IncludeEnum

Specify additional output data to include in the model response. Currently supported values are:
- `web_search_call.action.sources`: Include the sources of the web search tool call.
- `code_interpreter_call.outputs`: Includes the outputs of python code execution in code interpreter tool call items.
- `computer_call_output.output.image_url`: Include image urls from the computer call output.
- `file_search_call.results`: Include the search results of the file search tool call.
- `message.input_image.image_url`: Include image urls from the input message.
- `message.output_text.logprobs`: Include logprobs with assistant messages.
- `reasoning.encrypted_content`: Includes an encrypted version of reasoning tokens in reasoning item outputs. This enables reasoning items to be used in multi-turn conversations when using the Responses API statelessly (like when the `store` parameter is set to `false`, or when an organization is enrolled in the zero data retention program).

| Property | Value |
|----------|-------|
| **Description** | Specify additional output data to include in the model response. Currently supported values are:
- `web_search_call.action.sources`: Include the sources of the web search tool call.
- `code_interpreter_call.outputs`: Includes the outputs of python code execution in code interpreter tool call items.
- `computer_call_output.output.image_url`: Include image urls from the computer call output.
- `file_search_call.results`: Include the search results of the file search tool call.
- `message.input_image.image_url`: Include image urls from the input message.
- `message.output_text.logprobs`: Include logprobs with assistant messages.
- `reasoning.encrypted_content`: Includes an encrypted version of reasoning tokens in reasoning item outputs. This enables reasoning items to be used in multi-turn conversations when using the Responses API statelessly (like when the `store` parameter is set to `false`, or when an organization is enrolled in the zero data retention program). |
| **Type** | string |
| **Values** | `file_search_call.results`<br>`web_search_call.results`<br>`web_search_call.action.sources`<br>`message.input_image.image_url`<br>`computer_call_output.output.image_url`<br>`code_interpreter_call.outputs`<br>`reasoning.encrypted_content`<br>`message.output_text.logprobs`<br>`memory_search_call.results` |

### OpenAI.InputAudio

An audio input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_audio | [OpenAI.InputAudioInputAudio](#openaiinputaudioinputaudio) |  | Yes |  |
| type | enum | The type of the input item. Always `input_audio`.<br>Possible values: `input_audio` | Yes |  |

### OpenAI.InputAudioInputAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | string |  | Yes |  |
| format | enum | <br>Possible values: `mp3`, `wav` | Yes |  |

### OpenAI.InputContent


### Discriminator for OpenAI.InputContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `input_text` | [OpenAI.InputContentInputTextContent](#openaiinputcontentinputtextcontent) |
| `input_image` | [OpenAI.InputContentInputImageContent](#openaiinputcontentinputimagecontent) |
| `input_file` | [OpenAI.InputContentInputFileContent](#openaiinputcontentinputfilecontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.InputContentType](#openaiinputcontenttype) |  | Yes |  |

### OpenAI.InputContentInputFileContent

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string | The content of the file to be sent to the model. | No |  |
| file_id | string (nullable) |  | No |  |
| file_url | string | The URL of the file to be sent to the model. | No |  |
| filename | string | The name of the file to be sent to the model. | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.InputContentInputImageContent

An image input to the model. Learn about [image inputs](https://platform.openai.com/docs/guides/vision).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | [OpenAI.ImageDetail](#openaiimagedetail) |  | Yes |  |
| file_id | string (nullable) |  | No |  |
| image_url | string |  | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.InputContentInputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.InputContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `input_text`<br>`input_image`<br>`input_file` |

### OpenAI.InputFidelity

Control how much effort the model will exert to match the style and features, especially facial features, of input images. This parameter is only supported for `gpt-image-1`. Unsupported for `gpt-image-1-mini`. Supports `high` and `low`. Defaults to `low`.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `high`<br>`low` |

### OpenAI.InputFileContent

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string | The content of the file to be sent to the model. | No |  |
| file_id | string (nullable) |  | No |  |
| file_url | string | The URL of the file to be sent to the model. | No |  |
| filename | string | The name of the file to be sent to the model. | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.InputFileContentParam

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string (nullable) |  | No |  |
| file_id | string (nullable) |  | No |  |
| file_url | string |  | No |  |
| filename | string (nullable) |  | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.InputImageContent

An image input to the model. Learn about [image inputs](https://platform.openai.com/docs/guides/vision).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | [OpenAI.ImageDetail](#openaiimagedetail) |  | Yes |  |
| file_id | string (nullable) |  | No |  |
| image_url | string |  | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.InputImageContentParamAutoParam

An image input to the model. Learn about [image inputs](https://platform.openai.com/docs/guides/vision)

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | [OpenAI.DetailEnum](#openaidetailenum) (nullable) |  | No |  |
| file_id | string (nullable) |  | No |  |
| image_url | string |  | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.InputItem

An item representing part of the context for the response to be
generated by the model. Can contain text, images, and audio inputs,
as well as previous assistant responses and tool call outputs.


### Discriminator for OpenAI.InputItem

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `message` | [OpenAI.EasyInputMessage](#openaieasyinputmessage) |
| `item_reference` | [OpenAI.ItemReferenceParam](#openaiitemreferenceparam) |
| `output_message` | [OpenAI.InputItemOutputMessage](#openaiinputitemoutputmessage) |
| `file_search_call` | [OpenAI.InputItemFileSearchToolCall](#openaiinputitemfilesearchtoolcall) |
| `computer_call` | [OpenAI.InputItemComputerToolCall](#openaiinputitemcomputertoolcall) |
| `computer_call_output` | [OpenAI.InputItemComputerCallOutputItemParam](#openaiinputitemcomputercalloutputitemparam) |
| `web_search_call` | [OpenAI.InputItemWebSearchToolCall](#openaiinputitemwebsearchtoolcall) |
| `function_call` | [OpenAI.InputItemFunctionToolCall](#openaiinputitemfunctiontoolcall) |
| `function_call_output` | [OpenAI.InputItemFunctionCallOutputItemParam](#openaiinputitemfunctioncalloutputitemparam) |
| `reasoning` | [OpenAI.InputItemReasoningItem](#openaiinputitemreasoningitem) |
| `compaction` | [OpenAI.InputItemCompactionSummaryItemParam](#openaiinputitemcompactionsummaryitemparam) |
| `image_generation_call` | [OpenAI.InputItemImageGenToolCall](#openaiinputitemimagegentoolcall) |
| `code_interpreter_call` | [OpenAI.InputItemCodeInterpreterToolCall](#openaiinputitemcodeinterpretertoolcall) |
| `local_shell_call` | [OpenAI.InputItemLocalShellToolCall](#openaiinputitemlocalshelltoolcall) |
| `local_shell_call_output` | [OpenAI.InputItemLocalShellToolCallOutput](#openaiinputitemlocalshelltoolcalloutput) |
| `shell_call` | [OpenAI.InputItemFunctionShellCallItemParam](#openaiinputitemfunctionshellcallitemparam) |
| `shell_call_output` | [OpenAI.InputItemFunctionShellCallOutputItemParam](#openaiinputitemfunctionshellcalloutputitemparam) |
| `apply_patch_call` | [OpenAI.InputItemApplyPatchToolCallItemParam](#openaiinputitemapplypatchtoolcallitemparam) |
| `apply_patch_call_output` | [OpenAI.InputItemApplyPatchToolCallOutputItemParam](#openaiinputitemapplypatchtoolcalloutputitemparam) |
| `mcp_list_tools` | [OpenAI.InputItemMcpListTools](#openaiinputitemmcplisttools) |
| `mcp_approval_request` | [OpenAI.InputItemMcpApprovalRequest](#openaiinputitemmcpapprovalrequest) |
| `mcp_approval_response` | [OpenAI.InputItemMcpApprovalResponse](#openaiinputitemmcpapprovalresponse) |
| `mcp_call` | [OpenAI.InputItemMcpToolCall](#openaiinputitemmcptoolcall) |
| `custom_tool_call_output` | [OpenAI.InputItemCustomToolCallOutput](#openaiinputitemcustomtoolcalloutput) |
| `custom_tool_call` | [OpenAI.InputItemCustomToolCall](#openaiinputitemcustomtoolcall) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.InputItemType](#openaiinputitemtype) |  | Yes |  |

### OpenAI.InputItemApplyPatchToolCallItemParam

A tool call representing a request to create, delete, or update files using diff patches.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| operation | [OpenAI.ApplyPatchOperationParam](#openaiapplypatchoperationparam) | One of the create_file, delete_file, or update_file operations supplied to the apply_patch tool. | Yes |  |
| └─ type | [OpenAI.ApplyPatchOperationParamType](#openaiapplypatchoperationparamtype) |  | Yes |  |
| status | [OpenAI.ApplyPatchCallStatusParam](#openaiapplypatchcallstatusparam) | Status values reported for apply_patch tool calls. | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call`.<br>Possible values: `apply_patch_call` | Yes |  |

### OpenAI.InputItemApplyPatchToolCallOutputItemParam

The streamed output emitted by an apply patch tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| output | string (nullable) |  | No |  |
| status | [OpenAI.ApplyPatchCallOutputStatusParam](#openaiapplypatchcalloutputstatusparam) | Outcome values reported for apply_patch tool call outputs. | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call_output`.<br>Possible values: `apply_patch_call_output` | Yes |  |

### OpenAI.InputItemCodeInterpreterToolCall

A tool call to run code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string (nullable) |  | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| id | string | The unique ID of the code interpreter tool call. | Yes |  |
| outputs | array of [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) or [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) |  | Yes |  |
| status | enum | The status of the code interpreter tool call. Valid values are `in_progress`, `completed`, `incomplete`, `interpreting`, and `failed`.<br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | The type of the code interpreter tool call. Always `code_interpreter_call`.<br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.InputItemCompactionSummaryItemParam

A compaction item generated by the [`v1/responses/compact` API](https://platform.openai.com/docs/api-reference/responses/compact).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| encrypted_content | string | The encrypted content of the compaction summary.<br>**Constraints:** maxLength: 10485760 | Yes |  |
| id | string (nullable) |  | No |  |
| type | enum | The type of the item. Always `compaction`.<br>Possible values: `compaction` | Yes |  |

### OpenAI.InputItemComputerCallOutputItemParam

The output of a computer tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| acknowledged_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) |  | No |  |
| call_id | string | The ID of the computer tool call that produced the output.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| output | [OpenAI.ComputerScreenshotImage](#openaicomputerscreenshotimage) | A computer screenshot image used with the computer use tool. | Yes |  |
| status | [OpenAI.FunctionCallItemStatus](#openaifunctioncallitemstatus) (nullable) |  | No |  |
| type | enum | The type of the computer tool call output. Always `computer_call_output`.<br>Possible values: `computer_call_output` | Yes |  |

### OpenAI.InputItemComputerToolCall

A tool call to a computer use tool. See the
[computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| id | string | The unique ID of the computer call. | Yes |  |
| pending_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The pending safety checks for the computer call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the computer call. Always `computer_call`.<br>Possible values: `computer_call` | Yes |  |

### OpenAI.InputItemCustomToolCall

A call to a custom tool created by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | An identifier used to map this custom tool call to a tool call output. | Yes |  |
| id | string | The unique ID of the custom tool call in the OpenAI platform. | No |  |
| input | string | The input for the custom tool call generated by the model. | Yes |  |
| name | string | The name of the custom tool being called. | Yes |  |
| type | enum | The type of the custom tool call. Always `custom_tool_call`.<br>Possible values: `custom_tool_call` | Yes |  |

### OpenAI.InputItemCustomToolCallOutput

The output of a custom tool call from your code, being sent back to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The call ID, used to map this custom tool call output to a custom tool call. | Yes |  |
| id | string | The unique ID of the custom tool call output in the OpenAI platform. | No |  |
| output | string or array of [OpenAI.FunctionAndCustomToolCallOutput](#openaifunctionandcustomtoolcalloutput) | The output from the custom tool call generated by your code.<br>  Can be a string or an list of output content. | Yes |  |
| type | enum | The type of the custom tool call output. Always `custom_tool_call_output`.<br>Possible values: `custom_tool_call_output` | Yes |  |

### OpenAI.InputItemFileSearchToolCall

The results of a file search tool call. See the
[file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the file search tool call. | Yes |  |
| queries | array of string | The queries used to search for files. | Yes |  |
| results | array of [OpenAI.FileSearchToolCallResults](#openaifilesearchtoolcallresults) |  | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`,<br>  `searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | The type of the file search tool call. Always `file_search_call`.<br>Possible values: `file_search_call` | Yes |  |

### OpenAI.InputItemFunctionCallOutputItemParam

The output of a function tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the function tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| output | string or array of [OpenAI.InputTextContentParam](#openaiinputtextcontentparam) or [OpenAI.InputImageContentParamAutoParam](#openaiinputimagecontentparamautoparam) or [OpenAI.InputFileContentParam](#openaiinputfilecontentparam) | Text, image, or file output of the function tool call. | Yes |  |
| status | [OpenAI.FunctionCallItemStatus](#openaifunctioncallitemstatus) (nullable) |  | No |  |
| type | enum | The type of the function tool call output. Always `function_call_output`.<br>Possible values: `function_call_output` | Yes |  |

### OpenAI.InputItemFunctionShellCallItemParam

A tool representing a request to execute one or more shell commands.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.FunctionShellActionParam](#openaifunctionshellactionparam) | Commands and limits describing how to run the shell tool call. | Yes |  |
| └─ commands | array of string | Ordered shell commands for the execution environment to run. | Yes |  |
| └─ max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ timeout_ms | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| call_id | string | The unique ID of the shell tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| status | [OpenAI.FunctionShellCallItemStatus](#openaifunctionshellcallitemstatus) (nullable) | Status values reported for shell tool calls. | No |  |
| type | enum | The type of the item. Always `shell_call`.<br>Possible values: `shell_call` | Yes |  |

### OpenAI.InputItemFunctionShellCallOutputItemParam

The streamed output items emitted by a shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the shell tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| output | array of [OpenAI.FunctionShellCallOutputContentParam](#openaifunctionshellcalloutputcontentparam) | Captured chunks of stdout and stderr output, along with their associated outcomes. | Yes |  |
| type | enum | The type of the item. Always `shell_call_output`.<br>Possible values: `shell_call_output` | Yes |  |

### OpenAI.InputItemFunctionToolCall

A tool call to run a function. See the
[function calling guide](https://platform.openai.com/docs/guides/function-calling) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call. | No |  |
| name | string | The name of the function to run. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call. Always `function_call`.<br>Possible values: `function_call` | Yes |  |

### OpenAI.InputItemImageGenToolCall

An image generation request made by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the image generation call. | Yes |  |
| result | string (nullable) |  | Yes |  |
| status | enum | The status of the image generation call.<br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | The type of the image generation call. Always `image_generation_call`.<br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.InputItemLocalShellToolCall

A tool call to run a command on the local shell.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| id | string | The unique ID of the local shell call. | Yes |  |
| status | enum | The status of the local shell call.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the local shell call. Always `local_shell_call`.<br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.InputItemLocalShellToolCallOutput

The output of a local shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| output | string | A JSON string of the output of the local shell tool call. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the local shell tool call output. Always `local_shell_call_output`.<br>Possible values: `local_shell_call_output` | Yes |  |

### OpenAI.InputItemMcpApprovalRequest

A request for human approval of a tool invocation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| id | string | The unique ID of the approval request. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | The type of the item. Always `mcp_approval_request`.<br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.InputItemMcpApprovalResponse

A response to an MCP approval request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string | The ID of the approval request being answered. | Yes |  |
| approve | boolean | Whether the request was approved. | Yes |  |
| id | string (nullable) |  | No |  |
| reason | string (nullable) |  | No |  |
| type | enum | The type of the item. Always `mcp_approval_response`.<br>Possible values: `mcp_approval_response` | Yes |  |

### OpenAI.InputItemMcpListTools

A list of tools available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the list. | Yes |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array of [OpenAI.MCPListToolsTool](#openaimcplisttoolstool) | The tools available on the server. | Yes |  |
| type | enum | The type of the item. Always `mcp_list_tools`.<br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.InputItemMcpToolCall

An invocation of a tool on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string (nullable) |  | No |  |
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the tool call. | Yes |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string (nullable) |  | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| status | [OpenAI.MCPToolCallStatus](#openaimcptoolcallstatus) |  | No |  |
| type | enum | The type of the item. Always `mcp_call`.<br>Possible values: `mcp_call` | Yes |  |

### OpenAI.InputItemOutputMessage

An output message from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.OutputMessageContent](#openaioutputmessagecontent) | The content of the output message. | Yes |  |
| id | string | The unique ID of the output message. | Yes |  |
| role | enum | The role of the output message. Always `assistant`.<br>Possible values: `assistant` | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the output message. Always `message`.<br>Possible values: `output_message` | Yes |  |

### OpenAI.InputItemReasoningItem

A description of the chain of thought used by a reasoning model while generating
a response. Be sure to include these items in your `input` to the Responses API
for subsequent turns of a conversation if you are manually
[managing context](https://platform.openai.com/docs/guides/conversation-state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.ReasoningTextContent](#openaireasoningtextcontent) | Reasoning text content. | No |  |
| encrypted_content | string (nullable) |  | No |  |
| id | string | The unique identifier of the reasoning content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| summary | array of [OpenAI.Summary](#openaisummary) | Reasoning summary content. | Yes |  |
| type | enum | The type of the object. Always `reasoning`.<br>Possible values: `reasoning` | Yes |  |

### OpenAI.InputItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`output_message`<br>`file_search_call`<br>`computer_call`<br>`computer_call_output`<br>`web_search_call`<br>`function_call`<br>`function_call_output`<br>`reasoning`<br>`compaction`<br>`image_generation_call`<br>`code_interpreter_call`<br>`local_shell_call`<br>`local_shell_call_output`<br>`shell_call`<br>`shell_call_output`<br>`apply_patch_call`<br>`apply_patch_call_output`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`mcp_approval_response`<br>`mcp_call`<br>`custom_tool_call_output`<br>`custom_tool_call`<br>`item_reference` |

### OpenAI.InputItemWebSearchToolCall

The results of a web search tool call. See the
[web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) or [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) or [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) | An object describing the specific action taken in this web search call.<br>  Includes details on how the model used the web (search, open_page, find). | Yes |  |
| id | string | The unique ID of the web search tool call. | Yes |  |
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | The type of the web search tool call. Always `web_search_call`.<br>Possible values: `web_search_call` | Yes |  |

### OpenAI.InputMessage

A message input to the model with a role indicating instruction following
hierarchy. Instructions given with the `developer` or `system` role take
precedence over instructions given with the `user` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | [OpenAI.InputMessageContentList](#openaiinputmessagecontentlist) | A list of one or many input items to the model, containing different content<br>types. | Yes |  |
| role | enum | The role of the message input. One of `user`, `system`, or `developer`.<br>Possible values: `user`, `system`, `developer` | Yes |  |
| status | enum | The status of item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the message input. Always set to `message`.<br>Possible values: `message` | Yes |  |

### OpenAI.InputMessageContentList

A list of one or many input items to the model, containing different content
types.

**Array of**: [OpenAI.InputContent](#openaiinputcontent)


### OpenAI.InputMessageResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | [OpenAI.InputMessageContentList](#openaiinputmessagecontentlist) | A list of one or many input items to the model, containing different content<br>types. | Yes |  |
| id | string | The unique ID of the message input. | Yes |  |
| role | enum | The role of the message input. One of `user`, `system`, or `developer`.<br>Possible values: `user`, `system`, `developer` | Yes |  |
| status | enum | The status of item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the message input. Always set to `message`.<br>Possible values: `message` | Yes |  |

### OpenAI.InputParam

Text, image, or file inputs to the model, used to generate a response.
Learn more:
- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
- [Image inputs](https://platform.openai.com/docs/guides/images)
- [File inputs](https://platform.openai.com/docs/guides/pdf-files)
- [Conversation state](https://platform.openai.com/docs/guides/conversation-state)
- [Function calling](https://platform.openai.com/docs/guides/function-calling)

**Type**: string or array of [OpenAI.InputItem](#openaiinputitem)

Text, image, or file inputs to the model, used to generate a response.
Learn more:
- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
- [Image inputs](https://platform.openai.com/docs/guides/images)
- [File inputs](https://platform.openai.com/docs/guides/pdf-files)
- [Conversation state](https://platform.openai.com/docs/guides/conversation-state)
- [Function calling](https://platform.openai.com/docs/guides/function-calling)


### OpenAI.InputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.InputTextContentParam

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model.<br>**Constraints:** maxLength: 10485760 | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.Item

Content item used to generate a response.


### Discriminator for OpenAI.Item

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `memory_search_call` | [MemorySearchToolCallItemParam](#memorysearchtoolcallitemparam) |
| `message` | [OpenAI.InputMessage](#openaiinputmessage) |
| `output_message` | [OpenAI.ItemOutputMessage](#openaiitemoutputmessage) |
| `file_search_call` | [OpenAI.ItemFileSearchToolCall](#openaiitemfilesearchtoolcall) |
| `computer_call` | [OpenAI.ItemComputerToolCall](#openaiitemcomputertoolcall) |
| `computer_call_output` | [OpenAI.ItemComputerCallOutputItemParam](#openaiitemcomputercalloutputitemparam) |
| `web_search_call` | [OpenAI.ItemWebSearchToolCall](#openaiitemwebsearchtoolcall) |
| `function_call` | [OpenAI.ItemFunctionToolCall](#openaiitemfunctiontoolcall) |
| `function_call_output` | [OpenAI.ItemFunctionCallOutputItemParam](#openaiitemfunctioncalloutputitemparam) |
| `reasoning` | [OpenAI.ItemReasoningItem](#openaiitemreasoningitem) |
| `compaction` | [OpenAI.ItemCompactionSummaryItemParam](#openaiitemcompactionsummaryitemparam) |
| `image_generation_call` | [OpenAI.ItemImageGenToolCall](#openaiitemimagegentoolcall) |
| `code_interpreter_call` | [OpenAI.ItemCodeInterpreterToolCall](#openaiitemcodeinterpretertoolcall) |
| `local_shell_call` | [OpenAI.ItemLocalShellToolCall](#openaiitemlocalshelltoolcall) |
| `local_shell_call_output` | [OpenAI.ItemLocalShellToolCallOutput](#openaiitemlocalshelltoolcalloutput) |
| `shell_call` | [OpenAI.ItemFunctionShellCallItemParam](#openaiitemfunctionshellcallitemparam) |
| `shell_call_output` | [OpenAI.ItemFunctionShellCallOutputItemParam](#openaiitemfunctionshellcalloutputitemparam) |
| `apply_patch_call` | [OpenAI.ItemApplyPatchToolCallItemParam](#openaiitemapplypatchtoolcallitemparam) |
| `apply_patch_call_output` | [OpenAI.ItemApplyPatchToolCallOutputItemParam](#openaiitemapplypatchtoolcalloutputitemparam) |
| `mcp_list_tools` | [OpenAI.ItemMcpListTools](#openaiitemmcplisttools) |
| `mcp_approval_request` | [OpenAI.ItemMcpApprovalRequest](#openaiitemmcpapprovalrequest) |
| `mcp_approval_response` | [OpenAI.ItemMcpApprovalResponse](#openaiitemmcpapprovalresponse) |
| `mcp_call` | [OpenAI.ItemMcpToolCall](#openaiitemmcptoolcall) |
| `custom_tool_call_output` | [OpenAI.ItemCustomToolCallOutput](#openaiitemcustomtoolcalloutput) |
| `custom_tool_call` | [OpenAI.ItemCustomToolCall](#openaiitemcustomtoolcall) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ItemType](#openaiitemtype) |  | Yes |  |

### OpenAI.ItemApplyPatchToolCallItemParam

A tool call representing a request to create, delete, or update files using diff patches.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| operation | [OpenAI.ApplyPatchOperationParam](#openaiapplypatchoperationparam) | One of the create_file, delete_file, or update_file operations supplied to the apply_patch tool. | Yes |  |
| └─ type | [OpenAI.ApplyPatchOperationParamType](#openaiapplypatchoperationparamtype) |  | Yes |  |
| status | [OpenAI.ApplyPatchCallStatusParam](#openaiapplypatchcallstatusparam) | Status values reported for apply_patch tool calls. | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call`.<br>Possible values: `apply_patch_call` | Yes |  |

### OpenAI.ItemApplyPatchToolCallOutputItemParam

The streamed output emitted by an apply patch tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| output | string (nullable) |  | No |  |
| status | [OpenAI.ApplyPatchCallOutputStatusParam](#openaiapplypatchcalloutputstatusparam) | Outcome values reported for apply_patch tool call outputs. | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call_output`.<br>Possible values: `apply_patch_call_output` | Yes |  |

### OpenAI.ItemCodeInterpreterToolCall

A tool call to run code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string (nullable) |  | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| id | string | The unique ID of the code interpreter tool call. | Yes |  |
| outputs | array of [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) or [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) |  | Yes |  |
| status | enum | The status of the code interpreter tool call. Valid values are `in_progress`, `completed`, `incomplete`, `interpreting`, and `failed`.<br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | The type of the code interpreter tool call. Always `code_interpreter_call`.<br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.ItemCompactionSummaryItemParam

A compaction item generated by the [`v1/responses/compact` API](https://platform.openai.com/docs/api-reference/responses/compact).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| encrypted_content | string | The encrypted content of the compaction summary.<br>**Constraints:** maxLength: 10485760 | Yes |  |
| id | string (nullable) |  | No |  |
| type | enum | The type of the item. Always `compaction`.<br>Possible values: `compaction` | Yes |  |

### OpenAI.ItemComputerCallOutputItemParam

The output of a computer tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| acknowledged_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) |  | No |  |
| call_id | string | The ID of the computer tool call that produced the output.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| output | [OpenAI.ComputerScreenshotImage](#openaicomputerscreenshotimage) | A computer screenshot image used with the computer use tool. | Yes |  |
| status | [OpenAI.FunctionCallItemStatus](#openaifunctioncallitemstatus) (nullable) |  | No |  |
| type | enum | The type of the computer tool call output. Always `computer_call_output`.<br>Possible values: `computer_call_output` | Yes |  |

### OpenAI.ItemComputerToolCall

A tool call to a computer use tool. See the
[computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| id | string | The unique ID of the computer call. | Yes |  |
| pending_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The pending safety checks for the computer call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the computer call. Always `computer_call`.<br>Possible values: `computer_call` | Yes |  |

### OpenAI.ItemCustomToolCall

A call to a custom tool created by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | An identifier used to map this custom tool call to a tool call output. | Yes |  |
| id | string | The unique ID of the custom tool call in the OpenAI platform. | No |  |
| input | string | The input for the custom tool call generated by the model. | Yes |  |
| name | string | The name of the custom tool being called. | Yes |  |
| type | enum | The type of the custom tool call. Always `custom_tool_call`.<br>Possible values: `custom_tool_call` | Yes |  |

### OpenAI.ItemCustomToolCallOutput

The output of a custom tool call from your code, being sent back to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The call ID, used to map this custom tool call output to a custom tool call. | Yes |  |
| id | string | The unique ID of the custom tool call output in the OpenAI platform. | No |  |
| output | string or array of [OpenAI.FunctionAndCustomToolCallOutput](#openaifunctionandcustomtoolcalloutput) | The output from the custom tool call generated by your code.<br>  Can be a string or an list of output content. | Yes |  |
| type | enum | The type of the custom tool call output. Always `custom_tool_call_output`.<br>Possible values: `custom_tool_call_output` | Yes |  |

### OpenAI.ItemFileSearchToolCall

The results of a file search tool call. See the
[file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the file search tool call. | Yes |  |
| queries | array of string | The queries used to search for files. | Yes |  |
| results | array of [OpenAI.FileSearchToolCallResults](#openaifilesearchtoolcallresults) |  | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`,<br>  `searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | The type of the file search tool call. Always `file_search_call`.<br>Possible values: `file_search_call` | Yes |  |

### OpenAI.ItemFunctionCallOutputItemParam

The output of a function tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the function tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| output | string or array of [OpenAI.InputTextContentParam](#openaiinputtextcontentparam) or [OpenAI.InputImageContentParamAutoParam](#openaiinputimagecontentparamautoparam) or [OpenAI.InputFileContentParam](#openaiinputfilecontentparam) | Text, image, or file output of the function tool call. | Yes |  |
| status | [OpenAI.FunctionCallItemStatus](#openaifunctioncallitemstatus) (nullable) |  | No |  |
| type | enum | The type of the function tool call output. Always `function_call_output`.<br>Possible values: `function_call_output` | Yes |  |

### OpenAI.ItemFunctionShellCallItemParam

A tool representing a request to execute one or more shell commands.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.FunctionShellActionParam](#openaifunctionshellactionparam) | Commands and limits describing how to run the shell tool call. | Yes |  |
| └─ commands | array of string | Ordered shell commands for the execution environment to run. | Yes |  |
| └─ max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ timeout_ms | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| call_id | string | The unique ID of the shell tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| status | [OpenAI.FunctionShellCallItemStatus](#openaifunctionshellcallitemstatus) (nullable) | Status values reported for shell tool calls. | No |  |
| type | enum | The type of the item. Always `shell_call`.<br>Possible values: `shell_call` | Yes |  |

### OpenAI.ItemFunctionShellCallOutputItemParam

The streamed output items emitted by a shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the shell tool call generated by the model.<br>**Constraints:** minLength: 1, maxLength: 64 | Yes |  |
| id | string (nullable) |  | No |  |
| max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| output | array of [OpenAI.FunctionShellCallOutputContentParam](#openaifunctionshellcalloutputcontentparam) | Captured chunks of stdout and stderr output, along with their associated outcomes. | Yes |  |
| type | enum | The type of the item. Always `shell_call_output`.<br>Possible values: `shell_call_output` | Yes |  |

### OpenAI.ItemFunctionToolCall

A tool call to run a function. See the
[function calling guide](https://platform.openai.com/docs/guides/function-calling) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call. | No |  |
| name | string | The name of the function to run. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call. Always `function_call`.<br>Possible values: `function_call` | Yes |  |

### OpenAI.ItemImageGenToolCall

An image generation request made by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the image generation call. | Yes |  |
| result | string (nullable) |  | Yes |  |
| status | enum | The status of the image generation call.<br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | The type of the image generation call. Always `image_generation_call`.<br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.ItemLocalShellToolCall

A tool call to run a command on the local shell.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| id | string | The unique ID of the local shell call. | Yes |  |
| status | enum | The status of the local shell call.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the local shell call. Always `local_shell_call`.<br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.ItemLocalShellToolCallOutput

The output of a local shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| output | string | A JSON string of the output of the local shell tool call. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the local shell tool call output. Always `local_shell_call_output`.<br>Possible values: `local_shell_call_output` | Yes |  |

### OpenAI.ItemMcpApprovalRequest

A request for human approval of a tool invocation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| id | string | The unique ID of the approval request. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | The type of the item. Always `mcp_approval_request`.<br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.ItemMcpApprovalResponse

A response to an MCP approval request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string | The ID of the approval request being answered. | Yes |  |
| approve | boolean | Whether the request was approved. | Yes |  |
| id | string (nullable) |  | No |  |
| reason | string (nullable) |  | No |  |
| type | enum | The type of the item. Always `mcp_approval_response`.<br>Possible values: `mcp_approval_response` | Yes |  |

### OpenAI.ItemMcpListTools

A list of tools available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the list. | Yes |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array of [OpenAI.MCPListToolsTool](#openaimcplisttoolstool) | The tools available on the server. | Yes |  |
| type | enum | The type of the item. Always `mcp_list_tools`.<br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.ItemMcpToolCall

An invocation of a tool on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string (nullable) |  | No |  |
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the tool call. | Yes |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string (nullable) |  | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| status | [OpenAI.MCPToolCallStatus](#openaimcptoolcallstatus) |  | No |  |
| type | enum | The type of the item. Always `mcp_call`.<br>Possible values: `mcp_call` | Yes |  |

### OpenAI.ItemOutputMessage

An output message from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.OutputMessageContent](#openaioutputmessagecontent) | The content of the output message. | Yes |  |
| id | string | The unique ID of the output message. | Yes |  |
| role | enum | The role of the output message. Always `assistant`.<br>Possible values: `assistant` | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the output message. Always `message`.<br>Possible values: `output_message` | Yes |  |

### OpenAI.ItemReasoningItem

A description of the chain of thought used by a reasoning model while generating
a response. Be sure to include these items in your `input` to the Responses API
for subsequent turns of a conversation if you are manually
[managing context](https://platform.openai.com/docs/guides/conversation-state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.ReasoningTextContent](#openaireasoningtextcontent) | Reasoning text content. | No |  |
| encrypted_content | string (nullable) |  | No |  |
| id | string | The unique identifier of the reasoning content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| summary | array of [OpenAI.Summary](#openaisummary) | Reasoning summary content. | Yes |  |
| type | enum | The type of the object. Always `reasoning`.<br>Possible values: `reasoning` | Yes |  |

### OpenAI.ItemReferenceParam

An internal identifier for an item to reference.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The ID of the item to reference. | Yes |  |
| type | enum | The type of item to reference. Always `item_reference`.<br>Possible values: `item_reference` | Yes |  |

### OpenAI.ItemResource

Content item used to generate a response.


### Discriminator for OpenAI.ItemResource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `message` | [OpenAI.InputMessageResource](#openaiinputmessageresource) |
| `output_message` | [OpenAI.ItemResourceOutputMessage](#openaiitemresourceoutputmessage) |
| `file_search_call` | [OpenAI.ItemResourceFileSearchToolCall](#openaiitemresourcefilesearchtoolcall) |
| `computer_call` | [OpenAI.ItemResourceComputerToolCall](#openaiitemresourcecomputertoolcall) |
| `computer_call_output` | [OpenAI.ItemResourceComputerToolCallOutputResource](#openaiitemresourcecomputertoolcalloutputresource) |
| `web_search_call` | [OpenAI.ItemResourceWebSearchToolCall](#openaiitemresourcewebsearchtoolcall) |
| `function_call` | [OpenAI.ItemResourceFunctionToolCallResource](#openaiitemresourcefunctiontoolcallresource) |
| `function_call_output` | [OpenAI.ItemResourceFunctionToolCallOutputResource](#openaiitemresourcefunctiontoolcalloutputresource) |
| `image_generation_call` | [OpenAI.ItemResourceImageGenToolCall](#openaiitemresourceimagegentoolcall) |
| `code_interpreter_call` | [OpenAI.ItemResourceCodeInterpreterToolCall](#openaiitemresourcecodeinterpretertoolcall) |
| `local_shell_call` | [OpenAI.ItemResourceLocalShellToolCall](#openaiitemresourcelocalshelltoolcall) |
| `local_shell_call_output` | [OpenAI.ItemResourceLocalShellToolCallOutput](#openaiitemresourcelocalshelltoolcalloutput) |
| `shell_call` | [OpenAI.ItemResourceFunctionShellCall](#openaiitemresourcefunctionshellcall) |
| `shell_call_output` | [OpenAI.ItemResourceFunctionShellCallOutput](#openaiitemresourcefunctionshellcalloutput) |
| `apply_patch_call` | [OpenAI.ItemResourceApplyPatchToolCall](#openaiitemresourceapplypatchtoolcall) |
| `apply_patch_call_output` | [OpenAI.ItemResourceApplyPatchToolCallOutput](#openaiitemresourceapplypatchtoolcalloutput) |
| `mcp_list_tools` | [OpenAI.ItemResourceMcpListTools](#openaiitemresourcemcplisttools) |
| `mcp_approval_request` | [OpenAI.ItemResourceMcpApprovalRequest](#openaiitemresourcemcpapprovalrequest) |
| `mcp_approval_response` | [OpenAI.ItemResourceMcpApprovalResponseResource](#openaiitemresourcemcpapprovalresponseresource) |
| `mcp_call` | [OpenAI.ItemResourceMcpToolCall](#openaiitemresourcemcptoolcall) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ItemResourceType](#openaiitemresourcetype) |  | Yes |  |

### OpenAI.ItemResourceApplyPatchToolCall

A tool call that applies file diffs by creating, deleting, or updating files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the apply patch tool call. Populated when this item is returned via API. | Yes |  |
| operation | [OpenAI.ApplyPatchFileOperation](#openaiapplypatchfileoperation) | One of the create_file, delete_file, or update_file operations applied via apply_patch. | Yes |  |
| └─ type | [OpenAI.ApplyPatchFileOperationType](#openaiapplypatchfileoperationtype) |  | Yes |  |
| status | [OpenAI.ApplyPatchCallStatus](#openaiapplypatchcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call`.<br>Possible values: `apply_patch_call` | Yes |  |

### OpenAI.ItemResourceApplyPatchToolCallOutput

The output emitted by an apply patch tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call output. | No |  |
| id | string | The unique ID of the apply patch tool call output. Populated when this item is returned via API. | Yes |  |
| output | string (nullable) |  | No |  |
| status | [OpenAI.ApplyPatchCallOutputStatus](#openaiapplypatchcalloutputstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call_output`.<br>Possible values: `apply_patch_call_output` | Yes |  |

### OpenAI.ItemResourceCodeInterpreterToolCall

A tool call to run code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string (nullable) |  | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| id | string | The unique ID of the code interpreter tool call. | Yes |  |
| outputs | array of [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) or [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) |  | Yes |  |
| status | enum | The status of the code interpreter tool call. Valid values are `in_progress`, `completed`, `incomplete`, `interpreting`, and `failed`.<br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | The type of the code interpreter tool call. Always `code_interpreter_call`.<br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.ItemResourceComputerToolCall

A tool call to a computer use tool. See the
[computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| id | string | The unique ID of the computer call. | Yes |  |
| pending_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The pending safety checks for the computer call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the computer call. Always `computer_call`.<br>Possible values: `computer_call` | Yes |  |

### OpenAI.ItemResourceComputerToolCallOutputResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| acknowledged_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The safety checks reported by the API that have been acknowledged by the<br>  developer. | No |  |
| call_id | string | The ID of the computer tool call that produced the output. | Yes |  |
| id | string | The ID of the computer tool call output. | No |  |
| output | [OpenAI.ComputerScreenshotImage](#openaicomputerscreenshotimage) | A computer screenshot image used with the computer use tool. | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the computer tool call output. Always `computer_call_output`.<br>Possible values: `computer_call_output` | Yes |  |

### OpenAI.ItemResourceFileSearchToolCall

The results of a file search tool call. See the
[file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the file search tool call. | Yes |  |
| queries | array of string | The queries used to search for files. | Yes |  |
| results | array of [OpenAI.FileSearchToolCallResults](#openaifilesearchtoolcallresults) |  | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`,<br>  `searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | The type of the file search tool call. Always `file_search_call`.<br>Possible values: `file_search_call` | Yes |  |

### OpenAI.ItemResourceFunctionShellCall

A tool call that executes one or more shell commands in a managed environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.FunctionShellAction](#openaifunctionshellaction) | Execute a shell command. | Yes |  |
| └─ commands | array of string |  | Yes |  |
| └─ max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| └─ timeout_ms | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the shell tool call. Populated when this item is returned via API. | Yes |  |
| status | [OpenAI.LocalShellCallStatus](#openailocalshellcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `shell_call`.<br>Possible values: `shell_call` | Yes |  |

### OpenAI.ItemResourceFunctionShellCallOutput

The output of a shell tool call that was emitted.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The identifier of the actor that created the item. | No |  |
| id | string | The unique ID of the shell call output. Populated when this item is returned via API. | Yes |  |
| max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| output | array of [OpenAI.FunctionShellCallOutputContent](#openaifunctionshellcalloutputcontent) | An array of shell call output contents | Yes |  |
| type | enum | The type of the shell call output. Always `shell_call_output`.<br>Possible values: `shell_call_output` | Yes |  |

### OpenAI.ItemResourceFunctionToolCallOutputResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call output. Populated when this item<br>  is returned via API. | No |  |
| output | string or array of [OpenAI.FunctionAndCustomToolCallOutput](#openaifunctionandcustomtoolcalloutput) | The output from the function call generated by your code.<br>  Can be a string or an list of output content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call output. Always `function_call_output`.<br>Possible values: `function_call_output` | Yes |  |

### OpenAI.ItemResourceFunctionToolCallResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call. | No |  |
| name | string | The name of the function to run. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call. Always `function_call`.<br>Possible values: `function_call` | Yes |  |

### OpenAI.ItemResourceImageGenToolCall

An image generation request made by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the image generation call. | Yes |  |
| result | string (nullable) |  | Yes |  |
| status | enum | The status of the image generation call.<br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | The type of the image generation call. Always `image_generation_call`.<br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.ItemResourceLocalShellToolCall

A tool call to run a command on the local shell.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| id | string | The unique ID of the local shell call. | Yes |  |
| status | enum | The status of the local shell call.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the local shell call. Always `local_shell_call`.<br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.ItemResourceLocalShellToolCallOutput

The output of a local shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| output | string | A JSON string of the output of the local shell tool call. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the local shell tool call output. Always `local_shell_call_output`.<br>Possible values: `local_shell_call_output` | Yes |  |

### OpenAI.ItemResourceMcpApprovalRequest

A request for human approval of a tool invocation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| id | string | The unique ID of the approval request. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | The type of the item. Always `mcp_approval_request`.<br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.ItemResourceMcpApprovalResponseResource

A response to an MCP approval request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string | The ID of the approval request being answered. | Yes |  |
| approve | boolean | Whether the request was approved. | Yes |  |
| id | string | The unique ID of the approval response | Yes |  |
| reason | string (nullable) |  | No |  |
| type | enum | The type of the item. Always `mcp_approval_response`.<br>Possible values: `mcp_approval_response` | Yes |  |

### OpenAI.ItemResourceMcpListTools

A list of tools available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the list. | Yes |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array of [OpenAI.MCPListToolsTool](#openaimcplisttoolstool) | The tools available on the server. | Yes |  |
| type | enum | The type of the item. Always `mcp_list_tools`.<br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.ItemResourceMcpToolCall

An invocation of a tool on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string (nullable) |  | No |  |
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the tool call. | Yes |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string (nullable) |  | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| status | [OpenAI.MCPToolCallStatus](#openaimcptoolcallstatus) |  | No |  |
| type | enum | The type of the item. Always `mcp_call`.<br>Possible values: `mcp_call` | Yes |  |

### OpenAI.ItemResourceOutputMessage

An output message from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.OutputMessageContent](#openaioutputmessagecontent) | The content of the output message. | Yes |  |
| id | string | The unique ID of the output message. | Yes |  |
| role | enum | The role of the output message. Always `assistant`.<br>Possible values: `assistant` | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the output message. Always `message`.<br>Possible values: `output_message` | Yes |  |

### OpenAI.ItemResourceType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`output_message`<br>`file_search_call`<br>`computer_call`<br>`computer_call_output`<br>`web_search_call`<br>`function_call`<br>`function_call_output`<br>`image_generation_call`<br>`code_interpreter_call`<br>`local_shell_call`<br>`local_shell_call_output`<br>`shell_call`<br>`shell_call_output`<br>`apply_patch_call`<br>`apply_patch_call_output`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`mcp_approval_response`<br>`mcp_call`<br>`structured_outputs`<br>`oauth_consent_request`<br>`memory_search_call`<br>`workflow_action` |

### OpenAI.ItemResourceWebSearchToolCall

The results of a web search tool call. See the
[web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) or [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) or [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) | An object describing the specific action taken in this web search call.<br>  Includes details on how the model used the web (search, open_page, find). | Yes |  |
| id | string | The unique ID of the web search tool call. | Yes |  |
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | The type of the web search tool call. Always `web_search_call`.<br>Possible values: `web_search_call` | Yes |  |

### OpenAI.ItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`output_message`<br>`file_search_call`<br>`computer_call`<br>`computer_call_output`<br>`web_search_call`<br>`function_call`<br>`function_call_output`<br>`reasoning`<br>`compaction`<br>`image_generation_call`<br>`code_interpreter_call`<br>`local_shell_call`<br>`local_shell_call_output`<br>`shell_call`<br>`shell_call_output`<br>`apply_patch_call`<br>`apply_patch_call_output`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`mcp_approval_response`<br>`mcp_call`<br>`custom_tool_call_output`<br>`custom_tool_call`<br>`structured_outputs`<br>`oauth_consent_request`<br>`memory_search_call`<br>`workflow_action` |

### OpenAI.ItemWebSearchToolCall

The results of a web search tool call. See the
[web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) or [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) or [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) | An object describing the specific action taken in this web search call.<br>  Includes details on how the model used the web (search, open_page, find). | Yes |  |
| id | string | The unique ID of the web search tool call. | Yes |  |
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | The type of the web search tool call. Always `web_search_call`.<br>Possible values: `web_search_call` | Yes |  |

### OpenAI.KeyPressAction

A collection of keypresses the model would like to perform.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| keys | array of string | The combination of keys the model is requesting to be pressed. This is an array of strings, each representing a key. | Yes |  |
| type | enum | Specifies the event type. For a keypress action, this property is always set to `keypress`.<br>Possible values: `keypress` | Yes |  |

### OpenAI.ListFineTuningJobCheckpointsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.FineTuningJobCheckpoint](#openaifinetuningjobcheckpoint) |  | Yes |  |
| first_id | string (nullable) |  | No |  |
| has_more | boolean |  | Yes |  |
| last_id | string (nullable) |  | No |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListFineTuningJobEventsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.FineTuningJobEvent](#openaifinetuningjobevent) |  | Yes |  |
| has_more | boolean |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListPaginatedFineTuningJobsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.FineTuningJob](#openaifinetuningjob) |  | Yes |  |
| has_more | boolean |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.LocalShellCallStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`incomplete` |

### OpenAI.LocalShellExecAction

Execute a shell command on the server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| command | array of string | The command to run. | Yes |  |
| env | object | Environment variables to set for the command. | Yes |  |
| timeout_ms | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| type | enum | The type of the local shell action. Always `exec`.<br>Possible values: `exec` | Yes |  |
| user | string (nullable) |  | No |  |
| working_directory | string (nullable) |  | No |  |

### OpenAI.LocalShellToolParam

A tool that allows the model to execute shell commands in a local environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the local shell tool. Always `local_shell`.<br>Possible values: `local_shell` | Yes |  |

### OpenAI.LogProb

The log probability of a token.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array of [OpenAI.integer](#openaiinteger) |  | Yes |  |
| logprob | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| token | string |  | Yes |  |
| top_logprobs | array of [OpenAI.TopLogProb](#openaitoplogprob) |  | Yes |  |

### OpenAI.MCPListToolsTool

A tool available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | [OpenAI.MCPListToolsToolAnnotations](#openaimcplisttoolstoolannotations) (nullable) |  | No |  |
| description | string (nullable) |  | No |  |
| input_schema | [OpenAI.MCPListToolsToolInputSchema](#openaimcplisttoolstoolinputschema) |  | Yes |  |
| name | string | The name of the tool. | Yes |  |

### OpenAI.MCPListToolsToolAnnotations

**Type**: object


### OpenAI.MCPListToolsToolInputSchema

**Type**: object


### OpenAI.MCPTool

Give the model access to additional tools via remote Model Context Protocol
(MCP) servers. [Learn more about MCP](https://platform.openai.com/docs/guides/tools-remote-mcp).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| allowed_tools | array of string or [OpenAI.MCPToolFilter](#openaimcptoolfilter) |  | No |  |
| authorization | string | An OAuth access token that can be used with a remote MCP server, either<br>  with a custom MCP server URL or a service connector. Your application<br>  must handle the OAuth authorization flow and provide the token here. | No |  |
| connector_id | enum | Identifier for service connectors, like those available in ChatGPT. One of<br>  `server_url` or `connector_id` must be provided. Learn more about service<br>  connectors [here](https://platform.openai.com/docs/guides/tools-remote-mcp#connectors).<br>  Currently supported `connector_id` values are:<br>  - Dropbox: `connector_dropbox`<br>  - Gmail: `connector_gmail`<br>  - Google Calendar: `connector_googlecalendar`<br>  - Google Drive: `connector_googledrive`<br>  - Microsoft Teams: `connector_microsoftteams`<br>  - Outlook Calendar: `connector_outlookcalendar`<br>  - Outlook Email: `connector_outlookemail`<br>  - SharePoint: `connector_sharepoint`<br>Possible values: `connector_dropbox`, `connector_gmail`, `connector_googlecalendar`, `connector_googledrive`, `connector_microsoftteams`, `connector_outlookcalendar`, `connector_outlookemail`, `connector_sharepoint` | No |  |
| headers | object (nullable) |  | No |  |
| project_connection_id | string | The connection ID in the project for the MCP server. The connection stores authentication and other connection details needed to connect to the MCP server. | No |  |
| require_approval | object (see valid models below) |  | No |  |
| server_description | string | Optional description of the MCP server, used to provide more context. | No |  |
| server_label | string | A label for this MCP server, used to identify it in tool calls. | Yes |  |
| server_url | string | The URL for the MCP server. One of `server_url` or `connector_id` must be<br>  provided. | No |  |
| type | enum | The type of the MCP tool. Always `mcp`.<br>Possible values: `mcp` | Yes |  |

### OpenAI.MCPToolCallStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`incomplete`<br>`calling`<br>`failed` |

### OpenAI.MCPToolFilter

A filter object to specify which tools are allowed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| read_only | boolean | Indicates whether or not a tool modifies data or is read-only. If an<br>  MCP server is [annotated with `readOnlyHint`](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations-readonlyhint),<br>  it will match this filter. | No |  |
| tool_names | array of string | List of allowed tool names. | No |  |

### OpenAI.MCPToolRequireApproval

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| always | [OpenAI.MCPToolFilter](#openaimcptoolfilter) | A filter object to specify which tools are allowed. | No |  |
| never | [OpenAI.MCPToolFilter](#openaimcptoolfilter) | A filter object to specify which tools are allowed. | No |  |

### OpenAI.MessageContent

A content part that makes up an input or output item.


### Discriminator for OpenAI.MessageContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `text` | [OpenAI.TextContent](#openaitextcontent) |
| `summary_text` | [OpenAI.SummaryTextContent](#openaisummarytextcontent) |
| `computer_screenshot` | [OpenAI.ComputerScreenshotContent](#openaicomputerscreenshotcontent) |
| `input_text` | [OpenAI.MessageContentInputTextContent](#openaimessagecontentinputtextcontent) |
| `output_text` | [OpenAI.MessageContentOutputTextContent](#openaimessagecontentoutputtextcontent) |
| `reasoning_text` | [OpenAI.MessageContentReasoningTextContent](#openaimessagecontentreasoningtextcontent) |
| `refusal` | [OpenAI.MessageContentRefusalContent](#openaimessagecontentrefusalcontent) |
| `input_image` | [OpenAI.MessageContentInputImageContent](#openaimessagecontentinputimagecontent) |
| `input_file` | [OpenAI.MessageContentInputFileContent](#openaimessagecontentinputfilecontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.MessageContentType](#openaimessagecontenttype) |  | Yes |  |

### OpenAI.MessageContentInputFileContent

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string | The content of the file to be sent to the model. | No |  |
| file_id | string (nullable) |  | No |  |
| file_url | string | The URL of the file to be sent to the model. | No |  |
| filename | string | The name of the file to be sent to the model. | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.MessageContentInputImageContent

An image input to the model. Learn about [image inputs](https://platform.openai.com/docs/guides/vision).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | [OpenAI.ImageDetail](#openaiimagedetail) |  | Yes |  |
| file_id | string (nullable) |  | No |  |
| image_url | string |  | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.MessageContentInputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.MessageContentOutputTextContent

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array of [OpenAI.Annotation](#openaiannotation) | The annotations of the text output. | Yes |  |
| logprobs | array of [OpenAI.LogProb](#openailogprob) |  | No |  |
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.MessageContentReasoningTextContent

Reasoning text from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The reasoning text from the model. | Yes |  |
| type | enum | The type of the reasoning text. Always `reasoning_text`.<br>Possible values: `reasoning_text` | Yes |  |

### OpenAI.MessageContentRefusalContent

A refusal from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal explanation from the model. | Yes |  |
| type | enum | The type of the refusal. Always `refusal`.<br>Possible values: `refusal` | Yes |  |

### OpenAI.MessageContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `input_text`<br>`output_text`<br>`text`<br>`summary_text`<br>`reasoning_text`<br>`refusal`<br>`input_image`<br>`computer_screenshot`<br>`input_file` |

### OpenAI.MessageRole

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `unknown`<br>`user`<br>`assistant`<br>`system`<br>`critic`<br>`discriminator`<br>`developer`<br>`tool` |

### OpenAI.MessageStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`incomplete` |

### OpenAI.Metadata

Set of 16 key-value pairs that can be attached to an object. This can be
useful for storing additional information about the object in a structured
format, and querying for objects via API or the dashboard.
Keys are strings with a maximum length of 64 characters. Values are strings
with a maximum length of 512 characters.

**Type**: object


### OpenAI.ModelIdsCompaction

Model ID used to generate the response, like `gpt-5` or `o3`. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models) to browse and compare available models.

**Type**: [OpenAI.ModelIdsResponses](#openaimodelidsresponses) or string

Model ID used to generate the response, like `gpt-5` or `o3`. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models) to browse and compare available models.


### OpenAI.ModelIdsResponses

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `o1-pro`<br>`o1-pro-2025-03-19`<br>`o3-pro`<br>`o3-pro-2025-06-10`<br>`o3-deep-research`<br>`o3-deep-research-2025-06-26`<br>`o4-mini-deep-research`<br>`o4-mini-deep-research-2025-06-26`<br>`computer-use-preview`<br>`computer-use-preview-2025-03-11`<br>`gpt-5-codex`<br>`gpt-5-pro`<br>`gpt-5-pro-2025-10-06`<br>`gpt-5.1-codex-max` |

### OpenAI.ModelIdsShared

**Type**: string or [OpenAI.ChatModel](#openaichatmodel)


### OpenAI.Move

A mouse move action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a move action, this property is<br>  always set to `move`.<br>Possible values: `move` | Yes |  |
| x | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| y | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.OutputContent


### Discriminator for OpenAI.OutputContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `output_text` | [OpenAI.OutputContentOutputTextContent](#openaioutputcontentoutputtextcontent) |
| `refusal` | [OpenAI.OutputContentRefusalContent](#openaioutputcontentrefusalcontent) |
| `reasoning_text` | [OpenAI.OutputContentReasoningTextContent](#openaioutputcontentreasoningtextcontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.OutputContentType](#openaioutputcontenttype) |  | Yes |  |

### OpenAI.OutputContentOutputTextContent

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array of [OpenAI.Annotation](#openaiannotation) | The annotations of the text output. | Yes |  |
| logprobs | array of [OpenAI.LogProb](#openailogprob) |  | No |  |
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.OutputContentReasoningTextContent

Reasoning text from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The reasoning text from the model. | Yes |  |
| type | enum | The type of the reasoning text. Always `reasoning_text`.<br>Possible values: `reasoning_text` | Yes |  |

### OpenAI.OutputContentRefusalContent

A refusal from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal explanation from the model. | Yes |  |
| type | enum | The type of the refusal. Always `refusal`.<br>Possible values: `refusal` | Yes |  |

### OpenAI.OutputContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `output_text`<br>`refusal`<br>`reasoning_text` |

### OpenAI.OutputItem


### Discriminator for OpenAI.OutputItem

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `structured_outputs` | [StructuredOutputsOutputItem](#structuredoutputsoutputitem) |
| `workflow_action` | [WorkflowActionOutputItem](#workflowactionoutputitem) |
| `oauth_consent_request` | [OAuthConsentRequestOutputItem](#oauthconsentrequestoutputitem) |
| `memory_search_call` | [MemorySearchToolCallItemResource](#memorysearchtoolcallitemresource) |
| `output_message` | [OpenAI.OutputItemOutputMessage](#openaioutputitemoutputmessage) |
| `file_search_call` | [OpenAI.OutputItemFileSearchToolCall](#openaioutputitemfilesearchtoolcall) |
| `function_call` | [OpenAI.OutputItemFunctionToolCall](#openaioutputitemfunctiontoolcall) |
| `web_search_call` | [OpenAI.OutputItemWebSearchToolCall](#openaioutputitemwebsearchtoolcall) |
| `computer_call` | [OpenAI.OutputItemComputerToolCall](#openaioutputitemcomputertoolcall) |
| `reasoning` | [OpenAI.OutputItemReasoningItem](#openaioutputitemreasoningitem) |
| `compaction` | [OpenAI.OutputItemCompactionBody](#openaioutputitemcompactionbody) |
| `image_generation_call` | [OpenAI.OutputItemImageGenToolCall](#openaioutputitemimagegentoolcall) |
| `code_interpreter_call` | [OpenAI.OutputItemCodeInterpreterToolCall](#openaioutputitemcodeinterpretertoolcall) |
| `local_shell_call` | [OpenAI.OutputItemLocalShellToolCall](#openaioutputitemlocalshelltoolcall) |
| `shell_call` | [OpenAI.OutputItemFunctionShellCall](#openaioutputitemfunctionshellcall) |
| `shell_call_output` | [OpenAI.OutputItemFunctionShellCallOutput](#openaioutputitemfunctionshellcalloutput) |
| `apply_patch_call` | [OpenAI.OutputItemApplyPatchToolCall](#openaioutputitemapplypatchtoolcall) |
| `apply_patch_call_output` | [OpenAI.OutputItemApplyPatchToolCallOutput](#openaioutputitemapplypatchtoolcalloutput) |
| `mcp_call` | [OpenAI.OutputItemMcpToolCall](#openaioutputitemmcptoolcall) |
| `mcp_list_tools` | [OpenAI.OutputItemMcpListTools](#openaioutputitemmcplisttools) |
| `mcp_approval_request` | [OpenAI.OutputItemMcpApprovalRequest](#openaioutputitemmcpapprovalrequest) |
| `custom_tool_call` | [OpenAI.OutputItemCustomToolCall](#openaioutputitemcustomtoolcall) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| response_id | string | The response on which the item is created. | No |  |
| type | [OpenAI.OutputItemType](#openaioutputitemtype) |  | Yes |  |

### OpenAI.OutputItemApplyPatchToolCall

A tool call that applies file diffs by creating, deleting, or updating files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the apply patch tool call. Populated when this item is returned via API. | Yes |  |
| operation | [OpenAI.ApplyPatchFileOperation](#openaiapplypatchfileoperation) | One of the create_file, delete_file, or update_file operations applied via apply_patch. | Yes |  |
| └─ type | [OpenAI.ApplyPatchFileOperationType](#openaiapplypatchfileoperationtype) |  | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| status | [OpenAI.ApplyPatchCallStatus](#openaiapplypatchcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call`.<br>Possible values: `apply_patch_call` | Yes |  |

### OpenAI.OutputItemApplyPatchToolCallOutput

The output emitted by an apply patch tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call output. | No |  |
| id | string | The unique ID of the apply patch tool call output. Populated when this item is returned via API. | Yes |  |
| output | string (nullable) |  | No |  |
| response_id | string | The response on which the item is created. | No |  |
| status | [OpenAI.ApplyPatchCallOutputStatus](#openaiapplypatchcalloutputstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call_output`.<br>Possible values: `apply_patch_call_output` | Yes |  |

### OpenAI.OutputItemCodeInterpreterToolCall

A tool call to run code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| code | string (nullable) |  | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| id | string | The unique ID of the code interpreter tool call. | Yes |  |
| outputs | array of [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) or [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) |  | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| status | enum | The status of the code interpreter tool call. Valid values are `in_progress`, `completed`, `incomplete`, `interpreting`, and `failed`.<br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | The type of the code interpreter tool call. Always `code_interpreter_call`.<br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.OutputItemCompactionBody

A compaction item generated by the [`v1/responses/compact` API](https://platform.openai.com/docs/api-reference/responses/compact).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| created_by | string | The identifier of the actor that created the item. | No |  |
| encrypted_content | string | The encrypted content that was produced by compaction. | Yes |  |
| id | string | The unique ID of the compaction item. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| type | enum | The type of the item. Always `compaction`.<br>Possible values: `compaction` | Yes |  |

### OpenAI.OutputItemComputerToolCall

A tool call to a computer use tool. See the
[computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| id | string | The unique ID of the computer call. | Yes |  |
| pending_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The pending safety checks for the computer call. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the computer call. Always `computer_call`.<br>Possible values: `computer_call` | Yes |  |

### OpenAI.OutputItemCustomToolCall

A call to a custom tool created by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| call_id | string | An identifier used to map this custom tool call to a tool call output. | Yes |  |
| id | string | The unique ID of the custom tool call in the OpenAI platform. | No |  |
| input | string | The input for the custom tool call generated by the model. | Yes |  |
| name | string | The name of the custom tool being called. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| type | enum | The type of the custom tool call. Always `custom_tool_call`.<br>Possible values: `custom_tool_call` | Yes |  |

### OpenAI.OutputItemFileSearchToolCall

The results of a file search tool call. See the
[file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| id | string | The unique ID of the file search tool call. | Yes |  |
| queries | array of string | The queries used to search for files. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| results | array of [OpenAI.FileSearchToolCallResults](#openaifilesearchtoolcallresults) |  | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`,<br>  `searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | The type of the file search tool call. Always `file_search_call`.<br>Possible values: `file_search_call` | Yes |  |

### OpenAI.OutputItemFunctionShellCall

A tool call that executes one or more shell commands in a managed environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.FunctionShellAction](#openaifunctionshellaction) | Execute a shell command. | Yes |  |
| └─ commands | array of string |  | Yes |  |
| └─ max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| └─ timeout_ms | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the shell tool call. Populated when this item is returned via API. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| status | [OpenAI.LocalShellCallStatus](#openailocalshellcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `shell_call`.<br>Possible values: `shell_call` | Yes |  |

### OpenAI.OutputItemFunctionShellCallOutput

The output of a shell tool call that was emitted.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The identifier of the actor that created the item. | No |  |
| id | string | The unique ID of the shell call output. Populated when this item is returned via API. | Yes |  |
| max_output_length | [OpenAI.integer](#openaiinteger) (nullable) |  | Yes |  |
| output | array of [OpenAI.FunctionShellCallOutputContent](#openaifunctionshellcalloutputcontent) | An array of shell call output contents | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| type | enum | The type of the shell call output. Always `shell_call_output`.<br>Possible values: `shell_call_output` | Yes |  |

### OpenAI.OutputItemFunctionToolCall

A tool call to run a function. See the
[function calling guide](https://platform.openai.com/docs/guides/function-calling) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call. | No |  |
| name | string | The name of the function to run. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call. Always `function_call`.<br>Possible values: `function_call` | Yes |  |

### OpenAI.OutputItemImageGenToolCall

An image generation request made by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| id | string | The unique ID of the image generation call. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| result | string (nullable) |  | Yes |  |
| status | enum | The status of the image generation call.<br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | The type of the image generation call. Always `image_generation_call`.<br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.OutputItemLocalShellToolCall

A tool call to run a command on the local shell.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| id | string | The unique ID of the local shell call. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| status | enum | The status of the local shell call.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the local shell call. Always `local_shell_call`.<br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.OutputItemMcpApprovalRequest

A request for human approval of a tool invocation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| id | string | The unique ID of the approval request. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | The type of the item. Always `mcp_approval_request`.<br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.OutputItemMcpListTools

A list of tools available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the list. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array of [OpenAI.MCPListToolsTool](#openaimcplisttoolstool) | The tools available on the server. | Yes |  |
| type | enum | The type of the item. Always `mcp_list_tools`.<br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.OutputItemMcpToolCall

An invocation of a tool on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| approval_request_id | string (nullable) |  | No |  |
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string (nullable) |  | No |  |
| id | string | The unique ID of the tool call. | Yes |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string (nullable) |  | No |  |
| response_id | string | The response on which the item is created. | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| status | [OpenAI.MCPToolCallStatus](#openaimcptoolcallstatus) |  | No |  |
| type | enum | The type of the item. Always `mcp_call`.<br>Possible values: `mcp_call` | Yes |  |

### OpenAI.OutputItemOutputMessage

An output message from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| content | array of [OpenAI.OutputMessageContent](#openaioutputmessagecontent) | The content of the output message. | Yes |  |
| id | string | The unique ID of the output message. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| role | enum | The role of the output message. Always `assistant`.<br>Possible values: `assistant` | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the output message. Always `message`.<br>Possible values: `output_message` | Yes |  |

### OpenAI.OutputItemReasoningItem

A description of the chain of thought used by a reasoning model while generating
a response. Be sure to include these items in your `input` to the Responses API
for subsequent turns of a conversation if you are manually
[managing context](https://platform.openai.com/docs/guides/conversation-state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| content | array of [OpenAI.ReasoningTextContent](#openaireasoningtextcontent) | Reasoning text content. | No |  |
| encrypted_content | string (nullable) |  | No |  |
| id | string | The unique identifier of the reasoning content. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| summary | array of [OpenAI.Summary](#openaisummary) | Reasoning summary content. | Yes |  |
| type | enum | The type of the object. Always `reasoning`.<br>Possible values: `reasoning` | Yes |  |

### OpenAI.OutputItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `output_message`<br>`file_search_call`<br>`function_call`<br>`web_search_call`<br>`computer_call`<br>`reasoning`<br>`compaction`<br>`image_generation_call`<br>`code_interpreter_call`<br>`local_shell_call`<br>`shell_call`<br>`shell_call_output`<br>`apply_patch_call`<br>`apply_patch_call_output`<br>`mcp_call`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`custom_tool_call`<br>`structured_outputs`<br>`oauth_consent_request`<br>`memory_search_call`<br>`workflow_action` |

### OpenAI.OutputItemWebSearchToolCall

The results of a web search tool call. See the
[web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) or [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) or [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) | An object describing the specific action taken in this web search call.<br>  Includes details on how the model used the web (search, open_page, find). | Yes |  |
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| id | string | The unique ID of the web search tool call. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | The type of the web search tool call. Always `web_search_call`.<br>Possible values: `web_search_call` | Yes |  |

### OpenAI.OutputMessageContent


### Discriminator for OpenAI.OutputMessageContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `output_text` | [OpenAI.OutputMessageContentOutputTextContent](#openaioutputmessagecontentoutputtextcontent) |
| `refusal` | [OpenAI.OutputMessageContentRefusalContent](#openaioutputmessagecontentrefusalcontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.OutputMessageContentType](#openaioutputmessagecontenttype) |  | Yes |  |

### OpenAI.OutputMessageContentOutputTextContent

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array of [OpenAI.Annotation](#openaiannotation) | The annotations of the text output. | Yes |  |
| logprobs | array of [OpenAI.LogProb](#openailogprob) |  | No |  |
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.OutputMessageContentRefusalContent

A refusal from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal explanation from the model. | Yes |  |
| type | enum | The type of the refusal. Always `refusal`.<br>Possible values: `refusal` | Yes |  |

### OpenAI.OutputMessageContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `output_text`<br>`refusal` |

### OpenAI.Prompt

Reference to a prompt template and its variables.
[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique identifier of the prompt template to use. | Yes |  |
| variables | [OpenAI.ResponsePromptVariables](#openairesponsepromptvariables) (nullable) | Optional map of values to substitute in for variables in your<br>prompt. The substitution values can either be strings, or other<br>Response input types like images or files. | No |  |
| version | string (nullable) |  | No |  |

### OpenAI.RankerVersionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `auto`<br>`default-2024-11-15` |

### OpenAI.RankingOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hybrid_search | [OpenAI.HybridSearchOptions](#openaihybridsearchoptions) |  | No |  |
| └─ embedding_weight | [OpenAI.numeric](#openainumeric) | The weight of the embedding in the reciprocal ranking fusion. | Yes |  |
| └─ text_weight | [OpenAI.numeric](#openainumeric) | The weight of the text in the reciprocal ranking fusion. | Yes |  |
| ranker | [OpenAI.RankerVersionType](#openairankerversiontype) |  | No |  |
| score_threshold | [OpenAI.numeric](#openainumeric) |  | No |  |

### OpenAI.Reasoning

**gpt-5 and o-series models only**
Configuration options for
reasoning models.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| generate_summary | enum | <br>Possible values: `auto`, `concise`, `detailed` | No |  |
| summary | enum | <br>Possible values: `auto`, `concise`, `detailed` | No |  |

### OpenAI.ReasoningEffort

Constrains effort on reasoning for
reasoning models.
Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing
reasoning effort can result in faster responses and fewer tokens used
on reasoning in a response.
- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.
- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.
- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.
- `xhigh` is supported for all models after `gpt-5.1-codex-max`.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Nullable** | Yes |
| **Values** | `none`<br>`minimal`<br>`low`<br>`medium`<br>`high`<br>`xhigh` |

### OpenAI.ReasoningTextContent

Reasoning text from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The reasoning text from the model. | Yes |  |
| type | enum | The type of the reasoning text. Always `reasoning_text`.<br>Possible values: `reasoning_text` | Yes |  |

### OpenAI.Response

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) (nullable) |  | Yes |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| background | boolean (nullable) |  | No |  |
| completed_at | integer |  | No |  |
| conversation | [OpenAI.ConversationReference](#openaiconversationreference) (nullable) | The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation. | No |  |
| └─ id | string | The unique ID of the conversation that this response was associated with. | Yes |  |
| created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| error | [OpenAI.ResponseError](#openairesponseerror) (nullable) | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ code | [OpenAI.ResponseErrorCode](#openairesponseerrorcode) | The error code for the response. | Yes |  |
| └─ message | string | A human-readable description of the error. | Yes |  |
| id | string | Unique identifier for this Response. | Yes |  |
| incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) (nullable) |  | Yes |  |
| └─ reason | enum | <br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| instructions | string or array of [OpenAI.InputItem](#openaiinputitem) |  | Yes |  |
| max_output_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| max_tool_calls | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| model | string | The model deployment to use for the creation of this response. | No |  |
| object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| output_text | string (nullable) |  | No |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| previous_response_id | string (nullable) |  | No |  |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| prompt_cache_retention | enum | <br>Possible values: `in-memory`, `24h` | No |  |
| reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| └─ generate_summary | enum | <br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | <br>Possible values: `auto`, `concise`, `detailed` | No |  |
| safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| service_tier | [OpenAI.ServiceTier](#openaiservicetier) | Specifies the processing type used for serving the request.<br>- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.<br>- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.<br>- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.<br>- When not set, the default behavior is 'auto'.<br>When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter. | No |  |
| status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) |  | No |  |
| tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| top_logprobs | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| truncation | enum | <br>Possible values: `auto`, `disabled` | No |  |
| usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |

### OpenAI.ResponseAudioDeltaEvent

Emitted when there is a partial audio response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | A chunk of Base64 encoded response audio bytes. | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.audio.delta`.<br>Possible values: `response.audio.delta` | Yes |  |

### OpenAI.ResponseAudioDoneEvent

Emitted when the audio response is complete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.audio.done`.<br>Possible values: `response.audio.done` | Yes |  |

### OpenAI.ResponseAudioTranscriptDeltaEvent

Emitted when there is a partial transcript of audio.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The partial transcript of the audio response. | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.audio.transcript.delta`.<br>Possible values: `response.audio.transcript.delta` | Yes |  |

### OpenAI.ResponseAudioTranscriptDoneEvent

Emitted when the full audio transcript is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.audio.transcript.done`.<br>Possible values: `response.audio.transcript.done` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCodeDeltaEvent

Emitted when a partial code snippet is streamed by the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The partial code snippet being streamed by the code interpreter. | Yes |  |
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call_code.delta`.<br>Possible values: `response.code_interpreter_call_code.delta` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCodeDoneEvent

Emitted when the code snippet is finalized by the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The final code snippet output by the code interpreter. | Yes |  |
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call_code.done`.<br>Possible values: `response.code_interpreter_call_code.done` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCompletedEvent

Emitted when the code interpreter call is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.completed`.<br>Possible values: `response.code_interpreter_call.completed` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallInProgressEvent

Emitted when a code interpreter call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.in_progress`.<br>Possible values: `response.code_interpreter_call.in_progress` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallInterpretingEvent

Emitted when the code interpreter is actively interpreting the code snippet.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.interpreting`.<br>Possible values: `response.code_interpreter_call.interpreting` | Yes |  |

### OpenAI.ResponseCompletedEvent

Emitted when the model response is complete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ agent_reference | [AgentReference](#agentreference) (nullable) | The agent used for this response | Yes |  |
| └─ background | boolean (nullable) |  | No |  |
| └─ completed_at | integer (nullable) |  | No |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) (nullable) | The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation. | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) (nullable) | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) (nullable) |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) (nullable) |  | Yes |  |
| └─ max_output_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ max_tool_calls | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ model | string | The model deployment to use for the creation of this response. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string (nullable) |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string (nullable) |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | enum | <br>Possible values: `in-memory`, `24h` | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ service_tier | [OpenAI.ServiceTier](#openaiservicetier) | Specifies the processing type used for serving the request.<br>- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.<br>- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.<br>- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.<br>- When not set, the default behavior is 'auto'.<br>When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) |  | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ truncation | enum | <br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.completed`.<br>Possible values: `response.completed` | Yes |  |

### OpenAI.ResponseContentPartAddedEvent

Emitted when a new content part is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| item_id | string | The ID of the output item that the content part was added to. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| part | [OpenAI.OutputContent](#openaioutputcontent) |  | Yes |  |
| └─ type | [OpenAI.OutputContentType](#openaioutputcontenttype) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.content_part.added`.<br>Possible values: `response.content_part.added` | Yes |  |

### OpenAI.ResponseContentPartDoneEvent

Emitted when a content part is done.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| item_id | string | The ID of the output item that the content part was added to. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| part | [OpenAI.OutputContent](#openaioutputcontent) |  | Yes |  |
| └─ type | [OpenAI.OutputContentType](#openaioutputcontenttype) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.content_part.done`.<br>Possible values: `response.content_part.done` | Yes |  |

### OpenAI.ResponseCreatedEvent

An event that is emitted when a response is created.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ agent_reference | [AgentReference](#agentreference) (nullable) | The agent used for this response | Yes |  |
| └─ background | boolean (nullable) |  | No |  |
| └─ completed_at | integer (nullable) |  | No |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) (nullable) | The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation. | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) (nullable) | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) (nullable) |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) (nullable) |  | Yes |  |
| └─ max_output_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ max_tool_calls | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ model | string | The model deployment to use for the creation of this response. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string (nullable) |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string (nullable) |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | enum | <br>Possible values: `in-memory`, `24h` | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ service_tier | [OpenAI.ServiceTier](#openaiservicetier) | Specifies the processing type used for serving the request.<br>- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.<br>- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.<br>- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.<br>- When not set, the default behavior is 'auto'.<br>When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) |  | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ truncation | enum | <br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.created`.<br>Possible values: `response.created` | Yes |  |

### OpenAI.ResponseCustomToolCallInputDeltaEvent

Event representing a delta (partial update) to the input of a custom tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The incremental input data (delta) for the custom tool call. | Yes |  |
| item_id | string | Unique identifier for the API item associated with this event. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The event type identifier.<br>Possible values: `response.custom_tool_call_input.delta` | Yes |  |

### OpenAI.ResponseCustomToolCallInputDoneEvent

Event indicating that input for a custom tool call is complete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string | The complete input data for the custom tool call. | Yes |  |
| item_id | string | Unique identifier for the API item associated with this event. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The event type identifier.<br>Possible values: `response.custom_tool_call_input.done` | Yes |  |

### OpenAI.ResponseError

An error object returned when the model fails to generate a Response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | [OpenAI.ResponseErrorCode](#openairesponseerrorcode) | The error code for the response. | Yes |  |
| message | string | A human-readable description of the error. | Yes |  |

### OpenAI.ResponseErrorCode

The error code for the response.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `server_error`<br>`rate_limit_exceeded`<br>`invalid_prompt`<br>`vector_store_timeout`<br>`invalid_image`<br>`invalid_image_format`<br>`invalid_base64_image`<br>`invalid_image_url`<br>`image_too_large`<br>`image_too_small`<br>`image_parse_error`<br>`image_content_policy_violation`<br>`invalid_image_mode`<br>`image_file_too_large`<br>`unsupported_image_media_type`<br>`empty_image_file`<br>`failed_to_download_image`<br>`image_file_not_found` |

### OpenAI.ResponseErrorEvent

Emitted when an error occurs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string (nullable) |  | Yes |  |
| message | string | The error message. | Yes |  |
| param | string (nullable) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `error`.<br>Possible values: `error` | Yes |  |

### OpenAI.ResponseFailedEvent

An event that is emitted when a response fails.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ agent_reference | [AgentReference](#agentreference) (nullable) | The agent used for this response | Yes |  |
| └─ background | boolean (nullable) |  | No |  |
| └─ completed_at | integer (nullable) |  | No |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) (nullable) | The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation. | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) (nullable) | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) (nullable) |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) (nullable) |  | Yes |  |
| └─ max_output_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ max_tool_calls | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ model | string | The model deployment to use for the creation of this response. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string (nullable) |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string (nullable) |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | enum | <br>Possible values: `in-memory`, `24h` | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ service_tier | [OpenAI.ServiceTier](#openaiservicetier) | Specifies the processing type used for serving the request.<br>- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.<br>- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.<br>- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.<br>- When not set, the default behavior is 'auto'.<br>When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) |  | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ truncation | enum | <br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.failed`.<br>Possible values: `response.failed` | Yes |  |

### OpenAI.ResponseFileSearchCallCompletedEvent

Emitted when a file search call is completed (results found).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the output item that the file search call is initiated. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.file_search_call.completed`.<br>Possible values: `response.file_search_call.completed` | Yes |  |

### OpenAI.ResponseFileSearchCallInProgressEvent

Emitted when a file search call is initiated.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the output item that the file search call is initiated. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.file_search_call.in_progress`.<br>Possible values: `response.file_search_call.in_progress` | Yes |  |

### OpenAI.ResponseFileSearchCallSearchingEvent

Emitted when a file search is currently searching.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the output item that the file search call is initiated. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.file_search_call.searching`.<br>Possible values: `response.file_search_call.searching` | Yes |  |

### OpenAI.ResponseFormatJsonObject

JSON object response format. An older method of generating JSON responses.
Using `json_schema` is recommended for models that support it. Note that the
model will not generate JSON without a system or user message instructing it
to do so.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `json_object`.<br>Possible values: `json_object` | Yes |  |

### OpenAI.ResponseFormatJsonSchema

JSON Schema response format. Used to generate structured JSON responses.
Learn more about [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| json_schema | [OpenAI.ResponseFormatJsonSchemaJsonSchema](#openairesponseformatjsonschemajsonschema) |  | Yes |  |
| └─ description | string |  | No |  |
| └─ name | string |  | Yes |  |
| └─ schema | [OpenAI.ResponseFormatJsonSchemaSchema](#openairesponseformatjsonschemaschema) | The schema for the response format, described as a JSON Schema object.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | No |  |
| └─ strict | boolean (nullable) |  | No |  |
| type | enum | The type of response format being defined. Always `json_schema`.<br>Possible values: `json_schema` | Yes |  |

### OpenAI.ResponseFormatJsonSchemaJsonSchema

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string |  | No |  |
| name | string |  | Yes |  |
| schema | [OpenAI.ResponseFormatJsonSchemaSchema](#openairesponseformatjsonschemaschema) | The schema for the response format, described as a JSON Schema object.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | No |  |
| strict | boolean (nullable) |  | No |  |

### OpenAI.ResponseFormatJsonSchemaSchema

The schema for the response format, described as a JSON Schema object.
Learn how to build JSON schemas [here](https://json-schema.org/).

**Type**: object


### OpenAI.ResponseFormatText

Default response format. Used to generate text responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.ResponseFunctionCallArgumentsDeltaEvent

Emitted when there is a partial function-call arguments delta.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The function-call arguments delta that is added. | Yes |  |
| item_id | string | The ID of the output item that the function-call arguments delta is added to. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.function_call_arguments.delta`.<br>Possible values: `response.function_call_arguments.delta` | Yes |  |

### OpenAI.ResponseFunctionCallArgumentsDoneEvent

Emitted when function-call arguments are finalized.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | The function-call arguments. | Yes |  |
| item_id | string | The ID of the item. | Yes |  |
| name | string | The name of the function that was called. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | <br>Possible values: `response.function_call_arguments.done` | Yes |  |

### OpenAI.ResponseImageGenCallCompletedEvent

Emitted when an image generation tool call has completed and the final image is available.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.completed'.<br>Possible values: `response.image_generation_call.completed` | Yes |  |

### OpenAI.ResponseImageGenCallGeneratingEvent

Emitted when an image generation tool call is actively generating an image (intermediate state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.generating'.<br>Possible values: `response.image_generation_call.generating` | Yes |  |

### OpenAI.ResponseImageGenCallInProgressEvent

Emitted when an image generation tool call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.in_progress'.<br>Possible values: `response.image_generation_call.in_progress` | Yes |  |

### OpenAI.ResponseImageGenCallPartialImageEvent

Emitted when a partial image is available during image generation streaming.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| partial_image_b64 | string | Base64-encoded partial image data, suitable for rendering as an image. | Yes |  |
| partial_image_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.partial_image'.<br>Possible values: `response.image_generation_call.partial_image` | Yes |  |

### OpenAI.ResponseInProgressEvent

Emitted when the response is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ agent_reference | [AgentReference](#agentreference) (nullable) | The agent used for this response | Yes |  |
| └─ background | boolean (nullable) |  | No |  |
| └─ completed_at | integer (nullable) |  | No |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) (nullable) | The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation. | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) (nullable) | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) (nullable) |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) (nullable) |  | Yes |  |
| └─ max_output_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ max_tool_calls | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ model | string | The model deployment to use for the creation of this response. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string (nullable) |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string (nullable) |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | enum | <br>Possible values: `in-memory`, `24h` | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ service_tier | [OpenAI.ServiceTier](#openaiservicetier) | Specifies the processing type used for serving the request.<br>- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.<br>- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.<br>- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.<br>- When not set, the default behavior is 'auto'.<br>When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) |  | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ truncation | enum | <br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.in_progress`.<br>Possible values: `response.in_progress` | Yes |  |

### OpenAI.ResponseIncompleteDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| reason | enum | <br>Possible values: `max_output_tokens`, `content_filter` | No |  |

### OpenAI.ResponseIncompleteEvent

An event that is emitted when a response finishes as incomplete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ agent_reference | [AgentReference](#agentreference) (nullable) | The agent used for this response | Yes |  |
| └─ background | boolean (nullable) |  | No |  |
| └─ completed_at | integer (nullable) |  | No |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) (nullable) | The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation. | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) (nullable) | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) (nullable) |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) (nullable) |  | Yes |  |
| └─ max_output_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ max_tool_calls | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ model | string | The model deployment to use for the creation of this response. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string (nullable) |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string (nullable) |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | enum | <br>Possible values: `in-memory`, `24h` | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ service_tier | [OpenAI.ServiceTier](#openaiservicetier) | Specifies the processing type used for serving the request.<br>- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.<br>- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.<br>- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.<br>- When not set, the default behavior is 'auto'.<br>When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) |  | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ truncation | enum | <br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.incomplete`.<br>Possible values: `response.incomplete` | Yes |  |

### OpenAI.ResponseLogProb

A logprob is the logarithmic probability that the model assigns to producing
a particular token at a given position in the sequence. Less-negative (higher)
logprob values indicate greater model confidence in that token choice.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logprob | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| token | string | A possible text token. | Yes |  |
| top_logprobs | array of [OpenAI.ResponseLogProbTopLogprobs](#openairesponselogprobtoplogprobs) | The log probability of the top 20 most likely tokens. | No |  |

### OpenAI.ResponseLogProbTopLogprobs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logprob | [OpenAI.numeric](#openainumeric) |  | No |  |
| token | string |  | No |  |

### OpenAI.ResponseMCPCallArgumentsDeltaEvent

Emitted when there is a delta (partial update) to the arguments of an MCP tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | A JSON string containing the partial update to the arguments for the MCP tool call. | Yes |  |
| item_id | string | The unique identifier of the MCP tool call item being processed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call_arguments.delta'.<br>Possible values: `response.mcp_call_arguments.delta` | Yes |  |

### OpenAI.ResponseMCPCallArgumentsDoneEvent

Emitted when the arguments for an MCP tool call are finalized.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string containing the finalized arguments for the MCP tool call. | Yes |  |
| item_id | string | The unique identifier of the MCP tool call item being processed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call_arguments.done'.<br>Possible values: `response.mcp_call_arguments.done` | Yes |  |

### OpenAI.ResponseMCPCallCompletedEvent

Emitted when an MCP  tool call has completed successfully.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the MCP tool call item that completed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call.completed'.<br>Possible values: `response.mcp_call.completed` | Yes |  |

### OpenAI.ResponseMCPCallFailedEvent

Emitted when an MCP  tool call has failed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the MCP tool call item that failed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call.failed'.<br>Possible values: `response.mcp_call.failed` | Yes |  |

### OpenAI.ResponseMCPCallInProgressEvent

Emitted when an MCP  tool call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the MCP tool call item being processed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call.in_progress'.<br>Possible values: `response.mcp_call.in_progress` | Yes |  |

### OpenAI.ResponseMCPListToolsCompletedEvent

Emitted when the list of available MCP tools has been successfully retrieved.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the MCP tool call item that produced this output. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_list_tools.completed'.<br>Possible values: `response.mcp_list_tools.completed` | Yes |  |

### OpenAI.ResponseMCPListToolsFailedEvent

Emitted when the attempt to list available MCP tools has failed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the MCP tool call item that failed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_list_tools.failed'.<br>Possible values: `response.mcp_list_tools.failed` | Yes |  |

### OpenAI.ResponseMCPListToolsInProgressEvent

Emitted when the system is in the process of retrieving the list of available MCP tools.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the MCP tool call item that is being processed. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_list_tools.in_progress'.<br>Possible values: `response.mcp_list_tools.in_progress` | Yes |  |

### OpenAI.ResponseOutputItemAddedEvent

Emitted when a new output item is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item | [OpenAI.OutputItem](#openaioutputitem) |  | Yes |  |
| └─ agent_reference | [AgentReference](#agentreference) | The agent that created the item. | No |  |
| └─ response_id | string | The response on which the item is created. | No |  |
| └─ type | [OpenAI.OutputItemType](#openaioutputitemtype) |  | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.output_item.added`.<br>Possible values: `response.output_item.added` | Yes |  |

### OpenAI.ResponseOutputItemDoneEvent

Emitted when an output item is marked done.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item | [OpenAI.OutputItem](#openaioutputitem) |  | Yes |  |
| └─ agent_reference | [AgentReference](#agentreference) | The agent that created the item. | No |  |
| └─ response_id | string | The response on which the item is created. | No |  |
| └─ type | [OpenAI.OutputItemType](#openaioutputitemtype) |  | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.output_item.done`.<br>Possible values: `response.output_item.done` | Yes |  |

### OpenAI.ResponseOutputTextAnnotationAddedEvent

Emitted when an annotation is added to output text content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotation | [OpenAI.Annotation](#openaiannotation) | An annotation that applies to a span of output text. | Yes |  |
| └─ type | [OpenAI.AnnotationType](#openaiannotationtype) |  | Yes |  |
| annotation_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| item_id | string | The unique identifier of the item to which the annotation is being added. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.output_text.annotation.added'.<br>Possible values: `response.output_text.annotation.added` | Yes |  |

### OpenAI.ResponsePromptVariables

Optional map of values to substitute in for variables in your
prompt. The substitution values can either be strings, or other
Response input types like images or files.

**Type**: object


### OpenAI.ResponseQueuedEvent

Emitted when a response is queued and waiting to be processed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ agent_reference | [AgentReference](#agentreference) (nullable) | The agent used for this response | Yes |  |
| └─ background | boolean (nullable) |  | No |  |
| └─ completed_at | integer (nullable) |  | No |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) (nullable) | The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation. | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) (nullable) | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) (nullable) |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) (nullable) |  | Yes |  |
| └─ max_output_tokens | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ max_tool_calls | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ model | string | The model deployment to use for the creation of this response. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string (nullable) |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string (nullable) |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | enum | <br>Possible values: `in-memory`, `24h` | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ service_tier | [OpenAI.ServiceTier](#openaiservicetier) | Specifies the processing type used for serving the request.<br>- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.<br>- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.<br>- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.<br>- When not set, the default behavior is 'auto'.<br>When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) |  | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | [OpenAI.integer](#openaiinteger) (nullable) |  | No |  |
| └─ top_p | [OpenAI.numeric](#openainumeric) (nullable) |  | No | 1 |
| └─ truncation | enum | <br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always 'response.queued'.<br>Possible values: `response.queued` | Yes |  |

### OpenAI.ResponseReasoningSummaryPartAddedEvent

Emitted when a new reasoning summary part is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the item this summary part is associated with. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| part | [OpenAI.ResponseReasoningSummaryPartAddedEventPart](#openairesponsereasoningsummarypartaddedeventpart) |  | Yes |  |
| └─ text | string |  | Yes |  |
| └─ type | enum | <br>Possible values: `summary_text` | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| summary_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_part.added`.<br>Possible values: `response.reasoning_summary_part.added` | Yes |  |

### OpenAI.ResponseReasoningSummaryPartAddedEventPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | Yes |  |
| type | enum | <br>Possible values: `summary_text` | Yes |  |

### OpenAI.ResponseReasoningSummaryPartDoneEvent

Emitted when a reasoning summary part is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the item this summary part is associated with. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| part | [OpenAI.ResponseReasoningSummaryPartDoneEventPart](#openairesponsereasoningsummarypartdoneeventpart) |  | Yes |  |
| └─ text | string |  | Yes |  |
| └─ type | enum | <br>Possible values: `summary_text` | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| summary_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_part.done`.<br>Possible values: `response.reasoning_summary_part.done` | Yes |  |

### OpenAI.ResponseReasoningSummaryPartDoneEventPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | Yes |  |
| type | enum | <br>Possible values: `summary_text` | Yes |  |

### OpenAI.ResponseReasoningSummaryTextDeltaEvent

Emitted when a delta is added to a reasoning summary text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The text delta that was added to the summary. | Yes |  |
| item_id | string | The ID of the item this summary text delta is associated with. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| summary_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_text.delta`.<br>Possible values: `response.reasoning_summary_text.delta` | Yes |  |

### OpenAI.ResponseReasoningSummaryTextDoneEvent

Emitted when a reasoning summary text is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the item this summary text is associated with. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| summary_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| text | string | The full text of the completed reasoning summary. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_text.done`.<br>Possible values: `response.reasoning_summary_text.done` | Yes |  |

### OpenAI.ResponseReasoningTextDeltaEvent

Emitted when a delta is added to a reasoning text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| delta | string | The text delta that was added to the reasoning content. | Yes |  |
| item_id | string | The ID of the item this reasoning text delta is associated with. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_text.delta`.<br>Possible values: `response.reasoning_text.delta` | Yes |  |

### OpenAI.ResponseReasoningTextDoneEvent

Emitted when a reasoning text is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| item_id | string | The ID of the item this reasoning text is associated with. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| text | string | The full text of the completed reasoning content. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_text.done`.<br>Possible values: `response.reasoning_text.done` | Yes |  |

### OpenAI.ResponseRefusalDeltaEvent

Emitted when there is a partial refusal text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| delta | string | The refusal text that is added. | Yes |  |
| item_id | string | The ID of the output item that the refusal text is added to. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.refusal.delta`.<br>Possible values: `response.refusal.delta` | Yes |  |

### OpenAI.ResponseRefusalDoneEvent

Emitted when refusal text is finalized.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| item_id | string | The ID of the output item that the refusal text is finalized. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| refusal | string | The refusal text that is finalized. | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.refusal.done`.<br>Possible values: `response.refusal.done` | Yes |  |

### OpenAI.ResponseStreamOptions

Options for streaming responses. Only set this when you set `stream: true`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include_obfuscation | boolean | When true, stream obfuscation will be enabled. Stream obfuscation adds<br>  random characters to an `obfuscation` field on streaming delta events to<br>  normalize payload sizes as a mitigation to certain side-channel attacks.<br>  These obfuscation fields are included by default, but add a small amount<br>  of overhead to the data stream. You can set `include_obfuscation` to<br>  false to optimize for bandwidth if you trust the network links between<br>  your application and the OpenAI API. | No |  |

### OpenAI.ResponseTextDeltaEvent

Emitted when there is an additional text delta.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| delta | string | The text delta that was added. | Yes |  |
| item_id | string | The ID of the output item that the text delta was added to. | Yes |  |
| logprobs | array of [OpenAI.ResponseLogProb](#openairesponselogprob) | The log probabilities of the tokens in the delta. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.output_text.delta`.<br>Possible values: `response.output_text.delta` | Yes |  |

### OpenAI.ResponseTextDoneEvent

Emitted when text content is finalized.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| item_id | string | The ID of the output item that the text content is finalized. | Yes |  |
| logprobs | array of [OpenAI.ResponseLogProb](#openairesponselogprob) | The log probabilities of the tokens in the delta. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| text | string | The text content that is finalized. | Yes |  |
| type | enum | The type of the event. Always `response.output_text.done`.<br>Possible values: `response.output_text.done` | Yes |  |

### OpenAI.ResponseTextParam

Configuration options for a text response from the model. Can be plain
text or structured JSON data. Learn more:
- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.TextResponseFormatConfiguration](#openaitextresponseformatconfiguration) | An object specifying the format that the model must output.<br>Configuring `{ "type": "json_schema" }` enables Structured Outputs,<br>which ensures the model will match your supplied JSON schema. Learn more in the<br><br>The default format is `{ "type": "text" }` with no additional options.<br>*Not recommended for gpt-4o and newer models:**<br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | No |  |
| verbosity | [OpenAI.Verbosity](#openaiverbosity) | Constrains the verbosity of the model's response. Lower values will result in<br>more concise responses, while higher values will result in more verbose responses.<br>Currently supported values are `low`, `medium`, and `high`. | No |  |

### OpenAI.ResponseUsage

Represents token usage details including input tokens, output tokens,
a breakdown of output tokens, and the total tokens used.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| input_tokens_details | [OpenAI.ResponseUsageInputTokensDetails](#openairesponseusageinputtokensdetails) |  | Yes |  |
| └─ cached_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| output_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| output_tokens_details | [OpenAI.ResponseUsageOutputTokensDetails](#openairesponseusageoutputtokensdetails) |  | Yes |  |
| └─ reasoning_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| total_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.ResponseUsageInputTokensDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cached_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.ResponseUsageOutputTokensDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| reasoning_tokens | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.ResponseWebSearchCallCompletedEvent

Emitted when a web search call is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | Unique ID for the output item associated with the web search call. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.web_search_call.completed`.<br>Possible values: `response.web_search_call.completed` | Yes |  |

### OpenAI.ResponseWebSearchCallInProgressEvent

Emitted when a web search call is initiated.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | Unique ID for the output item associated with the web search call. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.web_search_call.in_progress`.<br>Possible values: `response.web_search_call.in_progress` | Yes |  |

### OpenAI.ResponseWebSearchCallSearchingEvent

Emitted when a web search call is executing.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | Unique ID for the output item associated with the web search call. | Yes |  |
| output_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| sequence_number | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | The type of the event. Always `response.web_search_call.searching`.<br>Possible values: `response.web_search_call.searching` | Yes |  |

### OpenAI.Screenshot

A screenshot action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a screenshot action, this property is<br>  always set to `screenshot`.<br>Possible values: `screenshot` | Yes |  |

### OpenAI.Scroll

A scroll action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| scroll_x | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| scroll_y | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| type | enum | Specifies the event type. For a scroll action, this property is<br>  always set to `scroll`.<br>Possible values: `scroll` | Yes |  |
| x | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| y | [OpenAI.integer](#openaiinteger) |  | Yes |  |

### OpenAI.SearchContextSize

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `low`<br>`medium`<br>`high` |

### OpenAI.ServiceTier

Specifies the processing type used for serving the request.
- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.
- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.
- If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or '[priority](https://openai.com/api-priority-processing/)', then the request will be processed with the corresponding service tier.
- When not set, the default behavior is 'auto'.
When the `service_tier` parameter is set, the response body will include the `service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Nullable** | Yes |
| **Values** | `auto`<br>`default`<br>`flex`<br>`scale`<br>`priority` |

### OpenAI.SpecificApplyPatchParam

Forces the model to call the apply_patch tool when executing a tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The tool to call. Always `apply_patch`.<br>Possible values: `apply_patch` | Yes |  |

### OpenAI.SpecificFunctionShellParam

Forces the model to call the shell tool when a tool call is required.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The tool to call. Always `shell`.<br>Possible values: `shell` | Yes |  |

### OpenAI.Summary

A summary text from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | A summary of the reasoning output from the model so far. | Yes |  |
| type | enum | The type of the object. Always `summary_text`.<br>Possible values: `summary_text` | Yes |  |

### OpenAI.SummaryTextContent

A summary text from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | A summary of the reasoning output from the model so far. | Yes |  |
| type | enum | The type of the object. Always `summary_text`.<br>Possible values: `summary_text` | Yes |  |

### OpenAI.TextContent

A text content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | Yes |  |
| type | enum | <br>Possible values: `text` | Yes |  |

### OpenAI.TextResponseFormatConfiguration

An object specifying the format that the model must output.
Configuring `{ "type": "json_schema" }` enables Structured Outputs,
which ensures the model will match your supplied JSON schema. Learn more in the

The default format is `{ "type": "text" }` with no additional options.
*Not recommended for gpt-4o and newer models:**
Setting to `{ "type": "json_object" }` enables the older JSON mode, which
ensures the message the model generates is valid JSON. Using `json_schema`
is preferred for models that support it.


### Discriminator for OpenAI.TextResponseFormatConfiguration

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `json_schema` | [OpenAI.TextResponseFormatJsonSchema](#openaitextresponseformatjsonschema) |
| `text` | [OpenAI.TextResponseFormatConfigurationResponseFormatText](#openaitextresponseformatconfigurationresponseformattext) |
| `json_object` | [OpenAI.TextResponseFormatConfigurationResponseFormatJsonObject](#openaitextresponseformatconfigurationresponseformatjsonobject) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.TextResponseFormatConfigurationType](#openaitextresponseformatconfigurationtype) |  | Yes |  |

### OpenAI.TextResponseFormatConfigurationResponseFormatJsonObject

JSON object response format. An older method of generating JSON responses.
Using `json_schema` is recommended for models that support it. Note that the
model will not generate JSON without a system or user message instructing it
to do so.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `json_object`.<br>Possible values: `json_object` | Yes |  |

### OpenAI.TextResponseFormatConfigurationResponseFormatText

Default response format. Used to generate text responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.TextResponseFormatConfigurationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`json_schema`<br>`json_object` |

### OpenAI.TextResponseFormatJsonSchema

JSON Schema response format. Used to generate structured JSON responses.
Learn more about [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the response format is for, used by the model to<br>  determine how to respond in the format. | No |  |
| name | string | The name of the response format. Must be a-z, A-Z, 0-9, or contain<br>  underscores and dashes, with a maximum length of 64. | Yes |  |
| schema | [OpenAI.ResponseFormatJsonSchemaSchema](#openairesponseformatjsonschemaschema) | The schema for the response format, described as a JSON Schema object.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| strict | boolean (nullable) |  | No |  |
| type | enum | The type of response format being defined. Always `json_schema`.<br>Possible values: `json_schema` | Yes |  |

### OpenAI.Tool

A tool that can be used to generate a response.


### Discriminator for OpenAI.Tool

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `bing_grounding` | [BingGroundingTool](#binggroundingtool) |
| `fabric_dataagent_preview` | [MicrosoftFabricPreviewTool](#microsoftfabricpreviewtool) |
| `sharepoint_grounding_preview` | [SharepointPreviewTool](#sharepointpreviewtool) |
| `azure_ai_search` | [AzureAISearchTool](#azureaisearchtool) |
| `openapi` | [OpenApiTool](#openapitool) |
| `bing_custom_search_preview` | [BingCustomSearchPreviewTool](#bingcustomsearchpreviewtool) |
| `browser_automation_preview` | [BrowserAutomationPreviewTool](#browserautomationpreviewtool) |
| `azure_function` | [AzureFunctionTool](#azurefunctiontool) |
| `capture_structured_outputs` | [CaptureStructuredOutputsTool](#capturestructuredoutputstool) |
| `a2a_preview` | [A2APreviewTool](#a2apreviewtool) |
| `memory_search_preview` | [MemorySearchPreviewTool](#memorysearchpreviewtool) |
| `code_interpreter` | [OpenAI.CodeInterpreterTool](#openaicodeinterpretertool) |
| `function` | [OpenAI.FunctionTool](#openaifunctiontool) |
| `file_search` | [OpenAI.FileSearchTool](#openaifilesearchtool) |
| `computer_use_preview` | [OpenAI.ComputerUsePreviewTool](#openaicomputerusepreviewtool) |
| `web_search` | [OpenAI.WebSearchTool](#openaiwebsearchtool) |
| `mcp` | [OpenAI.MCPTool](#openaimcptool) |
| `image_generation` | [OpenAI.ImageGenTool](#openaiimagegentool) |
| `local_shell` | [OpenAI.LocalShellToolParam](#openailocalshelltoolparam) |
| `shell` | [OpenAI.FunctionShellToolParam](#openaifunctionshelltoolparam) |
| `custom` | [OpenAI.CustomToolParam](#openaicustomtoolparam) |
| `web_search_preview` | [OpenAI.WebSearchPreviewTool](#openaiwebsearchpreviewtool) |
| `apply_patch` | [OpenAI.ApplyPatchToolParam](#openaiapplypatchtoolparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ToolType](#openaitooltype) |  | Yes |  |

### OpenAI.ToolChoiceAllowed

Constrains the tools available to the model to a pre-defined set.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| mode | enum | Constrains the tools available to the model to a pre-defined set.<br>  `auto` allows the model to pick from among the allowed tools and generate a<br>  message.<br>  `required` requires the model to call one or more of the allowed tools.<br>Possible values: `auto`, `required` | Yes |  |
| tools | array of object | A list of tool definitions that the model should be allowed to call.<br>  For the Responses API, the list of tool definitions might look like:<br>  ```json<br>  [<br>    { "type": "function", "name": "get_weather" },<br>    { "type": "mcp", "server_label": "deepwiki" },<br>    { "type": "image_generation" }<br>  ]<br>  ``` | Yes |  |
| type | enum | Allowed tool configuration type. Always `allowed_tools`.<br>Possible values: `allowed_tools` | Yes |  |

### OpenAI.ToolChoiceCodeInterpreter

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `code_interpreter` | Yes |  |

### OpenAI.ToolChoiceComputerUsePreview

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `computer_use_preview` | Yes |  |

### OpenAI.ToolChoiceCustom

Use this option to force the model to call a specific custom tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the custom tool to call. | Yes |  |
| type | enum | For custom tool calling, the type is always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.ToolChoiceFileSearch

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `file_search` | Yes |  |

### OpenAI.ToolChoiceFunction

Use this option to force the model to call a specific function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the function to call. | Yes |  |
| type | enum | For function calling, the type is always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.ToolChoiceImageGeneration

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `image_generation` | Yes |  |

### OpenAI.ToolChoiceMCP

Use this option to force the model to call a specific tool on a remote MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string (nullable) |  | No |  |
| server_label | string | The label of the MCP server to use. | Yes |  |
| type | enum | For MCP tools, the type is always `mcp`.<br>Possible values: `mcp` | Yes |  |

### OpenAI.ToolChoiceOptions

Controls which (if any) tool is called by the model.
`none` means the model will not call any tool and instead generates a message.
`auto` means the model can pick between generating a message or calling one or
more tools.
`required` means the model must call one or more tools.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `none`<br>`auto`<br>`required` |

### OpenAI.ToolChoiceParam

How the model should select which tool (or tools) to use when generating
a response. See the `tools` parameter to see how to specify which tools
the model can call.


### Discriminator for OpenAI.ToolChoiceParam

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `allowed_tools` | [OpenAI.ToolChoiceAllowed](#openaitoolchoiceallowed) |
| `function` | [OpenAI.ToolChoiceFunction](#openaitoolchoicefunction) |
| `mcp` | [OpenAI.ToolChoiceMCP](#openaitoolchoicemcp) |
| `custom` | [OpenAI.ToolChoiceCustom](#openaitoolchoicecustom) |
| `apply_patch` | [OpenAI.SpecificApplyPatchParam](#openaispecificapplypatchparam) |
| `shell` | [OpenAI.SpecificFunctionShellParam](#openaispecificfunctionshellparam) |
| `file_search` | [OpenAI.ToolChoiceFileSearch](#openaitoolchoicefilesearch) |
| `web_search_preview` | [OpenAI.ToolChoiceWebSearchPreview](#openaitoolchoicewebsearchpreview) |
| `computer_use_preview` | [OpenAI.ToolChoiceComputerUsePreview](#openaitoolchoicecomputerusepreview) |
| `web_search_preview_2025_03_11` | [OpenAI.ToolChoiceWebSearchPreview20250311](#openaitoolchoicewebsearchpreview20250311) |
| `image_generation` | [OpenAI.ToolChoiceImageGeneration](#openaitoolchoiceimagegeneration) |
| `code_interpreter` | [OpenAI.ToolChoiceCodeInterpreter](#openaitoolchoicecodeinterpreter) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ToolChoiceParamType](#openaitoolchoiceparamtype) |  | Yes |  |

### OpenAI.ToolChoiceParamType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `allowed_tools`<br>`function`<br>`mcp`<br>`custom`<br>`apply_patch`<br>`shell`<br>`file_search`<br>`web_search_preview`<br>`computer_use_preview`<br>`web_search_preview_2025_03_11`<br>`image_generation`<br>`code_interpreter` |

### OpenAI.ToolChoiceWebSearchPreview

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `web_search_preview` | Yes |  |

### OpenAI.ToolChoiceWebSearchPreview20250311

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `web_search_preview_2025_03_11` | Yes |  |

### OpenAI.ToolType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `function`<br>`file_search`<br>`computer_use_preview`<br>`web_search`<br>`mcp`<br>`code_interpreter`<br>`image_generation`<br>`local_shell`<br>`shell`<br>`custom`<br>`web_search_preview`<br>`apply_patch`<br>`a2a_preview`<br>`bing_custom_search_preview`<br>`browser_automation_preview`<br>`fabric_dataagent_preview`<br>`sharepoint_grounding_preview`<br>`memory_search_preview`<br>`azure_ai_search`<br>`azure_function`<br>`bing_grounding`<br>`capture_structured_outputs`<br>`openapi` |

### OpenAI.ToolsArray

An array of tools the model may call while generating a response. You
can specify which tool to use by setting the `tool_choice` parameter.
We support the following categories of tools:
- **Built-in tools**: Tools that are provided by OpenAI that extend the
model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)
or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about
[built-in tools](https://platform.openai.com/docs/guides/tools).
- **MCP Tools**: Integrations with third-party systems via custom MCP servers
or predefined connectors such as Google Drive and SharePoint. Learn more about
[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).
- **Function calls (custom tools)**: Functions that are defined by you,
enabling the model to call your own code with strongly typed arguments
and outputs. Learn more about
[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use
custom tools to call your own code.

**Array of**: [OpenAI.Tool](#openaitool)


### OpenAI.TopLogProb

The top log probability of a token.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array of [OpenAI.integer](#openaiinteger) |  | Yes |  |
| logprob | [OpenAI.numeric](#openainumeric) |  | Yes |  |
| token | string |  | Yes |  |

### OpenAI.Type

An action to type in text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text to type. | Yes |  |
| type | enum | Specifies the event type. For a type action, this property is<br>  always set to `type`.<br>Possible values: `type` | Yes |  |

### OpenAI.UpdateConversationBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |

### OpenAI.UrlCitationBody

A citation for a web resource used to generate a model response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| end_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| start_index | [OpenAI.integer](#openaiinteger) |  | Yes |  |
| title | string | The title of the web resource. | Yes |  |
| type | enum | The type of the URL citation. Always `url_citation`.<br>Possible values: `url_citation` | Yes |  |
| url | string | The URL of the web resource. | Yes |  |

### OpenAI.VectorStoreFileAttributes

Set of 16 key-value pairs that can be attached to an object. This can be
useful for storing additional information about the object in a structured
format, and querying for objects via API or the dashboard. Keys are strings
with a maximum length of 64 characters. Values are strings with a maximum
length of 512 characters, booleans, or numbers.

**Type**: object


### OpenAI.Verbosity

Constrains the verbosity of the model's response. Lower values will result in
more concise responses, while higher values will result in more verbose responses.
Currently supported values are `low`, `medium`, and `high`.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Nullable** | Yes |
| **Values** | `low`<br>`medium`<br>`high` |

### OpenAI.Wait

A wait action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a wait action, this property is<br>  always set to `wait`.<br>Possible values: `wait` | Yes |  |

### OpenAI.WebSearchActionFind

Action type "find": Searches for a pattern within a loaded page.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| pattern | string | The pattern or text to search for within the page. | Yes |  |
| type | enum | The action type.<br>Possible values: `find_in_page` | Yes |  |
| url | string | The URL of the page searched for the pattern. | Yes |  |

### OpenAI.WebSearchActionOpenPage

Action type "open_page" - Opens a specific URL from search results.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The action type.<br>Possible values: `open_page` | Yes |  |
| url | string | The URL opened by the model. | Yes |  |

### OpenAI.WebSearchActionSearch

Action type "search" - Performs a web search query.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| queries | array of string | The search queries. | No |  |
| query | string (deprecated) | [DEPRECATED] The search query. | Yes |  |
| sources | array of [OpenAI.WebSearchActionSearchSources](#openaiwebsearchactionsearchsources) | The sources used in the search. | No |  |
| type | enum | The action type.<br>Possible values: `search` | Yes |  |

### OpenAI.WebSearchActionSearchSources

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `url` | Yes |  |
| url | string |  | Yes |  |

### OpenAI.WebSearchApproximateLocation

The approximate location of the user.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| city | string (nullable) |  | No |  |
| country | string (nullable) |  | No |  |
| region | string (nullable) |  | No |  |
| timezone | string (nullable) |  | No |  |
| type | enum | The type of location approximation. Always `approximate`.<br>Possible values: `approximate` | No |  |

### OpenAI.WebSearchPreviewTool

This tool searches the web for relevant results to use in a response. Learn more about the [web search tool](https://platform.openai.com/docs/guides/tools-web-search).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| search_context_size | [OpenAI.SearchContextSize](#openaisearchcontextsize) |  | No |  |
| type | enum | The type of the web search tool. One of `web_search_preview` or `web_search_preview_2025_03_11`.<br>Possible values: `web_search_preview` | Yes |  |
| user_location | [OpenAI.ApproximateLocation](#openaiapproximatelocation) (nullable) |  | No |  |
| └─ city | string (nullable) |  | No |  |
| └─ country | string (nullable) |  | No |  |
| └─ region | string (nullable) |  | No |  |
| └─ timezone | string (nullable) |  | No |  |
| └─ type | enum | The type of location approximation. Always `approximate`.<br>Possible values: `approximate` | Yes |  |

### OpenAI.WebSearchTool

Search the Internet for sources related to the prompt. Learn more about the
[web search tool](https://platform.openai.com/docs/guides/tools-web-search).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom_search_configuration | [WebSearchConfiguration](#websearchconfiguration) | A web search configuration for bing custom search | No |  |
| └─ instance_name | string | Name of the custom configuration instance given to config. | Yes |  |
| └─ project_connection_id | string | Project connection id for grounding with bing custom search | Yes |  |
| filters | [OpenAI.WebSearchToolFilters](#openaiwebsearchtoolfilters) (nullable) |  | No |  |
| └─ allowed_domains | array of string (nullable) |  | No |  |
| search_context_size | enum | High level guidance for the amount of context window space to use for the search. One of `low`, `medium`, or `high`. `medium` is the default.<br>Possible values: `low`, `medium`, `high` | No |  |
| type | enum | The type of the web search tool. One of `web_search` or `web_search_2025_08_26`.<br>Possible values: `web_search` | Yes |  |
| user_location | [OpenAI.WebSearchApproximateLocation](#openaiwebsearchapproximatelocation) (nullable) | The approximate location of the user. | No |  |
| └─ city | string (nullable) |  | No |  |
| └─ country | string (nullable) |  | No |  |
| └─ region | string (nullable) |  | No |  |
| └─ timezone | string (nullable) |  | No |  |
| └─ type | enum | The type of location approximation. Always `approximate`.<br>Possible values: `approximate` | No |  |

### OpenAI.WebSearchToolFilters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| allowed_domains | array of string |  | No |  |

### OpenAI.integer

**Type**: integer

**Format**: int64


### OpenAI.numeric

**Type**: number

**Format**: double


### OpenApiAnonymousAuthDetails

Security details for OpenApi anonymous authentication

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The object type, which is always 'anonymous'.<br>Possible values: `anonymous` | Yes |  |

### OpenApiAuthDetails

authentication details for OpenApiFunctionDefinition


### Discriminator for OpenApiAuthDetails

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `anonymous` | [OpenApiAnonymousAuthDetails](#openapianonymousauthdetails) |
| `project_connection` | [OpenApiProjectConnectionAuthDetails](#openapiprojectconnectionauthdetails) |
| `managed_identity` | [OpenApiManagedAuthDetails](#openapimanagedauthdetails) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenApiAuthType](#openapiauthtype) | Authentication type for OpenApi endpoint. Allowed types are:<br>- Anonymous (no authentication required)<br>- Project Connection (requires project_connection_id to endpoint, as setup in AI Foundry)<br>- Managed_Identity (requires audience for identity based auth) | Yes |  |

### OpenApiAuthType

Authentication type for OpenApi endpoint. Allowed types are:
- Anonymous (no authentication required)
- Project Connection (requires project_connection_id to endpoint, as setup in AI Foundry)
- Managed_Identity (requires audience for identity based auth)

| Property | Value |
|----------|-------|
| **Description** | Authentication type for OpenApi endpoint. Allowed types are:<br>- Anonymous (no authentication required)<br>- Project Connection (requires project_connection_id to endpoint, as setup in AI Foundry)<br>- Managed_Identity (requires audience for identity based auth) |
| **Type** | string |
| **Values** | `anonymous`<br>`project_connection`<br>`managed_identity` |

### OpenApiFunctionDefinition

The input definition information for an openapi function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| auth | [OpenApiAuthDetails](#openapiauthdetails) | authentication details for OpenApiFunctionDefinition | Yes |  |
| └─ type | [OpenApiAuthType](#openapiauthtype) | The type of authentication, must be anonymous/project_connection/managed_identity | Yes |  |
| default_params | array of string | List of OpenAPI spec parameters that will use user-provided defaults | No |  |
| description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| functions | array of object | List of function definitions used by OpenApi tool | No |  |
| name | string | The name of the function to be called. | Yes |  |
| spec | object | The openapi function shape, described as a JSON Schema object. | Yes |  |

### OpenApiManagedAuthDetails

Security details for OpenApi managed_identity authentication

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| security_scheme | [OpenApiManagedSecurityScheme](#openapimanagedsecurityscheme) | Security scheme for OpenApi managed_identity authentication | Yes |  |
| └─ audience | string | Authentication scope for managed_identity auth type | Yes |  |
| type | enum | The object type, which is always 'managed_identity'.<br>Possible values: `managed_identity` | Yes |  |

### OpenApiManagedSecurityScheme

Security scheme for OpenApi managed_identity authentication

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audience | string | Authentication scope for managed_identity auth type | Yes |  |

### OpenApiProjectConnectionAuthDetails

Security details for OpenApi project connection authentication

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| security_scheme | [OpenApiProjectConnectionSecurityScheme](#openapiprojectconnectionsecurityscheme) | Security scheme for OpenApi managed_identity authentication | Yes |  |
| └─ project_connection_id | string | Project connection id for Project Connection auth type | Yes |  |
| type | enum | The object type, which is always 'project_connection'.<br>Possible values: `project_connection` | Yes |  |

### OpenApiProjectConnectionSecurityScheme

Security scheme for OpenApi managed_identity authentication

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| project_connection_id | string | Project connection id for Project Connection auth type | Yes |  |

### OpenApiTool

The input definition information for an OpenAPI tool as used to configure an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| openapi | [OpenApiFunctionDefinition](#openapifunctiondefinition) | The input definition information for an openapi function. | Yes |  |
| └─ auth | [OpenApiAuthDetails](#openapiauthdetails) | Open API authentication details | Yes |  |
| └─ default_params | array of string | List of OpenAPI spec parameters that will use user-provided defaults | No |  |
| └─ description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| └─ functions | array of object (read-only) | List of function definitions used by OpenApi tool | No |  |
|   └─ description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
|   └─ name | string | The name of the function to be called. | Yes |  |
|   └─ parameters | object | The parameters the functions accepts, described as a JSON Schema object. | Yes |  |
| └─ name | string | The name of the function to be called. | Yes |  |
| └─ spec | object | The openapi function shape, described as a JSON Schema object. | Yes |  |
| type | enum | The object type, which is always 'openapi'.<br>Possible values: `openapi` | Yes |  |

### PageOrder

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `asc`<br>`desc` |

### PagedConnection

Paged collection of Connection items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [Connection](#connection) | The Connection items on this page | Yes |  |

### PagedDatasetVersion

Paged collection of DatasetVersion items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [DatasetVersion](#datasetversion) | The DatasetVersion items on this page | Yes |  |

### PagedDeployment

Paged collection of Deployment items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [Deployment](#deployment) | The Deployment items on this page | Yes |  |

### PagedEvaluationRule

Paged collection of EvaluationRule items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [EvaluationRule](#evaluationrule) | The EvaluationRule items on this page | Yes |  |

### PagedEvaluationTaxonomy

Paged collection of EvaluationTaxonomy items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [EvaluationTaxonomy](#evaluationtaxonomy) | The EvaluationTaxonomy items on this page | Yes |  |

### PagedEvaluatorVersion

Paged collection of EvaluatorVersion items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [EvaluatorVersion](#evaluatorversion) | The EvaluatorVersion items on this page | Yes |  |

### PagedIndex

Paged collection of Index items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [Index](#index) | The Index items on this page | Yes |  |

### PagedInsight

Paged collection of Insight items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [Insight](#insight) | The Insight items on this page | Yes |  |

### PagedRedTeam

Paged collection of RedTeam items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [RedTeam](#redteam) | The RedTeam items on this page | Yes |  |

### PagedSchedule

Paged collection of Schedule items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [Schedule](#schedule) | The Schedule items on this page | Yes |  |

### PagedScheduleRun

Paged collection of ScheduleRun items

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page of items | No |  |
| value | array of [ScheduleRun](#schedulerun) | The ScheduleRun items on this page | Yes |  |

### PendingUploadRequest

Represents a request for a pending upload.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionName | string | Azure Storage Account connection name to use for generating temporary SAS token | No |  |
| pendingUploadId | string | If PendingUploadId is not provided, a random GUID will be used. | No |  |
| pendingUploadType | enum | BlobReference is the only supported type.<br>Possible values: `BlobReference` | Yes |  |

### PendingUploadResponse

Represents the response for a pending upload request

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| blobReference | [BlobReference](#blobreference) | Blob reference details. | Yes |  |
| └─ blobUri | string | Blob URI path for client to upload data. Example: ``https://blob.windows.core.net/Container/Path`` | Yes |  |
| └─ credential | [SasCredential](#sascredential) | Credential info to access the storage account. | Yes |  |
| └─ storageAccountArmId | string | ARM ID of the storage account to use. | Yes |  |
| pendingUploadId | string | ID for this upload request. | Yes |  |
| pendingUploadType | enum | BlobReference is the only supported type<br>Possible values: `BlobReference` | Yes |  |
| version | string | Version of asset to be created if user did not specify version when initially creating upload | No |  |

### PromptAgentDefinition

The prompt agent definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| instructions | string (nullable) | A system (or developer) message inserted into the model's context. | No |  |
| kind | enum | <br>Possible values: `prompt` | Yes |  |
| model | string | The model deployment to use for this agent. | Yes |  |
| rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| └─ rai_policy_name | string | The name of the RAI policy to apply. | Yes |  |
| reasoning | [OpenAI.Reasoning](#openaireasoning) (nullable) | **gpt-5 and o-series models only**<br>Configuration options for<br>reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| └─ generate_summary | enum | <br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | <br>Possible values: `auto`, `concise`, `detailed` | No |  |
| structured_inputs | object | Set of structured inputs that can participate in prompt template substitution or tool argument bindings. | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| text | [PromptAgentDefinitionTextOptions](#promptagentdefinitiontextoptions) | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
| └─ format | [OpenAI.TextResponseFormatConfiguration](#openaitextresponseformatconfiguration) | An object specifying the format that the model must output.<br>Configuring `{ "type": "json_schema" }` enables Structured Outputs,<br>which ensures the model will match your supplied JSON schema. Learn more in the<br><br>The default format is `{ "type": "text" }` with no additional options.<br>*Not recommended for gpt-4o and newer models:**<br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | No |  |
| tool_choice | string or [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating a response.<br>See the `tools` parameter to see how to specify which tools the model can call. | No |  |
| tools | array of [OpenAI.Tool](#openaitool) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |

### PromptAgentDefinitionTextOptions

Configuration options for a text response from the model. Can be plain text or structured JSON data.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.TextResponseFormatConfiguration](#openaitextresponseformatconfiguration) | An object specifying the format that the model must output.<br>Configuring `{ "type": "json_schema" }` enables Structured Outputs,<br>which ensures the model will match your supplied JSON schema. Learn more in the<br><br>The default format is `{ "type": "text" }` with no additional options.<br>*Not recommended for gpt-4o and newer models:**<br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | No |  |

### PromptBasedEvaluatorDefinition

Prompt-based evaluator

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_schema | object | The JSON schema (Draft 2020-12) for the evaluator's input data. This includes parameters like type, properties, required. | No |  |
| init_parameters | object | The JSON schema (Draft 2020-12) for the evaluator's input parameters. This includes parameters like type, properties, required. | No |  |
| metrics | object | List of output metrics produced by this evaluator | No |  |
| prompt_text | string | The prompt text used for evaluation | Yes |  |
| type | enum | <br>Possible values: `prompt` | Yes |  |

### ProtocolVersionRecord

A record mapping for a single protocol and its version.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| protocol | [AgentProtocol](#agentprotocol) |  | Yes |  |
| version | string | The version string for the protocol, e.g. 'v0.1.1'. | Yes |  |

### RaiConfig

Configuration for Responsible AI (RAI) content filtering and safety features.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| rai_policy_name | string | The name of the RAI policy to apply. | Yes |  |

### RecurrenceSchedule

Recurrence schedule model.


### Discriminator for RecurrenceSchedule

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `Hourly` | [HourlyRecurrenceSchedule](#hourlyrecurrenceschedule) |
| `Daily` | [DailyRecurrenceSchedule](#dailyrecurrenceschedule) |
| `Weekly` | [WeeklyRecurrenceSchedule](#weeklyrecurrenceschedule) |
| `Monthly` | [MonthlyRecurrenceSchedule](#monthlyrecurrenceschedule) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [RecurrenceType](#recurrencetype) | Recurrence type. | Yes |  |

### RecurrenceTrigger

Recurrence based trigger.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| endTime | string | End time for the recurrence schedule in ISO 8601 format. | No |  |
| interval | integer | Interval for the recurrence schedule. | Yes |  |
| schedule | [RecurrenceSchedule](#recurrenceschedule) | Recurrence schedule model. | Yes |  |
| └─ type | [RecurrenceType](#recurrencetype) | Recurrence type for the recurrence schedule. | Yes |  |
| startTime | string | Start time for the recurrence schedule in ISO 8601 format. | No |  |
| timeZone | string | Time zone for the recurrence schedule. | No | UTC |
| type | enum | Type of the trigger.<br>Possible values: `Recurrence` | Yes |  |

### RecurrenceType

Recurrence type.

| Property | Value |
|----------|-------|
| **Description** | Recurrence type. |
| **Type** | string |
| **Values** | `Hourly`<br>`Daily`<br>`Weekly`<br>`Monthly` |

### RedTeam

Red team details.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| applicationScenario | string | Application scenario for the red team operation, to generate scenario specific attacks. | No |  |
| attackStrategies | array of [AttackStrategy](#attackstrategy) | List of attack strategies or nested lists of attack strategies. | No |  |
| displayName | string | Name of the red-team run. | No |  |
| id | string (read-only) | Identifier of the red team run. | Yes |  |
| numTurns | integer | Number of simulation rounds. | No |  |
| properties | object | Red team's properties. Unlike tags, properties are add-only. Once added, a property cannot be removed. | No |  |
| riskCategories | array of [RiskCategory](#riskcategory) | List of risk categories to generate attack objectives for. | No |  |
| simulationOnly | boolean | Simulation-only or Simulation + Evaluation. Default false, if true the scan outputs conversation not evaluation result. | No | False |
| status | string (read-only) | Status of the red-team. It is set by service and is read-only. | No |  |
| tags | object | Red team's tags. Unlike properties, tags are fully mutable. | No |  |
| target | [TargetConfig](#targetconfig) | Abstract class for target configuration. | Yes |  |
| └─ type | string | Type of the model configuration. | Yes |  |

### RedTeamEvalRunDataSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_generation_params | [ItemGenerationParams](#itemgenerationparams) | Represents the set of parameters used to control item generation operations. | Yes |  |
| └─ type | [ItemGenerationParamsType](#itemgenerationparamstype) | The type of item generation parameters to use. | Yes |  |
| target | [Target](#target) | Base class for targets with discriminator support. | Yes |  |
| └─ type | string | The type of target. | Yes |  |
| type | enum | The type of data source. Always `azure_ai_red_team`.<br>Possible values: `azure_ai_red_team` | Yes |  |

### RedTeamItemGenerationParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attack_strategies | array of [AttackStrategy](#attackstrategy) | The collection of attack strategies to be used. | Yes |  |
| num_turns | integer | The number of turns allowed in the game. | Yes | 20 |
| type | enum | The type of item generation parameters.<br>Possible values: `red_team` | Yes |  |

### RedTeamSeedPromptsItemGenerationParams

Represents the parameters for red team seed prompts item generation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attack_strategies | array of [AttackStrategy](#attackstrategy) | The collection of attack strategies to be used. | Yes |  |
| num_turns | integer | The number of turns allowed in the game. | Yes | 20 |
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) |  | Yes |  |
| └─ content | array of [OpenAI.EvalJsonlFileContentSourceContent](#openaievaljsonlfilecontentsourcecontent) | The content of the jsonl file. | Yes |  |
| └─ type | enum | The type of jsonl source. Always `file_content`.<br>Possible values: `file_content` | Yes |  |
| type | enum | The type of item generation parameters, always `red_team_seed_prompts`.<br>Possible values: `red_team_seed_prompts` | Yes |  |

### RedTeamTaxonomyItemGenerationParams

Represents the parameters for red team taxonomy item generation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attack_strategies | array of [AttackStrategy](#attackstrategy) | The collection of attack strategies to be used. | Yes |  |
| num_turns | integer | The number of turns allowed in the game. | Yes | 20 |
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) |  | Yes |  |
| └─ content | array of [OpenAI.EvalJsonlFileContentSourceContent](#openaievaljsonlfilecontentsourcecontent) | The content of the jsonl file. | Yes |  |
| └─ type | enum | The type of jsonl source. Always `file_content`.<br>Possible values: `file_content` | Yes |  |
| type | enum | The type of item generation parameters, always `red_team_taxonomy`.<br>Possible values: `red_team_taxonomy` | Yes |  |

### ResponseRetrievalItemGenerationParams

Represents the parameters for response retrieval item generation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_mapping | object | Mapping from source fields to response_id field, required for retrieving chat history. | Yes |  |
| max_num_turns | integer | The maximum number of turns of chat history to evaluate. | Yes |  |
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) | The source from which JSONL content is read. | Yes |  |
| type | enum | The type of item generation parameters, always `response_retrieval`.<br>Possible values: `response_retrieval` | Yes |  |

### RiskCategory

Risk category for the attack objective.

| Property | Value |
|----------|-------|
| **Description** | Risk category for the attack objective. |
| **Type** | string |
| **Values** | `HateUnfairness`<br>`Violence`<br>`Sexual`<br>`SelfHarm`<br>`ProtectedMaterial`<br>`CodeVulnerability`<br>`UngroundedAttributes`<br>`ProhibitedActions`<br>`SensitiveDataLeakage`<br>`TaskAdherence` |

### SASCredentials

Shared Access Signature (SAS) credential definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| SAS | string (read-only) | SAS token | No |  |
| type | enum | The credential type<br>Possible values: `SAS` | Yes |  |

### SampleType

The type of sample used in the analysis.

| Property | Value |
|----------|-------|
| **Description** | The type of sample used in the analysis. |
| **Type** | string |
| **Values** | `EvaluationResultSample` |

### SasCredential

SAS Credential definition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| sasUri | string (read-only) | SAS uri | Yes |  |
| type | enum | Type of credential<br>Possible values: `SAS` | Yes |  |

### Schedule

Schedule model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | Description of the schedule. | No |  |
| displayName | string | Name of the schedule. | No |  |
| enabled | boolean | Enabled status of the schedule. | Yes |  |
| id | string (read-only) | Identifier of the schedule. | Yes |  |
| properties | object | Schedule's properties. Unlike tags, properties are add-only. Once added, a property cannot be removed. | No |  |
| provisioningStatus | [ScheduleProvisioningStatus](#scheduleprovisioningstatus) (read-only) | Schedule provisioning status. | No |  |
| systemData | object (read-only) | System metadata for the resource. | Yes |  |
| tags | object | Schedule's tags. Unlike properties, tags are fully mutable. | No |  |
| task | [ScheduleTask](#scheduletask) | Schedule task model. | Yes |  |
| └─ configuration | object | Configuration for the task. | No |  |
| └─ type | [ScheduleTaskType](#scheduletasktype) | Type of the task. | Yes |  |
| trigger | [Trigger](#trigger) | Base model for Trigger of the schedule. | Yes |  |
| └─ type | [TriggerType](#triggertype) | Type of the trigger. | Yes |  |

### ScheduleProvisioningStatus

Schedule provisioning status.

| Property | Value |
|----------|-------|
| **Description** | Schedule provisioning status. |
| **Type** | string |
| **Values** | `Creating`<br>`Updating`<br>`Deleting`<br>`Succeeded`<br>`Failed` |

### ScheduleRun

Schedule run model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string (read-only) | Error information for the schedule run. | No |  |
| id | string (read-only) | Identifier of the schedule run. | Yes |  |
| properties | object (read-only) | Properties of the schedule run. | Yes |  |
| scheduleId | string | Identifier of the schedule. | Yes |  |
| success | boolean (read-only) | Trigger success status of the schedule run. | Yes |  |
| triggerTime | string | Trigger time of the schedule run. | No |  |

### ScheduleTask

Schedule task model.


### Discriminator for ScheduleTask

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `Evaluation` | [EvaluationScheduleTask](#evaluationscheduletask) |
| `Insight` | [InsightScheduleTask](#insightscheduletask) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| configuration | object | Configuration for the task. | No |  |
| type | [ScheduleTaskType](#scheduletasktype) | Type of the task. | Yes |  |

### ScheduleTaskType

Type of the task.

| Property | Value |
|----------|-------|
| **Description** | Type of the task. |
| **Type** | string |
| **Values** | `Evaluation`<br>`Insight` |

### SharepointGroundingToolParameters

The sharepoint grounding tool parameters.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| project_connections | array of [ToolProjectConnection](#toolprojectconnection) | The project connections attached to this tool. There can be a maximum of 1 connection<br>resource attached to the tool. | No |  |

### SharepointPreviewTool

The input definition information for a sharepoint tool as used to configure an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| sharepoint_grounding_preview | [SharepointGroundingToolParameters](#sharepointgroundingtoolparameters) | The sharepoint grounding tool parameters. | Yes |  |
| └─ project_connections | array of [ToolProjectConnection](#toolprojectconnection) | The project connections attached to this tool. There can be a maximum of 1 connection<br>resource attached to the tool.<br>**Constraints:** maxItems: 1 | No |  |
| type | enum | The object type, which is always 'sharepoint_grounding_preview'.<br>Possible values: `sharepoint_grounding_preview` | Yes |  |

### Sku

Sku information

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| capacity | integer | Sku capacity | Yes |  |
| family | string | Sku family | Yes |  |
| name | string | Sku name | Yes |  |
| size | string | Sku size | Yes |  |
| tier | string | Sku tier | Yes |  |

### StructuredInputDefinition

An structured input that can participate in prompt template substitutions and tool argument binding.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| default_value |  | The default value for the input if no run-time value is provided. | No |  |
| description | string | A human-readable description of the input. | No |  |
| required | boolean | Whether the input property is required when the agent is invoked. | No | False |
| schema | object | The JSON schema for the structured input (optional). | No |  |

### StructuredOutputDefinition

A structured output that can be produced by the agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of the output to emit. Used by the model to determine when to emit the output. | Yes |  |
| name | string | The name of the structured output. | Yes |  |
| schema | object | The JSON schema for the structured output. | Yes |  |
| strict | boolean (nullable) | Whether to enforce strict validation. Default `true`. | Yes |  |

### StructuredOutputsOutputItem

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| output |  | The structured output captured during the response. | Yes |  |
| response_id | string | The response on which the item is created. | No |  |
| type | enum | <br>Possible values: `structured_outputs` | Yes |  |

### SyntheticDataGenerationPreviewEvalRunDataSource

Represents a data source for evaluation runs that evaluates based on generated synthetic data for testing purposes.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | [OpenAI.CreateEvalResponsesRunDataSourceInputMessagesTemplate](#openaicreateevalresponsesrundatasourceinputmessagestemplate) |  | No |  |
| └─ template | array of object or [OpenAI.EvalItem](#openaievalitem) |  | Yes |  |
| └─ type | enum | <br>Possible values: `template` | Yes |  |
| item_generation_params | [SyntheticDataGenerationPreviewItemGenerationParams](#syntheticdatagenerationpreviewitemgenerationparams) |  | Yes |  |
| └─ model_deployment_name | string | The name of the model deployment to use for generating synthetic data. | Yes |  |
| └─ output_dataset_id | string (read-only) | The identifier of the output dataset where generated synthetic data is stored. The generated data is a jsonl file with columns id, query and test_description. | No |  |
| └─ output_dataset_name | string | The name of the output dataset where generated synthetic data will be stored. If not provided, service generates dataset name automatically. | No |  |
| └─ prompt | string | The prompt used for generating synthetic data. This is option if target is of type 'azure_ai_agent' with instructions configured in agent. | No |  |
| └─ samples_count | integer | The maximum number of data samples to generate. | Yes |  |
| └─ sources | array of [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) | The optional seed data content source files for data generation. | Yes |  |
| └─ type | enum | The type of item generation parameters.<br>Possible values: `synthetic_data_gen_preview` | Yes |  |
| target | [Target](#target) | Base class for targets with discriminator support. | Yes |  |
| └─ type | string | The type of target. | Yes |  |
| type | enum | The type of data source, always `azure_ai_synthetic_data_gen_preview`.<br>Possible values: `azure_ai_synthetic_data_gen_preview` | Yes |  |

### SyntheticDataGenerationPreviewItemGenerationParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| model_deployment_name | string | The name of the model deployment to use for generating synthetic data. | Yes |  |
| output_dataset_id | string (read-only) | The identifier of the output dataset where generated synthetic data is stored. The generated data is a jsonl file with columns id, query and test_description. | No |  |
| output_dataset_name | string | The name of the output dataset where generated synthetic data will be stored. If not provided, service generates dataset name automatically. | No |  |
| prompt | string | The prompt used for generating synthetic data. This is option if target is of type 'azure_ai_agent' with instructions configured in agent. | No |  |
| samples_count | integer | The maximum number of data samples to generate. | Yes |  |
| sources | array of [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) | The optional seed data content source files for data generation. | Yes |  |
| type | enum | The type of item generation parameters.<br>Possible values: `synthetic_data_gen_preview` | Yes |  |

### Target

Base class for targets with discriminator support.


### Discriminator for Target

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `azure_ai_model` | [AzureAIModelTarget](#azureaimodeltarget) |
| `azure_ai_agent` | [AzureAIAgentTarget](#azureaiagenttarget) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | string | The type of target. | Yes |  |

### TargetCompletionEvalRunDataSource

Represents a data source for target-based completion evaluation configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | [OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesItemReference](#openaicreateevalcompletionsrundatasourceinputmessagesitemreference) |  | No |  |
| └─ item_reference | string |  | Yes |  |
| └─ type | enum | <br>Possible values: `item_reference` | Yes |  |
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) | The source configuration for inline or file data. | Yes |  |
| target | [Target](#target) | Base class for targets with discriminator support. | Yes |  |
| └─ type | string | The type of target. | Yes |  |
| type | enum | The type of data source, always `azure_ai_target_completions`.<br>Possible values: `azure_ai_target_completions` | Yes |  |

### TargetConfig

Abstract class for target configuration.


### Discriminator for TargetConfig

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `AzureOpenAIModel` | [AzureOpenAIModelConfiguration](#azureopenaimodelconfiguration) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | string | Type of the model configuration. | Yes |  |

### TargetUpdate

Base class for targets with discriminator support.


### Discriminator for TargetUpdate

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `azure_ai_model` | [AzureAIModelTargetUpdate](#azureaimodeltargetupdate) |
| `azure_ai_agent` | [AzureAIAgentTargetUpdate](#azureaiagenttargetupdate) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | string | The type of target. | Yes |  |

### TaxonomyCategory

Taxonomy category definition.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | Description of the taxonomy category. | No |  |
| id | string | Unique identifier of the taxonomy category. | Yes |  |
| name | string | Name of the taxonomy category. | Yes |  |
| properties | object | Additional properties for the taxonomy category. | No |  |
| riskCategory | [RiskCategory](#riskcategory) | Risk category for the attack objective. | Yes |  |
| subCategories | array of [TaxonomySubCategory](#taxonomysubcategory) | List of taxonomy sub categories. | Yes |  |

### TaxonomySubCategory

Taxonomy sub-category definition.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | Description of the taxonomy sub-category. | No |  |
| enabled | boolean | List of taxonomy items under this sub-category. | Yes |  |
| id | string | Unique identifier of the taxonomy sub-category. | Yes |  |
| name | string | Name of the taxonomy sub-category. | Yes |  |
| properties | object | Additional properties for the taxonomy sub-category. | No |  |

### ToolDescription

Description of a tool that can be used by an agent.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A brief description of the tool's purpose. | No |  |
| name | string | The name of the tool. | No |  |

### ToolProjectConnection

A project connection resource.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| project_connection_id | string | A project connection in a ToolProjectConnectionList attached to this tool. | Yes |  |

### TracesPreviewEvalRunDataSource

Represents a data source for evaluation runs that operate over Agent traces stored in Application Insights.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| agent_id | string | The agent ID used to filter traces for evaluation. | No |  |
| agent_name | string | The agent name used to filter traces for evaluation. | No |  |
| end_time | integer | Unix timestamp (in seconds) marking the end of the trace query window. Defaults to the current time. | No |  |
| ingestion_delay_seconds | integer | The delay to apply for ingestion when querying traces. | No | 300 |
| lookback_hours | integer | Lookback window (in hours) applied when retrieving traces from Application Insights.<br>    For scheduled evaluations this is inferred from the recurrence interval. | No | 168 |
| max_traces | integer | Sampling limit applied to traces retrieved for evaluation. | No | 1000 |
| trace_ids | array of string | Collection of Agent trace identifiers that should be evaluated. | No |  |
| type | enum | The type of data source, always `azure_ai_traces_preview`.<br>Possible values: `azure_ai_traces_preview` | Yes |  |

### TreatmentEffectType

Treatment Effect Type.

| Property | Value |
|----------|-------|
| **Description** | Treatment Effect Type. |
| **Type** | string |
| **Values** | `TooFewSamples`<br>`Inconclusive`<br>`Changed`<br>`Improved`<br>`Degraded` |

### Trigger

Base model for Trigger of the schedule.


### Discriminator for Trigger

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `Cron` | [CronTrigger](#crontrigger) |
| `Recurrence` | [RecurrenceTrigger](#recurrencetrigger) |
| `OneTime` | [OneTimeTrigger](#onetimetrigger) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [TriggerType](#triggertype) | Type of the trigger. | Yes |  |

### TriggerType

Type of the trigger.

| Property | Value |
|----------|-------|
| **Description** | Type of the trigger. |
| **Type** | string |
| **Values** | `Cron`<br>`Recurrence`<br>`OneTime` |

### UpdateAgentFromManifestRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| manifest_id | string | The manifest ID to import the agent version from. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| parameter_values | object | The inputs to the manifest that will result in a fully materialized Agent. | Yes |  |

### UpdateAgentRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | [AgentDefinition](#agentdefinition) |  | Yes |  |
| └─ kind | [AgentKind](#agentkind) |  | Yes |  |
| └─ rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| description | string | A human-readable description of the agent.<br>**Constraints:** maxLength: 512 | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |

### UpdateEvalParametersBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) (nullable) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string |  | No |  |
| properties | object | Set of immutable 16 key-value pairs that can be attached to an object for storing additional information.<br>    Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |

### UserProfileMemoryItem

A memory item specifically containing user profile information extracted from conversations, such as preferences, interests, and personal details.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string | The content of the memory. | Yes |  |
| kind | enum | The kind of the memory item.<br>Possible values: `user_profile` | Yes |  |
| memory_id | string | The unique ID of the memory item. | Yes |  |
| scope | string | The namespace that logically groups and isolates memories, such as a user ID. | Yes |  |
| updated_at | integer | The last update time of the memory item. | Yes |  |

### WebSearchConfiguration

A web search configuration for bing custom search

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| instance_name | string | Name of the custom configuration instance given to config. | Yes |  |
| project_connection_id | string | Project connection id for grounding with bing custom search | Yes |  |

### WeeklyRecurrenceSchedule

Weekly recurrence schedule.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| daysOfWeek | array of [DayOfWeek](#dayofweek) | Days of the week for the recurrence schedule. | Yes |  |
| type | enum | Weekly recurrence type.<br>Possible values: `Weekly` | Yes |  |

### WorkflowActionOutputItem

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action_id | string | Unique identifier for the action. | Yes |  |
| agent_reference | [AgentReference](#agentreference) |  | No |  |
| └─ name | string | The name of the agent.<br>**Constraints:** maxLength: 256 | Yes |  |
| └─ type | enum | <br>Possible values: `agent_reference` | Yes |  |
| └─ version | string | The version identifier of the agent. | No |  |
| kind | string | The kind of CSDL action (e.g., 'SetVariable', 'InvokeAzureAgent'). | Yes |  |
| parent_action_id | string | ID of the parent action if this is a nested action. | No |  |
| previous_action_id | string | ID of the previous action if this action follows another. | No |  |
| response_id | string | The response on which the item is created. | No |  |
| status | enum | Status of the action (e.g., 'in_progress', 'completed', 'failed', 'cancelled').<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled` | Yes |  |
| type | enum | <br>Possible values: `workflow_action` | Yes |  |

### WorkflowAgentDefinition

The workflow agent definition.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | enum | <br>Possible values: `workflow` | Yes |  |
| rai_config | [RaiConfig](#raiconfig) | Configuration for Responsible AI (RAI) content filtering and safety features. | No |  |
| └─ rai_policy_name | string | The name of the RAI policy to apply. | Yes |  |
| workflow | string | The CSDL YAML definition of the workflow. | No |  |

### integer

**Type**: integer

**Format**: int64


