// This is a RAG (Retrieval Augmented Generation) implementation that:
// 1. Takes a user query about hotels
// 2. Searches a hotel database using Azure AI Search
// 3. Formats the search results for the LLM
// 4. Sends the query and formatted results to Azure OpenAI
// 5. Returns a grounded response based only on the retrieved information

import { SearchClient, AzureKeyCredential, SearchDocumentsResult } from "@azure/search-documents";
import { AzureOpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

function getClients(): { openaiClient: AzureOpenAI, searchClient: SearchClient<{ HotelName: string; Description: string; Tags: string[] | string }>, modelName: string }  {

    const credential = new DefaultAzureCredential();

    // Search
    const azureSearchEndpoint = process.env.AZURE_SEARCH_ENDPOINT!;
    const azureSearchIndexName = process.env.AZURE_SEARCH_INDEX_NAME!;

    const searchClient = new SearchClient<{ HotelName: string; Description: string; Tags: string[] | string }>(
        azureSearchEndpoint,
        azureSearchIndexName,
        credential
    );


    // OpenAI
    const azureOpenAiEndpoint = process.env.AZURE_OPENAI_ENDPOINT!;
    const azureOpenAiApiVersion = process.env.AZURE_OPENAI_VERSION!;
    const azureOpenAiDeploymentName = process.env.AZURE_DEPLOYMENT_MODEL!;

    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);
    const options = { azureADTokenProvider, deployment: azureOpenAiDeploymentName, apiVersion: azureOpenAiApiVersion, endpoint: azureOpenAiEndpoint }
    const openaiClient = new AzureOpenAI(options);

    return { openaiClient, searchClient, modelName: azureOpenAiDeploymentName };
}

async function queryAISearchForSources(searchClient: SearchClient<{ HotelName: string; Description: string; Tags: string[] | string }>, query: string): Promise<string> {
    console.log(`Searching for: "${query}"\n`);
    const searchResults: SearchDocumentsResult<{ HotelName: string; Description: string; Tags: string[] | string }> = await searchClient.search(query, {
        top: 5,
        select: ["Description", "HotelName", "Tags"]
    });

    const sources: string[] = [];
    for await (const result of searchResults.results) {
        const doc = result.document;
        sources.push(
            `Hotel: ${doc.HotelName}\n` +
            `Description: ${doc.Description}\n` +
            `Tags: ${Array.isArray(doc.Tags) ? doc.Tags.join(', ') : doc.Tags}\n`
        );
    }
    const sourcesFormatted = sources.join("\n---\n");
    return sourcesFormatted;
}
async function queryOpenAIForResponse(
    openaiClient: AzureOpenAI, 
    query: string, 
    sourcesFormatted: string, 
    modelName: string
): Promise<{ choices: { message: { content: string | null } }[] }> {

    const GROUNDED_PROMPT = `
 You are a friendly assistant that recommends hotels based on activities and amenities.
 Answer the query using only the sources provided below in a friendly and concise bulleted manner.
 Answer ONLY with the facts listed in the list of sources below.
 If there isn't enough information below, say you don't know.
 Do not generate answers that don't use the sources below.

Query: {query}
Sources: {sources}
`;

    return openaiClient.chat.completions.create({
        model: modelName,
        messages: [
            {
                role: "user",
                content: GROUNDED_PROMPT.replace("{query}", query).replace("{sources}", sourcesFormatted),
            }
        ],
        temperature: 0.7,
        max_tokens: 800,
    });
}

async function main():Promise<void> {

    const { openaiClient, searchClient, modelName } = getClients();

    const query = "Can you recommend a few hotels with complimentary breakfast?";

    const sources = await queryAISearchForSources(searchClient, query);
    const response = await queryOpenAIForResponse(openaiClient, query, sources, modelName);

    // Print the response from the chat model
    const content = response.choices[0].message.content;
    if (content) {
        console.log(content);
    } else {
        console.log("No content available in the response.");
    }
}

main().catch((error) => {
    console.error("An error occurred:", error);
    process.exit(1);
});