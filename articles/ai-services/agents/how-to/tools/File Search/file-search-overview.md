# Azure AI Agent Service file search overview

File search augments agents with knowledge from outside its model, such as proprietary product information or documents provided by your users.  

[New] With the improved file search tool, your files remain in your own storage, and your Azure AI Search resource is used to ingest them, ensuring you maintain complete control over your data.     

### File Sources  
- Upload local files 
- [Coming soon] Azure Blob Storage 


## Dependency on Agent Setup

### Basic Agent Setup
The file search tool has the same functionality as AOAI Assistants. Microsoft managed search and storage resources are used. 
- Uploaded files get stored in Microsoft managed storage 
- A vector store is created using a Microsoft managed search resource 

### Standard Agent Setup
The file search tool uses the Azure AI Search and Azure Blob Storage resources you connected during agent setup. 
- Uploaded files get stored in your connected Azure Blob Storage account 
- Vector stores get created using your connected Azure AI Search resource 
<br> </br>

For both Agent setups, OpenAI handles the entire ingestion process, including automatically parsing and chunking documents, generating and storing embeddings, and utilizing both vector and keyword searches to retrieve relevant content for user queries. 

There is no difference in the code between the two setups; the only variation is in where your files and created vector stores are stored. 

