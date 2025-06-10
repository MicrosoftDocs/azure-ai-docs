// This is a RAG (Retrieval Augmented Generation) implementation that:
// 1. Takes a user query about hotels
// 2. Searches a hotel database using Azure AI Search
// 3. Formats the search results for the LLM
// 4. Sends the query and formatted results to Azure OpenAI
// 5. Returns a grounded response based only on the retrieved information

import { SearchClient } from "@azure/search-documents";
import { AzureOpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

function getClients() {

    const credential = new DefaultAzureCredential();

    // Search
    const azureSearchEndpoint = process.env.AZURE_SEARCH_ENDPOINT;
    const azureSearchIndexName = process.env.AZURE_SEARCH_INDEX_NAME;

    const searchClient = new SearchClient(
        azureSearchEndpoint,
        azureSearchIndexName,
        credential
    );


    // OpenAI
    const azureOpenAiEndpoint = process.env.AZURE_OPENAI_ENDPOINT;
    const azureOpenAiApiVersion = process.env.AZURE_OPENAI_VERSION;
    const azureOpenAiDeploymentName = process.env.AZURE_DEPLOYMENT_MODEL;

    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);
    const options = { azureADTokenProvider, deployment: azureOpenAiDeploymentName, apiVersion: azureOpenAiApiVersion, endpoint: azureOpenAiEndpoint }
    const openaiClient = new AzureOpenAI(options);

    return { openaiClient, searchClient, modelName: azureOpenAiDeploymentName };
}

async function queryAISearchForSources(
    searchClient,
    query
) {
    console.log(`Searching for: "${query}"\n`);

    const selectedFields = ["HotelName", "Description", "Address", "Rooms", "Tags"];
    const searchResults = await searchClient.search(query, {
        top: 5,
        select: selectedFields,
        queryType: "semantic",
        semanticSearchOptions: {},
    });

    return searchResults;
}
async function queryOpenAIForResponse(
    openaiClient, 
    query, 
    sourcesFormatted, 
    modelName
){

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

async function main() {

    const { openaiClient, searchClient, modelName } = getClients();

    const query = `
    Can you recommend a few hotels that offer complimentary breakfast? 
    Tell me their description, address, tags, and the rate for one room that sleeps 4 people.
    `;

    const sourcesResult = await queryAISearchForSources(searchClient, query);
    let sourcesFormatted = "";

    for await (const result of sourcesResult.results) {
        // Explicitly typing result to ensure compatibility
        sourcesFormatted += JSON.stringify(result.document) + "\n";
    }

    const response = await queryOpenAIForResponse(openaiClient, query, sourcesFormatted.trim(), modelName);

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