---
title: "Quickstart: Use Azure OpenAI Service with PowerShell"
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with PowerShell.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mgreenegit
ms.author: migreene
ms.date: 3/21/2025
---

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- <a href="https://aka.ms/installpowershell" target="_blank">You can use either the latest version, PowerShell 7, or Windows PowerShell 5.1.</a>
- An Azure OpenAI Service resource with a model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).
- An Azure OpenAI Service resource with the `gpt-4o` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).


### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Create a new PowerShell script

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

    ```console
    az login
    ```

1. Create a new PowerShell file called *quickstart.ps1*. Then open it up in your preferred editor or IDE.

1. Replace the contents of *quickstart.ps1* with the following code. You need to set the `engine` variable to the deployment name you chose when you deployed the GPT-4o model. Entering the model name results in an error unless you chose a deployment name that is identical to the underlying model name.

    ```powershell-interactive
    # Azure OpenAI metadata variables
    $openai = @{
       api_base    = $Env:AZURE_OPENAI_ENDPOINT
       api_version = '2024-10-21' # This can change in the future.
       name        = 'gpt-4o' # The name you chose for your model deployment.
    }
    
    # Use the recommended keyless authentication via bearer token.
    $headers = [ordered]@{
        #'api-key' = $Env:AZURE_OPENAI_API_KEY
        'Authorization' = "Bearer $($Env:DEFAULT_AZURE_CREDENTIAL_TOKEN)"
    }
    
    # Completion text
    $messages = @()
    $messages += @{
      role = 'system'
      content = 'You are a helpful assistant.'
    }
    $messages += @{
      role = 'user'
      content = 'Can I use honey as a substitute for sugar?'
    }
    $messages += @{
      role = 'assistant'
      content = 'Yes, you can use honey as a substitute for sugar.'
    }
    $messages += @{
      role = 'user'
      content = 'What other ingredients can I use as a substitute for sugar?'
    }
    
    # Adjust these values to fine-tune completions
    $body = [ordered]@{
       messages = $messages
    } | ConvertTo-Json
    
    # Send a request to generate an answer
    $url = "$($openai.api_base)/openai/deployments/$($openai.name)/chat/completions?api-version=$($openai.api_version)"
    
    $response = Invoke-RestMethod -Uri $url -Headers $headers -Body $body -Method Post -ContentType 'application/json'
    return $response
   ```

   > [!IMPORTANT]
   > For production, use a secure way of storing and accessing your credentials like [The PowerShell Secret Management with Azure Key Vault](/powershell/utility-modules/secretmanagement/how-to/using-azure-keyvault). For more information about credential security, see this [security](../../security-features.md) article.

1. Run the script using PowerShell. In this example, we're using the `-Depth` parameter to ensure that the output isn't truncated. 

   ```powershell
   ./quickstart.ps1 | ConvertTo-Json -Depth 4
   ```

## Output

The output of the script is a JSON object that contains the response from the Azure OpenAI Service. The output looks similar to the following:

