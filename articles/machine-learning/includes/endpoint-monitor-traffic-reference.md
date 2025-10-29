---
author: s-polly
ms.service: azure-machine-learning
ms.topic: include
ms.date: 01/02/2025
ms.author: scottpolly
---

| Property | Description |
|:--- |:--- |
| Method | The method that the client requests. |
| Path | The path that the client requests. |
| SubscriptionId | The machine learning subscription ID of the online endpoint. |
| AzureMLWorkspaceId | The machine learning workspace ID of the online endpoint. |
| AzureMLWorkspaceName | The machine learning workspace name of the online endpoint. |
| EndpointName | The name of the online endpoint. |
| DeploymentName | The name of the online deployment. |
| Protocol | The protocol of the request. |
| ResponseCode | The final response code that's returned to the client. |
| ResponseCodeReason | The final response code reason that's returned to the client. |
| ModelStatusCode | The response status code from the model. |
| ModelStatusReason | The response status reason from the model. |
| RequestPayloadSize | The total bytes received from the client. |
| ResponsePayloadSize | The total bytes sent back to the client. |
| UserAgent | The user-agent header of the request, including comments but truncated to a maximum of 70 characters. |
| XRequestId | The request ID that Azure Machine Learning generates for internal tracing. |
| XMSClientRequestId | The tracking ID that the client generates. |
| TotalDurationMs | The duration in milliseconds from the request start time to the time the last response byte is sent back to the client. If the client disconnects, the duration is taken from the start time to the client disconnect time. |
| RequestDurationMs | The duration in milliseconds from the request start time to the time the last byte of the request is received from the client. |
| ResponseDurationMs | The duration in milliseconds from the request start time to the time the first response byte is read from the model. |
| RequestThrottlingDelayMs | The delay in milliseconds in the request data transfer due to network throttling. |
| ResponseThrottlingDelayMs | The delay in milliseconds in the response data transfer due to network throttling. |