---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: include
ms.date: 09/23/2025
---

In this article, you learn how to use Azure AI Speech voice live with Azure AI Foundry models using the VoiceLive SDK for C#.

[!INCLUDE [Introduction](intro.md)]


## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- An [Azure AI Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [voice live overview documentation](../../../voice-live.md).
- [.NET SDK](https://dotnet.microsoft.com/download) version 6.0 or later installed.

<!--
## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.
-->


## Start a voice conversation

Follow these steps to create a console application and install the Speech SDK.

1. Open a command prompt window in the folder where you want the new project. Run this command to create a console application with the .NET CLI.

    ```dotnetcli
    dotnet new console
    ```

   This command creates the *Program.cs* file in your project directory.

1. Install the Voice Live SDK in your new project with the .NET CLI.

    ```dotnetcli
    dotnet add package Azure.AI.VoiceLive --prerelease
    ```

1. Create a new file named `appsettings.json` in the folder where you want to run the code. In that file, add the following JSON content:
    
    ```json
    {
      "VoiceLive": {
        "ApiKey": "YOUR_VOICELIVE_API_KEY",
        "Endpoint": "wss://api.voicelive.com/v1",
        "Model": "gpt-realtime",
        "Voice": "en-US-Ava:DragonHDLatestNeural",
        "Instructions": "You are a professional customer service representative for TechCorp. You have access to customer databases and order systems. Always be polite, helpful, and efficient. When customers ask about orders, accounts, or need to schedule service, use the available tools to provide accurate, real-time information. Keep your responses concise but thorough."
      },
      "Logging": {
        "LogLevel": {
          "Default": "Information",
          "Azure.AI.VoiceLive": "Debug"
        }
      }
    }
    ```
    
    Replace the `ApiKey` value with your AI Foundry API key, and replace the `Endpoint` value with your resource endpoint. You can also change the Model, Voice, and Instructions values as needed.

1. Replace the contents of `Program.cs` with the following code. This code creates a sample customer service bot. For more details, see the sample on [GitHub](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.VoiceLive/samples/CustomerServiceBot).
    
    ```csharp
    // Copyright (c) Microsoft Corporation. All rights reserved.
    // Licensed under the MIT License.
    
    using System.CommandLine;
    using Azure.Core;
    using Azure.Core.Pipeline;
    using Azure.Identity;
    using Microsoft.Extensions.Configuration;
    using Microsoft.Extensions.Logging;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;
    using System.Threading.Channels;
    using System.Threading.Tasks;
    using System.Text.Json;
    using NAudio.Wave;
    using Azure.AI.VoiceLive;
    using static SampleData;
    
    public static class FunctionModels
    {
        /// <summary>
        /// Parameters for checking order status.
        /// </summary>
        public class CheckOrderStatusArgs
        {
            /// <summary>
            /// The order number to check status for.
            /// </summary>
            public string order_number { get; set; } = string.Empty;
            /// <summary>
            /// Customer email.
            /// </summary>
            public string? email { get; set; }
        }
    
        /// <summary>
        /// Parameters for getting customer information.
        /// </summary>
        public class GetCustomerInfoArgs
        {
            /// <summary>
            /// Customer ID to retrieve information for.
            /// </summary>
            public string customer_id { get; set; } = string.Empty;
            /// <summary>
            /// Whether to include order history in the response.
            /// </summary>
            public bool include_history { get; set; } = false;
        }
    
        /// <summary>
        /// Parameters for scheduling support calls.
        /// </summary>
        public class ScheduleSupportCallArgs
        {
            /// <summary>
            /// The customer ID to schedule the call for.
            /// </summary>
            public string customer_id { get; set; } = string.Empty;
            /// <summary>
            /// The preferred time for the support call.
            /// </summary>
            public string? preferred_time { get; set; }
            /// <summary>
            /// The category of the support issue.
            /// </summary>
            public string issue_category { get; set; } = string.Empty;
            /// <summary>
            /// The urgency level of the support issue.
            /// </summary>
            public string urgency { get; set; } = "medium";
            /// <summary>
            /// A brief description of the issue.
            /// </summary>
            public string description { get; set; } = string.Empty;
        }
    
        /// <summary>
        /// Parameters for initiating return process.
        /// </summary>
        public class InitiateReturnProcessArgs
        {
            /// <summary>
            /// The order number for which the return is requested.
            /// </summary>
            public string order_number { get; set; } = string.Empty;
            /// <summary>
            /// The product ID to be returned.
            /// </summary>
            public string product_id { get; set; } = string.Empty;
            /// <summary>
            /// The reason for the return.
            /// </summary>
            public string reason { get; set; } = string.Empty;
            /// <summary>
            /// The return method preferred by the customer.
            /// </summary>
            public string return_type { get; set; } = string.Empty;
        }
    
        /// <summary>
        /// Address information for shipping updates.
        /// </summary>
        public class Address
        {
            /// <summary>
            ///  Street address for shipping.
            /// </summary>
            public string street { get; set; } = string.Empty;
            /// <summary>
            ///  City for shipping address.
            /// </summary>
            public string city { get; set; } = string.Empty;
            /// <summary>
            /// state for shipping address.
            /// </summary>
            public string state { get; set; } = string.Empty;
            /// <summary>
            /// zip code for shipping address.
            /// </summary>
            public string zip_code { get; set; } = string.Empty;
            /// <summary>
            /// Country/region for shipping address.
            /// </summary>
            public string country_region { get; set; } = "US";
        }
    
        /// <summary>
        /// Parameters for updating shipping address.
        /// </summary>
        public class UpdateShippingAddressArgs
        {
            /// <summary>
            /// Order number for which the address needs to be updated.
            /// </summary>
            public string order_number { get; set; } = string.Empty;
            /// <summary>
            /// New shipping address.
            /// </summary>
            public Address new_address { get; set; } = new();
        }
    }
    
    /// <summary>
    /// Sample data models for demonstration purposes.
    /// </summary>
    public static class SampleData
    {
        /// <summary>
        /// Sample order information.
        /// </summary>
        public class Order
        {
            /// <summary>
            /// The unique identifier for the order.
            /// </summary>
            public string OrderNumber { get; set; } = string.Empty;
            /// <summary>
            /// Status of the order.
            /// </summary>
            public string Status { get; set; } = string.Empty;
            /// <summary>
            /// Total amount for the order.
            /// </summary>
            public decimal TotalAmount { get; set; }
            /// <summary>
            /// The items included in the order.
            /// </summary>
            public List<OrderItem> Items { get; set; } = new();
            /// <summary>
            /// Estimated delivery date for the order.
            /// </summary>
            public DateTime? EstimatedDelivery { get; set; }
            /// <summary>
            /// Shipping tracking number, if available.
            /// </summary>
            public string? TrackingNumber { get; set; }
            /// <summary>
            /// Theustomer ID associated with the order.
            /// </summary>
            public string CustomerId { get; set; } = string.Empty;
            /// <summary>
            /// When the order was created.
            /// </summary>
            public DateTime CreatedAt { get; set; }
        }
    
        /// <summary>
        /// Sample order item information.
        /// </summary>
        public class OrderItem
        {
            /// <summary>
            /// The unique identifier for the product.
            /// </summary>
            public string ProductId { get; set; } = string.Empty;
            /// <summary>
            /// Name of the product.
            /// </summary>
            public string ProductName { get; set; } = string.Empty;
            /// <summary>
            /// quantity of the product ordered.
            /// </summary>
            public int Quantity { get; set; }
            /// <summary>
            /// status of the order item.
            /// </summary>
            public string Status { get; set; } = string.Empty;
            /// <summary>
            /// price of the product.
            /// </summary>
            public decimal Price { get; set; }
        }
    
        /// <summary>
        /// Sample customer information.
        /// </summary>
        public class Customer
        {
            /// <summary>
            /// customer ID.
            /// </summary>
            public string CustomerId { get; set; } = string.Empty;
            /// <summary>
            /// preferred name of the customer.
            /// </summary>
            public string Name { get; set; } = string.Empty;
            /// <summary>
            /// customer's email address.
            /// </summary>
            public string Email { get; set; } = string.Empty;
            /// <summary>
            /// phone number of the customer.
            /// </summary>
            public string? Phone { get; set; }
            /// <summary>
            /// customer's pricing tier.
            /// </summary>
            public string Tier { get; set; } = "Standard";
            /// <summary>
            /// When the customer was created.
            /// </summary>
            public DateTime CreatedAt { get; set; }
        }
    
        /// <summary>
        /// Sample support ticket information.
        /// </summary>
        public class SupportTicket
        {
            /// <summary>
            /// ID of the support ticket.
            /// </summary>
            public string TicketId { get; set; } = string.Empty;
            /// <summary>
            /// customer ID associated with the ticket.
            /// </summary>
            public string CustomerId { get; set; } = string.Empty;
            /// <summary>
            /// category of the support issue.
            /// </summary>
            public string Category { get; set; } = string.Empty;
            /// <summary>
            /// urgency level of the support issue.
            /// </summary>
            public string Urgency { get; set; } = string.Empty;
            /// <summary>
            /// brief description of the issue.
            /// </summary>
            public string Description { get; set; } = string.Empty;
            /// <summary>
            /// time when the ticket was created.
            /// </summary>
            public DateTime ScheduledTime { get; set; }
            /// <summary>
            /// current status of the support ticket.
            /// </summary>
            public string Status { get; set; } = "Scheduled";
        }
    }
    
    public interface ICustomerServiceFunctions
    {
        /// <summary>
        /// Executes a function by name with JSON arguments.
        /// </summary>
        /// <param name="functionName"></param>
        /// <param name="argumentsJson"></param>
        /// <param name="cancellationToken"></param>
        /// <returns></returns>
        Task<object> ExecuteFunctionAsync(string functionName, string argumentsJson, CancellationToken cancellationToken = default);
    }
    
    /// <summary>
    /// Implementation of customer service functions with mock data for demonstration.
    /// In a real implementation, these would connect to actual databases and services.
    /// </summary>
    public class CustomerServiceFunctions : ICustomerServiceFunctions
    {
        private readonly ILogger<CustomerServiceFunctions> _logger;
        private readonly Dictionary<string, Order> _orders;
        private readonly Dictionary<string, Customer> _customers;
        private readonly List<SupportTicket> _supportTickets;
    
        /// <summary>
        /// Constructor for CustomerServiceFunctions.
        /// </summary>
        /// <param name="logger"></param>
        /// <exception cref="ArgumentNullException"></exception>
        public CustomerServiceFunctions(ILogger<CustomerServiceFunctions> logger)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    
            // Initialize sample data
            _orders = InitializeSampleOrders();
            _customers = InitializeSampleCustomers();
            _supportTickets = new List<SupportTicket>();
        }
    
        /// <summary>
        /// Execute a function by name with JSON arguments.
        /// </summary>
        public async Task<object> ExecuteFunctionAsync(string functionName, string argumentsJson, CancellationToken cancellationToken = default)
        {
            try
            {
                _logger.LogInformation("Executing function: {FunctionName} with arguments: {Arguments}", functionName, argumentsJson);
    
                return functionName switch
                {
                    "check_order_status" => await CheckOrderStatusAsync(argumentsJson, cancellationToken).ConfigureAwait(false),
                    "get_customer_info" => await GetCustomerInfoAsync(argumentsJson, cancellationToken).ConfigureAwait(false),
                    "schedule_support_call" => await ScheduleSupportCallAsync(argumentsJson, cancellationToken).ConfigureAwait(false),
                    "initiate_return_process" => await InitiateReturnProcessAsync(argumentsJson, cancellationToken).ConfigureAwait(false),
                    "update_shipping_address" => await UpdateShippingAddressAsync(argumentsJson, cancellationToken).ConfigureAwait(false),
                    _ => new { success = false, error = $"Unknown function: {functionName}" }
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error executing function {FunctionName}", functionName);
                return new { success = false, error = "Internal error occurred while processing your request." };
            }
        }
    
        private async Task<object> CheckOrderStatusAsync(string argumentsJson, CancellationToken cancellationToken)
        {
            var args = JsonSerializer.Deserialize<FunctionModels.CheckOrderStatusArgs>(argumentsJson, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (args == null)
            {
                return new { success = false, message = "Invalid arguments provided." };
            }
    
            // Simulate async database lookup
            await Task.Delay(100, cancellationToken).ConfigureAwait(false);
    
            if (!_orders.TryGetValue(args.order_number, out var order))
            {
                return new
                {
                    success = false,
                    message = "Order not found. Please verify the order number and try again."
                };
            }
    
            return new
            {
                success = true,
                order = new
                {
                    number = order.OrderNumber,
                    status = order.Status,
                    total = order.TotalAmount,
                    items = order.Items.Select(item => new
                    {
                        name = item.ProductName,
                        quantity = item.Quantity,
                        status = item.Status,
                        price = item.Price
                    }),
                    estimated_delivery = order.EstimatedDelivery?.ToString("yyyy-MM-dd"),
                    tracking = order.TrackingNumber,
                    order_date = order.CreatedAt.ToString("yyyy-MM-dd")
                }
            };
        }
    
        private async Task<object> GetCustomerInfoAsync(string argumentsJson, CancellationToken cancellationToken)
        {
            var args = JsonSerializer.Deserialize<FunctionModels.GetCustomerInfoArgs>(argumentsJson, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (args == null)
            {
                return new { success = false, message = "Invalid arguments provided." };
            }
    
            // Simulate async database lookup
            await Task.Delay(150, cancellationToken).ConfigureAwait(false);
    
            var customer = _customers.Values.FirstOrDefault(c =>
                c.CustomerId == args.customer_id ||
                c.Email.Equals(args.customer_id, StringComparison.OrdinalIgnoreCase));
    
            if (customer == null)
            {
                return new
                {
                    success = false,
                    message = "Customer account not found. Please verify the customer ID or email address."
                };
            }
    
            var result = new
            {
                success = true,
                customer = new
                {
                    id = customer.CustomerId,
                    name = customer.Name,
                    email = customer.Email,
                    phone = customer.Phone,
                    tier = customer.Tier,
                    joined_date = customer.CreatedAt.ToString("yyyy-MM-dd")
                }
            };
    
            if (args.include_history)
            {
                var customerOrders = _orders.Values
                    .Where(o => o.CustomerId == customer.CustomerId)
                    .OrderByDescending(o => o.CreatedAt)
                    .Take(5)
                    .Select(order => new
                    {
                        number = order.OrderNumber,
                        date = order.CreatedAt.ToString("yyyy-MM-dd"),
                        total = order.TotalAmount,
                        status = order.Status
                    });
    
                return new
                {
                    result.success,
                    customer = new
                    {
                        result.customer.id,
                        result.customer.name,
                        result.customer.email,
                        result.customer.phone,
                        result.customer.tier,
                        result.customer.joined_date,
                        recent_orders = customerOrders
                    }
                };
            }
    
            return result;
        }
    
        private async Task<object> ScheduleSupportCallAsync(string argumentsJson, CancellationToken cancellationToken)
        {
            var args = JsonSerializer.Deserialize<FunctionModels.ScheduleSupportCallArgs>(argumentsJson, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (args == null)
            {
                return new { success = false, message = "Invalid arguments provided." };
            }
    
            // Validate customer exists
            var customer = _customers.Values.FirstOrDefault(c =>
                c.CustomerId == args.customer_id ||
                c.Email.Equals(args.customer_id, StringComparison.OrdinalIgnoreCase));
    
            if (customer == null)
            {
                return new
                {
                    success = false,
                    message = "Customer not found. Please verify the customer ID."
                };
            }
    
            // Simulate async scheduling system
            await Task.Delay(200, cancellationToken).ConfigureAwait(false);
    
            // Parse preferred time or use default
            DateTime scheduledTime;
            if (!string.IsNullOrEmpty(args.preferred_time) && DateTime.TryParse(args.preferred_time, out scheduledTime))
            {
                // Use provided time
            }
            else
            {
                // Default to next business day at 10 AM
                scheduledTime = DateTime.Today.AddDays(1);
                if (scheduledTime.DayOfWeek == DayOfWeek.Saturday)
                    scheduledTime = scheduledTime.AddDays(2);
                if (scheduledTime.DayOfWeek == DayOfWeek.Sunday)
                    scheduledTime = scheduledTime.AddDays(1);
                scheduledTime = scheduledTime.AddHours(10);
            }
    
            var ticket = new SupportTicket
            {
                TicketId = $"TICKET-{DateTime.Now:yyyyMMdd}-{Random.Shared.Next(1000, 9999)}",
                CustomerId = customer.CustomerId,
                Category = args.issue_category,
                Urgency = args.urgency,
                Description = args.description,
                ScheduledTime = scheduledTime,
                Status = "Scheduled"
            };
    
            _supportTickets.Add(ticket);
    
            return new
            {
                success = true,
                ticket = new
                {
                    ticket_id = ticket.TicketId,
                    customer_name = customer.Name,
                    scheduled_time = ticket.ScheduledTime.ToString("yyyy-MM-dd HH:mm"),
                    category = ticket.Category,
                    urgency = ticket.Urgency,
                    description = ticket.Description,
                    status = ticket.Status
                },
                message = $"Support call scheduled for {ticket.ScheduledTime:yyyy-MM-dd HH:mm}. You will receive a confirmation email shortly."
            };
        }
    
        private async Task<object> InitiateReturnProcessAsync(string argumentsJson, CancellationToken cancellationToken)
        {
            var args = JsonSerializer.Deserialize<FunctionModels.InitiateReturnProcessArgs>(argumentsJson, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (args == null)
            {
                return new { success = false, message = "Invalid arguments provided." };
            }
    
            // Simulate async database lookup
            await Task.Delay(150, cancellationToken).ConfigureAwait(false);
    
            if (!_orders.TryGetValue(args.order_number, out var order))
            {
                return new
                {
                    success = false,
                    message = "Order not found. Please verify the order number."
                };
            }
    
            var item = order.Items.FirstOrDefault(i => i.ProductId == args.product_id);
            if (item == null)
            {
                return new
                {
                    success = false,
                    message = "Product not found in this order."
                };
            }
    
            // Check if return is eligible (within 30 days and not already returned)
            if (order.CreatedAt < DateTime.Now.AddDays(-30))
            {
                return new
                {
                    success = false,
                    message = "This order is outside the 30-day return window."
                };
            }
    
            if (item.Status == "Returned")
            {
                return new
                {
                    success = false,
                    message = "This item has already been returned."
                };
            }
    
            var returnId = $"RTN-{DateTime.Now:yyyyMMdd}-{Random.Shared.Next(1000, 9999)}";
    
            return new
            {
                success = true,
                return_info = new
                {
                    return_id = returnId,
                    order_number = order.OrderNumber,
                    product_name = item.ProductName,
                    return_type = args.return_type,
                    reason = args.reason,
                    refund_amount = args.return_type == "refund" ? item.Price : 0,
                    estimated_processing = "3-5 business days",
                    return_label_url = $"https://returns.techcorp.com/label/{returnId}"
                },
                message = "Return request initiated successfully. You will receive a return shipping label via email within 24 hours."
            };
        }
    
        private async Task<object> UpdateShippingAddressAsync(string argumentsJson, CancellationToken cancellationToken)
        {
            var args = JsonSerializer.Deserialize<FunctionModels.UpdateShippingAddressArgs>(argumentsJson, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (args == null)
            {
                return new { success = false, message = "Invalid arguments provided." };
            }
    
            // Simulate async database lookup
            await Task.Delay(100, cancellationToken).ConfigureAwait(false);
    
            if (!_orders.TryGetValue(args.order_number, out var order))
            {
                return new
                {
                    success = false,
                    message = "Order not found. Please verify the order number."
                };
            }
    
            // Check if order can be modified
            if (order.Status == "Delivered" || order.Status == "Shipped")
            {
                return new
                {
                    success = false,
                    message = $"Cannot update address for {order.Status.ToLower()} orders."
                };
            }
    
            return new
            {
                success = true,
                updated_order = new
                {
                    order_number = order.OrderNumber,
                    status = order.Status,
                    new_shipping_address = new
                    {
                        args.new_address.street,
                        args.new_address.city,
                        args.new_address.state,
                        args.new_address.zip_code,
                        args.new_address.country_region
                    },
                    estimated_delivery = order.EstimatedDelivery?.AddDays(1).ToString("yyyy-MM-dd") // Adjust delivery date
                },
                message = "Shipping address updated successfully. Your estimated delivery date may have changed."
            };
        }
    
        private Dictionary<string, Order> InitializeSampleOrders()
        {
            return new Dictionary<string, Order>
            {
                ["ORD-2024-001"] = new Order
                {
                    OrderNumber = "ORD-2024-001",
                    Status = "Processing",
                    TotalAmount = 299.99m,
                    CustomerId = "CUST-001",
                    CreatedAt = DateTime.Now.AddDays(-2),
                    EstimatedDelivery = DateTime.Now.AddDays(3),
                    TrackingNumber = "1Z999AA1234567890",
                    Items = new List<OrderItem>
                    {
                        new() { ProductId = "LAPTOP-001", ProductName = "TechCorp Laptop Pro", Quantity = 1, Status = "Processing", Price = 299.99m }
                    }
                },
                ["ORD-2024-002"] = new Order
                {
                    OrderNumber = "ORD-2024-002",
                    Status = "Shipped",
                    TotalAmount = 159.98m,
                    CustomerId = "CUST-002",
                    CreatedAt = DateTime.Now.AddDays(-5),
                    EstimatedDelivery = DateTime.Now.AddDays(1),
                    TrackingNumber = "1Z999AA1234567891",
                    Items = new List<OrderItem>
                    {
                        new() { ProductId = "MOUSE-001", ProductName = "Wireless Gaming Mouse", Quantity = 1, Status = "Shipped", Price = 79.99m },
                        new() { ProductId = "PAD-001", ProductName = "Gaming Mouse Pad", Quantity = 1, Status = "Shipped", Price = 79.99m }
                    }
                },
                ["ORD-2024-003"] = new Order
                {
                    OrderNumber = "ORD-2024-003",
                    Status = "Delivered",
                    TotalAmount = 499.99m,
                    CustomerId = "CUST-001",
                    CreatedAt = DateTime.Now.AddDays(-10),
                    EstimatedDelivery = DateTime.Now.AddDays(-3),
                    TrackingNumber = "1Z999AA1234567892",
                    Items = new List<OrderItem>
                    {
                        new() { ProductId = "MONITOR-001", ProductName = "4K Gaming Monitor", Quantity = 1, Status = "Delivered", Price = 499.99m }
                    }
                }
            };
        }
    
        private Dictionary<string, Customer> InitializeSampleCustomers()
        {
            return new Dictionary<string, Customer>
            {
                ["CUST-001"] = new Customer
                {
                    CustomerId = "CUST-001",
                    Name = "John Smith",
                    Email = "john.smith@email.com",
                    Phone = "+1-555-0123",
                    Tier = "Gold",
                    CreatedAt = DateTime.Now.AddMonths(-8)
                },
                ["CUST-002"] = new Customer
                {
                    CustomerId = "CUST-002",
                    Name = "Sarah Johnson",
                    Email = "sarah.johnson@email.com",
                    Phone = "+1-555-0124",
                    Tier = "Silver",
                    CreatedAt = DateTime.Now.AddMonths(-3)
                },
                ["CUST-003"] = new Customer
                {
                    CustomerId = "CUST-003",
                    Name = "Mike Davis",
                    Email = "mike.davis@email.com",
                    Phone = "+1-555-0125",
                    Tier = "Standard",
                    CreatedAt = DateTime.Now.AddMonths(-1)
                }
            };
        }
    }
    
    /// <summary>
    /// Customer service voice bot implementing function calling with the VoiceLive SDK.
    /// </summary>
    /// <remarks>
    /// This sample demonstrates how to build a sophisticated customer service bot that can:
    /// - Check order status and track shipments
    /// - Retrieve customer account information and history
    /// - Schedule technical support calls
    /// - Process returns and exchanges
    /// - Update shipping addresses for pending orders
    ///
    /// The bot uses strongly-typed function definitions and provides real-time voice interaction
    /// with proper interruption handling and error recovery.
    /// </remarks>
    public class CustomerServiceBot : IDisposable
    {
        private readonly VoiceLiveClient _client;
        private readonly string _model;
        private readonly string _voice;
        private readonly string _instructions;
        private readonly ICustomerServiceFunctions _functions;
        private readonly ILogger<CustomerServiceBot> _logger;
        private readonly ILoggerFactory _loggerFactory;
    
        private readonly HashSet<string> _assistantMessageItems = new HashSet<string>();
        private readonly HashSet<string> _assistantMessageResponses = new HashSet<string>();
    
        private VoiceLiveSession? _session;
        private AudioProcessor? _audioProcessor;
        private bool _disposed;
    
        /// <summary>
        /// Initializes a new instance of the CustomerServiceBot class.
        /// </summary>
        /// <param name="client">The VoiceLive client.</param>
        /// <param name="model">The model to use.</param>
        /// <param name="voice">The voice to use.</param>
        /// <param name="instructions">The system instructions.</param>
        /// <param name="functions">The customer service functions implementation.</param>
        /// <param name="loggerFactory">Logger factory for creating loggers.</param>
        public CustomerServiceBot(
            VoiceLiveClient client,
            string model,
            string voice,
            string instructions,
            ICustomerServiceFunctions functions,
            ILoggerFactory loggerFactory)
        {
            _client = client ?? throw new ArgumentNullException(nameof(client));
            _model = model ?? throw new ArgumentNullException(nameof(model));
            _voice = voice ?? throw new ArgumentNullException(nameof(voice));
            _instructions = instructions ?? throw new ArgumentNullException(nameof(instructions));
            _functions = functions ?? throw new ArgumentNullException(nameof(functions));
            _loggerFactory = loggerFactory ?? throw new ArgumentNullException(nameof(loggerFactory));
            _logger = loggerFactory.CreateLogger<CustomerServiceBot>();
        }
    
        /// <summary>
        /// Start the customer service bot session.
        /// </summary>
        /// <param name="cancellationToken">Cancellation token for stopping the session.</param>
        public async Task StartAsync(CancellationToken cancellationToken = default)
        {
            try
            {
                _logger.LogInformation("Connecting to VoiceLive API with model {Model}", _model);
    
                // Start VoiceLive session
                _session = await _client.StartSessionAsync(_model, cancellationToken).ConfigureAwait(false);
    
                // Initialize audio processor
                _audioProcessor = new AudioProcessor(_session, _loggerFactory.CreateLogger<AudioProcessor>());
    
                // Configure session for voice conversation with function calling
                await SetupSessionAsync(cancellationToken).ConfigureAwait(false);
    
                // Start audio systems
                await _audioProcessor.StartPlaybackAsync().ConfigureAwait(false);
                await _audioProcessor.StartCaptureAsync().ConfigureAwait(false);
    
                _logger.LogInformation("Customer service bot ready! Start speaking...");
                Console.WriteLine();
                Console.WriteLine("=" + new string('=', 69));
                Console.WriteLine("🏢 CUSTOMER SERVICE BOT READY");
                Console.WriteLine("I can help you with orders, returns, account info, and scheduling support calls");
                Console.WriteLine("Start speaking to begin your customer service session");
                Console.WriteLine("Press Ctrl+C to exit");
                Console.WriteLine("=" + new string('=', 69));
                Console.WriteLine();
    
                // Process events
                await ProcessEventsAsync(cancellationToken).ConfigureAwait(false);
            }
            catch (OperationCanceledException)
            {
                _logger.LogInformation("Received cancellation signal, shutting down...");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Connection error");
                throw;
            }
            finally
            {
                // Cleanup
                if (_audioProcessor != null)
                {
                    await _audioProcessor.CleanupAsync().ConfigureAwait(false);
                }
            }
        }
    
        /// <summary>
        /// Configure the VoiceLive session for customer service with function calling.
        /// </summary>
        private async Task SetupSessionAsync(CancellationToken cancellationToken)
        {
            _logger.LogInformation("Setting up customer service session with function calling...");
    
            // Azure voice configuration
            var azureVoice = new AzureStandardVoice(_voice);
    
            // Create strongly typed turn detection configuration
            var turnDetectionConfig = new ServerVadTurnDetection
            {
                Threshold = 0.5f,
                PrefixPadding = TimeSpan.FromMilliseconds(300),
                SilenceDuration = TimeSpan.FromMilliseconds(500)
            };
    
            // Create conversation session options with function tools
            var sessionOptions = new VoiceLiveSessionOptions
            {
                Model = _model,
                Instructions = _instructions,
                Voice = azureVoice,
                InputAudioFormat = InputAudioFormat.Pcm16,
                OutputAudioFormat = OutputAudioFormat.Pcm16,
                TurnDetection = turnDetectionConfig
            };
    
            // Ensure modalities include audio
            sessionOptions.Modalities.Clear();
            sessionOptions.Modalities.Add(InputModality.Text);
            sessionOptions.Modalities.Add(InputModality.Audio);
    
            // Add function tools for customer service operations
            sessionOptions.Tools.Add(CreateCheckOrderStatusTool());
            sessionOptions.Tools.Add(CreateGetCustomerInfoTool());
            sessionOptions.Tools.Add(CreateScheduleSupportCallTool());
            sessionOptions.Tools.Add(CreateInitiateReturnProcessTool());
            sessionOptions.Tools.Add(CreateUpdateShippingAddressTool());
    
    
            await _session!.ConfigureSessionAsync(sessionOptions, cancellationToken).ConfigureAwait(false);
    
            _logger.LogInformation("Session configuration sent with {ToolCount} customer service tools", sessionOptions.Tools.Count);
        }
    
        /// <summary>
        /// Create the check order status function tool.
        /// </summary>
        private VoiceLiveFunctionDefinition CreateCheckOrderStatusTool()
        {
            var parameters = new
            {
                type = "object",
                properties = new
                {
                    order_number = new
                    {
                        type = "string",
                        description = "The customer's order number (required)"
                    },
                    email = new
                    {
                        type = "string",
                        description = "Customer's email address if order number is not available"
                    }
                },
                required = new[] { "order_number" }
            };
    
            return new VoiceLiveFunctionDefinition("check_order_status")
            {
                Description = "Check the status of a customer order by order number or email. Use this when customers ask about their order status, shipping, or delivery information.",
                Parameters = BinaryData.FromObjectAsJson(parameters)
            };
        }
    
        /// <summary>
        /// Create the get customer info function tool.
        /// </summary>
        private VoiceLiveFunctionDefinition CreateGetCustomerInfoTool()
        {
            var parameters = new
            {
                type = "object",
                properties = new
                {
                    customer_id = new
                    {
                        type = "string",
                        description = "Customer ID or email address to look up"
                    },
                    include_history = new
                    {
                        type = "boolean",
                        description = "Whether to include recent purchase history in the response",
                        @default = false
                    }
                },
                required = new[] { "customer_id" }
            };
    
            return new VoiceLiveFunctionDefinition("get_customer_info")
            {
                Description = "Retrieve customer account information and optionally their purchase history. Use this when customers ask about their account details or past orders.",
                Parameters = BinaryData.FromObjectAsJson(parameters)
            };
        }
    
        /// <summary>
        /// Create the schedule support call function tool.
        /// </summary>
        private VoiceLiveFunctionDefinition CreateScheduleSupportCallTool()
        {
            var parameters = new
            {
                type = "object",
                properties = new
                {
                    customer_id = new
                    {
                        type = "string",
                        description = "Customer identifier (ID or email)"
                    },
                    preferred_time = new
                    {
                        type = "string",
                        description = "Preferred call time in ISO format (optional)"
                    },
                    issue_category = new
                    {
                        type = "string",
                        @enum = new[] { "technical", "billing", "warranty", "returns" },
                        description = "Category of the support issue"
                    },
                    urgency = new
                    {
                        type = "string",
                        @enum = new[] { "low", "medium", "high", "critical" },
                        description = "Urgency level of the issue",
                        @default = "medium"
                    },
                    description = new
                    {
                        type = "string",
                        description = "Brief description of the issue the customer needs help with"
                    }
                },
                required = new[] { "customer_id", "issue_category", "description" }
            };
    
            return new VoiceLiveFunctionDefinition("schedule_support_call")
            {
                Description = "Schedule a technical support call with a specialist. Use this when customers need to speak with a technical expert about complex issues.",
                Parameters = BinaryData.FromObjectAsJson(parameters)
            };
        }
    
        /// <summary>
        /// Create the initiate return process function tool.
        /// </summary>
        private VoiceLiveFunctionDefinition CreateInitiateReturnProcessTool()
        {
            var parameters = new
            {
                type = "object",
                properties = new
                {
                    order_number = new
                    {
                        type = "string",
                        description = "Original order number for the return"
                    },
                    product_id = new
                    {
                        type = "string",
                        description = "Specific product ID to return from the order"
                    },
                    reason = new
                    {
                        type = "string",
                        @enum = new[] { "defective", "wrong_item", "not_satisfied", "damaged_shipping" },
                        description = "Reason for the return"
                    },
                    return_type = new
                    {
                        type = "string",
                        @enum = new[] { "refund", "exchange", "store_credit" },
                        description = "Type of return requested by the customer"
                    }
                },
                required = new[] { "order_number", "product_id", "reason", "return_type" }
            };
    
            return new VoiceLiveFunctionDefinition("initiate_return_process")
            {
                Description = "Start the return/exchange process for a product. Use this when customers want to return or exchange items they've purchased.",
                Parameters = BinaryData.FromObjectAsJson(parameters)
            };
        }
    
        /// <summary>
        /// Create the update shipping address function tool.
        /// </summary>
        private VoiceLiveFunctionDefinition CreateUpdateShippingAddressTool()
        {
            var parameters = new
            {
                type = "object",
                properties = new
                {
                    order_number = new
                    {
                        type = "string",
                        description = "Order number to update the shipping address for"
                    },
                    new_address = new
                    {
                        type = "object",
                        properties = new
                        {
                            street = new { type = "string", description = "Street address" },
                            city = new { type = "string", description = "City name" },
                            state = new { type = "string", description = "State or province" },
                            zip_code = new { type = "string", description = "ZIP or postal code" },
                            country_region = new { type = "string", description = "Country/region code", @default = "US" }
                        },
                        required = new[] { "street", "city", "state", "zip_code" },
                        description = "New shipping address information"
                    }
                },
                required = new[] { "order_number", "new_address" }
            };
    
            return new VoiceLiveFunctionDefinition("update_shipping_address")
            {
                Description = "Update shipping address for pending orders. Use this when customers need to change where their order will be delivered.",
                Parameters = BinaryData.FromObjectAsJson(parameters)
            };
        }
    
        /// <summary>
        /// Process events from the VoiceLive session.
        /// </summary>
        private async Task ProcessEventsAsync(CancellationToken cancellationToken)
        {
            try
            {
                await foreach (SessionUpdate serverEvent in _session!.GetUpdatesAsync(cancellationToken).ConfigureAwait(false))
                {
                    await HandleSessionUpdateAsync(serverEvent, cancellationToken).ConfigureAwait(false);
                }
            }
            catch (OperationCanceledException)
            {
                _logger.LogInformation("Event processing cancelled");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing events");
                throw;
            }
        }
    
        /// <summary>
        /// Handle different types of server events from VoiceLive.
        /// </summary>
        private async Task HandleSessionUpdateAsync(SessionUpdate serverEvent, CancellationToken cancellationToken)
        {
            _logger.LogDebug("Received event: {EventType}", serverEvent.GetType().Name);
    
            switch (serverEvent)
            {
                case SessionUpdateSessionCreated sessionCreated:
                    await HandleSessionCreatedAsync(sessionCreated, cancellationToken).ConfigureAwait(false);
                    break;
    
                case SessionUpdateSessionUpdated sessionUpdated:
                    _logger.LogInformation("Session updated successfully with function tools");
    
                    // Start audio capture once session is ready
                    if (_audioProcessor != null)
                    {
                        await _audioProcessor.StartCaptureAsync().ConfigureAwait(false);
                    }
                    break;
    
                case SessionUpdateInputAudioBufferSpeechStarted speechStarted:
                    _logger.LogInformation("🎤 Customer started speaking - stopping playback");
                    Console.WriteLine("🎤 Listening...");
    
                    // Stop current assistant audio playback (interruption handling)
                    if (_audioProcessor != null)
                    {
                        await _audioProcessor.StopPlaybackAsync().ConfigureAwait(false);
                    }
    
                    // Cancel any ongoing response
                    try
                    {
                        await _session!.CancelResponseAsync(cancellationToken).ConfigureAwait(false);
                    }
                    catch (Exception ex)
                    {
                        _logger.LogDebug(ex, "No response to cancel");
                    }
                    break;
    
                case SessionUpdateInputAudioBufferSpeechStopped speechStopped:
                    _logger.LogInformation("🎤 Customer stopped speaking");
                    Console.WriteLine("🤔 Processing...");
    
                    // Restart playback system for response
                    if (_audioProcessor != null)
                    {
                        await _audioProcessor.StartPlaybackAsync().ConfigureAwait(false);
                    }
                    break;
    
                case SessionUpdateResponseCreated responseCreated:
                    _logger.LogInformation("🤖 Assistant response created");
                    break;
    
                case SessionUpdateResponseOutputItemAdded outputItemAdded:
                    await HandleResponseOutputItemAddedAsync(outputItemAdded, cancellationToken).ConfigureAwait(false);
                    break;
    
                case SessionUpdateResponseAudioDelta audioDelta:
                    // Stream audio response to speakers
                    _logger.LogDebug("Received audio delta");
    
                    if (audioDelta.Delta != null && _audioProcessor != null)
                    {
                        byte[] audioData = audioDelta.Delta.ToArray();
                        await _audioProcessor.QueueAudioAsync(audioData).ConfigureAwait(false);
                    }
                    break;
    
                case SessionUpdateResponseAudioDone audioDone:
                    _logger.LogInformation("🤖 Assistant finished speaking");
                    Console.WriteLine("🎤 Ready for next customer inquiry...");
                    break;
    
                case SessionUpdateResponseContentPartAdded partAdded:
                    if (_assistantMessageItems.Contains(partAdded.ItemId))
                    {
                        _assistantMessageResponses.Add(partAdded.ResponseId);
                    }
    
                    break;
                case SessionUpdateResponseDone responseDone:
                    _logger.LogInformation("✅ Response complete");
                    break;
                case SessionUpdateResponseFunctionCallArgumentsDone functionCallArgumentsDone:
                    _logger.LogInformation("🔧 Function call arguments done for call ID: {CallId}", functionCallArgumentsDone.CallId);
                    await HandleFunctionCallAsync(functionCallArgumentsDone.Name, functionCallArgumentsDone.CallId, functionCallArgumentsDone.Arguments, cancellationToken).ConfigureAwait(false);
                    break;
                case SessionUpdateResponseAudioTranscriptDelta transcriptDelta:
                    // For now, only deal with the assistant responses.
                    if (_assistantMessageResponses.Contains(transcriptDelta.ResponseId))
                    {
                        Console.Write($"{transcriptDelta.Delta}");
                    }
                    break;
    
                case SessionUpdateResponseAudioTranscriptDone transcriptDone:
                    // For now, only deal with the assistant responses.
                    if (_assistantMessageResponses.Contains(transcriptDone.ResponseId))
                    {
                        Console.WriteLine();
                    }
                    break;
                case SessionUpdateError errorEvent:
                    _logger.LogError("❌ VoiceLive error: {ErrorMessage}", errorEvent.Error?.Message);
                    Console.WriteLine($"Error: {errorEvent.Error?.Message}");
                    break;
    
                default:
                    _logger.LogDebug("Unhandled event type: {EventType}", serverEvent.GetType().Name);
                    break;
            }
        }
    
        /// <summary>
        /// Handle response output item added events, including function calls.
        /// </summary>
        private async Task HandleResponseOutputItemAddedAsync(SessionUpdateResponseOutputItemAdded outputItemAdded, CancellationToken cancellationToken)
        {
            if (outputItemAdded.Item is ResponseFunctionCallItem item)
            {
                // This is a function call item, extract the details
                var functionName = item.Name;
                var callId = item.CallId;
                var arguments = item.Arguments;
    
                if (!string.IsNullOrEmpty(functionName) && !string.IsNullOrEmpty(callId) && !string.IsNullOrEmpty(arguments))
                {
                    await HandleFunctionCallAsync(functionName, callId, arguments, cancellationToken).ConfigureAwait(false);
                }
                else
                {
                    _logger.LogWarning("Function call item missing required properties: Name={Name}, CallId={CallId}, Arguments={Arguments}",
                        functionName, callId, arguments);
                }
            }
            else if (outputItemAdded.Item is ResponseMessageItem messageItem &&
                messageItem.Role == ResponseMessageRole.Assistant)
            {
                // Keep track of the items that are from the assistant, so we know how to display the conversation.
                _assistantMessageItems.Add(messageItem.Id);
            }
        }
    
        /// <summary>
        /// Handle function call execution and send results back to the session.
        /// </summary>
        private async Task HandleFunctionCallAsync(string functionName, string callId, string arguments, CancellationToken cancellationToken)
        {
            _logger.LogInformation("🔧 Executing function: {FunctionName}", functionName);
            Console.WriteLine($"🔧 Looking up {functionName.Replace("_", " ")}...");
    
            try
            {
                // Execute the function through our business logic layer
                var result = await _functions.ExecuteFunctionAsync(functionName, arguments, cancellationToken).ConfigureAwait(false);
    
                // Create function call output item using the model factory
                var outputItem = new FunctionCallOutputItem(callId, JsonSerializer.Serialize(result));
    
                // Add the result to the conversation
                await _session!.AddItemAsync(outputItem, cancellationToken).ConfigureAwait(false);
                await _session!.StartResponseAsync(cancellationToken).ConfigureAwait(false);
    
                _logger.LogInformation("✅ Function {FunctionName} completed successfully", functionName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Function {FunctionName} execution failed", functionName);
    
                // Send error response
                var errorResult = new { success = false, error = "I'm sorry, I'm having trouble accessing that information right now. Please try again in a moment." };
                var outputItem = new FunctionCallOutputItem(callId, JsonSerializer.Serialize(errorResult));
    
                await _session!.AddItemAsync(outputItem, cancellationToken).ConfigureAwait(false);
            }
        }
    
        /// <summary>
        /// Handle session created event.
        /// </summary>
        private async Task HandleSessionCreatedAsync(SessionUpdateSessionCreated sessionCreated, CancellationToken cancellationToken)
        {
            _logger.LogInformation("Session ready: {SessionId}", sessionCreated.Session?.Id);
    
            // Start audio capture once session is ready
            if (_audioProcessor != null)
            {
                await _audioProcessor.StartCaptureAsync().ConfigureAwait(false);
            }
        }
    
        /// <summary>
        /// Dispose of resources.
        /// </summary>
        public void Dispose()
        {
            if (_disposed)
                return;
    
            _audioProcessor?.Dispose();
            _session?.Dispose();
            _disposed = true;
        }
    }
    
    /// <summary>
    /// Handles real-time audio capture and playback for the voice assistant.
    /// </summary>
    /// <remarks>
    /// Threading Architecture:
    /// - Main thread: Event loop and UI
    /// - Capture thread: NAudio input stream reading
    /// - Send thread: Async audio data transmission to VoiceLive
    /// - Playback thread: NAudio output stream writing
    /// </remarks>
    public class AudioProcessor : IDisposable
    {
        private readonly VoiceLiveSession _session;
        private readonly ILogger<AudioProcessor> _logger;
    
        // Audio configuration - PCM16, 24kHz, mono as specified
        private const int SampleRate = 24000;
        private const int Channels = 1;
        private const int BitsPerSample = 16;
    
        // NAudio components
        private WaveInEvent? _waveIn;
        private WaveOutEvent? _waveOut;
        private BufferedWaveProvider? _playbackBuffer;
    
        // Audio capture and playback state
        private bool _isCapturing;
        private bool _isPlaying;
    
        // Audio streaming channels
        private readonly Channel<byte[]> _audioSendChannel;
        private readonly Channel<byte[]> _audioPlaybackChannel;
        private readonly ChannelWriter<byte[]> _audioSendWriter;
        private readonly ChannelReader<byte[]> _audioSendReader;
        private readonly ChannelWriter<byte[]> _audioPlaybackWriter;
        private readonly ChannelReader<byte[]> _audioPlaybackReader;
    
        // Background tasks
        private Task? _audioSendTask;
        private Task? _audioPlaybackTask;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private CancellationTokenSource _playbackCancellationTokenSource;
    
        /// <summary>
        /// Initializes a new instance of the AudioProcessor class.
        /// </summary>
        /// <param name="session">The VoiceLive session for audio communication.</param>
        /// <param name="logger">Logger for diagnostic information.</param>
        public AudioProcessor(VoiceLiveSession session, ILogger<AudioProcessor> logger)
        {
            _session = session ?? throw new ArgumentNullException(nameof(session));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    
            // Create unbounded channels for audio data
            _audioSendChannel = Channel.CreateUnbounded<byte[]>();
            _audioSendWriter = _audioSendChannel.Writer;
            _audioSendReader = _audioSendChannel.Reader;
    
            _audioPlaybackChannel = Channel.CreateUnbounded<byte[]>();
            _audioPlaybackWriter = _audioPlaybackChannel.Writer;
            _audioPlaybackReader = _audioPlaybackChannel.Reader;
    
            _cancellationTokenSource = new CancellationTokenSource();
            _playbackCancellationTokenSource = new CancellationTokenSource();
    
            _logger.LogInformation("AudioProcessor initialized with {SampleRate}Hz PCM16 mono audio", SampleRate);
        }
    
        /// <summary>
        /// Start capturing audio from microphone.
        /// </summary>
        public Task StartCaptureAsync()
        {
            if (_isCapturing)
                return Task.CompletedTask;
    
            _isCapturing = true;
    
            try
            {
                _waveIn = new WaveInEvent
                {
                    WaveFormat = new WaveFormat(SampleRate, BitsPerSample, Channels),
                    BufferMilliseconds = 50 // 50ms buffer for low latency
                };
    
                _waveIn.DataAvailable += OnAudioDataAvailable;
                _waveIn.RecordingStopped += OnRecordingStopped;
    
                /*
                _logger.LogInformation($"There are {WaveIn.DeviceCount} devices available.");
                for (int i = 0; i < WaveIn.DeviceCount; i++)
                {
                    var deviceInfo = WaveIn.GetCapabilities(i);
    
                    _logger.LogInformation($"{i}: {deviceInfo.ProductName}");
                }
                */
                _waveIn.DeviceNumber = 0; // Default to first device
    
                _waveIn.StartRecording();
    
                // Start audio send task
                _audioSendTask = ProcessAudioSendAsync(_cancellationTokenSource.Token);
    
                _logger.LogInformation("Started audio capture");
                return Task.CompletedTask;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to start audio capture");
                _isCapturing = false;
                throw;
            }
        }
    
        /// <summary>
        /// Stop capturing audio.
        /// </summary>
        public async Task StopCaptureAsync()
        {
            if (!_isCapturing)
                return;
    
            _isCapturing = false;
    
            if (_waveIn != null)
            {
                _waveIn.StopRecording();
                _waveIn.DataAvailable -= OnAudioDataAvailable;
                _waveIn.RecordingStopped -= OnRecordingStopped;
                _waveIn.Dispose();
                _waveIn = null;
            }
    
            // Complete the send channel and wait for the send task
            _audioSendWriter.TryComplete();
            if (_audioSendTask != null)
            {
                await _audioSendTask.ConfigureAwait(false);
                _audioSendTask = null;
            }
    
            _logger.LogInformation("Stopped audio capture");
        }
    
        /// <summary>
        /// Initialize audio playback system.
        /// </summary>
        public Task StartPlaybackAsync()
        {
            if (_isPlaying)
                return Task.CompletedTask;
    
            _isPlaying = true;
    
            try
            {
                _waveOut = new WaveOutEvent
                {
                    DesiredLatency = 100 // 100ms latency
                };
    
                _playbackBuffer = new BufferedWaveProvider(new WaveFormat(SampleRate, BitsPerSample, Channels))
                {
                    BufferDuration = TimeSpan.FromMinutes(5), // 5 second buffer
                    DiscardOnBufferOverflow = true
                };
    
                _waveOut.Init(_playbackBuffer);
                _waveOut.Play();
    
                _playbackCancellationTokenSource = new CancellationTokenSource();
    
                // Start audio playback task
                _audioPlaybackTask = ProcessAudioPlaybackAsync();
    
                _logger.LogInformation("Audio playback system ready");
                return Task.CompletedTask;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to initialize audio playback");
                _isPlaying = false;
                throw;
            }
        }
    
        /// <summary>
        /// Stop audio playback and clear buffer.
        /// </summary>
        public async Task StopPlaybackAsync()
        {
            if (!_isPlaying)
                return;
    
            _isPlaying = false;
    
            // Clear the playback channel
            while (_audioPlaybackReader.TryRead(out _))
            { }
    
            if (_playbackBuffer != null)
            {
                _playbackBuffer.ClearBuffer();
            }
    
            if (_waveOut != null)
            {
                _waveOut.Stop();
                _waveOut.Dispose();
                _waveOut = null;
            }
    
            _playbackBuffer = null;
    
            // Complete the playback channel and wait for the playback task
            _playbackCancellationTokenSource.Cancel();
    
            if (_audioPlaybackTask != null)
            {
                await _audioPlaybackTask.ConfigureAwait(false);
                _audioPlaybackTask = null;
            }
    
            _logger.LogInformation("Stopped audio playback");
        }
    
        /// <summary>
        /// Queue audio data for playback.
        /// </summary>
        /// <param name="audioData">The audio data to queue.</param>
        public async Task QueueAudioAsync(byte[] audioData)
        {
            if (_isPlaying && audioData.Length > 0)
            {
                await _audioPlaybackWriter.WriteAsync(audioData).ConfigureAwait(false);
            }
        }
    
        /// <summary>
        /// Event handler for audio data available from microphone.
        /// </summary>
        private void OnAudioDataAvailable(object? sender, WaveInEventArgs e)
        {
            if (_isCapturing && e.BytesRecorded > 0)
            {
                byte[] audioData = new byte[e.BytesRecorded];
                Array.Copy(e.Buffer, 0, audioData, 0, e.BytesRecorded);
    
                // Queue audio data for sending (non-blocking)
                if (!_audioSendWriter.TryWrite(audioData))
                {
                    _logger.LogWarning("Failed to queue audio data for sending - channel may be full");
                }
            }
        }
    
        /// <summary>
        /// Event handler for recording stopped.
        /// </summary>
        private void OnRecordingStopped(object? sender, StoppedEventArgs e)
        {
            if (e.Exception != null)
            {
                _logger.LogError(e.Exception, "Audio recording stopped due to error");
            }
        }
    
        /// <summary>
        /// Background task to process audio data and send to VoiceLive service.
        /// </summary>
        private async Task ProcessAudioSendAsync(CancellationToken cancellationToken)
        {
            try
            {
                await foreach (byte[] audioData in _audioSendReader.ReadAllAsync(cancellationToken).ConfigureAwait(false))
                {
                    if (cancellationToken.IsCancellationRequested)
                        break;
    
                    try
                    {
                        // Send audio data directly to the session
                        await _session.SendInputAudioAsync(audioData, cancellationToken).ConfigureAwait(false);
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, "Error sending audio data to VoiceLive");
                        // Continue processing other audio data
                    }
                }
            }
            catch (OperationCanceledException)
            {
                // Expected when cancellation is requested
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in audio send processing");
            }
        }
    
        /// <summary>
        /// Background task to process audio playback.
        /// </summary>
        private async Task ProcessAudioPlaybackAsync()
        {
            try
            {
                CancellationTokenSource combinedTokenSource = CancellationTokenSource.CreateLinkedTokenSource(_playbackCancellationTokenSource.Token, _cancellationTokenSource.Token);
                var cancellationToken = combinedTokenSource.Token;
    
                await foreach (byte[] audioData in _audioPlaybackReader.ReadAllAsync(cancellationToken).ConfigureAwait(false))
                {
                    if (cancellationToken.IsCancellationRequested)
                        break;
    
                    try
                    {
                        if (_playbackBuffer != null && _isPlaying)
                        {
                            _playbackBuffer.AddSamples(audioData, 0, audioData.Length);
                        }
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, "Error in audio playback");
                        // Continue processing other audio data
                    }
                }
            }
            catch (OperationCanceledException)
            {
                // Expected when cancellation is requested
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in audio playback processing");
            }
        }
    
        /// <summary>
        /// Clean up audio resources.
        /// </summary>
        public async Task CleanupAsync()
        {
            await StopCaptureAsync().ConfigureAwait(false);
            await StopPlaybackAsync().ConfigureAwait(false);
    
            _cancellationTokenSource.Cancel();
    
            // Wait for background tasks to complete
            var tasks = new List<Task>();
            if (_audioSendTask != null)
                tasks.Add(_audioSendTask);
            if (_audioPlaybackTask != null)
                tasks.Add(_audioPlaybackTask);
    
            if (tasks.Count > 0)
            {
                await Task.WhenAll(tasks).ConfigureAwait(false);
            }
    
            _logger.LogInformation("Audio processor cleaned up");
        }
    
        /// <summary>
        /// Dispose of resources.
        /// </summary>
        public void Dispose()
        {
            CleanupAsync().Wait();
            _cancellationTokenSource.Dispose();
        }
    }
    
    public class SampleProgram
    {
        /// <summary>
        /// Main entry point for the customer service bot sample.
        /// </summary>
        /// <param name="args"></param>
        /// <returns></returns>
        public static async Task<int> Main(string[] args)
        {
            // Create command line interface
            var rootCommand = CreateRootCommand();
            return await rootCommand.InvokeAsync(args).ConfigureAwait(false);
        }
    
        private static RootCommand CreateRootCommand()
        {
            var rootCommand = new RootCommand("Customer Service Bot using Azure VoiceLive SDK with Function Calling");
    
            var apiKeyOption = new Option<string?>(
                "--api-key",
                "Azure VoiceLive API key. If not provided, will use AZURE_VOICELIVE_API_KEY environment variable.");
    
            var endpointOption = new Option<string>(
                "--endpoint",
                () => "wss://api.voicelive.com/v1",
                "Azure VoiceLive endpoint");
    
            var modelOption = new Option<string>(
                "--model",
                () => "gpt-realtime",
                "VoiceLive model to use");
    
            var voiceOption = new Option<string>(
                "--voice",
                () => "en-US-Ava:DragonHDLatestNeural",
                "Voice to use for the customer service bot");
    
            var instructionsOption = new Option<string>(
                "--instructions",
                () => "You are a professional customer service representative for TechCorp. You have access to customer databases and order systems. Always be polite, helpful, and efficient. When customers ask about orders, accounts, or need to schedule service, use the available tools to provide accurate, real-time information. Keep your responses concise but thorough.",
                "System instructions for the customer service bot");
    
            var useTokenCredentialOption = new Option<bool>(
                "--use-token-credential",
                "Use Azure token credential instead of API key");
    
            var verboseOption = new Option<bool>(
                "--verbose",
                "Enable verbose logging");
    
            rootCommand.AddOption(apiKeyOption);
            rootCommand.AddOption(endpointOption);
            rootCommand.AddOption(modelOption);
            rootCommand.AddOption(voiceOption);
            rootCommand.AddOption(instructionsOption);
            rootCommand.AddOption(useTokenCredentialOption);
            rootCommand.AddOption(verboseOption);
    
            rootCommand.SetHandler(async (
                string? apiKey,
                string endpoint,
                string model,
                string voice,
                string instructions,
                bool useTokenCredential,
                bool verbose) =>
            {
                await RunCustomerServiceBotAsync(apiKey, endpoint, model, voice, instructions, useTokenCredential, verbose).ConfigureAwait(false);
            },
            apiKeyOption,
            endpointOption,
            modelOption,
            voiceOption,
            instructionsOption,
            useTokenCredentialOption,
            verboseOption);
    
            return rootCommand;
        }
    
        private static async Task RunCustomerServiceBotAsync(
            string? apiKey,
            string endpoint,
            string model,
            string voice,
            string instructions,
            bool useTokenCredential,
            bool verbose)
        {
            // Setup configuration
            var configuration = new ConfigurationBuilder()
                .AddJsonFile("appsettings.json", optional: true)
                .AddEnvironmentVariables()
                .Build();
    
            // Override with command line values if provided
            apiKey ??= configuration["VoiceLive:ApiKey"] ?? Environment.GetEnvironmentVariable("AZURE_VOICELIVE_API_KEY");
            endpoint = configuration["VoiceLive:Endpoint"] ?? endpoint;
            model = configuration["VoiceLive:Model"] ?? model;
            voice = configuration["VoiceLive:Voice"] ?? voice;
            instructions = configuration["VoiceLive:Instructions"] ?? instructions;
    
            // Setup logging
            using var loggerFactory = LoggerFactory.Create(builder =>
            {
                builder.AddConsole();
                if (verbose)
                {
                    builder.SetMinimumLevel(LogLevel.Debug);
                }
                else
                {
                    builder.SetMinimumLevel(LogLevel.Information);
                }
            });
    
            var logger = loggerFactory.CreateLogger<SampleProgram>();
    
            // Validate credentials
            if (string.IsNullOrEmpty(apiKey) && !useTokenCredential)
            {
                Console.WriteLine("❌ Error: No authentication provided");
                Console.WriteLine("Please provide an API key using --api-key or set AZURE_VOICELIVE_API_KEY environment variable,");
                Console.WriteLine("or use --use-token-credential for Azure authentication.");
                return;
            }
    
            // Check audio system before starting
            if (!CheckAudioSystem(logger))
            {
                return;
            }
    
            try
            {
                // Create client with appropriate credential
                VoiceLiveClient client;
                if (useTokenCredential)
                {
                    var tokenCredential = new DefaultAzureCredential();
                    client = new VoiceLiveClient(new Uri(endpoint), tokenCredential, new VoiceLiveClientOptions());
                    logger.LogInformation("Using Azure token credential");
                }
                else
                {
                    var keyCredential = new Azure.AzureKeyCredential(apiKey!);
                    client = new VoiceLiveClient(new Uri(endpoint), keyCredential, new VoiceLiveClientOptions());
                    logger.LogInformation("Using API key credential");
                }
    
                // Create customer service functions implementation
                var functions = new CustomerServiceFunctions(loggerFactory.CreateLogger<CustomerServiceFunctions>());
    
                // Create and start customer service bot
                using var bot = new CustomerServiceBot(
                    client,
                    model,
                    voice,
                    instructions,
                    functions,
                    loggerFactory);
    
                // Setup cancellation token for graceful shutdown
                using var cancellationTokenSource = new CancellationTokenSource();
                Console.CancelKeyPress += (sender, e) =>
                {
                    e.Cancel = true;
                    logger.LogInformation("Received shutdown signal");
                    cancellationTokenSource.Cancel();
                };
    
                // Display welcome message
                DisplayWelcomeMessage();
    
                // Start the customer service bot
                await bot.StartAsync(cancellationTokenSource.Token).ConfigureAwait(false);
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("\n👋 Customer service bot shut down. Thank you for using TechCorp support!");
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Fatal error");
                Console.WriteLine($"❌ Error: {ex.Message}");
            }
        }
    
        private static void DisplayWelcomeMessage()
        {
            Console.WriteLine();
            Console.WriteLine("🏢 Welcome to TechCorp Customer Service");
            Console.WriteLine("======================================");
            Console.WriteLine();
            Console.WriteLine("I can help you with:");
            Console.WriteLine("• 📦 Order status and tracking");
            Console.WriteLine("• 👤 Account information and history");
            Console.WriteLine("• 🔄 Returns and exchanges");
            Console.WriteLine("• 📞 Scheduling technical support calls");
            Console.WriteLine("• 🚚 Updating shipping addresses");
            Console.WriteLine();
            Console.WriteLine("Sample data available:");
            Console.WriteLine("• Orders: ORD-2024-001, ORD-2024-002, ORD-2024-003");
            Console.WriteLine("• Customers: john.smith@email.com, sarah.johnson@email.com");
            Console.WriteLine("• Products: LAPTOP-001, MOUSE-001, MONITOR-001");
            Console.WriteLine();
            Console.WriteLine("Try saying things like:");
            Console.WriteLine("• \"What's the status of order ORD-2024-001?\"");
            Console.WriteLine("• \"I need to return a defective laptop\"");
            Console.WriteLine("• \"Can you look up my account info for john.smith@email.com?\"");
            Console.WriteLine("• \"I need to schedule a technical support call\"");
            Console.WriteLine();
        }
    
        private static bool CheckAudioSystem(ILogger logger)
        {
            try
            {
                // Try input (default device)
                using (var waveIn = new WaveInEvent
                {
                    WaveFormat = new WaveFormat(24000, 16, 1),
                    BufferMilliseconds = 50
                })
                {
                    // Start/Stop to force initialization and surface any device errors
                    waveIn.DataAvailable += (_, __) => { };
                    waveIn.StartRecording();
                    waveIn.StopRecording();
                }
    
                // Try output (default device)
                var buffer = new BufferedWaveProvider(new WaveFormat(24000, 16, 1))
                {
                    BufferDuration = TimeSpan.FromMilliseconds(200)
                };
    
                using (var waveOut = new WaveOutEvent { DesiredLatency = 100 })
                {
                    waveOut.Init(buffer);
                    // Playing isn’t strictly required to validate a device, but it’s safe
                    waveOut.Play();
                    waveOut.Stop();
                }
    
                logger.LogInformation("Audio system check passed (default input/output initialized).");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Audio system check failed: {ex.Message}");
                return false;
            }
        }
    }

    ```

1. Run your console application to start the live conversation:

   ```dotnetcli
   dotnet run
   ```

## Output

The output of the script is printed to the console. You see messages indicating the status of the connection, audio stream, and playback. The audio is played back through your speakers or headphones.

```console
info: SampleProgram[0]
      Audio system check passed (default input/output initialized).
info: SampleProgram[0]
      Using API key credential

� Welcome to TechCorp Customer Service
======================================

I can help you with:
• � Order status and tracking
• � Account information and history
• � Returns and exchanges
• � Scheduling technical support calls
• � Updating shipping addresses

Sample data available:
• Orders: ORD-2024-001, ORD-2024-002, ORD-2024-003
• Customers: john.smith@email.com, sarah.johnson@email.com
• Products: LAPTOP-001, MOUSE-001, MONITOR-001

Try saying things like:
• "What's the status of order ORD-2024-001?"
• "I need to return a defective laptop"
• "Can you look up my account info for john.smith@email.com?"
• "I need to schedule a technical support call"

info: CustomerServiceBot[0]
      Connecting to VoiceLive API with model gpt-4o
info: AudioProcessor[0]
      AudioProcessor initialized with 24000Hz PCM16 mono audio
info: CustomerServiceBot[0]
      Setting up customer service session with function calling...
info: CustomerServiceBot[0]
      Session configuration sent with 5 customer service tools
info: AudioProcessor[0]
      Audio playback system ready

======================================================================
� CUSTOMER SERVICE BOT READY
I can help you with orders, returns, account info, and scheduling support calls
Start speaking to begin your customer service session
Press Ctrl+C to exit
======================================================================

info: AudioProcessor[0]
      Started audio capture
info: CustomerServiceBot[0]
      Customer service bot ready! Start speaking...
info: CustomerServiceBot[0]
      Session ready: sess_2Ti2YGckoXIN71yMJMW265
info: CustomerServiceBot[0]
      Session updated successfully with function tools
� Listening...
info: CustomerServiceBot[0]
      � Customer started speaking - stopping playback
info: AudioProcessor[0]
      Stopped audio playback
```