```json
{
  "choices": [
    {
      "content_filter_results": {
        "custom_blocklists": {
          "filtered": false
        },
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "protected_material_code": {
          "filtered": false,
          "detected": false
        },
        "protected_material_text": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "There are many alternatives to sugar that can be used in cooking and baking, depending on your dietary needs, taste preferences, and the type of recipe you're making. Here are some popular sugar substitutes:\n\n---\n\n### 1. **Natural Sweeteners**\n   - **Maple Syrup**: A natural sweetener with a rich, distinct flavor. Use about ¾ cup of maple syrup for every cup of sugar, and reduce the liquid in the recipe slightly.\n   - **Agave Nectar**: A liquid sweetener that’s sweeter than sugar. Use about ⅔ cup of agave nectar for each cup of sugar, and reduce the liquid in the recipe.\n   - **Coconut Sugar**: Made from the sap of the coconut palm, it has a mild caramel flavor. Substitute in a 1:1 ratio for sugar.\n   - **Molasses**: A by-product of sugar production, molasses is rich in flavor and best for recipes like gingerbread or barbecue sauce. Adjust quantities based on the recipe.\n   - **Stevia (Natural)**: Derived from the stevia plant, it's intensely sweet and available in liquid or powder form. Use sparingly, as a little goes a long way.\n\n---\n\n### 2. **Fruit-Based Sweeteners**\n   - **Ripe Bananas**: Mashed bananas work well for baking recipes like muffins or pancakes. Use about ½ cup of mashed banana for every cup of sugar and reduce the liquid slightly.\n   - **Applesauce**: Unsweetened applesauce adds sweetness and moisture to baked goods. Replace sugar in a 1:1 ratio, but reduce the liquid by ¼ cup.\n   - **Dates/Date Paste**: Blend dates with water to make a paste, which works well in recipes like energy bars, cakes, or smoothies. Use in a 1:1 ratio for sugar.\n   - **Fruit Juices (e.g., orange juice)**: Can be used to impart natural sweetness but is best suited for specific recipes like marinades or desserts.\n\n---\n\n### 3. **Artificial and Low-Calorie Sweeteners**\n   - **Erythritol**: A sugar alcohol with no calories. Substitute in equal amounts, but be careful as it may cause a cooling sensation in some recipes.\n   - **Xylitol**: Another sugar alcohol, often used in gum and candies. It’s a 1:1 sugar substitute but may affect digestion if consumed in large quantities.\n   - **Monk Fruit Sweetener**: A natural, calorie-free sweetener that’s significantly sweeter than sugar. Follow the product packaging for exact substitution measurements.\n   - **Aspartame, Sucralose, or Saccharin** (Artificial Sweeteners): Often used for calorie reduction in beverages or desserts. Follow package instructions for substitution.\n\n---\n\n### 4. **Other Natural Alternatives**\n   - **Brown Rice Syrup**: A sticky, malt-flavored syrup used in granolas or desserts. Substitute 1 ¼ cups of brown rice syrup for every cup of sugar.\n   - **Barley Malt Syrup**: A thick, dark syrup with a distinct flavor. It can replace sugar but might require recipe adjustments due to its strong taste.\n   - **Yacon Syrup**: Made from the root of the yacon plant, it’s similar in texture to molasses and has a mild sweetness.\n\n---\n\n### General Tips for Substituting Sugar:\n- **Adjust Liquids:** Many liquid sweeteners (like honey or maple syrup) require reducing the liquid in the recipe to maintain texture.\n- **Baking Powder Adjustment:** If replacing sugar with an acidic sweetener (e.g., honey or molasses), you might need to add a little baking soda to neutralize acidity.\n- **Flavor Changes:** Some substitutes, like molasses or coconut sugar, have distinct flavors that can influence the taste of your recipe.\n- **Browning:** Sugar contributes to caramelization and browning in baked goods. Some alternatives may yield lighter-colored results.\n\nBy trying out different substitutes, you can find what works best for your recipes!",
        "refusal": null,
        "role": "assistant"
      }
    }
  ],
  "created": 1742602230,
  "id": "chatcmpl-BDgjWjEboQ0z6r58pvSBgH842JbB2",
  "model": "gpt-4o-2024-11-20",
  "object": "chat.completion",
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "custom_blocklists": {
          "filtered": false
        },
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "system_fingerprint": "fp_a42ed5ff0c",
  "usage": {
    "completion_tokens": 836,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 0,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens": 60,
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    },
    "total_tokens": 896
  }
}
```


## Remarks

You can skip the `ConvertTo-Json` step if you want to see the raw output. 

```powershell
./quickstart.ps1
```

The output looks like this:

```shell
choices               : {@{content_filter_results=; finish_reason=stop; index=0; logprobs=; message=}}
created               : 1742602727
id                    : chatcmpl-BDgrX0BF38mZuszFeyU1NKZSiRpSX
model                 : gpt-4o-2024-11-20
object                : chat.completion
prompt_filter_results : {@{prompt_index=0; content_filter_results=}}
system_fingerprint    : fp_b705f0c291
usage                 : @{completion_tokens=944; completion_tokens_details=; prompt_tokens=60; prompt_tokens_details=; total_tokens=1004}
```

You can edit the contents of the *powershell.ps1* script to return the entire object or a specific property. For example, to return the text returned, you can replace the last line of the script (`return $response`) with the following:

```powershell
return $response.choices.message.content
```

Then run the script again. 

```powershell
./quickstart.ps1
```

The output looks like this:

```shell
There are several ingredients that can be used as substitutes for sugar, depending on the recipe and your dietary preferences. Here are some popular options:

---

### **Natural Sweeteners**
1. **Maple Syrup**
   - Flavor: Rich and slightly caramel-like.
   - Use: Works well in baking, sauces, oatmeal, and beverages.
   - Substitution: Replace sugar in a 1:1 ratio but reduce the liquid in your recipe by about 3 tablespoons per cup of maple syrup.

2. **Agave Nectar**
   - Flavor: Mildly sweet, less pronounced than honey.
   - Use: Good for beverages, desserts, and dressings.
   - Substitution: Use about 2/3 cup of agave nectar for every 1 cup of sugar, and reduce other liquids slightly.

3. **Molasses**
   - Flavor: Strong, earthy, and slightly bitter.
   - Use: Perfect for gingerbread, cookies, and marinades.
   - Substitution: Replace sugar in equal amounts, but adjust for the strong flavor.

4. **Date Paste**
   - Flavor: Naturally sweet with hints of caramel.
   - Use: Works well in energy bars, smoothies, or baking recipes.
   - Substitution: Blend pitted dates with water to create paste (about 1:1 ratio). Use equal amounts in recipes.

5. **Coconut Sugar**
   - Flavor: Similar to brown sugar, mildly caramel-like.
   - Use: Excellent for baking.
   - Substitution: Replace sugar in a 1:1 ratio.

---

### **Low-Calorie Sweeteners**
1. **Stevia**
   - Flavor: Very sweet but can have a slightly bitter aftertaste.
   - Use: Works in beverages, desserts, and some baked goods.
   - Substitution: Use less—around 1 teaspoon of liquid stevia or 1/2 teaspoon stevia powder for 1 cup of sugar. Check the package for exact conversion.

2. **Erythritol**
   - Flavor: Similar to sugar but less sweet.
   - Use: Perfect for baked goods and beverages.
   - Substitution: Replace sugar using a 1:1 ratio, though you may need to adjust for less sweetness.

3. **Xylitol**
   - Flavor: Similar to sugar.
   - Use: Great for baking or cooking but avoid using it for recipes requiring caramelization.
   - Substitution: Use a 1:1 ratio.

---

### **Fruit-Based Sweeteners**
1. **Mashed Bananas**
   - Flavor: Sweet with a fruity note.
   - Use: Great for muffins, cakes, and pancakes.
   - Substitution: Use 1 cup mashed banana for 1 cup sugar, but reduce liquid slightly in the recipe.

2. **Applesauce**
   - Flavor: Mildly sweet.
   - Use: Excellent for baked goods like muffins or cookies.
   - Substitution: Replace sugar 1:1, but reduce other liquids slightly.

3. **Fruit Juice Concentrates**
   - Flavor: Sweet with fruity undertones.
   - Use: Works well in marinades, sauces, and desserts.
   - Substitution: Use equal amounts, but adjust liquid content.

---

### **Minimal-Processing Sugars**
1. **Raw Honey**
   - Flavor: Sweet with floral undertones.
   - Use: Good for baked goods and beverages.
   - Substitution: Replace sugar in a 1:1 ratio, but reduce other liquids slightly.

2. **Brown Rice Syrup**
   - Flavor: Mildly sweet with a hint of nuttiness.
   - Use: Suitable for baked goods and granola bars.
   - Substitution: Use 1-1/4 cups of syrup for 1 cup of sugar, and decrease liquid in the recipe.

---

### Tips for Substitution:
- Adjust for sweetness: Some substitutes are sweeter or less sweet than sugar, so amounts may need tweaking.
- Baking considerations: Sugar affects texture, browning, and moisture. If you replace it, you may need to experiment to get the desired result.
- Liquid adjustments: Many natural sweeteners are liquid, so you’ll often need to reduce the amount of liquid in your recipe.

Would you like help deciding the best substitute for a specific recipe?
```

### Understanding the message structure

The GPT-4 models are optimized to work with inputs formatted as a conversation. The `messages` variable passes an array of dictionaries with different roles in the conversation delineated by system, user, and assistant. The system message can be used to prime the model by including context or instructions on how the model should respond.

The [GPT-4 how-to guide](../how-to/chatgpt.md) provides an in-depth introduction into the options for communicating with these models.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure PowerShell](../../multi-service-resource.md?pivots=azpowershell#clean-up-resources)

## Next steps

- Learn more about how to work with the GPT-4 models with [our how-to guide](../how-to/chatgpt.md).
- For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
